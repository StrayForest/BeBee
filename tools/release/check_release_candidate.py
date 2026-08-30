#!/usr/bin/env python3
"""Validate the bounded, privacy-safe P8 release-candidate surface."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MAX_BUNDLE_BYTES = 8 * 1024 * 1024
MAX_BUNDLE_FILES = 1500
MAX_STARTUP_MS = 10000


def read_json(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise RuntimeError(f"missing JSON report: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid JSON report: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON report must be an object: {path}")
    return value


def validate_release_candidate(*, head_sha: str, build_root: Path, build_report: Path, browser_smoke: Path, storage_report: Path) -> dict[str, object]:
    if not SHA_RE.fullmatch(head_sha):
        raise RuntimeError(f"release candidate head is not an exact commit SHA: {head_sha!r}")
    if not build_root.is_dir():
        raise RuntimeError(f"release bundle is missing: {build_root}")
    files = sorted(path for path in build_root.rglob("*") if path.is_file())
    if not files:
        raise RuntimeError("release bundle is empty")
    total_bytes = sum(path.stat().st_size for path in files)
    if total_bytes > MAX_BUNDLE_BYTES:
        raise RuntimeError(f"release bundle exceeds {MAX_BUNDLE_BYTES} bytes: {total_bytes}")
    if len(files) > MAX_BUNDLE_FILES:
        raise RuntimeError(f"release bundle exceeds {MAX_BUNDLE_FILES} files: {len(files)}")
    wasm_files = [path for path in files if path.suffix.lower() == ".wasm"]
    if not wasm_files:
        raise RuntimeError("release bundle has no WebAssembly payload")

    build = read_json(build_report)
    if build.get("build_commit_sha") and build.get("build_commit_sha") != head_sha:
        raise RuntimeError("release build report provenance drifted from the exact head")
    toolchain = build_report.with_name("release-toolchain.json")
    if toolchain.is_file():
        toolchain_report = read_json(toolchain)
        source_sha = toolchain_report.get("build_commit_sha")
        if source_sha and source_sha != head_sha:
            raise RuntimeError(f"release toolchain provenance drifted: {source_sha!r} != {head_sha!r}")
    smoke = read_json(browser_smoke)
    if smoke.get("result") != "pass":
        raise RuntimeError(f"browser smoke did not pass: {smoke!r}")
    startup_ms = smoke.get("startup_ms")
    if not isinstance(startup_ms, (int, float)) or startup_ms < 0 or startup_ms > MAX_STARTUP_MS:
        raise RuntimeError(f"browser startup budget failed: {startup_ms!r}")
    storage = read_json(storage_report)
    checks = storage.get("checks", [])
    release_checks = [check for check in checks if isinstance(check, dict) and check.get("id") == "release_debug_bridges_absent"]
    if len(release_checks) != 1 or release_checks[0].get("bridge_present") is not False or release_checks[0].get("bridge_names") != []:
        raise RuntimeError(f"release debug-bridge negative check failed: {release_checks!r}")
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(build_root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return {
        "schema_version": 1,
        "ticket": "P8-RELEASE-CANDIDATE",
        "head_sha": head_sha,
        "result": "pass",
        "bundle": {
            "bytes": total_bytes,
            "files": len(files),
            "wasm_files": [path.relative_to(build_root).as_posix() for path in wasm_files],
            "content_sha256": digest.hexdigest(),
        },
        "build_report": str(build_report),
        "browser_startup_ms": startup_ms,
        "browser_smoke": str(browser_smoke),
        "storage_report": str(storage_report),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--build-root", type=Path, required=True)
    parser.add_argument("--build-report", type=Path, required=True)
    parser.add_argument("--browser-smoke", type=Path, required=True)
    parser.add_argument("--storage-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = validate_release_candidate(head_sha=args.head_sha, build_root=args.build_root, build_report=args.build_report, browser_smoke=args.browser_smoke, storage_report=args.storage_report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
