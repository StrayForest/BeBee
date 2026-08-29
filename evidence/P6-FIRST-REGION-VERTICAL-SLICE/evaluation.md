# P6 First Region Vertical Slice — independent evidence evaluation

Evaluated: 2026-08-29
Mode: `independent_pass`
Evaluator ID: `p6-evidence-evaluator-pass-2026-08-29`
Implementation author ID: `p6-implementation-agent`
Verdict: **PASS WITH DEVIATION**

## Inputs

This evaluation starts from the P6 milestone problem and exit criteria rather than the implementation rationale. Inputs are the P6 research/official-platform contract, exact-head Test/data results, retained P1–P6 Chromium `motion-report.json`, the clean-save six-frame journey, desktop/mobile/Poki canonical frames, save/settings/analytics measurements, release-bundle/FPS measurements and the retained P1–P5 regression evidence in the same artifact.

Accepted runtime evidence before closeout-only source-of-truth commits:

- head `1001783236aac0ca2052bf6b4498c600a5dbf6fb`;
- Repository standards `33269124642` — PASS;
- Test/data `33269124670` — PASS, `102/102`;
- Pages preview `33269124643` — PASS;
- HTML5 CI `33269124636` — PASS;
- movement/P6 artifact `9719600537` (`movement-qa-1001783236aac0ca2052bf6b4498c600a5dbf6fb`), digest `sha256:77f0b0972eb7ba12bac3e292f429a6c1689820e9984b0d28bee5f2e527e3c9de`;
- storage artifact `9719600731`, digest `sha256:65b11cfc5258dbe1edcba1d7210f38074b9843dc77de2f0363e14daf2f89531a`;
- visual artifact `9719600159`, digest `sha256:81b38a8164273d4bf761055ef2eaf3d09aa41e40ae801391eb8592514ac7f324`;
- playable artifact `9719599927`, digest `sha256:4f5705db6b447962f3dd12e87d17d1fca8bcfbd1bcc18e8fd29bff14a3eca902`;
- HTML5 diagnostics artifact `9719600959`, digest `sha256:f0afea230b579dd79a3078de0242346ee43ff38efc92cafd5b8f6e0e6e693673`.

The final PR head must rerun the exact-head gates after this evidence/source-of-truth closeout and reproduce a non-N/A `movement-qa-$PR_HEAD` artifact before merge.

## Objective measurements

| Measurement | Result | Evaluation |
|---|---:|---|
| Sunny Meadows restored | 6 / 6 | PASS |
| Flight level at completion | 3 | PASS |
| Buzz level at completion | 3 | PASS |
| Lily before Buzz 3 | LOCKED / requires Buzz 3 / 1.35× | PASS |
| Lily after Buzz 3 | AVAILABLE / 1.65× | PASS |
| Final clean-save Honey | 386 | PASS; no forced replay |
| Settings exercised | reduced motion ON; audio MUTED | PASS |
| Analytics events | 19 events / 6 semantic types | PASS |
| Browser console/page errors | 0 / 0 | PASS |
| External runtime requests | 0 | PASS |
| Desktop canvas | 1280×720 in 1280×720 viewport | PASS |
| Mobile canvas | 844×390 in 844×390 viewport | PASS |
| Poki viewports | 640×360, 836×470, 1031×580 | PASS |
| Engine frame rate | 59.92 fps | PASS; budget ≥50 |
| Release bundle | 2,813,096 bytes | PASS; budget ≤12,582,912 |
| Test/data | 102 / 102 | PASS |

## Functional / interaction findings

### F1 — P6 is a real clean-save region journey, not six disconnected fixtures — PASS

The retained clean-save sequence begins at region start, restores the first Meadow, reaches the Lily capability gate, completes Sunny Meadows, changes settings and reloads the completed state. The same `motion-report.json` records `result=PASS` and all six authored Meadows restored. This satisfies the milestone's central coherence requirement more strongly than a collection of canonical screenshots alone.

### F2 — Lily is a genuine Buzz-3 climax gate and both level-3 upgrades are active — PASS

Before Buzz 3, Lily reports `LOCKED`, `requires_buzz=3` and the current Buzz multiplier is `1.35×`. After the Buzz-3 purchase it reports `AVAILABLE` with `1.65×`; the journey finishes at Flight 3 and Buzz 3. The gate is capability-based rather than another direct Honey payment.

### F3 — Seed ownership remains part of the region without rewriting campaign truth — PASS

The combined exact-head artifact retains the P5 ownership/planting path and campaign-state separation while P6 completes the region. P6 therefore scales the validated Hybrid topology instead of replacing it with a new decoration or campaign-state model.

### F4 — Save v4, settings and reload are evidenced across deterministic and browser layers — PASS

The Test/data suite passes `102/102`, including current migration/storage coverage. The browser journey enables reduced motion and audio mute, reaches region completion and then reloads successfully. This is sufficient autonomous evidence that P6's new persistent settings do not invalidate the existing versioned storage contract.

### F5 — Accessibility/settings remain text-readable and focus-safe — PASS

The retained settings surface explicitly renders `REDUCED MOTION` with ON/OFF text and `AUDIO` with ON/MUTED text. The clean-save journey records both settings enabled, so the evidence does not rely on color alone.

### F6 — Analytics remains a platform-neutral seam — PASS

The accepted journey records 19 events across `session_start`, `first_input`, `patch_completed`, `meadow_restored`, `region_completed` and `settings_changed`. The P6 browser proof reports zero external requests, so the milestone does not smuggle a portal/runtime dependency into gameplay.

### F7 — Desktop/mobile/Poki canvas coverage is now correct — previous blocker resolved

The accepted desktop canonical frame reports canvas `1280×720` in a `1280×720` viewport; mobile reports `844×390` in the same-sized viewport, and all three required Poki sizes are retained. This directly closes the earlier canvas-sizing defect rather than accepting a centered/shrunken game surface.

### F8 — Clean-save start is no longer contaminated by the QA Honey fixture — previous blocker resolved

The accepted `region_start` is a clean-save state rather than inheriting the older `120 Honey` fixture. The retained six-frame clean-save path is therefore usable as milestone evidence instead of mixing canonical fixture state into the journey.

### F9 — Performance and release-size budgets pass without an optimization claim — PASS

The measured engine rate is `59.92 fps` against a `≥50` budget. The release bundle is `2,813,096` bytes against `12 MiB`. No external requests are required at runtime. These are measured acceptance results, not an assertion that all future content will automatically retain the same headroom.

## Visual evaluation

### V1 — Region-level hierarchy and local identity are coherent enough to validate the six-Meadow structure — PASS

Across the retained start/mid/complete and clean-save frames, the region uses one route language, one sparse objective/Honey HUD, local labels/landmarks and different Meadow palettes/compositions. First Patch, Creek Garden, Tulip Rise and Lily Clearing do not read as identical coordinate copies, and the 6/6 restoration payoff is legible without adding a world-map or dashboard.

### V2 — Settings and objective text remain legible across target landscape sizes — PASS

The desktop, mobile and Poki captures keep the required objective/progress information within the canvas, and the settings state is text-redundant. No browser/render error accompanies the retained surfaces.

### V3 — Illustration finish does not fully meet the long-term art-direction target — PASS WITH DEVIATION

The inspected runtime still uses intentionally geometric repository-authored presentation for the bee, flowers, plot/terrain shapes and much of the UI. This is materially below the aspirational direction in `docs/09-art-direction.md`: the bee is not yet a rounded expressive illustrated character, flower species do not yet achieve the intended degree of silhouette differentiation, and the UI/typography are not final illustrator/type-system polish.

This is **not** an external placeholder-asset dependency: the runtime assets and shapes are local/original, gameplay information is readable, critical audio is real local Wave content, and the full player journey is functional. But calling the presentation final production illustration would overstate the evidence. The correct closeout is therefore **PASS WITH DEVIATION**, with illustration/animation/typography/species-silhouette polish carried explicitly into P7 content production and required to be resolved before P8 release-candidate art certification.

The deviation does not require reopening the six-Meadow topology, progression, save, settings, analytics, portal-size or performance decisions proven by P6.

## P1–P5 regression finding

The same accepted `movement-qa` artifact retains the prior movement/modal/reduced-motion, pollination, progression/Buzz gate, first-Meadow restoration/reload and seed-ownership/browser contracts before and alongside P6. The combined artifact result is `PASS`; P6 therefore does not receive a green result by dropping earlier milestone proofs.

## Evaluation conclusion

**PASS WITH DEVIATION.**

P6 validates the first-region product structure as one continuous six-Meadow Sunny Meadows journey: it completes from a clean save, uses the validated pollination/progression/seed systems, proves Flight/Buzz 3 and the Lily gate, persists through save v4 and reload, exposes text-readable reduced-motion/audio settings, emits the platform-neutral analytics schema, fills desktop/mobile/Poki viewports, makes zero external requests, and passes measured FPS/bundle budgets while retaining P1–P5 regressions.

The remaining deviation is specifically visual finish: the current original geometric runtime presentation does not yet fully realize the rounded character/species-silhouette/final-typography art direction. That limitation is explicit and non-blocking for validating P6's region/system architecture, but it must remain visible in P7/P8 planning and may not be silently relabeled final production art. No `ITERATE` finding remains for P6 closeout.
