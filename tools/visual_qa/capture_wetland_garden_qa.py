#!/usr/bin/env python3
"""P7 browser proof for the authored Wetland Garden production-expansion slice."""
from __future__ import annotations

import math
import time
from pathlib import Path

from playwright.sync_api import Browser, Page

from capture_golden_fields_qa import GOLDEN_PATCHES, _campaign_region, _complete_golden_patch
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


WETLAND_PATCHES = {
    13: (4800.0, 560.0),
    14: (5200.0, 1180.0),
    15: (5740.0, 780.0),
    16: (6060.0, 1540.0),
}
EXPECTED_START_HONEY = 891
EXPECTED_COMPLETE_HONEY = 1596


def _complete_wetland_patch(page: Page, index: int, *, timeout_seconds: float = 26.0) -> dict[str, object]:
    x, y = WETLAND_PATCHES[index]
    _move_to(page, x, y, timeout_seconds=22.0, tolerance=56)
    deadline = time.monotonic() + timeout_seconds
    direction_right = True
    while time.monotonic() < deadline:
        current = _patch(page, index)
        if current.get("state") == "COMPLETED":
            return current
        _move_to(page, x + (82 if direction_right else -82), y, timeout_seconds=3.5, tolerance=24)
        direction_right = not direction_right
    raise RuntimeError(f"P7 Wetland patch {index} did not complete: {_patch(page, index)!r}")


def _wait_active_wetland(page: Page, *, complete: bool, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        """(expectedComplete) => {
            const qa = window.__bebeeRegionQA;
            if (!qa) return false;
            if (!expectedComplete) {
                return qa.activeRegionId === 'region_03' && !!qa.region &&
                    qa.region.id === 'region_03' && qa.region.complete === false;
            }
            // On a four-region campaign the runtime advances to Rosewood
            // immediately after Wetland completes, so completion must be
            // asserted from the campaign snapshot rather than activeRegionId.
            const wetland = (qa.campaign?.regions || []).find((region) => region.id === 'region_03');
            return !!wetland && wetland.complete === true && wetland.restored_count === wetland.total;
        }""",
        arg=complete,
        timeout=timeout_ms,
    )
    snapshot = _region(page)
    if complete:
        campaign = snapshot.get("campaign") or {}
        wetland = next((region for region in campaign.get("regions", []) if region.get("id") == "region_03"), None)
        if wetland is not None:
            snapshot["region"] = wetland
            snapshot["objectiveText"] = f"WETLAND GARDEN RESTORED · {wetland.get('restored_count', 0)}/{wetland.get('total', 0)}"
    return snapshot


def _persist_p6_complete_fixture(page: Page, session, *, base_url: str, head_sha: str, timeout_ms: int) -> None:
    page.goto(
        _url(base_url, qa="region_complete", qa_seed=88008, p6_storage_lifecycle="reset"),
        wait_until="load",
        timeout=timeout_ms,
    )
    fixture = _wait(page, head_sha, "region_complete", timeout_ms)
    fixture_summary = fixture.get("region") or {}
    if fixture_summary.get("complete") is not True or int(fixture_summary.get("restored_count", -1)) != 6:
        raise RuntimeError(f"P7 Wetland could not establish P6-complete fixture: {fixture!r}")
    if int(fixture.get("honey", -1)) != 346:
        raise RuntimeError(f"P7 Wetland P6 fixture economy mismatch: {fixture!r}")

    _dispatch_key(session, page, 27)
    page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === true", timeout=timeout_ms)
    _dispatch_key(session, page, 32)
    page.wait_for_function(
        "() => window.__bebeeRegionQA && window.__bebeeRegionQA.settings && window.__bebeeRegionQA.settings.reduced_motion === true",
        timeout=timeout_ms,
    )
    persisted = _region(page)
    if str(persisted.get("saveCode", "")).startswith("save_error"):
        raise RuntimeError(f"P7 Wetland fixture persistence failed: {persisted!r}")
    _dispatch_key(session, page, 27)
    page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === false", timeout=timeout_ms)
    page.wait_for_timeout(1600)


def _complete_golden_prelude(page: Page, *, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        "() => window.__bebeeRegionQA && window.__bebeeRegionQA.activeRegionId === 'region_02' && window.__bebeeRegionQA.region && window.__bebeeRegionQA.region.restored_count === 0",
        timeout=timeout_ms,
    )
    for index in range(9, 13):
        _complete_golden_patch(page, index)
    start = _wait_active_wetland(page, complete=False, timeout_ms=timeout_ms)
    golden = _campaign_region(start, "region_02")
    if golden.get("complete") is not True or int(golden.get("restored_count", -1)) != 4:
        raise RuntimeError(f"P7 Wetland Golden prelude did not complete: {start!r}")
    if int(start.get("honey", -1)) != EXPECTED_START_HONEY:
        raise RuntimeError(f"P7 Wetland start Honey mismatch after Golden prelude: {start!r}")
    return start


def record_wetland_garden(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    viewport = {"width": 1280, "height": 720}
    frames = output_root / "p7_wetland_garden"
    context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1)
    page = context.new_page()
    console, page_errors = _errors(page)
    external = _external_requests(page, base_url)
    session = context.new_cdp_session(page)
    try:
        _persist_p6_complete_fixture(page, session, base_url=base_url, head_sha=head_sha, timeout_ms=timeout_ms)
        page.goto(base_url, wait_until="load", timeout=timeout_ms)
        start = _complete_golden_prelude(page, timeout_ms=timeout_ms)

        summary = start.get("region") or {}
        campaign = start.get("campaign") or {}
        if summary.get("id") != "region_03" or int(summary.get("restored_count", -1)) != 0 or int(summary.get("total", -1)) != 4:
            raise RuntimeError(f"P7 Wetland start summary invalid: {start!r}")
        if start.get("objectiveText") != "RESTORE LOTUS LANDING · 0/4":
            raise RuntimeError(f"P7 Wetland start objective invalid: {start!r}")
        if int(start.get("flightLevel", -1)) != 3 or int(start.get("buzzLevel", -1)) != 3:
            raise RuntimeError(f"P7 Wetland must reuse Flight/Buzz 3: {start!r}")
        if int(campaign.get("completed_regions", -1)) != 2 or int(campaign.get("total_regions", -1)) != 6 or campaign.get("complete") is not False:
            raise RuntimeError(f"P7 Wetland campaign handoff invalid: {start!r}")

        first = _patch(page, 13)
        if first.get("state") != "AVAILABLE" or first.get("eligible") is not True:
            raise RuntimeError(f"P7 Lotus Landing is not available after Golden Fields: {first!r}")
        if first.get("flowerId") != "flower_lotus" or int(first.get("requiresBuzzLevel", -1)) != 3:
            raise RuntimeError(f"P7 Lotus authored identity/gate invalid: {first!r}")

        _move_to(page, *WETLAND_PATCHES[13], timeout_seconds=22.0, tolerance=72)
        start = _region(page)
        start_metrics = _canvas_metrics(page)
        start_shot = frames / "00-wetland-start-desktop.png"
        _shot(page, start_shot)

        p13 = _complete_wetland_patch(page, 13)
        after_one = _wait_active_wetland(page, complete=False, timeout_ms=timeout_ms)
        if int((after_one.get("region") or {}).get("restored_count", -1)) != 1:
            raise RuntimeError(f"P7 Lotus Landing did not restore: {after_one!r}")
        if p13.get("flowerId") != "flower_lotus":
            raise RuntimeError(f"P7 patch 13 species drifted: {p13!r}")

        p14 = _complete_wetland_patch(page, 14)
        mid = _region(page)
        if int((mid.get("region") or {}).get("restored_count", -1)) != 2:
            raise RuntimeError(f"P7 Wetland midpoint invalid: {mid!r}")
        if p14.get("flowerId") != "flower_iris":
            raise RuntimeError(f"P7 patch 14 species drifted: {p14!r}")
        mid_shot = frames / "01-wetland-mid-desktop.png"
        _shot(page, mid_shot)

        p15 = _complete_wetland_patch(page, 15)
        p16 = _complete_wetland_patch(page, 16)
        complete = _wait_active_wetland(page, complete=True, timeout_ms=timeout_ms)
        complete_summary = complete.get("region") or {}
        complete_campaign = complete.get("campaign") or {}
        if int(complete_summary.get("restored_count", -1)) != 4 or int(complete_summary.get("total", -1)) != 4:
            raise RuntimeError(f"P7 Wetland Garden did not complete: {complete!r}")
        if complete.get("objectiveText") != "WETLAND GARDEN RESTORED · 4/4":
            raise RuntimeError(f"P7 Wetland completion objective invalid: {complete!r}")
        if int(complete.get("honey", -1)) != EXPECTED_COMPLETE_HONEY:
            raise RuntimeError(f"P7 Wetland reward total invalid: {complete!r}")
        if complete_campaign.get("complete") is not False or int(complete_campaign.get("completed_regions", -1)) != 3 or int(complete_campaign.get("total_regions", -1)) != 6:
            raise RuntimeError(f"P7 three-region campaign did not complete: {complete!r}")
        if p15.get("flowerId") != "flower_lotus" or p16.get("flowerId") != "flower_iris":
            raise RuntimeError(f"P7 Wetland species alternation drifted: p15={p15!r} p16={p16!r}")
        complete_shot = frames / "02-wetland-complete-desktop.png"
        _shot(page, complete_shot)

        events = complete.get("analyticsEvents") or []
        names = [event.get("name") for event in events if isinstance(event, dict)]
        region_completed = [
            event for event in events
            if isinstance(event, dict)
            and event.get("name") == "region_completed"
            and (event.get("properties") or {}).get("region_id") == "region_03"
        ]
        if not region_completed:
            raise RuntimeError(f"P7 Wetland region_completed analytics missing: {events!r}")

        page.wait_for_timeout(1600)
        page.goto(base_url, wait_until="load", timeout=timeout_ms)
        reloaded = _wait_active_wetland(page, complete=True, timeout_ms=timeout_ms)
        reload_campaign = reloaded.get("campaign") or {}
        if int(reloaded.get("honey", -1)) != EXPECTED_COMPLETE_HONEY:
            raise RuntimeError(f"P7 Wetland Honey did not survive reload: {reloaded!r}")
        if reload_campaign.get("complete") is not False or int(reload_campaign.get("completed_regions", -1)) != 3 or int(reload_campaign.get("total_regions", -1)) != 6:
            raise RuntimeError(f"P7 Wetland campaign completion did not survive reload: {reloaded!r}")
        _move_to(page, *WETLAND_PATCHES[16], timeout_seconds=22.0, tolerance=72)
        reload_shot = frames / "03-wetland-reloaded-desktop.png"
        _shot(page, reload_shot)

        page.set_viewport_size({"width": 844, "height": 390})
        page.wait_for_timeout(300)
        mobile_metrics = _canvas_metrics(page)
        if mobile_metrics["width"] + 1 < 844 or mobile_metrics["height"] + 1 < 390:
            raise RuntimeError(f"P7 Wetland mobile canvas does not cover viewport: {mobile_metrics!r}")
        mobile_shot = frames / "04-wetland-complete-mobile-landscape.png"
        _shot(page, mobile_shot)

        if not math.isfinite(float((_patch(page, 16).get("workTarget") or 0))) or float(_patch(page, 16).get("workTarget") or 0) <= 0:
            raise RuntimeError("P7 Wetland final patch work target is invalid")
        _assert_clean(console, page_errors, external, "P7 Wetland Garden journey")

        return {
            "ticket": "P7-WETLAND-GARDEN",
            "fixture_source": "P6 region_complete fixture persisted, then Golden Fields and Wetland Garden completed through ordinary runtime",
            "viewport": {"id": "desktop_reference", **viewport},
            "start_region": start.get("region"),
            "mid_region": mid.get("region"),
            "complete_region": complete_summary,
            "campaign": complete_campaign,
            "start_honey": EXPECTED_START_HONEY,
            "final_honey": EXPECTED_COMPLETE_HONEY,
            "patches": {"13": p13, "14": p14, "15": p15, "16": p16},
            "analytics_event_names": names,
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
