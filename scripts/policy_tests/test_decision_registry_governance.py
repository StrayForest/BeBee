import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_trust_boundary_v2 as policy_v2


def body(change_class: str = "player-facing") -> str:
    return f"""## Problem / outcome

- Ticket: BB-T002
- Change class: `{change_class}`
- Evidence manifest: `evidence/BB-T002/manifest.json`
- Milestone gate: `none`

## Research gate

### Official technical documentation
- Official doc 1: https://defold.com/manuals/input/
If official-doc research is not applicable, explain why: N/A — docs apply.

## Alternatives / BeBee decision
"""


VALID_MANIFEST = {
    "governance": {
        "trust_boundary_change": "Decision registry synchronized with the feature evidence.",
        "bypass_analysis": "No trusted policy or workflow changes.",
        "rollback": "Revert the feature decision and registry entry together.",
    },
    "research": {"candidate_pool": [], "selected_references": []},
}


class DecisionRegistryGovernanceTests(unittest.TestCase):
    def test_decisions_only_governance_touch_can_remain_player_facing(self):
        files = {"gameplay/bee/movement.lua", "DECISIONS.md", "evidence/BB-T002/manifest.json"}
        with patch.object(policy_v2.policy, "load_manifest", return_value=VALID_MANIFEST):
            errors = policy_v2.validate(body=body(), changed_files=files)
        self.assertNotIn(policy_v2.PROCESS_ONLY_ERROR, errors)
        self.assertEqual([], errors)

    def test_policy_authority_change_still_requires_process(self):
        files = {
            "gameplay/bee/movement.lua",
            "DECISIONS.md",
            ".github/workflows/pr-evidence-trusted.yml",
            "evidence/BB-T002/manifest.json",
        }
        with patch.object(policy_v2.policy, "load_manifest", return_value=VALID_MANIFEST):
            errors = policy_v2.validate(body=body(), changed_files=files)
        self.assertIn(policy_v2.PROCESS_ONLY_ERROR, errors)

    def test_decisions_update_still_requires_same_pr_manifest(self):
        files = {"gameplay/bee/movement.lua", "DECISIONS.md"}
        with patch.object(policy_v2.policy, "load_manifest", return_value=VALID_MANIFEST):
            errors = policy_v2.validate(body=body(), changed_files=files)
        self.assertTrue(any("manifest must be changed in the same PR" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
