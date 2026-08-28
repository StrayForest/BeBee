## Problem / outcome

- Ticket:
- Change class: `player-facing` / `economy` / `technical` / `process` / `trivial`
- Evidence manifest: `evidence/<ticket>/manifest.json` or `N/A — <reason>`
- Player/system problem:
- Intended observable outcome:
- Out of scope:

> The declared change class is not authoritative by itself. CI compares it with the actual PR diff. Player-facing/economy files cannot be downgraded to `technical`, `process` or `trivial`, and high-risk technical runtime changes require a same-PR evidence manifest.

## Decision status / provenance

Relevant `DECISIONS.md` IDs:

- Decision(s):
- Status before PR:
- Status after PR:
- Provenance type: `OWNER_CONSTRAINT` / `REFERENCE_PATTERN` / `TECH_CONSTRAINT` / `EXPERIMENT_RESULT` / `SIMULATION_RESULT` / `TELEMETRY_RESULT` / `PLAYTEST_RESULT` / `SUBJECTIVE_DIRECTION` / `N/A — <reason>`
- Evidence strength: `LOW` / `MEDIUM` / `HIGH` / `N/A — <reason>`
- [ ] `DECISIONS.md` updated if a status/LOCKED decision changed

## Research gate

### Reference candidate pool

For substantial player-facing/economy work, the machine-readable manifest is authoritative. Summarize the search here.

- Candidate count:
- Selected deep references:
- Materially different solution / anti-pattern:
- Candidate-pool exception if fewer than five reasonable candidates exist:

Candidate and selected-reference source URLs must be distinct; repeating the same source to satisfy a count is not valid evidence.

### Comparable shipped references

For player-facing/economy work, list at least two relevant problem-specific references when reasonably available.

- Reference 1:
  - source/platform/date:
  - why selected:
  - directly observed pattern:
  - inference (separate from observation):
  - measurable notes:
- Reference 2:
  - source/platform/date:
  - why selected:
  - directly observed pattern:
  - inference (separate from observation):
  - measurable notes:

If reference research is not applicable, explain why:

### Official technical documentation

List current official Defold/platform/library/tool docs consulted.

- Official doc 1:
- Official doc 2:
- Important API/constraints:
- Error/lifecycle cases considered:

If official-doc research is not applicable, explain why:

For high-risk technical runtime work, official-document constraints, alternatives, acceptance criteria and verification must also be recorded in the same-PR evidence manifest. Competitor research may be explicitly N/A where it does not apply.

## Alternatives / BeBee decision

- Alternatives considered:
- Selected alternative:
- Rejected alternative(s) and why:
- Pattern adopted:
- Intentional deviations:
- Why this fits BeBee:
- What proprietary expression/assets/code were explicitly not copied:

## Implementation impact

- Behavior/code:
- Data/content:
- Save/migration/storage:
- Analytics:
- Platform/SDK:
- Accessibility/input:
- Performance/load:

## Acceptance criteria

All non-trivial criteria must be checked before merge. Do not leave an unmet criterion unchecked and still mark the PR ready.

- [ ]
- [ ]
- [ ]

## Verification

- [ ] relevant unit/integration tests pass
- [ ] data validation passes where relevant
- [ ] HTML5 build succeeds
- [ ] keyboard path checked where relevant
- [ ] touch path checked where relevant
- [ ] save/reload/storage lifecycle checked where relevant
- [ ] economy simulation checked where relevant
- [ ] selected portal/device case checked where relevant
- [ ] no new runtime/console errors

Commands/builds/artifacts:

```text

```

## Visual QA

Required for player-facing changes. Follow `docs/13-visual-qa-scorecard.md`.

### Evidence

- [ ] idle/before state
- [ ] active/interacting state
- [ ] completed/reward state
- [ ] locked/blocked state where relevant
- [ ] dense/worst case where relevant
- [ ] desktop layout checked
- [ ] affected mobile/portal layout checked
- [ ] video/frame sequence attached for motion/timing when relevant

Evidence links/artifacts:

For structured player-facing evidence, record exact-head provenance in the manifest:

- `visual_evidence.provenance.capture_commit_sha` = exact PR head SHA
- `visual_evidence.provenance.capture_mode` = `ci` or `local-reproducible`
- `visual_evidence.provenance.artifact_locator` = retained evidence locator

Once P0 deterministic capture exists, CI artifact existence/hash verification replaces declaration-only artifact trust.

### Objective measurements first

Record applicable measured/observed values before subjective scores.

- actions/taps/clicks to result:
- feedback latency:
- completion/stationary wait time:
- persistent HUD count:
- instruction lines:
- playfield obstruction / modal depth:
- touch-control count / target size:

### Comparison scorecard

| Criterion | Reference A | Reference B | BeBee | Finding |
|---|---:|---:|---:|---|
| Actions to result | | | | |
| Time to first feedback | | | | |
| Persistent HUD count | | | | |
| Objective clarity (1–5 + note) | | | | |
| State readability (1–5 + note) | | | | |
| Feedback quality (1–5 + note) | | | | |
| Mobile comfort (1–5 + note) | | | | |
| Original BeBee expression (1–5 + note) | n/a | n/a | | |

Comparison conclusion:

- [ ] PASS
- [ ] PASS WITH DEVIATION — explained below
- [ ] ITERATE — not ready to merge

Deviation/iteration notes:

If visual QA is not applicable, explain why:

## Independent evaluation

Required for substantial player-facing work after rendered evidence exists.

- Evaluation mode: `independent_pass` / `human` / `N/A — <reason>`
- Review inputs: problem + acceptance criteria + reference observations + BeBee rendered evidence + measurements
- Findings:
- Evaluator verdict: `PASS` / `PASS WITH DEVIATION` / `ITERATE` / `N/A — <reason>`
- [ ] implementation iterated after evaluator findings where required

For `independent_pass`, the manifest must bind the evaluation to the exact PR head and identify a separate evaluator:

- `evaluation.provenance.evaluated_sha`
- `evaluation.provenance.evaluator_id`
- `evaluation.provenance.implementation_author_id`
- `evaluation.provenance.input_artifacts`
- `evaluation.provenance.record_locator`

`evaluator_id` must differ from `implementation_author_id` for `independent_pass`.

## Human milestone gate

Required at the ends of P2, P4 and P6.

- [ ] not a P2/P4/P6 subjective milestone gate
- [ ] designated human approval recorded

Approval/evidence:

## License / provenance

- [ ] no competitor proprietary assets/code were copied
- [ ] any new third-party dependency/asset has a compatible reviewed license
- [ ] `THIRD_PARTY.md` updated when required

## Known limitations / follow-ups

- None, or:
