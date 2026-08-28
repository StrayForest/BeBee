#!/usr/bin/env python3
"""Build and execute BeBee's deterministic Defold headless test suite."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TEST_SETTINGS = ROOT / "tests" / "test.settings"
TEST_BUNDLE = ROOT / "build" / "tests" / "BeBee"
TEST_REPORT = ROOT / "build" / "reports" / "tests.json"
TEST_RESULTS = ROOT / "build" / "test-results"

sys.path.insert(0, str(HERE))
import bundle_html5 as defold_builder  # noqa: E402


def build_headless(bob: Path) -> Path:
    build_output = ROOT / "build" / "bob" / "tests"
    shutil.rmtree(build_output, ignore_errors=True)
    shutil.rmtree(TEST_BUNDLE.parent, ignore_errors=True)
    TEST_REPORT.parent.mkdir(parents=True, exist_ok=True)

    build_output_arg = str(build_output.relative_to(ROOT))
    report_output_arg = str(TEST_REPORT.relative_to(ROOT))

    with tempfile.TemporaryDirectory(prefix="bebee-tests-bundle-") as temp_dir:
        staged_root = Path(temp_dir)
        command = [
            "java",
            "-jar",
            str(bob),
            "--root",
            str(ROOT),
            "--settings",
            str(TEST_SETTINGS),
            "--platform",
            "x86_64-linux",
            "--variant",
            "headless",
            "--archive",
            "--output",
            build_output_arg,
            "--bundle-output",
            str(staged_root),
            "--build-report-json",
            report_output_arg,
            "resolve",
            "build",
            "bundle",
        ]
        print("+", " ".join(command), flush=True)
        subprocess.run(command, check=True, cwd=ROOT)

        staged_bundle = staged_root / "BeBee"
        if not staged_bundle.is_dir():
            raise RuntimeError(
                f"Expected headless bundle was not produced: {staged_bundle}"
            )
        shutil.copytree(staged_bundle, TEST_BUNDLE)

    return TEST_BUNDLE


def find_executable(bundle_dir: Path) -> Path:
    preferred = bundle_dir / "dmengine_headless"
    if preferred.is_file():
        return preferred

    executable_files = sorted(
        path
        for path in bundle_dir.rglob("*")
        if path.is_file() and os.access(path, os.X_OK)
    )
    if len(executable_files) == 1:
        return executable_files[0]

    names = ", ".join(str(path.relative_to(bundle_dir)) for path in executable_files)
    raise RuntimeError(
        "Could not identify a unique headless executable in "
        f"{bundle_dir}; executable candidates: {names or '<none>'}"
    )


def parse_events(log_text: str) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    marker = "BEBEE_TEST "
    for line in log_text.splitlines():
        marker_index = line.find(marker)
        if marker_index < 0:
            continue
        payload = line[marker_index + len(marker) :].strip()
        try:
            event = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Invalid BEBEE_TEST JSON event: {payload!r}: {exc}"
            ) from exc
        if not isinstance(event, dict):
            raise RuntimeError(f"BEBEE_TEST event must be an object: {payload!r}")
        events.append(event)
    return events


def run_suite(executable: Path, timeout_seconds: int) -> dict[str, object]:
    TEST_RESULTS.mkdir(parents=True, exist_ok=True)
    log_path = TEST_RESULTS / "headless.log"

    try:
        result = subprocess.run(
            [str(executable)],
            cwd=executable.parent,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        log_path.write_text(stdout + stderr, encoding="utf-8")
        raise RuntimeError(
            f"Headless test suite timed out after {timeout_seconds}s"
        ) from exc

    log_text = result.stdout + result.stderr
    log_path.write_text(log_text, encoding="utf-8")
    events = parse_events(log_text)
    completions = [event for event in events if event.get("event") == "suite_end"]

    if len(completions) != 1:
        raise RuntimeError(
            f"Expected exactly one suite_end event, found {len(completions)}; "
            f"see {log_path.relative_to(ROOT)}"
        )

    completion = completions[0]
    if result.returncode != 0:
        raise RuntimeError(
            f"Headless suite exited with {result.returncode}; "
            f"see {log_path.relative_to(ROOT)}"
        )
    if completion.get("status") != "pass" or completion.get("failed") != 0:
        raise RuntimeError(
            f"Headless suite reported failure: {json.dumps(completion, sort_keys=True)}"
        )

    return {
        "schema_version": 1,
        "status": "pass",
        "exit_code": result.returncode,
        "completion": completion,
        "event_count": len(events),
        "log": str(log_path.relative_to(ROOT)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bob",
        type=Path,
        help="Optional local bob.jar path; it must match the pinned SHA-256.",
    )
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.timeout < 1:
        raise RuntimeError("--timeout must be at least one second")

    toolchain = defold_builder.load_toolchain()
    required_java = int(toolchain["java_major"])
    actual_java = defold_builder.java_major()
    if actual_java != required_java:
        raise RuntimeError(
            f"Pinned Defold toolchain requires Java {required_java}, got Java {actual_java}"
        )

    bob = (
        args.bob.expanduser().resolve()
        if args.bob
        else defold_builder.cached_bob_path(toolchain)
    )
    if args.bob:
        defold_builder.verify_bob(bob, str(toolchain["bob_sha256"]).lower())
    else:
        bob = defold_builder.download_bob(toolchain, bob)

    defold_builder.verify_bob_version(bob, str(toolchain["defold_version"]))
    bundle_dir = build_headless(bob)
    executable = find_executable(bundle_dir)
    summary = run_suite(executable, args.timeout)
    summary.update(
        {
            "defold_version": toolchain["defold_version"],
            "java_major": toolchain["java_major"],
            "platform": "x86_64-linux",
            "variant": "headless",
        }
    )

    TEST_RESULTS.mkdir(parents=True, exist_ok=True)
    summary_path = TEST_RESULTS / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "BB-004 tests: PASS "
        f"({summary['completion']['passed']}/{summary['completion']['tests']})"
    )
    print(f"Result: {summary_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"BB-004 tests failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
