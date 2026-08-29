# P6 — First Region Vertical Slice

Checked: 2026-08-29
Status: production implementation contract

## Problem

P1-P5 prove movement, pollination, progression, one restored Meadow and Hybrid seed ownership, but they still read as one compact test area rather than a coherent first region. P6 must turn those validated systems into one small complete game journey without introducing a second navigation architecture, a new combat/resource loop, or speculative portal code.

The player should be able to start from a clean save, understand where to go, restore six distinct authored Meadow beats, make at least one seed-ownership choice, buy capability/movement upgrades, finish Sunny Meadows, reload safely and recognize that the whole region changed.

## Decision status before implementation

- `D-004` authored Region -> Meadow -> Patch structure is LOCKED.
- `D-005` Hybrid native/player-shaped topology is VALIDATED.
- `D-006` movement-through pollination is VALIDATED.
- `D-007` Flight + Buzz are the vertical-slice upgrade tracks; later levels are explicitly tunable.
- `D-008` sparse HUD is VALIDATED.
- `D-011` six-Meadow first-region structure is still HYPOTHESIS and is the principal P6 content hypothesis under test.
- `T-010` collection-proxy lifecycle for major region/screen scaling remains HYPOTHESIS, so P6 must not make the six-Meadow structure depend on one proxy per Meadow.
- `P-001` Poki is the primary external validation target; direct web remains owned QA.

## Shipped-reference candidate pool

The pool is intentionally problem-specific: compact exploration/orientation, visible restoration, authored progression and player ownership.

1. **Garden Life: A Cozy Simulator** — authored garden restoration, unlockable areas, seed/decoration ownership and a story-mode path that remains compatible with free expression.
   - Official Nintendo description: https://www.nintendo.com/us/store/products/garden-life-a-cozy-simulator-switch/
   - Developer/Xbox Wire plant-system article: https://news.xbox.com/en-us/2024/02/22/theres-a-secret-high-tech-simulation-inside-garden-life-a-cozy-simulator/
2. **Alba: A Wildlife Adventure** — compact handcrafted island, relaxed traversal, local good-deed objectives and strong place identity without combat pressure.
   - Official site: https://www.albawildlife.com/?lang=en
   - Nintendo description: https://www.nintendo.com/store/products/alba-a-wildlife-adventure-switch/
3. **A Short Hike** — compact authored exploration with distinctive landmarks, paths/signs and curiosity-led orientation.
   - Public design summary: https://en.wikipedia.org/wiki/A_Short_Hike
4. **Grow: Song of the Evertree** — player actions visibly rejuvenate worlds; exploration and restoration are allowed to breathe rather than becoming a timed challenge.
   - PlayStation description: https://www.playstation.com/en-fi/games/grow-song-of-the-evertree/
5. **Terra Nil** — strong barren-to-thriving visual transformation and region/phased restoration language, but deliberately more systemic than BeBee.
   - Official site: https://www.terranil.com/

### Deep comparison: Garden Life

Observed facts:

- story tasks unlock tools, seeds, ornaments and new garden areas;
- the garden is authored, but plant placement/ownership remains expressive;
- visual plant variety comes from a small number of species rules rather than unrelated systems.

Adopted pattern:

- campaign restoration and player-shaped flower expression stay visibly separate but coexist in the same space;
- later areas reuse the same verbs while changing composition/route identity.

Not copied:

- no free-placement gardening simulation, request-board structure, plant-growth algorithm, models, art or UI.

### Deep comparison: Alba

Observed facts:

- the island is handcrafted and meant to be explored at the player's pace;
- distinct local places/landmarks carry orientation;
- the emotional payoff comes from doing small helpful actions in the world rather than combat or punishment.

Adopted pattern:

- one continuous authored first-region map with six locally distinct Meadow beats;
- readable landmarks/path language before adding a map/menu screen;
- restoration remains low-pressure and world-facing.

Not copied:

- no characters, photography mechanics, quest content, layout, art or narrative expression.

### Materially different reference: Terra Nil

Terra Nil validates the strength of phased ecological transformation, but its region progression is a system-heavy strategy puzzle. BeBee deliberately rejects importing that planning/building complexity. P6 uses authored routes and movement-through pollination so the region remains a flying/restoration game.

## Current official technical/platform documentation checked

### Poki requirements

- https://developers.poki.com/guide/requirements-quality — checked 2026-08-29.
- Current hard requirements include desktop/mobile/tablet support, a 16:9 canvas that proportionally covers the frame, incognito-safe behavior and no external runtime requests by default.

### Poki SDK events

- https://developers.poki.com/guide/sdk-overview — checked 2026-08-29.
- https://developers.poki.com/guide/sdk-defold — checked 2026-08-29.
- `gameLoadingFinished`, `gameplayStart` and `gameplayStop` are the relevant lifecycle signals. The gameplay domain must not call Poki directly; P6 therefore adds a platform-neutral analytics/lifecycle adapter seam and direct-web/no-op evidence, not a hardwired portal dependency.

### Defold sound

- https://defold.com/manuals/sound/ — checked 2026-08-29.
- Sound components support Wave/Ogg assets and group gain. Multiple overlapping plays can exhaust voices, so completion cues are gated by one completion transaction and mute uses mixer group gain rather than deleting components.

### Defold profiling

- https://defold.com/manuals/profiling/ — checked 2026-08-29.
- https://defold.com/manuals/optimization-speed/ — checked 2026-08-29.
- P6 records browser frame timing/build size and keeps profiling evidence measurable; it does not claim an optimization without a measured problem.

## Selected implementation

### Region topology

Validate the six-Meadow hypothesis as one continuous authored `region_01` map, not six collection-proxy screens.

| Meadow | Role | Route / landmark | Native challenge |
|---|---|---|---|
| `r01_m01` First Patch | tutorial + Hive + first ownership | Hive / starter clearing | existing Daisy, Clover, Lavender sequence |
| `r01_m02` Clover Bend | first route continuation | curved hedgerow / sign | Clover |
| `r01_m03` Lavender Bank | capability aspiration | raised lavender bank | Lavender, Buzz 2 |
| `r01_m04` Creek Garden | navigation variation | shallow creek + bridge | Daisy/Clover-grade traversal |
| `r01_m05` Tulip Rise | route/order landmark | warm rise / windmill silhouette | Tulip |
| `r01_m06` Lily Clearing | climax | lily ring / next-region silhouette | Lily, Buzz 3 |

Each later Meadow is intentionally compact in P6. It proves region rhythm and identity without multiplying patch count before external pacing evidence exists.

### Flower set

- retain validated Daisy / Clover / Lavender behavior;
- add Tulip as a medium late-region native species;
- add Lily as the strongest first-region native species and explicit Buzz-3 climax gate;
- flower behavior remains data-driven; visuals differ by silhouette/palette, not species-name conditionals in progression logic.

### Progression tuning

Use the earlier deterministic first-region candidate as the starting point for the two previously-unimplemented levels:

- Flight 3: `330 -> 360 u/s`, `56 Honey`, available after `r01_m03`;
- Buzz 3: `1.35x -> 1.65x`, `68 Honey`, available after `r01_m04`;
- Lily Clearing requires Buzz 3.

The exact speed/multiplier are P6 tunings, not new LOCKED values. Clean-save simulation must prove Buzz 2/Buzz 3 remain fundable without replay even when the player also buys both Flight upgrades and all P5 seed unlocks.

### Navigation and progress presentation

- no region-selection menu in the first region;
- one authored path ribbon and large local landmarks create forward direction;
- current objective remains the single persistent objective cluster;
- region progress is expressed as `SUNNY MEADOWS · x/6 RESTORED` inside that same cluster and on a world-space region marker, not as a third permanent HUD cluster;
- completed Meadows visibly retain restored color/detail.

### Accessibility/settings

P6 turns the existing reduced-motion support into a real player-facing setting and adds audio mute:

- `Esc` opens the existing focus-safe modal surface in `settings` mode;
- settings modal has `REDUCED MOTION` and `AUDIO` rows plus explicit ON/OFF or MUTED/ON text, so state is not color-only;
- reduced motion changes camera follow immediately;
- mute changes the Defold master sound group gain immediately;
- settings are persisted in save v4 and migrated from v3 with safe defaults.

### Audio

Add small original synthesized Wave assets produced for BeBee:

- a short pollination-complete chime;
- a stronger region-complete bloom cue.

No external audio assets or runtime requests are used.

### Analytics / portal seam

Add a platform-neutral lifecycle/analytics adapter with a deterministic direct-web/no-op implementation. P6 records at least:

- `session_start`;
- `first_input`;
- `patch_completed`;
- `meadow_restored`;
- `region_completed`;
- `settings_changed`.

This provides event semantics and testing without violating `T-005`; Poki SDK wiring remains adapter work, not gameplay-domain code.

## Rejected alternatives

1. **One collection proxy per Meadow** — rejected because `T-010` is still HYPOTHESIS and P6 should validate content rhythm before multiplying lifecycle/input ownership surfaces.
2. **World-map/menu navigation** — rejected because it adds a new screen and extra interaction cost before the first region proves that landmarks/pathing are insufficient.
3. **Six Meadows with many patches each** — rejected because autonomous evidence can prove structural coherence but cannot justify large content volume/pacing without later external playtest data.
4. **New currency or stamina for region progression** — rejected by D-002/D-003 and unnecessary for the P6 problem.
5. **Portal SDK calls directly from movement/progression code** — rejected by T-005/P-002.
6. **Audio through external web URLs or JS-only WebAudio** — rejected because Poki blocks external requests by default and Defold already supplies portable sound components.

## P6 acceptance / evidence contract

P6 may close only when the exact final PR head proves all of the following:

- clean-save browser journey reaches `region_01` completion with no replay reward/grind;
- all six Meadow IDs become restored in authored order and the final Lily gate is Buzz 3;
- at least one P5 player plot is planted during the clean-save journey and campaign completion remains independent;
- Flight/Buzz level 3 effects are real and purchase-safe;
- v3 -> v4 migration preserves Honey, upgrades, native completion, seed ownership and planted species while adding settings defaults;
- reload preserves completed region, settings, seeds and Honey;
- region-start / mid-region / region-complete deterministic captures exist on desktop, plus region-complete and settings captures at mobile-landscape size;
- visual evidence shows materially different local Meadow identities and obvious region-level restoration without adding HUD clutter;
- reduced-motion and mute settings are directly exercised and non-color text state is visible;
- analytics/lifecycle event schema is deterministic and no gameplay module imports a portal SDK;
- current Poki viewport/device/incognito/no-external-request checks pass in CI scope available to the repository;
- browser console/page/request errors remain zero for retained P6 proof;
- measured frame/bundle evidence stays inside the repository's declared P6 budgets;
- P1-P5 retained regression paths remain green on the exact same head;
- complete milestone manifest and separate evaluator record end in `PASS` or `PASS WITH DEVIATION`, never `ITERATE`.
