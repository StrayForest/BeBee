# 12 — Web Platform & Storage Constraints

## 1. Purpose

HTML5 is the first runtime target, but “web” is not one platform. Direct hosting, Poki and CrazyGames impose different onboarding, SDK, size, storage and lifecycle constraints. These constraints must be considered before player-facing shell and save architecture are locked.

`BB-P006` selected Poki as the primary external validation target with CrazyGames as fallback. `BB-P009` now owns a validated local-storage implementation contract at [`config/storage-contract.json`](../config/storage-contract.json).

## 2. Current official constraints snapshot

Research snapshot: 2026-08-28. Re-check official docs before integration because engine/portal requirements can change.

### Poki

Current official requirements include:

- desktop, mobile and tablet support;
- 16:9 scaling across documented canvas sizes;
- playable incognito/private-mode behavior;
- external requests blocked by default unless allowed;
- correct Poki SDK gameplay lifecycle events for releases;
- gameplay start should correspond to first real player interaction rather than mere page load.

Current account documentation also states that Poki cloud gamesaves monitor `localStorage` and IndexedDB and currently use a 1 MB gzip-compressed gamesave limit.

Implication for BeBee:

- bundle required fonts/assets/libraries locally unless platform policy explicitly allows otherwise;
- storage failure/private-mode behavior is a release test and may not crash/block play;
- title/onboarding shell must not create unnecessary friction;
- platform event calls live behind `platform_service`;
- do not assume Defold's IndexedDB virtual filesystem is cross-device synced by Poki until a real Poki build verifies that exact integration path.

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

## 3. Platform selection

`P-001` is `VALIDATED`:

- primary external target: **Poki**;
- secondary/fallback portal: **CrazyGames**;
- owned development/QA target: **direct web**.

See `docs/research/BB-P006-primary-web-target.md` and `config/web-targets.json`.

Platform selection does not change the storage-domain boundary: local save/recovery must function without portal accounts or cloud services.

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

## 5. Storage service boundary

Domain code talks to a storage service with a small contract:

```lua
storage.load(slot) -> result
storage.save(slot, value) -> result
storage.has(slot) -> bool
storage.delete(slot) -> result
```

Gameplay/domain code never calls `sys.save()`, `sys.load()` or a portal storage API directly.

Results expose semantic status rather than pretending every successful write is browser-durable:

```text
ok
code
durability
recovery
diagnostics
```

The first implementation uses a Defold local adapter. Portal/account cloud storage remains an optional adapter/platform capability.

## 6. Current Defold local-file constraints

Current official Defold documentation states:

- `sys.get_save_file()` returns the platform-specific application save path and can raise an error;
- on HTML5 the path is inside the browser's IndexedDB-backed virtual filesystem;
- `sys.load()` returns an empty table for a missing file but raises for corrupt/foreign/unsupported serialized files;
- recoverable loads therefore use protected execution (`pcall`);
- `sys.save()` uses an internal output workspace with a documented 512 KiB maximum output file size;
- an individual table is limited to 65,536 rows.

BeBee budgets per generation slot:

- warning: **128 KiB**;
- release gate: **256 KiB** unless an explicit evidence-backed technical decision changes it;
- engine ceiling: **512 KiB**, treated as a hard ceiling, never a target.

Persistent data should contain progression/state IDs and compact values, not large generated world snapshots.

## 7. BB-P009 local recovery protocol — two-generation A/B journal

A naive “write primary, occasionally copy backup” scheme can destroy the only recent valid copy if the primary write fails at the wrong time. BeBee instead uses two generation slots:

```text
save_a
save_b
```

Each valid file contains an envelope conceptually equivalent to:

```lua
{
  format_version = 1,
  generation = 42,
  payload = {
    save_version = 3,
    -- compact validated domain state
  }
}
```

### Load

1. Resolve both paths safely.
2. `pcall(sys.load, slot_a)` and `pcall(sys.load, slot_b)` independently.
3. Distinguish missing file from corrupt/error.
4. Validate envelope, positive generation, payload shape and `save_version`.
5. Run sequential migrations on an in-memory candidate.
6. Re-run domain invariants after migration.
7. If both are valid, choose the highest generation.
8. If only one is valid, recover from it.
9. Do **not** overwrite the invalid peer during load; preserve evidence until the next explicit save/checkpoint.

If two valid slots have the same generation and identical canonical payload, either is acceptable. If the generation ties but payload differs, record a generation conflict, preserve both and use the deterministic fallback defined by the adapter rather than silently pretending the conflict did not exist.

### Save

1. Validate domain invariants before serialization.
2. Build the next generation envelope.
3. Check serialized-size diagnostics/budget.
4. Choose the missing, invalid or lower-generation slot.
5. Never overwrite the sole highest valid generation first.
6. `pcall(sys.save, target, envelope)`.
7. Read the target back through protected `sys.load()`.
8. Validate generation/envelope/payload readback.
9. Only then report the local write as accepted.
10. Preserve the previous valid generation as recovery material.

No mutable “active slot” pointer file is required; ordering is determined by generation, not wall-clock time.

## 8. HTML5 durability semantics

Defold HTML5 file operations use a virtual filesystem persisted through browser IndexedDB. Official documentation notes that there can be a slight delay between a write and the change being stored persistently.

Therefore `sys.save()` success means:

> the Defold virtual filesystem accepted the write; it is **not proof of immediate IndexedDB durability**.

The local HTML5 adapter reports successful writes as conceptually:

```text
accepted_local_pending_browser_persistence
```

unless a future adapter/platform can explicitly prove a stronger durability state.

Rules:

- a visibly granted durable progression reward triggers a save checkpoint;
- UI must not claim stronger durability than the adapter can prove;
- avoid intentionally navigating/reloading immediately after critical progress when unnecessary;
- still test unavoidable immediate refresh/close cases;
- development diagnostics expose last result, generation, selected slot, recovery usage and serialized size.

## 9. Corruption and failure behavior

Failure is explicit rather than silently converted into “new game”.

Important cases:

- path resolution error;
- serialization/write error;
- readback failure;
- corrupt/unsupported slot;
- schema invalid;
- migration failure;
- both generation slots invalid;
- size release gate exceeded;
- partial reset/delete;
- browser storage unavailable/quota failure.

If one valid generation exists, gameplay may recover from it and report recovery diagnostics. If both are invalid, the application follows the explicit clean-start/recovery UX defined in P0 rather than overwriting both files immediately and destroying forensic/recovery evidence.

## 10. Save format principles

- `format_version` exists in the outer storage envelope;
- `save_version` always exists in the domain payload;
- generation is a positive integer and is the only save-order authority;
- stable authored IDs only;
- avoid serializing derived values that can be recomputed;
- customization state stored separately from campaign-native completion;
- transactional economy values validated before save;
- migrations run sequentially;
- migration tests cover every previously public supported version;
- failed migration never overwrites the only valid pre-migration generation.

Checksum/hash inside the save envelope remains open until P0 corruption tests show it adds value beyond `sys.load` errors + schema/domain validation. Do not add fake integrity complexity merely to make the format look sophisticated.

## 11. HTML5 storage test matrix

P0 must automate or explicitly exercise at minimum:

1. clean new save;
2. normal save/reload;
3. save then immediate refresh;
4. save then rapid tab/page close and reopen where automation permits;
5. multiple progression checkpoints in quick succession;
6. slot A corrupt + slot B valid;
7. slot B corrupt + slot A valid;
8. one slot missing + one valid;
9. both invalid;
10. equal-generation/different-payload conflict;
11. failed write preserves previous valid generation;
12. failed readback preserves previous valid generation;
13. old-version sequential migration;
14. migration failure preserves original generation;
15. 128 KiB warning behavior;
16. 256 KiB release-gate behavior;
17. storage unavailable/quota failure;
18. private/incognito play on the primary portal/browser.

If portal cloud save is introduced/reliably available later, add explicit cloud/local interaction and cross-device cases. Do not infer them from local tests.

## 12. Save triggers

Save after durable progression transactions such as:

- campaign patch completion;
- upgrade purchase;
- seed unlock/plant change;
- meadow restoration;
- region unlock;
- relevant settings changes.

Coalesce/debounce multiple events when appropriate without creating a window where a visibly granted reward is likely to vanish on normal navigation.

The coalescer may reduce redundant writes, but it may not cause a later lower-value event to replace/drop an unsaved critical progression checkpoint.

## 13. Poki storage boundary

Poki currently requires incognito playability and documents restricted `localStorage` behavior in incognito. BeBee must therefore remain playable when persistence is unavailable or fails.

Poki account documentation currently says its cloud gamesave system monitors `localStorage` and IndexedDB and uses a 1 MB gzip-compressed gamesave limit.

This does **not** prove that Defold's exact Emscripten/IndexedDB virtual-filesystem layout will automatically provide the cross-device behavior BeBee wants. Before relying on Poki cloud synchronization:

- upload a real Defold build;
- create save state through the production local adapter;
- verify what IndexedDB data Poki monitors/syncs;
- test guest -> account/login behavior where applicable;
- test cross-device restore;
- ensure two-generation files do not create cloud conflict behavior.

Local recovery correctness is mandatory regardless of cloud behavior.

## 14. Bundle and startup budget

The current web target budgets live in `config/web-targets.json`. BeBee also tracks:

- initial bytes to first playable state;
- total compressed bundle;
- file count where relevant;
- time to first interactive gameplay on representative network/device;
- largest texture/audio contributors.

The game must not discover at P8 that its art pipeline is incompatible with its intended portal.

## 15. P0 storage exit criteria

`BB-007` / storage foundation is not complete until:

- the storage service and local adapter exist;
- gameplay has no direct `sys.save/sys.load` dependency;
- A/B generation recovery is implemented and tested;
- corrupt loads are protected with `pcall`;
- every new generation is read back/validated before success is reported;
- failed writes/readbacks prove the previous valid generation survives;
- serialized-size diagnostics enforce warning/release budgets;
- normal + immediate-refresh persistence tests run in HTML5;
- at least one old-version migration fixture exists;
- storage failure does not crash normal gameplay;
- diagnostics expose generation/recovery/size/result;
- private/incognito behavior is tested for the selected web target before public release.

## 16. Official sources to re-check before implementation

- Defold `sys` API reference (`sys.get_save_file`, `sys.save`, `sys.load`)
- Defold file-access manual
- Defold HTML5 manual
- Poki current requirements / account gamesave documentation
- selected portal's current Defold SDK extension documentation
