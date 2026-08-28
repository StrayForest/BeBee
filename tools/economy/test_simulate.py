import json
import unittest
from pathlib import Path

import simulate


HERE = Path(__file__).resolve().parent
CONFIG = simulate.load_config(HERE / "first_region_candidate.json")


class EconomySimulationTests(unittest.TestCase):
    def test_named_strategies_pass_without_replay(self):
        report = simulate.build_report(CONFIG)
        self.assertEqual(report["hard_failures"], [])
        self.assertTrue(report["hard_assertions"]["named_paths_pass_required_gates"])
        self.assertTrue(report["hard_assertions"]["named_paths_no_replay"])

    def test_exhaustive_upgrade_order_count(self):
        report = simulate.exhaustive_orders(CONFIG)
        self.assertEqual(report["orders_tested"], 120)
        self.assertEqual(report["failed"], 0)

    def test_yield_payback_is_explicit(self):
        result = simulate.yield_payback(CONFIG)
        self.assertEqual(result["future_base_honey_to_break_even"], 266.67)
        self.assertEqual(result["break_even_after_availability"], "M06")

    def test_gate_failure_when_required_buzz_is_unaffordable(self):
        broken = json.loads(json.dumps(CONFIG))
        for purchase in broken["purchases"]:
            if purchase["id"] == "buzz_2":
                purchase["cost"] = 1000
        result = simulate.simulate_strategy(broken, "broken", [])
        self.assertFalse(result["passed"])
        self.assertEqual(result["failed_gate"], "M03")


if __name__ == "__main__":
    unittest.main()
