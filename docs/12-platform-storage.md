# 12 — Web Platform & Storage Constraints

## 1. Purpose

HTML5 is the first runtime target, but “web” is not one platform. Direct hosting, Poki and CrazyGames impose different onboarding, SDK, size, storage and lifecycle constraints. These constraints must be considered before player-facing shell and save architecture are locked.

## 2. Current official constraints snapshot

Research snapshot: 2026-08-28. Re-check official docs before integration because portal requirements can change.

### Poki

Current official requirements include:

- desktop, mobile and tablet support;
- 16:9 scaling across documented canvas sizes;
- playable incognito/private-mode behavior;
- external requests blocked by default unless allowed;
- correct Poki SDK gameplay lifecycle events for releases;
- gameplay start should correspond to first real player interaction rather than mere page load.

Implication for BeBee:

- bundle required fonts/assets/libraries locally unless platform policy explicitly allows otherwise;
- storage failure/private-mode behavior is a release test;
- title/onboarding shell must not create unnecessary friction;
- platform event calls live behind `platform_service`.

### CrazyGames

Current official requirements/guidelines include:

- responsive desktop iframe sizes and mobile support when targeted;
- readable content across representative 16:9 resolutions;
- full implementation should land new users directly in gameplay, or at most require one click when immediate gameplay is not feasible;
- current technical file-size/file-count limits apply;
- SDK integration and gameplay-start lifecycle matter for full implementation.

Implication for BeBee:

- onboarding should work inside gameplay;
- a standalone decorative title sequence must not become architecturally mandatory;
- build/download budgets are tracked from the first production art import.

## 3. Platform selection gate

`BB-P006` must produce a comparison table and set `P-001` in `DECISIONS.md` to `VALIDATED` or `LOCKED`.

Compare at minimum:

| Concern | Direct web | Poki | CrazyGames |
|---|---|---|---|
| Entry-to-gameplay | | | |
| Desktop/mobile/tablet | | | |
| Aspect ratio | | | |
| Initial download | | | |
| Total bundle/file count | | | |
| External requests | | | |
| Local/cloud storage | | | |
| SDK lifecycle | | | |
| Ads | | | |
| Analytics/privacy | | | |
| Review/quality requirements | | | |

Do not choose solely by monetization. Choose the primary target that best fits a fast, cute, low-friction HTML5 game and our ability to satisfy quality requirements.

## 4. Platform adapter contract

Gameplay may call semantic functions only:

```lua
platform.gameplay_started()
platform.gameplay_stopped(reason)
platform.get_locale()
platform.get_safe_area()
platform.save_cloud(slot, payload, callback) -- optional adapter capability
platform.load_cloud(slot, callback)          -- optional adapter capability
platform.show_rewarded(reason, callback)     -- future only
```

A direct-web adapter may implement many operations as no-ops/local behavior.

No FlowerPatch, Hive, Meadow or economy script imports a portal SDK directly.

## 5. Storage architecture

Domain code talks to a storage service with a small contract:

```lua
storage.load(slot) -> result
storage.save(slot, value) -> result
storage.has(slot) -> bool
storage.delete(slot) -> result
```

The first adapter may use Defold local file APIs. Future adapters may wrap portal/account cloud storage.

### Local adapter constraints

Current Defold API documentation states that `sys.save()` serializes into an internal output workspace with a documented maximum output size around 512 KB and limits rows in an individual table. Treat this as a hard technical ceiling, not a target.

BeBee target:

- warning at 128 KB serialized save;
- release gate at 256 KB unless an explicit design review approves otherwise;
- never approach the engine ceiling as normal operation.

Persistent data should contain progression/state IDs, not large generated world snapshots.

### HTML5 persistence behavior

Defold HTML5 file operations use a virtual filesystem persisted through browser IndexedDB. Official documentation notes that there can be a slight delay between a write and the change being stored persistently.

Therefore:

- never assume `sys.save()` immediately guarantees durable browser persistence;
- avoid designing rewards that require an unsafe rapid write→navigate-away sequence;
- test immediate refresh/close cases;
- expose save state to diagnostics in development builds.

### Corruption handling

`sys.load()` can raise an error for corrupt/foreign/unsupported files. The adapter must load via protected execution and validate shape/version before accepting data.

Required conceptual flow:

```text
load primary safely
 -> validate
 -> if invalid: load backup safely
 -> validate
 -> if valid backup: recover + record recovery event
 -> otherwise: start clean without overwriting evidence until recovery path is decided
```

## 6. Save format principles

- `save_version` always present;
- stable IDs only;
- avoid serializing derived values that can be recomputed;
- customization state stored separately from campaign-native completion;
- transactional economy values validated before save;
- migrations run sequentially;
- migration tests cover every public version.

## 7. HTML5 storage test matrix

Before public beta:

- clean new save;
- normal save/reload;
- save then immediate refresh;
- save then rapid page close/reopen where test harness allows;
- multiple progression events in quick succession;
- corrupt primary + valid backup;
- missing primary + valid backup;
- both invalid;
- old save migration;
- private/incognito mode on primary portal/browser;
- storage quota/unavailable failure simulation where possible;
- portal cloud/local fallback behavior if cloud storage is introduced.

## 8. Bundle and startup budget

The exact budget is selected with the primary portal, but BeBee always tracks:

- initial bytes to first playable state;
- total compressed bundle;
- file count where relevant;
- time to first interactive gameplay on representative network/device;
- largest texture/audio contributors.

The game must not discover at P8 that its art pipeline is incompatible with its intended portal.

## 9. Official sources to re-check before implementation

- Defold `sys` API reference (`sys.get_save_file`, `sys.save`, `sys.load`)
- Defold HTML5 manual
- Defold file-access manual
- Defold collection proxy and input manuals
- selected portal's current technical/gameplay requirements
- selected portal's current Defold SDK extension documentation
