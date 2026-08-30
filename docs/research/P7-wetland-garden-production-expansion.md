# P7 — Wetland Garden production expansion research

## Question

Can BeBee add a third authored region with a strong wetland identity while reusing the validated P1–P7 movement-through pollination, Honey, Flight/Buzz, restoration, save, analytics and bounded presentation systems?

The slice must not introduce lethal water, a new traversal verb, a second currency, a required spend, a world-map screen, per-region lifecycle or simulation-heavy fauna merely to make the biome feel different.

## Existing decisions and constraints

- `D-002`: Honey remains the single MVP currency.
- `D-006`: movement-through/sweep remains the core pollination interaction.
- `D-010`: world gates default to restoration/progression/Buzz rather than Honey payments.
- `D-012`: canonical order is Sunny Meadows → Golden Fields → Wetland Garden → Rosewood → Alpine Bloom → Moon Garden.
- `T-013`: authored-region expansion remains data-driven in one continuous gameplay world; patch presentation is bounded by visible complexity rather than total catalog size.
- `docs/04-world-content.md`: Wetland Garden proposal identity is water/roots/islands with Lotus/Iris; water edges are navigation language, not punishment.
- P7 roadmap: new regions should be mostly authored content/data and the geometric-art deviation should be reduced while content scales.

## Candidate pool

### Loddlenaut — selected reference

Source: https://www.loddlenaut.com/

Observed:

- ecological recovery is communicated through a visibly degraded-to-healthier environment;
- the ocean setting establishes a strong biome identity without requiring a separate strategic world-management screen for every local area;
- friendly aquatic life is presentation/reward language rather than combat pressure.

Transferable to BeBee:

- make water, reeds, roots and recovered-life accents the regional identity;
- preserve one familiar interaction vocabulary while the authored environment changes around it;
- keep fauna lightweight and non-blocking in this slice.

Not transferred:

- debris collection, survival/equipment loops and creature raising are unrelated core systems for BeBee.

### Alba: A Wildlife Adventure — selected reference

Sources:

- https://www.albawildlife.com/
- https://www.albawildlife.com/environment/

Observed:

- a compact authored natural space gains identity through landmarks, habitat variety and environmental context;
- the feel-good exploration loop is low-pressure and orientation comes from memorable places rather than a dense HUD;
- wetlands/mangroves are presented as valuable habitat, reinforcing water-edge ecology without punishment.

Transferable to BeBee:

- use a small number of readable landmarks and habitat silhouettes for navigation;
- keep the objective/Honey HUD sparse while world composition carries region identity;
- make Wetland restoration visually obvious without turning water into a lethal hazard.

Not transferred:

- photography, quest dialogue and advocacy/narrative systems are outside this slice.

### Terra Nil — counter-model / intentionally rejected architecture

Sources:

- https://www.terranil.com/
- https://store.steampowered.com/app/1593030/Terra_Nil/

Observed:

- restoration is driven by region-specific strategic transformation systems, buildings, biome conversion and resource-management decisions;
- maps and region phases are central mechanics rather than authored traversal content around one stable verb.

Why it is useful as a counterexample:

Wetland Garden could easily become a pretext for pumps, purification, water-level management, habitat requirements or a separate ecosystem economy. That would contradict the validated BeBee scope and turn a content slice into a new game layer.

Rejected for this slice:

- water-level simulation;
- purification/building tools;
- wetland-specific resource economy;
- region-management screen;
- procedural wetland generation.

## Selected BeBee slice

Wetland Garden remains `region_03` in the same continuous authored world.

Proposed four Meadow beats:

1. `LOTUS LANDING` — Lotus introduction and first broad water-edge composition;
2. `IRIS CHANNEL` — Iris silhouette plus narrow channel/root orientation language;
3. `ROOTWALK ISLES` — looping root/boardwalk landmark composition without a new movement verb;
4. `DRAGONFLY BASIN` — strongest wetland restoration reveal and region climax.

Content rules:

- exactly two new native flower families: Lotus and Iris;
- both reuse Buzz 3 rather than adding Buzz 4 or a new upgrade branch;
- four first-time rewards continue the no-mandatory-spend economy path;
- water is non-lethal visual/navigation language; no player damage, drowning or resource loss;
- the existing six-slot nearby-patch renderer remains unchanged in pool size;
- save schema stays v4 because stable campaign patch IDs fit the existing completion map;
- active region continues to derive from the first incomplete authored region;
- region completion emits existing semantic analytics events through the platform-neutral adapter.

## World-layout constraint

Golden Fields already occupies the current eastern world edge. Wetland Garden therefore extends authored world/camera bounds rather than overlapping existing Meadows. This is a content-scale bounds change, not a new lifecycle system.

The implementation must update movement, camera and GUI world extents consistently and extend deterministic soak/clamp coverage so the new bounds are measured rather than assumed.

## Visual direction for this slice

Wetland should not reuse Golden Fields colors under a new label.

Minimum identity:

- blue-green dormant/restored ground palette;
- translucent authored water channels/pools;
- root/boardwalk landmark shapes;
- Lotus broad radial silhouette;
- Iris tall narrow silhouette;
- wetland-specific Meadow marker tint;
- retained Golden/Sunny visual regressions.

This still does not claim release-candidate illustration. The P6/P7 geometric-art deviation remains explicit unless the independent evaluator can close it with evidence.

## Acceptance criteria

- persisted completion of regions 01 and 02 activates `region_03` at `0/4` through ordinary runtime derivation;
- Lotus Landing, Iris Channel, Rootwalk Isles and Dragonfly Basin all complete through existing movement-through pollination;
- Lotus and Iris are visually/species-distinct without adding a new core interaction;
- Wetland water/root/island identity is visible while water remains non-lethal and no new collision trap is introduced;
- Golden Fields max-first-sink end state `891 Honey` completes Wetland with no mandatory replay or spend;
- save v4 reload preserves all three authored-region completion states and Honey;
- `region_completed` analytics attributes Wetland completion to `region_03`;
- movement/camera reach the expanded authored bounds and deterministic soak remains finite/bounded;
- six-slot patch pool stays bounded and `max_nodes=512` is not raised;
- desktop/mobile canvas, browser errors, external requests, FPS and bundle remain inside existing budgets;
- P1–P7 regressions remain green in the same retained artifact;
- independent post-implementation evaluation has no open `ITERATE`.

## Decision

Proceed with a third data-driven authored region and bounded visual extension. Stop and repair architecture if real HTML5 execution shows a new total-catalog scaling failure or if Wetland requires a new core system to be legible.

Evidence strength before runtime proof: LOW/MEDIUM. Final slice acceptance requires deterministic + real Chromium evidence.
