import unittest
from pathlib import Path

import simulate
import upgrade_set_analysis


HERE = Path(__file__).resolve().parent
CONFIG = simulate.load_config(HERE / "first_region_candidate.json")


class UpgradeSetAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = upgrade_set_analysis.build_report(CONFIG)

    def test_no_yield_all_purchase_priorities_progress(self):
        exhaustive = self.report["no_yield_exhaustive_purchase_priorities"]
        self.assertEqual(exhaustive["orders_tested"], 5040)
        self.assertEqual(exhaustive["passed"], 5040)
        self.assertEqual(exhaustive["failed"], 0)
        self.assertEqual(exhaustive["minimum_final_balance"], 271)
        self.assertEqual(exhaustive["total_replay_actions"], 0)

    def test_selected_upgrade_set_is_intentionally_two_tracks(self):
        decision = self.report["decision_candidate"]
        self.assertEqual(decision["selected_upgrade_tracks"], ["flight", "buzz"])
        self.assertEqual(decision["excluded_vertical_slice_tracks"], ["yield"])
        self.assertEqual(self.report["hard_failures"], [])

    def test_yield_candidate_is_timing_sensitive_and_late_payback(self):
        comparison = self.report["yield_candidate_comparison"]
        self.assertEqual(comparison["break_even_after_availability"], "M06")
        self.assertEqual(comparison["no_yield_final_balance"], 382)
        self.assertEqual(comparison["yield_early_net_advantage"], 11)
        self.assertEqual(comparison["yield_mid_net_advantage"], -1)
        self.assertEqual(comparison["yield_late_net_advantage"], -15)

    def test_without_yield_removes_income_multiplier_purchase(self):
        no_yield = upgrade_set_analysis.without_yield(CONFIG)
        self.assertFalse(any(item.get("kind") == "yield" for item in no_yield["purchases"]))
        self.assertEqual(len(no_yield["purchases"]), 7)


if __name__ == "__main__":
    unittest.main()
