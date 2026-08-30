#!/usr/bin/env python3
"""P7 browser proof for the authored Rosewood production-expansion slice."""
from __future__ import annotations

import math
import time
from pathlib import Path

from playwright.sync_api import Browser, Page

from capture_region_qa import (
    _assert_clean,
    _canvas_metrics,
    _dispatch_key,
    _errors,
    _external_requests,
    _move_to,
    _patch,
    _region,
    _shot,
    _url,
    _wait,
)


ROSEWOOD_PATCHES = {
    17: (6800.0, 620.0),
    18: (7350.0, 1380.0),
    19: (8020.0, 860.0),
    20: (8750.0, 1500.0),
}
EXPECTED_START_HONEY = 1596
EXPECTED_COMPLETE_HONEY = 2506


def _wait_active_rosewood(page: Page, *, complete: bool | None, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        """(expectedComplete) => {
            const qa = window.__bebeeRegionQA;
            if (!qa || qa.activeRegionId !== 'region_04' || !qa.region || qa.region.id !== 'region_04') return false;
            if (expectedComplete === null) return true;
            return qa.region.complete === expectedComplete;
        }""",
        arg=complete,
        timeout=timeout_ms,
    )
    return _region(page)


def _complete_rosewood_patch(page: Page, index: int, *, timeout_seconds: float = 24.0) -> dict[str, object]:
    x, y = ROSEWOOD_PATCHES[index]
    _move_to(page, x, y, timeout_seconds=40.0, tolerance=72)
    deadline = time.monotonic() + timeout_seconds
    direction_right = True
    while time.monotonic() < deadline:
        current = _patch(page, index)
        if current.get("state") == "COMPLETED":
            return current
        _move_to(page, x + (84 if direction_right else -84), y, timeout_seconds=3.0, tolerance=22)
        direction_right = not direction_right
    raise RuntimeError(f"P7 Rosewood patch {index} did not complete: {_patch(page, index)!r}")


def _assert_start(payload: dict[str, object]) -> None:
    summary = payload.get("region") or {}
    campaign = payload.get("campaign") or {}
    if summary.get("id") != "region_04" or int(summary.get("restored_count", -1)) != 0 or int(summary.get("total", -1)) != 4:
        raise RuntimeError(f"P7 Rosewood start summary invalid: {payload!r}")
    if payload.get("objectiveText") != "RESTORE ROSE GLADE · 0/4":
        raise RuntimeError(f"P7 Rosewood objective invalid: {payload!r}")
    if int(payload.get("honey", -1)) != EXPECTED_START_HONEY:
        raise RuntimeError(f"P7 Rosewood fixture Honey drifted: {payload!r}")
    if int(payload.get("flightLevel", -1)) != 3 or int(payload.get("buzzLevel", -1)) != 3:
        raise RuntimeError(f"P7 Rosewood must reuse validated progression: {payload!r}")
    if int(campaign.get("completed_regions", -1)) != 3 or int(campaign.get("total_regions", -1)) != 4:
        raise RuntimeError(f"P7 Rosewood campaign transition invalid: {payload!r}")


def record_rosewood(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    viewport = {"width": 1280, "height": 720}
    frames = output_root / "p7_rosewood"
    context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1)
    page = context.new_page()
    console, page_errors = _errors(page)
    external = _external_requests(page, base_url)
    session = context.new_cdp_session(page)
    try:
        page.goto(
            _url(base_url, qa="rosewood_start", qa_seed=88008, rosewood_storage_lifecycle="reset"),
            wait_until="load",
            timeout=timeout_ms,
        )
        start = _wait(page, head_sha, "rosewood_start", timeout_ms)
        _assert_start(start)

        first = _patch(page, 17)
        if first.get("state") not in {"AVAILABLE", "ACTIVE"} or first.get("eligible") is not True:
            raise RuntimeError(f"P7 Rosewood first patch is not available: {first!r}")
        if first.get("flowerId") != "flower_rose" or int(first.get("requiresBuzzLevel", -1)) != 3:
            raise RuntimeError(f"P7 Rose Glade authored identity/gate invalid: {first!r}")

        _move_to(page, *ROSEWOOD_PATCHES[17], timeout_seconds=22.0, tolerance=72)
        start_metrics = _canvas_metrics(page)
        start_shot = frames / "00-rosewood-start-desktop.png"
        _shot(page, start_shot)

        # Persist the expansion fixture through the real settings save path before
        # switching to ordinary runtime with no QA route.
        _dispatch_key(session, page, 27)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === true", timeout=timeout_ms)
        _dispatch_key(session, page, 32)
        page.wait_for_function(
            "() => window.__bebeeRegionQA && window.__bebeeRegionQA.settings && window.__bebeeRegionQA.settings.reduced_motion === true",
            timeout=timeout_ms,
        )
        if str(_region(page).get("saveCode", "")).startswith("save_error"):
            raise RuntimeError(f"P7 Rosewood fixture persistence failed: {_region(page)!r}")
        _dispatch_key(session, page, 27)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === false", timeout=timeout_ms)
        page.wait_for_timeout(1600)
        page.goto(base_url, wait_until="load", timeout=timeout_ms)

        ordinary = _wait_active_rosewood(page, complete=False, timeout_ms=timeout_ms)
        _assert_start(ordinary)

        p17 = _complete_rosewood_patch(page, 17)
        after_one = _wait_active_rosewood(page, complete=False, timeout_ms=timeout_ms)
        if int((after_one.get("region") or {}).get("restored_count", -1)) != 1:
            raise RuntimeError(f"P7 Rose Glade did not restore: {after_one!r}")
        if p17.get("flowerId") != "flower_rose":
            raise RuntimeError(f"P7 Rose patch species drifted: {p17!r}")

        p18 = _complete_rosewood_patch(page, 18)
        mid = _region(page)
        if int((mid.get("region") or {}).get("restored_count", -1)) != 2:
            raise RuntimeError(f"P7 Rosewood midpoint invalid: {mid!r}")
        if p18.get("flowerId") != "flower_bluebell":
            raise RuntimeError(f"P7 Bluebell patch species drifted: {p18!r}")
        mid_shot = frames / "01-rosewood-mid-desktop.png"
        _shot(page, mid_shot)

        p19 = _complete_rosewood_patch(page, 19)
        p20 = _complete_rosewood_patch(page, 20)
        complete = _wait_active_rosewood(page, complete=True, timeout_ms=timeout_ms)
        complete_summary = complete.get("region") or {}
        campaign = complete.get("campaign") or {}
        if int(complete_summary.get("restored_count", -1)) != 4 or int(complete_summary.get("total", -1)) != 4:
            raise RuntimeError(f"P7 Rosewood did not complete: {complete!r}")
        if complete.get("objectiveText") != "ROSEWOOD RESTORED · 4/4":
            raise RuntimeError(f"P7 Rosewood completion objective invalid: {complete!r}")
        if int(complete.get("honey", -1)) != EXPECTED_COMPLETE_HONEY:
            raise RuntimeError(f"P7 Rosewood reward total invalid: {complete!r}")
        if campaign.get("complete") is not True or int(campaign.get("completed_regions", -1)) != 4 or int(campaign.get("total_regions", -1)) != 4:
            raise RuntimeError(f"P7 four-region campaign did not complete: {complete!r}")
        if p19.get("flowerId") != "flower_rose" or p20.get("flowerId") != "flower_bluebell":
            raise RuntimeError(f"P7 Rosewood species alternation drifted: p19={p19!r} p20={p20!r}")
        complete_shot = frames / "02-rosewood-complete-desktop.png"
        _shot(page, complete_shot)

        events = complete.get("analyticsEvents") or []
        region_completed = [
            event for event in events
            if isinstance(event, dict)
            and event.get("name") == "region_completed"
            and (event.get("properties") or {}).get("region_id") == "region_04"
        ]
        if not region_completed:
            raise RuntimeError(f"P7 Rosewood region_completed analytics missing: {events!r}")

        page.wait_for_timeout(1600)
        page.goto(base_url, wait_until="load", timeout=timeout_ms)
        reloaded = _wait_active_rosewood(page, complete=True, timeout_ms=timeout_ms)
        reload_campaign = reloaded.get("campaign") or {}
        if int(reloaded.get("honey", -1)) != EXPECTED_COMPLETE_HONEY:
            raise RuntimeError(f"P7 Rosewood Honey did not survive reload: {reloaded!r}")
        if reload_campaign.get("complete") is not True or int(reload_campaign.get("completed_regions", -1)) != 4:
            raise RuntimeError(f"P7 Rosewood campaign completion did not survive reload: {reloaded!r}")
        _move_to(page, *ROSEWOOD_PATCHES[20], timeout_seconds=22.0, tolerance=72)
        reload_shot = frames / "03-rosewood-reloaded-desktop.png"
        _shot(page, reload_shot)

        page.set_viewport_size({"width": 844, "height": 390})
        page.wait_for_timeout(300)
        mobile_metrics = _canvas_metrics(page)
        if mobile_metrics["width"] + 1 < 844 or mobile_metrics["height"] + 1 < 390:
            raise RuntimeError(f"P7 Rosewood mobile canvas does not cover viewport: {mobile_metrics!r}")
        mobile_shot = frames / "04-rosewood-complete-mobile-landscape.png"
        _shot(page, mobile_shot)

        if not math.isfinite(float((_patch(page, 20).get("workTarget") or 0))) or float(_patch(page, 20).get("workTarget") or 0) <= 0:
            raise RuntimeError("P7 Rosewood final patch work target is invalid")
        _assert_clean(console, page_errors, external, "P7 Rosewood journey")

        return {
            "ticket": "P7-ROSEWOOD",
            "fixture_source": "P7 Wetland completion fixture persisted through real settings save, then Rosewood completed through ordinary runtime",
            "viewport": {"id": "desktop_reference", **viewport},
            "start_region": start.get("region"),
            "mid_region": mid.get("region"),
            "complete_region": complete_summary,
            "campaign": campaign,
            "start_honey": EXPECTED_START_HONEY,
            "final_honey": EXPECTED_COMPLETE_HONEY,
            "patches": {"17": p17, "18": p18, "19": p19, "20": p20},
            "analytics_event_names": [event.get("name") for event in events if isinstance(event, dict)],
            "reload_region": reloaded.get("region"),
            "desktop_canvas": start_metrics,
            "mobile_canvas": mobile_metrics,
            "screenshots": [
                start_shot.relative_to(output_root).as_posix(),
                mid_shot.relative_to(output_root).as_posix(),
                complete_shot.relative_to(output_root).as_posix(),
                reload_shot.relative_to(output_root).as_posix(),
                mobile_shot.relative_to(output_root).as_posix(),
            ],
            "console_error_count": len(console),
            "page_error_count": len(page_errors),
            "external_request_count": len(external),
            "result": "PASS",
        }
    finally:
        context.close()
