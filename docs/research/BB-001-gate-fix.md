# BB-001 gate repair

Date checked: 2026-08-28

## Problem

P-1 hardening left two contradictory constraints that first became operational blockers at BB-001:

1. a committed evidence manifest was required to contain the exact final PR-head SHA, although that SHA depends on the committed manifest content itself;
2. generic Defold resource extensions such as `.collection` could force technical bootstrap resources into `player-facing` classification even when they lived under an explicitly high-risk technical architecture prefix.

The first condition is self-referential. Git objects are content-addressed, so changing tracked content changes the resulting object identity. The second condition conflates runtime architecture with player-visible presentation.

## Selected repair

- Allow the literal `$PR_HEAD` in committed visual/evaluation provenance fields. Trusted CI resolves it against the concrete pull-request head and exact-head artifacts retain the actual SHA.
- Keep arbitrary literal SHA values invalid unless they equal the concrete head.
- Give explicit high-risk technical files/prefixes precedence over generic player-facing resource extensions.
- Place BB-001 bootstrap runtime under `app/`, matching the existing long-lived application-layer architecture.
- Extend the read-only Defold runtime evidence workflow to `app/**`.

## Rejected alternatives

- Disable visual/evidence policy for bootstrap work: rejected because it weakens governance rather than fixing contradictory rules.
- Keep all `.collection`/`.script` resources player-facing globally: rejected because technical lifecycle resources can legitimately use those Defold formats.
- Hard-code a previously known commit SHA in the manifest: rejected because it would not bind the evidence to the final candidate head.

## Verification strategy

The governance PR adds regression tests for `$PR_HEAD` and technical bootstrap classification. Because the trusted `pull_request_target` workflow intentionally executes policy/tests from the PR base, those new tests become authoritative only after this repair is merged. The immediately following BB-001 PR therefore serves as the first trusted-base execution of the repaired test suite.
