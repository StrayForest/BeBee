# 06 — Production Roadmap

## 1. Delivery rule

Do not advance because the calendar says so. Advance only when the milestone exit criteria pass.

The roadmap started with **P-1 Blueprint Hardening** because the audit found several early design assumptions that were written before the repository adopted research-first development. **P-1, P0 Foundation, P1 Bee Movement, P2 Pollination Core Loop, P3 Progression, P4 First Meadow Restoration, P5 Seed Ownership During Restoration and P6 First Region Vertical Slice are complete for milestone closeout. P7 — Production Expansion is IN PROGRESS: Golden Fields, Wetland Garden and Rosewood are accepted slices; Alpine Bloom is the next production handoff.**

All milestone and merge gates are autonomous by default. No human review, approval, second GitHub account or manual action is required for phase progression.

## 2. Milestones

| Milestone | Goal | Main evidence |
|---|---|---|
| P-1 | Validate blueprint assumptions and evidence governance | research, prototypes, economy model, platform decision, machine-checkable evidence |
| P0 | Foundation | reproducible HTML5 build + CI + QA hooks |
| P1 | Movement | bee feels good to control |
| P2 | Pollination loop | validated core verb is satisfying and complete |
| P3 | Progression | Honey buys meaningful, non-dominant upgrades |
| P4 | First restoration | one meadow visibly changes from dormant to alive |
| P5 | Seed ownership | seed choice participates in restoration safely |
| P6 | Vertical slice | one coherent first region with measured web/device/performance proof |
| P7 | Production expansion | additional regions reuse proven systems |
| P8 | Release candidate | portal integration, QA, legal, telemetry, launch |

---

# P-1 — Blueprint Hardening

**Status: COMPLETE — exit criteria PASS.**

Detailed closeout: `docs/11-blueprint-hardening.md` and `docs/research/BB-P017-ruleset-closeout.md`.

## Required tasks

- `BB-P001` documentation consistency + decision registry;
- `BB-P002` retroactive problem-specific competitor benchmark;
- `BB-P003` pollination A/B/C micro-prototypes;
- `BB-P004` seed/restoration flow prototypes;
- `BB-P005` deterministic economy simulation;
- `BB-P006` primary web distribution decision;
- `BB-P007` visual style bible;
- `BB-P008` deterministic visual QA design;
- `BB-P009` HTML5 storage specification;
- `BB-P010` agent context/decision model;
- `BB-P011` reusable repository-local agent skills;
- `BB-P012` quality-gate enforcement design;
- `BB-P013` machine-readable evidence schema;
- `BB-P014` research selection / anti-confirmation protocol;
- `BB-P015` decision provenance + evidence-strength model;
- `BB-P016` separate player-facing evaluator protocol;
- `BB-P017` hard PR evidence/merge gates.

## Exit criteria

- core pollination interaction is `VALIDATED`;
- seed/restoration model is `VALIDATED`;
- upgrade set is validated and intentionally limited to Flight + Buzz;
- first-region economy has a no-grind path under exhaustive retained-sink purchase ordering;
- primary web target is selected;
- visual QA/style constraints are specified;
- storage/platform risks are specified;
- unresolved assumptions are explicitly `HYPOTHESIS`/`OPEN`, not disguised as facts;
- substantial decisions have explicit provenance/evidence strength;
- substantial player-facing/economy work has machine-readable evidence;
- reference selection includes a search-space/counterexample discipline rather than confirmation-only examples;
- substantial player-facing work has a separate evaluation pass;
- PR evidence CI validates structured evidence, not headings alone;
- `main` is protected by required PR/status checks with strict/up-to-date enforcement.

All criteria above pass. The repository ruleset closeout is retained in `evidence/BB-P017-RULESET-CLOSEOUT/`.

Do **not** build dependent production systems around downstream hypotheses that P-1 deliberately left for runtime validation.

---

# P0 — Foundation

**Status: COMPLETE — BB-001 through BB-007 complete; exit criteria PASS.**

## Goal

Create a deterministic Defold project, CI path and evidence pipeline.

### BB-001 — Defold bootstrap — COMPLETE

Delivered:

- root `game.project` with a minimal long-lived `app/` bootstrap collection/controller;
- explicit development/release settings;
- reproducible editor-independent HTML5 path;
- Defold `1.13.1`, Bob SHA-256, OpenJDK `25` and `wasm-web` pinned in a machine-readable toolchain contract;
- exact-head development + release HTML5 build proof;
- exact-head Chromium smoke capture and retained artifact.

The first fully successful runtime proof was GitHub Actions run `33201017563` on head `46d48bd265458b14e7b5d0a5673800ab39d50a3c`; the final merge head must repeat the same checks successfully. BB-001 intentionally leaves semantic input, collection-proxy focus/lifecycle, storage, test/data harness and deterministic gameplay QA to their scoped follow-up tasks.

### BB-002 — Repository/tooling standards — COMPLETE

Delivered:

- Defold-aware `.gitignore` covering editor/build state plus BeBee generated roots;
- `.editorconfig` and project-root `.luacheckrc` conventions;
- machine-readable `config/repository-standards.json` source/text/command contract;
- stable production runtime roots with misplaced Defold resources rejected by validation;
- machine-readable `config/dependencies.json` plus synchronized `THIRD_PARTY.md` license process;
- explicit Defold 1.13.1 engine/Bob provenance instead of treating the toolchain as no third-party technology;
- bidirectional validation between `game.project` Defold-library URLs and the dependency ledger;
- dependency-free `scripts/check_repository_standards.py` gate;
- exact-source PR/main `Repository standards` CI workflow;
- repository drift found by the new gate was repaired rather than grandfathered.

BB-002 does not implement or claim semantic input/proxy focus, test/data harness, full HTML5 PR artifact CI, deterministic gameplay capture or storage; those remain BB-003 through BB-007.

### BB-003 — Input and proxy-focus proof — COMPLETE

Delivered:

- semantic movement/action IDs instead of raw device keys in gameplay-facing code;
- W/arrow keyboard aliases and Space/Enter primary-action aliases;
- one HTML5 mouse/single-touch `pointer_primary` abstraction without prematurely choosing final touch movement UX;
- explicit main-world collection-proxy input ownership;
- a lower main-world sentinel plus proxied gameplay/modal listeners that expose the actual nested Defold input-stack behavior;
- modal focus acquisition, cross-stack consumption, release and restoration proof;
- frame-synchronized dependency-free Chromium CDP input injection retained in exact-head runtime evidence;
- `T-011` runtime behavior proven. BB-003 did not itself decide full region lifecycle; later P6/P7 multi-region evidence deprecates the old `T-010` per-major-region proxy hypothesis in favor of `T-013`.

The first fully successful behavioral runtime proof was GitHub Actions run `33205217201` on head `797271f19251529dfed5970d8b189ca0a1aa34bb`; the final merge head must repeat development/release builds, browser input/proxy smoke and repository/trusted evidence gates successfully. Detailed reasoning and scope boundaries are retained in `docs/research/BB-003-input-proxy-focus.md` and `evidence/BB-003/manifest.json`.

### BB-004 — Test/data harness — COMPLETE

Delivered:

- dependency-free deterministic Lua test runner with aggregate case reporting;
- dedicated Defold headless test bootstrap selected only through `tests/test.settings`;
- canonical content catalog plus stable-ID/reference validation;
- eleven initial deterministic cases covering merged input semantics plus positive/adversarial data validation;
- editor-independent `bash scripts/test.sh` command using the repository-pinned Defold/Bob/Java toolchain;
- timeout, complete log retention, one required structured `suite_end` event and non-zero failure propagation;
- PR/main `Test and data` workflow with read-only contents permission and retained diagnostic artifacts.

The exact stacked candidate `7c3aefb8112fd1385ddeeec760b3aa27b32548e2` produced `BB-004 tests: PASS (11/11)` and retained `summary.json`, the engine log and Bob build report. The first CI execution also correctly exposed the missing Ubuntu `libopenal.so.1` runtime dependency; CI now installs `libopenal1` rather than masking the failure. Detailed scope and alternatives are retained in `docs/research/BB-004-test-data-harness.md` and `evidence/BB-004-HARNESS/manifest.json`. Later P0 work can extend the suite while preserving this harness contract.

### BB-005 — HTML5 CI — COMPLETE

Delivered:

- one exact-source `HTML5 CI` workflow for every pull request and `main` update;
- repository-pinned development and release `wasm-web` builds;
- release Chromium startup/resource/console smoke requiring a usable canvas, successful `application/wasm` delivery, no actionable HTTP/network failures, no actionable console errors and no runtime exceptions;
- retained BB-003 keyboard/touch/proxy-focus browser smoke against the development bundle;
- dedicated `html5-playable-<sha>` release artifact separated from build/browser diagnostics;
- `html5-ci-evidence-<sha>` containing exact source SHA, browser logs/JSON, release screenshot, bundle hashes and Defold build reports;
- existing `Test and data` kept as an independent PR/main signal instead of rebuilding the BB-004 headless suite inside the browser job;
- read-only candidate execution kept outside the trusted `pull_request_target` governance authority.

The first strict run `33212975885` stopped on an error-level Chromium message; retained HTTP evidence identified the sole 404 as the browser's automatic `/favicon.ico` request while all Defold game resources, including `BeBee.wasm`, loaded successfully. The smoke was narrowed only for a Network-domain-proven favicon 404 while every other HTTP 4xx/5xx remains fatal. Exact candidate `3c50ca49d1b9fee8e39bac744e7d340e3f419963` then passed `Repository standards` (`33213154277`), `Test and data` (`33213154235`) and `HTML5 CI` (`33213154271`), retaining playable artifact `9702369697` and evidence artifact `9702370265`. Detailed reasoning and closeout proof are retained in `docs/research/BB-005-html5-ci.md` and `evidence/BB-005-CI/manifest.json`.

### BB-006 — Visual QA harness foundation — COMPLETE

Delivered:

- development/CI-only `?qa=<state>&qa_seed=<seed>` routing plus engine-owned `window.__bebeeQA` readiness/provenance bridge;
- release-mode hard disable of the QA bridge and explicit negative browser proof;
- exact source-commit binding injected through the canonical pinned Bob build path;
- infrastructure-only `foundation_probe` that proves the harness without falsely implementing future gameplay QA states;
- canonical local HTTP server with explicit `application/wasm` handling;
- pinned Playwright Python/Chromium tooling using fresh BrowserContexts per independent capture;
- deterministic 1280×720 desktop and 844×390 mobile-landscape still capture;
- two isolated repetitions per viewport with exact PNG SHA-256 equality for the unchanged foundation fixture;
- machine-readable `capture-report.json`, `console.log` and dedicated `visual-qa-<sha>` CI artifact;
- deterministic QA request/seed tests added to the existing Test/data harness;
- candidate Playwright execution remains read-only and separate from trusted `pull_request_target` governance authority.

The first complete proof was HTML5 CI run `33214438370` on exact head `56fa405c48d7c193c5e9888b825c48a0779c93a2` using Playwright Chromium `151.0.7922.34` and Defold `1.13.1`. Desktop repeats both hashed to `9efcf3f167dad760168b6d3fe14dc3b5126115960bda827260ac4687a8cc1f11`; mobile repeats both hashed to `046b359c483baeb1cae2240dd0c8a01000dab6509047b41e99197e746de2c471`; both viewports reported zero console/page errors, and release reported `bridge_present=false` / `probe_present=false`. Visual artifact `9702826036` has Actions digest `sha256:cabb48fd669f9f55e1482a55413538da6d33fbfb2c8fdeb9dfb22301d997593d`. Detailed reasoning and closeout proof are retained in `docs/research/BB-006-visual-qa-harness.md`, `docs/18-deterministic-visual-qa.md` and `evidence/BB-006-CI/manifest.json`.

The fifteen canonical future player-facing QA states remain semantic contracts owned by their actual gameplay/UI milestones; BB-006 does not claim they already render. Motion capture and selective golden-image policies are added only where later evidence requires them.

### BB-007 — Storage adapter proof — COMPLETE

Delivered:

- storage abstraction with a versioned domain-state contract;
- local Defold adapter with A/B generation journal and monotonic generation metadata;
- protected corrupt-newest fallback/recovery without silently treating corrupt data as valid;
- serialized-size diagnostics and explicit persistent-delete semantics;
- HTML5 lifecycle semantics that distinguish accepted/pending writes from confirmed browser-durable state;
- deterministic headless coverage for generation choice, recovery and delete behavior;
- real Chromium settled reload, immediate refresh, rapid close/reopen, corruption recovery, persistent delete and release-negative bridge proof;
- dedicated `storage-qa-<sha>` artifact retained by exact-source HTML5 CI on PR and `main`.

The first immediate-navigation process candidate exposed a real Defold VFS → IndexedDB race and PR #36 was closed unmerged rather than normalizing the failure. PR #37 corrected rapid-refresh/close recovery semantics. Final process PR #38 passed exact-head `Repository standards` (`33238316582`), `Test and data` (`33238316615`), `HTML5 CI` (`33238316601`) and trusted PR evidence (`33238419907`) on `5efabc3b24b6524984a452fbc1e8f9bd4afd1b3d`, then merged as `4bd31d40515772775a575762206a8c707b8a6fbc`. Merged `main` repeated `Repository standards` (`33238436244`), `Test and data` (`33238436138`) and HTML5/storage proof (`33238436135`), retaining storage artifact `9710629332`. Full evidence is retained in `evidence/BB-007-CLOSEOUT/manifest.json`.

## Exit criteria

- fresh clone builds reproducibly — PASS;
- CI produces a playable HTML5 artifact — PASS;
- test/data validation runs — PASS;
- one deterministic screenshot can be produced automatically — PASS;
- storage smoke test passes — PASS on exact candidate and merged `main`;
- input focus/proxy ownership is understood rather than assumed — PASS.

**P0 exit: PASS. Production advances to P1 — Bee Movement.**

---

# P1 — Bee Movement

**Status: COMPLETE — exit criteria PASS.**

## Goal

Make an empty test field enjoyable to fly through before resource content is added.

### Work

- normalized controller with acceleration/deceleration;
- camera follow/bounds;
- collision only where meaningful;
- bee idle/fly/turn presentation;
- selected desktop/touch input scheme;
- reduced-motion behavior;
- deterministic movement QA state.

## Validation

Research comparable movement/camera solutions first. Capture motion evidence, not screenshots only. Use a changed `evidence/<ticket>/manifest.json` and separate evaluation pass for the substantial player-facing result.

## Exit criteria

- 5-minute movement test exposes no obvious control/camera frustration — PASS through 18,000-frame/300-second deterministic soak plus retained motion evaluation;
- keyboard/touch produce consistent intent — PASS; both normalized paths reach 300 units/s and return to zero;
- no collision snagging — PASS; P1 uses authored bounds without decorative collision and central browser exercises report zero bound hits;
- representative target frame pacing is stable — PASS; accepted desktop browser exercise measured 61.40 fps;
- movement visual-QA comparison is `PASS` or approved deviation — PASS after iterating the initial undersized-bee finding into V-001's 12–15% band.

### P1 exit record

Accepted runtime evidence head before closeout-only source-of-truth changes: `2e1098ac10596d02ad7d8b71e6034b5e778a7315`.

- Repository standards `33240599831` — PASS;
- Test/data `33240599809` — PASS;
- HTML5 CI `33240599811` — PASS;
- movement artifact `9711246614` — retained desktop/mobile WebM, frame sequences, still states and `motion-report.json`;
- keyboard/touch cardinal/diagonal maximum speed 300 units/s; stopped speed 0;
- reduced-motion camera lag X/Y = 0.0 / 0.0;
- modal movement displacement = 0.0;
- console/page errors = 0;
- bee height = 14.17% desktop, 13.33% Poki small, 13.33% mobile landscape;
- separate evaluation verdict = PASS;
- complete evidence = `evidence/P1-BEE-MOVEMENT/manifest.json` and `evidence/P1-BEE-MOVEMENT/evaluation.md`.

**P1 exit: PASS. Production advances to P2 — Pollination Core Loop.**

---

# P2 — Pollination Core Loop

**Status: COMPLETE — BB-020 through BB-025 complete; exit criteria PASS.**

## Goal

Implement the **P-1 validated pollination interaction**, not the old auto-pollination assumption by default.

### BB-020 — Flower definition model — COMPLETE

- stable IDs;
- requirement/reward data;
- validation.

### BB-021 — FlowerPatch state model — COMPLETE

Production domain states:

```text
LOCKED / AVAILABLE / ACTIVE / COMPLETED
```

Presentation substates remain separate from persistent progression.

### BB-022 — Validated pollination interaction — COMPLETE

Movement-through/sweep uses forgiving authored bounds and actual travelled distance. The work target is above one complete forgiving-zone diameter so a center fly-through gives substantial progress but cannot complete an untouched patch.

### BB-023 — Bloom feedback stack — COMPLETE for P2 scope

- visible progress;
- staged flower opening;
- pollen/VFX;
- audio semantic hook;
- completion reaction;
- reward attribution.

Final illustration/audio polish remains later scope.

### BB-024 — Honey transaction — COMPLETE

- one currency;
- non-negative invariant;
- single-reward completion;
- HUD/reward feedback.

### BB-025 — Save v1 — COMPLETE

Minimal campaign patch completion and Honey persist through the existing A/B storage abstraction. Partial in-progress patch work intentionally remains session-local.

## Exit criteria

- player can fly and pollinate with movement only — PASS on keyboard and floating touch;
- stationary wait advances zero work — PASS, `0.0`;
- one straight fly-through cannot finish the first patch — PASS, 82.33% desktop / 82.92% mobile;
- return traversal completes and awards one Honey transaction — PASS, `+45`, transaction count `1`;
- dependent patch unlocks — PASS, patch #2 becomes `AVAILABLE`;
- reload preserves completion/Honey/unlock and replays no reward — PASS;
- required P2 states/HUD render without browser errors — PASS, 10 canonical stills with zero console/page errors;
- P1 movement/modal/reduced-motion and P0 storage regressions remain green — PASS;
- independent evaluation has no open `ITERATE` — PASS after two blocking visual iterations.

### P2 exit record

Accepted runtime evidence head before closeout-only source-of-truth changes: `bc3f878254d800063822377d57e99e7e5d42efd7`.

- Repository standards `33244624975` — PASS;
- Test/data `33244624972` — PASS;
- HTML5 CI `33244624996` — PASS;
- movement/P2 artifact `9712446750` (`movement-qa-bc3f8782…`), digest `sha256:585a74cc55eaac926034c3f16be3eacb0dee61654b67fb1a5aa961821d84fca7`;
- desktop straight fly-through `337.56 / 410 = 82.33%`, no completion;
- mobile straight fly-through `339.99 / 410 = 82.92%`, no completion;
- stationary work delta `0.0`;
- completion event `1`, reward transaction `1`, audio semantic hook `1`, Honey `+45`;
- patch #2 unlocks to `AVAILABLE`;
- reload: patch #1 `COMPLETED`, Honey `45`, patch #2 `AVAILABLE`, reward transactions `0`;
- representative desktop movement `60.98 fps`;
- modal displacement `0.0`, reduced-motion camera lag X/Y `0.0 / 0.0`, P2 console/page errors `0 / 0`;
- first functional green-CI artifact was rejected because the bee obscured the active flower cluster;
- second green-CI artifact was rejected because mobile `LOCKED` overlapped the Honey HUD;
- final retained desktop/Poki-small/mobile active stills resolve both blocking visual findings;
- separate evaluation verdict = PASS;
- complete evidence = `evidence/P2-POLLINATION-CORE-LOOP/manifest.json` and `evidence/P2-POLLINATION-CORE-LOOP/evaluation.md`.

### Autonomous milestone gate

P2 has the actual build, motion/rendered evidence, objective measurements, structured evidence, reference comparison, passing acceptance/test results and a separate PASS evaluation. The final closeout PR head must still repeat Repository standards, Test/data, HTML5 CI and trusted `validate-pr-evidence`, with a retained non-N/A `movement-qa-$PR_HEAD`, before merge.

**P2 exit: PASS. Production advances to P3 — Progression.**

---

# P3 — Progression

**Status: COMPLETE — BB-030 through BB-034 complete; exit criteria PASS.**

## Goal

Create a reward-to-power loop with meaningful choices and no mathematically compulsory filler stat.

### BB-030 — Validated upgrade set — COMPLETE

- the vertical slice keeps exactly **Flight + Buzz** (`D-007`); Yield remains excluded;
- Flight level 2: `300 -> 330 u/s`, cost `30 Honey`;
- Buzz level 2: `1.00x -> 1.35x` pollination work, cost `35 Honey`;
- later levels and final effect curves remain tunable rather than silently locked by P3.

### BB-031 — Hive/progression interaction — COMPLETE

A dedicated Hive surface implements one-action purchasing with two selectable cards, explicit current/next effect and Honey cost, atomic economy/progression ownership outside GUI, and modal input isolation. Purchase effects apply immediately.

### BB-032 — Progression UI — COMPLETE for P3 scope

The Hive renders exactly the two validated tracks rather than preserving the original three-card assumption. The accepted 1280x720 and 844x390 captures keep both cards complete and readable after a rejected mobile-readability iteration.

### BB-033 — Flower gates — COMPLETE for first production gate

Lavender patch #3 is the first explicit progression gate. After patch #2 it reports `LOCKED / requires_buzz / requirement 2` and visibly states `REQUIRES BUZZ 2`; buying Buzz 2 changes it immediately to `AVAILABLE`. The gate checks permanent capability rather than charging Honey directly, preserving D-010.

### BB-034 — Economy regression simulation — COMPLETE

CI/Test-data re-runs the candidate values across Flight-first, Buzz-first, the complete two-upgrade ordering, minimal-required progression and a customization-heavy shadow-spend path. The accepted candidate has no negative Honey, unintended replay requirement or progression dead-end.

## Exit criteria

- each shipped stat has an obvious experiential/economic purpose — PASS; Flight changes real traversal and Buzz changes real pollination capability/work;
- no upgrade is consistently mandatory or consistently ignored in the P3 choice slice — PASS; both are individually affordable from the first 45 Honey and both orderings progress safely;
- no negative Honey — PASS in atomic purchase invariants and deterministic economy regression;
- customization spending cannot create a progression dead-end — PASS in the customization-heavy regression;
- reload preserves progression — PASS for Flight level/speed, Buzz level/multiplier and resulting Lavender eligibility;
- P2 v1 saves migrate to v2 without losing Honey/campaign completion — PASS;
- Hive input isolation remains correct — PASS, modal movement displacement `0.0`;
- desktop/mobile progression surfaces and first Buzz gate are readable without browser errors — PASS after the blocking visual iteration;
- separate evidence-first evaluation has no open `ITERATE` — PASS.

### P3 exit record

Accepted runtime evidence head before closeout-only source-of-truth changes: `3b4b990923851217d9a25e2954a86443dea3916f`.

- Repository standards `33247411592` — PASS;
- Test/data `33247411586` — PASS;
- Pages preview `33247411600` — PASS;
- HTML5 CI `33247411645` — PASS;
- movement/P3 artifact `9713299114` (`movement-qa-3b4b9909…`), digest `sha256:f7e1ce37eba04ecec26a23b42991f7bea4681ecdde64feaec8d225a1f7101ef9`;
- Flight purchase: Honey `45 -> 15`, level `1 -> 2`, captured real cruise `330/330 u/s`;
- Flight reload: level 2, max speed 330 u/s, Honey 15;
- Hive modal movement displacement `0.0`;
- Buzz purchase: Honey `100 -> 65`, level `1 -> 2`, work multiplier `1.35x`;
- Lavender: `LOCKED / requires_buzz / 2 -> AVAILABLE` after Buzz purchase;
- Buzz reload: level 2, multiplier `1.35x`, Honey 65, Lavender `AVAILABLE`;
- representative P1 movement `60.39 fps`, modal/reduced-motion invariants remain zero;
- P2 pollination regression remains PASS, including zero stationary work and one-time reward semantics under save schema v2;
- P3 desktop Hive, Buzz-gate and 844x390 mobile panel report zero console/page errors;
- previous mechanically green head `de277105…` was rejected because mobile card copy was too small and the Buzz-gate label was poorly positioned;
- accepted `3b4b9909…` captures split card copy into readable rows and place `REQUIRES BUZZ 2` safely below the HUD;
- separate evaluation verdict = PASS;
- complete evidence = `evidence/P3-PROGRESSION/manifest.json` and `evidence/P3-PROGRESSION/evaluation.md`.

### autonomous milestone gate

P3 has the production runtime effects, deterministic economy/migration coverage, desktop/mobile rendered evidence, objective measurements, structured evidence, reference comparison and separate PASS evaluation. The final closeout PR head must still repeat Repository standards, Test/data, HTML5 CI and trusted `validate-pr-evidence`, with a retained non-N/A `movement-qa-$PR_HEAD`, before merge.

**P3 exit: PASS. Production advances to P4 — First Meadow Restoration after the merge gate completes.**

---

# P4 — First Meadow Restoration

**Status: COMPLETE for closeout — exit criteria PASS.**

## Goal

Prove the central visual promise: a weak/dormant space becomes alive because of the player's actions.

### Stable Meadow model — COMPLETE

The first authored meadow `r01_m01` has an explicit `restoration_target = 3` and four validated stage definitions. A pure domain module derives stage from authored patch completion contributions; presentation does not own campaign truth.

### Authored dormant/waking/growing/restored stages — COMPLETE

The accepted ladder is:

```text
DORMANT  contribution 0  ground 0.00  detail 8   ambient life 0
WAKING   contribution 1  ground 0.35  detail 14  ambient life 1
GROWING  contribution 2  ground 0.68  detail 22  ambient life 2
RESTORED contribution 3  ground 1.00  detail 28  ambient life 6
```

Data validation rejects malformed stage order, thresholds, ranges and final-target mismatches.

### Minimal objective guidance / no modal tutorial — COMPLETE

Ordinary gameplay retains one objective plus Honey and existing patch/gate cues. P4 adds no modal tutorial stack, restoration confirmation or second restoration verb. HUD-hidden proof is a first-class acceptance path rather than a cosmetic optional capture.

### Restoration celebration — COMPLETE

The final transition adds a bounded 1.5-second world-space accent inside V-001's 1.2–2.0-second major-reveal band. Real Chromium input during the accent moves the bee `86.644` design units, proving the celebration does not capture control.

### Deterministic before/mid/after QA — COMPLETE

Canonical clean-context fixtures independently produce:

- `meadow_dormant` → `DORMANT / 0`;
- `meadow_mid` → `GROWING / 2`;
- `meadow_restored` → `RESTORED / 3`.

They are intentionally separated from real persistence proof so fixture names cannot inherit whichever browser save happens to exist.

### Save/reload across restoration stages — COMPLETE

P4 does not add save schema v3. Stage is derived from the existing v2 `world.campaign_completion` stable IDs plus authored restoration contributions. Real `p4_storage_lifecycle=reset/reload` browser proof restores `GROWING` at midpoint and `RESTORED` at final state. Reloading an already-restored save does not replay the one-shot celebration.

## Exit criteria

- new player understands the meadow without external explanation — PASS for autonomous milestone evidence: one objective plus existing world-space patch/gate cues, no modal tutorial, deterministic in-world staged transformation; no external novice playtest is claimed, so evidence strength remains MEDIUM;
- before/after difference is strong with HUD hidden — PASS: ground mix `0.00 -> 1.00`, detail count `8 -> 28` (`3.5x`), ambient life `0 -> 6`, retained at desktop and Poki-small;
- no modal tutorial stack is required — PASS, modal tutorial count `0`, no restoration input action added;
- restoration state is save-safe — PASS at midpoint/final reload with no duplicate persisted stage and no restored-reload celebration replay;
- reference/visual scorecard passes — PASS in the separate evidence-first evaluation; no open `ITERATE` finding;
- desktop/mobile/canonical browser evidence contains no P4 console/page errors — PASS, `0 / 0`;
- P0/P1/P2/P3 regressions remain green inside the accepted HTML5 run — PASS.

### P4 exit record

Accepted runtime evidence head before closeout-only source-of-truth changes: `a45f9dac2f9d7136c3da51dc5b761eb0c05ce739`.

- Repository standards `33249086788` — PASS;
- Test/data `33249086793` — PASS;
- Pages preview `33249086822` — PASS;
- HTML5 CI `33249086913` — PASS;
- movement/P4 artifact `9713808008` (`movement-qa-a45f9dac2f9d7136c3da51dc5b761eb0c05ce739`), digest `sha256:7385f1161ad2c68a91027bbc5585b6246abb14fdc56c42929ade4f158d8369ec`;
- storage artifact `9713808284` — retained;
- playable artifact `9713807374` — retained;
- visual artifact `9713807618` — retained;
- HTML5 diagnostics artifact `9713808576` — retained;
- restoration ladder measurements: ground `0.00 -> 0.35 -> 0.68 -> 1.00`, detail `8 -> 14 -> 22 -> 28`, ambient life `0 -> 1 -> 2 -> 6`;
- final reveal control displacement `86.644` design units;
- midpoint reload `GROWING`, final reload `RESTORED`, restored reload celebration `false`;
- canonical clean fixtures `DORMANT/0`, `GROWING/2`, `RESTORED/3`;
- desktop/Poki-small/mobile P4 browser errors `0 / 0`;
- earlier candidate lifecycle defect that replayed final celebration after restored reload was fixed before acceptance;
- earlier canonical-fixture contract defect that allowed storage inheritance was fixed before acceptance;
- separate evaluation verdict = PASS;
- complete evidence = `evidence/P4-FIRST-MEADOW-RESTORATION/manifest.json` and `evidence/P4-FIRST-MEADOW-RESTORATION/evaluation.md`.

### autonomous milestone gate

P4 has the production runtime transformation, deterministic clean fixtures, real lifecycle persistence proof, HUD-hidden desktop/Poki-small/mobile rendered evidence, objective measurements, structured evidence, reference comparison and a separate PASS evaluation. The final closeout PR head must still repeat Repository standards, Test/data, Pages preview, HTML5 CI and trusted `validate-pr-evidence`, with a retained non-N/A `movement-qa-$PR_HEAD`, before merge.

**P4 exit: PASS. Production advances to P5 — Seed Ownership During Restoration after the merge gate completes.**

---

# P5 — Seed Ownership During Restoration

**Status: COMPLETE for closeout — exit criteria PASS.**

## Goal

Implement the **P-1 validated Hybrid seed/restoration model** so player flower choice contributes to ownership during restoration without changing native campaign truth or creating repeat aesthetic grind.

### Seed definitions / one-time ownership — COMPLETE

The first production seed set is:

```text
Daisy     available after native patch 1   unlock 15 Honey   owned replant 0
Clover    available after native patch 2   unlock 18 Honey   owned replant 0
Lavender  available after native patch 3   unlock 22 Honey   owned replant 0
```

Ownership is a permanent one-time sink rather than a consumable inventory quantity.

### Native campaign vs player-shaped plots — COMPLETE

The three native Daisy/Clover/Lavender campaign patches retain their authored species and remain the only first-Meadow restoration contributors. Two dedicated player-shaped plots (`r01_m01_player_plot_01`, `r01_m01_player_plot_02`) are separate bounded `YOUR PLOT` spaces and never enter `world.campaign_completion`.

### Low-friction contextual planting — COMPLETE

P5 adds no seed inventory modal or second persistent HUD. Keyboard reuses `PRIMARY_ACTION` (`SPACE / ENTER` in the current browser proof); pointer/touch directly taps the nearby visible player plot. World-space labels/prompts expose `YOUR PLOT`, locked/native prerequisite state and the concrete plant/replant action/cost.

### Reversible replant / campaign safety — COMPLETE

Real Chromium lifecycle proof plants Daisy, later plants Clover and then replants already-owned Daisy for `0 Honey`. Honey remains `67 -> 67` across the replant and native completion remains patch 1/2 complete, patch 3 incomplete. The aesthetic state changes while campaign truth does not.

### Save v3 / migration — COMPLETE

Save schema advances v2 -> v3:

- `player.seed_unlocks` stores owned stable seed IDs;
- `world.player_plants` stores stable player-plot -> flower selections;
- `world.campaign_completion` remains exclusively native campaign completion.

Deterministic migration coverage preserves Honey, Flight/Buzz upgrades and prior native completions. Real browser reload restores owned Daisy+Clover, Daisy on plot 1, Honey `67` and the same native completion state.

### Economy regression — COMPLETE

The deterministic P5 model exhaustively evaluates all `5! = 120` priority orders across Flight 2, Buzz 2, Daisy, Clover and Lavender first sinks. All `120/120` pass without negative Honey, replay/grind or progression dead-end; after all first sinks the model leaves `50 Honey`.

### Desktop/mobile runtime proof — COMPLETE

Accepted desktop browser proof covers native patch -> Daisy unlock/plant -> native patch -> Clover unlock/plant -> free Daisy replant -> reload. Accepted 844x390 mobile proof directly taps the player plot, changes Honey `45 -> 30`, owns Daisy and plants `flower_daisy`. P5 browser console/page errors are `0 / 0`.

Two exact-runtime defects were found and fixed before acceptance:

1. mobile world hit-testing initially double-scaled Defold virtual `action.x/y`; the runtime now uses physical `action.screen_x/screen_y` before one screen-to-design conversion;
2. after schema v3, the old BB-007 browser storage probe still emitted hard-coded save v2; it now derives `migrations.CURRENT_SAVE_VERSION`, and the full storage lifecycle passes again.

## Exit criteria

- player can explain native challenge vs chosen flowers — PASS for autonomous milestone evidence: ownership is confined to bounded `YOUR PLOT` spaces, locked plots explicitly say `RESTORE NATIVE PATCH FIRST`, and native authored patches retain their established progression role; no external novice playtest is claimed, so evidence strength remains MEDIUM;
- seed choice is visible in the recovering world — PASS: retained frames show empty/offer -> Daisy -> Clover -> Daisy on the same player plot before full campaign completion;
- choices are reversible where promised — PASS: owned Daisy replant costs `0 Honey`;
- campaign progress cannot be broken by aesthetics — PASS: replant does not change native completion and all 120 economy priorities remain no-grind/progression-safe;
- customization survives reload — PASS: Daisy+Clover ownership, Daisy plant, Honey `67` and native completion survive save v3 reload;
- the flow remains low-friction on desktop and touch — PASS: contextual `SPACE / TAP`, no new modal/inventory, direct 844x390 touch transaction;
- P0/P1/P2/P3/P4 regressions remain green in the same accepted HTML5 artifact — PASS;
- separate evidence-first evaluation has no open `ITERATE` — PASS.

### P5 exit record

Accepted runtime evidence head before closeout-only source-of-truth changes: `8967ab565bc9ff9c7838344676587fbf0a6d2ae0`.

- Repository standards `33251552722` — PASS;
- Test/data `33251552769` — PASS, `92/92` tests;
- P5 economy regression — PASS, `120/120` priorities, final Honey `50`;
- Pages preview `33251552723` — PASS;
- HTML5 CI `33251552740` — PASS;
- movement/P5 artifact `9714546464` (`movement-qa-8967ab565bc9ff9c7838344676587fbf0a6d2ae0`), digest `sha256:64a04641fbd44542217ded406f785115b5939c8cd593436ec094f1b452e5e4ce`;
- storage artifact `9714546696`, digest `sha256:ccb79b5276118eadcb2c0161e3d9f1f20bfaa46ef41bad27c2a85037f27fb6c8`;
- visual artifact `9714546052` — retained;
- playable artifact `9714545805` — retained;
- HTML5 diagnostics artifact `9714546973` — retained;
- Daisy real transaction Honey `45 -> 30`;
- Daisy+Clover owned after second native patch; Honey `67`;
- free Daisy replant Honey `67 -> 67`, campaign completion remains `true / true / false`;
- reload retains owned Daisy+Clover, Daisy on plot 1, Honey `67` and native completion;
- direct mobile touch transaction Honey `45 -> 30`, Daisy owned/planted;
- P5 browser errors `0 / 0`;
- mobile coordinate double-conversion defect fixed before acceptance;
- stale v2 storage-probe fixture fixed before acceptance;
- separate evaluation verdict = PASS;
- complete evidence = `evidence/P5-SEED-OWNERSHIP/manifest.json` and `evidence/P5-SEED-OWNERSHIP/evaluation.md`.

### autonomous milestone gate

P5 has production Hybrid topology, deterministic migration/economy coverage, desktop/mobile real transactions, reversible replant proof, campaign-state separation, retained P1-P4 regressions, structured evidence, reference comparison and a separate PASS evaluation. The final closeout PR head must still repeat Repository standards, Test/data, Pages preview, HTML5 CI and trusted `validate-pr-evidence`, with a retained non-N/A `movement-qa-$PR_HEAD`, before merge.

**P5 exit: PASS. Production advances to P6 — First Region Vertical Slice after the merge gate completes.**

---

# P6 — First Region Vertical Slice

**Status: COMPLETE for closeout — functional exit criteria PASS; independent verdict PASS WITH DEVIATION.**

## Goal

Ship one small game that feels coherent rather than a collection of systems.

### Validated first-region content — COMPLETE

Sunny Meadows is one continuous authored `region_01` with six compact Meadow beats:

1. First Patch — tutorial/Hive/first ownership;
2. Clover Bend — first route continuation;
3. Lavender Bank — Buzz-2 capability aspiration;
4. Creek Garden — traversal/navigation variation;
5. Tulip Rise — late-region landmark and Tulip challenge;
6. Lily Clearing — Buzz-3 climax.

P6 validates the six-Meadow hypothesis without introducing a world-map/menu or one collection proxy per Meadow.

### Region navigation / progress presentation — COMPLETE

The continuous region uses authored path/landmark language and one sparse persistent objective cluster. Region progress is exposed as Sunny Meadows restored count inside the existing objective hierarchy; completed Meadows retain visibly restored presentation.

### Flower/progression extension — COMPLETE

Tulip and Lily join the data-driven native flower set. Flight 3 raises real maximum speed `330 -> 360 u/s`; Buzz 3 raises pollination work `1.35x -> 1.65x`. Lily Clearing is explicitly `LOCKED / requires_buzz 3` before the Buzz-3 purchase and becomes `AVAILABLE` immediately after it.

### Save v4 / settings / audio — COMPLETE

Save schema advances v3 -> v4 while preserving Honey, upgrades, native completion, seed ownership and player plants. P6 adds persistent reduced-motion and audio-mute settings with safe migration defaults. The focus-isolated settings surface renders text-redundant `REDUCED MOTION` and `AUDIO` state. Pollination/region completion use local repository-authored Wave assets; mute is runtime-controlled.

### Analytics / portal seam — COMPLETE for P6 scope

A platform-neutral analytics adapter records the semantic event family `session_start`, `first_input`, `patch_completed`, `meadow_restored`, `region_completed`, `settings_changed`. Gameplay does not import a portal SDK directly. The accepted browser journey records 19 events and zero external runtime requests.

### Portal/device/performance proof — COMPLETE

The accepted retained P6 artifact covers:

- desktop reference `1280x720`, with canvas exactly `1280x720`;
- mobile landscape `844x390`, with full viewport canvas coverage;
- Poki `640x360`, `836x470`, `1031x580`;
- browser console/page errors `0 / 0`;
- external runtime requests `0`;
- measured engine FPS `59.92` against budget `>=50`;
- release bundle `2,813,096` bytes against `12,582,912` bytes.

The exact browser run also forced two late P6 fixes before acceptance: full-viewport HTML5 canvas sizing and removal of stale `120 Honey` fixture contamination from clean-save `region_start`.

## Exit criteria

- first region completes from clean save with no blocker — PASS, 6/6 Meadows restored;
- onboarding works without external help — PASS for autonomous evidence through one objective/path/landmark hierarchy; no external novice study is claimed;
- economy does not require unintended replay grind — PASS in the clean-save journey; final Honey `386` after Flight/Buzz 3 and region completion;
- seed system is actually used in tests/journey — PASS; combined retained P1-P6 artifact keeps P5 ownership/planting and campaign separation green;
- stable save/migrations — PASS; Test/data `102/102`, storage regression and completed-region/settings reload pass under save v4;
- deterministic visual QA artifacts cover critical surfaces — PASS; region start/mid/complete, clean-save milestones, settings, reload, desktop/mobile/Poki retained;
- target portal/device requirements pass in repository-controlled scope — PASS; required landscape sizes fill the canvas, errors/requests are zero;
- no hidden critical placeholder dependency — PASS WITH DEVIATION; audio/settings/region UI are real local runtime implementations and no external placeholder media is required, but the current original geometric bee/flower/UI illustration still falls short of the long-term rounded/species-silhouette/final-typography art direction and is carried explicitly to P7/P8;
- performance/load budgets pass — PASS, `59.92 fps` and `2,813,096` bytes;
- independent evaluation has no open `ITERATE` — PASS WITH DEVIATION.

### P6 exit record

Accepted runtime evidence head before closeout-only source-of-truth changes: `1001783236aac0ca2052bf6b4498c600a5dbf6fb`.

- Repository standards `33269124642` — PASS;
- Test/data `33269124670` — PASS, `102/102`;
- Pages preview `33269124643` — PASS;
- HTML5 CI `33269124636` — PASS;
- movement/P6 artifact `9719600537` (`movement-qa-1001783236aac0ca2052bf6b4498c600a5dbf6fb`), digest `sha256:77f0b0972eb7ba12bac3e292f429a6c1689820e9984b0d28bee5f2e527e3c9de`;
- storage artifact `9719600731`, digest `sha256:65b11cfc5258dbe1edcba1d7210f38074b9843dc77de2f0363e14daf2f89531a`;
- visual artifact `9719600159`, digest `sha256:81b38a8164273d4bf761055ef2eaf3d09aa41e40ae801391eb8592514ac7f324`;
- playable artifact `9719599927`, digest `sha256:4f5705db6b447962f3dd12e87d17d1fca8bcfbd1bcc18e8fd29bff14a3eca902`;
- HTML5 diagnostics artifact `9719600959`, digest `sha256:f0afea230b579dd79a3078de0242346ee43ff38efc92cafd5b8f6e0e6e693673`;
- all six Meadows restored from clean save;
- Lily `LOCKED / requires Buzz 3 / 1.35x -> AVAILABLE / 1.65x`;
- final Flight/Buzz levels `3 / 3`;
- final clean-save Honey `386`;
- reduced motion ON and audio MUTED exercised and retained through reload;
- analytics `19` events across six semantic event types;
- browser console/page errors `0 / 0`, external requests `0`;
- desktop canvas `1280x720`, mobile `844x390`, three Poki viewports retained;
- measured engine FPS `59.92`, bundle `2,813,096` bytes;
- separate evaluation verdict = `PASS WITH DEVIATION`;
- complete evidence = `evidence/P6-FIRST-REGION-VERTICAL-SLICE/manifest.json` and `evidence/P6-FIRST-REGION-VERTICAL-SLICE/evaluation.md`.

### autonomous milestone gate

P6 has the complete playable journey, critical-surface captures, objective measurements, save/settings/analytics/platform/performance proof, structured evidence and a separate `PASS WITH DEVIATION` evaluation with no open `ITERATE`. The final closeout PR head must still repeat Repository standards, Test/data, Pages preview, HTML5 CI and trusted `validate-pr-evidence`, with a retained non-N/A `movement-qa-$PR_HEAD`, before merge.

**P6 exit: PASS WITH DEVIATION. Production advances to P7 — Production Expansion after the merge gate completes. The visual-finish deviation remains explicit P7/P8 work and must be resolved before release-candidate visual certification.**

---

# P7 — Production Expansion

**Status: IN PROGRESS — Golden Fields and Wetland Garden accepted; Rosewood in progress.**

Scale proven content/system patterns only.

Rules:

- new regions should be mostly authored content/data;
- every new system still follows research-first workflow and evidence governance;
- if each region requires core architecture rewrites, stop and repair architecture;
- canonical proposed region order lives in `DECISIONS.md` / `04-world-content.md`;
- P6's explicit geometric-illustration deviation must be reduced while content scales; do not mass-produce final assets on the assumption that the current geometric presentation is release-certified art.

Potential cut-first items remain: accent species, helper insects, replay economy, advanced fast travel, cosmetics/live content.

## Golden Fields — ACCEPTED SLICE, PASS WITH DEVIATION

The first P7 slice proves that the P6 architecture scales into a second authored region without another core verb, currency, mandatory sink, world-management screen or per-region game-world lifecycle.

### Authored content — COMPLETE for Golden Fields

`region_02` contains four Meadows:

1. Sun Gate — Sunflower, Buzz-3 continuation;
2. Poppy Run — Poppy;
3. Windmill Loop — Sunflower + Windmill landmark;
4. Harvest Crown — Poppy + Golden Wind Vane identity.

The active region is derived from the first incomplete authored region. P6 QA fixtures remain pinned to `region_01`; production runtime continues to Golden Fields automatically after Sunny Meadows completion.

### Economy / progression reuse — COMPLETE

Golden Fields adds no new currency, upgrade branch or required spend. The accepted P6 max-first-sink state begins at `346 Honey`; four first-time Golden Fields rewards total `545`, ending at `891 Honey`. Deterministic and browser evidence both pass without replay or progression dead-end.

### Browser journey / persistence — COMPLETE

The retained journey starts from the P6 region-complete fixture only long enough to persist that state through the real save/settings path, then removes the QA route. Ordinary runtime derives Golden Fields at `0/4`, completes it to `4/4`, records region-scoped analytics and reloads with both campaign regions complete.

Accepted runtime evidence head before closeout-only source-of-truth changes: `8d9640522ffc742ffe79178718fa2df0517dd6bc`.

- Repository standards `33271607224` — PASS;
- Test/data `33271607179` — PASS, `108/108`;
- Pages preview `33271607241` — PASS;
- HTML5 CI `33271607193` — PASS;
- movement/P7 artifact `9720322590` (`movement-qa-8d9640522ffc742ffe79178718fa2df0517dd6bc`), digest `sha256:b58dc0c217aa1845a3f42a2b1cf2fcb4685f2a548f452d09be50d00cbeb0fd80`;
- storage artifact `9720322807`, digest `sha256:7101d69c975e8543fe1babf7e7b835826408ce73fb3e489a5fb0d8537354ce6a`;
- visual artifact `9720322272`, digest `sha256:02fec4d9a4b5ad298c83bb72211c6a600093bd1ef3a335decbc58fe964e53a44`;
- playable artifact `9720322102`, digest `sha256:8c8c5fed6235c72460485ad235c7110e59b42998e11a3be3a31dce48da45bd3e`;
- HTML5 diagnostics artifact `9720323006`, digest `sha256:66c7580f97f7ba00ee1a1e27fa5c6ec493e8941e82c696906e0aebddd0c3f682`;
- Test/data artifact `9720268026`, digest `sha256:ed82ab40085d5bbf226f7fb7d341cdcb0a329133c11c4858d993aac251b4f987`;
- Golden Fields `0/4 -> 4/4`;
- campaign `region_01 6/6 + region_02 4/4`, `2/2` complete after reload;
- Honey `346 -> 891` with no new mandatory spend/replay;
- 11 P7 analytics events through `region_completed`;
- P7 browser console/page errors `0 / 0`, external requests `0`;
- desktop canvas `1280x720`, mobile canvas `844x390`;
- current combined engine FPS `59.87` against `>=50`;
- current release bundle `2,815,539` bytes against `12,582,912` bytes.

### GUI scalability repair — COMPLETE for current two-region catalog

The first Golden Fields HTML5 candidate `ba4c4be33f7353944a5ff5ea1389e04948a79eb4` failed with `ERROR:GUI: Could not create the node since the buffer is full (512)` / `Out of nodes (max 512)`. This is retained as a real P7 architecture finding, not normalized as flaky CI.

The accepted repair:

- keeps `movement_field.gui` at `max_nodes: 512`;
- removes one permanent flower-GUI subtree per authored patch;
- allocates six reusable patch-visual slots;
- rebinds those slots to nearby authored patches from camera distance;
- keeps gameplay/campaign state in the controller/domain layer; GUI remains presentation-only.

The exact accepted HTML5 run passes after this repair, so rendering cost is now bounded by visible complexity instead of total authored patch count for the current architecture.

### Golden Fields independent evaluation

Verdict: **PASS WITH DEVIATION**.

Functional/multi-region architecture is accepted: the second region derives from persisted campaign state, reuses the core verb/economy/save/analytics seams, completes without replay, survives reload, retains P1-P6 regressions and passes current browser/performance budgets. The original 512-node failure is fixed architecturally rather than by raising the budget.

The deviation remains visual finish. Golden Fields has a distinct palette, landmarks and Sunflower/Poppy presentation, but the bee, flower illustration, typography and full-scene composition remain intentionally geometric and below the long-term release-art target. Some wide-view edge framing is also sparse despite correct full-canvas sizing. This is not a hidden placeholder dependency and does not block the content-scaling proof, but it may not be relabeled release-candidate art.

Complete Golden Fields records:

- `docs/research/P7-golden-fields-production-expansion.md`;
- `evidence/P7-GOLDEN-FIELDS/manifest.json`;
- `evidence/P7-GOLDEN-FIELDS/evaluation.md`.

### Golden Fields autonomous merge gate

The accepted runtime evidence is complete. The final closeout PR head must still repeat Repository standards, Test/data, Pages preview, HTML5 CI and trusted `validate-pr-evidence`, and retain a non-N/A `movement-qa-$PR_HEAD`, before merge.

**Golden Fields slice: PASS WITH DEVIATION. P7 milestone remains IN PROGRESS. Wetland Garden is the second accepted slice; Rosewood is the active production handoff.**

Remaining P7 region sequence:

1. Rosewood — active;
2. Alpine Bloom;
3. Moon Garden.

---

## Rosewood — ACCEPTED SLICE, PASS WITH DEVIATION

Rosewood is the fourth authored region and closes the woodland content slice without adding a verb, currency, mandatory spend, world-management screen or per-region lifecycle.

### Authored content — COMPLETE for Rosewood

region_04 contains four Meadows: Rose Glade, Bluebell Hollow, Cedar Turn and Woodland Crown. Rose and Bluebell use distinct authored flower IDs and canopy, trunk, root and arch landmark language; all restoration remains movement-through pollination with Buzz 3.

### Economy / progression reuse — COMPLETE

The persisted Golden/Wetland end state starts at 1596 Honey. Rosewood first-time rewards are 205 + 220 + 235 + 250 = 910, ending at 2506 Honey with no mandatory spend or replay.

### Browser journey / persistence — COMPLETE

The exact Chromium journey persists the Wetland-complete fixture through the real settings/save path, derives Rosewood at 0/4, completes it through ordinary runtime, records region_completed for region_04, reloads at four completed campaign regions and retains the mobile-landscape evidence. The accepted candidate head before source-of-truth closeout changes is 6b5eb076cc4361bcf097c350c4d0f46228727766.

- Repository standards 33312103054 — PASS;
- Test/data 33312103035 — PASS;
- Pages preview 33312103045 — PASS;
- HTML5 CI 33312103046 — PASS;
- movement artifact 9732383632, movement-qa-6b5eb076cc4361bcf097c350c4d0f46228727766;
- storage artifact 9732383768;
- visual artifact 9732383407;
- playable artifact 9732383268;
- HTML5 diagnostics artifact 9732383910;
- Rosewood 0/4 → 2/4 → 4/4, reload 4/4, Honey 1596 → 2506;
- browser console/page errors 0/0, external requests 0, desktop 1280×720, mobile 844×390;
- retained release bundle 2,818,788 bytes against the 12 MiB budget; exact movement evidence remains approximately 60 fps against ≥50.

### Rosewood independent evaluation

Verdict: PASS WITH DEVIATION. The fourth-region architecture, authored woodland identity, progression, persistence, analytics, bounds and measured runtime budgets pass. The existing geometric bee/flower illustration, typography, animation and full-scene polish remain explicit P8 visual-certification work; this is not an open ITERATE on Rosewood content architecture.

Complete Rosewood records:

- docs/research/P7-rosewood-production-expansion.md;
- evidence/P7-ROSEWOOD/manifest.json;
- evidence/P7-ROSEWOOD/evaluation.md.

### Rosewood autonomous merge gate

The closeout head must repeat Repository standards, Test/data, Pages preview, HTML5 CI and trusted validate-pr-evidence, retaining non-N/A movement, storage, visual and playable artifacts before merge.

**Rosewood slice: PASS WITH DEVIATION. P7 milestone remains IN PROGRESS. Alpine Bloom is the next production slice; Moon Garden follows.**

---
# P8 — Release Candidate

## Important correction

The **primary distribution target is selected in P-1**, not here. P8 integrates and certifies it.

### Work

- final selected portal SDK/adapter integration;
- gameplay lifecycle events;
- privacy/consent/legal/license review;
- final bundle/startup profiling;
- complete save migration/recovery matrix;
- browser/device QA;
- production telemetry dashboard;
- store/portal metadata and capture set;
- final production illustration/animation/typography certification, including closure of the P6/P7 visual-finish deviation;
- verify no debug QA state injection is exposed unsafely in release.

## Release gates

- no known progression blocker;
- no reproducible save-loss bug;
- complete required journey reachable from clean save;
- selected portal requirements satisfied;
- analytics/privacy behavior approved;
- third-party inventory complete;
- stable player-visible performance/load behavior;
- P6/P7 visual-finish deviation closed or replaced by an explicitly approved release-quality art decision;
- production build contains no secrets or unsafe dev tools.

---

## Prioritization

1. progression blocker;
2. save/data loss;
3. control/core-verb feel;
4. comprehension/UX;
5. performance/load;
6. core-loop polish;
7. content;
8. optional meta systems;
9. monetization extras.

A repository full of systems is not a working product. A working BeBee is one where a new player can understand the fantasy, enjoy the core verb, visibly restore and personalize the world, leave and return safely, and run the release build reliably on the chosen target.
