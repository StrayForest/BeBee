#!/usr/bin/env python3
"""Trusted-base trust-boundary checks for BeBee pull requests.

This layer is intentionally small and additive. The workflow must execute the copy
from the PR base/default branch while the working directory is the candidate
checkout. Candidate changes are therefore data, not policy.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

PLAYER_DATA_PREFIXES = ("data/flowers", "data/regions", "data/meadows")
HIGH_RISK_EXTENSIONS = {".lua", ".script"}
GOVERNANCE_FILES = {
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/pr-evidence.yml",
    ".github/workflows/pr-evidence-trusted.yml",
    "AGENTS.md",
    "DECISIONS.md",
    "docs/10-development-workflow.md",
    "docs/11-blueprint-hardening.md",
    "docs/15-agent-evidence-governance.md",
    "docs/16-ci-trust-boundary.md",
    "scripts/check_pr_evidence.py",
    "scripts/check_pr_evidence_policy.py",
    "scripts/check_trust_boundary.py",
}
GOVERNANCE_PREFIXES = (".github/workflows/", "scripts/policy_tests/")
MILESTONE_GATES = {"none", "P2", "P4", "P6"}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    p = urlparse(value.strip())
    return p.scheme in {"http", "https"} and bool(p.netloc)


def field_from_body(body: str, label: str) -> str:
    match = re.search(
        rf"^- {re.escape(label)}:[ \t]*(.*?)[ \t]*$",
        body,
        flags=re.MULTILINE,
    )
    if not match:
        return ""
    value = match.group(1).strip()
    if value.startswith("`") and value.endswith("`") and value.count("`") == 2:
        value = value[1:-1].strip()
    return value


def section_between(body: str, start: str, end: str) -> str:
    match = re.search(
        rf"{re.escape(start)}(?P<block>.*?){re.escape(end)}",
        body,
        flags=re.DOTALL,
    )
    return match.group("block") if match else ""


def same_line_value(block: str, label: str) -> str:
    match = re.search(
        rf"^{re.escape(label)}[ \t]*(.*?)[ \t]*$",
        block,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def changed_files_from_git(base_sha: str, head_sha: str) -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base_sha, head_sha],
        check=True,
        capture_output=True,
        text=True,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def is_governance(path: str) -> bool:
    return path in GOVERNANCE_FILES or any(path.startswith(prefix) for prefix in GOVERNANCE_PREFIXES)


def is_player_data(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in PLAYER_DATA_PREFIXES)


def is_unclassified_high_risk_script(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    if suffix not in HIGH_RISK_EXTENSIONS:
        return False
    known_player = path.startswith(("gameplay/", "ui/", "main/", "input/", "levels/"))
    known_economy = path.startswith(
        ("data/economy", "data/upgrades", "data/seeds", "systems/economy", "systems/progression")
    )
    return not known_player and not known_economy


def load_manifest(candidate_path: str) -> dict | None:
    if not re.fullmatch(r"evidence/[A-Za-z0-9._-]+/manifest\.json", candidate_path or ""):
        return None
    path = Path(candidate_path)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def validate_official_docs(body: str) -> list[str]:
    block = section_between(body, "### Official technical documentation", "## Alternatives / BeBee decision")
    if not block:
        return ["Official technical documentation section is missing."]
    doc = same_line_value(block, "- Official doc 1:")
    na = same_line_value(block, "If official-doc research is not applicable, explain why:")
    if (doc and not doc.startswith("<")) or (na and not na.startswith("<")):
        return []
    return [
        "Official-doc evidence is blank: provide Official doc 1 or a same-line N/A reason. "
        "Blank fields may not consume text from following lines."
    ]


def validate_reference_identity(data: dict) -> list[str]:
    errors: list[str] = []
    research = data.get("research")
    if not isinstance(research, dict):
        return ["Player-facing/economy manifest research must be an object."]

    for key in ("candidate_pool", "selected_references"):
        items = research.get(key)
        if not isinstance(items, list):
            continue
        product_ids: list[str] = []
        urls: list[str] = []
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"research.{key}[{index}] must be an object.")
                continue
            product_id = item.get("product_id")
            if not nonempty(product_id):
                errors.append(f"research.{key}[{index}].product_id is required.")
            else:
                product_ids.append(product_id.strip().lower())
            source = item.get("source")
            if valid_http_url(source):
                urls.append(source.strip())
        if len(product_ids) != len(set(product_ids)):
            errors.append(
                f"research.{key} must use distinct product_id values; multiple URLs/pages from one product do not count as independent products."
            )
        if len(urls) != len(set(urls)):
            errors.append(f"research.{key} contains duplicate source URLs.")
    return errors


def validate_governance_manifest(data: dict | None) -> list[str]:
    if data is None:
        return ["Governance-critical changes require a valid same-PR evidence manifest."]
    governance = data.get("governance")
    if not isinstance(governance, dict):
        return ["Governance-critical evidence requires a governance object."]
    errors: list[str] = []
    for key in ("trust_boundary_change", "bypass_analysis", "rollback"):
        if not nonempty(governance.get(key)):
            errors.append(f"governance.{key} must be non-empty.")
    return errors


def validate(*, body: str, changed_files: set[str]) -> list[str]:
    errors: list[str] = []
    change_class = field_from_body(body, "Change class")
    manifest_path = field_from_body(body, "Evidence manifest")
    milestone_gate = field_from_body(body, "Milestone gate")

    errors.extend(validate_official_docs(body))

    if milestone_gate not in MILESTONE_GATES:
        errors.append("Milestone gate must be exactly one of: none, P2, P4, P6.")

    if any(is_player_data(path) for path in changed_files) and change_class not in {"player-facing", "economy"}:
        errors.append("Flower/region/meadow data is player-facing content and cannot be classified as technical/process/trivial.")

    if any(is_unclassified_high_risk_script(path) for path in changed_files) and change_class not in {
        "technical",
        "player-facing",
        "economy",
    }:
        errors.append("Unclassified .lua/.script runtime changes require at least technical evidence.")

    governance_changed = any(is_governance(path) for path in changed_files)
    data = load_manifest(manifest_path)

    if governance_changed:
        if change_class != "process":
            errors.append("Governance-critical files must use Change class `process`.")
        if manifest_path not in changed_files:
            errors.append("Governance-critical evidence manifest must be changed in the same PR.")
        errors.extend(validate_governance_manifest(data))

    if change_class in {"player-facing", "economy"} and data is not None:
        errors.extend(validate_reference_identity(data))

    return errors


def main() -> int:
    body = os.environ.get("PR_BODY", "")
    base_sha = os.environ.get("BASE_SHA", "").strip()
    head_sha = os.environ.get("HEAD_SHA", "").strip()
    try:
        changed_files = changed_files_from_git(base_sha, head_sha)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Trust-boundary validation failed:\n\n- Could not determine changed files: {exc}")
        return 1

    errors = validate(body=body, changed_files=changed_files)
    if errors:
        print("Trust-boundary validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Trusted-base trust-boundary checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
