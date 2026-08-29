#!/usr/bin/env python3
"""Compatibility wrapper fixing mixed player-facing/high-risk classification precedence.

The trusted base policy already defines the intended precedence as economy ->
player-facing -> technical, but its chained condition can fall through when the
selected player-facing class is valid and then reject the same diff as technical.
This wrapper reuses every existing evidence check and replaces only that classifier.
"""

from __future__ import annotations

import check_pr_evidence_policy as policy


def validate_change_class(change_class: str, change_files: set[str]) -> list[str]:
    errors: list[str] = []
    required = policy.required_policy(change_files)

    if change_class not in policy.ALLOWED_CLASSES:
        return [f"Unknown Change class: {change_class!r}."]

    if required["economy"]:
        if change_class != "economy":
            errors.append(
                "Diff changes economy/progression files, so Change class must be `economy`."
            )
    elif required["player"]:
        if change_class != "player-facing":
            errors.append(
                "Diff changes player-facing/runtime presentation files, so Change class "
                "must be `player-facing` (or `economy` when economy files are also changed)."
            )
    elif required["high_risk_technical"]:
        if change_class != "technical":
            errors.append(
                "Diff changes high-risk technical/runtime files, so Change class must be `technical`."
            )

    if change_class == "trivial" and required["meaningful_runtime"]:
        errors.append(
            "`trivial` cannot be used when runtime/gameplay/UI/economy/high-risk technical files change."
        )

    if change_class == "process" and required["meaningful_runtime"]:
        errors.append(
            "`process` cannot be used to bypass evidence requirements for runtime/gameplay/UI/economy/high-risk technical changes."
        )

    return errors


policy.validate_change_class = validate_change_class


if __name__ == "__main__":
    raise SystemExit(policy.main())
