#!/usr/bin/env python3
"""Validate the BB-P008 deterministic visual-QA contract without runtime dependencies."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA_PATH = ROOT / "config" / "visual-qa.json"
STYLE_PATH = ROOT / "config" / "visual-style.json"

REQUIRED_CATEGORIES = {
    "movement",
    "pollination",
    "gating",
    "hud",
    "hive",
    "seed",
    "restoration",
}
REQUIRED_STATE_IDS = {
    "movement_empty",
    "movement_dense",
    "pollination_idle",
    "pollination_active_50",
    "pollination_complete",
    "flower_soft_gate",
    "flower_hard_gate",
    "hud_default",
    "hive_affordable",
    "hive_unaffordable",
    "seed_locked",
    "seed_unlocked",
    "meadow_dormant",
    "meadow_mid",
    "meadow_restored",
}
CAPTURE_KINDS = {"still", "still_and_motion"}
ROUTE_RE = re.compile(r"^\?qa=([a-z0-9_]+)$")
SHA_FIELDS = {"bundle_sha256", "capture_sha256"}


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} root must be an object")
    return data


def validate(qa: dict, style: dict) -> list[str]:
    errors: list[str] = []

    def need(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    need(qa.get("schema_version") == 1, "visual QA schema_version must be 1")
    need(qa.get("ticket") == "BB-P008", "visual QA ticket must be BB-P008")
    need(qa.get("status") == "VALIDATED", "BB-P008 contract must be VALIDATED")

    runtime = qa.get("runtime_contract", {})
    need(isinstance(runtime, dict), "runtime_contract must be an object")
    if isinstance(runtime, dict):
        need(runtime.get("query_parameter") == "qa", "canonical QA query parameter must be qa")
        need(runtime.get("seed_parameter") == "qa_seed", "canonical QA seed parameter must be qa_seed")
        need(isinstance(runtime.get("default_seed"), int), "default QA seed must be an integer")
        need(runtime.get("disabled_in_release") is True, "QA state injection must be disabled in release")
        need(runtime.get("unknown_state_behavior") == "fail_closed", "unknown QA states must fail closed")
        bridge = runtime.get("required_bridge_fields", [])
        need(isinstance(bridge, list) and {"stateId", "seed", "captureReady", "buildCommitSha"}.issubset(set(bridge)), "bridge fields must bind state, seed, readiness and exact build SHA")

    viewports = qa.get("viewports", [])
    need(isinstance(viewports, list) and bool(viewports), "viewports must be a non-empty list")
    viewport_by_id: dict[str, dict] = {}
    if isinstance(viewports, list):
        for item in viewports:
            if not isinstance(item, dict):
                errors.append("viewport entries must be objects")
                continue
            viewport_id = item.get("id")
            if not isinstance(viewport_id, str) or not viewport_id:
                errors.append("viewport id must be non-empty")
                continue
            if viewport_id in viewport_by_id:
                errors.append(f"duplicate viewport id: {viewport_id}")
            viewport_by_id[viewport_id] = item
            need(isinstance(item.get("width"), int) and item["width"] > 0, f"viewport {viewport_id} width must be positive integer")
            need(isinstance(item.get("height"), int) and item["height"] > 0, f"viewport {viewport_id} height must be positive integer")
            need(isinstance(item.get("role"), str) and bool(item["role"].strip()), f"viewport {viewport_id} role must be explained")

    style_viewport = style.get("reference_viewport", {})
    expected_viewports = {
        "desktop_reference": (style_viewport.get("width"), style_viewport.get("height")),
    }
    portal_examples = style_viewport.get("portal_scale_examples", [])
    if isinstance(portal_examples, list) and len(portal_examples) == 3:
        expected_viewports.update({
            "poki_small": tuple(portal_examples[0]),
            "poki_medium": tuple(portal_examples[1]),
            "poki_large": tuple(portal_examples[2]),
        })
    mobile = style_viewport.get("mobile_qa", [])
    if isinstance(mobile, list) and len(mobile) == 2:
        expected_viewports["mobile_landscape"] = tuple(mobile)

    for viewport_id, dims in expected_viewports.items():
        item = viewport_by_id.get(viewport_id)
        need(item is not None, f"missing V-001 viewport in QA plan: {viewport_id}")
        if item:
            need((item.get("width"), item.get("height")) == dims, f"QA viewport {viewport_id} drifts from config/visual-style.json")

    states = qa.get("states", [])
    need(isinstance(states, list) and bool(states), "states must be a non-empty list")
    seen: set[str] = set()
    categories: set[str] = set()
    if isinstance(states, list):
        for state in states:
            if not isinstance(state, dict):
                errors.append("state entries must be objects")
                continue
            state_id = state.get("id")
            if not isinstance(state_id, str) or not state_id:
                errors.append("state id must be non-empty")
                continue
            if state_id in seen:
                errors.append(f"duplicate QA state id: {state_id}")
            seen.add(state_id)

            route = state.get("route")
            match = ROUTE_RE.fullmatch(route or "") if isinstance(route, str) else None
            need(match is not None and match.group(1) == state_id, f"state {state_id} route must be exactly ?qa={state_id}")

            category = state.get("category")
            if isinstance(category, str):
                categories.add(category)
            else:
                errors.append(f"state {state_id} category must be a string")
            need(state.get("capture_kind") in CAPTURE_KINDS, f"state {state_id} has invalid capture_kind")

            state_viewports = state.get("default_viewports")
            need(isinstance(state_viewports, list) and bool(state_viewports), f"state {state_id} needs at least one default viewport")
            if isinstance(state_viewports, list):
                for viewport_id in state_viewports:
                    need(viewport_id in viewport_by_id, f"state {state_id} references unknown viewport {viewport_id}")

            assertions = state.get("assertions")
            need(isinstance(assertions, list) and any(isinstance(v, str) and v.strip() for v in assertions or []), f"state {state_id} needs observable assertions")

    need(REQUIRED_STATE_IDS.issubset(seen), "QA plan is missing one or more canonical BB-P008 states")
    need(REQUIRED_CATEGORIES.issubset(categories), "QA plan is missing one or more required evidence categories")

    hud = next((item for item in states if isinstance(item, dict) and item.get("id") == "hud_default"), None)
    if isinstance(hud, dict):
        need(set(hud.get("default_viewports", [])) == set(viewport_by_id), "hud_default must cover every configured baseline viewport")

    pipeline = qa.get("capture_pipeline", {})
    need(isinstance(pipeline, dict), "capture_pipeline must be an object")
    if isinstance(pipeline, dict):
        need(pipeline.get("builder") == "Defold Bob CLI", "P0 capture builder must be Defold Bob CLI")
        need(pipeline.get("bundle_target") == "HTML5", "visual capture target must be HTML5")
        serve = str(pipeline.get("serve_requirement", ""))
        need("HTTP" in serve and "file://" in serve, "serve contract must require HTTP and forbid file://")
        need(pipeline.get("browser_runner") == "Playwright Chromium", "browser runner must be Playwright Chromium")
        need(isinstance(pipeline.get("readiness_timeout_seconds"), int) and 1 <= pipeline["readiness_timeout_seconds"] <= 60, "readiness timeout must be bounded to 1..60 seconds")
        steps = pipeline.get("steps", [])
        need(isinstance(steps, list) and any("build one HTML5 bundle" in str(step) for step in steps), "pipeline must build one exact-head HTML5 bundle")
        need(any("buildCommitSha" in str(step) for step in steps), "pipeline must assert exact-head buildCommitSha")
        need(any("page errors" in str(step) for step in steps), "pipeline must collect browser page errors")

    artifact = qa.get("artifact_contract", {})
    need(isinstance(artifact, dict), "artifact_contract must be an object")
    if isinstance(artifact, dict):
        fields = artifact.get("report_required_fields", [])
        need(isinstance(fields, list), "report_required_fields must be a list")
        if isinstance(fields, list):
            required = {"head_sha", "state_id", "qa_seed", "viewport_id", "capture_file", "console_error_count", "page_error_count"} | SHA_FIELDS
            need(required.issubset(set(fields)), "capture report does not bind enough provenance/error data")

    failure = qa.get("failure_policy", {})
    need(isinstance(failure, dict), "failure_policy must be an object")
    if isinstance(failure, dict):
        fail_when = failure.get("fail_capture_when", [])
        joined = "\n".join(str(v) for v in fail_when) if isinstance(fail_when, list) else ""
        need("buildCommitSha mismatch" in joined, "failure policy must reject exact-build SHA mismatch")
        need("release bundle exposes QA bridge" in joined, "failure policy must reject release QA exposure")
        need("required screenshot or motion artifact missing" in joined, "failure policy must reject missing evidence")

    return errors


def main() -> int:
    qa = load_json(QA_PATH)
    style = load_json(STYLE_PATH)
    errors = validate(qa, style)
    if errors:
        print("BB-P008 visual QA plan validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"BB-P008 visual QA plan: PASS ({len(qa['states'])} states, {len(qa['viewports'])} viewports)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
