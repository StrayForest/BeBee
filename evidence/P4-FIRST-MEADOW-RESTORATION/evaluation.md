# P4 First Meadow Restoration — independent evidence evaluation

Evaluated: 2026-08-29
Mode: `independent_pass`
Evaluator ID: `p4-evidence-evaluator-pass-2026-08-29`
Implementation author ID: `p4-implementation-agent`
Verdict: **PASS**

## Inputs

The evaluation began from the P4 player problem and exit criteria, not from the implementation rationale. Inputs were the selected reference observations, P4 authored-stage contract, deterministic Test/data results, exact-head Chromium motion report, HUD-hidden desktop before/mid/after frames, Poki-small before/after frames, mobile-landscape restored frame, reload evidence and reveal-control measurement.

Accepted runtime evidence before closeout-only source-of-truth commits:

- head `a45f9dac2f9d7136c3da51dc5b761eb0c05ce739`;
- Repository standards `33249086788` — PASS;
- Test/data `33249086793` — PASS;
- Pages preview `33249086822` — PASS;
- HTML5 CI `33249086913` — PASS;
- movement/P4 artifact `9713808008` (`movement-qa-a45f9dac2f9d7136c3da51dc5b761eb0c05ce739`), digest `sha256:7385f1161ad2c68a91027bbc5585b6246abb14fdc56c42929ade4f158d8369ec`;
- storage artifact `9713808284`;
- playable artifact `9713807374`;
- visual artifact `9713807618`;
- HTML5 diagnostics artifact `9713808576`.

The final PR head must rerun the exact-head gates after this evaluation/source-of-truth closeout and reproduce a non-N/A `movement-qa-$PR_HEAD` artifact before merge.

## Objective measurements

| Measurement | Dormant | Mid / Growing | Restored | Evaluation |
|---|---:|---:|---:|---|
| Restoration contribution | 0 | 2 | 3 | PASS; deterministic ladder source is observable |
| Ground mix | 0.00 | 0.68 | 1.00 | PASS; large environment-value change |
| Detail count | 8 | 22 | 28 | PASS; restored scene has 3.5× dormant detail count |
| Ambient-life count | 0 | 2 | 6 | PASS; later stages add a separate living-world cue |
| HUD hidden in comparison frames | yes | yes | yes | PASS; world state does not depend on HUD copy |
| Modal tutorial count | 0 | 0 | 0 | PASS |
| Persistent objective count | 1 | 1 | 1 | PASS; D-008 density retained |
| Reveal duration | n/a | n/a | 1.5 s | PASS; inside V-001 1.2–2.0 s major-reveal band |
| Movement during reveal | n/a | n/a | 86.644 u displacement | PASS; celebration does not capture/block control |
| Reload stage | n/a | GROWING retained | RESTORED retained | PASS |
| Celebration after restored reload | n/a | n/a | false | PASS; one-shot reveal is not replayed |
| P4 console/page errors | 0 / 0 | 0 / 0 | 0 / 0 | PASS |

Canonical fixture proof independently reports `meadow_dormant = DORMANT/0`, `meadow_mid = GROWING/2`, and `meadow_restored = RESTORED/3`, so deterministic QA state names are not merely labels over whichever player save happened to be present.

## Visual findings

### F1 — HUD-hidden transformation is materially readable — no blocker

The inspected dormant frame is muted and sparse; the restored frame is substantially brighter/greener, contains materially more ground detail and visible ambient-life marks, while the same bee/patch geography keeps the comparison understandable. The distinction remains visible at Poki-small. This satisfies P4's central requirement better than a completion banner or HUD meter would. **PASS.**

### F2 — intermediate state reads as recovery rather than binary completion — no blocker

The WAKING/GROWING frames progressively increase ground value, flowers/details and ambient-life count rather than jumping directly from dormant to restored. The measured 8 → 14 → 22 → 28 detail ladder and 0 → 1 → 2 → 6 ambient-life ladder provide redundant stage cues. **PASS.**

### F3 — restored state remains legible on mobile landscape — no blocker

The 844×390 restored capture keeps the meadow, bee and restoration detail readable without HUD overlap. P4 introduces no new touch control or modal surface, so mobile interaction complexity does not increase. **PASS.**

### F4 — completion accent is bounded and non-blocking — no blocker

The final restored transition activates the authored 1.5-second world-space accent. Browser input during that window moves the bee by 86.644 design units, proving that celebration presentation does not take input ownership. **PASS.**

### F5 — reload semantics are correct — previous runtime bug fixed before acceptance

An earlier candidate replayed the final celebration when an already-restored save was loaded. The accepted head initializes the restored presentation without replaying the one-shot accent. Midpoint reload restores `GROWING`; final reload restores `RESTORED`; Buzz 2 needed for the Lavender path also survives. **Resolved before acceptance.**

### F6 — canonical QA fixtures are independent of persistence — previous evidence-contract defect fixed before acceptance

An earlier candidate allowed named `meadow_*` states to inherit player-save state, which could make a deterministic fixture name misleading. The accepted head separates canonical fixture capture from `p4_storage_lifecycle=reset/reload` proof. Clean-context fixtures deterministically yield DORMANT/0, GROWING/2 and RESTORED/3. **Resolved before acceptance.**

### F7 — player comprehension evidence is sufficient for the autonomous milestone, but not external playtest evidence — non-blocking limitation

Ordinary gameplay retains one objective plus Honey, existing patch state/gate cues still communicate the next actionable area, and P4 adds no modal tutorial or second restoration button. The rendered evidence therefore supports the autonomous P4 comprehension criterion. No external novice playtest was run, so evidence strength remains **MEDIUM** rather than being presented as observed user-study proof. **Non-blocking.**

### F8 — presentation is still primitive development art — non-blocking limitation

The transformation is objectively readable, but the current flowers, bee, ground details, ambient life and celebration use repository-authored primitive shapes. P4 proves the restoration system/visual hierarchy, not final illustration, animation, typography or audio. P6 owns production-art/audio polish. **Non-blocking for P4.**

## Reference comparison scorecard

| Criterion | Terra Nil | The Gunk | BeBee P4 | Finding |
|---|---:|---:|---:|---|
| Transformation shown in-world | strong | strong | strong for P4 scope | PASS; no separate results screen |
| Multiple world-state channels | terrain + ecology | corruption removal + regrowth | ground mix + detail density + ambient life | PASS |
| Extra restore confirmation | no equivalent post-result confirmation needed for the observed payoff | no separate BeBee-style confirmation pattern | 0 | PASS; avoids redundant administrative action |
| HUD-independent before/after | yes as product premise | yes as product premise | yes in exact-head captures | PASS |
| Objective clarity | n/a for direct numeric comparison | n/a | 4/5 — one objective and existing patch cues | strong for current scope |
| State readability | n/a | n/a | 4/5 — dormant/mid/restored visibly distinct | strong |
| Feedback quality | n/a | n/a | 4/5 — automatic multi-channel change + bounded reveal | strong |
| Mobile comfort | n/a | n/a | 4/5 — no new touch action/modal, restored capture readable | strong |
| World transformation | n/a | n/a | 4/5 — 3.5× detail count plus full ground/ambient shift | strong for primitive-art milestone |
| Original BeBee expression | n/a | n/a | 3/5 — bee/pollination causality is distinct, art remains placeholder | acceptable baseline; P6 polish remains |

The scorecard is not a claim that BeBee matches the production-art richness or scale of the references. It shows that P4 adopts the relevant structural principle — the environment itself changes through multiple channels — at the deliberately smaller vertical-slice scope.

## Evaluation conclusion

**PASS.**

P4 proves the central restoration promise at the system/visual-hierarchy level: the same authored meadow progresses through four deterministic stages as existing pollination completions accumulate; the before/after is materially legible with HUD hidden; no modal tutorial or extra restoration action is introduced; the final accent is bounded and non-blocking; midpoint/final state survives reload; canonical fixtures are independent of persistence; and desktop/Poki-small/mobile evidence reports zero browser errors.

Evidence strength is **MEDIUM**. The milestone may advance to P5 after the final exact-head closeout gates and merge, while external novice comprehension testing and production art/audio remain later validation/polish work. No `ITERATE` finding remains open.
