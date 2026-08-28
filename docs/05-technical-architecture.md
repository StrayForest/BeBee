# 05 — Technical Architecture

## 1. Authority

This document owns runtime architecture. Decision status lives in `DECISIONS.md`; current web/storage constraints live in `12-platform-storage.md`.

Do not build around a `HYPOTHESIS` as if it were a permanent interface unless the architecture deliberately isolates the experiment.

## 2. Goals

BeBee should be:

- small and fast in HTML5;
- straightforward to reason about;
- deterministic enough to test;
- safe to save/reload;
- data-driven for content/balance;
- easy to render in deterministic QA states;
- portable across direct web / portal adapters;
- scalable in content without core rewrites.

## 3. Engine

**Defold + Lua**.

Use current official Defold documentation for implementation details rather than memory or old samples.

## 4. Proposed repository layout

```text
BeBee/
├─ game.project
├─ README.md
├─ AGENTS.md
├─ DECISIONS.md
├─ THIRD_PARTY.md
├─ .agents/skills/
├─ .github/
├─ docs/
├─ input/
├─ main/
├─ app/
│  ├─ app_state.lua
│  ├─ commands.lua
│  ├─ events.lua
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
│  └─ camera/
├─ ui/
├─ systems/
│  ├─ economy.lua
│  ├─ progression.lua
│  ├─ storage.lua
│  ├─ analytics.lua
│  ├─ platform.lua
│  ├─ audio.lua
│  └─ settings.lua
├─ adapters/
│  ├─ storage_local.lua
│  ├─ platform_direct_web.lua
│  └─ portal adapters when selected
├─ levels/
├─ art/
├─ audio/
├─ tests/
└─ scripts/
   ├─ build.sh
   ├─ test.sh
   ├─ validate_data.*
   ├─ serve_build.*
   └─ capture_visuals.*
```

Exact directories may change, but dependency direction should not.

## 5. Dependency direction

```text
content/data
   ↓
domain systems (economy/progression/storage contracts)
   ↓
gameplay controllers
   ↓
presentation/view models
   ↓
GUI / VFX / audio presentation

platform/portal SDKs -> adapters -> internal platform/storage contracts
```

GUI does not own Honey, upgrades or campaign completion.

Portal SDKs do not appear inside FlowerPatch/Meadow/Hive gameplay code.

## 6. Application state

Persistent state is a plain versioned Lua table managed behind storage/save services.

Conceptual shape:

```lua
{
  save_version = 1,
  player = {
    honey = 0,
    upgrades = {},
    unlocked_seeds = {},
  },
  world = {
    campaign_completion = {},
    planted_species = {},
    restored_meadows = {},
    unlocked_regions = {},
  },
  settings = {},
  stats = {},
}
```

Important: campaign/native completion and planted/customization state are separate.

Derived values should be recomputed rather than serialized when practical.

## 7. Stable IDs

Persistent objects use authored IDs such as:

- `region_01`;
- `r01_m03`;
- `r01_m03_patch_04`;
- `flower_lavender`;
- `seed_lavender`.

Never persist array index, collection instance order or transient runtime URL as semantic identity.

Renaming a public persistent ID requires a migration.

## 8. Storage abstraction

Domain/gameplay code never calls `sys.save()` / `sys.load()` directly.

Internal contract:

```lua
storage.load(slot)
storage.save(slot, value)
storage.has(slot)
storage.delete(slot)
```

First implementation uses a local Defold adapter. Future portal/cloud adapters may coexist.

See `12-platform-storage.md` for current HTML5 constraints.

### Local adapter requirements

- path from `sys.get_save_file()`;
- `pcall`/protected corrupt-load handling;
- schema/version validation;
- sequential migrations;
- previous-good backup strategy;
- serialized-size diagnostics;
- explicit error result rather than silent data loss.

Current Defold documentation imposes a serialized `sys.save()` output ceiling around 512 KB. BeBee intentionally budgets far below it.

### HTML5 durability tests

Because HTML5 file persistence is backed by browser IndexedDB and can lag slightly after write, test immediate refresh/close scenarios rather than assuming synchronous durability.

## 9. Save triggers

Save after durable progression transactions such as:

- campaign patch completion;
- upgrade purchase;
- seed unlock/plant change;
- meadow restoration;
- region unlock;
- relevant settings changes.

Coalesce/debounce multiple events when appropriate without creating a window where a visibly granted reward is likely to vanish on normal navigation.

## 10. Economy system

Pure/testable Lua owns:

- Honey add/spend validation;
- upgrade cost/effect data access;
- reward calculation;
- no-negative-balance invariant.

Economy does not decide UI animation.

A deterministic simulation command must be able to exercise campaign paths outside the full rendered game.

## 11. Progression system

Owns:

- flower/capability eligibility;
- meadow/region completion;
- planet progress;
- seed availability rules;
- separation of campaign completion from planted expression.

Do not check specific species names in generic progression logic.

## 12. FlowerPatch controller

Owns local runtime interaction/presentation state for one logical patch.

It may:

- detect selected/validated pollination interaction;
- update local progress;
- trigger bloom staging;
- emit semantic completion once.

It does not:

- mutate Honey directly;
- write saves directly;
- own global meadow completion;
- manipulate arbitrary HUD nodes.

The exact pollination interaction is implemented only after P-1 validation.

## 13. Input architecture

Raw device inputs map to semantic actions.

Gameplay consumes normalized movement/action intent independent of keyboard/touch source.

### Input focus

Defold uses input focus stacks. Modal GUI must consume relevant input so gameplay does not continue behind it.

### Collection proxies

Collection proxies remain a `HYPOTHESIS` for major region/screen lifecycle until P0 proof.

Current official Defold behavior to account for:

- proxy-loaded collections are separate game worlds/physics worlds;
- input into a proxy world depends on the game object owning the proxy participating in the main input stack;
- each loaded world has its own input stack;
- loading many proxy worlds has memory cost.

P0 must prove the chosen lifecycle/input approach before content scales.

## 14. Scene/lifecycle strategy

Keep one long-lived bootstrap/application layer.

Candidate flow:

```text
bootstrap
 -> selected entry/onboarding shell
 -> region/gameplay world
 -> overlays/task-specific GUI
```

Do not architecturally require a standalone title/menu before gameplay because portal requirements may favor direct gameplay entry.

If collection proxies are retained, load only what is needed and explicitly manage enable/disable/unload and input focus.

## 15. UI architecture

Pattern:

```text
domain state/events
 -> presenter/view model
 -> GUI

GUI input
 -> command/domain call
 -> state change
 -> semantic event
 -> presentation update
```

Task-specific menus remain shallow.

Responsive layout behavior is tested at selected portal/device sizes, not only one desktop resolution.

## 16. Camera

Camera module owns follow/bounds/reveal behavior.

Rules:

- normal objectives do not yank camera away from bee;
- reduced-motion behavior supported;
- authored reveal may exist only when orientation remains understandable;
- camera tuning is validated with motion evidence.

## 17. Collision

Use collision sparingly:

- bee;
- meaningful world blockers;
- pollination/interaction areas as needed by the validated verb.

Decorative flowers generally do not collide.

Avoid detailed per-flower physics.

## 18. Rendering/VFX

One logical patch may display many flowers without making every petal a gameplay entity.

Use small authored sprite groups/batched decoration as appropriate.

Pool only where repeated spawn/despawn and profiling justify it (pollen, reward flyouts, ambient insects, transient text).

## 19. Platform adapter

Internal semantic API may include:

```lua
platform.gameplay_started()
platform.gameplay_stopped(reason)
platform.get_locale()
platform.get_safe_area()
```

Ads/cloud/account APIs are added only when required by the selected target and remain optional capabilities.

Gameplay must function when analytics/platform optional calls fail.

## 20. Analytics adapter

Gameplay emits semantic events; provider integration is behind an adapter.

No gameplay behavior depends on successful telemetry.

Never place private credentials in an HTML5 bundle/repository.

## 21. Localization

Player-facing copy uses keys from first implementation.

Do not scatter hard-coded English copy through scripts.

Exact launch languages are a product decision; font/assets must support chosen scripts and commercial licensing.

## 22. Deterministic QA states

Development builds should support deterministic test state injection for player-facing evidence.

See `13-visual-qa-scorecard.md`.

Requirements:

- known player/world state;
- repeatable camera position;
- deterministic content where practical;
- production-safe disable/removal;
- browser automation can load a state and capture artifacts.

## 23. Testing layers

### Pure Lua

- economy;
- gate eligibility;
- completion rules;
- planet progress;
- save migrations/validation;
- data references;
- economy simulation.

### Runtime smoke

- boot;
- input;
- validated pollination completion;
- Honey update;
- upgrade purchase;
- save/reload;
- planted state persistence;
- modal input isolation.

### Browser/storage

- normal persistence;
- immediate refresh/close cases;
- corrupt primary/backup recovery;
- selected portal/private-mode behavior.

### Visual

- deterministic screenshot/video artifacts for critical states.

## 24. Performance/load budgets

Target smooth 60 FPS on normal supported devices, with stable lower fallback preferred over unstable frame pacing.

Track early:

- initial bytes/time to playable state;
- total bundle/file count for selected portal;
- dense meadow frame pacing;
- memory across repeated region transitions;
- save hitch;
- VFX-heavy completion;
- representative low/mid mobile/Chromebook where relevant.

Exact portal budgets are set in P-1 after target selection.

## 25. Dependency policy

Every dependency/asset needs:

- clear need;
- pinned version/commit where appropriate;
- compatible license;
- `THIRD_PARTY.md` entry;
- current official docs/source review.

Do not add a framework because a reference project uses it.

## 26. Error handling

- optional analytics/platform failure -> continue gameplay;
- corrupt save -> protected recovery path;
- invalid content reference -> fail CI/dev loudly;
- duplicate stable ID -> fail validation;
- insufficient Honey -> transaction returns failure, balance unchanged;
- storage write failure -> surfaced in diagnostics and never reported as durable success silently.

## 27. Implementation sequence

Normal production begins only after P-1.

Then build the smallest vertical path:

```text
bootstrap/build/CI
 -> input + deterministic QA state
 -> movement
 -> validated pollination interaction
 -> one completion/reward
 -> storage save/reload
 -> one validated upgrade
 -> one meadow restoration
 -> validated seed/restoration flow
```

Do not scale regions, menus or art production before this path is proven.
