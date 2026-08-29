#!/usr/bin/env python3
"""Trusted-boundary compatibility wrapper for DECISIONS.md updates.

DECISIONS.md is governance-protected and must retain same-PR manifest/governance
evidence, but updating the decision registry is also mandatory for substantive
player-facing/technical decisions. A DECISIONS-only governance touch therefore
must not force an otherwise valid feature PR to declare itself process.
"""

from __future__ import annotations

import check_trust_boundary as policy

PROCESS_ONLY_ERROR = "Governance-critical files must use Change class `process`."
_BASE_VALIDATE = policy.validate


def validate(*, body: str, changed_files: set[str]) -> list[str]:
    errors = _BASE_VALIDATE(body=body, changed_files=changed_files)
    governance_files = {path for path in changed_files if policy.is_governance(path)}
    change_class = policy.field_from_body(body, "Change class")

    if governance_files == {"DECISIONS.md"} and change_class in {
        "player-facing",
        "economy",
        "technical",
    }:
        errors = [error for error in errors if error != PROCESS_ONLY_ERROR]

    return errors


policy.validate = validate


if __name__ == "__main__":
    raise SystemExit(policy.main())
