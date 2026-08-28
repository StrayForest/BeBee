#!/usr/bin/env python3
"""Additional BeBee PR policy checks that bind evidence requirements to the actual diff.

This complements scripts/check_pr_evidence.py. The original validator checks the
declared PR/evidence structure. This layer checks whether the declared change
class is compatible with files changed by the PR and adds stricter requirements
for high-risk technical work.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_CLASSES = {"player-facing", "economy", "technical", "process", "trivial"}

PLAYER_PREFIXES = (
    "gameplay/",
    "ui/",
    "art/",
    "audio/",
    "levels/",
    "input/",
    "main/",
)
PLAYER_EXTENSIONS = {
    ".gui",
    ".collection",
    ".go",
    ".sprite",
    ".atlas",
    ".particlefx",
    ".tilesource",
    ".tilemap",
    ".font",
    ".material",
    ".render",
    ".render_script",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".wav",
    ".ogg",
    ".mp3",
}

ECONOMY_PREFIXES = (
    "data/economy",
    "data/upgrades",
    "data/seeds",
    "systems/economy",
    "systems/progression",
)

HIGH_RISK_TECH_PREFIXES = (
    "app/",
    "adapters/",
    "systems/storage",
    "systems/platform",
    "systems/analytics",
    "scripts/build",
    "scripts/test",
    "scripts/serve_build",
    "scripts/capture_visuals",
)
HIGH_RISK_TECH_FILES = {
    "game.project",
}
HIGH_RISK_TECH_EXTENSIONS = {".lua"}

MEANINGFUL_RUNTIME_EXTENSIONS = PLAYER_EXTENSIONS | HIGH_RISK_TECH_EXTENSIONS | {
    ".script",
    ".input_binding",
}

ALLOWED_PROVENANCE = {
    "OWNER_CONSTRAINT",
    "REFERENCE_PATTERN",
    "TECH_CONSTRAINT",
    "EXPERIMENT_RESULT",
    "SIMULATION_RESULT",
    "TELEMETRY_RESULT",
    "PLAYTEST_RESULT",
    "SUBJECTIVE_DIRECTION",
}
ALLOWED_STRENGTH = {"LOW", "MEDIUM", "HIGH"}
PR_HEAD_BINDING = "$PR_HEAD"


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def field_from_body(body: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+?)\s*$", body, flags=re.MULTILINE)
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


def changed_files_from_git(base_sha: str, head_sha: str) -> set[str]:
    if not base_sha or not head_sha:
        return set()
    result = subprocess.run(
        ["git", "diff", "--name-only", base_sha, head_sha],
        check=True,
        capture_output=True,
        text=True,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def _starts_with_any(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path.startswith(prefix) for prefix in prefixes)


def is_economy_file(path: str) -> bool:
    return _starts_with_any(path, ECONOMY_PREFIXES)


def is_player_facing_file(path: str) -> bool:
    if path in HIGH_RISK_TECH_FILES or _starts_with_any(path, HIGH_RISK_TECH_PREFIXES):
        return False
    suffix = Path(path).suffix.lower()
    return _starts_with_any(path, PLAYER_PREFIXES) or suffix in PLAYER_EXTENSIONS


def is_high_risk_technical_file(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    if path in HIGH_RISK_TECH_FILES:
        return True
    if _starts_with_any(path, HIGH_RISK_TECH_PREFIXES):
        return True
    if suffix in HIGH_RISK_TECH_EXTENSIONS and not is_player_facing_file(path) and not is_economy_file(path):
        return True
    return False


def is_meaningful_runtime_file(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    return (
        is_economy_file(path)
        or is_player_facing_file(path)
        or is_high_risk_technical_file(path)
        or suffix in MEANINGFUL_RUNTIME_EXTENSIONS
    )


def required_policy(change_files: set[str]) -> dict[str, bool]:
    has_economy = any(is_economy_file(path) for path in change_files)
    has_player = any(is_player_facing_file(path) for path in change_files)
    has_high_risk_technical = any(is_high_risk_technical_file(path) for path in change_files)
    has_meaningful_runtime = any(is_meaningful_runtime_file(path) for path in change_files)
    return {
        "economy": has_economy,
        "player": has_player,
        "high_risk_technical": has_high_risk_technical,
        "meaningful_runtime": has_meaningful_runtime,
    }


def validate_change_class(change_class: str, change_files: set[str]) -> list[str]:
    errors: list[str] = []
    policy = required_policy(change_files)

    if change_class not in ALLOWED_CLASSES:
        return [f"Unknown Change class: {change_class!r}."]

    if policy["economy"] and change_class != "economy":
        errors.append(
            "Diff changes economy/progression files, so Change class must be `economy`."
        )
    elif policy["player"] and change_class not in {"player-facing", "economy"}:
        errors.append(
            "Diff changes player-facing/runtime presentation files, so Change class "
            "must be `player-facing` (or `economy` when economy files are also changed)."
        )
    elif policy["high_risk_technical"] and change_class != "technical":
        errors.append(
            "Diff changes high-risk technical/runtime files, so Change class must be `technical`."
        )

    if change_class == "trivial" and policy["meaningful_runtime"]:
        errors.append(
            "`trivial` cannot be used when runtime/gameplay/UI/economy/high-risk technical files change."
        )

    if change_class == "process" and policy["meaningful_runtime"]:
        errors.append(
            "`process` cannot be used to bypass evidence requirements for runtime/gameplay/UI/economy/high-risk technical changes."
        )

    return errors


def validate_acceptance_checkboxes(body: str, change_class: str) -> list[str]:
    if change_class == "trivial":
        return []
    errors: list[str] = []
    block = section_between(body, "## Acceptance criteria", "## Verification")
    rows = re.findall(r"^- \[([ xX])\]\s*(.*)$", block, flags=re.MULTILINE)
    substantive = [(state, text.strip()) for state, text in rows if text.strip()]
    if not substantive:
        return ["Acceptance criteria contain no substantive checklist item."]
    unchecked = [text for state, text in substantive if state == " "]
    if unchecked:
        errors.append(
            "All acceptance criteria must be checked before merge; unchecked: "
            + "; ".join(unchecked[:5])
        )
    return errors


def load_manifest(
    manifest_value: str,
    ticket: str,
    change_class: str,
    changed_files: set[str],
) -> tuple[dict | None, list[str], Path | None]:
    errors: list[str] = []
    if not manifest_value or manifest_value.upper().startswith("N/A"):
        return None, errors, None

    if not re.fullmatch(r"evidence/[A-Za-z0-9._-]+/manifest\.json", manifest_value):
        return None, ["Evidence manifest must use path evidence/<ticket>/manifest.json."], None

    path = Path(manifest_value)
    if not path.is_file():
        return None, [f"Evidence manifest does not exist in checkout: {manifest_value}"], path
    if changed_files and manifest_value not in changed_files:
        errors.append("Evidence manifest must be changed in the same PR.")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, errors + [f"Evidence manifest is unreadable/invalid JSON: {exc}"], path

    if data.get("schema_version") != 1:
        errors.append("Evidence manifest schema_version must be 1.")
    if data.get("ticket") != ticket:
        errors.append("Evidence manifest ticket must exactly match PR Ticket.")
    if data.get("change_class") != change_class:
        errors.append("Evidence manifest change_class must exactly match PR Change class.")

    return data, errors, path


def validate_common_manifest(data: dict) -> list[str]:
    errors: list[str] = []

    if not nonempty(data.get("problem")):
        errors.append("Evidence manifest problem must be non-empty.")

    decision = data.get("decision")
    if not isinstance(decision, dict):
        errors.append("Evidence manifest decision must be an object.")
        decision = {}

    if decision.get("provenance_type") not in ALLOWED_PROVENANCE:
        errors.append("decision.provenance_type is missing or invalid.")
    if decision.get("evidence_strength") not in ALLOWED_STRENGTH:
        errors.append("decision.evidence_strength is missing or invalid.")
    if not nonempty(decision.get("selected_alternative")):
        errors.append("decision.selected_alternative must be non-empty.")
    if not nonempty(decision.get("rationale")):
        errors.append("decision.rationale must be non-empty.")

    official_docs = data.get("official_docs")
    official_exception = data.get("official_docs_exception")
    if not isinstance(official_docs, list):
        official_docs = []
    if not official_docs and not nonempty(official_exception):
        errors.append("Evidence manifest needs official_docs or explicit official_docs_exception.")
    for index, doc in enumerate(official_docs, start=1):
        if not isinstance(doc, dict):
            errors.append(f"official_docs[{index}] must be an object.")
            continue
        if not valid_http_url(doc.get("source")):
            errors.append(f"official_docs[{index}].source must be an http(s) URL.")
        if not nonempty(doc.get("date_checked")):
            errors.append(f"official_docs[{index}].date_checked is missing.")
        if not nonempty(doc.get("verified_constraint")):
            errors.append(f"official_docs[{index}].verified_constraint is missing.")

    alternatives = data.get("alternatives")
    if not isinstance(alternatives, list) or len(alternatives) < 2:
        errors.append("Evidence manifest needs at least two credible alternatives.")
        alternatives = alternatives if isinstance(alternatives, list) else []

    selected_ids: list[str] = []
    for index, alt in enumerate(alternatives, start=1):
        if not isinstance(alt, dict):
            errors.append(f"alternatives[{index}] must be an object.")
            continue
        if not nonempty(alt.get("id")) or not nonempty(alt.get("reason")):
            errors.append(f"alternatives[{index}] needs id and reason.")
        if alt.get("disposition") not in {"selected", "rejected"}:
            errors.append(f"alternatives[{index}].disposition must be selected or rejected.")
        if alt.get("disposition") == "selected":
            selected_ids.append(str(alt.get("id")))

    if len(selected_ids) != 1:
        errors.append("Evidence manifest must contain exactly one selected alternative.")
    elif selected_ids[0] != decision.get("selected_alternative"):
        errors.append("Selected alternative must match decision.selected_alternative.")

    acceptance = data.get("acceptance_criteria")
    if not isinstance(acceptance, list) or len(acceptance) < 2:
        errors.append("Evidence manifest needs at least two acceptance criteria.")
        acceptance = acceptance if isinstance(acceptance, list) else []
    for index, criterion in enumerate(acceptance, start=1):
        if not isinstance(criterion, dict):
            errors.append(f"acceptance_criteria[{index}] must be an object.")
            continue
        if criterion.get("status") != "pass":
            errors.append(f"acceptance_criteria[{index}] is not pass.")
        if not nonempty(criterion.get("criterion")) or not nonempty(criterion.get("evidence")):
            errors.append(f"acceptance_criteria[{index}] needs criterion and evidence.")

    verification = data.get("verification")
    if not isinstance(verification, dict):
        errors.append("Evidence manifest verification must be an object.")
        verification = {}
    automated = verification.get("automated")
    manual = verification.get("manual")
    automated = automated if isinstance(automated, list) else []
    manual = manual if isinstance(manual, list) else []
    if not any(nonempty(item) for item in automated + manual):
        errors.append("Verification needs at least one substantive automated or manual result.")
    if not nonempty(verification.get("runtime_errors")):
        errors.append("verification.runtime_errors must state the checked result.")
    if not nonempty(verification.get("save_data_impact")):
        errors.append("verification.save_data_impact must be explicit.")

    return errors


def validate_unique_references(data: dict) -> list[str]:
    errors: list[str] = []
    research = data.get("research")
    if not isinstance(research, dict):
        return errors

    candidate_pool = research.get("candidate_pool")
    if isinstance(candidate_pool, list):
        urls = [
            item.get("source")
            for item in candidate_pool
            if isinstance(item, dict) and valid_http_url(item.get("source"))
        ]
        if len(urls) != len(set(urls)):
            errors.append("candidate_pool contains duplicate source URLs; filler duplicates are not allowed.")

    selected = research.get("selected_references")
    if isinstance(selected, list):
        urls = [
            item.get("source")
            for item in selected
            if isinstance(item, dict) and valid_http_url(item.get("source"))
        ]
        if len(urls) != len(set(urls)):
            errors.append("selected_references must use distinct source URLs.")

    return errors


def validate_visual_and_evaluation_provenance(data: dict, head_sha: str) -> list[str]:
    errors: list[str] = []

    visual = data.get("visual_evidence")
    if not isinstance(visual, dict):
        return ["Player-facing evidence requires visual_evidence object."]

    provenance = visual.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("visual_evidence.provenance is required.")
        provenance = {}
    if provenance.get("capture_commit_sha") not in {head_sha, PR_HEAD_BINDING}:
        errors.append(
            "visual_evidence.provenance.capture_commit_sha must equal exact PR HEAD_SHA "
            "or use the $PR_HEAD binding resolved by exact-head CI."
        )
    if provenance.get("capture_mode") not in {"ci", "local-reproducible"}:
        errors.append("visual_evidence.provenance.capture_mode must be `ci` or `local-reproducible`.")
    if not nonempty(provenance.get("artifact_locator")):
        errors.append("visual_evidence.provenance.artifact_locator must identify the retained evidence.")

    evaluation = data.get("evaluation")
    if not isinstance(evaluation, dict):
        return errors + ["Player-facing evidence requires evaluation object."]

    eval_prov = evaluation.get("provenance")
    if not isinstance(eval_prov, dict):
        errors.append("evaluation.provenance is required.")
        eval_prov = {}
    if eval_prov.get("evaluated_sha") not in {head_sha, PR_HEAD_BINDING}:
        errors.append(
            "evaluation.provenance.evaluated_sha must equal exact PR HEAD_SHA "
            "or use the $PR_HEAD binding resolved by exact-head CI."
        )
    evaluator = eval_prov.get("evaluator_id")
    implementer = eval_prov.get("implementation_author_id")
    if not nonempty(evaluator):
        errors.append("evaluation.provenance.evaluator_id is required.")
    if not nonempty(implementer):
        errors.append("evaluation.provenance.implementation_author_id is required.")
    if (
        evaluation.get("mode") == "independent_pass"
        and nonempty(evaluator)
        and nonempty(implementer)
        and evaluator == implementer
    ):
        errors.append("independent_pass evaluator_id must differ from implementation_author_id.")
    inputs = eval_prov.get("input_artifacts")
    if not isinstance(inputs, list) or not any(nonempty(item) for item in inputs):
        errors.append("evaluation.provenance.input_artifacts must identify evaluated evidence.")
    if not nonempty(eval_prov.get("record_locator")):
        errors.append("evaluation.provenance.record_locator must identify the retained evaluation record.")

    return errors


def validate_policy(
    *,
    body: str,
    changed_files: set[str],
    base_sha: str,
    head_sha: str,
) -> list[str]:
    errors: list[str] = []

    change_class = field_from_body(body, "Change class")
    ticket = field_from_body(body, "Ticket")
    manifest_value = field_from_body(body, "Evidence manifest")

    errors.extend(validate_change_class(change_class, changed_files))
    errors.extend(validate_acceptance_checkboxes(body, change_class))

    diff_policy = required_policy(changed_files)
    requires_manifest = (
        change_class in {"player-facing", "economy"}
        or (change_class == "technical" and diff_policy["high_risk_technical"])
    )

    if requires_manifest and (not manifest_value or manifest_value.upper().startswith("N/A")):
        if change_class == "technical":
            errors.append(
                "High-risk technical diff requires evidence/<ticket>/manifest.json; "
                "N/A is not allowed."
            )
        else:
            errors.append(f"{change_class} PR requires evidence/<ticket>/manifest.json.")
        return errors

    data, manifest_errors, _ = load_manifest(
        manifest_value, ticket, change_class, changed_files
    )
    errors.extend(manifest_errors)

    if data is not None:
        errors.extend(validate_common_manifest(data))

        if change_class in {"player-facing", "economy"}:
            errors.extend(validate_unique_references(data))

        needs_visual = change_class == "player-facing" or (
            change_class == "economy" and diff_policy["player"]
        )
        if needs_visual:
            errors.extend(validate_visual_and_evaluation_provenance(data, head_sha))

    return errors


def main() -> int:
    body = os.environ.get("PR_BODY", "")
    base_sha = os.environ.get("BASE_SHA", "").strip()
    head_sha = os.environ.get("HEAD_SHA", "").strip()

    try:
        changed_files = changed_files_from_git(base_sha, head_sha)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"PR evidence policy validation failed:\n\n- Could not determine changed files: {exc}")
        return 1

    errors = validate_policy(
        body=body,
        changed_files=changed_files,
        base_sha=base_sha,
        head_sha=head_sha,
    )

    if errors:
        print("PR evidence policy validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PR diff classification and evidence policy checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())