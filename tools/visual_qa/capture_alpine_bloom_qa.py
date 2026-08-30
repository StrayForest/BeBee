#!/usr/bin/env python3
"""P7 browser proof for the authored Alpine Bloom production-expansion slice."""
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
    _movement,
)


ALPINE_PATCHES = {
    21: (9600.0, 600.0),
    22: (10150.0, 1400.0),
    23: (10700.0, 820.0),
    24: (11250.0, 1540.0),
}
EXPECTED_START_HONEY = 2506
EXPECTED_COMPLETE_HONEY = 3636


def _wait_active_alpine_bloom(page: Page, *, complete: bool | None, timeout_ms: int) -> dict[str, object]:
    page.wait_for_function(
        """(expectedComplete) => {
            const qa = window.__bebeeRegionQA;
            if (!qa) return false;
            if (expectedComplete !== true) {
                return qa.activeRegionId === 'region_05' && !!qa.region &&
                    qa.region.id === 'region_05' && qa.region.complete === expectedComplete;
            }
            const alpine = (qa.campaign?.regions || []).find((region) => region.id === 'region_05');
            return !!alpine && alpine.complete === true && alpine.restored_count === alpine.total;
        }""",
        arg=complete,
        timeout=timeout_ms,
    )
    snapshot = _region(page)
    if complete:
        campaign = snapshot.get("campaign") or {}
        alpine = next((region for region in campaign.get("regions", []) if region.get("id") == "region_05"), None)
        if alpine is not None:
            snapshot["region"] = alpine
            snapshot["objectiveText"] = f"ALPINE BLOOM RESTORED · {alpine.get('restored_count', 0)}/{alpine.get('total', 0)}"
    return snapshot


def _complete_alpine_patch(page: Page, index: int, *, timeout_seconds: float = 24.0) -> dict[str, object]:
    x, y = ALPINE_PATCHES[index]
    start_movement = _movement(page)
    try:
        _move_to(page, x, y, timeout_seconds=40.0, tolerance=72)
    except RuntimeError as exc:
        raise RuntimeError(f"P7 Alpine Bloom patch {index} navigation failed: start={start_movement!r}; {exc}") from exc
    deadline = time.monotonic() + timeout_seconds
    direction_right = True
    while time.monotonic() < deadline:
        current = _patch(page, index)
        if current.get("state") == "COMPLETED":
            return current
        _move_to(page, x + (84 if direction_right else -84), y, timeout_seconds=3.0, tolerance=22)
        direction_right = not direction_right
    raise RuntimeError(f"P7 Alpine Bloom patch {index} did not complete: {_patch(page, index)!r}")


def _assert_start(payload: dict[str, object]) -> None:
    summary = payload.get("region") or {}
    campaign = payload.get("campaign") or {}
    if summary.get("id") != "region_05" or int(summary.get("restored_count", -1)) != 0 or int(summary.get("total", -1)) != 4:
        raise RuntimeError(f"P7 Alpine Bloom start summary invalid: {payload!r}")
    if payload.get("objectiveText") != "RESTORE SNOWDROP PASS · 0/4":
        raise RuntimeError(f"P7 Alpine Bloom objective invalid: {payload!r}")
    if int(payload.get("honey", -1)) != EXPECTED_START_HONEY:
        raise RuntimeError(f"P7 Alpine Bloom fixture Honey drifted: {payload!r}")
    if int(payload.get("flightLevel", -1)) != 3 or int(payload.get("buzzLevel", -1)) != 3:
        raise RuntimeError(f"P7 Alpine Bloom must reuse validated progression: {payload!r}")
    if int(campaign.get("completed_regions", -1)) != 4 or int(campaign.get("total_regions", -1)) != 6:
        raise RuntimeError(f"P7 Alpine Bloom campaign transition invalid: {payload!r}")


def record_alpine_bloom(
    browser: Browser,
    *,
    base_url: str,
    head_sha: str,
    output_root: Path,
    timeout_ms: int,
) -> dict[str, object]:
    viewport = {"width": 1280, "height": 720}
    frames = output_root / "p7_alpine_bloom"
    context = browser.new_context(viewport=viewport, screen=viewport, device_scale_factor=1)
    page = context.new_page()
    console, page_errors = _errors(page)
    external = _external_requests(page, base_url)
    session = context.new_cdp_session(page)
    try:
        page.goto(
            _url(base_url, qa="alpine_bloom_start", qa_seed=88008, alpine_bloom_storage_lifecycle="reset"),
            wait_until="load",
            timeout=timeout_ms,
        )
        start = _wait(page, head_sha, "alpine_bloom_start", timeout_ms)
        _assert_start(start)

        first = _patch(page, 21)
        if first.get("state") not in {"AVAILABLE", "ACTIVE"} or first.get("eligible") is not True:
            raise RuntimeError(f"P7 Alpine Bloom first patch is not available: {first!r}")
        if first.get("flowerId") != "flower_edelweiss" or int(first.get("requiresBuzzLevel", -1)) != 3:
            raise RuntimeError(f"P7 Snowdrop Pass authored identity/gate invalid: {first!r}")

        _move_to(page, *ALPINE_PATCHES[21], timeout_seconds=22.0, tolerance=72)
        start_metrics = _canvas_metrics(page)
        start_shot = frames / "00-alpine_bloom-start-desktop.png"
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
            raise RuntimeError(f"P7 Alpine Bloom fixture persistence failed: {_region(page)!r}")
        _dispatch_key(session, page, 27)
        page.wait_for_function("() => window.__bebeeRegionQA && window.__bebeeRegionQA.settingsOpen === false", timeout=timeout_ms)
        page.wait_for_timeout(1600)
        page.goto(base_url, wait_until="load", timeout=timeout_ms)

        ordinary = _wait_active_alpine_bloom(page, complete=False, timeout_ms=timeout_ms)
        _assert_start(ordinary)

        p17 = _complete_alpine_patch(page, 21)
        after_one = _wait_active_alpine_bloom(page, complete=False, timeout_ms=timeout_ms)
        if int((after_one.get("region") or {}).get("restored_count", -1)) != 1:
            raise RuntimeError(f"P7 Snowdrop Pass did not restore: {after_one!r}")
        if p17.get("flowerId") != "flower_edelweiss":
            raise RuntimeError(f"P7 Rose patch species drifted: {p17!r}")

        p18 = _complete_alpine_patch(page, 22)
        mid = _region(page)
        if int((mid.get("region") or {}).get("restored_count", -1)) != 2:
            raise RuntimeError(f"P7 Alpine Bloom midpoint invalid: {mid!r}")
        if p18.get("flowerId") != "flower_anemone":
            raise RuntimeError(f"P7 Anemone patch species drifted: {p18!r}")
        mid_shot = frames / "01-alpine_bloom-mid-desktop.png"
        _shot(page, mid_shot)

        p19 = _complete_alpine_patch(page, 23)
        p20 = _complete_alpine_patch(page, 24)
        complete = _wait_active_alpine_bloom(page, complete=True, timeout_ms=timeout_ms)
        complete_summary = complete.get("region") or {}
        campaign = complete.get("campaign") or {}
        if int(complete_summary.get("restored_count", -1)) != 4 or int(complete_summary.get("total", -1)) != 4:
            raise RuntimeError(f"P7 Alpine Bloom did not complete: {complete!r}")
        if complete.get("objectiveText") != "ALPINE BLOOM RESTORED · 4/4":
            raise RuntimeError(f"P7 Alpine Bloom completion objective invalid: {complete!r}")
        if int(complete.get("honey", -1)) != EXPECTED_COMPLETE_HONEY:
            raise RuntimeError(f"P7 Alpine Bloom reward total invalid: {complete!r}")
        if campaign.get("complete") is not False or int(campaign.get("completed_regions", -1)) != 5 or int(campaign.get("total_regions", -1)) != 6:
            raise RuntimeError(f"P7 four-region campaign did not complete: {complete!r}")
        if p19.get("flowerId") != "flower_edelweiss" or p20.get("flowerId") != "flower_anemone":
            raise RuntimeError(f"P7 Alpine Bloom species alternation drifted: p19={p19!r} p20={p20!r}")
        complete_shot = frames / "02-alpine_bloom-complete-desktop.png"
        _shot(page, complete_shot)

        events = complete.get("analyticsEvents") or []
        region_completed = [
            event for event in events
            if isinstance(event, dict)
            and event.get("name") == "region_completed"
            and (event.get("properties") or {}).get("region_id") == "region_05"
        ]
        if not region_completed:
            raise RuntimeError(f"P7 Alpine Bloom region_completed analytics missing: {events!r}")

        page.wait_for_timeout(1600)
        page.goto(base_url, wait_until="load", timeout=timeout_ms)
        reloaded = _wait_active_alpine_bloom(page, complete=True, timeout_ms=timeout_ms)
        reload_campaign = reloaded.get("campaign") or {}
        if int(reloaded.get("honey", -1)) != EXPECTED_COMPLETE_HONEY:
            raise RuntimeError(f"P7 Alpine Bloom Honey did not survive reload: {reloaded!r}")
        if reload_campaign.get("complete") is not False or int(reload_campaign.get("completed_regions", -1)) != 5:
            raise RuntimeError(f"P7 Alpine Bloom campaign completion did not survive reload: {reloaded!r}")
        _move_to(page, *ALPINE_PATCHES[24], timeout_seconds=40.0, tolerance=72)
        reload_shot = frames / "03-alpine_bloom-reloaded-desktop.png"
        _shot(page, reload_shot)

        page.set_viewport_size({"width": 844, "height": 390})
        page.wait_for_timeout(300)
        mobile_metrics = _canvas_metrics(page)
        if mobile_metrics["width"] + 1 < 844 or mobile_metrics["height"] + 1 < 390:
            raise RuntimeError(f"P7 Alpine Bloom mobile canvas does not cover viewport: {mobile_metrics!r}")
        mobile_shot = frames / "04-alpine_bloom-complete-mobile-landscape.png"
        _shot(page, mobile_shot)

        if not math.isfinite(float((_patch(page, 24).get("workTarget") or 0))) or float(_patch(page, 24).get("workTarget") or 0) <= 0:
            raise RuntimeError("P7 Alpine Bloom final patch work target is invalid")
        _assert_clean(console, page_errors, external, "P7 Alpine Bloom journey")

        return {
            "ticket": "P7-ALPINE_BLOOM",
            "fixture_source": "P7 Rosewood completion fixture persisted through real settings save, then Alpine Bloom completed through ordinary runtime",
            "viewport": {"id": "desktop_reference", **viewport},
            "start_region": start.get("region"),
            "mid_region": mid.get("region"),
            "complete_region": complete_summary,
            "campaign": campaign,
            "start_honey": EXPECTED_START_HONEY,
            "final_honey": EXPECTED_COMPLETE_HONEY,
            "patches": {"21": p17, "22": p18, "23": p19, "24": p20},
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
