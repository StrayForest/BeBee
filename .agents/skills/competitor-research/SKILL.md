# Skill — Competitor Research

Use for player-facing gameplay, UX/UI, progression, art/VFX and onboarding work.

## Required sequence

1. Restate the exact player problem before searching.
2. Read `DECISIONS.md`, `docs/15-agent-evidence-governance.md` and the relevant BeBee domain doc.
3. Build a candidate pool of at least five plausible shipped references when reasonably available.
4. Select at least two references for deep observation; prefer references that solve the exact problem and do not over-index on one developer.
5. Include at least one materially different solution or anti-pattern.
6. Record why each deep reference was selected and why notable candidates were rejected or considered less relevant.
7. Observe the exact state/flow, not only store descriptions.
8. Record source/platform/date and what is directly observed vs inferred.
9. Measure where possible: actions, timing, stationary waiting, HUD count, blocked state, reward timing, mobile behavior, modal depth.
10. Identify the transferable pattern and the proprietary expression that must not be copied.
11. Produce alternatives, a recommendation and unresolved questions before implementation.
12. Feed the result into `docs/templates/feature-research.md` and, for substantial work, `evidence/<ticket>/manifest.json`.

If five reasonable candidate references cannot be found, record an explicit candidate-pool exception and the search limitation rather than inventing filler references.

## Do not

- copy maps, art, sounds, text, proprietary code or exact distinctive layouts;
- treat popularity as proof that every feature is good;
- select only references that confirm the initially preferred solution;
- use open-source architecture as visual/UX authority;
- blur direct observation and inference;
- invent measurements that were not observed;
- write code before the research conclusion exists.
