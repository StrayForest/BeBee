# P9 — Garden Experience Overhaul

- ticket: `P9-GARDEN-EXPERIENCE`
- change class: player-facing, economy, runtime presentation
- status: implementation in progress; validation is only complete after exact-head CI and retained-artifact inspection

## Problem

The current BeBee loop is visually flat and asks the player to infer too much:

1. the garden is represented by rectangular blocks instead of readable flower beds;
2. every bed reads as the same five-flower stack;
3. there is no clear home/portal/zone rhythm;
4. a player can wander toward pollination without a strong route signal;
5. pollination has no short spatial challenge;
6. the current sound palette does not distinguish arrival, success, and danger;
7. labels and progress bars can occupy the same visual band;
8. zones do not yet look like gardens;
9. flower placement is static;
10. there is no low-stakes pressure while travelling;
11. Honey has too few meaningful non-upgrade sinks.

The goal is a compact, legible, replayable loop that keeps the existing save contract and remains small enough for HTML5.

## Research candidate pool

| Product | Official source | Relevant pattern |
| --- | --- | --- |
| APICO | https://whitethorngames.com/apico | Bee/plant care is broken into tactile, short rituals with immediate feedback. |
| Alba: A Wildlife Adventure | https://www.albawildlife.com/ | Compact spaces present one understandable environmental task at a time. |
| Garden Story | https://www.rosecitygames.com/garden-story | Restoration makes the world visibly better while optional threats and small objectives add texture. |
| Pikmin 4 | https://pikmin4.nintendo.com/ | Route planning, compact challenge nodes, and readable goals make exploration feel intentional. |
| Strange Horticulture | https://apps.apple.com/us/iphone/story/id1740155670?l=ko | Plant identity can be taught through observable traits and constrained deduction. |
| Tinykin | https://www.tinykingame.com/ | Small exploration spaces and traversal puzzles keep the player moving between meaningful points. |

## Deep observations

### APICO

Observed from the official product description: beekeeping and flower work are framed as a sequence of hands-on interactions rather than one long passive wait. The transferable lesson is the cadence—approach, perform a short readable action, receive a distinct result. BeBee adopts this as portal arrival, three route beacons, and movement-through-pollination. It does not copy APICO's assets, UI, or minigames.

### Alba: A Wildlife Adventure

Observed from the official product positioning: the experience is organized around a small island and a series of understandable wildlife tasks. The transferable lesson is spatial economy: a small zone can feel rich when the next action is obvious. BeBee uses small portal destinations and one active region at a time instead of exposing the full continuous world as the primary navigation problem.

### Garden Story

Observed from the official product positioning: restoring a community and dealing with threats are complementary activities. The transferable lesson is that optional pressure should add atmosphere and route choice, not punish the core restorative fantasy. BeBee's pests orbit the first bed, slow the bee briefly on contact, and never remove Honey or reset progress.

### Pikmin 4

Observed from the official product positioning: exploration is structured around route choices and small challenge spaces. The transferable lesson is to make traversal itself a decision. BeBee's three ordered checkpoints are a lightweight route puzzle: wrong order is safe but does not advance the route; correct order unlocks the beds.

### Strange Horticulture

Observed from the official product positioning: plant work is grounded in naming, traits, and observation. The transferable lesson is to keep labels tied to a visible object and avoid unexplained state changes. BeBee uses explicit portal labels, fenced beds, and a single separate progress band; the current implementation does not introduce a plant-identification screen because it would be a different core verb.

## Anti-pattern and materially different alternative

The anti-pattern is the current flat treatment: a large continuous field, identical rectangular beds, fixed flower coordinates, long labels over the same status band, and rewards without a visible spending decision. It produces movement without a destination and makes the player read implementation state rather than a garden.

A materially different alternative considered was a combat-first zone loop with enemy defeat as the gate. It was rejected because it would make combat the new core verb, conflict with the restorative tone, increase state/save complexity, and require more art/audio than the HTML5 budget justifies. The selected solution is route planning plus non-punitive pests: the garden remains the star, while the player gets a small amount of tension and choice.

## Selected solution

The runtime loop is now:

`home hive ightarrow active portal ightarrow compact zone ightarrow 3-beacon route ightarrow fenced flower pens ightarrow restore zone ightarrow timed return home`

- The home garden exposes six portals. Only the next playable portal is active; later portals stay locked until the previous region is complete.
- A zone starts with a three-checkpoint route puzzle. The checkpoints are ordered, wrong attempts have no penalty, and successful completion enables pollination.
- Pollination is limited to the active region. Pens use organic elliptical ground, wood rails, varied flower counts, and deterministic per-bed placement.
- A scent trail of warm dots runs from the bee toward the next route or flower target.
- Three orbiting pests create low-stakes pressure. Contact briefly reduces travel speed and plays a soft alert; no progress or Honey is lost.
- Home has a Garden Shop card with three one-time Honey sinks: Scent Lantern, Hive Garden, and Wildflower Bundle.
- Graphics are code-native GUI geometry and three short original synthesized PCM cues. No raster pack or third-party runtime dependency is added.

## Acceptance criteria

- Home, portal, zone, and return-home states are visually distinct.
- Only the next portal is enterable; the chain is deterministic and save-safe.
- Pollination cannot start before the route puzzle is solved.
- Fence/ground, varied count, and deterministic spread are visible in runtime evidence.
- The scent trail points to the current route or eligible pen.
- Pests are readable, non-lethal, and have bounded slow/alert feedback.
- Garden Shop spends Honey once, rejects locked/duplicate/unaffordable purchases, and persists through the existing save service.
- Objective, labels, and progress bars occupy separate visual bands at 1440x900 and 390x844.
- Existing v4 saves remain valid; new ephemeral route/pest state is not serialized.
- Defold node/audio constraints remain within the existing HTML5 budget and the view-state payload stays below the runtime message limit.
- Automated tests, repository standards, browser/evidence checks, trusted validation, and retained visual artifacts pass on one exact commit.

## Save and dependency impact

The only persisted addition is optional `world.honey_spends` in save v4. Existing saves without the table are treated as empty and remain valid; no migration/version bump is required. Route puzzle state, pests, timers, and visual guidance are ephemeral runtime state. No third-party dependency is introduced.

## Official implementation constraints checked on 2026-08-30

- Defold GUI boxes, pie nodes, text nodes, and dynamic node limits: https://defold.com/manuals/gui/, https://defold.com/manuals/gui-pie/, https://defold.com/manuals/gui-text/
- Defold sound components and runtime gating: https://defold.com/manuals/sound/
- Defold atlases and draw-call/bundle considerations: https://defold.com/manuals/atlas/

The implementation keeps the existing dynamic GUI approach, uses pie nodes for organic bed/portal/bee silhouettes, and adds only small mono PCM cues. The sound mute setting continues to gate the master group.

## Validation record

This section is updated only after the exact branch head has completed automated checks, browser/evidence capture, retained artifact inspection, and independent evaluation.
