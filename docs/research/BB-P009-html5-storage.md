# BB-P009 — HTML5 storage specification research

Research snapshot: **2026-08-28**.

## Problem

BeBee's HTML5 save path must survive corrupt files, failed writes, migrations and browser persistence delay without silently losing the only good copy or presenting a successful `sys.save()` as stronger durability than Defold actually guarantees.

## Current Defold constraints

### `sys.get_save_file`, `sys.save`, `sys.load`

Official source: https://defold.com/ref/stable/sys/

Current behavior checked 2026-08-28:

- `sys.get_save_file()` returns the platform-specific save location and may raise an error;
- HTML5 paths live inside IndexedDB-backed virtual storage;
- `sys.load()` returns an empty table for a missing file;
- corrupt, foreign or unsupported serialized data causes `sys.load()` to raise;
- `sys.save()` can raise on failure;
- `sys.save()` uses a documented 512 KiB output workspace ceiling;
- a single serialized table is limited to 65,536 rows.

Consequence: local adapter path/load/save boundaries use protected execution and explicit result codes. BeBee budgets far below 512 KiB.

### Defold file-access guidance

Official source: https://defold.com/manuals/file-access/

Defold's current file-access manual explicitly demonstrates `pcall(sys.load, path)` for recoverable corrupt/foreign/unsupported save data.

Consequence: protected load is mandatory, not optional defensive style.

### HTML5 IndexedDB persistence

Official source: https://defold.com/manuals/html5/

Defold HTML5 uses a browser virtual filesystem backed by IndexedDB. The current manual notes there may be a slight delay between writing a file and the change becoming persisted in the database.

Consequence: successful `sys.save()` is treated as accepted by the virtual filesystem, not proof that closing/reloading the page immediately cannot lose the newest browser-side change. Immediate-refresh/rapid-close tests are mandatory.

## Current Poki constraints

### Incognito

Official source: https://developers.poki.com/guide/requirements-quality

Poki currently requires incognito support and explicitly warns that local browser storage can be restricted. The game must remain playable.

Consequence: storage unavailable/failure is a supported degraded mode, not a fatal boot dependency.

### Cloud gamesaves

Official source: https://developers.poki.com/guide/accounts

Poki currently documents monitoring `localStorage` and IndexedDB for account cloud gamesaves and a 1 MB gzip-compressed gamesave limit.

Consequence: BeBee's local format fits comfortably below the portal ceiling if it obeys the stricter Defold/local 128/256 KiB budgets. However, Poki documentation does not by itself prove that the exact Defold/Emscripten IndexedDB filesystem layout behaves as desired for cross-device sync, so that remains a real-build verification gate.

## Recovery alternatives

### A — Single file only

Rejected.

A corrupt or interrupted write can remove the only usable generation. It provides no local rollback material.

### B — Primary + backup copied before/after writes

Rejected as the canonical protocol.

It can be made safe, but the ordering is easy to get wrong: a “backup” may accidentally copy already-corrupt or stale state, or a primary overwrite may happen before the backup is proven valid.

### C — Two-generation A/B journal

Selected.

Both slots are peers with monotonically increasing generation numbers. The highest valid generation is authoritative. The next write targets the missing/invalid/lower generation slot and is read back before success is reported.

Properties:

- the sole newest valid generation is never overwritten first;
- no mutable active-pointer file is needed;
- load can recover from either slot;
- failed candidate write/readback leaves the previous valid generation intact;
- order is based on generation rather than wall clock.

## Generation conflict rule

If both slots are valid and generation differs, highest wins.

If generations tie and canonical payloads are equal, either is equivalent.

If generations tie but payload differs, this is an explicit conflict. Preserve both and report diagnostics rather than silently claiming one is definitely newer. The P0 adapter may choose a deterministic fallback for playability, but must not overwrite evidence during load.

## Migration rule

Migration happens on an in-memory candidate after protected load and envelope validation. Sequential migrations advance `save_version` step-by-step, then domain invariants run again.

A migration failure must never overwrite the only valid pre-migration generation. A later successful explicit save may commit the migrated payload as a new generation.

## Size budget rationale

- 128 KiB warning catches save-shape growth early;
- 256 KiB release gate keeps large safety distance from Defold's 512 KiB hard ceiling;
- current Poki 1 MB compressed cloud limit is not used to relax the local budget.

The save should contain compact IDs/progression rather than serialized world snapshots, so these limits should be generous for the vertical slice.

## Durability semantics

The storage service separates write acceptance from durability:

- `not_written`;
- `accepted_local_pending_browser_persistence`;
- `durable_confirmed_if_future_adapter_can_prove_it`.

The local HTML5 adapter defaults to `accepted_local_pending_browser_persistence` after successful readback. This avoids a false “saved safely to disk” claim that current Defold HTML5 behavior cannot prove synchronously.

## Result

Selected pattern: **two-generation A/B journal with protected load/save, candidate readback validation, sequential migration and explicit pending-browser-durability semantics**.

Runtime implementation remains P0/BB-007. BB-P009 validates the contract and test matrix only.
