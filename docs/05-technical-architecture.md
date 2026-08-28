# 05 — Technical Architecture

## 1. Architecture goals

BeBee should be easy to reason about, cheap to run in a browser, deterministic enough to test, and structured so content can scale without rewriting core systems.

Primary goals:

- HTML5-first performance;
- stable save data;
- data-driven flowers/upgrades/regions;
- clean separation of simulation and GUI;
- low dependency count;
- minimal runtime allocation in hot gameplay paths;
- fast local iteration;
- straightforward automated validation.

---

## 2. Engine

**Defold + Lua**.

Why:

- strong 2D workflow;
- compact runtime and browser builds;
- official HTML5, Android, iOS and desktop support;
- input abstraction supports keyboard, mouse, touch and gamepads;
- GUI system is separate from world camera and supports responsive layouts;
- collection proxies can load/unload level collections;
- built-in profiling tools are available during development;
- `sys.save()` / `sys.load()` provide a simple local persistence foundation.

Do not introduce Unity/Godot runtime dependencies into the production game.

---

## 3. Proposed repository layout

```text
BeBee/
├─ game.project
├─ README.md
├─ AGENTS.md
├─ THIRD_PARTY.md
├─ docs/
├─ input/
│  └─ game.input_binding
├─ main/
│  ├─ main.collection
│  └─ bootstrap.script
├─ app/
│  ├─ app_state.lua
│  ├─ event_bus.lua
│  ├─ commands.lua
│  └─ constants.lua
├─ data/
│  ├─ flowers.lua
│  ├─ upgrades.lua
│  ├─ seeds.lua
│  ├─ regions.lua
│  ├─ meadows.lua
│  └─ economy.lua
├─ gameplay/
│  ├─ bee/
│  ├─ flowers/
│  ├─ meadow/
│  ├─ world/
│  ├─ hive/
│  └─ camera/
├─ ui/
│  ├─ hud/
│  ├─ hive/
│  ├─ seeds/
│  ├─ map/
│  ├─ pause/
│  └─ common/
├─ systems/
│  ├─ economy.lua
│  ├─ progression.lua
│  ├─ save_service.lua
│  ├─ analytics.lua
│  ├─ audio.lua
│  └─ settings.lua
├─ levels/
│  ├─ region_01/
│  └─ shared/
├─ art/
├─ audio/
├─ tests/
│  ├─ unit/
│  ├─ fixtures/
│  └─ smoke/
└─ scripts/
   ├─ build.sh
   ├─ test.sh
   └─ validate_data.py (optional tooling only)
```

Lua remains the gameplay language. A small Python validator is acceptable for CI/content validation but must not become a runtime dependency.

---

## 4. Boot and scene flow

`main/main.collection` is the bootstrap collection.

It owns only long-lived application-level objects:

- app controller;
- audio controller;
- save service;
- analytics adapter;
- screen/collection proxy controller.

Gameplay regions and major screens are loaded as collections rather than permanently keeping the whole planet active.

Suggested flow:

```text
bootstrap
 -> title collection
 -> region collection
 -> optional map overlay/screen
 -> title
```

Do not load every region and all flower assets at startup.

---

## 5. State model

Persistent player state lives in a plain Lua table managed by `app_state`/`save_service`.

Example conceptual state:

```lua
{
  save_version = 1,
  player = {
    honey = 0,
    upgrades = {
      flight = 1,
      buzz = 1,
      yield = 1,
    },
    unlocked_seeds = {
      daisy = true,
    },
  },
  world = {
    restored_meadows = {},
    patches = {},
    unlocked_regions = { "region_01" },
  },
  settings = {
    music = 1.0,
    sfx = 1.0,
    haptics = true,
    reduced_motion = false,
  },
  stats = {
    total_honey_earned = 0,
    total_patches_pollinated = 0,
  }
}
```

Gameplay objects should not be the source of truth for permanent progression.

---

## 6. Stable identifiers

Every persistent content object needs a stable authored ID.

Examples:

- `region_01`
- `r01_m03`
- `r01_m03_patch_04`
- `flower_lavender`
- `seed_lavender`

Never use collection instance order, transient URL strings or array position as persistent identity.

Renaming a persistent ID requires a save migration.

---

## 7. Save system

MVP uses local save.

Implementation:

1. obtain platform-valid path using `sys.get_save_file()`;
2. write a versioned Lua table using `sys.save()`;
3. load using `sys.load()`;
4. validate loaded shape/version;
5. migrate older versions sequentially;
6. if corrupt, retain a backup and initialize a clean state rather than crashing.

### Save triggers

Save after:

- patch completion;
- upgrade purchase;
- seed unlock/replant;
- meadow restoration;
- region unlock;
- settings changes;
- orderly pause/exit where available.

Debounce high-frequency saves if multiple progression events happen in one animation sequence.

### Backup strategy

Maintain at least:

- primary save;
- previous-good backup.

A write should not destroy the only recoverable state before the new state has been successfully serialized.

### Save migrations

Example:

```lua
local migrations = {
  [1] = function(save) return migrate_v1_to_v2(save) end,
  [2] = function(save) return migrate_v2_to_v3(save) end,
}
```

Never scatter migration conditionals across gameplay scripts.

---

## 8. Data-driven content

Gameplay balance data lives in Lua definition modules.

Example flower API:

```lua
local M = {}

M.by_id = {
  flower_daisy = {
    tier = 1,
    pollination_required = 3,
    base_honey = 10,
    min_buzz_level = 1,
    soft_gate = false,
  },
}

return M
```

Benefits:

- balancing does not require editing behavior scripts;
- tests can iterate all definitions;
- IDs can be validated in CI;
- designers/agents have one place to compare values.

Do not duplicate economy numbers inside scene files where avoidable.

---

## 9. Systems and responsibilities

### Bee controller

Responsible for:

- normalized movement input;
- acceleration/deceleration;
- facing/lean animation state;
- entering/leaving pollination trigger areas;
- player-local presentation.

Not responsible for:

- calculating economy rewards;
- saving data;
- deciding meadow completion;
- directly manipulating GUI node state.

### FlowerPatch controller

Responsible for:

- local patch state;
- pollination progress;
- bloom presentation staging;
- emitting completion event exactly once.

Uses flower definition data for requirements/reward reference.

### Economy system

Pure-ish Lua module responsible for:

- upgrade cost lookup;
- honey reward calculation;
- affordability;
- honey add/spend transaction validation.

Should be unit-testable without a Defold scene.

### Progression system

Responsible for:

- hard/soft gate checks;
- meadow completion;
- region unlock criteria;
- planet restoration calculation;
- seed unlock availability.

### Save service

Only persistence boundary.

Gameplay modules request persistence through app-level messages/events, not direct `sys.save()` calls everywhere.

### Analytics adapter

Gameplay emits semantic events to an internal interface. Provider-specific SDK integration sits behind the adapter.

Example:

```lua
analytics.track("patch_completed", {
  patch_id = patch_id,
  flower_id = flower_id,
  buzz_level = buzz_level,
  reward = reward,
})
```

No gameplay logic may depend on analytics success.

---

## 10. Event architecture

Use direct Defold messages when sender/receiver relationship is local and obvious.

Use a small app event bus only for cross-cutting domain events such as:

- `honey_changed`
- `upgrade_purchased`
- `patch_completed`
- `meadow_restored`
- `seed_planted`
- `region_unlocked`

Avoid turning every function call into an event. The goal is decoupling, not indirection.

---

## 11. Input architecture

Defold input bindings map raw inputs to semantic actions.

Input layer outputs one normalized movement vector.

Desktop:

```text
left/right/up/down -> movement vector
```

Touch:

```text
virtual joystick -> movement vector
```

Gameplay does not care whether the vector came from keyboard or touch.

UI input should consume relevant actions so joystick/world input does not activate behind modal screens.

---

## 12. Camera

Camera follows bee with damping.

Requirements:

- deterministic bounds per meadow;
- aspect-ratio-aware framing;
- no automatic objective camera yank;
- optional short authored reveal for a newly opened route only when control can remain understandable;
- reduced-motion setting disables/shortens nonessential camera animations.

The camera module exposes simple commands instead of allowing arbitrary scripts to manipulate it.

---

## 13. Collision

Use collision sparingly.

Gameplay collision groups:

- `bee`
- `world_blocker`
- `pollination_area`
- `interaction_area`

Decorative flowers should generally not have collision.

Pollination triggers are larger forgiving shapes around authored patches.

Avoid detailed per-flower collision geometry.

---

## 14. Flower rendering strategy

A patch may visually contain many flowers but should not require a heavy full game object hierarchy for every petal.

Preferred options depending on art implementation:

- small number of authored sprite game objects per patch;
- batched/tilemap-like decoration for non-interactive flowers;
- pooled transient particles/honey icons.

The gameplay patch controller remains one logical entity.

Profile before introducing custom rendering extensions.

---

## 15. Object pooling

Pool objects only when they are repeatedly spawned/despawned and profiling shows value.

Likely candidates:

- pollen particles;
- honey fly-to-HUD world effects;
- ambient insects;
- repeated transient text popups.

Permanent patch objects do not need pooling simply because pooling exists in reference projects.

---

## 16. UI architecture

Each major GUI scene has a small presenter/controller.

Pattern:

```text
Domain state/events
 -> view-model/presenter
 -> GUI nodes

GUI input
 -> command/domain call
 -> state mutation
 -> domain event
 -> GUI update
```

Do not make GUI scripts the owners of honey, upgrades or progression.

---

## 17. Localization

All player-facing strings use localization keys from the first implementation.

Example keys:

- `ui.play`
- `ui.continue`
- `upgrade.flight.name`
- `flower.lily.name`
- `objective.restore_meadow`

English can be the first content language, but code must not embed UI copy throughout scripts.

---

## 18. Audio architecture

Audio service exposes semantic calls:

- `play_ui(name)`
- `play_world(name, position)`
- `set_music_state(state)`
- `set_music_volume(v)`
- `set_sfx_volume(v)`

Music can layer as restoration progresses, but MVP should keep implementation simple.

---

## 19. Performance budgets

Targets for representative supported hardware/browser:

- gameplay: stable 60 FPS target;
- acceptable fallback: stable 30 FPS on lower-end devices rather than uneven frame pacing;
- no noticeable hitch on patch completion or save;
- first interactive load should remain small enough for casual web distribution;
- no unbounded world entity growth;
- region changes unload content no longer needed.

Concrete bundle-size budget must be established after first art/audio import. Track it in CI after the vertical slice exists.

---

## 20. Profiling policy

Profile these moments explicitly:

- cold startup;
- region load;
- dense restored meadow;
- many pollen/VFX effects simultaneously;
- seed replant transition;
- save operation;
- portrait mobile browser;
- low-end Android device/browser if available.

Do not optimize hypothetical bottlenecks before measurements.

---

## 21. Testing strategy

### Pure Lua unit tests

Prioritize:

- economy formulas;
- upgrade costs;
- gate eligibility;
- reward calculation;
- meadow completion;
- planet progress;
- save migration;
- data-reference validation.

### Smoke tests

Automate or script repeatable checks for:

- boot to title;
- start new game;
- movement;
- first patch completion;
- honey increases;
- upgrade purchase;
- save/reload;
- restored patch retains customization.

### Visual/manual QA

Capture milestone screenshots/videos for:

- movement and camera;
- pollination feedback;
- HUD responsive layouts;
- meadow before/after;
- seed transformation;
- region completion.

---

## 22. Dependency policy

Every external library/extension must have:

- a clear need;
- active maintenance or trivial replaceability;
- compatible license;
- entry in `THIRD_PARTY.md`;
- pinned version/commit where appropriate.

Prefer official Defold extensions or small focused dependencies.

Do not add frameworks simply because an open-source reference uses them.

---

## 23. Platform SDKs

Distribution SDKs such as Poki/CrazyGames should be integration adapters, not embedded in gameplay logic.

Example boundary:

```text
gameplay -> platform_service.show_rewarded_ad(reason)
```

If platform SDK is unavailable, gameplay remains functional with a no-op implementation.

No SDK integration belongs in the first movement/pollination milestone.

---

## 24. Error handling

Player-facing builds should fail soft where possible.

- missing optional analytics: continue game;
- corrupt save: attempt backup, then clean state with explicit log;
- missing flower definition: fail loudly in development/CI;
- invalid content reference: CI error;
- duplicate stable ID: CI error;
- insufficient honey transaction: return false, never produce negative balance.

---

## 25. Security/privacy baseline

MVP has no account/backend and should collect minimal analytics.

Before public analytics deployment:

- document provider and event payloads;
- avoid sending unnecessary personal data;
- provide required consent/privacy surfaces for target distribution/regions;
- never place secrets/API private keys in the repository or browser bundle.

---

## 26. Initial implementation sequence

Create the smallest end-to-end path first:

```text
game.project + bootstrap
 -> bee movement
 -> one patch trigger
 -> pollination state
 -> reward calculation
 -> honey HUD
 -> save
 -> one Hive Buzz upgrade
 -> reload and verify
```

Only then add the first meadow and content authoring pipeline.
