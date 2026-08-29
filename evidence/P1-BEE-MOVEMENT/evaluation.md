# P1 Bee Movement — independent evidence evaluation

Evaluated: 2026-08-29
Mode: `independent_pass`
Evaluator ID: `p1-evidence-evaluator-pass-2026-08-29`
Implementation author ID: `p1-implementation-agent`
Verdict: **PASS**

## Inputs

The evaluation was evidence-first. Inputs were the P1 problem/acceptance criteria, selected-reference observations, V-001 visual guardrails, exact-head HTML5 results and retained motion/still evidence.

Accepted runtime evidence before the closeout-only documentation commit:

- head `2e1098ac10596d02ad7d8b71e6034b5e778a7315`;
- Repository standards run `33240599831` — PASS;
- Test/data run `33240599809` — PASS;
- HTML5 CI run `33240599811` — PASS;
- movement artifact `9711246614` (`movement-qa-2e1098ac…`), digest `sha256:c7ce6fb028ea0e4a44bdfe66a4f5764be0e313af2e3b416381ea843b9dfda62e`;
- visual artifact `9711246280`;
- playable artifact `9711245985`;
- storage artifact `9711246878`;
- HTML5 diagnostics artifact `9711247199`.

The final PR head must rerun the same exact-head checks and reproduce a `movement-qa-$PR_HEAD` artifact before merge. The closeout commit changes evidence/source-of-truth text, not movement runtime behavior.

## Objective measurements

| Measurement | Result | Evaluation |
|---|---:|---|
| Desktop observed frame rate | 61.40 fps | PASS; no representative browser stall |
| Desktop cardinal cruise | 300 units/s | PASS |
| Desktop normalized diagonal | 300 units/s | PASS; no diagonal advantage |
| Desktop release speed | 0 | PASS; no stuck/coast state |
| Mobile horizontal speed | 300 units/s | PASS |
| Mobile normalized diagonal | 300 units/s | PASS |
| Mobile release speed | 0 | PASS |
| Central motion bound hits | 0 | PASS |
| Modal displacement while modal owns focus | 0.0 | PASS |
| Reduced-motion camera lag X/Y | 0.0 / 0.0 | PASS |
| Browser console/page errors | 0 / 0 | PASS |
| Desktop bee height | 102/720 = 14.17% | PASS against V-001 12–15% |
| Poki-small bee height | 48/360 = 13.33% | PASS against V-001 |
| Mobile-landscape bee height | 52/390 = 13.33% | PASS against V-001 |
| Deterministic soak | 18,000 frames / 300 s | PASS; finite and bounded |

## Findings

### F1 — initial bee scale violated V-001 — blocking, fixed

The first fully functional retained artifact (`5f2a32f…`) rendered the bee at only about 6.7–6.9% of viewport height. That was substantially below V-001's validated 12–15% ordinary-bee band and was a merge blocker even though the movement mechanics passed.

The presentation geometry was doubled in `2e1098a…`. Final retained stills measure 13.33–14.17% across desktop, Poki-small and mobile-landscape captures. No overlap or readability regression was introduced. **Resolved.**

### F2 — native proxy/modal ownership — blocking risk, resolved

Earlier candidates showed that custom owner-side movement forwarding could bypass the proxy world's modal consumption. A subsequent attempted cross-world block message also exposed an invalid socket assumption.

The accepted architecture keeps the main-world proxy owner free of `on_input()` forwarding, places movement inside the proxied gameplay world, and forwards semantic movement from the existing proxied gameplay listener to the movement object in that same world. Modal focus therefore remains authoritative under the already-proven BB-003 Defold stack. Exact-head evidence reports modal displacement `0.0`, and the existing BB-003 proxy smoke passes. **Resolved.**

### F3 — movement/touch parity — no blocker

Keyboard and touch both drive the same normalized controller and reach the same 300-unit/s maximum. Diagonal intent remains normalized, and both input methods return to zero on release. The touch joystick is floating rather than permanently occupying screen space. **PASS.**

### F4 — camera/reduced motion — no blocker

Normal follow preserves a modest lag/dead-zone relationship without changing input ownership. Reduced-motion removes that lag entirely: measured X/Y lag is `0.0`. No camera instability or bound escape is present in the deterministic soak. **PASS.**

### F5 — presentation scope — non-blocking limitation

The retained field and bee use original repository-authored primitive development shapes. They are sufficient to evaluate position, scale, direction, touch-control obstruction and camera motion, but they are not final illustration/animation/audio. P1 does not claim otherwise. **Non-blocking; later visual/audio milestones own replacement.**

## Reference comparison

The selected floating direct-intent solution preserves the transferable parts of the Stardew mobile invisible-joystick and Sky touch-surface patterns without copying their UI, artwork or movement constants. The rejected tap-to-move alternative would add path ownership and blocker/rerouting behavior that conflicts with BeBee's already validated movement-through/sweep core verb.

BeBee intentionally does not add an independent camera gesture in P1. The stable top-down follow camera is consistent with the V-001 direction and avoids adding a second touch-control problem before P2 needs contextual interaction.

## Evaluation conclusion

**PASS.**

The evidence supports promoting the P1 traversal baseline to `VALIDATED` with **MEDIUM** evidence strength. This is not a claim that the values are immutable: P2 may tune pollination-related movement requirements and P3 may tune Flight effects if new evidence identifies a concrete problem.

No `ITERATE` finding remains open. Final merge is still conditional on the closeout PR head passing Repository standards, Test/data, HTML5 CI and trusted PR evidence on that exact head.
