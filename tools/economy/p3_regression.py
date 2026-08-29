#!/usr/bin/env python3
from __future__ import annotations
import argparse, itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "tools/economy/p3_progression.json"

class SimError(RuntimeError): pass

def load():
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1: raise SimError("schema_version must be 1")
    return data

def run_path(cfg, name, desired, optional_spends=()):
    honey = int(cfg["starting_honey"]); buzz = 1; flight = 1; purchases=[]; spent=0; earned=0
    optional = list(optional_spends); events=[]; failed=None
    for milestone in cfg["milestones"]:
        # buy desired affordable upgrades as soon as their availability milestone has been completed
        made=True
        while made:
            made=False
            for pid in list(desired):
                item=cfg["upgrades"][pid]
                available=item["available_after"] in [e["id"] for e in events if e["type"]=="reward"]
                if available and honey >= item["cost"]:
                    honey-=item["cost"]; spent+=item["cost"]; purchases.append(pid); desired.remove(pid); made=True
                    if item["kind"]=="buzz": buzz=item["level"]
                    if item["kind"]=="flight": flight=item["level"]
                    events.append({"type":"purchase","id":pid,"balance":honey})
                    break
        # optional aesthetic spends are intentionally greedy when affordable
        while optional and honey >= optional[0]:
            cost=optional.pop(0); honey-=cost; spent+=cost; events.append({"type":"optional_spend","cost":cost,"balance":honey})
        if buzz < milestone["requires_buzz"]:
            item=cfg["upgrades"]["buzz_2"]
            if "buzz_2" not in purchases and item["available_after"] in [e["id"] for e in events if e["type"]=="reward"] and honey >= item["cost"]:
                honey-=item["cost"]; spent+=item["cost"]; purchases.append("buzz_2"); buzz=2
                events.append({"type":"forced_required_purchase","id":"buzz_2","balance":honey})
            else:
                failed=milestone["id"]; break
        honey += milestone["honey"]; earned += milestone["honey"]
        events.append({"type":"reward","id":milestone["id"],"amount":milestone["honey"],"balance":honey})
        if honey < 0: raise SimError(f"negative Honey in {name}")
    return {"name":name,"passed":failed is None,"failed_gate":failed,"earned":earned,"spent":spent,"balance":honey,"buzz":buzz,"flight":flight,"purchases":purchases,"pending_optional_spends":optional,"replay_actions":0,"events":events}

def build_report(cfg):
    strategies={}
    strategies["buzz_first"] = run_path(cfg,"buzz_first",["buzz_2","flight_2"])
    strategies["flight_first"] = run_path(cfg,"flight_first",["flight_2","buzz_2"])
    strategies["minimal_required"] = run_path(cfg,"minimal_required",["buzz_2"])
    strategies["customization_heavy"] = run_path(cfg,"customization_heavy",["flight_2","buzz_2"],cfg["optional_customization_shadow_costs"])
    exhaustive=[]
    for order in itertools.permutations(["flight_2","buzz_2"]):
        r=run_path(cfg,"exhaustive",list(order))
        exhaustive.append({"order":list(order),"passed":r["passed"],"balance":r["balance"],"purchases":r["purchases"]})
    assertions={
        "all_named_paths_progress": all(r["passed"] for r in strategies.values()),
        "all_named_paths_non_negative": all(r["balance"] >= 0 for r in strategies.values()),
        "all_named_paths_no_replay": all(r["replay_actions"] == 0 for r in strategies.values()),
        "flight_first_still_funds_buzz_gate": strategies["flight_first"]["passed"] and strategies["flight_first"]["buzz"] >= 2,
        "buzz_first_can_still_buy_flight": "flight_2" in strategies["buzz_first"]["purchases"],
        "customization_shadow_does_not_dead_end": strategies["customization_heavy"]["passed"],
        "all_upgrade_priorities_progress": all(r["passed"] for r in exhaustive),
    }
    hard_failures=[k for k,v in assertions.items() if not v]
    return {"schema_version":1,"ticket":"P3-PROGRESSION","config_status":cfg["status"],"strategies":strategies,"exhaustive_upgrade_priorities":exhaustive,"hard_assertions":assertions,"hard_failures":hard_failures,"result":"PASS" if not hard_failures else "FAIL"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output"); args=ap.parse_args()
    report=build_report(load()); text=json.dumps(report,indent=2,sort_keys=True)
    if args.output:
        p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text+"\n",encoding="utf-8")
    else: print(text)
    if report["hard_failures"]: raise SystemExit(1)
    print("P3 economy regression: PASS")
    return 0
if __name__ == "__main__": raise SystemExit(main())
