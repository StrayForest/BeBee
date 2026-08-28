#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from copy import deepcopy
from pathlib import Path

import simulate


def without_yield(config: dict) -> dict:
    result = deepcopy(config)
    result["purchases"] = [item for item in result["purchases"] if item.get("kind") != "yield"]
    return result


def exhaustive_purchase_priorities(config: dict) -> dict:
    ids = [item["id"] for item in config["purchases"]]
    failures: list[dict] = []
    balances: list[int] = []
    replay_actions = 0

    for order in itertools.permutations(ids):
        result = simulate.simulate_strategy(config, "all_purchase_priorities", order)
        replay_actions += result["replay_actions"]
        if result["passed"] and result["balance"] >= 0 and result["replay_actions"] == 0:
            balances.append(result["balance"])
        else:
            failures.append({
                "order": list(order),
                "passed": result["passed"],
                "failed_gate": result["failed_gate"],
                "balance": result["balance"],
                "replay_actions": result["replay_actions"],
                "purchases": result["purchases"],
                "pending_desired": result["pending_desired"],
            })

    orders_tested = 1
    for number in range(2, len(ids) + 1):
        orders_tested *= number

    return {
        "purchase_ids": ids,
        "orders_tested": orders_tested,
        "passed": orders_tested - len(failures),
        "failed": len(failures),
        "minimum_final_balance": min(balances, default=None),
        "maximum_final_balance": max(balances, default=None),
        "total_replay_actions": replay_actions,
        "failures": failures[:20],
    }


def build_report(config: dict) -> dict:
    historical = simulate.build_report(config)
    no_yield = without_yield(config)
    exhaustive = exhaustive_purchase_priorities(no_yield)

    no_yield_baseline = historical["strategies"]["no_yield"]
    yield_early = historical["strategies"]["yield_early"]
    yield_mid = historical["strategies"]["yield_mid"]
    yield_late = historical["strategies"]["yield_late"]
    payback = historical["yield_payback"]

    yield_comparison = {
        "candidate_cost": payback["cost"],
        "candidate_multiplier": 1.15,
        "break_even_after_availability": payback["break_even_after_availability"],
        "future_base_honey_to_break_even": payback["future_base_honey_to_break_even"],
        "future_base_honey_after_availability": payback["future_base_honey_after_availability"],
        "no_yield_final_balance": no_yield_baseline["balance"],
        "yield_early_final_balance": yield_early["balance"],
        "yield_mid_final_balance": yield_mid["balance"],
        "yield_late_final_balance": yield_late["balance"],
        "yield_early_net_advantage": yield_early["balance"] - no_yield_baseline["balance"],
        "yield_mid_net_advantage": yield_mid["balance"] - no_yield_baseline["balance"],
        "yield_late_net_advantage": yield_late["balance"] - no_yield_baseline["balance"],
        "sensitivity": historical["yield_sensitivity"],
    }

    hard_assertions = {
        "flight_buzz_seed_orders_all_progress": exhaustive["failed"] == 0,
        "flight_buzz_seed_orders_need_no_replay": exhaustive["total_replay_actions"] == 0,
        "flight_buzz_seed_orders_stay_non_negative": exhaustive["minimum_final_balance"] is not None and exhaustive["minimum_final_balance"] >= 0,
        "yield_is_not_required_for_region_completion": no_yield_baseline["passed"] and no_yield_baseline["replay_actions"] == 0,
        "yield_candidate_breaks_even_only_at_or_after_m06": payback["break_even_after_availability"] in {"M06", "REGION_COMPLETE", None},
    }
    hard_failures = [name for name, passed in hard_assertions.items() if not passed]

    return {
        "decision_candidate": {
            "selected_upgrade_tracks": ["flight", "buzz"],
            "excluded_vertical_slice_tracks": ["yield"],
            "selection": "flight_buzz_only",
            "reason": "Flight and Buzz change the bee's direct play capability. Yield is not required for no-grind progression, its tested 1.15x form only repays at M06, and its outcome flips materially with purchase timing/multiplier tuning. The vertical slice therefore stays intentionally smaller instead of preserving a third card for symmetry.",
        },
        "no_yield_exhaustive_purchase_priorities": exhaustive,
        "yield_candidate_comparison": yield_comparison,
        "hard_assertions": hard_assertions,
        "hard_failures": hard_failures,
        "scope": {
            "validated": [
                "Flight and Buzz are the vertical-slice upgrade tracks.",
                "Yield is excluded from the vertical slice unless reopened by new evidence.",
                "The current first-region candidate is arithmetically no-grind across all 5040 full purchase-priority orders after removing Yield.",
            ],
            "not_validated": [
                "Exact Honey rewards/costs.",
                "Real-time minutes between purchases.",
                "Final Flight/Buzz effect curves.",
                "Human preference for upgrade cadence.",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", default="tools/economy/first_region_candidate.json")
    parser.add_argument("--output")
    args = parser.parse_args()

    config = simulate.load_config(Path(args.config))
    report = build_report(config)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 1 if report["hard_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
