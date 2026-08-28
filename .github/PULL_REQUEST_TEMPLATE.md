## Problem / outcome

- Ticket:
- Change class: `player-facing` / `economy` / `technical` / `process` / `trivial`
- Evidence manifest: `evidence/<ticket>/manifest.json` or `N/A — <reason>`
- Milestone gate: `none` / `P2` / `P4` / `P6`
- Player/system problem:
- Intended observable outcome:
- Out of scope:

> CI does not trust the declared class alone. Runtime/data paths are classified from the actual diff.
> Governance-critical files require a same-PR evidence manifest and are judged by policy from the trusted base branch.
> A second GitHub reviewer is not required by default.

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

For substantial player-facing/economy work, the manifest is authoritative.

- Candidate count:
- Selected deep references:
- Materially different solution / anti-pattern:
- Candidate-pool exception if fewer than five reasonable candidates exist:

Each candidate/reference in the manifest must identify the actual shipped product with a stable `product_id`.
Different URLs/pages for the same game do not count as independent products.

### Comparable shipped references

- Reference 1:
  - product:
  - source/platform/date:
  - why selected:
  - directly observed pattern:
  - inference:
  - measurable notes:
- Reference 2:
  - product:
  - source/platform/date:
  - why selected:
  - directly observed pattern:
  - inference:
  - measurable notes:

If reference research is not applicable, explain why:

### Official technical documentation

- Official doc 1:
- Official doc 2:
- Important API/constraints:
- Error/lifecycle cases considered:

If official-doc research is not applicable, explain why:

> The N/A explanation must be on this same line. A blank field is not accepted merely because later prose exists.

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

For governance-critical changes, the manifest must also contain:

```text
governance.trust_boundary_change
governance.bypass_analysis
governance.rollback
```

## Acceptance criteria

All non-trivial criteria must be checked before merge.

- [ ]
- [ ]
- [ ]

## Verification

- [ ] relevant unit/integration tests pass
- [ ] data validation passes where relevant
- [ ] HTML5 build succeeds where relevant
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

Required for player-facing changes.

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

### Objective measurements first

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
- Review inputs:
- Findings:
- Evaluator verdict: `PASS` / `PASS WITH DEVIATION` / `ITERATE` / `N/A — <reason>`
- [ ] implementation iterated after evaluator findings where required

## Milestone checkpoint

- Milestone declared above: `none` / `P2` / `P4` / `P6`
- Evidence package complete for the declared milestone: `yes` / `no` / `N/A`
- Optional owner/human review requested: `yes` / `no`

P2/P4/P6 are stronger evidence checkpoints, but CI does not require a second GitHub account. `ITERATE`, missing evidence, or failed acceptance criteria still blocks progress.

## License / provenance

- [ ] no competitor proprietary assets/code were copied
- [ ] any new third-party dependency/asset has a compatible reviewed license
- [ ] `THIRD_PARTY.md` updated when required

## Known limitations / follow-ups

- None, or:
