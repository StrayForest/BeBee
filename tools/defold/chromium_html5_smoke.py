#!/usr/bin/env python3
"""Smoke-test a served BeBee HTML5 bundle through Chromium DevTools.

The script is dependency-free. It verifies that the page reaches a usable canvas,
loads a WebAssembly engine with the expected MIME type, and produces no browser
console errors, runtime exceptions, or non-cancelled network failures.
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

from chromium_input_proxy_smoke import WebSocket, devtools_target, free_port


class SmokeDevTools:
    def __init__(self, websocket_url: str) -> None:
        self.ws = WebSocket(websocket_url)
        self.next_id = 1
        self.page_loaded = False
        self.console: list[str] = []
        self.console_errors: list[str] = []
        self.runtime_exceptions: list[str] = []
        self.network_requests: dict[str, str] = {}
        self.network_responses: list[dict[str, object]] = []
        self.network_failures: list[dict[str, object]] = []

    def _record(self, message: dict) -> None:
        method = message.get("method")
        params = message.get("params", {})

        if method == "Page.loadEventFired":
            self.page_loaded = True
            return

        if method == "Runtime.consoleAPICalled":
            values = []
            for item in params.get("args", []):
                value = item.get("value")
                if value is None:
                    value = item.get("description", "")
                values.append(str(value))
            line = " ".join(values).strip()
            if line:
                self.console.append(line)
                if params.get("type") in {"error", "assert"}:
                    self.console_errors.append(line)
            return

        if method == "Log.entryAdded":
            entry = params.get("entry", {})
            text = str(entry.get("text", "")).strip()
            if text:
                self.console.append(text)
                if entry.get("level") == "error":
                    self.console_errors.append(text)
            return

        if method == "Runtime.exceptionThrown":
            details = params.get("exceptionDetails", {})
            text = str(details.get("text", "runtime exception"))
            exception = details.get("exception")
            if isinstance(exception, dict):
                description = exception.get("description")
                if description:
                    text = f"{text}: {description}"
            self.runtime_exceptions.append(text)
            return

        if method == "Network.requestWillBeSent":
            request_id = str(params.get("requestId", ""))
            request = params.get("request", {})
            url = request.get("url")
            if request_id and url:
                self.network_requests[request_id] = str(url)
            return

        if method == "Network.responseReceived":
            response = params.get("response", {})
            request_id = str(params.get("requestId", ""))
            url = str(response.get("url") or self.network_requests.get(request_id, ""))
            self.network_responses.append(
                {
                    "request_id": request_id,
                    "url": url,
                    "status": response.get("status"),
                    "mime_type": response.get("mimeType"),
                    "resource_type": params.get("type"),
                }
            )
            return

        if method == "Network.loadingFailed":
            request_id = str(params.get("requestId", ""))
            self.network_failures.append(
                {
                    "request_id": request_id,
                    "url": self.network_requests.get(request_id, ""),
                    "error_text": params.get("errorText"),
                    "resource_type": params.get("type"),
                    "canceled": bool(params.get("canceled", False)),
                    "blocked_reason": params.get("blockedReason"),
                }
            )

    def call(self, method: str, params: dict | None = None, timeout: float = 5) -> dict:
        command_id = self.next_id
        self.next_id += 1
        self.ws.send_json({"id": command_id, "method": method, "params": params or {}})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                message = self.ws.recv_json(max(0.05, deadline - time.monotonic()))
            except socket.timeout:
                continue
            self._record(message)
            if message.get("id") == command_id:
                if "error" in message:
                    raise RuntimeError(f"CDP {method} failed: {message['error']}")
                return message.get("result", {})
        raise RuntimeError(f"Timed out waiting for CDP response to {method}")

    def drain(self, seconds: float) -> None:
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            try:
                message = self.ws.recv_json(min(0.1, max(0.01, deadline - time.monotonic())))
            except socket.timeout:
                continue
            self._record(message)

    def wait_for_load(self, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.page_loaded:
                return
            try:
                message = self.ws.recv_json(min(0.25, max(0.01, deadline - time.monotonic())))
            except socket.timeout:
                continue
            self._record(message)
        raise RuntimeError("Timed out waiting for Page.loadEventFired")

    def close(self) -> None:
        self.ws.close()


def canvas_state(cdp: SmokeDevTools) -> dict[str, object]:
    result = cdp.call(
        "Runtime.evaluate",
        {
            "expression": """
                (() => {
                    const canvas = document.querySelector("canvas");
                    return {
                        ready_state: document.readyState,
                        has_canvas: !!canvas,
                        canvas_width: canvas ? canvas.width : 0,
                        canvas_height: canvas ? canvas.height : 0,
                        webassembly_available: typeof WebAssembly === "object"
                    };
                })()
            """,
            "returnByValue": True,
        },
    )
    return dict(result.get("result", {}).get("value") or {})


def wait_for_canvas(cdp: SmokeDevTools, timeout: float) -> dict[str, object]:
    deadline = time.monotonic() + timeout
    last: dict[str, object] = {}
    while time.monotonic() < deadline:
        last = canvas_state(cdp)
        if (
            last.get("ready_state") == "complete"
            and last.get("has_canvas") is True
            and int(last.get("canvas_width") or 0) > 0
            and int(last.get("canvas_height") or 0) > 0
            and last.get("webassembly_available") is True
        ):
            return last
        cdp.drain(0.15)
    raise RuntimeError(f"HTML5 canvas did not become ready: {last!r}")


def is_ignored_network_failure(item: dict[str, object]) -> bool:
    if item.get("canceled"):
        return True
    url = str(item.get("url") or "")
    if not url:
        return False
    parsed = urlparse(url)
    if parsed.path.endswith("/favicon.ico"):
        return True
    return parsed.scheme not in {"http", "https"}


def wasm_responses(cdp: SmokeDevTools) -> list[dict[str, object]]:
    responses = []
    for item in cdp.network_responses:
        path = urlparse(str(item.get("url") or "")).path.lower()
        if ".wasm" in path:
            responses.append(item)
    return responses


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", default="html5-ci/browser-smoke.json")
    parser.add_argument("--browser-log", default="html5-ci/browser.log")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--settle-seconds", type=float, default=3.0)
    args = parser.parse_args()

    output = Path(args.output)
    browser_log = Path(args.browser_log)
    output.parent.mkdir(parents=True, exist_ok=True)
    browser_log.parent.mkdir(parents=True, exist_ok=True)

    observed: dict[str, object] = {
        "schema_version": 1,
        "url": args.url,
        "checks": [],
        "result": "fail",
    }

    port = free_port()
    with tempfile.TemporaryDirectory(
        prefix="bebee-html5-smoke-", ignore_cleanup_errors=True
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
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=log_file,
        )
        cdp: SmokeDevTools | None = None
        try:
            target = devtools_target(port, timeout=args.timeout)
            cdp = SmokeDevTools(str(target["webSocketDebuggerUrl"]))
            cdp.call("Runtime.enable")
            cdp.call("Log.enable")
            cdp.call("Page.enable")
            cdp.call("Network.enable")

            cdp.call("Page.navigate", {"url": args.url})
            cdp.wait_for_load(args.timeout)
            observed["checks"].append("page_load_event")

            state = wait_for_canvas(cdp, args.timeout)
            observed["canvas"] = state
            observed["checks"].append("nonzero_canvas_and_webassembly")

            cdp.drain(args.settle_seconds)

            wasm = wasm_responses(cdp)
            observed["wasm_responses"] = wasm
            good_wasm = [
                item
                for item in wasm
                if int(float(item.get("status") or 0)) == 200
                and str(item.get("mime_type") or "").lower().startswith("application/wasm")
            ]
            if not good_wasm:
                raise RuntimeError(
                    "No successful application/wasm response observed; "
                    f"wasm_responses={wasm!r}"
                )
            observed["checks"].append("wasm_200_application_wasm")

            actionable_failures = [
                item for item in cdp.network_failures if not is_ignored_network_failure(item)
            ]
            observed["network_failures"] = actionable_failures
            observed["console_errors"] = cdp.console_errors
            observed["runtime_exceptions"] = cdp.runtime_exceptions
            observed["console_tail"] = cdp.console[-100:]

            if actionable_failures:
                raise RuntimeError(f"Network loading failures observed: {actionable_failures!r}")
            observed["checks"].append("no_network_loading_failures")

            if cdp.console_errors:
                raise RuntimeError(f"Browser console errors observed: {cdp.console_errors!r}")
            observed["checks"].append("no_console_errors")

            if cdp.runtime_exceptions:
                raise RuntimeError(f"Runtime exceptions observed: {cdp.runtime_exceptions!r}")
            observed["checks"].append("no_runtime_exceptions")

            observed["result"] = "pass"
            output.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
            print("BB-005 HTML5 browser smoke passed")
            return 0
        except Exception as exc:
            if cdp is not None:
                observed["network_failures"] = [
                    item
                    for item in cdp.network_failures
                    if not is_ignored_network_failure(item)
                ]
                observed["console_errors"] = cdp.console_errors
                observed["runtime_exceptions"] = cdp.runtime_exceptions
                observed["console_tail"] = cdp.console[-100:]
                observed["wasm_responses"] = wasm_responses(cdp)
            observed["error"] = str(exc)
            output.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
            print(f"BB-005 HTML5 browser smoke failed: {exc}")
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
