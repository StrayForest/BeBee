#!/usr/bin/env python3
"""Exercise BeBee P1-P7 runtime milestones in real Chromium."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from capture_movement_qa_impl import (
    record_desktop_motion,
    record_touch_motion,
    verify_modal_and_reduced_motion,
)
from capture_pollination_qa import record_pollination_core
from capture_progression_qa import record_progression
from capture_restoration_qa import record_restoration
from capture_seed_qa import record_seed_ownership
from capture_region_qa import record_region
from capture_golden_fields_qa import record_golden_fields


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--url", default="http://127.0.0.1:8000/development/BeBee/")
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=20)
    args = parser.parse_args()

    head_sha = args.head_sha.strip().lower()
    if len(head_sha) != 40 or any(ch not in "0123456789abcdef" for ch in head_sha):
        raise RuntimeError("--head-sha must be a full 40-character Git SHA")
    output_root = args.output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    timeout_ms = args.timeout_seconds * 1000

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            desktop = record_desktop_motion(browser, base_url=args.url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
            touch = record_touch_motion(browser, base_url=args.url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
            safety = verify_modal_and_reduced_motion(browser, base_url=args.url, head_sha=head_sha, timeout_ms=timeout_ms)
            pollination = record_pollination_core(browser, base_url=args.url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
            progression = record_progression(browser, base_url=args.url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
            restoration = record_restoration(browser, base_url=args.url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
            seeds = record_seed_ownership(browser, base_url=args.url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
            first_region = record_region(browser, base_url=args.url, head_sha=head_sha, output_root=output_root, timeout_ms=timeout_ms)
            golden_fields = record_golden_fields(browser, base_url=args.url, head_sha=head_sha, output_root=output_root, timeout_ms=max(timeout_ms, 30000))
            browser_version = browser.version
        finally:
            browser.close()

    report = {
        "schema_version": 6,
        "ticket": "P1-P7-RUNTIME",
        "head_sha": head_sha,
        "browser_name": "Playwright Chromium",
        "browser_version": browser_version,
        "qa_seed": 88008,
        "desktop_keyboard": desktop,
        "mobile_touch": touch,
        "focus_and_accessibility": safety,
        "p2_pollination_core": pollination,
        "p3_progression": progression,
        "p4_restoration": restoration,
        "p5_seed_ownership": seeds,
        "p6_first_region": first_region,
        "p7_golden_fields": golden_fields,
        "result": "PASS",
    }
    report_path = output_root / "motion-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "P1-P7 browser proof: PASS "
        f"(desktop movement {desktop['exercise_seconds']}s, touch movement {touch['exercise_seconds']}s, "
        f"desktop movement {desktop['observed_fps']} fps, P2={pollination['result']}, "
        f"P3={progression['result']}, P4={restoration['result']}, P5={seeds['result']}, "
        f"P6={first_region['result']}, P7={golden_fields['result']})"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"P1-P7 browser proof failed: {exc}")
        raise SystemExit(1)
