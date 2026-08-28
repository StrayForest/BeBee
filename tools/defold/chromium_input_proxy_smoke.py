#!/usr/bin/env python3
"""Exercise BeBee's HTML5 input/proxy-focus contract through Chromium CDP.

The script intentionally uses only the Python standard library. It dispatches real
browser keyboard and touch events, observes Defold console markers, and proves that
modal input consumption stops delivery to the proxied gameplay listener and the
main-world proxy owner.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import socket
import struct
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path


class WebSocket:
    def __init__(self, url: str) -> None:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "ws":
            raise RuntimeError(f"Unsupported DevTools URL: {url}")
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 80
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query

        self.sock = socket.create_connection((host, port), timeout=5)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode("ascii"))
        response = self._read_http_headers()
        if not response.startswith("HTTP/1.1 101"):
            raise RuntimeError(f"DevTools WebSocket upgrade failed: {response!r}")

    def _read_http_headers(self) -> str:
        data = bytearray()
        while b"\r\n\r\n" not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            data.extend(chunk)
        return data.decode("latin1", errors="replace")

    @staticmethod
    def _read_exact(sock: socket.socket, size: int) -> bytes:
        data = bytearray()
        while len(data) < size:
            chunk = sock.recv(size - len(data))
            if not chunk:
                raise RuntimeError("DevTools WebSocket closed unexpectedly")
            data.extend(chunk)
        return bytes(data)

    def send_json(self, payload: dict) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        mask = os.urandom(4)
        first = 0x81
        length = len(body)
        if length < 126:
            header = bytes((first, 0x80 | length))
        elif length <= 0xFFFF:
            header = bytes((first, 0x80 | 126)) + struct.pack("!H", length)
        else:
            header = bytes((first, 0x80 | 127)) + struct.pack("!Q", length)
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(body))
        self.sock.sendall(header + mask + masked)

    def recv_json(self, timeout: float) -> dict:
        self.sock.settimeout(timeout)
        while True:
            first, second = self._read_exact(self.sock, 2)
            opcode = first & 0x0F
            length = second & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._read_exact(self.sock, 2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._read_exact(self.sock, 8))[0]
            masked = bool(second & 0x80)
            mask = self._read_exact(self.sock, 4) if masked else b""
            payload = self._read_exact(self.sock, length)
            if masked:
                payload = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
            if opcode == 0x9:
                self._send_control(0xA, payload)
                continue
            if opcode == 0x8:
                raise RuntimeError("DevTools WebSocket closed")
            if opcode != 0x1:
                continue
            return json.loads(payload.decode("utf-8"))

    def _send_control(self, opcode: int, payload: bytes) -> None:
        mask = os.urandom(4)
        header = bytes((0x80 | opcode, 0x80 | len(payload)))
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def close(self) -> None:
        self.sock.close()


class DevTools:
    def __init__(self, websocket_url: str) -> None:
        self.ws = WebSocket(websocket_url)
        self.next_id = 1
        self.console: list[str] = []
        self.runtime_exceptions: list[str] = []

    def _record(self, message: dict) -> None:
        method = message.get("method")
        params = message.get("params", {})
        if method == "Runtime.consoleAPICalled":
            values = []
            for item in params.get("args", []):
                value = item.get("value")
                if value is None:
                    value = item.get("description", "")
                values.append(str(value))
            if values:
                self.console.append(" ".join(values))
        elif method == "Log.entryAdded":
            text = params.get("entry", {}).get("text")
            if text:
                self.console.append(str(text))
        elif method == "Runtime.exceptionThrown":
            details = params.get("exceptionDetails", {})
            self.runtime_exceptions.append(str(details.get("text", "runtime exception")))

    def call(self, method: str, params: dict | None = None, timeout: float = 5) -> dict:
        command_id = self.next_id
        self.next_id += 1
        self.ws.send_json({"id": command_id, "method": method, "params": params or {}})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            message = self.ws.recv_json(max(0.05, deadline - time.monotonic()))
            self._record(message)
            if message.get("id") == command_id:
                if "error" in message:
                    raise RuntimeError(f"CDP {method} failed: {message['error']}")
                return message.get("result", {})
        raise RuntimeError(f"Timed out waiting for CDP response to {method}")

    def drain(self, seconds: float = 0.25) -> None:
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            try:
                message = self.ws.recv_json(min(0.1, max(0.01, deadline - time.monotonic())))
            except socket.timeout:
                continue
            self._record(message)

    def wait_for(self, marker: str, timeout: float = 10) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if any(marker in line for line in self.console):
                return
            try:
                message = self.ws.recv_json(min(0.25, max(0.01, deadline - time.monotonic())))
            except socket.timeout:
                continue
            self._record(message)
        raise RuntimeError(f"Missing console marker {marker!r}; console={self.console!r}")

    def close(self) -> None:
        self.ws.close()


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def devtools_target(port: int, timeout: float = 10) -> dict:
    deadline = time.monotonic() + timeout
    endpoint = f"http://127.0.0.1:{port}/json/list"
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(endpoint, timeout=1) as response:
                targets = json.load(response)
            for target in targets:
                if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
                    return target
        except Exception as exc:
            last_error = exc
        time.sleep(0.1)
    raise RuntimeError(f"Chromium DevTools endpoint did not become ready: {last_error}")


def advance_frames(cdp: DevTools, frame_count: int = 2) -> None:
    if frame_count < 1:
        return
    expression = f"""
        new Promise((resolve) => {{
            let remaining = {frame_count};
            const tick = () => {{
                remaining -= 1;
                if (remaining <= 0) {{
                    resolve(true);
                }} else {{
                    requestAnimationFrame(tick);
                }}
            }};
            requestAnimationFrame(tick);
        }})
    """
    cdp.call(
        "Runtime.evaluate",
        {"expression": expression, "awaitPromise": True, "returnByValue": True},
        timeout=5,
    )
    cdp.drain(0.05)


def dispatch_key(cdp: DevTools, *, key: str, code: str, virtual_key: int) -> None:
    common = {
        "key": key,
        "code": code,
        "windowsVirtualKeyCode": virtual_key,
        "nativeVirtualKeyCode": virtual_key,
    }
    advance_frames(cdp, 1)
    cdp.call("Input.dispatchKeyEvent", {"type": "keyDown", **common})
    advance_frames(cdp, 2)
    cdp.call("Input.dispatchKeyEvent", {"type": "keyUp", **common})
    advance_frames(cdp, 1)
    cdp.drain(0.1)


def dispatch_escape(cdp: DevTools) -> None:
    # Match Chromium's own DevTools protocol browsertest for the Escape event
    # shape, but hold the state across game frames so Defold can sample edges.
    common = {
        "windowsVirtualKeyCode": 27,
        "nativeVirtualKeyCode": 27,
    }
    advance_frames(cdp, 1)
    cdp.call("Input.dispatchKeyEvent", {"type": "rawKeyDown", **common})
    advance_frames(cdp, 2)
    cdp.call("Input.dispatchKeyEvent", {"type": "keyUp", **common})
    advance_frames(cdp, 1)
    cdp.drain(0.1)


def dispatch_touch(cdp: DevTools, x: float, y: float) -> None:
    point = {"x": x, "y": y, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}
    advance_frames(cdp, 1)
    cdp.call("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [point]})
    advance_frames(cdp, 2)
    cdp.call("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    advance_frames(cdp, 1)
    cdp.drain(0.1)


def require_marker(lines: list[str], marker: str, context: str) -> None:
    if not any(marker in line for line in lines):
        raise RuntimeError(f"{context}: expected {marker!r}, got {lines!r}")


def forbid_marker(lines: list[str], marker: str, context: str) -> None:
    if any(marker in line for line in lines):
        raise RuntimeError(f"{context}: forbidden {marker!r} leaked through modal: {lines!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", required=True)
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    parser.add_argument("--output", default="runtime-evidence/input-proxy-smoke.json")
    parser.add_argument("--browser-log", default="runtime-evidence/input-browser.log")
    args = parser.parse_args()

    output = Path(args.output)
    browser_log = Path(args.browser_log)
    output.parent.mkdir(parents=True, exist_ok=True)
    browser_log.parent.mkdir(parents=True, exist_ok=True)

    port = free_port()
    observed: dict[str, object] = {
        "schema_version": 1,
        "url": args.url,
        "checks": [],
        "console_markers": [],
    }

    with tempfile.TemporaryDirectory(
        prefix="bebee-chromium-", ignore_cleanup_errors=True
    ) as profile_dir, browser_log.open("w", encoding="utf-8") as log_file:
        process = subprocess.Popen(
            [
                args.browser,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--window-size=1280,720",
                f"--remote-debugging-port={port}",
                "--remote-debugging-address=127.0.0.1",
                f"--user-data-dir={profile_dir}",
                args.url,
            ],
            stdout=subprocess.DEVNULL,
            stderr=log_file,
        )
        cdp: DevTools | None = None
        try:
            target = devtools_target(port)
            cdp = DevTools(str(target["webSocketDebuggerUrl"]))
            cdp.call("Runtime.enable")
            cdp.call("Log.enable")
            cdp.call("Page.enable")
            cdp.call("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 1})
            cdp.call("Page.reload", {"ignoreCache": True})

            cdp.wait_for("BEBEE_INPUT proxy_loaded owner_focus=1", timeout=15)
            cdp.wait_for("BEBEE_INPUT gameplay_focus acquired", timeout=15)
            advance_frames(cdp, 2)
            observed["checks"].append("proxy_owner_and_gameplay_focus_ready")

            before = len(cdp.console)
            dispatch_key(cdp, key="w", code="KeyW", virtual_key=87)
            keyboard_lines = cdp.console[before:]
            require_marker(keyboard_lines, "BEBEE_INPUT gameplay move_up pressed", "keyboard proxy delivery")
            require_marker(keyboard_lines, "BEBEE_INPUT owner move_up pressed", "keyboard owner delivery")
            observed["checks"].append("keyboard_semantic_action_reaches_proxy_and_owner")

            dispatch_escape(cdp)
            cdp.wait_for("BEBEE_INPUT modal_open focus_acquired", timeout=5)
            advance_frames(cdp, 2)

            before = len(cdp.console)
            dispatch_key(cdp, key="w", code="KeyW", virtual_key=87)
            modal_lines = cdp.console[before:]
            require_marker(modal_lines, "BEBEE_INPUT modal_consumed move_up pressed", "modal consumption")
            forbid_marker(modal_lines, "BEBEE_INPUT gameplay move_up pressed", "modal consumption")
            forbid_marker(modal_lines, "BEBEE_INPUT owner move_up pressed", "modal consumption")
            observed["checks"].append("modal_consumes_before_gameplay_and_proxy_owner")

            dispatch_escape(cdp)
            cdp.wait_for("BEBEE_INPUT modal_closed focus_released", timeout=5)
            advance_frames(cdp, 2)

            before = len(cdp.console)
            dispatch_key(cdp, key="w", code="KeyW", virtual_key=87)
            restored_lines = cdp.console[before:]
            require_marker(restored_lines, "BEBEE_INPUT gameplay move_up pressed", "focus restoration")
            require_marker(restored_lines, "BEBEE_INPUT owner move_up pressed", "focus restoration")
            observed["checks"].append("closing_modal_restores_delivery")

            before = len(cdp.console)
            dispatch_touch(cdp, 320, 360)
            touch_lines = cdp.console[before:]
            require_marker(touch_lines, "BEBEE_INPUT gameplay pointer_primary pressed", "single-touch abstraction")
            require_marker(touch_lines, "BEBEE_INPUT owner pointer_primary pressed", "single-touch owner delivery")
            observed["checks"].append("browser_touch_reaches_pointer_primary_semantic_action")

            if cdp.runtime_exceptions:
                raise RuntimeError(f"Runtime exceptions observed: {cdp.runtime_exceptions!r}")

            observed["console_markers"] = [line for line in cdp.console if "BEBEE_INPUT" in line]
            observed["result"] = "pass"
            output.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
            print("BB-003 Chromium input/proxy smoke passed")
            return 0
        except Exception as exc:
            if cdp is not None:
                observed["console_markers"] = [line for line in cdp.console if "BEBEE_INPUT" in line]
                observed["runtime_exceptions"] = cdp.runtime_exceptions
            observed["result"] = "fail"
            observed["error"] = str(exc)
            output.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
            print(f"BB-003 Chromium input/proxy smoke failed: {exc}")
            return 1
        finally:
            if cdp is not None:
                cdp.close()
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
