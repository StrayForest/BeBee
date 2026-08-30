#!/usr/bin/env python3
"""Unit tests for the P8 release-candidate checker."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from check_release_candidate import validate_release_candidate


class ReleaseCandidateTests(unittest.TestCase):
    def test_valid_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            bundle = root / "bundle"
            bundle.mkdir()
            (bundle / "index.html").write_text("ok", encoding="utf-8")
            (bundle / "BeBee.wasm").write_bytes(b"wasm")
            build_report = root / "release.json"
            build_report.write_text(json.dumps({"ok": True}), encoding="utf-8")
            smoke = root / "smoke.json"
            smoke.write_text(json.dumps({"result": "pass", "startup_ms": 120}), encoding="utf-8")
            storage = root / "storage.json"
            storage.write_text(json.dumps({"checks": [{"id": "release_debug_bridges_absent", "bridge_present": False, "bridge_names": []}]}), encoding="utf-8")
            report = validate_release_candidate(head_sha="a" * 40, build_root=bundle, build_report=build_report, browser_smoke=smoke, storage_report=storage)
            self.assertEqual(report["result"], "pass")
            self.assertEqual(report["bundle"]["files"], 2)

    def test_rejects_non_exact_head(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            bundle = root / "bundle"
            bundle.mkdir()
            (bundle / "index.html").write_text("ok", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "exact commit SHA"):
                validate_release_candidate(head_sha="main", build_root=bundle, build_report=root / "build.json", browser_smoke=root / "smoke.json", storage_report=root / "storage.json")


if __name__ == "__main__":
    unittest.main()
