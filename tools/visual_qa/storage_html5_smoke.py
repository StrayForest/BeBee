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


def require_marker(result: dict, expected: str, scenario: str) -> None:
    value = result.get("value")
    if not isinstance(value, dict) or value.get("marker") != expected:
        raise AssertionError(f"{scenario}: expected marker {expected!r}, got {result!r}")


def attach_error_capture(page: Page, errors: list[str]) -> None:
    page.on(
        "console",
        lambda message: errors.append(f"console:{message.type}:{message.text}")
        if message.type == "error"
        else None,
    )
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
            require_ok(clean, "clean")
            if clean.get("code") != "not_found_clean_start":
                raise AssertionError(f"clean: unexpected result {clean!r}")
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

            run_scenario(page, args.development_url, "clean")
            immediate_marker = "immediate-refresh"
            immediate_saved = run_scenario(page, args.development_url, "save", immediate_marker)
            require_ok(immediate_saved, "save_immediate_refresh")
            verified_immediate = run_scenario(page, args.development_url, "verify")
            require_ok(verified_immediate, "verify_immediate_refresh")
            require_marker(verified_immediate, immediate_marker, "save_immediate_refresh")
            checks.append(
                {
                    "id": "save_immediate_refresh",
                    "save": immediate_saved,
                    "load": verified_immediate,
                }
            )

            quick_marker = "checkpoint"
            quick = run_scenario(page, args.development_url, "quick_checkpoints", quick_marker)
            require_ok(quick, "quick_checkpoints")
            require_marker(quick, quick_marker + "-3", "quick_checkpoints")
            if quick.get("diagnostics", {}).get("last_generation") != 3:
                raise AssertionError(f"quick_checkpoints: expected generation 3, got {quick!r}")
            checks.append({"id": "multiple_quick_progression_checkpoints", "result": quick})

            corrupt_marker = "corrupt"
            recovered = run_scenario(page, args.development_url, "corrupt_newest", corrupt_marker)
            require_ok(recovered, "corrupt_newest")
            require_marker(recovered, corrupt_marker + "-stable", "corrupt_newest")
            if recovered.get("code") != "recovered_single_valid_slot" or recovered.get("recovery") is not True:
                raise AssertionError(f"corrupt_newest: recovery semantics mismatch {recovered!r}")
            checks.append({"id": "slot_b_corrupt_slot_a_valid", "result": recovered})

            run_scenario(page, args.development_url, "clean")
            close_marker = "rapid-close-reopen"
            close_saved = run_scenario(page, args.development_url, "save", close_marker)
            require_ok(close_saved, "rapid_close_save")
            context.close()

            context = playwright.chromium.launch_persistent_context(
                profile_dir,
                headless=True,
                viewport={"width": 1280, "height": 720},
            )
            page = context.pages[0] if context.pages else context.new_page()
            attach_error_capture(page, errors)
            reopened = run_scenario(page, args.development_url, "verify")
            require_ok(reopened, "rapid_close_reopen")
            require_marker(reopened, close_marker, "rapid_close_reopen")
            checks.append({"id": "save_rapid_close_reopen", "save": close_saved, "load": reopened})

            page.goto(with_query(args.release_url, storage_test="verify"), wait_until="load")
            page.wait_for_timeout(1500)
            release_bridge_present = page.evaluate(
                "() => typeof window.__bebeeStorageTest !== 'undefined'"
            )
            if release_bridge_present:
                raise AssertionError("release bundle exposed development storage bridge")
            checks.append(
                {
                    "id": "release_probe_absent",
                    "bridge_present": release_bridge_present,
                }
            )
            browser_version = context.browser.version if context.browser else "unknown"
            context.close()

    if errors:
        raise AssertionError("browser errors: " + " | ".join(errors))

    report = {
        "schema_version": 1,
        "ticket": "BB-007",
        "status": "pass",
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
