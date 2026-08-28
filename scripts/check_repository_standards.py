#!/usr/bin/env python3
"""Validate BeBee repository/tooling standards without third-party Python packages."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
STANDARDS_PATH = ROOT / "config" / "repository-standards.json"
DEPENDENCIES_PATH = ROOT / "config" / "dependencies.json"
THIRD_PARTY_PATH = ROOT / "THIRD_PARTY.md"
GITIGNORE_PATH = ROOT / ".gitignore"

TEXT_SUFFIXES = {
    ".atlas",
    ".camera",
    ".collection",
    ".collectionfactory",
    ".collectionproxy",
    ".editorconfig",
    ".factory",
    ".font",
    ".go",
    ".gui",
    ".gui_script",
    ".input_binding",
    ".json",
    ".label",
    ".lua",
    ".material",
    ".md",
    ".mesh",
    ".model",
    ".particlefx",
    ".project",
    ".py",
    ".render",
    ".render_script",
    ".script",
    ".settings",
    ".sound",
    ".sprite",
    ".tilemap",
    ".tilesource",
    ".yaml",
    ".yml",
}
TEXT_NAMES = {".editorconfig", ".gitignore", ".luacheckrc", "game.project"}
PYTHON_SUFFIXES = {".py"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(errors, f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(errors, f"{path.relative_to(ROOT)}: top level must be an object")
        return {}
    return value


def tracked_files(errors: list[str]) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(errors, f"git ls-files failed: {exc}")
        return []
    paths: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if raw:
            paths.append(ROOT / raw.decode("utf-8"))
    return paths


def check_required_files(errors: list[str]) -> None:
    for relative in (
        ".editorconfig",
        ".gitignore",
        ".luacheckrc",
        "config/dependencies.json",
        "config/repository-standards.json",
        "THIRD_PARTY.md",
        "game.project",
    ):
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required repository-standard file: {relative}")


def check_gitignore(standards: dict[str, object], errors: list[str]) -> None:
    try:
        entries = {
            line.strip()
            for line in GITIGNORE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
    except OSError as exc:
        fail(errors, f".gitignore unreadable: {exc}")
        return
    required = standards.get("required_gitignore_entries", [])
    if not isinstance(required, list):
        fail(errors, "repository-standards required_gitignore_entries must be an array")
        return
    for entry in required:
        if not isinstance(entry, str) or entry not in entries:
            fail(errors, f".gitignore missing required entry: {entry!r}")


def is_text_file(path: Path) -> bool:
    return path.name in TEXT_NAMES or path.suffix in TEXT_SUFFIXES


def check_text_hygiene(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if not is_text_file(path):
            continue
        relative = path.relative_to(ROOT)
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            fail(errors, f"{relative}: expected UTF-8 text: {exc}")
            continue
        if b"\r" in raw:
            fail(errors, f"{relative}: CR/CRLF line ending found; LF is required")
        if raw and not raw.endswith(b"\n"):
            fail(errors, f"{relative}: final newline required")
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip(" \t") != line:
                fail(errors, f"{relative}:{number}: trailing whitespace")
        if path.suffix in {".lua", ".script", ".gui_script", ".render_script", ".py"}:
            for number, line in enumerate(text.splitlines(), 1):
                prefix = line[: len(line) - len(line.lstrip(" \t"))]
                if "\t" in prefix:
                    fail(errors, f"{relative}:{number}: leading tabs are not allowed")


def check_json(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            fail(errors, f"{path.relative_to(ROOT)}: invalid JSON: {exc}")


def check_python(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix not in PYTHON_SUFFIXES:
            continue
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path.relative_to(ROOT)), "exec")
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            fail(errors, f"{path.relative_to(ROOT)}: Python syntax error: {exc}")


def check_source_layout(
    files: list[Path], standards: dict[str, object], errors: list[str]
) -> None:
    runtime_roots = standards.get("canonical_runtime_roots", [])
    prototype_roots = standards.get("allowed_nonproduction_runtime_roots", [])
    runtime_extensions = standards.get("runtime_resource_extensions", [])
    if not all(isinstance(item, str) for item in runtime_roots):
        fail(errors, "canonical_runtime_roots must contain strings only")
        return
    if not all(isinstance(item, str) for item in prototype_roots):
        fail(errors, "allowed_nonproduction_runtime_roots must contain strings only")
        return
    if not all(isinstance(item, str) for item in runtime_extensions):
        fail(errors, "runtime_resource_extensions must contain strings only")
        return
    allowed = set(runtime_roots) | set(prototype_roots)
    extensions = set(runtime_extensions)
    for path in files:
        relative = path.relative_to(ROOT)
        if relative.name == "game.project" or path.suffix not in extensions:
            continue
        if not relative.parts or relative.parts[0] not in allowed:
            fail(
                errors,
                f"{relative}: Defold/runtime resource is outside canonical roots {sorted(allowed)}",
            )


def valid_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def dependency_urls_from_game_project(errors: list[str]) -> set[str]:
    try:
        lines = (ROOT / "game.project").read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(errors, f"game.project unreadable: {exc}")
        return set()
    urls: set[str] = set()
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = (part.strip() for part in stripped.split("=", 1))
        if key == "dependencies" or key.startswith("dependencies#"):
            for item in value.split(","):
                item = item.strip()
                if item:
                    urls.add(item)
    return urls


def check_dependencies(errors: list[str]) -> None:
    manifest = load_json(DEPENDENCIES_PATH, errors)
    dependencies = manifest.get("dependencies", [])
    if not isinstance(dependencies, list):
        fail(errors, "config/dependencies.json: dependencies must be an array")
        return
    required = {
        "id",
        "name",
        "kind",
        "source",
        "version",
        "license",
        "license_source",
        "commercial_use_allowed",
        "redistribution_allowed",
        "runtime_included",
        "attribution",
        "reviewed_date",
    }
    ids: set[str] = set()
    library_urls: set[str] = set()
    try:
        ledger = THIRD_PARTY_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        fail(errors, f"THIRD_PARTY.md unreadable: {exc}")
        ledger = ""
    for index, item in enumerate(dependencies):
        if not isinstance(item, dict):
            fail(errors, f"dependency[{index}] must be an object")
            continue
        missing = sorted(required - item.keys())
        if missing:
            fail(errors, f"dependency[{index}] missing fields: {', '.join(missing)}")
            continue
        dep_id = item.get("id")
        if not isinstance(dep_id, str) or not dep_id:
            fail(errors, f"dependency[{index}] id must be a non-empty string")
        elif dep_id in ids:
            fail(errors, f"duplicate dependency id: {dep_id}")
        else:
            ids.add(dep_id)
        for field in ("name", "kind", "version", "license", "attribution", "reviewed_date"):
            if not isinstance(item.get(field), str) or not str(item[field]).strip():
                fail(errors, f"dependency[{index}] {field} must be non-empty")
        if not valid_http_url(item.get("source")):
            fail(errors, f"dependency[{index}] source must be an https URL")
        if not valid_http_url(item.get("license_source")):
            fail(errors, f"dependency[{index}] license_source must be an https URL")
        if item.get("commercial_use_allowed") is not True:
            fail(errors, f"dependency[{index}] is not approved for commercial use")
        if item.get("redistribution_allowed") is not True:
            fail(errors, f"dependency[{index}] is not approved for redistribution")
        if not isinstance(item.get("runtime_included"), bool):
            fail(errors, f"dependency[{index}] runtime_included must be boolean")
        name = item.get("name")
        source = item.get("source")
        if isinstance(name, str) and name not in ledger:
            fail(errors, f"THIRD_PARTY.md missing dependency name: {name}")
        if isinstance(source, str) and source not in ledger:
            fail(errors, f"THIRD_PARTY.md missing dependency source: {source}")
        if item.get("kind") == "defold-library" and isinstance(source, str):
            library_urls.add(source)

    project_urls = dependency_urls_from_game_project(errors)
    for url in sorted(project_urls - library_urls):
        fail(errors, f"game.project dependency is not registered as defold-library: {url}")
    for url in sorted(library_urls - project_urls):
        fail(errors, f"registered defold-library is not present in game.project: {url}")


def check_generated_not_tracked(
    files: list[Path], standards: dict[str, object], errors: list[str]
) -> None:
    generated = standards.get("generated_roots", [])
    if not all(isinstance(item, str) for item in generated):
        fail(errors, "generated_roots must contain strings only")
        return
    generated_set = set(generated)
    for path in files:
        relative = path.relative_to(ROOT)
        if relative.parts and relative.parts[0] in generated_set:
            fail(errors, f"generated path is tracked: {relative}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    standards = load_json(STANDARDS_PATH, errors)
    files = tracked_files(errors)
    if standards:
        check_gitignore(standards, errors)
        check_source_layout(files, standards, errors)
        check_generated_not_tracked(files, standards, errors)
    check_text_hygiene(files, errors)
    check_json(files, errors)
    check_python(files, errors)
    check_dependencies(errors)

    if errors:
        print("Repository standards: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Repository standards: PASS ({len(files)} tracked files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
