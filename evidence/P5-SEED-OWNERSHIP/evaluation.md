# P5 Seed Ownership During Restoration — independent evidence evaluation

Evaluated: 2026-08-29
Mode: `independent_pass`
Evaluator ID: `p5-evidence-evaluator-pass-2026-08-29`
Implementation author ID: `p5-implementation-agent`
Verdict: **PASS**

## Inputs

This evaluation starts from the P5 problem and exit criteria rather than the implementation rationale. Inputs are the validated P-1 Hybrid topology, P5 production research/official Defold constraints, deterministic Test/data/economy results, the exact-head Chromium `motion-report.json`, desktop canonical/lifecycle frames, 844×390 mobile-touch frames, save/reload measurements and the retained P1–P4 regression evidence in the same artifact.

Accepted runtime evidence before closeout-only source-of-truth commits:

- head `8967ab565bc9ff9c7838344676587fbf0a6d2ae0`;
- Repository standards `33251552722` — PASS;
- Test/data `33251552769` — PASS, `92/92`;
- P5 economy regression — PASS, `120/120` priority orders, final Honey `50` after all first sinks;
- Pages preview `33251552723` — PASS;
- HTML5 CI `33251552740` — PASS;
- movement/P5 artifact `9714546464` (`movement-qa-8967ab565bc9ff9c7838344676587fbf0a6d2ae0`), digest `sha256:64a04641fbd44542217ded406f785115b5939c8cd593436ec094f1b452e5e4ce`;
- storage artifact `9714546696`, digest `sha256:ccb79b5276118eadcb2c0161e3d9f1f20bfaa46ef41bad27c2a85037f27fb6c8`;
- visual artifact `9714546052`;
- playable artifact `9714545805`;
- HTML5 diagnostics artifact `9714546973`.

The final PR head must rerun the exact-head gates after this evidence/source-of-truth closeout and reproduce a non-N/A `movement-qa-$PR_HEAD` artifact before merge.

## Objective measurements

| Measurement | Result | Evaluation |
|---|---:|---|
| Player-shaped plots | 2 | PASS; bounded expression scope |
| Seed species | Daisy / Clover / Lavender | PASS; three first-region identities |
| One-time unlock costs | 15 / 18 / 22 Honey | PASS; explicit ownership sinks |
| Daisy real transaction | 45 → 30 Honey | PASS |
| Clover state after real transaction | owned; Honey 67 | PASS |
| Owned Daisy replant | 67 → 67 Honey | PASS; repeat cost 0 |
| Campaign completion after replant | patch 1=true, patch 2=true, patch 3=false | PASS; aesthetics do not rewrite campaign truth |
| Reload | Daisy+Clover owned, Daisy planted, Honey 67 | PASS |
| Save version | 3 | PASS |
| Mobile direct plot touch | true; 45 → 30 Honey | PASS |
| P5 console/page errors | 0 / 0 | PASS |
| Test/data | 92 / 92 | PASS |
| Economy priority orders | 120 / 120 | PASS |
| Economy final Honey after all first sinks | 50 | PASS; no forced replay/grind |

## Visual / interaction findings

### F1 — Native challenge and chosen flowers are separated in the rendered world — no blocker

The inspected desktop canonical/lifecycle frames reserve a visibly bounded object for ownership and label it `YOUR PLOT`. Before the prerequisite native patch is restored it is visibly locked and the nearby prompt says `RESTORE NATIVE PATCH FIRST`; after unlock the same object offers `PLANT DAISY`, then visibly contains the selected flower species. Native campaign patches remain in their established authored positions and continue to drive the objective/restoration ladder. This is a clearer separation than allowing the player to rewrite the identity of an incomplete native patch. **PASS.**

This is autonomous rendered evidence, not a claim that a novice human study was conducted. Comprehension confidence therefore remains **MEDIUM**.

### F2 — Ownership is visible before full meadow restoration — no blocker

After native patch 1, Daisy can be bought/planted while later native work remains. The retained frame changes the dedicated plot from empty soil to a visible Daisy cluster, satisfying the P5 ownership timing goal without waiting for full restoration. **PASS.**

### F3 — Replanting is reversible and campaign-safe — no blocker

The real browser sequence changes plot 1 Daisy → Clover → Daisy. Honey remains `67` across the owned Daisy replant and native completion remains patch 1/2 complete, patch 3 incomplete. The visible choice changes while campaign truth does not. **PASS.**

### F4 — Save v3 keeps the state domains independent — no blocker

Reload restores owned Daisy+Clover, Daisy on plot 1, Honey `67`, and the same native completion set. Deterministic migration coverage preserves previous Honey/upgrades/campaign progress while adding empty seed/plant state for v2 saves. **PASS.**

### F5 — Mobile touch uses the same low-friction world interaction — previous runtime bug fixed

The accepted 844×390 path moves to the player plot and directly taps it; the transaction changes Honey `45 → 30`, owns `seed_daisy`, plants `flower_daisy`, and reports zero browser errors. An earlier candidate failed because Defold's virtual `action.x/y` coordinates were scaled a second time. The fix uses physical `action.screen_x/screen_y` before the single screen→design conversion used by the world hit-test. **Resolved before acceptance.**

### F6 — BB-007 storage proof remains valid under schema v3 — previous evidence-contract defect fixed

After the mobile fix, HTML5 P5 proof itself passed but the old browser storage probe still generated a hard-coded `save_version = 2` fixture, which the current storage schema correctly rejected. The probe now derives `migrations.CURRENT_SAVE_VERSION`; the accepted exact-head HTML5 run passes the full storage lifecycle again. This changes the test fixture, not runtime acceptance semantics. **Resolved before acceptance.**

### F7 — Economy safety is stronger than one happy-path purchase order — no blocker

The P5 regression exhaustively evaluates all `5! = 120` priority orders across Flight 2, Buzz 2, Daisy, Clover and Lavender first sinks. Every order remains non-negative, avoids replay/grind and completes with Honey `50`. Free owned-species replant adds no recurring sink. **PASS.**

### F8 — Presentation is still primitive development art — non-blocking limitation

The role hierarchy is readable, but the bee, flowers, plot border/soil and typography are still repository-authored primitive development presentation. P5 proves topology, interaction, economy and persistence; P6 owns production illustration/animation/audio and full-scene polish. **Non-blocking for P5.**

## P1–P4 regression finding

The same accepted `movement-qa` artifact repeats movement/modal/reduced-motion, P2 pollination, P3 progression/Buzz gate and P4 restoration/reload evidence before executing P5. The artifact result is `PASS`, so P5 does not receive an isolated green result by dropping earlier browser contracts. **PASS.**

## Evaluation conclusion

**PASS.**

P5 productionizes the Hybrid model at vertical-slice scope: native campaign patches retain authored progression meaning; two dedicated `YOUR PLOT` spaces make seed ownership visible during restoration; Daisy/Clover/Lavender are one-time Honey sinks; owned replant is free and cannot mutate campaign completion; save v3 separates ownership/plants/native progress and reloads correctly; the desktop and mobile-touch paths use the same contextual interaction without a new modal; all 120 economy priorities remain progression-safe; and P1–P4 browser evidence remains green.

Evidence strength is **MEDIUM** because no external novice comprehension study or final production-art evaluation is claimed. No `ITERATE` finding remains open. P5 may advance to P6 only after final exact-head closeout gates, trusted evidence validation and merge.
