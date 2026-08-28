#!/usr/bin/env python3
"""Capture deterministic BeBee HTML5 QA evidence with pinned Playwright Chromium."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlencode, urlparse

try:
    from playwright.sync_api import Browser, Page, sync_playwright
except ImportError as exc:  # pragma: no cover - exercised as a setup failure in CI
    raise SystemExit(
        "Playwright is required. Install tools/visual_qa/requirements.txt and "
        "run `python -m playwright install chromium`."
    ) from exc

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = ROOT / "config" / "visual-qa.json"
TOOLCHAIN = ROOT / "tools" / "defold" / "toolchain.json"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bundle(directory: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(path for path in directory.rglob("*") if path.is_file())
    if not files:
        raise RuntimeError(f"Bundle is empty: {directory}")
    for path in files:
        relative = path.relative_to(directory).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256_file(path)))
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != PNG_SIGNATURE or data[12:16] != b"IHDR":
        raise RuntimeError(f"Not a valid PNG screenshot: {path}")
    return struct.unpack(">II", data[16:24])


def is_favicon_url(url: object) -> bool:
    return urlparse(str(url or "")).path == "/favicon.ico"


def join_url(base_url: str, suffix: str, params: dict[str, object] | None = None) -> str:
    url = base_url.rstrip("/") + "/" + suffix.lstrip("/")
    if params:
        url += "?" + urlencode(params)
    return url


@dataclass
class BrowserEvidence:
    label: str
    console: list[dict[str, object]] = field(default_factory=list)
    page_errors: list[str] = field(default_factory=list)
    http_errors: list[dict[str, object]] = field(default_factory=list)
    request_failures: list[dict[str, object]] = field(default_factory=list)

    def attach(self, page: Page) -> None:
        def on_console(message) -> None:
            self.console.append(
                {
                    "type": message.type,
                    "text": message.text,
                    "url": str((message.location or {}).get("url") or ""),
                }
            )

        def on_page_error(error) -> None:
            self.page_errors.append(str(error))

        def on_response(response) -> None:
            if response.status >= 400:
                self.http_errors.append(
                    {
                        "status": response.status,
                        "url": response.url,
                    }
                )

        def on_request_failed(request) -> None:
            self.request_failures.append(
                {
                    "url": request.url,
                    "failure": request.failure,
                }
            )

        page.on("console", on_console)
        page.on("pageerror", on_page_error)
        page.on("response", on_response)
        page.on("requestfailed", on_request_failed)

    def ignored_http_errors(self) -> list[dict[str, object]]:
        return [
            item
            for item in self.http_errors
            if int(item.get("status") or 0) == 404 and is_favicon_url(item.get("url"))
        ]

    def actionable_http_errors(self) -> list[dict[str, object]]:
        return [
            item
            for item in self.http_errors
            if not (int(item.get("status") or 0) == 404 and is_favicon_url(item.get("url")))
        ]

    def actionable_console_errors(self) -> list[dict[str, object]]:
        http_errors = self.actionable_http_errors()
        ignored_http = self.ignored_http_errors()
        actionable: list[dict[str, object]] = []
        for item in self.console:
            if item.get("type") not in {"error", "assert"}:
                continue
            url = str(item.get("url") or "")
            text = str(item.get("text") or "")
            if is_favicon_url(url) and "404" in text:
                continue
            if (
                not url
                and "Failed to load resource" in text
                and "404" in text
                and ignored_http
                and not http_errors
            ):
                continue
            actionable.append(item)
        return actionable

    def assert_clean(self) -> None:
        failures = self.actionable_http_errors()
        console_errors = self.actionable_console_errors()
        if failures:
            raise RuntimeError(f"{self.label}: HTTP errors: {failures!r}")
        if self.request_failures:
            raise RuntimeError(
                f"{self.label}: request failures: {self.request_failures!r}"
            )
        if console_errors:
            raise RuntimeError(f"{self.label}: console errors: {console_errors!r}")
        if self.page_errors:
            raise RuntimeError(f"{self.label}: page errors: {self.page_errors!r}")

    def log_lines(self) -> list[str]:
        lines = [f"[{self.label}] browser evidence"]
        for item in self.console:
            lines.append(
                "console "
                + json.dumps(item, sort_keys=True, separators=(",", ":"))
            )
        for item in self.http_errors:
            lines.append(
                "http_error "
                + json.dumps(item, sort_keys=True, separators=(",", ":"))
            )
        for item in self.request_failures:
            lines.append(
                "request_failure "
                + json.dumps(item, sort_keys=True, separators=(",", ":"))
            )
        for item in self.page_errors:
            lines.append("page_error " + item)
        return lines


def load_plan(path: Path) -> dict[str, object]:
    plan = json.loads(path.read_text(encoding="utf-8"))
    if plan.get("schema_version") != 1:
        raise RuntimeError("Unsupported visual QA plan schema")
    return plan


def state_by_id(plan: dict[str, object], state_id: str) -> dict[str, object]:
    states = plan.get("states")
    if not isinstance(states, list):
        raise RuntimeError("visual QA plan states must be a list")
    for state in states:
        if isinstance(state, dict) and state.get("id") == state_id:
            return state
    raise RuntimeError(f"Unknown QA state in plan: {state_id}")


def viewport_by_id(plan: dict[str, object], viewport_id: str) -> dict[str, object]:
    viewports = plan.get("viewports")
    if not isinstance(viewports, list):
        raise RuntimeError("visual QA plan viewports must be a list")
    for viewport in viewports:
        if isinstance(viewport, dict) and viewport.get("id") == viewport_id:
            return viewport
    raise RuntimeError(f"Unknown viewport in plan: {viewport_id}")


def wait_for_canvas(page: Page, timeout_ms: int) -> None:
    page.wait_for_function(
        """
        () => {
            const canvas = document.querySelector('canvas');
            return document.readyState === 'complete' && canvas &&
                canvas.width > 0 && canvas.height > 0;
        }
        """,
        timeout=timeout_ms,
    )


def wait_for_qa_bridge(page: Page, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        """
        () => window.__bebeeQA &&
            window.__bebeeQA.engineReady === true &&
            (window.__bebeeQA.captureReady === true || window.__bebeeQA.error)
        """,
        timeout=timeout_ms,
    )
    bridge = page.evaluate("() => ({...window.__bebeeQA})")
    if not isinstance(bridge, dict):
        raise RuntimeError(f"QA bridge did not return an object: {bridge!r}")
    return bridge


def capture_development_once(
    browser: Browser,
    *,
    base_url: str,
    state_id: str,
    seed: int,
    head_sha: str,
    viewport: dict[str, object],
    timeout_ms: int,
    destination: Path,
    label: str,
) -> tuple[dict[str, object], BrowserEvidence]:
    width = int(viewport["width"])
    height = int(viewport["height"])
    evidence = BrowserEvidence(label)
    context = browser.new_context(viewport={"width": width, "height": height})
    try:
        page = context.new_page()
        evidence.attach(page)
        page.goto(
            join_url(
                base_url,
                "development/BeBee/",
                {"qa": state_id, "qa_seed": seed},
            ),
            wait_until="load",
            timeout=timeout_ms,
        )
        wait_for_canvas(page, timeout_ms)
        bridge = wait_for_qa_bridge(page, timeout_ms)

        if bridge.get("error"):
            raise RuntimeError(f"{label}: QA bridge failed closed: {bridge!r}")
        expected = {
            "schemaVersion": 1,
            "stateId": state_id,
            "seed": seed,
            "engineReady": True,
            "captureReady": True,
            "buildCommitSha": head_sha,
        }
        mismatches = {
            key: {"expected": value, "actual": bridge.get(key)}
            for key, value in expected.items()
            if bridge.get(key) != value
        }
        if mismatches:
            raise RuntimeError(f"{label}: QA bridge mismatch: {mismatches!r}")

        destination.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(destination), full_page=False, animations="disabled")
        actual_width, actual_height = png_dimensions(destination)
        if (actual_width, actual_height) != (width, height):
            raise RuntimeError(
                f"{label}: capture dimensions {(actual_width, actual_height)} != "
                f"configured {(width, height)}"
            )
        evidence.assert_clean()
        return bridge, evidence
    finally:
        context.close()


def verify_release_guard(
    browser: Browser,
    *,
    base_url: str,
    state_id: str,
    seed: int,
    viewport: dict[str, object],
    timeout_ms: int,
    scratch: Path,
) -> tuple[dict[str, object], list[BrowserEvidence]]:
    width = int(viewport["width"])
    height = int(viewport["height"])
    records: list[BrowserEvidence] = []
    hashes: dict[str, str] = {}
    bridge_exposed: dict[str, bool] = {}

    for variant, params in (
        ("plain", None),
        ("qa_query", {"qa": state_id, "qa_seed": seed}),
    ):
        evidence = BrowserEvidence(f"release-{variant}")
        records.append(evidence)
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            evidence.attach(page)
            page.goto(
                join_url(base_url, "release/BeBee/", params),
                wait_until="load",
                timeout=timeout_ms,
            )
            wait_for_canvas(page, timeout_ms)
            page.evaluate(
                "() => new Promise(resolve => requestAnimationFrame(() => "
                "requestAnimationFrame(resolve)))"
            )
            bridge_exposed[variant] = bool(
                page.evaluate("() => typeof window.__bebeeQA !== 'undefined'")
            )
            path = scratch / f"release-{variant}.png"
            page.screenshot(path=str(path), full_page=False, animations="disabled")
            if png_dimensions(path) != (width, height):
                raise RuntimeError(
                    f"release-{variant}: screenshot dimensions do not match viewport"
                )
            hashes[variant] = sha256_file(path)
            evidence.assert_clean()
        finally:
            context.close()

    if any(bridge_exposed.values()):
        raise RuntimeError(f"Release exposed window.__bebeeQA: {bridge_exposed!r}")
    if hashes["plain"] != hashes["qa_query"]:
        raise RuntimeError(
            "Release rendering changed when QA query parameters were supplied: "
            f"plain={hashes['plain']} qa_query={hashes['qa_query']}"
        )

    return (
        {
            "viewport_id": str(viewport["id"]),
            "bridge_exposed": bridge_exposed,
            "plain_capture_sha256": hashes["plain"],
            "qa_query_capture_sha256": hashes["qa_query"],
            "qa_query_ignored": True,
        },
        records,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/")
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--development-bundle", type=Path, required=True)
    parser.add_argument("--release-bundle", type=Path, required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--state", default="movement_empty")
    parser.add_argument(
        "--viewports",
        default="desktop_reference,mobile_landscape",
        help="Comma-separated viewport IDs to capture twice each.",
    )
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float, default=20.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    head_sha = args.head_sha.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", head_sha):
        raise RuntimeError("--head-sha must be an exact 40-character Git SHA")

    plan_path = args.plan.resolve()
    plan = load_plan(plan_path)
    state = state_by_id(plan, args.state)
    seed = int(plan["runtime_contract"]["default_seed"])
    timeout_ms = int(args.timeout_seconds * 1000)
    requested_viewports = [
        item.strip() for item in args.viewports.split(",") if item.strip()
    ]
    if not requested_viewports:
        raise RuntimeError("At least one viewport is required")

    development_bundle = args.development_bundle.resolve()
    release_bundle = args.release_bundle.resolve()
    for name, directory in (
        ("development", development_bundle),
        ("release", release_bundle),
    ):
        if not (directory / "index.html").is_file():
            raise RuntimeError(f"Missing {name} bundle index.html: {directory}")

    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    scratch = output_root / ".repeat"
    scratch.mkdir(parents=True, exist_ok=True)

    development_digest = sha256_bundle(development_bundle)
    release_digest = sha256_bundle(release_bundle)
    toolchain = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    captures: list[dict[str, object]] = []
    all_evidence: list[BrowserEvidence] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            browser_version = browser.version
            for viewport_id in requested_viewports:
                viewport = viewport_by_id(plan, viewport_id)
                first_path = output_root / args.state / f"{viewport_id}.png"
                second_path = scratch / f"{args.state}-{viewport_id}-repeat.png"

                first_bridge, first_evidence = capture_development_once(
                    browser,
                    base_url=args.base_url,
                    state_id=args.state,
                    seed=seed,
                    head_sha=head_sha,
                    viewport=viewport,
                    timeout_ms=timeout_ms,
                    destination=first_path,
                    label=f"{args.state}/{viewport_id}/first",
                )
                second_bridge, second_evidence = capture_development_once(
                    browser,
                    base_url=args.base_url,
                    state_id=args.state,
                    seed=seed,
                    head_sha=head_sha,
                    viewport=viewport,
                    timeout_ms=timeout_ms,
                    destination=second_path,
                    label=f"{args.state}/{viewport_id}/repeat",
                )
                all_evidence.extend([first_evidence, second_evidence])

                first_sha = sha256_file(first_path)
                second_sha = sha256_file(second_path)
                if first_sha != second_sha:
                    raise RuntimeError(
                        f"Unstable repeated capture for {args.state}/{viewport_id}: "
                        f"{first_sha} != {second_sha}"
                    )
                if first_bridge.get("simulationFrame") != second_bridge.get(
                    "simulationFrame"
                ):
                    raise RuntimeError(
                        f"Simulation frame drift for {args.state}/{viewport_id}: "
                        f"{first_bridge.get('simulationFrame')} != "
                        f"{second_bridge.get('simulationFrame')}"
                    )

                captures.append(
                    {
                        "schema_version": 1,
                        "head_sha": head_sha,
                        "bundle_sha256": development_digest,
                        "defold_version": str(toolchain["defold_version"]),
                        "browser_name": "chromium",
                        "browser_version": browser_version,
                        "state_id": args.state,
                        "qa_seed": seed,
                        "viewport_id": viewport_id,
                        "viewport_width": int(viewport["width"]),
                        "viewport_height": int(viewport["height"]),
                        "simulation_frame": int(first_bridge["simulationFrame"]),
                        "capture_file": first_path.relative_to(output_root).as_posix(),
                        "capture_sha256": first_sha,
                        "repeat_capture_sha256": second_sha,
                        "repeat_stable": True,
                        "console_error_count": len(
                            first_evidence.actionable_console_errors()
                        ),
                        "page_error_count": len(first_evidence.page_errors),
                    }
                )

            release_viewport = viewport_by_id(plan, requested_viewports[0])
            release_guard, release_evidence = verify_release_guard(
                browser,
                base_url=args.base_url,
                state_id=args.state,
                seed=seed,
                viewport=release_viewport,
                timeout_ms=timeout_ms,
                scratch=scratch,
            )
            all_evidence.extend(release_evidence)
        finally:
            browser.close()

    report = {
        "schema_version": 1,
        "head_sha": head_sha,
        "state_id": args.state,
        "state_category": state.get("category"),
        "qa_seed": seed,
        "development_bundle_sha256": development_digest,
        "release_bundle_sha256": release_digest,
        "defold_version": str(toolchain["defold_version"]),
        "browser_name": "chromium",
        "browser_version": browser_version,
        "captures": captures,
        "release_guard": release_guard,
        "result": "pass",
    }
    (output_root / "capture-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    log_lines: list[str] = []
    for evidence in all_evidence:
        log_lines.extend(evidence.log_lines())
    (output_root / "console.log").write_text(
        "\n".join(log_lines) + "\n",
        encoding="utf-8",
    )

    for path in scratch.glob("*.png"):
        path.unlink()
    scratch.rmdir()

    print(
        "BB-006 visual QA capture passed: "
        f"state={args.state} viewports={','.join(requested_viewports)} "
        f"browser=Chromium {browser_version}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        print(f"BB-006 visual QA failed: {exc}")
        raise SystemExit(1)
