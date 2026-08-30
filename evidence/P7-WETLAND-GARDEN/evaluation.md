# P7 — Wetland Garden independent evaluation

## Evaluation input

- Feature: third authored region `region_03` — Wetland Garden.
- Acceptance criteria: same-PR `evidence/P7-WETLAND-GARDEN/manifest.json`.
- Evaluated head: `$PR_HEAD` (trusted exact-head CI resolves this binding for the final PR head).
- Runtime inputs: retained `movement-qa`, `visual-qa`, `storage-qa`, `html5-ci-evidence` and `html5-playable` artifacts from HTML5 CI run `33304395113`.
- Implementation author: `p7-wetland-garden-implementation-agent`.
- Evaluator: `p7-wetland-garden-independent-evaluator-2026-08-30`.

## Evidence review

The exact-head retained movement report is `P1-P7-RUNTIME` with result `PASS`. Its Wetland journey starts from the persisted P6/Golden state at region_03 `0/4` and `891 Honey`, reaches a `2/4` midpoint, completes Lotus Landing, Iris Channel, Rootwalk Isles and Dragonfly Basin through the existing patch completion path, and reports `4/4`, `1596 Honey` and `region_03` after reload.

The campaign reload contains all three authored regions complete. The event list includes the existing `region_completed` event after Wetland completion. The four Wetland patch records retain the existing `requiresBuzzLevel: 3` capability and `COMPLETED` state; no new verb, currency or lethal water state is present.

The retained still sequence covers desktop start/mid/complete/reload and mobile-landscape completion. It shows a distinct blue-green wetland palette, water pools/channels, root/boardwalk accents, islands and different Lotus/Iris silhouettes. The objective and Honey HUD remain readable. Repeated movement captures are byte-stable and have zero console/page errors. Storage evidence confirms save version 4 across clean start, normal save/reload, immediate refresh recovery, delete persistence, quick checkpoints and corrupt-newest recovery.

The HTML5 job completed build, smoke, deterministic capture, playable bundle and all evidence upload steps. Structured browser smoke reports WebAssembly/canvas readiness, no actionable HTTP errors, no network-loading failures, no console errors and no runtime exceptions. The retained Wetland capture reports desktop `1280x720`, mobile `844x390`, console/page errors `0/0` and external requests `0`. Retained exact-head runs measure approximately `60 fps` against a `50 fps` minimum and approximately `2.82 MB` bundles against a `12,582,912`-byte budget.

The first candidate exposed a scaling defect where `view_state` exceeded Defold's `msg.post` buffer at `2040 bytes` after the catalog grew. The accepted repair omits transient `qualifying=false` for inactive patches and adds a regression test. The exact-head HTML5 run passes without that failure while retaining `PATCH_POOL_SIZE=6` and `max_nodes=512`.

## Findings

### F1 — Functional region acceptance

Severity: none.

The authored region, four Meadows, existing movement-through pollination, Buzz 3 gate, Honey path, region analytics, save/reload and expanded world/camera bounds are all supported by deterministic and real Chromium evidence. The economy path is `891 -> 1596 Honey` with `+705` first-time rewards and no mandatory spend/replay.

### F2 — Runtime and evidence integrity

Severity: none.

The artifact head binding matches the PR head. The retained artifacts are non-empty, non-N/A and their structured reports agree on the head, result, viewport, error and persistence claims. HTML5 CI and the other exact-head checks pass.

### F3 — Existing art-direction deviation

Severity: accepted deviation, non-blocking for this slice.

The rendered bee, flower forms, typography and full-scene composition remain intentionally geometric and below the long-term rounded expressive character/species-silhouette/final-typography target. Wetland identity is nevertheless readable through palette, silhouettes, landmarks and layout. This should remain explicit in the PR and must be addressed before release-candidate visual certification; it is not evidence for an `ITERATE` on the Wetland architecture/content slice.

## Comparison conclusion

- [ ] PASS
- [x] PASS WITH DEVIATION
- [ ] ITERATE

The Wetland Garden slice is accepted with the existing art-direction deviation explicitly carried forward. No further iteration is required to merge this slice.

## Verdict

**PASS WITH DEVIATION**

`iteration_required=false`.

Record provenance: `evidence/P7-WETLAND-GARDEN/evaluation.md` in this PR; captured/evaluated exact head `$PR_HEAD`, resolved by trusted CI.
