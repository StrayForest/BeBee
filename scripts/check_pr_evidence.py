#!/usr/bin/env python3
"""Validate BeBee PR evidence and structured feature manifests.

This gate intentionally checks more than PR headings. For substantial player-facing
and economy work, the PR must point to a machine-readable evidence manifest that is
changed in the same PR and contains the minimum research/decision/evaluation record.

The gate cannot prove observations are truthful; it makes omissions, self-contradiction
and unsupported process shortcuts harder and leaves evidence auditable.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


body = os.environ.get("PR_BODY", "")
base_sha = os.environ.get("BASE_SHA", "").strip()
head_sha = os.environ.get("HEAD_SHA", "").strip()

required_headings = [
    "## Problem / outcome",
    "## Decision status / provenance",
    "## Research gate",
    "## Alternatives / BeBee decision",
    "## Acceptance criteria",
    "## Verification",
    "## Visual QA",
    "## Independent evaluation",
    "## License / provenance",
    "## Known limitations / follow-ups",
]

allowed_change_classes = {"player-facing", "economy", "technical", "process", "trivial"}
allowed_statuses = {"LOCKED", "VALIDATED", "HYPOTHESIS", "OPEN", "DEPRECATED"}
allowed_provenance = {
    "OWNER_CONSTRAINT",
    "REFERENCE_PATTERN",
    "TECH_CONSTRAINT",
    "EXPERIMENT_RESULT",
    "SIMULATION_RESULT",
    "TELEMETRY_RESULT",
    "PLAYTEST_RESULT",
    "SUBJECTIVE_DIRECTION",
}
allowed_strength = {"LOW", "MEDIUM", "HIGH"}
allowed_verdicts = {"PASS", "PASS WITH DEVIATION"}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def field_from_body(label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+?)\s*$", body, flags=re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip()
    if value.startswith("`") and value.endswith("`") and value.count("`") == 2:
        value = value[1:-1].strip()
    return value


def section_between(start: str, end: str) -> str:
    match = re.search(
        rf"{re.escape(start)}(?P<block>.*?){re.escape(end)}",
        body,
        flags=re.DOTALL,
    )
    return match.group("block") if match else ""


def changed_files() -> set[str]:
    if not base_sha or not head_sha:
        return set()
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", base_sha, head_sha],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"Could not determine files changed in PR: {exc}")
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


if not body.strip():
    fail("PR body is empty.")

for heading in required_headings:
    if heading not in body:
        fail(f"Missing required heading: {heading}")

# Reject untouched template option lists rather than silently choosing the first option.
change_class = field_from_body("Change class")
if not change_class:
    fail("Missing Change class.")
elif "/" in change_class or change_class not in allowed_change_classes:
    fail(
        "Change class must be exactly one of: "
        + ", ".join(sorted(allowed_change_classes))
        + "."
    )

ticket = field_from_body("Ticket")
if not ticket or ticket.startswith("<"):
    fail("Ticket must be filled with a concrete ticket/identifier.")

# Acceptance criteria must contain substantive items and may not retain blank template rows.
criteria_block = section_between("## Acceptance criteria", "## Verification")
criteria = re.findall(r"^- \[([ xX])\]\s*(.*)$", criteria_block, flags=re.MULTILINE)
substantive_criteria = [(state, text.strip()) for state, text in criteria if text.strip()]
if not substantive_criteria:
    fail("Acceptance criteria contain no substantive checklist item.")
if any(not text for _, text in criteria):
    fail("Acceptance criteria still contain blank template checklist items.")

# An explicit ITERATE conclusion is never merge-ready.
if re.search(r"^- \[[xX]\]\s+ITERATE\b", body, flags=re.MULTILINE | re.IGNORECASE):
    fail("Visual comparison is marked ITERATE; PR is not merge-ready.")

# Require a determinate comparison conclusion for non-trivial work, even when visual QA is N/A.
if change_class and change_class != "trivial":
    conclusion_block = section_between("Comparison conclusion:", "Deviation/iteration notes:")
    checked = re.findall(
        r"^- \[[xX]\]\s+(PASS WITH DEVIATION|PASS|ITERATE)\b",
        conclusion_block,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    if len(checked) != 1:
        fail("Select exactly one comparison conclusion: PASS, PASS WITH DEVIATION, or ITERATE.")

# Official technical research remains required or must be explicitly inapplicable.
official_block = section_between(
    "### Official technical documentation", "## Alternatives / BeBee decision"
)
if official_block:
    has_doc = bool(re.search(r"^- Official doc 1:\s*\S", official_block, flags=re.MULTILINE))
    has_na = bool(
        re.search(
            r"If official-doc research is not applicable, explain why:\s*\S",
            official_block,
            flags=re.IGNORECASE | re.DOTALL,
        )
    )
    if not (has_doc or has_na):
        fail("Official documentation research is blank and no explicit N/A explanation is present.")

manifest_value = field_from_body("Evidence manifest")
manifest_required = change_class in {"player-facing", "economy"}
manifest_path: Path | None = None

if manifest_required:
    if not manifest_value or manifest_value.upper().startswith("N/A"):
        fail("Player-facing/economy PRs require an evidence/<ticket>/manifest.json file.")
    elif not re.fullmatch(r"evidence/[A-Za-z0-9._-]+/manifest\.json", manifest_value):
        fail("Evidence manifest must use path evidence/<ticket>/manifest.json.")
    else:
        manifest_path = Path(manifest_value)
        if not manifest_path.is_file():
            fail(f"Evidence manifest does not exist in checkout: {manifest_value}")
        changed = changed_files()
        if changed and manifest_value not in changed:
            fail("Evidence manifest must be changed in the same PR as the feature/economy work.")
else:
    if not manifest_value:
        fail("Evidence manifest must be a path or an explicit N/A — reason.")
    elif manifest_value.upper().startswith("N/A") and len(manifest_value.split("—", 1)) < 2 and len(manifest_value.split("-", 1)) < 2:
        fail("Evidence manifest N/A must include a reason.")


def validate_manifest(path: Path) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Evidence manifest is unreadable/invalid JSON: {exc}")
        return

    if data.get("schema_version") != 1:
        fail("Evidence manifest schema_version must be 1.")
    if data.get("ticket") != ticket:
        fail("Evidence manifest ticket must exactly match PR Ticket.")
    if data.get("change_class") != change_class:
        fail("Evidence manifest change_class must exactly match PR Change class.")
    if not nonempty(data.get("problem")):
        fail("Evidence manifest problem must be non-empty.")

    decision = data.get("decision")
    if not isinstance(decision, dict):
        fail("Evidence manifest decision must be an object.")
        decision = {}

    if decision.get("status_before") not in allowed_statuses:
        fail("decision.status_before is missing or invalid.")
    if decision.get("status_after") not in allowed_statuses:
        fail("decision.status_after is missing or invalid.")
    if decision.get("provenance_type") not in allowed_provenance:
        fail("decision.provenance_type is missing or invalid.")
    if decision.get("evidence_strength") not in allowed_strength:
        fail("decision.evidence_strength is missing or invalid.")
    if not nonempty(decision.get("selected_alternative")):
        fail("decision.selected_alternative must be non-empty.")
    if not nonempty(decision.get("rationale")):
        fail("decision.rationale must be non-empty.")

    research = data.get("research")
    if not isinstance(research, dict):
        fail("Evidence manifest research must be an object.")
        research = {}

    candidate_pool = research.get("candidate_pool")
    candidate_exception = research.get("candidate_pool_exception")
    if not isinstance(candidate_pool, list):
        candidate_pool = []
    if len(candidate_pool) < 5 and not nonempty(candidate_exception):
        fail("Research candidate_pool needs at least five candidates or an explicit exception.")
    for index, candidate in enumerate(candidate_pool, start=1):
        if not isinstance(candidate, dict):
            fail(f"candidate_pool[{index}] must be an object.")
            continue
        if not nonempty(candidate.get("name")):
            fail(f"candidate_pool[{index}].name is missing.")
        if not valid_http_url(candidate.get("source")):
            fail(f"candidate_pool[{index}].source must be an http(s) URL.")
        if not nonempty(candidate.get("relevance")):
            fail(f"candidate_pool[{index}].relevance is missing.")

    selected_refs = research.get("selected_references")
    reference_exception = research.get("reference_exception")
    if not isinstance(selected_refs, list):
        selected_refs = []
    if len(selected_refs) < 2 and not nonempty(reference_exception):
        fail("Research needs at least two selected references or an explicit exception.")
    for index, ref in enumerate(selected_refs, start=1):
        if not isinstance(ref, dict):
            fail(f"selected_references[{index}] must be an object.")
            continue
        for key in ("name", "platform_version_date", "selection_reason", "observed_behavior"):
            if not nonempty(ref.get(key)):
                fail(f"selected_references[{index}].{key} is missing.")
        if not valid_http_url(ref.get("source")):
            fail(f"selected_references[{index}].source must be an http(s) URL.")
        if "inference" not in ref:
            fail(f"selected_references[{index}] must explicitly separate inference from observation.")
        if not isinstance(ref.get("measurements"), dict):
            fail(f"selected_references[{index}].measurements must be an object (may be empty when unobservable).")

    anti_pattern = research.get("anti_pattern")
    if not isinstance(anti_pattern, dict):
        fail("research.anti_pattern must record a materially different solution/failure mode.")
    else:
        if not valid_http_url(anti_pattern.get("source")):
            fail("research.anti_pattern.source must be an http(s) URL.")
        if not nonempty(anti_pattern.get("observation")) or not nonempty(anti_pattern.get("lesson")):
            fail("research.anti_pattern needs observation and lesson.")

    official_docs = data.get("official_docs")
    official_exception = data.get("official_docs_exception")
    if not isinstance(official_docs, list):
        official_docs = []
    if not official_docs and not nonempty(official_exception):
        fail("Evidence manifest needs official_docs or an explicit official_docs_exception.")
    for index, doc in enumerate(official_docs, start=1):
        if not isinstance(doc, dict):
            fail(f"official_docs[{index}] must be an object.")
            continue
        if not valid_http_url(doc.get("source")):
            fail(f"official_docs[{index}].source must be an http(s) URL.")
        if not nonempty(doc.get("date_checked")) or not nonempty(doc.get("verified_constraint")):
            fail(f"official_docs[{index}] needs date_checked and verified_constraint.")

    alternatives = data.get("alternatives")
    if not isinstance(alternatives, list) or len(alternatives) < 2:
        fail("Evidence manifest needs at least two credible alternatives.")
        alternatives = alternatives if isinstance(alternatives, list) else []

    selected = []
    for index, alternative in enumerate(alternatives, start=1):
        if not isinstance(alternative, dict):
            fail(f"alternatives[{index}] must be an object.")
            continue
        if not nonempty(alternative.get("id")) or not nonempty(alternative.get("reason")):
            fail(f"alternatives[{index}] needs id and reason.")
        disposition = alternative.get("disposition")
        if disposition not in {"selected", "rejected"}:
            fail(f"alternatives[{index}].disposition must be selected or rejected.")
        if disposition == "selected":
            selected.append(alternative.get("id"))
    if len(selected) != 1:
        fail("Evidence manifest must contain exactly one selected alternative.")
    elif selected[0] != decision.get("selected_alternative"):
        fail("Selected alternative must match decision.selected_alternative.")

    acceptance = data.get("acceptance_criteria")
    if not isinstance(acceptance, list) or len(acceptance) < 2:
        fail("Evidence manifest needs at least two acceptance criteria.")
        acceptance = acceptance if isinstance(acceptance, list) else []
    for index, criterion in enumerate(acceptance, start=1):
        if not isinstance(criterion, dict):
            fail(f"acceptance_criteria[{index}] must be an object.")
            continue
        if not nonempty(criterion.get("criterion")) or not nonempty(criterion.get("evidence")):
            fail(f"acceptance_criteria[{index}] needs criterion and evidence.")
        if criterion.get("status") != "pass":
            fail(f"acceptance_criteria[{index}] is not pass; PR is not merge-ready.")

    verification = data.get("verification")
    if not isinstance(verification, dict):
        fail("Evidence manifest verification must be an object.")
        verification = {}
    automated = verification.get("automated")
    manual = verification.get("manual")
    if not isinstance(automated, list):
        automated = []
    if not isinstance(manual, list):
        manual = []
    if not any(nonempty(item) for item in automated + manual):
        fail("Verification needs at least one substantive automated or manual result.")
    if not nonempty(verification.get("runtime_errors")):
        fail("verification.runtime_errors must state the checked result.")
    if not nonempty(verification.get("save_data_impact")):
        fail("verification.save_data_impact must be explicit, including 'none' where applicable.")

    if change_class == "player-facing":
        visual = data.get("visual_evidence")
        if not isinstance(visual, dict):
            fail("Player-facing manifest requires visual_evidence object.")
            visual = {}
        if visual.get("required") is not True:
            fail("Player-facing visual_evidence.required must be true.")
        for key in ("artifacts", "states", "viewports"):
            value = visual.get(key)
            if not isinstance(value, list) or not any(nonempty(item) for item in value):
                fail(f"Player-facing visual_evidence.{key} must contain evidence.")

        comparison = data.get("comparison")
        if not isinstance(comparison, dict):
            fail("Player-facing manifest requires comparison object.")
            comparison = {}
        measurements = comparison.get("measurements")
        if not isinstance(measurements, dict) or not measurements:
            fail("Player-facing comparison.measurements must contain observable values where the feature is evaluated.")

        evaluation = data.get("evaluation")
        if not isinstance(evaluation, dict):
            fail("Player-facing manifest requires separate evaluation object.")
            evaluation = {}
        if evaluation.get("mode") not in {"independent_pass", "human"}:
            fail("evaluation.mode must be independent_pass or human for player-facing work.")
        if evaluation.get("verdict") not in allowed_verdicts:
            fail("evaluation.verdict must be PASS or PASS WITH DEVIATION; ITERATE is not merge-ready.")
        findings = evaluation.get("findings")
        if not isinstance(findings, list) or not any(nonempty(item) for item in findings):
            fail("evaluation.findings must contain the evaluator finding or explicit 'none'.")
        if evaluation.get("iteration_required") is not False:
            fail("evaluation.iteration_required must be false before merge.")


if manifest_path and manifest_path.is_file():
    validate_manifest(manifest_path)

if errors:
    print("PR evidence validation failed:\n")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PR evidence and structured evidence checks passed.")
