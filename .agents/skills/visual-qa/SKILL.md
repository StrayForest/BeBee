# Skill — Visual QA

Use for any player-facing change.

## Sequence

1. Read `docs/13-visual-qa-scorecard.md`.
2. Identify exact states that prove the feature.
3. Build the real HTML5 artifact.
4. Enter deterministic QA state when available.
5. Capture required desktop/mobile screenshots and motion evidence.
6. Inspect the captures at full size; do not trust intended layout.
7. Compare against researched references using objective metrics plus the scorecard.
8. Mark `PASS`, `PASS WITH DEVIATION`, or `ITERATE`.
9. If `ITERATE`, change the smallest likely cause, rebuild and recapture.
10. Attach evidence to the PR/CI artifact.

## Mandatory checks

- hierarchy;
- interaction count;
- state readability;
- reward/feedback timing;
- playfield obstruction;
- mobile layout when affected;
- BeBee originality;
- before/active/after states when applicable.

A rendered feature without inspected evidence is incomplete.
