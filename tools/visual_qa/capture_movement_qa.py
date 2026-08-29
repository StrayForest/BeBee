#!/usr/bin/env python3
"""Exercise real BeBee movement inputs and retain exact-head motion evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import tempfile
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def with_query(base_url: str, **values: object) -> str:
    parsed = urlsplit(base_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for key, value in values.items():
        query[key] = str(value)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def finite(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def bridge(page: Page) -> dict[str, object]:
    value = page.evaluate("() => window.__bebeeMovementQA ? ({...window.__bebeeMovementQA}) : null")
    if not isinstance(value, dict):
        raise RuntimeError("window.__bebeeMovementQA is not available")
    for field in ("beeX", "beeY", "speed", "cameraX", "cameraY", "distanceTravelled", "frame"):
        if not finite(value.get(field)):
            raise RuntimeError(f"Movement bridge field {field} is not finite: {value!r}")
    return value


def install_error_capture(page: Page) -> tuple[list[str], list[str]]:
    console_errors: list[str] = []
    page_errors: list[str] = []

    def on_console(message) -> None:
        if message.type in {"error", "assert"}:
            console_errors.append(f"[{message.type}] {message.text}")

    def on_page_error(error) -> None:
        page_errors.append(str(error))

    page.on("console", on_console)
    page.on("pageerror", on_page_error)
    return console_errors, page_errors


def wait_ready(page: Page, *, head_sha: str, state_id: str, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        """() => {
            const qa = window.__bebeeQA;
            const movement = window.__bebeeMovementQA;
            return !!qa && qa.captureReady === true && !!movement;
        }""",
        timeout=timeout_ms,
    )
    qa = page.evaluate("() => ({...window.__bebeeQA})")
    if not isinstance(qa, dict):
        raise RuntimeError("window.__bebeeQA did not return an object")
    if qa.get("stateId") != state_id:
        raise RuntimeError(f"QA state mismatch: expected {state_id}, got {qa.get('stateId')!r}")
    if qa.get("buildCommitSha") != head_sha:
        raise RuntimeError(
            f"QA build SHA mismatch: expected {head_sha}, got {qa.get('buildCommitSha')!r}"
        )
    return bridge(page)


def assert_no_errors(console_errors: list[str], page_errors: list[str], context: str) -> None:
    if console_errors:
        raise RuntimeError(f"{context}: unexpected console errors: {console_errors!r}")
    if page_errors:
        raise RuntimeError(f"{context}: unexpected page errors: {page_errors!r}")


def screenshot(page: Page, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path), full_page=False, animations="disabled")


def record_desktop_motion(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    frames_dir = output_root / "movement_dense" / "desktop_reference_frames"
    video_path = output_root / "movement_dense" / "desktop_reference.webm"
    video_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="bebee-movement-video-") as video_dir:
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            screen={"width": 1280, "height": 720},
            device_scale_factor=1,
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        video = page.video
        console_errors, page_errors = install_error_capture(page)
        url = with_query(base_url, qa="movement_dense", qa_seed=88008)
        try:
            page.goto(url, wait_until="load", timeout=timeout_ms)
            start = wait_ready(page, head_sha=head_sha, state_id="movement_dense", timeout_ms=timeout_ms)
            screenshot(page, frames_dir / "00-idle.png")

            t0 = time.monotonic()
            page.keyboard.down("d")
            page.wait_for_timeout(350)
            early = bridge(page)
            screenshot(page, frames_dir / "01-accelerating.png")
            page.wait_for_timeout(500)
            cruise = bridge(page)
            screenshot(page, frames_dir / "02-cruise.png")

            page.keyboard.down("w")
            page.wait_for_timeout(650)
            diagonal = bridge(page)
            screenshot(page, frames_dir / "03-diagonal.png")
            page.keyboard.up("w")
            page.keyboard.up("d")
            page.wait_for_timeout(450)
            stopped = bridge(page)
            screenshot(page, frames_dir / "04-stopped.png")
            duration = time.monotonic() - t0

            if early.get("inputSource") != "keyboard" or float(early["speed"]) <= 100:
                raise RuntimeError(f"Desktop input did not accelerate through keyboard path: {early!r}")
            if float(cruise["beeX"]) - float(start["beeX"]) <= 80:
                raise RuntimeError(f"Desktop bee displacement too small: start={start!r} cruise={cruise!r}")
            if float(cruise["speed"]) < 250 or float(cruise["speed"]) > 305:
                raise RuntimeError(f"Desktop cruise speed outside expected band: {cruise!r}")
            if diagonal.get("inputSource") != "keyboard":
                raise RuntimeError(f"Diagonal keyboard source lost: {diagonal!r}")
            intent_length = math.hypot(float(diagonal["intentX"]), float(diagonal["intentY"]))
            if abs(intent_length - 1.0) > 0.02:
                raise RuntimeError(f"Diagonal intent is not normalized: {diagonal!r}")
            if float(stopped["speed"]) > 5 or stopped.get("inputSource") != "none":
                raise RuntimeError(f"Desktop release did not settle to idle: {stopped!r}")
            if int(stopped.get("boundHits", 0)) != 0:
                raise RuntimeError(f"Unexpected desktop bound hit in central motion proof: {stopped!r}")

            observed_seconds = max(0.001, duration)
            observed_frames = int(stopped["frame"]) - int(start["frame"])
            observed_fps = observed_frames / observed_seconds
            if observed_fps < 20:
                raise RuntimeError(f"Desktop movement runtime stalled: observed {observed_fps:.1f} fps")
            if not 2.0 <= duration <= 6.0:
                raise RuntimeError(f"Desktop motion exercise must span 2-6 seconds, got {duration:.3f}")

            assert_no_errors(console_errors, page_errors, "desktop movement")
            result = {
                "viewport": {"id": "desktop_reference", "width": 1280, "height": 720},
                "exercise_seconds": round(duration, 3),
                "observed_frames": observed_frames,
                "observed_fps": round(observed_fps, 2),
                "start": start,
                "early": early,
                "cruise": cruise,
                "diagonal": diagonal,
                "stopped": stopped,
                "console_error_count": len(console_errors),
                "page_error_count": len(page_errors),
            }
        finally:
            context.close()

        if video is None:
            raise RuntimeError("Playwright did not expose desktop video")
        video.save_as(str(video_path))

    if not video_path.is_file() or video_path.stat().st_size == 0:
        raise RuntimeError("Desktop motion video is missing")
    result["video_file"] = video_path.relative_to(output_root).as_posix()
    result["video_sha256"] = sha256_file(video_path)
    result["frame_files"] = [path.relative_to(output_root).as_posix() for path in sorted(frames_dir.glob("*.png"))]
    return result


def dispatch_touch(session, event_type: str, points: list[dict[str, object]]) -> None:
    session.send("Input.dispatchTouchEvent", {"type": event_type, "touchPoints": points})


def record_touch_motion(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    frames_dir = output_root / "movement_dense" / "mobile_landscape_frames"
    video_path = output_root / "movement_dense" / "mobile_landscape.webm"
    video_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="bebee-touch-video-") as video_dir:
        context = browser.new_context(
            viewport={"width": 844, "height": 390},
            screen={"width": 844, "height": 390},
            device_scale_factor=1,
            has_touch=True,
            is_mobile=True,
            record_video_dir=video_dir,
            record_video_size={"width": 844, "height": 390},
        )
        page = context.new_page()
        video = page.video
        console_errors, page_errors = install_error_capture(page)
        session = context.new_cdp_session(page)
        session.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 1})
        url = with_query(base_url, qa="movement_dense", qa_seed=88008)
        try:
            page.goto(url, wait_until="load", timeout=timeout_ms)
            start = wait_ready(page, head_sha=head_sha, state_id="movement_dense", timeout_ms=timeout_ms)
            screenshot(page, frames_dir / "00-idle.png")

            anchor = {"x": 170, "y": 210, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}
            right = {"x": 290, "y": 210, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}
            diagonal_point = {"x": 275, "y": 125, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}

            t0 = time.monotonic()
            dispatch_touch(session, "touchStart", [anchor])
            page.wait_for_timeout(250)
            dispatch_touch(session, "touchMove", [right])
            page.wait_for_timeout(500)
            active = bridge(page)
            screenshot(page, frames_dir / "01-horizontal.png")
            page.wait_for_timeout(400)
            dispatch_touch(session, "touchMove", [diagonal_point])
            page.wait_for_timeout(500)
            diagonal = bridge(page)
            screenshot(page, frames_dir / "02-diagonal.png")
            dispatch_touch(session, "touchEnd", [])
            page.wait_for_timeout(500)
            stopped = bridge(page)
            screenshot(page, frames_dir / "03-stopped.png")
            duration = time.monotonic() - t0

            if active.get("inputSource") != "touch" or float(active["speed"]) <= 100:
                raise RuntimeError(f"Touch drag did not drive movement: {active!r}")
            if float(active["beeX"]) - float(start["beeX"]) <= 50:
                raise RuntimeError(f"Touch displacement too small: start={start!r} active={active!r}")
            touch_intent = math.hypot(float(diagonal["intentX"]), float(diagonal["intentY"]))
            if diagonal.get("inputSource") != "touch" or touch_intent <= 0.4 or touch_intent > 1.02:
                raise RuntimeError(f"Touch diagonal intent invalid: {diagonal!r}")
            if float(stopped["speed"]) > 5 or stopped.get("inputSource") != "none":
                raise RuntimeError(f"Touch release did not clear movement: {stopped!r}")
            if not 2.0 <= duration <= 6.0:
                raise RuntimeError(f"Touch motion exercise must span 2-6 seconds, got {duration:.3f}")

            assert_no_errors(console_errors, page_errors, "touch movement")
            result = {
                "viewport": {"id": "mobile_landscape", "width": 844, "height": 390},
                "exercise_seconds": round(duration, 3),
                "start": start,
                "active": active,
                "diagonal": diagonal,
                "stopped": stopped,
                "console_error_count": len(console_errors),
                "page_error_count": len(page_errors),
            }
        finally:
            context.close()

        if video is None:
            raise RuntimeError("Playwright did not expose touch video")
        video.save_as(str(video_path))

    if not video_path.is_file() or video_path.stat().st_size == 0:
        raise RuntimeError("Touch motion video is missing")
    result["video_file"] = video_path.relative_to(output_root).as_posix()
    result["video_sha256"] = sha256_file(video_path)
    result["frame_files"] = [path.relative_to(output_root).as_posix() for path in sorted(frames_dir.glob("*.png"))]
    return result


def verify_modal_and_reduced_motion(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    timeout_ms: int,
) -> dict[str, object]:
    context: BrowserContext = browser.new_context(
        viewport={"width": 1280, "height": 720},
        screen={"width": 1280, "height": 720},
        device_scale_factor=1,
    )
    page = context.new_page()
    console_errors, page_errors = install_error_capture(page)
    console_lines: list[str] = []
    page.on("console", lambda message: console_lines.append(message.text))
    url = with_query(base_url, qa="movement_empty", qa_seed=88008, reduced_motion=1)
    try:
        page.goto(url, wait_until="load", timeout=timeout_ms)
        start = wait_ready(page, head_sha=head_sha, state_id="movement_empty", timeout_ms=timeout_ms)
        if start.get("reducedMotion") is not True:
            raise RuntimeError(f"Reduced-motion override was not applied: {start!r}")

        page.keyboard.down("d")
        page.wait_for_timeout(700)
        moving = bridge(page)
        page.keyboard.up("d")
        page.wait_for_timeout(300)
        if abs(float(moving["beeX"]) - float(moving["cameraX"])) > 0.1:
            raise RuntimeError(f"Reduced-motion camera retained horizontal lag: {moving!r}")
        if abs(float(moving["beeY"]) - float(moving["cameraY"])) > 0.1:
            raise RuntimeError(f"Reduced-motion camera retained vertical lag: {moving!r}")

        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
        if not any("BEBEE_INPUT modal_open focus_acquired" in line for line in console_lines):
            raise RuntimeError(f"Modal did not acquire focus: {console_lines!r}")
        before_modal = bridge(page)
        page.keyboard.down("d")
        page.wait_for_timeout(550)
        page.keyboard.up("d")
        page.wait_for_timeout(250)
        after_modal = bridge(page)
        if abs(float(after_modal["beeX"]) - float(before_modal["beeX"])) > 1.0:
            raise RuntimeError(
                f"Movement leaked through modal focus: before={before_modal!r} after={after_modal!r}"
            )
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        if not any("BEBEE_INPUT modal_closed focus_released" in line for line in console_lines):
            raise RuntimeError(f"Modal did not release focus: {console_lines!r}")
        assert_no_errors(console_errors, page_errors, "modal/reduced-motion")
        return {
            "reduced_motion_applied": True,
            "camera_lag_abs_x": round(abs(float(moving["beeX"]) - float(moving["cameraX"])), 4),
            "camera_lag_abs_y": round(abs(float(moving["beeY"]) - float(moving["cameraY"])), 4),
            "modal_displacement": round(abs(float(after_modal["beeX"]) - float(before_modal["beeX"])), 4),
            "modal_focus_consumed_movement": True,
            "console_error_count": len(console_errors),
            "page_error_count": len(page_errors),
        }
    finally:
        context.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--url", default="http://127.0.0.1:8000/development/BeBee/")
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=20)
    args = parser.parse_args()

    head_sha = args.head_sha.strip().lower()
    if len(head_sha) != 40 or any(character not in "0123456789abcdef" for character in head_sha):
        raise RuntimeError("--head-sha must be a full 40-character Git SHA")
    output_root = args.output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    timeout_ms = args.timeout_seconds * 1000

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            desktop = record_desktop_motion(
                browser,
                base_url=args.url,
                head_sha=head_sha,
                output_root=output_root,
                timeout_ms=timeout_ms,
            )
            touch = record_touch_motion(
                browser,
                base_url=args.url,
                head_sha=head_sha,
                output_root=output_root,
                timeout_ms=timeout_ms,
            )
            safety = verify_modal_and_reduced_motion(
                browser,
                base_url=args.url,
                head_sha=head_sha,
                timeout_ms=timeout_ms,
            )
            browser_version = browser.version
        finally:
            browser.close()

    report = {
        "schema_version": 1,
        "ticket": "P1-BEE-MOVEMENT",
        "head_sha": head_sha,
        "browser_name": "Playwright Chromium",
        "browser_version": browser_version,
        "qa_seed": 88008,
        "desktop_keyboard": desktop,
        "mobile_touch": touch,
        "focus_and_accessibility": safety,
        "result": "PASS",
    }
    report_path = output_root / "motion-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "P1 movement browser proof: PASS "
        f"(desktop {desktop['exercise_seconds']}s, touch {touch['exercise_seconds']}s, "
        f"observed desktop {desktop['observed_fps']} fps)"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"P1 movement browser proof failed: {exc}")
        raise SystemExit(1)
