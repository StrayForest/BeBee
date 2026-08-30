#!/usr/bin/env python3
"""P5 browser proof for seed ownership, player-shaped plots, free replant and persistence."""
from __future__ import annotations

import math
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import Browser, Page


def _url(base: str, **values: object) -> str:
    parsed = urlsplit(base)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.update({key: str(value) for key, value in values.items()})
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def _errors(page: Page):
    console=[]; page_errors=[]; platform_request_seen=False

    def on_request(request):
        nonlocal platform_request_seen
        if 'ads.poki.com' in request.url or 'crazygames.com' in request.url:
            platform_request_seen=True

    def on_console(message):
        if message.type not in {'error','assert'}:
            return
        text=message.text
        if 'ads.poki.com' in text or 'crazygames.com' in text:
            return
        if platform_request_seen and 'Failed to load resource: net::ERR_FAILED' in text:
            return
        if 'Cross-Origin-Opener-Policy header has been ignored' in text:
            return
        console.append(text)

    page.on('request', on_request)
    page.on('console', on_console)
    page.on('pageerror', lambda e: page_errors.append(str(e)))
    return console,page_errors



def _assert_clean(console: list[str], page_errors: list[str], label: str) -> None:
    if console or page_errors:
        raise RuntimeError(f"{label}: console={console!r} page={page_errors!r}")


def _bridge(page: Page, name: str) -> dict[str, object]:
    value = page.evaluate(f"() => window.{name} ? structuredClone(window.{name}) : null")
    if not isinstance(value, dict):
        raise RuntimeError(f"{name} bridge missing")
    return value


def _movement(page: Page) -> dict[str, object]:
    return _bridge(page, "__bebeeMovementQA")


def _pollination(page: Page) -> dict[str, object]:
    return _bridge(page, "__bebeePollinationQA")


def _seed(page: Page) -> dict[str, object]:
    return _bridge(page, "__bebeeSeedQA")


def _wait(page: Page, head_sha: str, state: str, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        "() => window.__bebeeQA && window.__bebeeQA.captureReady === true && "
        "!!window.__bebeeMovementQA && !!window.__bebeePollinationQA && !!window.__bebeeSeedQA",
        timeout=timeout_ms,
    )
    qa = page.evaluate("() => structuredClone(window.__bebeeQA)")
    if qa.get("stateId") != state or qa.get("buildCommitSha") != head_sha:
        raise RuntimeError(f"P5 provenance mismatch: {qa!r}")
    return _seed(page)


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


def _move_to(page: Page, x: float, y: float, *, timeout_seconds: float = 10.0, tolerance: float = 48.0) -> dict[str, object]:
    deadline = time.monotonic() + timeout_seconds
    try:
        while time.monotonic() < deadline:
            current = _movement(page)
            dx = x - float(current["beeX"])
            dy = y - float(current["beeY"])
            distance = math.hypot(dx, dy)
            if distance <= tolerance:
                _release(page)
                page.wait_for_timeout(120)
                settled = _movement(page)
                if math.hypot(x - float(settled["beeX"]), y - float(settled["beeY"])) <= tolerance * 1.55:
                    return settled
            keys: list[str] = []
            deadband = 18.0
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
            page.wait_for_timeout(70 if distance < 120 else 130)
            for key in keys:
                page.keyboard.up(key)
            page.wait_for_timeout(25)
    finally:
        _release(page)
    raise RuntimeError(f"could not move bee to ({x},{y}); last={_movement(page)!r}")


def _patch(page: Page, key: str) -> dict[str, object]:
    payload = _pollination(page).get(key)
    if not isinstance(payload, dict):
        raise RuntimeError(f"{key} missing from pollination bridge")
    return payload


def _complete_patch(page: Page, key: str, x: float, y: float, *, timeout_seconds: float = 14.0) -> dict[str, object]:
    _move_to(page, x, y, tolerance=55)
    deadline = time.monotonic() + timeout_seconds
    target_left = x - 68
    target_right = x + 68
    direction_right = True
    while time.monotonic() < deadline:
        current = _patch(page, key)
        if current.get("state") == "COMPLETED":
            return current
        _move_to(page, target_right if direction_right else target_left, y, timeout_seconds=2.5, tolerance=24)
        direction_right = not direction_right
    raise RuntimeError(f"{key} did not complete: {_patch(page, key)!r}")


def _dispatch_key(session, page: Page, key_code: int) -> None:
    common = {"windowsVirtualKeyCode": key_code, "nativeVirtualKeyCode": key_code}
    session.send("Input.dispatchKeyEvent", {"type": "rawKeyDown", **common})
    page.wait_for_timeout(100)
    session.send("Input.dispatchKeyEvent", {"type": "keyUp", **common})
    page.wait_for_timeout(140)


def _assert_owned(payload: dict[str, object], expected: list[str]) -> None:
    actual = payload.get("ownedSeedIds")
    if actual != expected:
        raise RuntimeError(f"owned seed mismatch expected={expected!r} payload={payload!r}")


def _canonical(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict[str, object]:
    results: dict[str, object] = {}
    for state, viewport in (
        ("seed_locked", {"width": 1280, "height": 720}),
        ("seed_unlocked", {"width": 1280, "height": 720}),
        ("seed_unlocked", {"width": 844, "height": 390}),
    ):
        context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1, has_touch=viewport["width"] == 844)
        page = context.new_page()
        console, page_errors = _errors(page)
        label = f"{state}-{viewport['width']}x{viewport['height']}"
        try:
            page.goto(_url(base_url, qa=state, qa_seed=88008), wait_until="load", timeout=timeout_ms)
            payload = _wait(page, head_sha, state, timeout_ms)
            plot1 = payload.get("plot1") or {}
            if state == "seed_locked":
                if plot1.get("available") is not False or plot1.get("actionCode") != "plot_locked" or plot1.get("currentFlowerId") is not None:
                    raise RuntimeError(f"seed_locked canonical fixture invalid: {payload!r}")
                if payload.get("nativePatch1Completed") is not False:
                    raise RuntimeError(f"seed_locked changed native campaign state: {payload!r}")
            else:
                _assert_owned(payload, ["seed_daisy"])
                if int(payload.get("saveVersion", -1)) != 4 or int(payload.get("honey", -1)) != 30:
                    raise RuntimeError(f"seed_unlocked save/economy fixture invalid: {payload!r}")
                if plot1.get("currentFlowerId") != "flower_daisy" or payload.get("nativePatch1Completed") is not True or payload.get("nativePatch2Completed") is not False:
                    raise RuntimeError(f"seed_unlocked canonical fixture invalid: {payload!r}")
            shot = output_root / "p5_seed" / "canonical" / f"{label}.png"
            _shot(page, shot)
            _assert_clean(console, page_errors, f"P5 canonical {label}")
            results[label] = {
                "viewport": viewport,
                "payload": payload,
                "screenshot": shot.relative_to(output_root).as_posix(),
                "console_error_count": len(console),
                "page_error_count": len(page_errors),
            }
        finally:
            context.close()
    return results


def _desktop_persistence(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict[str, object]:
    viewport = {"width": 1280, "height": 720}
    frames = output_root / "p5_seed" / "desktop_persistence"
    context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1)
    page = context.new_page()
    console, page_errors = _errors(page)
    session = context.new_cdp_session(page)
    try:
        page.goto(_url(base_url, qa="seed_locked", qa_seed=88008, p5_storage_lifecycle="reset"), wait_until="load", timeout=timeout_ms)
        start = _wait(page, head_sha, "seed_locked", timeout_ms)
        if int(start.get("honey", -1)) != 0 or start.get("nativePatch1Completed") is not False:
            raise RuntimeError(f"P5 reset did not start clean: {start!r}")
        _shot(page, frames / "00-native-before.png")

        _complete_patch(page, "patch1", 1550, 800)
        page.wait_for_function("() => window.__bebeeSeedQA && window.__bebeeSeedQA.nativePatch1Completed === true", timeout=timeout_ms)
        after_patch1 = _seed(page)
        plot1 = after_patch1.get("plot1") or {}
        if int(after_patch1.get("honey", -1)) != 45 or plot1.get("action") != "unlock_and_plant" or int(plot1.get("cost", -1)) != 15:
            raise RuntimeError(f"Daisy seed did not become available after native patch: {after_patch1!r}")
        _move_to(page, 1410, 1110, tolerance=65)
        _shot(page, frames / "01-player-plot-daisy-offer.png")
        _dispatch_key(session, page, 32)
        page.wait_for_function("() => window.__bebeeSeedQA && window.__bebeeSeedQA.plot1.currentFlowerId === 'flower_daisy'", timeout=timeout_ms)
        daisy = _seed(page)
        _assert_owned(daisy, ["seed_daisy"])
        if int(daisy.get("honey", -1)) != 30 or daisy.get("nativePatch1Completed") is not True:
            raise RuntimeError(f"Daisy unlock/plant transaction invalid: {daisy!r}")
        _shot(page, frames / "02-daisy-planted.png")

        _complete_patch(page, "patch2", 1950, 840)
        page.wait_for_function("() => window.__bebeeSeedQA && window.__bebeeSeedQA.nativePatch2Completed === true", timeout=timeout_ms)
        _move_to(page, 1410, 1110, tolerance=65)
        clover_offer = _seed(page)
        plot1 = clover_offer.get("plot1") or {}
        if int(clover_offer.get("honey", -1)) != 85 or plot1.get("nextSeedId") != "seed_clover" or int(plot1.get("cost", -1)) != 18:
            raise RuntimeError(f"Clover offer invalid after second native patch: {clover_offer!r}")
        _dispatch_key(session, page, 32)
        page.wait_for_function("() => window.__bebeeSeedQA && window.__bebeeSeedQA.plot1.currentFlowerId === 'flower_clover'", timeout=timeout_ms)
        clover = _seed(page)
        _assert_owned(clover, ["seed_daisy", "seed_clover"])
        if int(clover.get("honey", -1)) != 67:
            raise RuntimeError(f"Clover unlock cost invalid: {clover!r}")
        _shot(page, frames / "03-clover-planted.png")

        before_replant_honey = int(clover["honey"])
        _dispatch_key(session, page, 32)
        page.wait_for_function("() => window.__bebeeSeedQA && window.__bebeeSeedQA.plot1.currentFlowerId === 'flower_daisy'", timeout=timeout_ms)
        replanted = _seed(page)
        if int(replanted.get("honey", -1)) != before_replant_honey:
            raise RuntimeError(f"owned-species replant charged Honey: {replanted!r}")
        if replanted.get("nativePatch1Completed") is not True or replanted.get("nativePatch2Completed") is not True or replanted.get("nativePatch3Completed") is not False:
            raise RuntimeError(f"replant mutated campaign completion: {replanted!r}")
        _shot(page, frames / "04-free-replant-daisy.png")

        page.wait_for_timeout(1700)
        page.goto(_url(base_url, qa="seed_unlocked", qa_seed=88008, p5_storage_lifecycle="reload"), wait_until="load", timeout=timeout_ms)
        reloaded = _wait(page, head_sha, "seed_unlocked", timeout_ms)
        _assert_owned(reloaded, ["seed_daisy", "seed_clover"])
        if int(reloaded.get("honey", -1)) != 67 or (reloaded.get("plot1") or {}).get("currentFlowerId") != "flower_daisy":
            raise RuntimeError(f"seed customization did not survive reload: {reloaded!r}")
        if reloaded.get("nativePatch1Completed") is not True or reloaded.get("nativePatch2Completed") is not True or reloaded.get("nativePatch3Completed") is not False:
            raise RuntimeError(f"campaign state changed across seed reload: {reloaded!r}")
        _move_to(page, 1410, 1110, tolerance=70)
        _shot(page, frames / "05-reloaded-daisy.png")
        _assert_clean(console, page_errors, "P5 desktop persistence")
        return {
            "viewport": viewport,
            "after_patch1": after_patch1,
            "daisy": daisy,
            "clover": clover,
            "replanted": replanted,
            "reloaded": reloaded,
            "replant_cost": 0,
            "frame_files": [path.relative_to(output_root).as_posix() for path in sorted(frames.glob("*.png"))],
            "console_error_count": len(console),
            "page_error_count": len(page_errors),
        }
    finally:
        context.close()


def _dispatch_touch(session, event_type: str, points: list[dict[str, object]]) -> None:
    session.send("Input.dispatchTouchEvent", {"type": event_type, "touchPoints": points})


def _tap_plot(page: Page, session, payload: dict[str, object]) -> None:
    movement = _movement(page)
    plot = payload.get("plot1") or {}
    design_x = 640.0 + float(plot["x"]) - float(movement["cameraX"])
    design_y = 360.0 + float(plot["y"]) - float(movement["cameraY"])
    viewport = page.viewport_size or {"width": 844, "height": 390}
    x = design_x * viewport["width"] / 1280.0
    y_from_bottom = design_y * viewport["height"] / 720.0
    candidates = [viewport["height"] - y_from_bottom, y_from_bottom]
    for y in candidates:
        point = {"x": x, "y": y, "radiusX": 1, "radiusY": 1, "force": 1, "id": 1}
        _dispatch_touch(session, "touchStart", [point])
        page.wait_for_timeout(90)
        _dispatch_touch(session, "touchEnd", [])
        page.wait_for_timeout(240)
        if "seed_daisy" in (_seed(page).get("ownedSeedIds") or []):
            return
    raise RuntimeError(f"touch tap did not activate player plot: seed={_seed(page)!r} movement={movement!r}")


def _mobile_touch(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict[str, object]:
    viewport = {"width": 844, "height": 390}
    frames = output_root / "p5_seed" / "mobile_touch"
    context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1, has_touch=True, is_mobile=True)
    page = context.new_page()
    console, page_errors = _errors(page)
    session = context.new_cdp_session(page)
    session.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 1})
    try:
        page.goto(_url(base_url, qa="seed_locked", qa_seed=88008, p5_storage_lifecycle="reset"), wait_until="load", timeout=timeout_ms)
        _wait(page, head_sha, "seed_locked", timeout_ms)
        _complete_patch(page, "patch1", 1550, 800)
        page.wait_for_function("() => window.__bebeeSeedQA && window.__bebeeSeedQA.plot1.action === 'unlock_and_plant'", timeout=timeout_ms)
        _move_to(page, 1410, 1110, tolerance=65)
        offer = _seed(page)
        _shot(page, frames / "00-touch-offer.png")
        _tap_plot(page, session, offer)
        page.wait_for_function("() => window.__bebeeSeedQA && window.__bebeeSeedQA.plot1.currentFlowerId === 'flower_daisy'", timeout=timeout_ms)
        planted = _seed(page)
        if int(planted.get("honey", -1)) != 30 or planted.get("nativePatch1Completed") is not True:
            raise RuntimeError(f"mobile touch planting transaction invalid: {planted!r}")
        _shot(page, frames / "01-touch-planted.png")
        _assert_clean(console, page_errors, "P5 mobile touch")
        return {
            "viewport": {"id": "mobile_landscape", **viewport},
            "offer": offer,
            "planted": planted,
            "touch_direct_plot_action": True,
            "frame_files": [path.relative_to(output_root).as_posix() for path in sorted(frames.glob("*.png"))],
            "console_error_count": len(console),
            "page_error_count": len(page_errors),
        }
    finally:
        context.close()


def record_seed_ownership(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict[str, object]:
    canonical = _canonical(browser, base_url=base_url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
    desktop = _desktop_persistence(browser, base_url=base_url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
    mobile = _mobile_touch(browser, base_url=base_url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
    return {
        "ticket": "P5-SEED-OWNERSHIP",
        "canonical": canonical,
        "desktop_persistence": desktop,
        "mobile_touch": mobile,
        "result": "PASS",
    }
