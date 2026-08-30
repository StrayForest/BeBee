#!/usr/bin/env python3
"""P7 browser proof for the authored Golden Fields production-expansion slice."""
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


GOLDEN_PATCHES = {
    9: (2720.0, 1260.0),
    10: (3320.0, 900.0),
    11: (4040.0, 1190.0),
    12: (3900.0, 470.0),
}
EXPECTED_START_HONEY = 346
EXPECTED_COMPLETE_HONEY = 891


def _complete_golden_patch(page: Page, index: int, *, timeout_seconds: float = 24.0) -> dict[str, object]:
    x, y = GOLDEN_PATCHES[index]
    _move_to(page, x, y, timeout_seconds=20.0, tolerance=54)
    deadline = time.monotonic() + timeout_seconds
    direction_right = True
    while time.monotonic() < deadline:
        current = _patch(page, index)
        if current.get("state") == "COMPLETED":
            return current
        _move_to(page, x + (76 if direction_right else -76), y, timeout_seconds=3.0, tolerance=22)
        direction_right = not direction_right
    raise RuntimeError(f"P7 patch {index} did not complete: {_patch(page, index)!r}")


def _wait_active_region(page: Page, *, complete: bool | None, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        """(expectedComplete) => {
            const qa = window.__bebeeRegionQA;
            if (!qa || qa.activeRegionId !== 'region_02' || !qa.region || qa.region.id !== 'region_02') return false;
            if (expectedComplete === null) return true;
            return qa.region.complete === expectedComplete;
        }""",
        arg=complete,
        timeout=timeout_ms,
    )
    return _region(page)


def _campaign_region(payload: dict[str, object], region_id: str) -> dict[str, object]:
    campaign = payload.get("campaign") or {}
    regions = campaign.get("regions") if isinstance(campaign, dict) else None
    if isinstance(regions, list):
        for item in regions:
            if isinstance(item, dict) and item.get("id") == region_id:
                return item
    raise RuntimeError(f"campaign region {region_id} missing: {payload!r}")


def _wait_wetland_handoff(page: Page, *, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        """() => {
            const qa = window.__bebeeRegionQA;
            if (!qa || qa.activeRegionId !== 'region_03' || !qa.region || qa.region.id !== 'region_03') return false;
            const regions = qa.campaign && qa.campaign.regions;
            if (!Array.isArray(regions)) return false;
            const golden = regions.find(item => item && item.id === 'region_02');
            return !!golden && golden.complete === true && golden.restored_count === 4;
        }""",
        timeout=timeout_ms,
    )
    return _region(page)


def _assert_region_start(payload: dict[str, object]) -> None:
    summary = payload.get("region") or {}
    campaign = payload.get("campaign") or {}
    if summary.get("id") != "region_02" or int(summary.get("restored_count", -1)) != 0 or int(summary.get("total", -1)) != 4:
        raise RuntimeError(f"P7 Golden Fields start summary invalid: {payload!r}")
    if payload.get("objectiveText") != "RESTORE SUN GATE · 0/4":
        raise RuntimeError(f"P7 Golden Fields objective invalid: {payload!r}")
    if int(payload.get("honey", -1)) != EXPECTED_START_HONEY:
        raise RuntimeError(f"P7 fixture Honey drifted: {payload!r}")
    if int(payload.get("flightLevel", -1)) != 3 or int(payload.get("buzzLevel", -1)) != 3:
        raise RuntimeError(f"P7 must reuse P6 progression rather than introduce a new required branch: {payload!r}")
    if int(campaign.get("completed_regions", -1)) != 1 or int(campaign.get("total_regions", -1)) != 6:
        raise RuntimeError(f"P7 campaign transition invalid: {payload!r}")


def record_golden_fields(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    viewport = {"width": 1280, "height": 720}
    frames = output_root / "p7_golden_fields"
    context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1)
    page = context.new_page()
    console, page_errors = _errors(page)
    external = _external_requests(page, base_url)
    session = context.new_cdp_session(page)
    try:
        # Reuse the retained P6-complete repository fixture, but exercise a real persistence write
        # before dropping all QA-state injection. Everything after the navigation to base_url is
        # normal runtime state derived solely from the saved campaign completion map.
        page.goto(
            _url(base_url, qa="region_complete", qa_seed=88008, p6_storage_lifecycle="reset"),
            wait_until="load",
            timeout=timeout_ms,
        )
        fixture = _wait(page, head_sha, "region_complete", timeout_ms)
        fixture_summary = fixture.get("region") or {}
        if fixture_summary.get("complete") is not True or int(fixture_summary.get("restored_count", -1)) != 6:
            raise RuntimeError(f"P7 could not establish P6-complete fixture: {fixture!r}")
        if int(fixture.get("honey", -1)) != EXPECTED_START_HONEY:
            raise RuntimeError(f"P7 fixture economy mismatch: {fixture!r}")

        _dispatch_key(session, page, 27)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === true", timeout=timeout_ms)
        _dispatch_key(session, page, 32)
        page.wait_for_function(
            "() => window.__bebeeRegionQA && window.__bebeeRegionQA.settings && window.__bebeeRegionQA.settings.reduced_motion === true",
            timeout=timeout_ms,
        )
        persisted_fixture = _region(page)
        if str(persisted_fixture.get("saveCode", "")).startswith("save_error"):
            raise RuntimeError(f"P7 fixture persistence failed: {persisted_fixture!r}")
        _dispatch_key(session, page, 27)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === false", timeout=timeout_ms)
        page.wait_for_timeout(1600)

        page.goto(base_url, wait_until="load", timeout=timeout_ms)
        start = _wait_active_region(page, complete=False, timeout_ms=timeout_ms)
        _assert_region_start(start)
        first = _patch(page, 9)
        if first.get("state") != "AVAILABLE" or first.get("eligible") is not True:
            raise RuntimeError(f"P7 first Golden Fields patch is not available after Sunny Meadows: {first!r}")
        if first.get("flowerId") != "flower_sunflower" or int(first.get("requiresBuzzLevel", -1)) != 3:
            raise RuntimeError(f"P7 Sun Gate authored identity/gate invalid: {first!r}")

        _move_to(page, *GOLDEN_PATCHES[9], timeout_seconds=20.0, tolerance=70)
        start = _region(page)
        start_metrics = _canvas_metrics(page)
        start_shot = frames / "00-golden-fields-start-desktop.png"
        _shot(page, start_shot)

        p9 = _complete_golden_patch(page, 9)
        after_one = _wait_active_region(page, complete=False, timeout_ms=timeout_ms)
        if int((after_one.get("region") or {}).get("restored_count", -1)) != 1:
            raise RuntimeError(f"P7 Sun Gate did not restore: {after_one!r}")
        if p9.get("flowerId") != "flower_sunflower":
            raise RuntimeError(f"P7 patch 9 species drifted: {p9!r}")

        p10 = _complete_golden_patch(page, 10)
        mid = _region(page)
        if int((mid.get("region") or {}).get("restored_count", -1)) != 2:
            raise RuntimeError(f"P7 Golden Fields midpoint invalid: {mid!r}")
        if p10.get("flowerId") != "flower_poppy":
            raise RuntimeError(f"P7 patch 10 species drifted: {p10!r}")
        mid_shot = frames / "01-golden-fields-mid-desktop.png"
        _shot(page, mid_shot)

        p11 = _complete_golden_patch(page, 11)
        p12 = _complete_golden_patch(page, 12)
        handoff = _wait_wetland_handoff(page, timeout_ms=timeout_ms)
        golden_summary = _campaign_region(handoff, "region_02")
        next_summary = handoff.get("region") or {}
        campaign = handoff.get("campaign") or {}
        if int(golden_summary.get("restored_count", -1)) != 4 or int(golden_summary.get("total", -1)) != 4 or golden_summary.get("complete") is not True:
            raise RuntimeError(f"P7 Golden Fields did not complete before Wetland handoff: {handoff!r}")
        if next_summary.get("id") != "region_03" or int(next_summary.get("restored_count", -1)) != 0:
            raise RuntimeError(f"P7 did not hand off to a fresh Wetland Garden: {handoff!r}")
        if handoff.get("objectiveText") != "RESTORE LOTUS LANDING · 0/4":
            raise RuntimeError(f"P7 post-Golden objective invalid: {handoff!r}")
        if int(handoff.get("honey", -1)) != EXPECTED_COMPLETE_HONEY:
            raise RuntimeError(f"P7 Golden Fields reward total invalid: {handoff!r}")
        if campaign.get("complete") is not False or int(campaign.get("completed_regions", -1)) != 2 or int(campaign.get("total_regions", -1)) != 6:
            raise RuntimeError(f"P7 campaign summary did not expose Wetland continuation: {handoff!r}")
        if p11.get("flowerId") != "flower_sunflower" or p12.get("flowerId") != "flower_poppy":
            raise RuntimeError(f"P7 species alternation drifted: p11={p11!r} p12={p12!r}")
        complete_shot = frames / "02-golden-fields-complete-desktop.png"
        _shot(page, complete_shot)

        events = handoff.get("analyticsEvents") or []
        names = [event.get("name") for event in events if isinstance(event, dict)]
        if "patch_completed" not in names or "meadow_restored" not in names or "region_completed" not in names:
            raise RuntimeError(f"P7 expansion analytics missing: {names!r}")
        region_completed = [
            event for event in events
            if isinstance(event, dict)
            and event.get("name") == "region_completed"
            and (event.get("properties") or {}).get("region_id") == "region_02"
        ]
        if not region_completed:
            raise RuntimeError(f"P7 region_completed analytics not attributed to region_02: {events!r}")

        page.wait_for_timeout(1600)
        page.goto(base_url, wait_until="load", timeout=timeout_ms)
        reloaded = _wait_wetland_handoff(page, timeout_ms=timeout_ms)
        reload_campaign = reloaded.get("campaign") or {}
        reload_golden = _campaign_region(reloaded, "region_02")
        if int(reloaded.get("honey", -1)) != EXPECTED_COMPLETE_HONEY or reload_golden.get("complete") is not True:
            raise RuntimeError(f"P7 Golden Fields completion did not survive reload: {reloaded!r}")
        if int(reload_campaign.get("completed_regions", -1)) != 2 or int(reload_campaign.get("total_regions", -1)) != 6:
            raise RuntimeError(f"P7 reload campaign transition invalid: {reloaded!r}")
        _move_to(page, *GOLDEN_PATCHES[12], timeout_seconds=20.0, tolerance=70)
        reload_shot = frames / "03-golden-fields-reloaded-desktop.png"
        _shot(page, reload_shot)

        page.set_viewport_size({"width": 844, "height": 390})
        page.wait_for_timeout(300)
        mobile_metrics = _canvas_metrics(page)
        if mobile_metrics["width"] + 1 < 844 or mobile_metrics["height"] + 1 < 390:
            raise RuntimeError(f"P7 Golden Fields mobile canvas does not cover viewport: {mobile_metrics!r}")
        mobile_shot = frames / "04-golden-fields-complete-mobile-landscape.png"
        _shot(page, mobile_shot)

        if not math.isfinite(float((_patch(page, 12).get("workTarget") or 0))) or float(_patch(page, 12).get("workTarget") or 0) <= 0:
            raise RuntimeError("P7 final Golden Fields patch work target is invalid")
        _assert_clean(console, page_errors, external, "P7 Golden Fields journey")

        return {
            "ticket": "P7-GOLDEN-FIELDS",
            "fixture_source": "P6 region_complete fixture persisted through real settings save, then QA route removed",
            "viewport": {"id": "desktop_reference", **viewport},
            "start_region": start.get("region"),
            "mid_region": mid.get("region"),
            "complete_region": golden_summary,
            "next_active_region": next_summary,
            "campaign": campaign,
            "start_honey": EXPECTED_START_HONEY,
            "final_honey": EXPECTED_COMPLETE_HONEY,
            "patches": {"9": p9, "10": p10, "11": p11, "12": p12},
            "analytics_event_names": names,
            "reload_region": reload_golden,
            "reload_active_region": reloaded.get("region"),
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
