#!/usr/bin/env python3
"""Validate the BB-P009 storage contract without a Defold runtime."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "config" / "storage-contract.json"

REQUIRED_TESTS = {
    "clean_start",
    "normal_save_reload",
    "save_immediate_refresh",
    "save_rapid_close_reopen",
    "slot_a_corrupt_slot_b_valid",
    "slot_b_corrupt_slot_a_valid",
    "both_invalid",
    "generation_conflict_different_payload",
    "failed_write_preserves_previous_generation",
    "failed_readback_preserves_previous_generation",
    "old_version_sequential_migration",
    "migration_failure_preserves_original",
    "size_warning",
    "size_release_gate",
    "private_incognito_primary_portal",
    "storage_unavailable_or_quota_failure",
}


def load_contract(path: Path = CONTRACT_PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("storage contract root must be an object")
    return data


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    def need(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    need(data.get("schema_version") == 1, "schema_version must be 1")
    need(data.get("ticket") == "BB-P009", "ticket must be BB-P009")
    need(data.get("status") == "VALIDATED", "BB-P009 contract must be VALIDATED")

    boundary = data.get("domain_boundary", {})
    need(isinstance(boundary, dict), "domain_boundary must be an object")
    if isinstance(boundary, dict):
        need(boundary.get("gameplay_calls_sys_directly") is False, "gameplay may not call sys.save/sys.load directly")
        ops = boundary.get("service_operations", [])
        need(isinstance(ops, list) and {"load", "save", "has", "delete"}.issubset(set(ops)), "storage service operations are incomplete")

    local = data.get("local_adapter", {})
    need(isinstance(local, dict), "local_adapter must be an object")
    if isinstance(local, dict):
        need(local.get("defold_path_api") == "sys.get_save_file", "local adapter must resolve paths with sys.get_save_file")
        need(local.get("serialization_api") == "sys.save/sys.load", "local adapter serialization API mismatch")
        need(local.get("load_must_use_pcall") is True, "sys.load recovery must use pcall")
        slots = local.get("slot_files", {})
        need(isinstance(slots, dict), "slot_files must be an object")
        if isinstance(slots, dict):
            a, b = slots.get("a"), slots.get("b")
            need(isinstance(a, str) and bool(a), "slot A file must be named")
            need(isinstance(b, str) and bool(b), "slot B file must be named")
            need(a != b, "slot A and B must be distinct")
        need(local.get("temp_pointer_file") is None, "A/B journal must not depend on a mutable active-pointer file")
        need(local.get("readback_verification_required") is True, "new generation must be verified by readback")
        selection = str(local.get("selection_rule", "")).lower()
        need("highest generation" in selection, "load selection must prefer the highest valid generation")
        write_rule = str(local.get("write_rule", "")).lower()
        need("never overwrite the sole highest valid generation first" in write_rule, "save rule must preserve the sole latest valid generation")
        repair = str(local.get("repair_rule", "")).lower()
        need("do not immediately overwrite" in repair, "load recovery must preserve corrupt/invalid peer evidence")

    envelope = data.get("envelope", {})
    need(isinstance(envelope, dict), "envelope must be an object")
    if isinstance(envelope, dict):
        required = envelope.get("required_fields", [])
        need(isinstance(required, list) and {"format_version", "generation", "payload"}.issubset(set(required)), "save envelope fields are incomplete")
        need(envelope.get("ordering_uses_wall_clock") is False, "save ordering must not depend on wall clock")
        payload_required = envelope.get("payload_required_fields", [])
        need(isinstance(payload_required, list) and "save_version" in payload_required, "payload must require save_version")

    budget = data.get("size_budget", {})
    need(isinstance(budget, dict), "size_budget must be an object")
    if isinstance(budget, dict):
        ceiling = budget.get("defold_documented_output_ceiling_bytes")
        warning = budget.get("warning_bytes")
        gate = budget.get("release_gate_bytes")
        need(all(isinstance(v, int) and v > 0 for v in (warning, gate, ceiling)), "save size budgets must be positive integers")
        if all(isinstance(v, int) for v in (warning, gate, ceiling)):
            need(warning < gate < ceiling, "save size budget must satisfy warning < release gate < Defold ceiling")
        need(ceiling == 524288, "documented sys.save output ceiling must remain 512 KiB unless official docs change")

    durability = data.get("durability", {})
    need(isinstance(durability, dict), "durability must be an object")
    if isinstance(durability, dict):
        need(durability.get("html5_backend") == "browser virtual filesystem backed by IndexedDB", "HTML5 persistence backend must be IndexedDB-backed virtual FS")
        need(durability.get("local_html5_default_after_success") == "accepted_local_pending_browser_persistence", "HTML5 sys.save success must not be mislabeled as immediately durable")
        semantics = str(durability.get("sys_save_success_semantics", ""))
        need("not_proof_of_immediate_indexeddb_durability" in semantics, "durability semantics must record delayed browser persistence")

    migration = data.get("migration", {})
    need(isinstance(migration, dict), "migration must be an object")
    if isinstance(migration, dict):
        need(migration.get("required") is True, "save migrations are required")
        need(migration.get("strategy") == "sequential_version_steps", "migration strategy must be sequential version steps")
        need("never overwrite the only valid pre-migration generation" in str(migration.get("migration_failure_rule", "")), "migration failure must preserve original valid generation")

    matrix = data.get("test_matrix", [])
    need(isinstance(matrix, list), "test_matrix must be a list")
    ids: set[str] = set()
    if isinstance(matrix, list):
        for row in matrix:
            if not isinstance(row, dict):
                errors.append("test_matrix entries must be objects")
                continue
            test_id = row.get("id")
            if not isinstance(test_id, str) or not test_id:
                errors.append("test_matrix id must be non-empty")
                continue
            if test_id in ids:
                errors.append(f"duplicate storage test id: {test_id}")
            ids.add(test_id)
            if test_id in REQUIRED_TESTS:
                need(row.get("required") is True, f"required storage test {test_id} may not be optional")
    missing = REQUIRED_TESTS - ids
    need(not missing, "storage test matrix is missing: " + ", ".join(sorted(missing)))

    poki = data.get("poki", {})
    need(isinstance(poki, dict), "poki storage constraints must be an object")
    if isinstance(poki, dict):
        need("MUST_VERIFY" in str(poki.get("defold_idbfs_cloud_sync_status", "")), "Defold IndexedDB cloud-sync behavior must remain verification-gated")
        need("playable" in str(poki.get("incognito_requirement", "")).lower(), "incognito storage failure must preserve playability")

    p0 = data.get("p0_exit_requirements", [])
    need(isinstance(p0, list) and len(p0) >= 8, "P0 storage exit requirements are incomplete")

    return errors


def main() -> int:
    errors = validate(load_contract())
    if errors:
        print("BB-P009 storage contract validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print("BB-P009 storage contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
