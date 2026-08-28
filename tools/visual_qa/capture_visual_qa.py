#!/usr/bin/env python3
"""Capture deterministic BeBee HTML5 visual-QA evidence with Playwright Chromium."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import tempfile
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

try:
    from playwright.sync_api import Browser, Page, sync_playwright
except ImportError as exc:  # pragma: no cover - exercised by environment setup
    raise SystemExit(
        "Playwright is required. Install tools/visual_qa/requirements.txt and run "
        "`python -m playwright install chromium`."
    ) from exc

ROOT = Path(__file__).resolve().parents[2]
QA_CONFIG = ROOT / "config" / "visual-qa.json"
TOOLCHAIN = ROOT / "tools" / "defold" / "toolchain.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"{path} must contain a JSON object")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(path for path in root.rglob("*") if path.is_file())
    if not files:
        raise RuntimeError(f"Bundle directory has no files: {root}")
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256_file(path)))
        digest.update(b"\0")
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError(f"Capture is not a valid PNG: {path}")
    return struct.unpack(">II", data[16:24])


def with_qa_query(base_url: str, state_id: str, seed: int) -> str:
    parsed = urlsplit(base_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["qa"] = state_id
    query["qa_seed"] = str(seed)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def capture_once(
    browser: Browser,
    *,
    url: str,
    state_id: str,
    seed: int,
    head_sha: str,
    viewport_id: str,
    width: int,
    height: int,
    timeout_ms: int,
    output: Path,
) -> dict[str, object]:
    console_lines: list[str] = []
    console_errors: list[str] = []
    page_errors: list[str] = []
    context = browser.new_context(
        viewport={"width": width, "height": height},
        screen={"width": width, "height": height},
        device_scale_factor=1,
    )
    page: Page = context.new_page()

    def on_console(message) -> None:
        line = f"[{message.type}] {message.text}"
        console_lines.append(line)
        if message.type in {"error", "assert"}:
            console_errors.append(line)

    def on_page_error(error) -> None:
        page_errors.append(str(error))

    page.on("console", on_console)
    page.on("pageerror", on_page_error)
    try:
        page.goto(url, wait_until="load", timeout=timeout_ms)
        page.wait_for_function(
            """
            () => {
                const qa = window.__bebeeQA;
                return !!qa && qa.engineReady === true && (qa.captureReady === true || !!qa.error);
            }
            """,
            timeout=timeout_ms,
        )
        bridge = page.evaluate("() => ({...window.__bebeeQA})")
        if not isinstance(bridge, dict):
            raise RuntimeError("window.__bebeeQA did not return an object")
        if bridge.get("error"):
            raise RuntimeError(f"QA bridge rejected state: {bridge.get('error')}")
        if bridge.get("captureReady") is not True:
            raise RuntimeError(f"QA bridge never became capture-ready: {bridge!r}")
        if bridge.get("stateId") != state_id:
            raise RuntimeError(
                f"QA state mismatch: expected {state_id!r}, got {bridge.get('stateId')!r}"
            )
        if int(bridge.get("seed", -1)) != seed:
            raise RuntimeError(f"QA seed mismatch: expected {seed}, got {bridge.get('seed')!r}")
        if bridge.get("buildCommitSha") != head_sha:
            raise RuntimeError(
                "QA build SHA mismatch: "
                f"expected {head_sha}, got {bridge.get('buildCommitSha')!r}"
            )

        if state_id == "foundation_probe":
            probe = page.locator("#bebee-qa-foundation-probe")
            probe.wait_for(state="visible", timeout=timeout_ms)

        if console_errors:
            raise RuntimeError(f"Unexpected browser console errors: {console_errors!r}")
        if page_errors:
            raise RuntimeError(f"Unexpected page errors: {page_errors!r}")

        output.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(output), full_page=False, animations="disabled")
        actual_width, actual_height = png_dimensions(output)
        if (actual_width, actual_height) != (width, height):
            raise RuntimeError(
                f"Capture dimensions mismatch for {viewport_id}: "
                f"expected {width}x{height}, got {actual_width}x{actual_height}"
            )

        return {
            "bridge": bridge,
            "console_lines": console_lines,
            "console_errors": console_errors,
            "page_errors": page_errors,
            "capture_sha256": sha256_file(output),
            "simulation_frame": int(bridge.get("simulationFrame", -1)),
        }
    finally:
        context.close()


def assert_release_bridge_absent(
    browser: Browser,
    *,
    release_url: str,
    state_id: str,
    seed: int,
    width: int,
    height: int,
    timeout_ms: int,
) -> dict[str, object]:
    context = browser.new_context(
        viewport={"width": width, "height": height},
        screen={"width": width, "height": height},
        device_scale_factor=1,
    )
    page = context.new_page()
    try:
        page.goto(with_qa_query(release_url, state_id, seed), wait_until="load", timeout=timeout_ms)
        page.wait_for_function(
            """
            () => {
                const canvas = document.querySelector("canvas");
                return document.readyState === "complete" && !!canvas && canvas.width > 0 && canvas.height > 0;
            }
            """,
            timeout=timeout_ms,
        )
        bridge_present = page.evaluate("() => typeof window.__bebeeQA !== 'undefined'")
        probe_present = page.locator("#bebee-qa-foundation-probe").count() > 0
        if bridge_present or probe_present:
            raise RuntimeError(
                "Release bundle exposed deterministic QA surface: "
                f"bridge_present={bridge_present}, probe_present={probe_present}"
            )
        return {"bridge_present": False, "probe_present": False}
    finally:
        context.close()


def parse_args() -> argparse.Namespace:
    qa = load_json(QA_CONFIG)
    parser = argparse.ArgumentParser()
    parser.add_argument("--head-sha", required=True)
    parser.add_argument(
        "--bundle-dir",
        type=Path,
        default=ROOT / "build" / "html5" / "development" / "BeBee",
    )
    parser.add_argument("--url", default="http://127.0.0.1:8000/development/BeBee/")
    parser.add_argument("--release-url", default="http://127.0.0.1:8000/release/BeBee/")
    parser.add_argument("--state", default="foundation_probe")
    parser.add_argument("--seed", type=int, default=int(qa["runtime_contract"]["default_seed"]))
    parser.add_argument("--viewports", default="")
    parser.add_argument("--repeat", type=int, default=2)
    parser.add_argument(
        "--output-root",
        type=Path,
        help="Defaults to artifacts/visual-qa/<head_sha>.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    head_sha = args.head_sha.strip().lower()
    if not SHA_RE.fullmatch(head_sha):
        raise RuntimeError("--head-sha must be a full 40-character Git SHA")
    if args.repeat < 2:
        raise RuntimeError("--repeat must be at least 2 so unchanged-state stability is exercised")

    qa = load_json(QA_CONFIG)
    toolchain = load_json(TOOLCHAIN)
    states = {item["id"]: item for item in qa["states"]}
    viewports = {item["id"]: item for item in qa["viewports"]}
    if args.state not in states:
        raise RuntimeError(f"Unknown configured QA state: {args.state}")
    state = states[args.state]

    viewport_ids = [item for item in args.viewports.split(",") if item]
    if not viewport_ids:
        viewport_ids = list(state["default_viewports"])
    for viewport_id in viewport_ids:
        if viewport_id not in viewports:
            raise RuntimeError(f"Unknown configured viewport: {viewport_id}")

    bundle_dir = args.bundle_dir.expanduser().resolve()
    if not (bundle_dir / "index.html").is_file():
        raise RuntimeError(f"Development HTML5 bundle not found: {bundle_dir}")
    bundle_digest = sha256_tree(bundle_dir)
    output_root = (
        args.output_root.expanduser().resolve()
        if args.output_root
        else ROOT / "artifacts" / "visual-qa" / head_sha
    )
    output_root.mkdir(parents=True, exist_ok=True)
    timeout_ms = int(qa["capture_pipeline"]["readiness_timeout_seconds"]) * 1000
    console_log: list[str] = []
    capture_records: list[dict[str, object]] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            browser_version = browser.version
            for viewport_id in viewport_ids:
                viewport = viewports[viewport_id]
                width = int(viewport["width"])
                height = int(viewport["height"])
                capture_path = output_root / args.state / f"{viewport_id}.png"
                capture_url = with_qa_query(args.url, args.state, args.seed)
                first = capture_once(
                    browser,
                    url=capture_url,
                    state_id=args.state,
                    seed=args.seed,
                    head_sha=head_sha,
                    viewport_id=viewport_id,
                    width=width,
                    height=height,
                    timeout_ms=timeout_ms,
                    output=capture_path,
                )
                for line in first["console_lines"]:
                    console_log.append(f"{args.state}/{viewport_id}/run1 {line}")

                repeat_digests = [str(first["capture_sha256"])]
                with tempfile.TemporaryDirectory(prefix="bebee-visual-qa-repeat-") as temp_dir:
                    for repeat_index in range(2, args.repeat + 1):
                        repeat_path = Path(temp_dir) / f"repeat-{repeat_index}.png"
                        repeated = capture_once(
                            browser,
                            url=capture_url,
                            state_id=args.state,
                            seed=args.seed,
                            head_sha=head_sha,
                            viewport_id=viewport_id,
                            width=width,
                            height=height,
                            timeout_ms=timeout_ms,
                            output=repeat_path,
                        )
                        repeat_digests.append(str(repeated["capture_sha256"]))
                        for line in repeated["console_lines"]:
                            console_log.append(
                                f"{args.state}/{viewport_id}/run{repeat_index} {line}"
                            )

                if len(set(repeat_digests)) != 1:
                    raise RuntimeError(
                        f"Unchanged-state capture is not byte-stable for {viewport_id}: "
                        f"{repeat_digests!r}"
                    )

                capture_records.append(
                    {
                        "state_id": args.state,
                        "qa_seed": args.seed,
                        "viewport_id": viewport_id,
                        "viewport_width": width,
                        "viewport_height": height,
                        "simulation_frame": first["simulation_frame"],
                        "capture_file": capture_path.relative_to(output_root).as_posix(),
                        "capture_sha256": first["capture_sha256"],
                        "console_error_count": len(first["console_errors"]),
                        "page_error_count": len(first["page_errors"]),
                        "repeat_count": args.repeat,
                        "repeat_sha256": repeat_digests,
                        "stable_exact_sha256": True,
                    }
                )

            release_probe = assert_release_bridge_absent(
                browser,
                release_url=args.release_url,
                state_id=args.state,
                seed=args.seed,
                width=int(viewports[viewport_ids[0]]["width"]),
                height=int(viewports[viewport_ids[0]]["height"]),
                timeout_ms=timeout_ms,
            )
        finally:
            browser.close()

    (output_root / "console.log").write_text(
        "\n".join(console_log) + ("\n" if console_log else ""), encoding="utf-8"
    )
    report = {
        "schema_version": 1,
        "head_sha": head_sha,
        "bundle_sha256": bundle_digest,
        "defold_version": toolchain["defold_version"],
        "browser_name": "Playwright Chromium",
        "browser_version": browser_version,
        "state_id": args.state,
        "qa_seed": args.seed,
        "release_qa_absence": release_probe,
        "captures": capture_records,
    }
    (output_root / "capture-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"BB-006 visual QA capture: PASS ({args.state}, {len(capture_records)} viewports, "
        f"{args.repeat} exact repeats each)"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"BB-006 visual QA capture failed: {exc}")
        raise SystemExit(1)
