# P3 Progression — independent evidence evaluation

Evaluated: 2026-08-29
Mode: `independent_pass`
Evaluator ID: `p3-evidence-evaluator-pass-2026-08-29`
Implementation author ID: `p3-implementation-agent`
Verdict: **PASS**

## Inputs

The evaluation was evidence-first. Inputs were the P3 problem and acceptance criteria, D-007/D-009/D-010/D-013 constraints, production reference analysis, deterministic economy/migration coverage, exact-head HTML5 motion report, desktop/mobile Hive stills, Flight motion evidence, Buzz-gate frame sequence and reload evidence.

Accepted runtime evidence before the closeout-only documentation/evidence commits:

- head `3b4b990923851217d9a25e2954a86443dea3916f`;
- Repository standards run `33247411592` — PASS;
- Test/data run `33247411586` — PASS;
- Pages preview run `33247411600` — PASS;
- HTML5 CI run `33247411645` — PASS;
- movement/P3 artifact `9713299114` (`movement-qa-3b4b9909…`), digest `sha256:f7e1ce37eba04ecec26a23b42991f7bea4681ecdde64feaec8d225a1f7101ef9`;
- visual artifact `9713298823`;
- storage artifact `9713299343`;
- playable artifact `9713298577`;
- HTML5 diagnostics artifact `9713299597`.

The final PR head must rerun the same exact-head checks and reproduce `movement-qa-$PR_HEAD` before merge. The closeout commits change evidence/source-of-truth text only, not P3 runtime behavior.

## Objective measurements

| Measurement | Result | Evaluation |
|---|---:|---|
| First completion Honey available | 45 | PASS; both first choices affordable |
| Flight cost | 30 Honey | PASS |
| Flight level 1 → 2 speed | 300 → 330 u/s | PASS; real movement effect |
| Flight post-purchase Honey | 15 | PASS; no negative balance |
| Captured Flight cruise | 330 / 330 u/s | PASS |
| Flight reload | level 2 / 330 u/s / Honey 15 | PASS |
| Buzz cost | 35 Honey | PASS |
| Buzz level 1 → 2 work | 1.00× → 1.35× | PASS; real pollination effect |
| Buzz test Honey | 100 → 65 | PASS |
| Lavender before Buzz 2 | `LOCKED / requires_buzz / 2` | PASS; explicit capability reason |
| Lavender after Buzz 2 | `AVAILABLE` | PASS |
| Buzz reload | level 2 / 1.35× / Lavender AVAILABLE / Honey 65 | PASS |
| Hive modal movement displacement | 0.0 | PASS; input isolation retained |
| Representative P1 movement | 60.39 fps | PASS; regression retained |
| Reduced-motion camera lag X/Y | 0.0 / 0.0 | PASS |
| P3 browser console/page errors | 0 / 0 | PASS |
| P3 upgrade cards | 2 | PASS; no filler track |

## Findings

### F1 — mobile Hive card copy too small — blocking on previous head, fixed

The mechanically green `de277105c142d4d251bd8f560fcac162c2a1d164` artifact displayed the right information but compressed the mobile card copy too aggressively at 844×390. That was a real readability failure for a purchase decision and was not accepted merely because the purchase mechanics passed.

The accepted `3b4b9909…` head separates level, current→next effect and Honey cost into readable rows. Both complete cards remain inside the mobile panel without clipping or HUD overlap. **Resolved before closeout.**

### F2 — Buzz gate cue sat too close to the upper HUD — blocking on previous head, fixed

The previous runtime candidate made the Lavender requirement difficult to scan because its Buzz-gate label was positioned close to the top/Honey surfaces. The requirement is the only explicit non-color reason the patch cannot yet be used, so its readability is part of the gate semantics.

The accepted head renders `REQUIRES BUZZ 2` in a safe world-space position below the upper HUD. In the inspected locked frame the label is unobstructed; after buying Buzz 2 the patch becomes `AVAILABLE` and the requirement cue disappears. Reload preserves the unlocked state. **Resolved.**

### F3 — Flight is real power rather than a saved counter — no blocker

The accepted desktop sequence starts at 300 u/s, spends exactly 30 Honey from 45, records Flight level 2 and then captures a real 330/330 u/s cruise. Reload restores level 2 and 330 u/s. The upgrade therefore changes the P1 traversal system itself rather than only changing UI/save data. **PASS.**

### F4 — Buzz has both immediate effect and explicit aspiration gate — no blocker

The Buzz sequence spends exactly 35 Honey, changes the work multiplier to 1.35×, and changes Lavender from `LOCKED / requires_buzz / 2` to `AVAILABLE`. The gate is capability-based rather than a Honey payment, preserving D-010. **PASS.**

### F5 — first-purchase choice and economy safety — no blocker

From the P2 first reward of 45 Honey, Flight 2 costs 30 and Buzz 2 costs 35, so either is a valid first purchase. Deterministic regression covers both orders, the complete two-upgrade ordering, a minimal-required path and a customization-heavy shadow-spend path without negative Honey, unintended replay or a progression dead-end. **PASS.**

### F6 — purchase input isolation and durability — no blocker

Opening the Hive consumes movement through the existing modal stack; measured movement displacement while open is 0.0. Flight and Buzz purchases survive reload with their real gameplay/gate effects. Save v1→v2 migration coverage preserves P2 Honey/completion state while adding valid upgrade state. **PASS.**

### F7 — presentation scope — non-blocking limitation

The accepted build intentionally still uses repository-authored primitive development presentation and the existing placeholder font. The evidence is sufficient to judge card information hierarchy, world-gate obstruction, state change and movement/pollination effects, but it is not final production art, typography, animation or audio. **Non-blocking; later milestones own replacement/polish.**

## Reference comparison

Slime Rancher supplies the dedicated home-upgrade structural pattern; Dave the Diver supplies a compact current/next/price information hierarchy; A Short Hike demonstrates why traversal progression should be felt directly. BeBee deliberately rejects the density of Hades' broad meta-progression and the waiting friction of Stardew Valley's multi-day tool-upgrade flow for this small browser-first vertical slice.

The selected result copies no competitor artwork, code, UI expression or proprietary assets. The references constrain interaction purpose and information requirements only.

## Evaluation conclusion

**PASS.**

P3 supports keeping `D-007` `VALIDATED` while adding a production first-level baseline: Flight `300 → 330 u/s` for `30 Honey`, Buzz `1.00× → 1.35×` for `35 Honey`, with Lavender as the first explicit `Buzz 2` capability gate. It also clarifies D-013: 300 u/s remains the level-1 traversal baseline while Flight progression may deliberately raise the computed max speed without changing controller semantics.

Evidence strength remains **MEDIUM**. Exact-build autonomous browser/runtime and deterministic economy evidence are sufficient to advance production to P4, but later external playtest/telemetry may still retune costs, effect size and gate cadence.

No `ITERATE` finding remains open. Final merge is still conditional on the closeout PR head passing Repository standards, Test/data, HTML5 CI and trusted PR evidence on that exact head, with a retained non-N/A movement/P3 artifact.
