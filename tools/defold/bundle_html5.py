#!/usr/bin/env python3
"""Build BeBee HTML5 bundles with the repository-pinned Defold Bob toolchain."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLCHAIN_PATH = ROOT / "tools" / "defold" / "toolchain.json"
MODES = {
    "development": {
        "settings": ROOT / "config" / "defold" / "development.settings",
        "variant": "debug",
    },
    "release": {
        "settings": ROOT / "config" / "defold" / "release.settings",
        "variant": "release",
    },
}


def load_toolchain() -> dict[str, object]:
    data = json.loads(TOOLCHAIN_PATH.read_text(encoding="utf-8"))
    required = {
        "defold_version",
        "bob_url",
        "bob_sha256",
        "java_major",
        "platform",
        "architectures",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise RuntimeError(f"Missing toolchain keys: {', '.join(missing)}")
    digest = str(data["bob_sha256"]).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise RuntimeError("toolchain bob_sha256 must be a 64-character SHA-256 digest")
    return data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_commit_sha() -> str:
    override = os.environ.get("BEBEE_BUILD_COMMIT_SHA", "").strip().lower()
    if override:
        if not re.fullmatch(r"[0-9a-f]{40}", override):
            raise RuntimeError("BEBEE_BUILD_COMMIT_SHA must be a full 40-character Git SHA")
        return override

    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    commit_sha = result.stdout.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", commit_sha):
        raise RuntimeError(f"Could not resolve exact source Git SHA: {commit_sha!r}")
    return commit_sha


def verify_bob(path: Path, expected_sha256: str) -> None:
    if not path.is_file():
        raise RuntimeError(f"Bob JAR not found: {path}")
    actual = sha256(path)
    if actual != expected_sha256:
        raise RuntimeError(
            f"Bob SHA-256 mismatch for {path}: expected {expected_sha256}, got {actual}"
        )


def cached_bob_path(toolchain: dict[str, object]) -> Path:
    cache_root = Path(
        os.environ.get(
            "BEBEE_DEFOLD_CACHE",
            str(Path.home() / ".cache" / "bebee" / "defold"),
        )
    )
    return cache_root / str(toolchain["defold_version"]) / "bob.jar"


def download_bob(toolchain: dict[str, object], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    expected = str(toolchain["bob_sha256"]).lower()
    if destination.is_file():
        verify_bob(destination, expected)
        return destination

    request = urllib.request.Request(
        str(toolchain["bob_url"]),
        headers={"User-Agent": "BeBee-BB001-pinned-builder"},
    )
    with tempfile.NamedTemporaryFile(
        prefix="bob-", suffix=".jar", dir=destination.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                shutil.copyfileobj(response, handle)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise

    try:
        verify_bob(temporary, expected)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def java_major() -> int:
    result = subprocess.run(
        ["java", "-version"],
        check=True,
        capture_output=True,
        text=True,
    )
    text = (result.stdout + "\n" + result.stderr).strip()
    match = re.search(r'version "(\d+)', text)
    if not match:
        raise RuntimeError(f"Could not parse Java version from:\n{text}")
    return int(match.group(1))


def verify_bob_version(bob: Path, expected_version: str) -> str:
    result = subprocess.run(
        ["java", "-jar", str(bob), "--version"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    if expected_version not in output:
        raise RuntimeError(
            f"Pinned Bob did not report Defold {expected_version}. Output:\n{output}"
        )
    return output


def build(mode: str, bob: Path, toolchain: dict[str, object], commit_sha: str) -> Path:
    mode_config = MODES[mode]
    settings = Path(mode_config["settings"])
    if not settings.is_file():
        raise RuntimeError(f"Missing {mode} settings: {settings}")

    build_output = ROOT / "build" / "bob" / mode
    bundle_output = ROOT / "build" / "html5" / mode
    report_output = ROOT / "build" / "reports" / f"{mode}.json"

    shutil.rmtree(build_output, ignore_errors=True)
    shutil.rmtree(bundle_output, ignore_errors=True)
    build_output.parent.mkdir(parents=True, exist_ok=True)
    bundle_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.parent.mkdir(parents=True, exist_ok=True)

    build_output_arg = str(build_output.relative_to(ROOT))
    report_output_arg = str(report_output.relative_to(ROOT))

    # Defold reserves the project's build/ tree for compiled intermediates and
    # refuses to bundle into it directly. Bundle into an external temporary
    # directory first, then copy the completed artifact into our stable CI path.
    with tempfile.TemporaryDirectory(prefix=f"bebee-{mode}-bundle-") as temp_dir:
        temp_root = Path(temp_dir)
        staged_bundle_output = temp_root / "bundle"
        staged_bundle_output.mkdir()
        provenance_settings = temp_root / "build-provenance.settings"
        provenance_settings.write_text(
            "[bebee]\n" f"build_commit_sha = {commit_sha}\n",
            encoding="utf-8",
        )
        command = [
            "java",
            "-jar",
            str(bob),
            "--root",
            str(ROOT),
            "--settings",
            str(settings),
            "--settings",
            str(provenance_settings),
            "--platform",
            str(toolchain["platform"]),
            "--architectures",
            str(toolchain["architectures"]),
            "--variant",
            str(mode_config["variant"]),
            "--archive",
            "--output",
            build_output_arg,
            "--bundle-output",
            str(staged_bundle_output),
            "--build-report-json",
            report_output_arg,
            "resolve",
            "build",
            "bundle",
        ]
        print("+", " ".join(command), flush=True)
        subprocess.run(command, check=True, cwd=ROOT)

        staged_bundle_dir = staged_bundle_output / "BeBee"
        staged_index = staged_bundle_dir / "index.html"
        if not staged_index.is_file():
            raise RuntimeError(
                f"Expected staged HTML5 entry point was not produced: {staged_index}"
            )
        shutil.copytree(staged_bundle_dir, bundle_output / "BeBee")

    bundle_dir = bundle_output / "BeBee"
    index = bundle_dir / "index.html"
    if not index.is_file():
        raise RuntimeError(f"Expected HTML5 entry point was not produced: {index}")

    metadata = {
        "mode": mode,
        "build_commit_sha": commit_sha,
        "qa_enabled": mode == "development",
        "defold_version": toolchain["defold_version"],
        "bob_sha256": toolchain["bob_sha256"],
        "java_major": toolchain["java_major"],
        "platform": toolchain["platform"],
        "architectures": toolchain["architectures"],
        "variant": mode_config["variant"],
        "settings": str(settings.relative_to(ROOT)),
        "bundle": str(bundle_dir.relative_to(ROOT)),
    }
    (report_output.parent / f"{mode}-toolchain.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return bundle_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=sorted(MODES), required=True)
    parser.add_argument(
        "--bob",
        type=Path,
        help="Optional local bob.jar path. It must match the pinned SHA-256.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    toolchain = load_toolchain()

    required_java = int(toolchain["java_major"])
    actual_java = java_major()
    if actual_java != required_java:
        raise RuntimeError(
            f"Pinned Defold toolchain requires Java {required_java}, got Java {actual_java}"
        )

    commit_sha = source_commit_sha()
    bob = args.bob.expanduser().resolve() if args.bob else cached_bob_path(toolchain)
    if args.bob:
        verify_bob(bob, str(toolchain["bob_sha256"]).lower())
    else:
        bob = download_bob(toolchain, bob)

    version_output = verify_bob_version(bob, str(toolchain["defold_version"]))
    print(version_output, flush=True)
    bundle_dir = build(args.mode, bob, toolchain, commit_sha)
    print(f"HTML5 bundle ready: {bundle_dir} (source {commit_sha})", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"BB-001 build failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
