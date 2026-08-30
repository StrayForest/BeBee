#!/usr/bin/env python3
"""Browser-level BB-007 persistence and recovery smoke for Defold HTML5 bundles."""

from __future__ import annotations

import argparse
import json
import tempfile
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import Page, sync_playwright


def with_query(base: str, **updates: str) -> str:
    parts = urlsplit(base)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update(updates)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _platform_sdk_url(url: object) -> bool:
    hostname = (urlsplit(str(url or "")).hostname or "").lower()
    suffixes = (
        ".poki.com",
        ".poki-cdn.com",
        ".poki.io",
        ".crazygames.com",
        ".googleapis.com",
        ".doubleclick.net",
        ".amazon-adsystem.com",
        ".2mdn.net",
        ".googlesyndication.com",
        ".jsdelivr.net",
        ".publisher-services.amazon.dev",
    )
    return any(hostname == suffix[1:] or hostname.endswith(suffix) for suffix in suffixes)


def _platform_console_message(text: object) -> bool:
    value = str(text or "")
    return "ads.poki.com" in value or "crazygames.com" in value


def wait_result(page: Page, scenario: str, timeout_ms: int = 15000) -> dict:
    page.wait_for_function(
        "() => window.__bebeeStorageTest && window.__bebeeStorageTest.ready === true",
        timeout=timeout_ms,
    )
    result = page.evaluate("() => window.__bebeeStorageTest")
    if not isinstance(result, dict):
        raise AssertionError(f"{scenario}: storage bridge did not return an object")
    if result.get("scenario") != scenario:
        raise AssertionError(f"{scenario}: bridge scenario mismatch: {result!r}")
    return result


def require_ok(result: dict, scenario: str) -> None:
    if result.get("ok") is not True:
        raise AssertionError(f"{scenario}: expected ok result, got {result!r}")


def marker_of(result: dict) -> str | None:
    value = result.get("value")
    if not isinstance(value, dict):
        return None
    marker = value.get("marker")
    return marker if isinstance(marker, str) else None


def require_marker(result: dict, expected: str, scenario: str) -> None:
    if marker_of(result) != expected:
        raise AssertionError(f"{scenario}: expected marker {expected!r}, got {result!r}")


def require_clean_start(result: dict, scenario: str) -> None:
    require_ok(result, scenario)
    if result.get("code") != "not_found_clean_start" or result.get("value") is not None:
        raise AssertionError(f"{scenario}: expected clean start, got {result!r}")


def classify_rapid_window(
    result: dict,
    *,
    latest_marker: str,
    confirmed_marker: str,
    scenario: str,
) -> str:
    """Validate BB-P009's bounded pending-durability window.

    Defold HTML5 starts an asynchronous MEM->IndexedDB sync when FS.close runs.
    `accepted_local_pending_browser_persistence` therefore cannot promise that a
    navigation racing that sync will retain the just-accepted generation. The
    rapid-window invariant is stricter about integrity instead: after reload we
    must get either the newest generation or the last previously confirmed
    generation through explicit recovery, never corruption/clean-start/unknown
    state.
    """

    require_ok(result, scenario)
    marker = marker_of(result)
    if marker == latest_marker:
        return "latest_generation_persisted"
    if marker == confirmed_marker:
        if result.get("recovery") is not True:
            raise AssertionError(
                f"{scenario}: previous generation loaded without explicit recovery metadata: {result!r}"
            )
        if result.get("code") not in {
            "recovered_single_valid_slot",
            "recovered_newest_generation",
        }:
            raise AssertionError(
                f"{scenario}: previous generation recovery code is not explicit: {result!r}"
            )
        return "pending_generation_lost_recovered_confirmed_previous"
    raise AssertionError(
        f"{scenario}: expected latest {latest_marker!r} or confirmed previous "
        f"{confirmed_marker!r}, got {result!r}"
    )


def attach_error_capture(page: Page, errors: list[str]) -> None:
    platform_request_seen = False

    def on_request(request) -> None:
        nonlocal platform_request_seen
        if _platform_sdk_url(request.url):
            platform_request_seen = True

    def on_console(message) -> None:
        if message.type != "error":
            return
        text = message.text
        if _platform_console_message(text):
            return
        if platform_request_seen and "Failed to load resource: net::ERR_FAILED" in text:
            return
        if "Cross-Origin-Opener-Policy header has been ignored" in text:
            return
        errors.append(f"console:{message.type}:{text}")

    page.on("request", on_request)
    page.on("console", on_console)
    page.on("pageerror", lambda error: errors.append(f"pageerror:{error}"))


def run_scenario(page: Page, base_url: str, scenario: str, marker: str = "") -> dict:
    page.goto(with_query(base_url, storage_test=scenario, marker=marker), wait_until="load")
    return wait_result(page, scenario)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--development-url", required=True)
    parser.add_argument("--release-url", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--settle-seconds", type=float, default=1.0)
    args = parser.parse_args()

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    checks: list[dict] = []

    with tempfile.TemporaryDirectory(prefix="bebee-storage-profile-") as profile_dir:
        with sync_playwright() as playwright:
            context = playwright.chromium.launch_persistent_context(
                profile_dir,
                headless=True,
                viewport={"width": 1280, "height": 720},
            )
            page = context.pages[0] if context.pages else context.new_page()
            attach_error_capture(page, errors)

            clean = run_scenario(page, args.development_url, "clean")
            require_clean_start(clean, "clean")
            checks.append({"id": "clean_start", "result": clean})

            normal_marker = "normal-save-reload"
            saved = run_scenario(page, args.development_url, "save", normal_marker)
            require_ok(saved, "save")
            if saved.get("durability") != "accepted_local_pending_browser_persistence":
                raise AssertionError(f"save: durability semantics mismatch {saved!r}")
            time.sleep(args.settle_seconds)
            verified = run_scenario(page, args.development_url, "verify")
            require_ok(verified, "verify")
            require_marker(verified, normal_marker, "normal_save_reload")
            checks.append({"id": "normal_save_reload", "save": saved, "load": verified})

            # Do not erase the confirmed baseline. The point of this case is to
            # race a newly accepted *pending* generation against navigation and
            # prove bounded recovery if IndexedDB has not committed it yet.
            immediate_marker = "immediate-refresh"
            immediate_saved = run_scenario(page, args.development_url, "save", immediate_marker)
            require_ok(immediate_saved, "save_immediate_refresh")
            if immediate_saved.get("durability") != "accepted_local_pending_browser_persistence":
                raise AssertionError(
                    f"save_immediate_refresh: durability semantics mismatch {immediate_saved!r}"
                )
            verified_immediate = run_scenario(page, args.development_url, "verify")
            immediate_outcome = classify_rapid_window(
                verified_immediate,
                latest_marker=immediate_marker,
                confirmed_marker=normal_marker,
                scenario="save_immediate_refresh",
            )
            checks.append(
                {
                    "id": "save_immediate_refresh",
                    "expectation": "latest_or_explicit_recovery_to_last_confirmed",
                    "outcome": immediate_outcome,
                    "save": immediate_saved,
                    "load": verified_immediate,
                }
            )

            # Reset and let Defold's asynchronous persistence settle before the
            # next independent scenario.
            reset = run_scenario(page, args.development_url, "clean")
            require_clean_start(reset, "reset_before_quick_checkpoints")
            time.sleep(args.settle_seconds)
            reset_reloaded = run_scenario(page, args.development_url, "verify")
            require_clean_start(reset_reloaded, "delete_persists_after_reload")
            checks.append({"id": "delete_persists_after_reload", "result": reset_reloaded})

            quick_marker = "checkpoint"
            quick = run_scenario(page, args.development_url, "quick_checkpoints", quick_marker)
            require_ok(quick, "quick_checkpoints")
            require_marker(quick, quick_marker + "-3", "quick_checkpoints")
            if quick.get("diagnostics", {}).get("last_generation") != 3:
                raise AssertionError(f"quick_checkpoints: expected generation 3, got {quick!r}")
            time.sleep(args.settle_seconds)
            quick_reloaded = run_scenario(page, args.development_url, "verify")
            require_ok(quick_reloaded, "quick_checkpoints_reload")
            require_marker(quick_reloaded, quick_marker + "-3", "quick_checkpoints_reload")
            checks.append(
                {
                    "id": "multiple_quick_progression_checkpoints",
                    "result": quick,
                    "reloaded": quick_reloaded,
                }
            )

            corrupt_marker = "corrupt"
            recovered = run_scenario(page, args.development_url, "corrupt_newest", corrupt_marker)
            require_ok(recovered, "corrupt_newest")
            require_marker(recovered, corrupt_marker + "-stable", "corrupt_newest")
            if recovered.get("code") != "recovered_single_valid_slot" or recovered.get("recovery") is not True:
                raise AssertionError(f"corrupt_newest: recovery semantics mismatch {recovered!r}")
            checks.append({"id": "slot_b_corrupt_slot_a_valid", "result": recovered})

            # Establish a separately confirmed generation before the close race.
            reset = run_scenario(page, args.development_url, "clean")
            require_clean_start(reset, "reset_before_rapid_close")
            time.sleep(args.settle_seconds)
            require_clean_start(
                run_scenario(page, args.development_url, "verify"),
                "reset_before_rapid_close_reload",
            )

            close_baseline = "rapid-close-confirmed"
            close_baseline_saved = run_scenario(
                page, args.development_url, "save", close_baseline
            )
            require_ok(close_baseline_saved, "rapid_close_baseline_save")
            time.sleep(args.settle_seconds)
            close_baseline_verified = run_scenario(page, args.development_url, "verify")
            require_ok(close_baseline_verified, "rapid_close_baseline_verify")
            require_marker(
                close_baseline_verified,
                close_baseline,
                "rapid_close_baseline_verify",
            )

            close_marker = "rapid-close-reopen"
            close_saved = run_scenario(page, args.development_url, "save", close_marker)
            require_ok(close_saved, "rapid_close_save")
            if close_saved.get("durability") != "accepted_local_pending_browser_persistence":
                raise AssertionError(f"rapid_close_save: durability mismatch {close_saved!r}")
            context.close()

            context = playwright.chromium.launch_persistent_context(
                profile_dir,
                headless=True,
                viewport={"width": 1280, "height": 720},
            )
            page = context.pages[0] if context.pages else context.new_page()
            attach_error_capture(page, errors)
            reopened = run_scenario(page, args.development_url, "verify")
            close_outcome = classify_rapid_window(
                reopened,
                latest_marker=close_marker,
                confirmed_marker=close_baseline,
                scenario="rapid_close_reopen",
            )
            checks.append(
                {
                    "id": "save_rapid_close_reopen",
                    "expectation": "latest_or_explicit_recovery_to_last_confirmed",
                    "outcome": close_outcome,
                    "save": close_saved,
                    "load": reopened,
                }
            )

            page.goto(with_query(args.release_url, storage_test="verify"), wait_until="load")
            page.wait_for_timeout(1500)
            release_bridge_names = [
                name
                for name in [
                    "__bebeeQA",
                    "__bebeeStorageTest",
                    "__bebeeMovementQA",
                    "__bebeePollinationQA",
                    "__bebeeProgressionQA",
                    "__bebeeSeedQA",
                    "__bebeeRegionQA",
                    "__bebeeRestorationQA",
                ]
                if page.evaluate(f"() => typeof window.{name} !== 'undefined'")
            ]
            if release_bridge_names:
                raise AssertionError(
                    "release bundle exposed development QA bridges: "
                    + ", ".join(release_bridge_names)
                )
            checks.append({"id": "release_probe_absent", "bridge_present": False})
            checks.append(
                {
                    "id": "release_debug_bridges_absent",
                    "bridge_present": False,
                    "bridge_names": release_bridge_names,
                }
            )
            browser_version = context.browser.version if context.browser else "unknown"
            context.close()

    if errors:
        raise AssertionError("browser errors: " + " | ".join(errors))

    report = {
        "schema_version": 2,
        "ticket": "BB-007",
        "status": "pass",
        "durability_model": "accepted_local_pending_browser_persistence",
        "rapid_window_invariant": "latest_or_explicit_recovery_to_last_confirmed",
        "browser": browser_version,
        "development_url": args.development_url,
        "release_url": args.release_url,
        "checks": checks,
        "browser_errors": errors,
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
