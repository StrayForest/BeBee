import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_pr_evidence_policy_v2 as policy_v2


class MixedClassificationTests(unittest.TestCase):
    def test_player_facing_wins_over_high_risk_when_both_are_present(self):
        files = {"gameplay/bee/movement.lua", "app/qa_runtime.lua"}
        self.assertEqual([], policy_v2.validate_change_class("player-facing", files))
        errors = policy_v2.validate_change_class("technical", files)
        self.assertTrue(any("player-facing" in error for error in errors))

    def test_pure_high_risk_runtime_remains_technical(self):
        files = {"app/qa_runtime.lua"}
        self.assertEqual([], policy_v2.validate_change_class("technical", files))
        errors = policy_v2.validate_change_class("player-facing", files)
        self.assertTrue(any("technical" in error for error in errors))

    def test_economy_keeps_highest_precedence(self):
        files = {"systems/economy/rewards.lua", "gameplay/bee/movement.lua", "app/qa_runtime.lua"}
        self.assertEqual([], policy_v2.validate_change_class("economy", files))
        errors = policy_v2.validate_change_class("player-facing", files)
        self.assertTrue(any("economy" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
