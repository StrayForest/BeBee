#!/usr/bin/env python3
"""Validate that BeBee PRs contain the minimum research/verification evidence.

This is intentionally a structural gate, not a substitute for human/product review.
Docs/trivial PRs may use explicit N/A explanations, but may not leave required sections blank.
"""

from __future__ import annotations

import os
import re
import sys

body = os.environ.get("PR_BODY", "")

required_headings = [
    "## Problem / outcome",
    "## Decision status",
    "## Research gate",
    "## BeBee decision",
    "## Acceptance criteria",
    "## Verification",
    "## Visual QA",
    "## License / provenance",
    "## Known limitations / follow-ups",
]

errors: list[str] = []

if not body.strip():
    errors.append("PR body is empty.")

for heading in required_headings:
    if heading not in body:
        errors.append(f"Missing required heading: {heading}")

# Prevent the explicit not-ready state from being selected.
if re.search(r"- \[x\]\s+ITERATE", body, flags=re.IGNORECASE):
    errors.append("Visual comparison is marked ITERATE; PR is not merge-ready.")

# Require either references or an explicit applicability explanation.
reference_block = re.search(
    r"### Comparable shipped references(?P<block>.*?)(?:### Official technical documentation)",
    body,
    flags=re.DOTALL,
)
if reference_block:
    block = reference_block.group("block")
    has_ref = bool(re.search(r"source/platform/date:\s*\S", block, flags=re.IGNORECASE))
    has_na = bool(re.search(r"not applicable.*\S", block, flags=re.IGNORECASE | re.DOTALL))
    if not (has_ref or has_na):
        errors.append("Competitor/reference research is blank and no explicit N/A explanation is present.")

# Require official docs or an explicit N/A explanation.
official_block = re.search(
    r"### Official technical documentation(?P<block>.*?)(?:## BeBee decision)",
    body,
    flags=re.DOTALL,
)
if official_block:
    block = official_block.group("block")
    has_doc = bool(re.search(r"Official doc 1:\s*\S", block, flags=re.IGNORECASE))
    has_na = bool(re.search(r"not applicable.*\S", block, flags=re.IGNORECASE | re.DOTALL))
    if not (has_doc or has_na):
        errors.append("Official documentation research is blank and no explicit N/A explanation is present.")

# Acceptance criteria should contain at least one completed or intentionally pending checkbox line.
criteria_block = re.search(
    r"## Acceptance criteria(?P<block>.*?)(?:## Verification)", body, flags=re.DOTALL
)
if criteria_block and not re.search(r"- \[[ xX]\]\s+\S", criteria_block.group("block")):
    errors.append("Acceptance criteria contain no substantive checklist item.")

if errors:
    print("PR evidence validation failed:\n")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PR evidence structure looks valid.")
