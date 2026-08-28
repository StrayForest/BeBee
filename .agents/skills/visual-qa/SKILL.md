# Skill — Visual QA

Use for any player-facing change.

## Sequence

1. Read `docs/13-visual-qa-scorecard.md`, `docs/17-visual-style-bible.md` and `docs/15-agent-evidence-governance.md`.
2. Treat `config/visual-style.json` as the canonical numeric V-001 token source; generic older viewport/style examples never override it.
3. Identify exact states that prove the feature.
4. Define observable measurements before assigning subjective scores.
5. Build the real HTML5 artifact.
6. Enter deterministic QA state when available.
7. Capture required desktop/mobile screenshots and motion evidence, including the V-001/Poki scale cases affected by the change.
8. Inspect the captures at full size; do not trust intended layout.
9. Compare against researched references using objective metrics first, then anchored subjective scores.
10. Run a separate evaluation pass for substantial player-facing work using primarily the problem, acceptance criteria, reference observations, rendered evidence and measurements.
11. Mark `PASS`, `PASS WITH DEVIATION`, or `ITERATE` from the evaluation result.
12. If `ITERATE`, change the smallest likely cause, rebuild and recapture.
13. Attach evidence to the PR/CI artifact and record it in `evidence/<ticket>/manifest.json` when required.

## Mandatory checks

- hierarchy;
- interaction count;
- state readability;
- reward/feedback timing;
- stationary waiting where relevant;
- playfield obstruction;
- V-001 bee/camera/UI/VFX token compliance or an explicit evidence-backed deviation;
- 16:9 portal scale/crop safety where gameplay composition is affected;
- mobile layout when affected;
- BeBee originality;
- before/active/after states when applicable.

## Evaluation discipline

- Measure first, judge second.
- Every subjective score requires a concrete note.
- Do not use the implementer's intent as evidence that the rendered result succeeds.
- Do not mark `PASS` merely because the implementation matches the plan.
- A meaningful gap against the target problem is `ITERATE`, even if the code is technically correct.
- Once P0/BB-P008 runtime capture exists, its exact-build screenshots outrank BB-P007 primitive blocking frames; the blocking frames remain composition intent, not golden production art.

A rendered feature without inspected evidence is incomplete.
