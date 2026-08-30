#!/usr/bin/env python3
"""P6 browser proof for the complete Sunny Meadows vertical slice."""
from __future__ import annotations

import math
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import Browser, Page


HIVE = (1120.0, 800.0)
PLOT1 = (1410.0, 1110.0)
PATCHES = [
    (1550.0, 800.0),
    (1950.0, 840.0),
    (2070.0, 1160.0),
    (2120.0, 340.0),
    (1450.0, 300.0),
    (730.0, 430.0),
    (430.0, 980.0),
    (760.0, 1380.0),
]
RELEASE_BUNDLE_BUDGET_BYTES = 12 * 1024 * 1024
MIN_ENGINE_FPS = 50.0


def _url(base: str, **values: object) -> str:
    parsed = urlsplit(base)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.update({key: str(value) for key, value in values.items()})
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def _errors(page: Page) -> tuple[list[str], list[str]]:
    console: list[str] = []
    page_errors: list[str] = []
    page.on("console", lambda message: console.append(message.text) if message.type in {"error", "assert"} else None)
    page.on("pageerror", lambda error: page_errors.append(str(error)))
    return console, page_errors


def _external_requests(page: Page, base_url: str) -> list[str]:
    expected = urlsplit(base_url).netloc
    external: list[str] = []

    def on_request(request) -> None:
        parsed = urlsplit(request.url)
        if parsed.scheme in {"http", "https"} and parsed.netloc != expected:
            external.append(request.url)

    page.on("request", on_request)
    return external


def _assert_clean(console: list[str], page_errors: list[str], external: list[str], label: str) -> None:
    if console or page_errors or external:
        raise RuntimeError(f"{label}: console={console!r} page={page_errors!r} external={external!r}")


def _bridge(page: Page, name: str) -> dict[str, object]:
    value = page.evaluate(f"() => window.{name} ? structuredClone(window.{name}) : null")
    if not isinstance(value, dict):
        raise RuntimeError(f"{name} bridge missing")
    return value


def _movement(page: Page) -> dict[str, object]:
    return _bridge(page, "__bebeeMovementQA")


def _pollination(page: Page) -> dict[str, object]:
    return _bridge(page, "__bebeePollinationQA")


def _progression(page: Page) -> dict[str, object]:
    return _bridge(page, "__bebeeProgressionQA")


def _seed(page: Page) -> dict[str, object]:
    return _bridge(page, "__bebeeSeedQA")


def _region(page: Page) -> dict[str, object]:
    return _bridge(page, "__bebeeRegionQA")


def _wait(page: Page, head_sha: str, state: str, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        "() => window.__bebeeQA && window.__bebeeQA.captureReady === true && "
        "!!window.__bebeeMovementQA && !!window.__bebeePollinationQA && !!window.__bebeeProgressionQA && "
        "!!window.__bebeeSeedQA && !!window.__bebeeRegionQA",
        timeout=timeout_ms,
    )
    qa = page.evaluate("() => structuredClone(window.__bebeeQA)")
    if qa.get("stateId") != state or qa.get("buildCommitSha") != head_sha:
        raise RuntimeError(f"P6 provenance mismatch: {qa!r}")
    return _region(page)


def _shot(page: Page, path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path), full_page=False, animations="disabled")
    return path.as_posix()


def _release(page: Page) -> None:
    for key in ("w", "a", "s", "d"):
        try:
            page.keyboard.up(key)
        except Exception:
            pass


def _move_to(page: Page, x: float, y: float, *, timeout_seconds: float = 16.0, tolerance: float = 50.0) -> dict[str, object]:
    deadline = time.monotonic() + timeout_seconds
    try:
        while time.monotonic() < deadline:
            current = _movement(page)
            dx = x - float(current["beeX"])
            dy = y - float(current["beeY"])
            distance = math.hypot(dx, dy)
            if distance <= tolerance:
                _release(page)
                page.wait_for_timeout(100)
                return _movement(page)
            keys: list[str] = []
            deadband = min(18.0, tolerance / math.sqrt(2.0))
            if dx > deadband:
                keys.append("d")
            elif dx < -deadband:
                keys.append("a")
            if dy > deadband:
                keys.append("w")
            elif dy < -deadband:
                keys.append("s")
            for key in keys:
                page.keyboard.down(key)
            page.wait_for_timeout(65 if distance < 130 else 130)
            for key in keys:
                page.keyboard.up(key)
            page.wait_for_timeout(20)
    finally:
        _release(page)
    raise RuntimeError(f"could not move bee to ({x},{y}); last={_movement(page)!r}")


def _patch(page: Page, index: int) -> dict[str, object]:
    patches = _pollination(page).get("patches")
    if not isinstance(patches, list) or len(patches) < index:
        raise RuntimeError(f"patch {index} missing from pollination bridge")
    payload = patches[index - 1]
    if not isinstance(payload, dict):
        raise RuntimeError(f"patch {index} payload invalid: {payload!r}")
    return payload


def _complete_patch(page: Page, index: int, *, timeout_seconds: float = 22.0) -> dict[str, object]:
    x, y = PATCHES[index - 1]
    _move_to(page, x, y, tolerance=52)
    deadline = time.monotonic() + timeout_seconds
    direction_right = True
    while time.monotonic() < deadline:
        current = _patch(page, index)
        if current.get("state") == "COMPLETED":
            return current
        _move_to(page, x + (72 if direction_right else -72), y, timeout_seconds=3.0, tolerance=20)
        direction_right = not direction_right
    raise RuntimeError(f"patch {index} did not complete: {_patch(page, index)!r}")


def _dispatch_key(session, page: Page, key_code: int) -> None:
    common = {"windowsVirtualKeyCode": key_code, "nativeVirtualKeyCode": key_code}
    session.send("Input.dispatchKeyEvent", {"type": "rawKeyDown", **common})
    page.wait_for_timeout(90)
    session.send("Input.dispatchKeyEvent", {"type": "keyUp", **common})
    page.wait_for_timeout(140)


def _buy_upgrade(page: Page, session, upgrade: str, expected_level: int, timeout_ms: int) -> dict[str, object]:
    _move_to(page, HIVE[0], HIVE[1], tolerance=70)
    _dispatch_key(session, page, 32)
    page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === true", timeout=timeout_ms)
    if upgrade == "buzz":
        _dispatch_key(session, page, 39)
        page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.selectedUpgrade === 'buzz'", timeout=timeout_ms)
    else:
        _dispatch_key(session, page, 37)
        page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.selectedUpgrade === 'flight'", timeout=timeout_ms)
    _dispatch_key(session, page, 32)
    field = "buzzLevel" if upgrade == "buzz" else "flightLevel"
    page.wait_for_function(f"() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.{field} === {expected_level}", timeout=timeout_ms)
    result = _progression(page)
    _dispatch_key(session, page, 27)
    page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === false", timeout=timeout_ms)
    return result


def _plant_daisy(page: Page, session, timeout_ms: int) -> dict[str, object]:
    _move_to(page, PLOT1[0], PLOT1[1], tolerance=65)
    _dispatch_key(session, page, 32)
    page.wait_for_function(
        "() => window.__bebeeSeedQA && window.__bebeeSeedQA.plot1 && window.__bebeeSeedQA.plot1.currentFlowerId === 'flower_daisy'",
        timeout=timeout_ms,
    )
    return _seed(page)


def _canvas_metrics(page: Page) -> dict[str, float]:
    metrics = page.evaluate(
        """() => {
            const c = document.querySelector('canvas');
            if (!c) return null;
            const r = c.getBoundingClientRect();
            return {x:r.x,y:r.y,width:r.width,height:r.height,viewportWidth:innerWidth,viewportHeight:innerHeight};
        }"""
    )
    if not isinstance(metrics, dict):
        raise RuntimeError("P6 canvas missing")
    return {key: float(value) for key, value in metrics.items()}


def _canonical(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict[str, object]:
    cases = [
        ("region_start", "desktop_reference", 1280, 720, False),
        ("region_mid", "desktop_reference", 1280, 720, False),
        ("region_complete", "desktop_reference", 1280, 720, False),
        ("region_complete", "mobile_landscape", 844, 390, True),
        ("settings_accessibility", "mobile_landscape", 844, 390, True),
        ("region_mid", "poki_small", 640, 360, False),
        ("region_mid", "poki_medium", 836, 470, False),
        ("region_mid", "poki_large", 1031, 580, False),
    ]
    results: dict[str, object] = {}
    for state, viewport_id, width, height, touch in cases:
        viewport = {"width": width, "height": height}
        context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1, has_touch=touch, is_mobile=touch)
        page = context.new_page()
        console, page_errors = _errors(page)
        external = _external_requests(page, base_url)
        label = f"{state}-{viewport_id}"
        try:
            page.goto(_url(base_url, qa=state, qa_seed=88008), wait_until="load", timeout=timeout_ms)
            payload = _wait(page, head_sha, state, timeout_ms)
            metrics = _canvas_metrics(page)
            if metrics["width"] + 1 < width or metrics["height"] + 1 < height:
                raise RuntimeError(f"P6 canvas does not cover {viewport_id}: {metrics!r}")
            shot = output_root / "p6_region" / "canonical" / f"{label}.png"
            _shot(page, shot)
            _assert_clean(console, page_errors, external, f"P6 canonical {label}")
            results[label] = {
                "viewport": {"id": viewport_id, **viewport},
                "region": payload.get("region"),
                "objective_text": payload.get("objectiveText"),
                "settings": payload.get("settings"),
                "canvas": metrics,
                "screenshot": shot.relative_to(output_root).as_posix(),
                "console_error_count": len(console),
                "page_error_count": len(page_errors),
                "external_request_count": len(external),
            }
        finally:
            context.close()
    return results


def _journey(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict[str, object]:
    viewport = {"width": 1280, "height": 720}
    frames = output_root / "p6_region" / "clean_save_journey"
    context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1)
    page = context.new_page()
    console, page_errors = _errors(page)
    external = _external_requests(page, base_url)
    session = context.new_cdp_session(page)
    checkpoints: list[dict[str, object]] = []
    try:
        page.goto(_url(base_url, qa="region_start", qa_seed=88008, p6_storage_lifecycle="reset"), wait_until="load", timeout=timeout_ms)
        start = _wait(page, head_sha, "region_start", timeout_ms)
        if int(start.get("saveVersion", -1)) != 4 or int(start.get("honey", -1)) != 0:
            raise RuntimeError(f"P6 clean start invalid: {start!r}")
        _shot(page, frames / "00-start.png")

        _complete_patch(page, 1)
        planted = _plant_daisy(page, session, timeout_ms)
        if int(planted.get("honey", -1)) != 30:
            raise RuntimeError(f"P6 Daisy transaction invalid: {planted!r}")
        flight2 = _buy_upgrade(page, session, "flight", 2, timeout_ms)
        if int(flight2.get("honey", -1)) != 0 or float(flight2.get("flightMaxSpeed", 0)) != 330:
            raise RuntimeError(f"P6 Flight 2 invalid: {flight2!r}")

        _complete_patch(page, 2)
        buzz2 = _buy_upgrade(page, session, "buzz", 2, timeout_ms)
        if int(buzz2.get("honey", -1)) != 20 or abs(float(buzz2.get("buzzWorkMultiplier", 0)) - 1.35) > 0.001:
            raise RuntimeError(f"P6 Buzz 2 invalid: {buzz2!r}")
        _complete_patch(page, 3)
        after_m1 = _region(page)
        if int((after_m1.get("region") or {}).get("restored_count", -1)) != 1:
            raise RuntimeError(f"P6 first Meadow did not restore: {after_m1!r}")
        _shot(page, frames / "01-first-meadow-restored.png")

        _complete_patch(page, 4)
        _complete_patch(page, 5)
        flight3 = _buy_upgrade(page, session, "flight", 3, timeout_ms)
        if float(flight3.get("flightMaxSpeed", 0)) != 360:
            raise RuntimeError(f"P6 Flight 3 runtime effect invalid: {flight3!r}")
        _complete_patch(page, 6)
        _complete_patch(page, 7)
        lily_locked = _patch(page, 8)
        if lily_locked.get("state") != "LOCKED" or lily_locked.get("eligibilityReason") != "requires_buzz" or int(lily_locked.get("requirement", -1)) != 3:
            raise RuntimeError(f"P6 Lily Buzz-3 gate invalid: {lily_locked!r}")
        _shot(page, frames / "02-lily-buzz3-gate.png")

        buzz3 = _buy_upgrade(page, session, "buzz", 3, timeout_ms)
        if abs(float(buzz3.get("buzzWorkMultiplier", 0)) - 1.65) > 0.001:
            raise RuntimeError(f"P6 Buzz 3 runtime effect invalid: {buzz3!r}")
        lily_unlocked = _patch(page, 8)
        if lily_unlocked.get("eligible") is not True:
            raise RuntimeError(f"P6 Lily did not unlock after Buzz 3: {lily_unlocked!r}")
        _complete_patch(page, 8)
        complete = _region(page)
        summary = complete.get("region") or {}
        if summary.get("complete") is not True or int(summary.get("restored_count", -1)) != 6:
            raise RuntimeError(f"P6 region did not complete: {complete!r}")
        if int(complete.get("honey", -1)) != 386 or int(complete.get("flightLevel", -1)) != 3 or int(complete.get("buzzLevel", -1)) != 3:
            raise RuntimeError(f"P6 final economy/progression mismatch: {complete!r}")
        if complete.get("playerPlants", {}).get("r01_m01_player_plot_01") != "flower_daisy":
            raise RuntimeError(f"P6 player plot lost during campaign: {complete!r}")
        _shot(page, frames / "03-region-complete.png")

        _dispatch_key(session, page, 27)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === true", timeout=timeout_ms)
        _dispatch_key(session, page, 32)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settings.reduced_motion === true", timeout=timeout_ms)
        _dispatch_key(session, page, 40)
        _dispatch_key(session, page, 32)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settings.audio_muted === true", timeout=timeout_ms)
        settings = _region(page)
        _shot(page, frames / "04-settings-enabled.png")
        _dispatch_key(session, page, 27)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === false", timeout=timeout_ms)

        events = _region(page).get("analyticsEvents") or []
        names = [event.get("name") for event in events if isinstance(event, dict)]
        for required in ("session_start", "first_input", "patch_completed", "meadow_restored", "region_completed", "settings_changed"):
            if required not in names:
                raise RuntimeError(f"P6 analytics event missing {required}: {names!r}")

        page.wait_for_timeout(1500)
        page.goto(_url(base_url, qa="region_complete", qa_seed=88008, p6_storage_lifecycle="reload"), wait_until="load", timeout=timeout_ms)
        reloaded = _wait(page, head_sha, "region_complete", timeout_ms)
        reload_summary = reloaded.get("region") or {}
        reload_settings = reloaded.get("settings") or {}
        if reload_summary.get("complete") is not True or int(reload_summary.get("restored_count", -1)) != 6:
            raise RuntimeError(f"P6 completed region did not survive reload: {reloaded!r}")
        if int(reloaded.get("honey", -1)) != 386 or int(reloaded.get("flightLevel", -1)) != 3 or int(reloaded.get("buzzLevel", -1)) != 3:
            raise RuntimeError(f"P6 progression did not survive reload: {reloaded!r}")
        if reload_settings.get("reduced_motion") is not True or reload_settings.get("audio_muted") is not True:
            raise RuntimeError(f"P6 settings did not survive reload: {reloaded!r}")
        if reloaded.get("playerPlants", {}).get("r01_m01_player_plot_01") != "flower_daisy":
            raise RuntimeError(f"P6 planted species did not survive reload: {reloaded!r}")
        _shot(page, frames / "05-reloaded-complete.png")

        frame_before = int(_movement(page).get("frame", 0))
        wall_before = time.monotonic()
        page.wait_for_timeout(2200)
        wall_seconds = time.monotonic() - wall_before
        frame_after = int(_movement(page).get("frame", 0))
        engine_fps = (frame_after - frame_before) / wall_seconds if wall_seconds > 0 else 0.0
        if engine_fps < MIN_ENGINE_FPS:
            raise RuntimeError(f"P6 engine fps below budget: {engine_fps:.2f} < {MIN_ENGINE_FPS}")

        _assert_clean(console, page_errors, external, "P6 clean-save journey")
        checkpoints.extend([start, after_m1, complete, settings, reloaded])
        return {
            "viewport": {"id": "desktop_reference", **viewport},
            "final_honey": int(reloaded["honey"]),
            "flight_level": int(reloaded["flightLevel"]),
            "buzz_level": int(reloaded["buzzLevel"]),
            "lily_gate_before_buzz3": lily_locked,
            "lily_after_buzz3": lily_unlocked,
            "settings": reload_settings,
            "analytics_event_names": names,
            "engine_fps": round(engine_fps, 2),
            "min_engine_fps_budget": MIN_ENGINE_FPS,
            "frame_files": [path.relative_to(output_root).as_posix() for path in sorted(frames.glob("*.png"))],
            "console_error_count": len(console),
            "page_error_count": len(page_errors),
            "external_request_count": len(external),
        }
    finally:
        context.close()


def _bundle_measurement() -> dict[str, object]:
    root = Path("build/html5/release/BeBee")
    files = [path for path in root.rglob("*") if path.is_file()]
    total = sum(path.stat().st_size for path in files)
    if not files:
        raise RuntimeError("P6 release bundle files missing")
    if total > RELEASE_BUNDLE_BUDGET_BYTES:
        raise RuntimeError(f"P6 release bundle above budget: {total} > {RELEASE_BUNDLE_BUDGET_BYTES}")
    return {
        "release_bundle_bytes": total,
        "release_bundle_file_count": len(files),
        "budget_bytes": RELEASE_BUNDLE_BUDGET_BYTES,
        "result": "PASS",
    }


def record_region(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict[str, object]:
    canonical = _canonical(browser, base_url=base_url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
    journey = _journey(browser, base_url=base_url, head_sha=head_sha, output_root=output_root, timeout_ms=max(timeout_ms, 30000))
    bundle = _bundle_measurement()
    return {
        "ticket": "P6-FIRST-REGION-VERTICAL-SLICE",
        "canonical": canonical,
        "clean_save_journey": journey,
        "performance": {"engine_fps": journey["engine_fps"], "min_engine_fps_budget": MIN_ENGINE_FPS, **bundle},
        "result": "PASS",
    }
