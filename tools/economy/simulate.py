#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class State:
    honey: int
    earned: int = 0
    spent: int = 0
    buzz: int = 1
    flight: int = 1
    yield_multiplier: float = 1.0
    purchases: list[str] = field(default_factory=list)
    events: list[dict] = field(default_factory=list)
    replay_actions: int = 0
    completed_milestones: list[str] = field(default_factory=list)


class SimulationError(RuntimeError):
    pass


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise SimulationError("schema_version must be 1")
    return data


def purchase_map(config: dict) -> dict[str, dict]:
    return {item["id"]: item for item in config["purchases"]}


def can_purchase(item: dict, state: State) -> bool:
    parent = item.get("requires_purchase")
    if parent is not None and parent not in state.purchases:
        return False
    available_after = item.get("available_after")
    return available_after is None or available_after in state.completed_milestones


def apply_purchase(item: dict, state: State) -> bool:
    if item["id"] in state.purchases or not can_purchase(item, state):
        return False
    if state.honey < item["cost"]:
        return False

    state.honey -= item["cost"]
    state.spent += item["cost"]
    state.purchases.append(item["id"])
    if item["kind"] == "buzz":
        state.buzz = max(state.buzz, item["level"])
    elif item["kind"] == "flight":
        state.flight = max(state.flight, item["level"])
    elif item["kind"] == "yield":
        state.yield_multiplier = max(state.yield_multiplier, item["reward_multiplier"])
    state.events.append({
        "type": "purchase",
        "id": item["id"],
        "cost": item["cost"],
        "balance": state.honey,
    })
    return True


def earn_milestone(milestone: dict, state: State) -> None:
    if state.buzz < milestone["requires_buzz"]:
        raise SimulationError(
            f"gate {milestone['id']} requires Buzz {milestone['requires_buzz']}, has {state.buzz}"
        )
    reward = round(milestone["base_honey"] * state.yield_multiplier)
    state.honey += reward
    state.earned += reward
    state.completed_milestones.append(milestone["id"])
    state.events.append({
        "type": "reward",
        "id": milestone["id"],
        "base_honey": milestone["base_honey"],
        "multiplier": state.yield_multiplier,
        "reward": reward,
        "balance": state.honey,
    })


def required_purchase_for(milestone: dict, purchases: dict[str, dict], state: State) -> list[dict]:
    target = milestone["requires_buzz"]
    result: list[dict] = []
    for level in range(state.buzz + 1, target + 1):
        item = next(
            (p for p in purchases.values() if p["kind"] == "buzz" and p.get("level") == level),
            None,
        )
        if item is None:
            raise SimulationError(f"no Buzz purchase available for required level {level}")
        result.append(item)
    return result


def force_required_progression(milestone: dict, purchases: dict[str, dict], state: State) -> bool:
    for item in required_purchase_for(milestone, purchases, state):
        if not apply_purchase(item, state):
            return False
    return True


def simulate_strategy(
    config: dict,
    name: str,
    desired_order: Iterable[str],
    not_before: dict[str, str] | None = None,
) -> dict:
    purchases = purchase_map(config)
    state = State(honey=config.get("starting_honey", 0))
    desired = list(desired_order)
    not_before = not_before or {}
    cursor = 0
    failed_gate = None

    for milestone in config["milestones"]:
        made_purchase = True
        while made_purchase:
            made_purchase = False
            for index in range(cursor, len(desired)):
                item = purchases[desired[index]]
                strategy_gate = not_before.get(item["id"])
                strategy_ready = strategy_gate is None or strategy_gate in state.completed_milestones
                if strategy_ready and can_purchase(item, state) and state.honey >= item["cost"]:
                    apply_purchase(item, state)
                    desired[cursor], desired[index] = desired[index], desired[cursor]
                    cursor += 1
                    made_purchase = True
                    break

        if state.buzz < milestone["requires_buzz"]:
            if not force_required_progression(milestone, purchases, state):
                failed_gate = milestone["id"]
                break

        earn_milestone(milestone, state)

    made_purchase = True
    while failed_gate is None and cursor < len(desired) and made_purchase:
        made_purchase = False
        for index in range(cursor, len(desired)):
            item = purchases[desired[index]]
            strategy_gate = not_before.get(item["id"])
            strategy_ready = strategy_gate is None or strategy_gate in state.completed_milestones
            if strategy_ready and can_purchase(item, state) and state.honey >= item["cost"]:
                apply_purchase(item, state)
                desired[cursor], desired[index] = desired[index], desired[cursor]
                cursor += 1
                made_purchase = True
                break

    return {
        "name": name,
        "passed": failed_gate is None,
        "failed_gate": failed_gate,
        "earned": state.earned,
        "spent": state.spent,
        "balance": state.honey,
        "buzz": state.buzz,
        "flight": state.flight,
        "yield_multiplier": state.yield_multiplier,
        "purchases": state.purchases,
        "pending_desired": desired[cursor:],
        "replay_actions": state.replay_actions,
        "events": state.events,
    }


def yield_payback(config: dict, purchase_id: str = "yield_2") -> dict:
    purchases = purchase_map(config)
    item = purchases[purchase_id]
    delta = item["reward_multiplier"] - 1.0
    base_needed = None if delta <= 0 else item["cost"] / delta
    available_after = item.get("available_after")
    available_seen = available_after is None
    cumulative = 0
    break_even_at = None
    for milestone in config["milestones"]:
        if available_seen:
            cumulative += milestone["base_honey"]
            if base_needed is not None and cumulative >= base_needed and break_even_at is None:
                break_even_at = milestone["id"]
        if milestone["id"] == available_after:
            available_seen = True
    return {
        "purchase_id": purchase_id,
        "cost": item["cost"],
        "available_after": available_after,
        "incremental_multiplier": round(delta, 4),
        "future_base_honey_to_break_even": None if base_needed is None else round(base_needed, 2),
        "break_even_after_availability": break_even_at,
        "future_base_honey_after_availability": cumulative,
        "total_region_base_honey": sum(m["base_honey"] for m in config["milestones"]),
    }


def yield_sensitivity(config: dict, multipliers=(1.10, 1.15, 1.20)) -> list[dict]:
    rows = []
    for multiplier in multipliers:
        cloned = json.loads(json.dumps(config))
        for item in cloned["purchases"]:
            if item["id"] == "yield_2":
                item["reward_multiplier"] = multiplier
        payback = yield_payback(cloned)
        early = simulate_strategy(
            cloned,
            f"yield_{multiplier}",
            ["yield_2", "buzz_2", "flight_2", "buzz_3"],
        )
        rows.append({
            "multiplier": multiplier,
            "final_balance": early["balance"],
            "payback": payback,
        })
    return rows


def named_strategies() -> dict[str, dict]:
    return {
        "minimal_progression": {"order": ["buzz_2", "buzz_3"]},
        "buzz_first": {"order": ["buzz_2", "buzz_3", "flight_2", "flight_3"]},
        "flight_first": {"order": ["flight_2", "buzz_2", "flight_3", "buzz_3"]},
        "balanced": {"order": ["buzz_2", "flight_2", "buzz_3", "seed_daisy", "flight_3"]},
        "customization_heavy": {"order": ["seed_daisy", "seed_clover", "seed_lavender", "buzz_2", "flight_2", "buzz_3"]},
        "poor_but_valid": {"order": ["seed_daisy", "flight_2", "seed_clover", "yield_2", "flight_3", "buzz_2", "seed_lavender", "buzz_3"]},
        "no_yield": {"order": ["buzz_2", "flight_2", "buzz_3"]},
        "yield_early": {"order": ["yield_2", "buzz_2", "flight_2", "buzz_3"], "not_before": {"yield_2": "M03"}},
        "yield_mid": {"order": ["buzz_2", "flight_2", "yield_2", "buzz_3"], "not_before": {"yield_2": "M04"}},
        "yield_late": {"order": ["buzz_2", "flight_2", "buzz_3", "yield_2"], "not_before": {"yield_2": "M05"}},
    }


def exhaustive_orders(config: dict) -> dict:
    ids = ["buzz_2", "buzz_3", "flight_2", "flight_3", "yield_2"]
    results = []
    for order in itertools.permutations(ids):
        result = simulate_strategy(config, "exhaustive", order)
        results.append({
            "order": list(order),
            "passed": result["passed"],
            "failed_gate": result["failed_gate"],
            "balance": result["balance"],
            "purchases": result["purchases"],
            "pending_desired": result["pending_desired"],
        })
    passed = [row for row in results if row["passed"]]
    failed = [row for row in results if not row["passed"]]
    return {
        "orders_tested": len(results),
        "passed": len(passed),
        "failed": len(failed),
        "minimum_final_balance": min((row["balance"] for row in passed), default=None),
        "failures": failed[:20],
    }


def build_report(config: dict) -> dict:
    strategies = {
        name: simulate_strategy(config, name, spec["order"], spec.get("not_before"))
        for name, spec in named_strategies().items()
    }
    exhaustive = exhaustive_orders(config)
    hard_failures = [
        name for name, result in strategies.items()
        if not result["passed"] or result["balance"] < 0 or result["replay_actions"] > 0
    ]
    if exhaustive["failed"]:
        hard_failures.append("exhaustive_upgrade_orders")
    customization = strategies["customization_heavy"]
    return {
        "candidate_status": config.get("status"),
        "strategies": strategies,
        "exhaustive_upgrade_orders": exhaustive,
        "yield_payback": yield_payback(config),
        "yield_sensitivity": yield_sensitivity(config),
        "hard_assertions": {
            "named_paths_no_negative_balance": all(r["balance"] >= 0 for r in strategies.values()),
            "named_paths_no_replay": all(r["replay_actions"] == 0 for r in strategies.values()),
            "named_paths_pass_required_gates": all(r["passed"] for r in strategies.values()),
            "customization_heavy_passes": customization["passed"],
            "all_exhaustive_upgrade_priorities_progress": exhaustive["failed"] == 0,
        },
        "hard_failures": hard_failures,
        "interpretation": [
            "Numbers remain HYPOTHESIS until seed flow and pollination pacing are validated.",
            "A passing arithmetic path does not prove a fun pacing curve.",
            "Yield dominance must be reviewed using payback plus playtest opportunity cost, not balance alone.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", default="tools/economy/first_region_candidate.json")
    parser.add_argument("--output")
    args = parser.parse_args()
    config = load_config(Path(args.config))
    report = build_report(config)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 1 if report["hard_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
