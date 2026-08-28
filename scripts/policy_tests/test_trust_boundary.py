import json
import os
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
            head_sha="head",
            pr_author="author",
        )
        self.assertTrue(any("player-facing content" in e for e in errors))

    def test_meadow_data_is_player_facing(self):
        errors = gate.validate(
            body=body(change_class="technical"),
            changed_files={"data/meadows.lua"},
            head_sha="head",
            pr_author="author",
        )
        self.assertTrue(any("player-facing content" in e for e in errors))

    def test_script_cannot_be_process(self):
        errors = gate.validate(
            body=body(change_class="process"),
            changed_files={"systems/foo.script"},
            head_sha="head",
            pr_author="author",
        )
        self.assertTrue(any(".lua/.script" in e for e in errors))


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


class HumanApprovalTests(unittest.TestCase):
    def setUp(self):
        self.old = {
            "PR_REVIEWS_FILE": os.environ.get("PR_REVIEWS_FILE"),
            "ENFORCE_INDEPENDENT_HUMAN_REVIEW": os.environ.get("ENFORCE_INDEPENDENT_HUMAN_REVIEW"),
        }
        os.environ["ENFORCE_INDEPENDENT_HUMAN_REVIEW"] = "1"

    def tearDown(self):
        for key, value in self.old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def _reviews(self, reviews):
        f = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
        json.dump(reviews, f)
        f.close()
        os.environ["PR_REVIEWS_FILE"] = f.name

    def test_milestone_requires_exact_head_non_author_review(self):
        self._reviews([])
        errors = gate.validate(
            body=body(milestone="P2"),
            changed_files=set(),
            head_sha="head",
            pr_author="author",
        )
        self.assertTrue(any("Independent human approval" in e for e in errors))

    def test_old_review_does_not_count(self):
        self._reviews([{
            "state": "APPROVED",
            "commit_id": "old",
            "user": {"login": "reviewer", "type": "User"},
        }])
        errors = gate.validate(
            body=body(milestone="P4"),
            changed_files=set(),
            head_sha="head",
            pr_author="author",
        )
        self.assertTrue(any("Independent human approval" in e for e in errors))

    def test_exact_head_other_user_counts(self):
        self._reviews([{
            "state": "APPROVED",
            "commit_id": "head",
            "user": {"login": "reviewer", "type": "User"},
        }])
        errors = gate.validate(
            body=body(milestone="P6"),
            changed_files=set(),
            head_sha="head",
            pr_author="author",
        )
        self.assertFalse(any("Independent human approval" in e for e in errors))


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.old_enforce = os.environ.get("ENFORCE_INDEPENDENT_HUMAN_REVIEW")
        os.environ["ENFORCE_INDEPENDENT_HUMAN_REVIEW"] = "0"

    def tearDown(self):
        if self.old_enforce is None:
            os.environ.pop("ENFORCE_INDEPENDENT_HUMAN_REVIEW", None)
        else:
            os.environ["ENFORCE_INDEPENDENT_HUMAN_REVIEW"] = self.old_enforce

    def test_governance_requires_same_pr_manifest(self):
        errors = gate.validate(
            body=body(),
            changed_files={"scripts/check_pr_evidence.py"},
            head_sha="head",
            pr_author="author",
        )
        self.assertTrue(any("same PR" in e for e in errors))

    def test_governance_object_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path.cwd()
            try:
                os.chdir(tmp)
                p = Path("evidence/BB-X/manifest.json")
                p.parent.mkdir(parents=True)
                p.write_text(json.dumps({}), encoding="utf-8")
                errors = gate.validate(
                    body=body(manifest="evidence/BB-X/manifest.json"),
                    changed_files={"scripts/check_pr_evidence.py", "evidence/BB-X/manifest.json"},
                    head_sha="head",
                    pr_author="author",
                )
            finally:
                os.chdir(old)
        self.assertTrue(any("governance object" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
