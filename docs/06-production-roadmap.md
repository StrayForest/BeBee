# 06 — Production Roadmap

## 1. Delivery rule

Do not advance because the calendar says so. Advance only when the milestone exit criteria pass.

The roadmap started with **P-1 Blueprint Hardening** because the audit found several early design assumptions that were written before the repository adopted research-first development. **P-1, P0 Foundation, P1 Bee Movement, P2 Pollination Core Loop and P3 Progression are complete for milestone closeout; the next production handoff after P3 merge is P4 — First Meadow Restoration.**

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
| P6 | Vertical slice | one polished region, shippable quality |
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
- `T-011` runtime behavior proven while `T-010` correctly remains `HYPOTHESIS` because proxy memory and complete region/screen lifecycle are not covered by this ticket.

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

**Status: COMPLETE for closeout — BB-030 through BB-034 complete; exit criteria PASS.**

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

## Goal

Prove the central visual promise: a weak/dormant space becomes alive because of the player's actions.

### Work

- stable Meadow model;
- authored dormant/waking/growing/restored stages;
- compact tutorial layout;
- minimal objective guidance;
- restoration celebration;
- deterministic before/mid/after QA states;
- save/reload across restoration stages.

## Exit criteria

- new player understands the meadow without external explanation;
- before/after difference is strong with HUD hidden;
- no modal tutorial stack is required;
- restoration state is save-safe;
- reference/visual scorecard passes.

### autonomous milestone gate

Before more meadows are authored, P4 requires deterministic before/mid/after evidence, objective comparison, passing acceptance/test results and a separate evaluation verdict. `ITERATE` blocks progression. Human approval is not required.

---

# P5 — Seed Ownership During Restoration

## Goal

Implement the **P-1 validated Hybrid seed/restoration model** so player flower choice contributes to ownership, rather than existing only as post-completion decoration.

### Work

- seed definitions/unlocks;
- separate campaign-native state from planted visual species;
- validated placement/plant flow;
- reversible replanting;
- one pollination/establishment loop if validated;
- persistence/migration;
- economy regression scenarios with customization-heavy spending.

## Exit criteria

- player can explain native challenge vs chosen flowers;
- seed choice is visible in the recovering world;
- choices are reversible where promised;
- campaign progress cannot be broken by aesthetics;
- customization survives reload;
- the flow remains low-friction on desktop and touch.

---

# P6 — First Region Vertical Slice

## Goal

Ship one small game that feels coherent rather than a collection of systems.

### Proposed content (still subject to validation)

1. First Patch;
2. Clover Bend;
3. Lavender Bank;
4. Creek Garden;
5. Tulip Rise;
6. Lily Clearing.

### Work

- region navigation;
- validated flower set;
- planet/region progress presentation;
- production bee/terrain/flowers/UI/VFX;
- audio pass;
- accessibility/settings;
- analytics adapter/events;
- balance/telemetry pass;
- portal-specific device/aspect/download checks for selected primary target.

## Exit criteria

- first region completes from clean save with no blocker;
- onboarding works without external help;
- economy does not require unintended replay grind;
- seed system is actually used in tests;
- stable save/migrations;
- deterministic visual QA artifacts cover critical surfaces;
- target portal/device requirements pass;
- no placeholder critical player-facing art/audio/UI;
- performance/load budgets pass.

### autonomous milestone gate

Before mass content production, P6 requires a complete playable artifact, critical-surface captures/motion evidence, objective measurements, scorecards, test/build/performance evidence, known deviations and a separate evaluation verdict. `ITERATE` blocks progression. No human approval is required.

---

# P7 — Production Expansion

Scale proven content/system patterns only.

Rules:

- new regions should be mostly authored content/data;
- every new system still follows research-first workflow and evidence governance;
- if each region requires core architecture rewrites, stop and repair architecture;
- canonical proposed region order lives in `DECISIONS.md` / `04-world-content.md`.

Potential cut-first items remain: accent species, helper insects, replay economy, advanced fast travel, cosmetics/live content.

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
- verify no debug QA state injection is exposed unsafely in release.

## Release gates

- no known progression blocker;
- no reproducible save-loss bug;
- complete required journey reachable from clean save;
- selected portal requirements satisfied;
- analytics/privacy behavior approved;
- third-party inventory complete;
- stable player-visible performance/load behavior;
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
