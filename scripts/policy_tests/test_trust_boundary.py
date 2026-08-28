import json
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_trust_boundary as gate


def body(change_class="process", manifest="N/A — reason", milestone="none", doc="https://docs.github.com/"):
    return f"""## Problem / outcome

- Ticket: BB-X
- Change class: `{change_class}`
- Evidence manifest: {manifest}
- Milestone gate: {milestone}

## Decision status / provenance

## Research gate

### Official technical documentation

- Official doc 1: {doc}

If official-doc research is not applicable, explain why:

## Alternatives / BeBee decision

## Acceptance criteria

- [x] one
- [x] two

## Verification

## Visual QA

## Independent evaluation

## Human milestone gate

## License / provenance

## Known limitations / follow-ups
"""


class OfficialDocsTests(unittest.TestCase):
    def test_blank_na_cannot_consume_next_line(self):
        errors = gate.validate_official_docs(body(doc=""))
        self.assertTrue(errors)

    def test_same_line_na_is_valid(self):
        b = body(doc="").replace(
            "If official-doc research is not applicable, explain why:",
            "If official-doc research is not applicable, explain why: process-only change",
        )
        self.assertEqual(gate.validate_official_docs(b), [])


class ClassificationTests(unittest.TestCase):
    def test_flower_data_is_player_facing(self):
        errors = gate.validate(
            body=body(change_class="technical"),
            changed_files={"data/flowers.lua"},
        )
        self.assertTrue(any("player-facing content" in e for e in errors))

    def test_meadow_data_is_player_facing(self):
        errors = gate.validate(
            body=body(change_class="technical"),
            changed_files={"data/meadows.lua"},
        )
        self.assertTrue(any("player-facing content" in e for e in errors))

    def test_script_cannot_be_process(self):
        errors = gate.validate(
            body=body(change_class="process"),
            changed_files={"systems/foo.script"},
        )
        self.assertTrue(any(".lua/.script" in e for e in errors))

    def test_milestone_is_informational_not_human_blocked(self):
        errors = gate.validate(
            body=body(milestone="P2"),
            changed_files=set(),
        )
        self.assertFalse(any("human approval" in e.lower() for e in errors))


class ReferenceIdentityTests(unittest.TestCase):
    def test_different_urls_same_product_fail(self):
        data = {
            "research": {
                "candidate_pool": [
                    {"product_id": "same", "source": "https://example.com/a"},
                    {"product_id": "same", "source": "https://example.com/b"},
                ],
                "selected_references": [],
            }
        }
        errors = gate.validate_reference_identity(data)
        self.assertTrue(any("distinct product_id" in e for e in errors))


class GovernanceTests(unittest.TestCase):
    def test_governance_requires_same_pr_manifest(self):
        errors = gate.validate(
            body=body(),
            changed_files={"scripts/check_pr_evidence.py"},
        )
        self.assertTrue(any("same PR" in e for e in errors))

    def test_governance_object_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path.cwd()
            try:
                import os
                os.chdir(tmp)
                p = Path("evidence/BB-X/manifest.json")
                p.parent.mkdir(parents=True)
                p.write_text(json.dumps({}), encoding="utf-8")
                errors = gate.validate(
                    body=body(manifest="evidence/BB-X/manifest.json"),
                    changed_files={"scripts/check_pr_evidence.py", "evidence/BB-X/manifest.json"},
                )
            finally:
                os.chdir(old)
        self.assertTrue(any("governance object" in e for e in errors))

    def test_governance_manifest_does_not_require_second_human(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path.cwd()
            try:
                import os
                os.chdir(tmp)
                p = Path("evidence/BB-X/manifest.json")
                p.parent.mkdir(parents=True)
                p.write_text(
                    json.dumps({
                        "governance": {
                            "trust_boundary_change": "change",
                            "bypass_analysis": "analysis",
                            "rollback": "rollback",
                        }
                    }),
                    encoding="utf-8",
                )
                errors = gate.validate(
                    body=body(manifest="evidence/BB-X/manifest.json"),
                    changed_files={"scripts/check_pr_evidence.py", "evidence/BB-X/manifest.json"},
                )
            finally:
                os.chdir(old)
        self.assertFalse(any("human" in e.lower() for e in errors))


if __name__ == "__main__":
    unittest.main()
