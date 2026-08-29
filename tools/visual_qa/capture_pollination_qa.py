#!/usr/bin/env python3
"""P2 browser proof for movement-through pollination, canonical states, Honey and reload."""

from __future__ import annotations

import hashlib
import tempfile
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import Browser, Page


def _with_query(base_url: str, **values: object) -> str:
    parsed = urlsplit(base_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for key, value in values.items():
        query[key] = str(value)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _errors(page: Page) -> tuple[list[str], list[str]]:
    console_errors: list[str] = []
    page_errors: list[str] = []
    page.on("console", lambda message: console_errors.append(message.text) if message.type in {"error", "assert"} else None)
    page.on("pageerror", lambda error: page_errors.append(str(error)))
    return console_errors, page_errors


def _bridge(page: Page) -> dict[str, object]:
    value = page.evaluate("() => window.__bebeePollinationQA ? structuredClone(window.__bebeePollinationQA) : null")
    if not isinstance(value, dict):
        raise RuntimeError("window.__bebeePollinationQA is not available")
    return value


def _wait_ready(page: Page, *, head_sha: str, state_id: str, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        """() => {
            const qa = window.__bebeeQA;
            return !!qa && qa.captureReady === true && !!window.__bebeePollinationQA;
        }""",
        timeout=timeout_ms,
    )
    qa = page.evaluate("() => structuredClone(window.__bebeeQA)")
    if qa.get("stateId") != state_id:
        raise RuntimeError(f"pollination QA state mismatch: {qa!r}")
    if qa.get("buildCommitSha") != head_sha:
        raise RuntimeError(f"pollination QA head mismatch: {qa!r}")
    return _bridge(page)


def _shot(page: Page, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path), full_page=False, animations="disabled")


def _assert_clean(console_errors: list[str], page_errors: list[str], label: str) -> None:
    if console_errors or page_errors:
        raise RuntimeError(f"{label} browser errors: console={console_errors!r} page={page_errors!r}")


def _patch(payload: dict[str, object], key: str = "patch1") -> dict[str, object]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise RuntimeError(f"missing {key} payload: {payload!r}")
    return value


def _capture_canonical_stills(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> list[dict[str, object]]:
    matrix = [
        ("pollination_idle", "desktop_reference", 1280, 720),
        ("pollination_active_50", "desktop_reference", 1280, 720),
        ("pollination_active_50", "poki_small", 640, 360),
        ("pollination_active_50", "mobile_landscape", 844, 390),
        ("pollination_complete", "desktop_reference", 1280, 720),
        ("hud_default", "desktop_reference", 1280, 720),
        ("hud_default", "poki_small", 640, 360),
        ("hud_default", "poki_medium", 836, 470),
        ("hud_default", "poki_large", 1031, 580),
        ("hud_default", "mobile_landscape", 844, 390),
    ]
    records: list[dict[str, object]] = []
    for state_id, viewport_id, width, height in matrix:
        context = browser.new_context(
            viewport={"width": width, "height": height},
            screen={"width": width, "height": height},
            device_scale_factor=1,
            has_touch=viewport_id == "mobile_landscape",
            is_mobile=viewport_id == "mobile_landscape",
        )
        page = context.new_page()
        console_errors, page_errors = _errors(page)
        try:
            page.goto(_with_query(base_url, qa=state_id, qa_seed=88008), wait_until="load", timeout=timeout_ms)
            payload = _wait_ready(page, head_sha=head_sha, state_id=state_id, timeout_ms=timeout_ms)
            if state_id == "pollination_idle" and _patch(payload)["state"] != "AVAILABLE":
                raise RuntimeError(f"canonical idle fixture invalid: {payload!r}")
            if state_id == "pollination_active_50":
                progress = float(_patch(payload)["progress"])
                if _patch(payload)["state"] != "ACTIVE" or abs(progress - 0.5) > 0.01:
                    raise RuntimeError(f"canonical 50% fixture invalid: {payload!r}")
            if state_id == "pollination_complete":
                if _patch(payload)["state"] != "COMPLETED" or int(payload.get("honey", -1)) != 45:
                    raise RuntimeError(f"canonical completion fixture invalid: {payload!r}")
            _assert_clean(console_errors, page_errors, f"canonical {state_id}/{viewport_id}")
            path = output_root / state_id / f"{viewport_id}.png"
            _shot(page, path)
            records.append({
                "state_id": state_id,
                "viewport_id": viewport_id,
                "width": width,
                "height": height,
                "capture_file": path.relative_to(output_root).as_posix(),
                "capture_sha256": _sha256(path),
                "console_error_count": len(console_errors),
                "page_error_count": len(page_errors),
            })
        finally:
            context.close()
    return records


def _record_desktop(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    frames = output_root / "pollination_core" / "desktop_reference_frames"
    video_path = output_root / "pollination_core" / "desktop_reference.webm"
    video_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="bebee-p2-desktop-") as video_dir:
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            screen={"width": 1280, "height": 720},
            device_scale_factor=1,
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        video = page.video
        console_errors, page_errors = _errors(page)
        try:
            page.goto(
                _with_query(base_url, qa="pollination_idle", qa_seed=88008, p2_storage_lifecycle="reset"),
                wait_until="load",
                timeout=timeout_ms,
            )
            before = _wait_ready(page, head_sha=head_sha, state_id="pollination_idle", timeout_ms=timeout_ms)
            _shot(page, frames / "00-before.png")
            if _patch(before)["state"] != "AVAILABLE" or _patch(before, "patch2")["state"] != "LOCKED":
                raise RuntimeError(f"unexpected initial P2 states: {before!r}")
            if int(before.get("honey", -1)) != 0:
                raise RuntimeError(f"P2 clean start Honey is not zero: {before!r}")
            if before.get("extraPollinationInput") is not False:
                raise RuntimeError(f"P2 unexpectedly exposes a pollination action: {before!r}")

            t0 = time.monotonic()
            page.keyboard.down("d")
            page.wait_for_timeout(1200)
            active = _bridge(page)
            _shot(page, frames / "01-active.png")
            if _patch(active)["state"] != "ACTIVE" or float(_patch(active)["work"]) <= 0:
                raise RuntimeError(f"movement did not activate pollination: {active!r}")

            page.wait_for_timeout(900)
            page.keyboard.up("d")
            page.wait_for_timeout(450)
            straight_pass = _bridge(page)
            _shot(page, frames / "02-straight-pass-incomplete.png")
            if _patch(straight_pass)["state"] == "COMPLETED":
                raise RuntimeError(f"one straight forgiving-zone pass completed the patch: {straight_pass!r}")
            straight_work = float(_patch(straight_pass)["work"])
            target = float(_patch(straight_pass)["workTarget"])
            if straight_work <= target * 0.55 or straight_work >= target:
                raise RuntimeError(f"straight-pass work is outside intended partial-progress band: {straight_pass!r}")

            page.wait_for_timeout(700)
            stationary = _bridge(page)
            _shot(page, frames / "03-stationary-zero-work.png")
            stationary_delta = float(_patch(stationary)["work"]) - straight_work
            if abs(stationary_delta) > 0.1:
                raise RuntimeError(f"stationary time advanced pollination by {stationary_delta}: {stationary!r}")

            page.keyboard.down("a")
            page.wait_for_function(
                "() => window.__bebeePollinationQA && window.__bebeePollinationQA.patch1.state === 'COMPLETED'",
                timeout=3000,
            )
            completed = _bridge(page)
            _shot(page, frames / "04-completed.png")
            page.keyboard.up("a")
            page.wait_for_timeout(300)
            duration = time.monotonic() - t0

            if int(completed.get("honey", -1)) != 45:
                raise RuntimeError(f"completion did not award exactly one 45-Honey reward: {completed!r}")
            if int(completed.get("completionCount", -1)) != 1 or int(completed.get("rewardTransactions", -1)) != 1:
                raise RuntimeError(f"completion/reward was not single-shot: {completed!r}")
            if int(completed.get("audioHookCount", -1)) != 1:
                raise RuntimeError(f"completion audio hook did not fire exactly once: {completed!r}")
            if _patch(completed, "patch2")["state"] != "AVAILABLE":
                raise RuntimeError(f"second patch did not unlock: {completed!r}")
            if completed.get("saveCode") != "ok":
                raise RuntimeError(f"completion was not accepted by storage adapter: {completed!r}")

            page.wait_for_timeout(1600)
            page.goto(
                _with_query(base_url, qa="pollination_complete", qa_seed=88008, p2_storage_lifecycle="reload"),
                wait_until="load",
                timeout=timeout_ms,
            )
            reloaded = _wait_ready(page, head_sha=head_sha, state_id="pollination_complete", timeout_ms=timeout_ms)
            _shot(page, frames / "05-reloaded.png")
            if _patch(reloaded)["state"] != "COMPLETED" or int(reloaded.get("honey", -1)) != 45:
                raise RuntimeError(f"reload did not preserve completion/Honey: {reloaded!r}")
            if _patch(reloaded, "patch2")["state"] != "AVAILABLE":
                raise RuntimeError(f"reload did not preserve dependent unlock: {reloaded!r}")
            if int(reloaded.get("completionCount", -1)) != 0 or int(reloaded.get("rewardTransactions", -1)) != 0:
                raise RuntimeError(f"reload replayed completion/reward: {reloaded!r}")

            _assert_clean(console_errors, page_errors, "desktop P2")
            result = {
                "viewport": {"id": "desktop_reference", "width": 1280, "height": 720},
                "exercise_seconds": round(duration, 3),
                "before": before,
                "active": active,
                "straight_pass": straight_pass,
                "stationary": stationary,
                "stationary_work_delta": round(stationary_delta, 4),
                "completed": completed,
                "reloaded": reloaded,
                "console_error_count": len(console_errors),
                "page_error_count": len(page_errors),
            }
        finally:
            context.close()

        if video is None:
            raise RuntimeError("desktop P2 video handle missing")
        video.save_as(str(video_path))

    if not video_path.is_file() or video_path.stat().st_size == 0:
        raise RuntimeError("desktop P2 video missing")
    result["video_file"] = video_path.relative_to(output_root).as_posix()
    result["video_sha256"] = _sha256(video_path)
    result["frame_files"] = [p.relative_to(output_root).as_posix() for p in sorted(frames.glob("*.png"))]
    return result


def _dispatch_touch(session, event_type: str, points: list[dict[str, object]]) -> None:
    session.send("Input.dispatchTouchEvent", {"type": event_type, "touchPoints": points})


def _record_touch(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    frames = output_root / "pollination_core" / "mobile_landscape_frames"
    video_path = output_root / "pollination_core" / "mobile_landscape.webm"
    video_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="bebee-p2-touch-") as video_dir:
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
        console_errors, page_errors = _errors(page)
        session = context.new_cdp_session(page)
        session.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 1})
        try:
            page.goto(
                _with_query(base_url, qa="pollination_idle", qa_seed=88008, p2_storage_lifecycle="reset"),
                wait_until="load",
                timeout=timeout_ms,
            )
            before = _wait_ready(page, head_sha=head_sha, state_id="pollination_idle", timeout_ms=timeout_ms)
            _shot(page, frames / "00-before.png")

            anchor = {"x": 170, "y": 210, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}
            right = {"x": 290, "y": 210, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}
            left_anchor = {"x": 270, "y": 210, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}
            left = {"x": 150, "y": 210, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}

            _dispatch_touch(session, "touchStart", [anchor])
            page.wait_for_timeout(250)
            _dispatch_touch(session, "touchMove", [right])
            page.wait_for_timeout(2100)
            _dispatch_touch(session, "touchEnd", [])
            page.wait_for_timeout(450)
            partial = _bridge(page)
            _shot(page, frames / "01-straight-pass-incomplete.png")
            if _patch(partial)["state"] == "COMPLETED":
                raise RuntimeError(f"touch straight pass completed P2 patch: {partial!r}")

            _dispatch_touch(session, "touchStart", [left_anchor])
            page.wait_for_timeout(200)
            _dispatch_touch(session, "touchMove", [left])
            page.wait_for_function(
                "() => window.__bebeePollinationQA && window.__bebeePollinationQA.patch1.state === 'COMPLETED'",
                timeout=3500,
            )
            completed = _bridge(page)
            _shot(page, frames / "02-completed.png")
            _dispatch_touch(session, "touchEnd", [])
            page.wait_for_timeout(250)

            if int(completed.get("honey", -1)) != 45:
                raise RuntimeError(f"touch completion Honey mismatch: {completed!r}")
            if completed.get("extraPollinationInput") is not False:
                raise RuntimeError(f"touch path exposed extra pollination input: {completed!r}")
            _assert_clean(console_errors, page_errors, "touch P2")
            result = {
                "viewport": {"id": "mobile_landscape", "width": 844, "height": 390},
                "before": before,
                "straight_pass": partial,
                "completed": completed,
                "console_error_count": len(console_errors),
                "page_error_count": len(page_errors),
            }
        finally:
            context.close()

        if video is None:
            raise RuntimeError("touch P2 video handle missing")
        video.save_as(str(video_path))

    if not video_path.is_file() or video_path.stat().st_size == 0:
        raise RuntimeError("touch P2 video missing")
    result["video_file"] = video_path.relative_to(output_root).as_posix()
    result["video_sha256"] = _sha256(video_path)
    result["frame_files"] = [p.relative_to(output_root).as_posix() for p in sorted(frames.glob("*.png"))]
    return result


def record_pollination_core(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    canonical_stills = _capture_canonical_stills(
        browser,
        base_url=base_url,
        head_sha=head_sha,
        output_root=output_root,
        timeout_ms=timeout_ms,
    )
    desktop = _record_desktop(
        browser,
        base_url=base_url,
        head_sha=head_sha,
        output_root=output_root,
        timeout_ms=timeout_ms,
    )
    touch = _record_touch(
        browser,
        base_url=base_url,
        head_sha=head_sha,
        output_root=output_root,
        timeout_ms=timeout_ms,
    )
    return {
        "ticket": "P2-POLLINATION-CORE-LOOP",
        "canonical_stills": canonical_stills,
        "desktop_keyboard": desktop,
        "mobile_touch": touch,
        "result": "PASS",
    }
