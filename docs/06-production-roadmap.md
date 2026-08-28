# 06 — Production Roadmap

## 1. Delivery strategy

The repository starts from zero. The correct path is not “build the full planet.” We ship increasingly complete playable slices, each of which is testable and releasable internally.

Milestone rule:

> Do not start the next milestone because the calendar says so. Start it because the current milestone's exit criteria are met.

---

## 2. Milestone overview

| Milestone | Goal | Player-visible result |
|---|---|---|
| P0 | Foundation | project boots reliably on HTML5 |
| P1 | Movement | bee feels good to control |
| P2 | Pollination loop | one patch can be completed for honey |
| P3 | Progression | honey buys meaningful upgrades |
| P4 | First meadow | complete restoration loop works |
| P5 | Customization | player replants restored patches |
| P6 | Vertical slice | one complete region, polished |
| P7 | Production expansion | more regions/content using proven pipeline |
| P8 | Release candidate | analytics, QA, distribution, launch readiness |

---

# P0 — Foundation

## Goal

Create a minimal, deterministic Defold project and CI path before gameplay complexity.

## Tasks

### BB-001 — Defold project bootstrap

- create `game.project`;
- bootstrap/main collection;
- basic app lifecycle controller;
- development and release build configuration;
- confirm HTML5 bundle launches.

### BB-002 — Repository standards

- `.gitignore`;
- `THIRD_PARTY.md`;
- contribution/PR template if useful;
- formatting/lint conventions;
- stable folder structure from architecture document.

### BB-003 — Input abstraction

- semantic actions;
- keyboard directional movement input;
- touch abstraction placeholder;
- input focus rules.

### BB-004 — Test harness

- pure Lua test runner or selected lightweight test dependency;
- first example unit test;
- CI command that fails on test failure.

### BB-005 — Build CI

At minimum:

- validate repository/data;
- run unit tests;
- produce/check HTML5 build.

## Exit criteria

- fresh clone can build with documented command;
- HTML5 build opens with no errors;
- CI runs on pull requests;
- no gameplay implementation is required yet.

---

# P1 — Bee Movement

## Goal

Make an empty field enjoyable to fly around.

## Tasks

### BB-010 — Bee controller

- normalized input vector;
- movement speed;
- acceleration/deceleration;
- collision against simple blockers.

### BB-011 — Camera

- follow smoothing;
- meadow bounds;
- aspect ratio checks;
- reduced-motion-compatible behavior.

### BB-012 — Bee presentation

Temporary art is acceptable, but behavior must support:

- idle/fly states;
- facing/turn lean;
- wing animation;
- simple completion reaction hook.

### BB-013 — Touch joystick

- floating joystick;
- deadzone;
- same movement vector contract as keyboard;
- portrait + landscape test.

## Exit criteria

- keyboard and touch movement feel consistent;
- no collision snagging in test arena;
- 5-minute movement playtest does not reveal camera nausea or obvious control frustration;
- target framerate stable in empty arena.

---

# P2 — Pollination Core Loop

## Goal

Prove the game's central verb before building menus/content.

## Tasks

### BB-020 — Flower data model

- flower definitions;
- stable IDs;
- difficulty/buzz requirements;
- reward data validation.

### BB-021 — FlowerPatch state machine

Implement:

```text
AVAILABLE -> POLLINATING -> BLOOMED
```

with pause-on-exit and no progress reset.

### BB-022 — Pollination trigger

- forgiving radius;
- automatic activation;
- enter/exit feedback;
- no per-flower collider spam.

### BB-023 — Bloom feedback

- staged opening;
- pollen particles;
- completion burst;
- SFX hook;
- bee reaction.

### BB-024 — Honey economy transaction

- reward formula;
- honey state;
- transaction validation;
- honey HUD.

### BB-025 — Save v1

Persist:

- honey;
- completed patch IDs;
- base player progression state.

## Exit criteria

A player can:

1. load the game;
2. fly to one flower patch;
3. pollinate it;
4. see it bloom;
5. receive honey;
6. refresh/relaunch;
7. see the completed state and honey preserved.

This is the first true playable build.

---

# P3 — Progression

## Goal

Create the reward-to-power loop.

## Tasks

### BB-030 — Upgrade data

Flight, Buzz, Yield definitions and costs.

### BB-031 — Hive interaction

- world-space affordance;
- open/close upgrade UI;
- no accidental movement input behind panel.

### BB-032 — Upgrade screen

- three cards;
- current/next values;
- affordability states;
- purchase feedback.

### BB-033 — Buzz gates

- soft gate modifier;
- hard gate state;
- explicit requirement UI;
- unlock toast after relevant upgrade.

### BB-034 — Progression persistence

Persist upgrade levels and gate-relevant state with migration tests.

## Exit criteria

- first honey can buy Buzz 2;
- effect is immediately measurable and visible;
- Lily-like hard gate communicates exactly why it is locked;
- reload retains upgrades;
- no negative honey transaction is possible.

---

# P4 — First Meadow Restoration

## Goal

Prove the visual “dead -> alive” promise.

## Tasks

### BB-040 — Meadow model

- required patch IDs;
- completion calculation;
- stable meadow ID;
- restoration stage state.

### BB-041 — Tutorial meadow layout

- 3–4 patches;
- Hive placement;
- visible future flower;
- route/landmark readability.

### BB-042 — Restoration stages

Implement authored visual stages:

- dormant;
- waking;
- growing;
- restored.

### BB-043 — Objective strip

- contextual tutorial objective;
- patch count;
- upgrade objective;
- no quest log complexity.

### BB-044 — Meadow completion event

- celebration;
- milestone honey reward if used;
- unlock next path;
- analytics hook.

## Exit criteria

- complete meadow can be understood without developer explanation;
- before/after screenshot difference is strong;
- no tutorial modal stack;
- first meadow completes in target onboarding window;
- state survives save/reload at every restoration stage.

---

# P5 — Seed Customization

## Goal

Turn restoration from a linear checklist into player ownership.

## Tasks

### BB-050 — Seed definitions/unlocks

- seed IDs;
- permanent unlock cost;
- availability rules;
- first seed grant.

### BB-051 — Restored patch customization state

Separate campaign-native completion from current planted species.

### BB-052 — Seed selector UI

- responsive bottom sheet/panel;
- locked/unlocked/planted states;
- one-action plant flow.

### BB-053 — Replant transition

- soil/seed feedback;
- bud state;
- one pollination pass establishes new flower;
- persistent visual selection.

### BB-054 — Save migration

Persist planted species independently from native patch identity.

## Exit criteria

- player can change a restored patch between at least three species;
- replant is reversible;
- campaign progression cannot be broken by planting another species;
- customization survives reload;
- player understands the feature without opening documentation.

---

# P6 — First Region Vertical Slice

## Goal

Produce one small game that feels shippable, not a collection of prototypes.

## Content

Six meadows from the world document:

1. First Patch;
2. Clover Bend;
3. Lavender Bank;
4. Creek Garden;
5. Tulip Rise;
6. Lily Clearing.

## Tasks

### BB-060 — Region navigation

- transitions/continuous layout decision;
- meadow boundaries;
- path unlocks;
- region progress state.

### BB-061 — Full first-region flower set

Daisy, Clover, Lavender, Tulip, Lily.

### BB-062 — Planet/region map

- region progress;
- planet bloom percentage;
- next region silhouette.

### BB-063 — Audio pass

- movement ambience;
- pollination;
- bloom;
- honey;
- upgrades;
- restoration;
- music state/layer.

### BB-064 — Art/polish pass

- consistent bee;
- flower silhouettes;
- terrain/landmarks;
- VFX;
- UI skin;
- no placeholder art in player-facing review build.

### BB-065 — Accessibility/settings

- music/SFX;
- reduced motion;
- text scale;
- haptics where available.

### BB-066 — Analytics implementation

Instrument core funnel/economy events.

### BB-067 — Vertical-slice balance pass

Tune using playtests and telemetry rather than intuition only.

## Exit criteria

- first region plays start-to-finish;
- no blocker/softlock;
- new player can complete without external help;
- meaningful choices among upgrades exist;
- seed system is used by playtesters;
- stable save across the whole region;
- responsive browser/mobile layouts pass;
- performance budgets pass;
- no placeholder critical UX/audio/art.

**Do not start mass content production until P6 passes.**

---

# P7 — Production Expansion

## Goal

Scale only the systems proven in P6.

## Workstreams

- Regions 2–6;
- additional flowers;
- new landmarks/environment sets;
- seed collection expansion;
- optional Accent flower system if validated;
- optional replay/regrowth mechanic if validated;
- localization;
- content balancing.

### Production rule

New regions should mostly be **content**, not new engine architecture.

If every new region requires core-system rewrites, stop production and fix architecture.

---

# P8 — Release Candidate

## Goal

Turn a complete game into a production product.

## Tasks

### BB-080 — Distribution integration

Select target(s):

- direct HTML5 hosting;
- Poki/CrazyGames or another portal if accepted;
- Android/iOS after browser validation.

Platform SDK lives behind adapter.

### BB-081 — Privacy/legal

- privacy policy;
- analytics disclosure/consent as required;
- third-party license review;
- store/portal metadata.

### BB-082 — Release performance pass

- startup/load profiling;
- memory/entity stability;
- dense restored meadows;
- mobile browser/device checks.

### BB-083 — Save resilience

- migration from every public beta save version;
- corrupt primary backup restore;
- reset flow requires explicit confirmation.

### BB-084 — Full QA matrix

- clean install;
- returning save;
- all region gates;
- all seed combinations within supported model;
- all upgrade levels;
- all aspect ratios;
- input transitions;
- pause/resume/background behavior.

### BB-085 — Release telemetry dashboard

Track:

- first-session funnel;
- meadow completion;
- upgrade distribution;
- seed usage;
- session length;
- crash/error indicators where available;
- performance telemetry where practical.

## Release gates

Production release requires:

- no known progression blocker;
- no known reproducible save-loss bug;
- complete game reachable from a clean save;
- release build has no debug-only secrets/tools exposed;
- analytics/privacy behavior approved;
- license inventory complete;
- distribution build loads reliably;
- player-visible performance is acceptable on representative low/mid devices.

---

## 3. Prioritization framework

When choosing between tasks:

1. progression blocker;
2. save/data loss;
3. control/feel defect;
4. comprehension/UX defect;
5. performance defect;
6. core-loop polish;
7. content;
8. optional meta systems;
9. monetization extras.

Never prioritize a new flower skin over a broken save or confusing pollination interaction.

---

## 4. Scope kill list

If schedule/scope becomes unstable, cut in this order before compromising core quality:

1. Accent species within one patch;
2. replay/regrowth economy;
3. ambient helper insects;
4. cosmetics;
5. advanced map fast travel;
6. extra regions beyond the minimum satisfying campaign;
7. seasonal/live content.

Do **not** cut:

- movement quality;
- pollination feedback;
- save reliability;
- upgrade clarity;
- restoration transformation;
- seed customization core;
- first-session onboarding.

---

## 5. Definition of “working product”

BeBee is a working product when a player can arrive with no instructions, understand the fantasy, complete a meaningful restoration journey, personalize the planet, leave and return without losing progress, and run the release build reliably on the target platform.

A repository full of systems does not satisfy this definition.
