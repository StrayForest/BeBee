# BB-007 — local storage adapter and recovery harness

Status: implementation candidate

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

## Implementation

- `systems/storage/storage_service.lua`: semantic `load/save/has/delete` boundary.
- `adapters/storage/local_adapter.lua`: A/B generation selection, migrations, schema checks, size gate, write + readback verification, diagnostics and deterministic conflict fallback.
- `adapters/storage/defold_backend.lua`: protected Defold path/load/save/delete/measurement functions using stable application id `com.strayforest.bebee`.
- `systems/storage/migrations.lua`: sequential migration runner that requires each step to advance exactly one version.
- `tests/test_storage.lua`: adversarial in-memory cases for clean start, generation alternation, corruption, missing/invalid slots, equal-generation conflict, write/readback failures, migration, size gates, unavailable storage and partial delete.
- `app/storage_probe.lua` + `tools/visual_qa/storage_html5_smoke.py`: development-only real-browser persistence probe for normal reload, immediate refresh, rapid browser close/reopen, quick checkpoints and corrupt-newest recovery. Release must not expose the bridge.

## Durability semantics

A successful HTML5 save result means Defold accepted the local write and readback verified the target generation. It does **not** claim that IndexedDB has already completed durable browser persistence. The result therefore uses `accepted_local_pending_browser_persistence`.

## P0 acceptance mapping

- service boundary: implemented;
- A/B journal and deterministic selection: unit tested;
- corrupt `sys.load`: protected with `pcall` in Defold backend;
- serialized-size diagnostic and release gate: unit tested;
- previous generation survives failed write/readback: unit tested;
- migration fixture: unit tested;
- storage unavailable: explicit non-throwing result;
- normal reload, immediate refresh and rapid close/reopen: executed by the HTML5 browser smoke after CI wiring;
- diagnostics: generation, selected slot, recovery, serialized bytes and result code exposed.

Private/incognito behavior on the primary portal remains a P0/P8 platform case and is not treated as proof of local A/B correctness.
