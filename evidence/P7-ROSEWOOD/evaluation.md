# P7 — Rosewood independent evaluation

## Evaluation input

- Feature: fourth authored region `region_04` — Rosewood.
- Acceptance criteria: same-PR `evidence/P7-ROSEWOOD/manifest.json`.
- Evaluated head: `$PR_HEAD` (trusted exact-head CI resolves this binding for the final PR head).
- Runtime inputs: retained `movement-qa`, `visual-qa`, `storage-qa`, `html5-ci-evidence` and `html5-playable` artifacts from the candidate HTML5 CI run `33312103046`.
- Implementation author: `p7-rosewood-implementation-agent`.
- Evaluator: `p7-rosewood-independent-evaluator-2026-08-30`.

## Evidence review

The retained Rosewood journey starts from persisted regions 01–03 at region_04 `0/4` and `1596 Honey`, reaches a `2/4` midpoint, completes Rose Glade, Bluebell Hollow, Cedar Turn and Woodland Crown through the existing movement-through pollination path, and reports `4/4`, `2506 Honey`, `region_04` and a completed four-region campaign after reload.

The four patch records retain the existing Buzz-3 capability and COMPLETED state; no new verb, currency, mandatory spend or lethal water/woodland state is present. The retained still sequence covers desktop start/mid/complete/reload and mobile-landscape completion, with authored woodland palette, Rose/Bluebell identity, landmarks and readable objective/Honey HUD. Repeated movement captures and storage evidence remain clean.

The candidate exposed no functional failure after the earlier catalog/view_state repair. The accepted source retains `PATCH_POOL_SIZE=6`, `max_nodes=512`, compact inactive-patch serialization and expanded finite camera/movement bounds.

## Findings

### F1 — Functional region acceptance

Severity: none.

The authored fourth region, four Meadows, existing movement-through pollination, Buzz 3 gate, Honey path, region analytics, save/reload and expanded bounds are supported by deterministic and Chromium evidence.

### F2 — Runtime and evidence integrity

Severity: none for the candidate inputs; final exact-head producer and trusted validation remain required before merge.

The retained candidate artifacts are non-empty, identify the implementation head and agree on the journey, viewport, error and persistence claims. The same-PR manifest/evaluation record this evidence and bind final closeout to `$PR_HEAD`.

### F3 — Existing art-direction deviation

Severity: accepted deviation, non-blocking for this slice.

The rendered bee, flower forms, typography, animation and full-scene composition remain intentionally geometric and below the long-term rounded expressive/species-silhouette/final-typography target. Rosewood identity is nevertheless readable through palette, silhouettes, landmarks and layout. This must be addressed before release-candidate visual certification; it is not an ITERATE finding on the Rosewood architecture/content slice.

## Comparison conclusion

- [ ] PASS
- [x] PASS WITH DEVIATION
- [ ] ITERATE

## Verdict

**PASS WITH DEVIATION**

`iteration_required=false`.

Record provenance: `evidence/P7-ROSEWOOD/evaluation.md` in this PR; captured/evaluated exact head `$PR_HEAD`, resolved by trusted CI.
