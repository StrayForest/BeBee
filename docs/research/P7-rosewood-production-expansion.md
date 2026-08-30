# P7 — Rosewood production expansion research

## Question

Can BeBee add a fourth authored region with a clear woodland/rose identity while continuing to use the validated movement-through pollination, Honey, Flight/Buzz, restoration, save, analytics and bounded presentation systems?

Rosewood must remain a content expansion, not a new game layer. It must not introduce a new traversal verb, a second currency, a mandatory spend, lethal hazards, per-region lifecycle, procedural generation or a separate management screen.

## Existing decisions and constraints

- `D-002`: Honey remains the single MVP currency.
- `D-006`: movement-through/sweep remains the core pollination interaction.
- `D-010`: world gates default to restoration/progression/Buzz rather than Honey payments.
- `D-012`: canonical order is Sunny Meadows → Golden Fields → Wetland Garden → Rosewood → Alpine Bloom → Moon Garden.
- `T-013`: authored expansion remains data-driven in one continuous gameplay world; patch presentation is bounded by visible complexity rather than total catalog size.
- `docs/04-world-content.md`: Rosewood identity is woodland clearings with rose and bluebell flora.
- P7 roadmap: regions need authored content/data, research-first evidence, bounded runtime complexity and explicit treatment of the geometric-art deviation.

## Candidate pool

### A Short Hike — selected reference

Source: https://ashorthike.com/

Observed:

- a compact authored landscape is remembered through distinct clearings, routes and landmarks;
- exploration remains low-pressure and readable without a large strategic navigation layer;
- environmental composition carries orientation and reward.

Transferable to BeBee:

- use a sequence of woodland clearings with readable entrances and landmarks;
- vary silhouettes and framing while retaining one familiar movement/restoration loop;
- keep the HUD sparse and let authored layout communicate progression.

Not transferred:

- climbing/gliding as player verbs, quest structure and collectible progression are outside Rosewood.

### Alba: A Wildlife Adventure — selected reference

Sources:

- https://www.albawildlife.com/
- https://www.albawildlife.com/environment/

Observed:

- authored habitat context and recognizable landmarks differentiate nearby spaces;
- low-pressure exploration uses environmental clues rather than combat or a dense HUD;
- ecology is communicated through place identity and recovered life.

Transferable to BeBee:

- use Rose Arbor, Bluebell Arch, Cedar Turn and Woodland Crown as orientation anchors;
- make restoration visually legible through staged canopy, root and flower accents;
- keep Rosewood non-lethal and compatible with the existing relaxed pacing.

Not transferred:

- photography, quest dialogue and advocacy/narrative systems are outside this slice.

### Garden Life: A Cozy Simulator — selected reference

Source: https://store.steampowered.com/app/1915380/Garden_Life_A_Cozy_Simulator/

Observed:

- garden identity comes from plant variety, authored beds and incremental visual growth;
- the core gardening vocabulary remains stable while local composition changes;
- customization is presented as a positive expression rather than a progression penalty.

Transferable to BeBee:

- Rose and Bluebell are two readable native flower families with distinct silhouettes;
- authored restoration stages should add detail without changing the pollination verb;
- first-time rewards continue an explicit no-replay/no-mandatory-spend economy path.

Not transferred:

- freeform garden editing, simulation-heavy growth and a separate decorating loop are not part of P7.

### Spiritfarer — counter-model / intentionally rejected architecture

Sources:

- https://thunderlotusgames.com/spiritfarer/
- https://store.steampowered.com/app/972660/Spiritfarer/

Observed:

- the experience depends on a broad set of character, vehicle, resource and task-management systems;
- new places can imply new schedules, dependencies and management layers.

Why it is useful as a counterexample:

Rosewood could become a pretext for forestry tasks, a lumber resource, crafting, NPC schedules or a separate garden-management screen. That would make a region addition own new systems instead of scaling BeBee's validated loop.

Rejected for this slice:

- lumber or rose-specific currency;
- crafting/building or forestry tools;
- NPC schedule dependencies;
- a woodland management layer;
- procedural forest generation.

### Yonder: The Cloud Catcher Chronicles — counter-model / intentionally rejected architecture

Source: https://store.steampowered.com/app/580200/Yonder_The_Cloud_Catcher_Chronicles/

Observed:

- broad authored biomes coexist with crafting, farming, quests and multi-system progression;
- biome identity is often coupled to several resource and task systems.

Why it is useful as a counterexample:

The visual language of a forest must not be confused with a requirement for a forest-specific economy or a second progression tree.

Rejected for this slice:

- region-specific crafting materials;
- extra tool upgrades;
- quest-gated Rosewood lifecycle;
- biome-specific resource conversion.

## Selected BeBee slice

Rosewood is `region_04` in the same continuous authored world.

Proposed four Meadow beats:

1. `ROSE GLADE` — Rose introduction and the first open woodland clearing;
2. `BLUEBELL HOLLOW` — Bluebell silhouette plus a sheltered landmark composition;
3. `CEDAR TURN` — alternating canopy/root framing while the same traversal remains primary;
4. `WOODLAND CROWN` — strongest restored-canopy reveal and region climax.

Content rules:

- exactly two new native flower families: Rose and Bluebell;
- both reuse Buzz 3 rather than adding Buzz 4 or a new upgrade branch;
- four first-time rewards continue the no-mandatory-spend economy path;
- woodland decoration, roots and canopy are visual/orientation language, not collision traps or damage;
- the existing six-slot nearby-patch renderer remains unchanged in pool size;
- save schema stays v4 because stable campaign patch IDs fit the existing completion map;
- active region continues to derive from the first incomplete authored region;
- region completion emits the existing semantic analytics event through the platform-neutral adapter.

## World-layout constraint

Wetland Garden ends at the current eastern authored edge. Rosewood extends movement, camera and GUI world extents consistently. This is a measured content-scale bounds change, not a new lifecycle system.

The implementation must retain:

- `PATCH_POOL_SIZE=6`;
- `max_nodes=512`;
- deterministic clamp/soak coverage;
- one continuous gameplay-world lifecycle;
- existing save v4 and platform-neutral analytics boundaries.

## Visual direction for this slice

Rosewood must not be Wetland or Golden Fields recolored under a new label.

Minimum identity:

- deep woodland green and warm rose/bluebell accent palette;
- canopy, trunk, root and arch landmark shapes;
- Rose broad clustered silhouette;
- Bluebell narrow hanging silhouette;
- Rosewood-specific Meadow marker tint;
- retained Sunny Meadows, Golden Fields and Wetland visual regressions.

This does not claim release-candidate illustration or final typography. The P6/P7 geometric-art deviation remains explicit until the independent evaluator and the later P8 art-certification gate close it.

## Acceptance criteria

- persisted completion of regions 01–03 activates `region_04` at `0/4` through ordinary runtime derivation;
- Rose Glade, Bluebell Hollow, Cedar Turn and Woodland Crown complete through existing movement-through pollination;
- Rose and Bluebell are visually/species-distinct without adding a new core interaction;
- woodland identity is visible while roots, canopy and decoration remain non-lethal and introduce no collision trap;
- the Golden/Wetland max-first-sink end state `1596 Honey` completes Rosewood with no mandatory replay or spend;
- save v4 reload preserves all four authored-region completion states and Honey;
- `region_completed` analytics attributes Rosewood completion to `region_04`;
- movement/camera reach the expanded authored bounds and deterministic soak remains finite/bounded;
- six-slot patch pool stays bounded and `max_nodes=512` is not raised;
- desktop/mobile canvas, browser errors, external requests, FPS and bundle remain inside existing budgets;
- P1–P7 regressions remain green in the same retained artifact;
- independent post-implementation evaluation has no open `ITERATE`.

## Decision

Proceed with a fourth data-driven authored region and bounded woodland visual extension. Stop and repair architecture if real HTML5 execution shows a new total-catalog scaling failure or if Rosewood requires a new core system to be legible.

Evidence strength before runtime proof: LOW/MEDIUM. Final slice acceptance requires deterministic tests plus real Chromium evidence.
