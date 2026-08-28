#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "visual_qa" / "check_visual_qa_plan.py"

spec = importlib.util.spec_from_file_location("check_visual_qa_plan", MODULE_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class VisualQAPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.qa = load("config/visual-qa.json")
        self.style = load("config/visual-style.json")

    def errors_for(self, mutate) -> list[str]:
        qa = copy.deepcopy(self.qa)
        style = copy.deepcopy(self.style)
        mutate(qa, style)
        return checker.validate(qa, style)

    def assertRejected(self, mutate, needle: str) -> None:
        errors = self.errors_for(mutate)
        self.assertTrue(any(needle in error for error in errors), errors)

    def test_current_contract_passes(self) -> None:
        self.assertEqual(checker.validate(self.qa, self.style), [])

    def test_rejects_release_qa_exposure(self) -> None:
        self.assertRejected(
            lambda qa, _: qa["runtime_contract"].__setitem__("disabled_in_release", False),
            "disabled in release",
        )

    def test_rejects_viewport_drift_from_style_contract(self) -> None:
        def mutate(qa, _):
            qa["viewports"][0]["width"] = 1279

        self.assertRejected(mutate, "drifts from config/visual-style.json")

    def test_rejects_state_route_mismatch(self) -> None:
        def mutate(qa, _):
            qa["states"][0]["route"] = "?qa=some_other_state"

        self.assertRejected(mutate, "route must be exactly")

    def test_rejects_unknown_viewport_reference(self) -> None:
        def mutate(qa, _):
            qa["states"][0]["default_viewports"] = ["not_a_viewport"]

        self.assertRejected(mutate, "references unknown viewport")

    def test_rejects_missing_exact_head_bridge_binding(self) -> None:
        def mutate(qa, _):
            qa["runtime_contract"]["required_bridge_fields"].remove("buildCommitSha")

        self.assertRejected(mutate, "exact build SHA")

    def test_rejects_missing_exact_head_failure_rule(self) -> None:
        def mutate(qa, _):
            qa["failure_policy"]["fail_capture_when"] = [
                item
                for item in qa["failure_policy"]["fail_capture_when"]
                if "buildCommitSha mismatch" not in item
            ]

        self.assertRejected(mutate, "reject exact-build SHA mismatch")

    def test_rejects_missing_evidence_artifact_failure_rule(self) -> None:
        def mutate(qa, _):
            qa["failure_policy"]["fail_capture_when"] = [
                item
                for item in qa["failure_policy"]["fail_capture_when"]
                if "required screenshot or motion artifact missing" not in item
            ]

        self.assertRejected(mutate, "reject missing evidence")

    def test_hud_must_cover_all_baseline_viewports(self) -> None:
        def mutate(qa, _):
            hud = next(state for state in qa["states"] if state["id"] == "hud_default")
            hud["default_viewports"].pop()

        self.assertRejected(mutate, "hud_default must cover every configured baseline viewport")


if __name__ == "__main__":
    unittest.main()
