# Skill — Visual QA

Use for any player-facing change.

## Sequence

1. Read `docs/13-visual-qa-scorecard.md` and `docs/15-agent-evidence-governance.md`.
2. Identify exact states that prove the feature.
3. Define observable measurements before assigning subjective scores.
4. Build the real HTML5 artifact.
5. Enter deterministic QA state when available.
6. Capture required desktop/mobile screenshots and motion evidence.
7. Inspect the captures at full size; do not trust intended layout.
8. Compare against researched references using objective metrics first, then anchored subjective scores.
9. Run a separate evaluation pass for substantial player-facing work using primarily the problem, acceptance criteria, reference observations, rendered evidence and measurements.
10. Mark `PASS`, `PASS WITH DEVIATION`, or `ITERATE` from the evaluation result.
11. If `ITERATE`, change the smallest likely cause, rebuild and recapture.
12. Attach evidence to the PR/CI artifact and record it in `evidence/<ticket>/manifest.json` when required.

## Mandatory checks

- hierarchy;
- interaction count;
- state readability;
- reward/feedback timing;
- stationary waiting where relevant;
- playfield obstruction;
- mobile layout when affected;
- BeBee originality;
- before/active/after states when applicable.

## Evaluation discipline

- Measure first, judge second.
- Every subjective score requires a concrete note.
- Do not use the implementer's intent as evidence that the rendered result succeeds.
- Do not mark `PASS` merely because the implementation matches the plan.
- A meaningful gap against the target problem is `ITERATE`, even if the code is technically correct.

A rendered feature without inspected evidence is incomplete.
