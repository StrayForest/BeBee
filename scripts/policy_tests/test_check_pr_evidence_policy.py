import json
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_pr_evidence_policy as policy


def pr_body(change_class: str, manifest: str = "N/A — test") -> str:
    return f"""## Problem / outcome

- Ticket: BB-T001
- Change class: `{change_class}`
- Evidence manifest: {manifest}

## Decision status / provenance

## Research gate

## Alternatives / BeBee decision

## Acceptance criteria

- [x] criterion one
- [x] criterion two

## Verification
"""


def manifest_payload(change_class: str, head_sha: str = "head") -> dict:
    return {
        "schema_version": 1,
        "ticket": "BB-T001",
        "change_class": change_class,
        "problem": "Observable problem.",
        "decision": {
            "status_before": "HYPOTHESIS",
            "status_after": "VALIDATED",
            "provenance_type": "TECH_CONSTRAINT",
            "evidence_strength": "MEDIUM",
            "selected_alternative": "b",
            "rationale": "Evidence-backed rationale.",
        },
        "research": {
            "candidate_pool": [
                {"name": f"Game {i}", "source": f"https://example.com/{i}", "relevance": "relevant"}
                for i in range(5)
            ],
            "candidate_pool_exception": "",
            "selected_references": [
                {
                    "name": "A",
                    "source": "https://example.com/a",
                    "platform_version_date": "web / 2026-08-28",
                    "selection_reason": "same problem",
                    "observed_behavior": "observed",
                    "inference": "inference",
                    "measurements": {},
                },
                {
                    "name": "B",
                    "source": "https://example.com/b",
                    "platform_version_date": "web / 2026-08-28",
                    "selection_reason": "different solution",
                    "observed_behavior": "observed",
                    "inference": "inference",
                    "measurements": {},
                },
            ],
            "reference_exception": "",
            "anti_pattern": {
                "source": "https://example.com/anti",
                "observation": "different pattern",
                "lesson": "test rather than assume",
            },
        },
        "official_docs": [
            {
                "source": "https://defold.com/manuals/input/",
                "date_checked": "2026-08-28",
                "verified_constraint": "Verified current behavior.",
            }
        ],
        "official_docs_exception": "",
        "alternatives": [
            {"id": "a", "disposition": "rejected", "reason": "worse"},
            {"id": "b", "disposition": "selected", "reason": "better"},
        ],
        "acceptance_criteria": [
            {"criterion": "one", "status": "pass", "evidence": "test"},
            {"criterion": "two", "status": "pass", "evidence": "test"},
        ],
        "verification": {
            "automated": ["python tests"],
            "manual": [],
            "runtime_errors": "none",
            "save_data_impact": "none",
        },
        "visual_evidence": {
            "required": True,
            "artifacts": ["capture"],
            "states": ["idle"],
            "viewports": ["1440x900"],
            "provenance": {
                "capture_commit_sha": head_sha,
                "capture_mode": "ci",
                "artifact_locator": "actions-artifact:visual-qa",
            },
        },
        "comparison": {"measurements": {"actions_to_result": 1}},
        "evaluation": {
            "mode": "independent_pass",
            "findings": ["none"],
            "verdict": "PASS",
            "iteration_required": False,
            "provenance": {
                "evaluated_sha": head_sha,
                "evaluator_id": "review-agent",
                "implementation_author_id": "implementation-agent",
                "input_artifacts": ["actions-artifact:visual-qa"],
                "record_locator": "actions-artifact:evaluation",
            },
        },
    }


class DiffClassificationTests(unittest.TestCase):
    def test_player_facing_diff_cannot_claim_technical(self):
        errors = policy.validate_change_class("technical", {"ui/hud.gui"})
        self.assertTrue(any("player-facing" in error for error in errors))

    def test_economy_diff_must_claim_economy(self):
        errors = policy.validate_change_class("player-facing", {"data/economy.lua"})
        self.assertTrue(any("must be `economy`" in error for error in errors))

    def test_runtime_diff_cannot_claim_trivial(self):
        errors = policy.validate_change_class("trivial", {"gameplay/bee/bee.lua"})
        self.assertTrue(errors)

    def test_docs_only_can_be_process(self):
        self.assertEqual(
            policy.validate_change_class("process", {"docs/15-agent-evidence-governance.md"}),
            [],
        )

    def test_app_bootstrap_runtime_can_be_technical(self):
        changed = {"game.project", "app/bootstrap.collection", "app/bootstrap.script"}
        required = policy.required_policy(changed)
        self.assertTrue(required["high_risk_technical"])
        self.assertFalse(required["player"])
        self.assertEqual(policy.validate_change_class("technical", changed), [])


class AcceptanceTests(unittest.TestCase):
    def test_unchecked_acceptance_fails(self):
        body = pr_body("process").replace("- [x] criterion two", "- [ ] criterion two")
        errors = policy.validate_acceptance_checkboxes(body, "process")
        self.assertTrue(any("unchecked" in error.lower() for error in errors))


class ReferenceTests(unittest.TestCase):
    def test_duplicate_candidate_urls_fail(self):
        data = manifest_payload("player-facing")
        data["research"]["candidate_pool"][4]["source"] = data["research"]["candidate_pool"][0]["source"]
        errors = policy.validate_unique_references(data)
        self.assertTrue(any("duplicate" in error.lower() for error in errors))

    def test_duplicate_selected_urls_fail(self):
        data = manifest_payload("player-facing")
        data["research"]["selected_references"][1]["source"] = data["research"]["selected_references"][0]["source"]
        errors = policy.validate_unique_references(data)
        self.assertTrue(any("distinct" in error.lower() for error in errors))


class ProvenanceTests(unittest.TestCase):
    def test_fake_capture_sha_fails(self):
        data = manifest_payload("player-facing", head_sha="wrong")
        errors = policy.validate_visual_and_evaluation_provenance(data, "actual")
        self.assertTrue(any("capture_commit_sha" in error for error in errors))

    def test_pr_head_binding_is_accepted(self):
        data = manifest_payload("player-facing", head_sha=policy.PR_HEAD_BINDING)
        errors = policy.validate_visual_and_evaluation_provenance(data, "actual")
        self.assertEqual(errors, [])

    def test_same_implementer_and_evaluator_fails(self):
        data = manifest_payload("player-facing")
        data["evaluation"]["provenance"]["evaluator_id"] = "same"
        data["evaluation"]["provenance"]["implementation_author_id"] = "same"
        errors = policy.validate_visual_and_evaluation_provenance(data, "head")
        self.assertTrue(any("must differ" in error for error in errors))


class HighRiskTechnicalTests(unittest.TestCase):
    def test_high_risk_technical_requires_manifest(self):
        body = pr_body("technical", "N/A — no manifest")
        errors = policy.validate_policy(
            body=body,
            changed_files={"systems/storage.lua"},
            base_sha="base",
            head_sha="head",
        )
        self.assertTrue(any("High-risk technical diff requires" in error for error in errors))

    def test_valid_high_risk_technical_manifest_passes_policy_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manifest_path = tmp_path / "evidence" / "BB-T001" / "manifest.json"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(manifest_payload("technical")),
                encoding="utf-8",
            )

            body = pr_body("technical", "evidence/BB-T001/manifest.json")
            old_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)
                errors = policy.validate_policy(
                    body=body,
                    changed_files={
                        "systems/storage.lua",
                        "evidence/BB-T001/manifest.json",
                    },
                    base_sha="base",
                    head_sha="head",
                )
            finally:
                os.chdir(old_cwd)

            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
