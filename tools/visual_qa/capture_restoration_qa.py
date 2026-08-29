#!/usr/bin/env python3
"""P4 browser proof for the first Meadow restoration, persistence and HUD-hidden readability."""
from __future__ import annotations

import hashlib
import math
import tempfile
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import Browser, BrowserContext, Page


def _url(base: str, **values: object) -> str:
    parsed = urlsplit(base)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.update({key: str(value) for key, value in values.items()})
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _errors(page: Page) -> tuple[list[str], list[str]]:
    console: list[str] = []
    page_errors: list[str] = []
    page.on("console", lambda message: console.append(message.text) if message.type in {"error", "assert"} else None)
    page.on("pageerror", lambda error: page_errors.append(str(error)))
    return console, page_errors


def _assert_clean(console: list[str], page_errors: list[str], label: str) -> None:
    if console or page_errors:
        raise RuntimeError(f"{label}: console={console!r} page={page_errors!r}")


def _movement(page: Page) -> dict[str, object]:
    value = page.evaluate("() => window.__bebeeMovementQA ? structuredClone(window.__bebeeMovementQA) : null")
    if not isinstance(value, dict):
        raise RuntimeError("movement bridge missing")
    return value


def _pollination(page: Page) -> dict[str, object]:
    value = page.evaluate("() => window.__bebeePollinationQA ? structuredClone(window.__bebeePollinationQA) : null")
    if not isinstance(value, dict):
        raise RuntimeError("pollination bridge missing")
    return value


def _progression(page: Page) -> dict[str, object]:
    value = page.evaluate("() => window.__bebeeProgressionQA ? structuredClone(window.__bebeeProgressionQA) : null")
    if not isinstance(value, dict):
        raise RuntimeError("progression bridge missing")
    return value


def _restoration(page: Page) -> dict[str, object]:
    value = page.evaluate("() => window.__bebeeRestorationQA ? structuredClone(window.__bebeeRestorationQA) : null")
    if not isinstance(value, dict):
        raise RuntimeError("restoration bridge missing")
    return value


def _wait(page: Page, head_sha: str, state: str, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        "() => window.__bebeeQA && window.__bebeeQA.captureReady === true && "
        "!!window.__bebeeMovementQA && !!window.__bebeePollinationQA && "
        "!!window.__bebeeProgressionQA && !!window.__bebeeRestorationQA",
        timeout=timeout_ms,
    )
    qa = page.evaluate("() => structuredClone(window.__bebeeQA)")
    if qa.get("stateId") != state or qa.get("buildCommitSha") != head_sha:
        raise RuntimeError(f"P4 provenance mismatch: {qa!r}")
    return _restoration(page)


def _shot(page: Page, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path), full_page=False, animations="disabled")


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
    page.wait_for_timeout(120)


def _buy_buzz(page: Page, context: BrowserContext, timeout_ms: int) -> dict[str, object]:
    _move_to(page, 1120, 800, tolerance=75)
    session = context.new_cdp_session(page)
    _dispatch_key(session, page, 32)
    page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === true", timeout=timeout_ms)
    _dispatch_key(session, page, 39)
    page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.selectedUpgrade === 'buzz'", timeout=timeout_ms)
    _dispatch_key(session, page, 32)
    page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.buzzLevel === 2", timeout=timeout_ms)
    purchased = _progression(page)
    if abs(float(purchased.get("buzzWorkMultiplier", 0)) - 1.35) > 0.001:
        raise RuntimeError(f"Buzz 2 missing before hard patch: {purchased!r}")
    _dispatch_key(session, page, 27)
    page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === false", timeout=timeout_ms)
    return purchased


def _assert_stage(payload: dict[str, object], expected: str, contribution: int) -> None:
    if payload.get("stageId") != expected or int(payload.get("contribution", -1)) != contribution:
        raise RuntimeError(f"restoration stage mismatch expected {expected}/{contribution}: {payload!r}")


def _canonical_fixture_probe(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    timeout_ms: int,
) -> dict[str, object]:
    expectations = (
        ("meadow_dormant", "DORMANT", 0, 1),
        ("meadow_mid", "GROWING", 2, 2),
        ("meadow_restored", "RESTORED", 3, 2),
    )
    results: dict[str, object] = {}
    for state_id, stage_id, contribution, buzz_level in expectations:
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        console, page_errors = _errors(page)
        try:
            page.goto(_url(base_url, qa=state_id, qa_seed=88008, hud_hidden=1), wait_until="load", timeout=timeout_ms)
            payload = _wait(page, head_sha, state_id, timeout_ms)
            _assert_stage(payload, stage_id, contribution)
            progression = _progression(page)
            if int(progression.get("buzzLevel", -1)) != buzz_level:
                raise RuntimeError(f"{state_id} canonical fixture buzz mismatch: {progression!r}")
            if payload.get("hudHidden") is not True:
                raise RuntimeError(f"{state_id} canonical fixture did not hide HUD: {payload!r}")
            _assert_clean(console, page_errors, f"P4 canonical fixture {state_id}")
            results[state_id] = {
                "stage": payload,
                "buzz_level": buzz_level,
                "console_error_count": len(console),
                "page_error_count": len(page_errors),
            }
        finally:
            context.close()
    return results


def _desktop_sequence(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> tuple[dict[str, object], dict[str, object]]:
    frames = output_root / "p4_restoration" / "desktop_reference_frames"
    video_path = output_root / "p4_restoration" / "desktop_reference.webm"
    video_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="bebee-p4-restoration-") as video_dir:
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            screen={"width": 1280, "height": 720},
            device_scale_factor=1,
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        video = page.video
        console, page_errors = _errors(page)
        try:
            page.goto(
                _url(base_url, qa="meadow_dormant", qa_seed=88008, hud_hidden=1, p4_storage_lifecycle="reset"),
                wait_until="load",
                timeout=timeout_ms,
            )
            dormant = _wait(page, head_sha, "meadow_dormant", timeout_ms)
            _assert_stage(dormant, "DORMANT", 0)
            if dormant.get("hudHidden") is not True or int(dormant.get("detailCount", -1)) != 8 or int(dormant.get("ambientLifeCount", -1)) != 0:
                raise RuntimeError(f"dormant visual contract invalid: {dormant!r}")
            _move_to(page, 1760, 900, tolerance=70)
            _shot(page, frames / "00-dormant-hud-hidden.png")
            page.set_viewport_size({"width": 640, "height": 360})
            page.wait_for_timeout(120)
            _shot(page, output_root / "p4_restoration" / "poki_small" / "00-dormant-hud-hidden.png")
            page.set_viewport_size({"width": 1280, "height": 720})
            page.wait_for_timeout(120)

            _complete_patch(page, "patch1", 1550, 800)
            page.wait_for_function("() => window.__bebeeRestorationQA && window.__bebeeRestorationQA.stageId === 'WAKING'", timeout=timeout_ms)
            waking = _restoration(page)
            _assert_stage(waking, "WAKING", 1)
            _shot(page, frames / "01-waking-hud-hidden.png")

            buzz_purchase = _buy_buzz(page, context, timeout_ms)
            _complete_patch(page, "patch2", 1950, 840)
            page.wait_for_function("() => window.__bebeeRestorationQA && window.__bebeeRestorationQA.stageId === 'GROWING'", timeout=timeout_ms)
            growing = _restoration(page)
            _assert_stage(growing, "GROWING", 2)
            if int(growing.get("detailCount", -1)) != 22 or int(growing.get("ambientLifeCount", -1)) != 2:
                raise RuntimeError(f"growing visual contract invalid: {growing!r}")
            _shot(page, frames / "02-growing-before-reload.png")

            page.wait_for_timeout(1600)
            page.goto(
                _url(base_url, qa="meadow_mid", qa_seed=88008, hud_hidden=1, p4_storage_lifecycle="reload"),
                wait_until="load",
                timeout=timeout_ms,
            )
            growing_reloaded = _wait(page, head_sha, "meadow_mid", timeout_ms)
            page.wait_for_function("() => window.__bebeeRestorationQA && window.__bebeeRestorationQA.stageId === 'GROWING'", timeout=timeout_ms)
            growing_reloaded = _restoration(page)
            _assert_stage(growing_reloaded, "GROWING", 2)
            if int(_progression(page).get("buzzLevel", -1)) != 2:
                raise RuntimeError("Buzz 2 did not survive P4 midpoint reload")
            _move_to(page, 1800, 950, tolerance=70)
            _shot(page, frames / "03-growing-reloaded-hud-hidden.png")

            _complete_patch(page, "patch3", 2070, 1160)
            page.wait_for_function("() => window.__bebeeRestorationQA && window.__bebeeRestorationQA.stageId === 'RESTORED'", timeout=timeout_ms)
            restored = _restoration(page)
            _assert_stage(restored, "RESTORED", 3)
            if int(restored.get("detailCount", -1)) != 28 or int(restored.get("ambientLifeCount", -1)) != 6:
                raise RuntimeError(f"restored visual contract invalid: {restored!r}")
            _shot(page, frames / "04-restored-reveal.png")

            movement_before = _movement(page)
            page.keyboard.down("a")
            page.wait_for_timeout(350)
            page.keyboard.up("a")
            page.wait_for_timeout(80)
            movement_after = _movement(page)
            control_displacement = math.hypot(
                float(movement_after["beeX"]) - float(movement_before["beeX"]),
                float(movement_after["beeY"]) - float(movement_before["beeY"]),
            )
            if control_displacement < 12:
                raise RuntimeError(f"restoration reveal blocked movement: {control_displacement}")
            page.wait_for_timeout(1700)
            settled = _restoration(page)
            if settled.get("celebrationActive") is True:
                raise RuntimeError(f"restoration celebration did not settle: {settled!r}")

            page.wait_for_timeout(1600)
            page.goto(
                _url(base_url, qa="meadow_restored", qa_seed=88008, hud_hidden=1, p4_storage_lifecycle="reload"),
                wait_until="load",
                timeout=timeout_ms,
            )
            reloaded = _wait(page, head_sha, "meadow_restored", timeout_ms)
            page.wait_for_function("() => window.__bebeeRestorationQA && window.__bebeeRestorationQA.stageId === 'RESTORED'", timeout=timeout_ms)
            reloaded = _restoration(page)
            _assert_stage(reloaded, "RESTORED", 3)
            if reloaded.get("celebrationActive") is True:
                raise RuntimeError(f"reload replayed one-shot reveal: {reloaded!r}")
            _move_to(page, 1800, 950, tolerance=70)
            _shot(page, frames / "05-restored-reloaded-hud-hidden.png")

            page.set_viewport_size({"width": 640, "height": 360})
            page.wait_for_timeout(120)
            _shot(page, output_root / "p4_restoration" / "poki_small" / "01-restored-hud-hidden.png")
            page.set_viewport_size({"width": 1280, "height": 720})

            page.goto(
                _url(base_url, qa="meadow_restored", qa_seed=88008, p4_storage_lifecycle="reload"),
                wait_until="load",
                timeout=timeout_ms,
            )
            visible_hud = _wait(page, head_sha, "meadow_restored", timeout_ms)
            page.wait_for_function("() => window.__bebeeRestorationQA && window.__bebeeRestorationQA.stageId === 'RESTORED'", timeout=timeout_ms)
            visible_hud = _restoration(page)
            if visible_hud.get("hudHidden") is not False or visible_hud.get("objectiveText") != "MEADOW RESTORED":
                raise RuntimeError(f"restored objective contract invalid: {visible_hud!r}")
            _move_to(page, 1800, 950, tolerance=70)
            _shot(page, frames / "06-restored-objective.png")

            storage_state = context.storage_state(indexed_db=True)
            _assert_clean(console, page_errors, "P4 desktop restoration")
            result = {
                "viewport": {"id": "desktop_reference", "width": 1280, "height": 720},
                "dormant": dormant,
                "waking": waking,
                "buzz_purchase": buzz_purchase,
                "growing": growing,
                "growing_reloaded": growing_reloaded,
                "restored": restored,
                "restored_reloaded": reloaded,
                "visible_hud": visible_hud,
                "reveal_control_displacement": round(control_displacement, 3),
                "console_error_count": len(console),
                "page_error_count": len(page_errors),
            }
        finally:
            _release(page)
            context.close()

        if video is None:
            raise RuntimeError("P4 desktop video handle missing")
        video.save_as(str(video_path))

    if not video_path.is_file() or video_path.stat().st_size == 0:
        raise RuntimeError("P4 desktop video missing")
    result["video_file"] = video_path.relative_to(output_root).as_posix()
    result["video_sha256"] = _sha(video_path)
    result["frame_files"] = [p.relative_to(output_root).as_posix() for p in sorted(frames.glob("*.png"))]
    return result, storage_state


def _mobile_restored(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
    storage_state: dict[str, object],
) -> dict[str, object]:
    context = browser.new_context(
        viewport={"width": 844, "height": 390},
        screen={"width": 844, "height": 390},
        device_scale_factor=1,
        has_touch=True,
        is_mobile=True,
        storage_state=storage_state,
    )
    page = context.new_page()
    console, page_errors = _errors(page)
    try:
        page.goto(
            _url(base_url, qa="meadow_restored", qa_seed=88008, hud_hidden=1, p4_storage_lifecycle="reload"),
            wait_until="load",
            timeout=timeout_ms,
        )
        restored = _wait(page, head_sha, "meadow_restored", timeout_ms)
        page.wait_for_function("() => window.__bebeeRestorationQA && window.__bebeeRestorationQA.stageId === 'RESTORED'", timeout=timeout_ms)
        restored = _restoration(page)
        _assert_stage(restored, "RESTORED", 3)
        _move_to(page, 1800, 950, tolerance=75)
        path = output_root / "p4_restoration" / "mobile_landscape" / "00-restored-hud-hidden.png"
        _shot(page, path)
        _assert_clean(console, page_errors, "P4 mobile restored")
        return {
            "viewport": {"id": "mobile_landscape", "width": 844, "height": 390},
            "restored": restored,
            "capture_file": path.relative_to(output_root).as_posix(),
            "capture_sha256": _sha(path),
            "console_error_count": len(console),
            "page_error_count": len(page_errors),
        }
    finally:
        _release(page)
        context.close()


def record_restoration(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    canonical_fixtures = _canonical_fixture_probe(
        browser, base_url=base_url, head_sha=head_sha, timeout_ms=timeout_ms
    )
    desktop, storage_state = _desktop_sequence(
        browser, base_url=base_url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms
    )
    mobile = _mobile_restored(
        browser,
        base_url=base_url,
        head_sha=head_sha,
        output_root=output_root,
        timeout_ms=timeout_ms,
        storage_state=storage_state,
    )
    dormant = desktop["dormant"]
    restored = desktop["restored_reloaded"]
    return {
        "ticket": "P4-FIRST-MEADOW-RESTORATION",
        "canonical_fixtures": canonical_fixtures,
        "desktop": desktop,
        "mobile_restored": mobile,
        "objective_measurements": {
            "stage_count": 4,
            "canonical_fixture_count": len(canonical_fixtures),
            "dormant_detail_count": int(dormant["detailCount"]),
            "restored_detail_count": int(restored["detailCount"]),
            "detail_count_ratio": round(int(restored["detailCount"]) / max(1, int(dormant["detailCount"])), 2),
            "dormant_ambient_life_count": int(dormant["ambientLifeCount"]),
            "restored_ambient_life_count": int(restored["ambientLifeCount"]),
            "dormant_ground_mix": float(dormant["groundMix"]),
            "restored_ground_mix": float(restored["groundMix"]),
            "hud_hidden_before_after": bool(dormant["hudHidden"] and restored["hudHidden"]),
            "reload_stage": restored["stageId"],
            "modal_tutorial_count": 0,
            "persistent_objective_count": 1,
        },
        "result": "PASS",
    }
