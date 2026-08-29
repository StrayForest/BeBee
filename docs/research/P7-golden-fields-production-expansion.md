# P7 Golden Fields — Production Expansion Research

Date checked: 2026-08-29

## Problem

P6 proved one coherent six-Meadow Sunny Meadows region. P7 must prove that the same movement → pollination → Honey → progression/restoration architecture can scale into a second authored region without adding another core verb, currency, mandatory sink, world-management screen, or per-region runtime architecture.

The first P7 slice is **Golden Fields**. It is intentionally a content-expansion proof, not the completion of all P7 regions.

## Locked inputs

- `D-004`: authored regions / meadows / patches, not an infinite procedural world.
- `D-009`: customization/spending cannot create unrecoverable grind.
- `D-010`: world gates use restoration/progression/Buzz by default, not Honey payments.
- `D-012`: canonical order is Sunny Meadows → Golden Fields → Wetland Garden → Rosewood → Alpine Bloom → Moon Garden.
- `T-004`: GUI scripts do not own gameplay/economy/progression state.
- P6 accepted runtime: one continuous authored world, six Sunny Meadows Meadows, Flight/Buzz 3, seed ownership, settings, analytics and save v4.

## Candidate pool

| product_id | Reference | Why it matters |
|---|---|---|
| `garden-life` | Garden Life: A Cozy Simulator | Authored restoration expands through areas, seeds and planting without replacing the basic gardening verb. |
| `loddlenaut` | Loddlenaut | Multiple biomes reuse a small interaction vocabulary while giving each place a distinct ecological identity. |
| `alba` | Alba: A Wildlife Adventure | Compact authored areas use landmarks and local identity instead of adding heavy navigation systems. |
| `a-short-hike` | A Short Hike | Hand-authored traversal demonstrates readable local routes and landmarks with minimal meta-UI. |
| `grow-evertree` | Grow: Song of the Evertree | Materially different counter-model: world-seed/generative scope can multiply systems and content-management complexity. |

## Selected references

### Garden Life — authored restoration plus expression

Observed behavior: progression opens/restores authored garden areas while seeds and planting remain expression inside the same overall activity.

Inference for BeBee: Golden Fields can be a new authored region made from new Meadows, species and landmarks while keeping native campaign completion separate from player-shaped planting. A second inventory/currency/world-management layer is not justified by the second region alone.

### Loddlenaut — biome identity through reused interactions

Observed behavior: distinct biomes change local ecological presentation and goals while the player keeps using the familiar movement/cleanup/upgrade vocabulary.

Inference for BeBee: Golden Fields should feel different through layout, flower families, palette and landmarks, not through a new primary input or progression branch.

## Anti-pattern / materially different alternative

### Grow: Song of the Evertree — generative world expansion

World Seeds and broader world-management systems create a much larger systemic content surface.

Lesson for P7: do not introduce procedural/generative region production, world-seed management, or settlement/meta-management merely because content volume is increasing. BeBee's current product rule is authored readability and a very small core loop.

## Official technical constraints

### Defold collection proxy

Source: https://defold.com/manuals/collection-proxy/

A collection proxy loads a separate game world with its own lifecycle/resources. That overhead is useful when a genuinely separate world/lifecycle is required, but Golden Fields does not require another game world. P7 therefore keeps the second region in the already-proven authored world instead of creating one proxy per region or Meadow.

### Defold collection factory

Source: https://defold.com/manuals/collection-factory/

Collection factories spawn content into the current world. This supports the broader architectural direction that authored expansion should remain data/content in the current world until a real lifecycle/memory requirement proves otherwise.

### Defold GUI node budget

Sources:

- https://defold.com/manuals/gui/
- https://defold.com/manuals/optimization-memory/

A GUI scene exposes `Current Nodes` and `Max Nodes`; Defold recommends keeping GUI node counts close to what is actually required instead of simply inflating preallocated limits. The first Golden Fields browser run exposed the concrete scaling defect: the old GUI allocated a full flower visualization for every authored patch and exceeded the scene's `max_nodes: 512` at 12 patches.

P7 repairs this as architecture rather than raising the limit: the runtime GUI uses a fixed six-slot patch-visual pool and rebinds those slots to nearby authored patches. Total authored patch count no longer determines dynamic patch-node allocation.

## Alternatives

### A — selected: one continuous authored world + data-driven ordered regions

- Region identity and order are catalog data.
- Active region is derived from the first incomplete region in catalog order.
- Golden Fields uses existing movement, pollination, Honey, Buzz/Flight, restoration, analytics and save state.
- Region content adds two flower families, four Meadows and landmarks.
- Patch visuals use a bounded pool rather than one permanent GUI subtree per patch.

Why selected: it directly tests the P7 scaling hypothesis and preserves the P6 seams.

### B — rejected: collection proxy per region

Why rejected: Golden Fields does not yet need a separate world lifecycle. It would multiply lifecycle/input/resource surfaces before a concrete memory/load requirement exists.

### C — rejected: world-map / region-selection screen

Why rejected: adds a new screen/navigation verb before continuous traversal has failed. P6 already proved landmark-led authored navigation.

### D — rejected: new Golden currency or new upgrade track

Why rejected: no second-region need justifies another economy. P6's Flight/Buzz 3 and Honey remain sufficient gates/rewards, and D-009/D-010 favor progression capability over payment gates.

### E — rejected: simply increase GUI `max_nodes`

Why rejected as the production fix: it masks linear per-patch visual allocation and moves the same failure to a later region. The selected bounded visual pool keeps the existing 512-node scene budget and makes the renderer scale with visible complexity instead of total catalog size.

## Authored Golden Fields slice

- Region: `region_02` / **GOLDEN FIELDS**.
- Meadow 1: **SUN GATE** — Sunflower, Buzz 3, follows Sunny Meadows Lily completion.
- Meadow 2: **POPPY RUN** — Poppy.
- Meadow 3: **WINDMILL LOOP** — Sunflower + Windmill landmark.
- Meadow 4: **HARVEST CROWN** — Poppy + Golden Wind Vane identity.
- Total new first-time Honey rewards: `125 + 130 + 140 + 150 = 545`.
- Proven P6 max-first-sink completion state starts P7 at `346 Honey`; completing Golden Fields with no new mandatory spend ends at `891 Honey`.
- No new required purchase, replay, currency or upgrade branch.

## Acceptance criteria

1. P1–P6 Test/data and browser evidence remain green.
2. Completing Sunny Meadows activates `region_02` automatically from derived campaign state.
3. Golden Fields begins at 0/4 with `RESTORE SUN GATE · 0/4`.
4. Sun Gate is a real Buzz-3 continuation gate and Sunflower/Poppy use species-specific presentation rather than palette-only aliases.
5. All four Golden Fields Meadows complete through the same movement-through pollination verb.
6. P6 max-first-sink state `346 Honey` completes all four P7 patches with no mandatory replay/spend and ends at `891 Honey`.
7. Golden Fields completion, Honey and campaign state survive a real browser reload through the existing save abstraction.
8. Analytics attributes patch/meadow/region completion to `region_02` without a platform SDK dependency.
9. Desktop and mobile landscape canvas coverage remain full-frame with zero browser/runtime errors or external requests.
10. GUI patch rendering remains under the existing `max_nodes: 512`; authored patch count must not allocate one permanent flower subtree per patch.
11. The retained exact-head artifact includes a real `region_01 → region_02` journey rather than only injected Golden Fields fixtures.
12. Remaining rounded-bee/final-typography art-direction debt is explicitly evaluated; Golden Fields acceptance must not be mislabeled final production-art certification.

## Iteration trace

### Iteration 0 — naive authored expansion

Head: `ba4c4be33f7353944a5ff5ea1389e04948a79eb4`

- Repository standards: PASS.
- Test/data: PASS.
- Pages preview: PASS.
- HTML5 CI: FAIL.
- Exact runtime failure: `ERROR:GUI: Could not create the node since the buffer is full (512)` / `Out of nodes (max 512)` while constructing per-patch flowers.

Interpretation: this was a genuine P7 architecture failure, not a flaky test. Static one-visual-tree-per-patch does not satisfy the production-expansion premise.

### Iteration 1 — bounded patch visual pool

Head begins at commit `3e4bbba91d69b6af23df35b91e19e30516abcf8f`.

- Keeps GUI `max_nodes: 512` unchanged.
- Allocates six reusable patch visual slots instead of one full subtree for every catalog patch.
- Selects nearby patches by camera distance and rebinds species/state/progress to those slots.
- Preserves authored patch state in the gameplay controller; GUI remains presentation-only.

Final acceptance is determined only by exact-head Test/data + HTML5/Chromium + retained evidence and independent evaluation. This document does not predeclare the verdict.
