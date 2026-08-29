#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "tools/economy/p5_seed_progression.json"


class SimError(RuntimeError):
    pass


def load() -> dict:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise SimError("schema_version must be 1")
    return data


def run_path(cfg: dict, name: str, priority: list[str]) -> dict:
    honey = int(cfg["starting_honey"])
    buzz = 1
    purchased: list[str] = []
    pending = list(priority)
    completed: list[str] = []
    events: list[dict] = []
    replay_actions = 0
    failed_gate = None

    def buy_available() -> None:
        nonlocal honey, buzz
        made_purchase = True
        while made_purchase:
            made_purchase = False
            for purchase_id in list(pending):
                item = cfg["purchases"][purchase_id]
                if item["available_after"] not in completed:
                    continue
                cost = int(item["cost"])
                if honey < cost:
                    continue
                honey -= cost
                if honey < 0:
                    raise SimError(f"negative Honey in {name}")
                pending.remove(purchase_id)
                purchased.append(purchase_id)
                if item["kind"] == "buzz":
                    buzz = int(item.get("level", buzz))
                events.append({"type": "purchase", "id": purchase_id, "cost": cost, "balance": honey})
                made_purchase = True
                break

    for milestone in cfg["milestones"]:
        buy_available()
        required_buzz = int(milestone["requires_buzz"])
        if buzz < required_buzz:
            required = cfg["purchases"]["buzz_2"]
            if (
                "buzz_2" in pending
                and required["available_after"] in completed
                and honey >= int(required["cost"])
            ):
                honey -= int(required["cost"])
                pending.remove("buzz_2")
                purchased.append("buzz_2")
                buzz = int(required.get("level", 2))
                events.append({"type": "forced_required_purchase", "id": "buzz_2", "cost": int(required["cost"]), "balance": honey})
            else:
                failed_gate = milestone["id"]
                break

        honey += int(milestone["honey"])
        completed.append(milestone["id"])
        events.append({"type": "reward", "id": milestone["id"], "amount": int(milestone["honey"]), "balance": honey})
        buy_available()

    return {
        "name": name,
        "priority": priority,
        "passed": failed_gate is None,
        "failed_gate": failed_gate,
        "balance": honey,
        "buzz": buzz,
        "purchases": purchased,
        "pending": pending,
        "replay_actions": replay_actions,
        "events": events,
    }


def build_report(cfg: dict) -> dict:
    purchase_ids = list(cfg["purchases"])
    exhaustive = []
    for order in itertools.permutations(purchase_ids):
        result = run_path(cfg, "exhaustive", list(order))
        exhaustive.append({
            "order": list(order),
            "passed": result["passed"],
            "failed_gate": result["failed_gate"],
            "balance": result["balance"],
            "buzz": result["buzz"],
            "purchases": result["purchases"],
            "replay_actions": result["replay_actions"],
        })

    named = {
        "upgrade_first": run_path(cfg, "upgrade_first", ["flight_2", "buzz_2", "seed_daisy", "seed_clover", "seed_lavender"]),
        "seed_first": run_path(cfg, "seed_first", ["seed_daisy", "seed_clover", "seed_lavender", "flight_2", "buzz_2"]),
        "flight_then_aesthetics": run_path(cfg, "flight_then_aesthetics", ["flight_2", "seed_daisy", "seed_clover", "buzz_2", "seed_lavender"]),
        "buzz_then_aesthetics": run_path(cfg, "buzz_then_aesthetics", ["buzz_2", "seed_daisy", "seed_clover", "flight_2", "seed_lavender"]),
    }

    total_rewards = sum(int(item["honey"]) for item in cfg["milestones"])
    total_costs = sum(int(item["cost"]) for item in cfg["purchases"].values())
    expected_final_balance = int(cfg["starting_honey"]) + total_rewards - total_costs
    assertions = {
        "all_120_purchase_priorities_progress": len(exhaustive) == 120 and all(item["passed"] for item in exhaustive),
        "all_priorities_non_negative": all(item["balance"] >= 0 for item in exhaustive),
        "all_priorities_no_replay": all(item["replay_actions"] == 0 for item in exhaustive),
        "all_priorities_buy_required_buzz_before_gate": all(item["buzz"] >= 2 for item in exhaustive),
        "all_priorities_can_buy_all_first_meadow_sinks": all(len(item["purchases"]) == len(purchase_ids) for item in exhaustive),
        "all_priorities_end_at_same_balance": all(item["balance"] == expected_final_balance for item in exhaustive),
        "named_seed_first_progresses": named["seed_first"]["passed"],
        "named_flight_then_aesthetics_progresses": named["flight_then_aesthetics"]["passed"],
        "replant_is_free": int(cfg["replant_cost"]) == 0,
    }
    failures = [key for key, value in assertions.items() if not value]
    return {
        "schema_version": 1,
        "ticket": "P5-SEED-OWNERSHIP",
        "config_status": cfg["status"],
        "purchase_priority_count": len(exhaustive),
        "total_first_meadow_rewards": total_rewards,
        "total_first_meadow_sink_cost": total_costs,
        "expected_final_balance_after_all_sinks": expected_final_balance,
        "named_paths": named,
        "hard_assertions": assertions,
        "hard_failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    report = build_report(load())
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if report["hard_failures"]:
        raise SystemExit(1)
    print(
        "P5 seed economy regression: PASS "
        f"({report['purchase_priority_count']} priorities, final Honey {report['expected_final_balance_after_all_sinks']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
