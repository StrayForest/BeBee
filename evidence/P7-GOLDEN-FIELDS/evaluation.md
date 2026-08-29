# P7 Golden Fields — independent evidence evaluation

Evaluated: 2026-08-29
Mode: `independent_pass`
Evaluator ID: `p7-golden-fields-evaluator-pass-2026-08-29`
Implementation author ID: `p7-golden-fields-implementation-agent`
Verdict: **PASS WITH DEVIATION**

## Inputs

This evaluation starts from the P7 production-expansion problem and the Golden Fields acceptance criteria rather than from the implementation rationale. Inputs are the P7 research record, exact-head Test/data results, retained P1–P7 Chromium `motion-report.json`, the Golden Fields start/mid/complete/reload/mobile frames, browser error/request measurements, economy measurements, the current release performance measurements and retained P1–P6 regressions in the same artifact.

Accepted runtime evidence before closeout-only source-of-truth commits:

- head `8d9640522ffc742ffe79178718fa2df0517dd6bc`;
- Repository standards `33271607224` — PASS;
- Test/data `33271607179` — PASS, `108/108`;
- Pages preview `33271607241` — PASS;
- HTML5 CI `33271607193` — PASS;
- movement/P7 artifact `9720322590` (`movement-qa-8d9640522ffc742ffe79178718fa2df0517dd6bc`), digest `sha256:b58dc0c217aa1845a3f42a2b1cf2fcb4685f2a548f452d09be50d00cbeb0fd80`;
- storage artifact `9720322807`, digest `sha256:7101d69c975e8543fe1babf7e7b835826408ce73fb3e489a5fb0d8537354ce6a`;
- visual artifact `9720322272`, digest `sha256:02fec4d9a4b5ad298c83bb72211c6a600093bd1ef3a335decbc58fe964e53a44`;
- playable artifact `9720322102`, digest `sha256:8c8c5fed6235c72460485ad235c7110e59b42998e11a3be3a31dce48da45bd3e`;
- HTML5 diagnostics artifact `9720323006`, digest `sha256:66c7580f97f7ba00ee1a1e27fa5c6ec493e8941e82c696906e0aebddd0c3f682`;
- Test/data artifact `9720268026`, digest `sha256:ed82ab40085d5bbf226f7fb7d341cdcb0a329133c11c4858d993aac251b4f987`.

The final PR head must rerun the exact-head gates after this evidence/source-of-truth closeout and reproduce a non-N/A `movement-qa-$PR_HEAD` artifact before merge.

## Objective measurements

| Measurement | Result | Evaluation |
|---|---:|---|
| Golden Fields restored | 4 / 4 | PASS |
| Campaign regions complete | 2 / 2 | PASS |
| Start Honey | 346 | PASS |
| Final Honey | 891 | PASS; +545 with no required replay/spend |
| Golden Fields analytics events | 11 | PASS |
| Browser console/page errors | 0 / 0 | PASS |
| External runtime requests | 0 | PASS |
| Desktop canvas | 1280×720 in 1280×720 viewport | PASS |
| Mobile canvas | 844×390 in 844×390 viewport | PASS |
| Engine frame rate | 59.87 fps | PASS; budget ≥50 |
| Release bundle | 2,815,539 bytes | PASS; budget ≤12,582,912 |
| GUI `max_nodes` | 512 unchanged | PASS |
| Patch visual pool | 6 reusable slots | PASS |
| Test/data | 108 / 108 | PASS |

## Functional / interaction findings

### F1 — Golden Fields is reached through real persisted campaign state — PASS

The P7 journey starts from the accepted P6 region-complete fixture, persists it through the real settings/save path, removes the QA route, and then continues through ordinary runtime derivation. The recorded `fixture_source` is `P6 region_complete fixture persisted through real settings save, then QA route removed`; `region_02` starts at 0/4 with `r02_m01` as the next Meadow. This is materially stronger than injecting a Golden Fields-only fixture.

### F2 — All four Meadows reuse the proven core verb and economy — PASS

Sun Gate, Poppy Run, Windmill Loop and Harvest Crown all complete through the existing movement-through pollination path. Sunflower and Poppy patches retain Buzz-3 capability requirements and the journey moves from `346` to `891 Honey`, exactly matching the deterministic +545 reward path with no new required purchase, replay, currency or upgrade branch.

### F3 — Region derivation and reload scale beyond one region — PASS

At completion the campaign reports both `region_01` at 6/6 and `region_02` at 4/4, `completed_regions=2`, `total_regions=2`, and `complete=true`. Reload retains Golden Fields at 4/4 and Honey 891 through the existing save-v4 abstraction; P7 does not add a second persistence model.

### F4 — The first HTML5 failure exposed a real scaling defect and the repair is architectural — PASS

The naive expansion head `ba4c4be33f7353944a5ff5ea1389e04948a79eb4` failed in Chromium with `Out of nodes (max 512)` while constructing one permanent flower GUI tree per authored patch. The accepted implementation does not raise the scene budget: `max_nodes` remains 512 and rendering uses six reusable nearby-patch visual slots. The accepted HTML5 run then passes. This closes the concrete failure by bounding rendering cost to visible complexity instead of total catalog size.

### F5 — Browser/platform regressions remain intact — PASS

The combined artifact result is PASS and retains P1–P6 movement, pollination, progression, restoration, seed ownership, settings, storage and first-region proofs. P7 itself reports zero console/page errors, zero external requests, exact full-canvas desktop/mobile sizes, 59.87 fps against the 50-fps floor and a 2,815,539-byte bundle under 12 MiB.

## Visual evaluation

### V1 — Golden Fields has distinct regional identity — PASS

The retained frames use a materially different golden field palette, Sun Gate/Windmill/Harvest landmark language and distinct Sunflower/Poppy presentation. Sunflower and Poppy are not merely recolored copies: their retained flower shapes differ as well as their color treatment, which is sufficient for this authored-content expansion proof.

### V2 — The presentation is not final production illustration — PASS WITH DEVIATION

The current runtime remains deliberately geometric. The bee, flower forms, typography and much of the full-scene composition are readable but still below the long-term rounded expressive character, richer species-silhouette and final typography/illustration target documented in the art direction. Some edge-of-world framing is also visually sparse at wide landscape positions even though the canvas itself correctly fills the viewport.

This does not invalidate the Golden Fields scaling result: the assets are repository-authored, interaction/state remains readable, and no external placeholder dependency is being hidden. It does mean Golden Fields must not be labeled release-candidate art. The P6 visual-finish deviation remains open P7/P8 work.

## Milestone-scope finding

Golden Fields is the **first P7 production-expansion slice**, not completion of P7 as a whole. Wetland Garden, Rosewood, Alpine Bloom and Moon Garden remain ahead. The correct project state after this PR is therefore **P7 IN PROGRESS — Golden Fields accepted with deviation**, with Wetland Garden as the next production slice.

## Evaluation conclusion

**PASS WITH DEVIATION.**

Golden Fields proves that the validated P1–P6 architecture can scale into a second authored region without a new core verb, currency, upgrade branch, world-management screen or per-region game-world lifecycle. The real browser journey activates `region_02` from persisted P6 completion, restores all four Meadows, raises Honey `346 → 891`, records region-scoped analytics, survives reload, retains all prior browser evidence and passes current performance/request/error budgets. The first browser attempt exposed a genuine GUI-node scaling failure; the accepted six-slot visual pool repairs that failure while keeping `max_nodes: 512` unchanged.

The remaining deviation is visual finish, not functional architecture. No `ITERATE` finding remains for the Golden Fields slice, but P7 itself remains in progress and final art certification remains a later gate.
