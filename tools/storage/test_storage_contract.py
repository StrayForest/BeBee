#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "storage" / "check_storage_contract.py"

spec = importlib.util.spec_from_file_location("check_storage_contract", MODULE_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def load_contract() -> dict:
    return json.loads((ROOT / "config" / "storage-contract.json").read_text(encoding="utf-8"))


class StorageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_contract()

    def assertRejected(self, mutate, needle: str) -> None:
        data = copy.deepcopy(self.contract)
        mutate(data)
        errors = checker.validate(data)
        self.assertTrue(any(needle in error for error in errors), errors)

    def test_current_contract_passes(self) -> None:
        self.assertEqual(checker.validate(self.contract), [])

    def test_gameplay_cannot_call_sys_directly(self) -> None:
        self.assertRejected(
            lambda data: data["domain_boundary"].__setitem__("gameplay_calls_sys_directly", True),
            "may not call sys.save/sys.load directly",
        )

    def test_rejects_single_slot_configuration(self) -> None:
        def mutate(data):
            data["local_adapter"]["slot_files"]["b"] = data["local_adapter"]["slot_files"]["a"]

        self.assertRejected(mutate, "must be distinct")

    def test_rejects_mutable_pointer_dependency(self) -> None:
        self.assertRejected(
            lambda data: data["local_adapter"].__setitem__("temp_pointer_file", "active_slot"),
            "must not depend on a mutable active-pointer",
        )

    def test_rejects_missing_readback_verification(self) -> None:
        self.assertRejected(
            lambda data: data["local_adapter"].__setitem__("readback_verification_required", False),
            "verified by readback",
        )

    def test_rejects_budget_inversion(self) -> None:
        self.assertRejected(
            lambda data: data["size_budget"].__setitem__("release_gate_bytes", 600000),
            "warning < release gate < Defold ceiling",
        )

    def test_rejects_false_immediate_durability_claim(self) -> None:
        self.assertRejected(
            lambda data: data["durability"].__setitem__("local_html5_default_after_success", "durable_confirmed_if_future_adapter_can_prove_it"),
            "must not be mislabeled as immediately durable",
        )

    def test_rejects_missing_corruption_recovery_case(self) -> None:
        def mutate(data):
            data["test_matrix"] = [
                row for row in data["test_matrix"] if row["id"] != "slot_a_corrupt_slot_b_valid"
            ]

        self.assertRejected(mutate, "storage test matrix is missing")

    def test_rejects_optional_failed_write_preservation_case(self) -> None:
        def mutate(data):
            row = next(
                row
                for row in data["test_matrix"]
                if row["id"] == "failed_write_preserves_previous_generation"
            )
            row["required"] = False

        self.assertRejected(mutate, "may not be optional")

    def test_rejects_unverified_portal_cloud_assumption(self) -> None:
        self.assertRejected(
            lambda data: data["poki"].__setitem__("defold_idbfs_cloud_sync_status", "ASSUMED_WORKING"),
            "must remain verification-gated",
        )


if __name__ == "__main__":
    unittest.main()
