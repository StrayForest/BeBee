# BB-007 — local storage adapter and recovery harness

Status: implementation + browser lifecycle validation in progress

## Problem

P0 needs a browser-local persistence boundary that does not let gameplay code depend directly on `sys.save`, `sys.load` or browser storage details. A successful call must not destroy the only known-good generation, corrupt files must be recoverable without crashing startup, and HTML5 durability must be described conservatively because Defold's virtual filesystem can flush to IndexedDB after the Lua write call returns.

## Governing contract

`config/storage-contract.json` (BB-P009) is the source of truth. BB-007 implements its two-generation A/B journal, readback verification, size budgets, migration path, explicit result codes and browser persistence tests. This ticket does not add cloud saves or portal account semantics.

## Current official constraints checked 2026-08-29

- Defold file access: https://defold.com/manuals/file-access/
  - use `sys.get_save_file()` to obtain a platform-correct save path;
  - use `sys.save()` / `sys.load()` for table persistence;
  - `sys.load()` can raise for corrupt/foreign/unsupported files, so loads must be protected with `pcall`;
  - HTML5 uses the browser virtual filesystem backed by IndexedDB.
- Defold sys API: https://defold.com/llms/apis/sys-lua/
  - `sys.get_save_file()` is the supported save-path API;
  - documented serialized output ceiling is 512 KiB, so BeBee keeps a stricter 256 KiB release gate and 128 KiB warning threshold.
- Defold HTML5 manual: https://defold.com/manuals/html5/
  - browser filesystem writes can reach IndexedDB with a delay; therefore BeBee reports `accepted_local_pending_browser_persistence` instead of claiming immediate durable persistence.
- Defold engine PR #9828 / generated `dmloader.js` behavior:
  - Defold patches `FS.close` on HTML5 so each close calls `Module.persistentSync()`;
  - `persistentSync()` coalesces asynchronous `FS.syncfs(false)` MEM→IndexedDB work;
  - therefore `sys.save()` already starts browser persistence through its file close, but completion can race navigation;
  - `os.remove()` does not pass through `FS.close`, so BeBee explicitly requests the same loader persistence sync after a successful delete and after deleting the temporary size-measurement file.

## Alternatives

### Selected: two-generation A/B journal behind a service boundary

Every explicit save writes the next generation to the missing, invalid or lower-generation slot. The current highest valid generation is never overwritten first. The new slot is loaded back and validated before success is returned.

Why selected:

- directly implements the validated BB-P009 contract;
- a failed write/readback can leave the prior valid generation intact;
- corrupt-load recovery is deterministic and diagnosable;
- no pointer file or wall-clock ordering is required.

### Rejected: single file overwrite

A failed or truncated replacement can destroy the only valid save. It does not satisfy BB-P009 recovery requirements.

### Rejected: timestamp-selected files

Wall-clock ordering is weaker than an explicit monotonic generation and can be affected by clock changes. BB-P009 explicitly avoids wall-clock ordering.

### Rejected: immediate repair during load

Overwriting the corrupt/invalid peer while merely loading destroys forensic evidence and turns a read operation into an implicit write. Repair is deferred to the next explicit successful checkpoint.

### Rejected: pretend pending HTML5 writes are durable

The browser lifecycle proof showed that a just-accepted generation can still be absent after an immediate navigation while the previous generation remains valid. Tightening the test to require the pending generation would contradict the documented durability value and Defold's asynchronous sync model. BeBee instead requires a bounded rapid-window invariant: either the latest pending generation survives, or the last previously confirmed persistent generation is recovered explicitly. Clean-start, corruption, unknown state or anything older than the last confirmed generation fails.

## Implementation

- `systems/storage/storage_service.lua`: semantic `load/save/has/delete` boundary.
- `adapters/storage/local_adapter.lua`: A/B generation selection, migrations, schema checks, size gate, write + readback verification, diagnostics and deterministic conflict fallback.
- `adapters/storage/defold_backend.lua`: protected Defold path/load/save/delete/measurement functions using stable application id `com.strayforest.bebee`; explicit HTML5 persistence sync after unlink-only operations.
- `systems/storage/migrations.lua`: sequential migration runner that requires each step to advance exactly one version.
- `tests/test_storage.lua`: adversarial in-memory cases for clean start, generation alternation, corruption, missing/invalid slots, equal-generation conflict, write/readback failures, migration, size gates, unavailable storage and partial delete.
- `tests/test_storage_preservation.lua`: migration-evidence preservation and durability-value contract cases.
- `app/storage_probe.lua` + `tools/visual_qa/storage_html5_smoke.py`: development-only real-browser persistence probe for normal reload, immediate refresh, rapid browser close/reopen, quick checkpoints, persistent delete and corrupt-newest recovery. Release must not expose the bridge.

## Browser finding from the first retained candidate

The first process candidate (`6ab34cbabf946d4b9908d8b7f4c9cd2486046ab8`, HTML5 CI run `33218660810`) deliberately failed before merge:

- normal save → settle → reload preserved `normal-save-reload`;
- a second save returned `accepted_local_pending_browser_persistence`;
- immediate navigation then loaded the previous confirmed generation 1 from slot A with `recovered_single_valid_slot` instead of the pending generation 2;
- no crash, schema corruption or unknown state occurred.

This is evidence that the A/B recovery design is doing useful work and that pending browser durability must not be relabeled as confirmed. It also exposed the separate unlink-sync gap fixed in the Defold backend.

## Durability semantics

A successful HTML5 save result means Defold accepted the local write and readback verified the target generation. It does **not** claim that IndexedDB has already completed durable browser persistence. The result therefore uses `accepted_local_pending_browser_persistence`.

For rapid refresh/close tests, the invariant is:

1. first establish and reload a confirmed generation;
2. write the next generation and verify the adapter reports pending durability;
3. refresh/close immediately, without an artificial settle delay;
4. after restart accept only:
   - the latest generation, if its async sync won the race; or
   - the last confirmed generation with explicit recovery metadata;
5. fail clean-start, corrupt/unknown state or any generation older than the last confirmed baseline.

Normal save/reload and quick-checkpoint tests still require the latest generation after a deliberate persistence settle window.

## P0 acceptance mapping

- service boundary: implemented;
- A/B journal and deterministic selection: unit tested;
- corrupt `sys.load`: protected with `pcall` in Defold backend;
- serialized-size diagnostic and release gate: unit tested;
- previous generation survives failed write/readback: unit tested;
- migration fixture: unit tested;
- storage unavailable: explicit non-throwing result;
- stable application id: `com.strayforest.bebee`;
- normal reload: latest generation required after settled persistence;
- immediate refresh / rapid close: latest-or-explicit-recovery-to-last-confirmed invariant;
- delete: reload must remain clean after settled persistence;
- diagnostics: generation, selected slot, recovery, serialized bytes and result code exposed.

Private/incognito behavior on the primary portal remains a P0/P8 platform case and is not treated as proof of local A/B correctness.
