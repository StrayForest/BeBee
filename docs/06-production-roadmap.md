# 06 — Production Roadmap

## 1. Delivery rule

Do not advance because the calendar says so. Advance only when the milestone exit criteria pass.

The roadmap started with **P-1 Blueprint Hardening** because the audit found several early design assumptions that were written before the repository adopted research-first development. P-1 is complete; P0 Foundation is in progress and the current production handoff is **P0 / BB-003 — Input and proxy-focus proof**.

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

**Status: IN PROGRESS — BB-001 and BB-002 complete; BB-003 next.**

## Goal

Create a deterministic Defold project, CI path and evidence pipeline.

### BB-001 — Defold bootstrap — COMPLETE

Delivered:

- root `game.project` with a minimal long-lived `app/` bootstrap collection/controller;
- explicit development/release settings;
- reproducible editor-independent HTML5 bundler;
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

### BB-003 — Input and proxy-focus proof

- semantic movement/actions;
- keyboard path;
- touch abstraction;
- explicit input-focus ownership;
- if collection proxies are retained, prove input propagation and modal consumption with a small test scene.

### BB-004 — Test/data harness

- unit test runner;
- data validator;
- first deterministic tests;
- CI failure on test/data errors.

### BB-005 — HTML5 CI

- build on PR;
- unit/data validation;
- retain playable artifact;
- browser console smoke check where practical.

### BB-006 — Visual QA harness foundation

- deterministic development state injection/router;
- local serve command;
- automated screenshot tooling design implemented far enough to capture a known test state;
- desktop/mobile artifact capture.

### BB-007 — Storage adapter proof

- storage interface;
- local Defold adapter;
- protected corrupt-load path;
- primary/backup concept;
- serialized size diagnostic;
- browser save/reload smoke test.

## Exit criteria

- fresh clone builds reproducibly;
- CI produces a playable HTML5 artifact;
- test/data validation runs;
- one deterministic screenshot can be produced automatically;
- storage smoke test passes;
- input focus/proxy ownership is understood rather than assumed.

---

# P1 — Bee Movement

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

- 5-minute movement test exposes no obvious control/camera frustration;
- keyboard/touch produce consistent intent;
- no collision snagging;
- representative target frame pacing is stable;
- movement visual-QA comparison is `PASS` or approved deviation.

---

# P2 — Pollination Core Loop

## Goal

Implement the **P-1 validated pollination interaction**, not the old auto-pollination assumption by default.

### BB-020 — Flower definition model

- stable IDs;
- requirement/reward data;
- validation.

### BB-021 — FlowerPatch state model

Minimum domain states:

```text
LOCKED / AVAILABLE / ACTIVE / COMPLETED
```

Presentation substates may exist without contaminating persistent progression.

### BB-022 — Validated pollination interaction

Implement movement-through/sweep with forgiving bounds and clear start/stop feedback. Exact work target and incidental fly-through behavior are tuned here from the validated P-1 interaction pattern.

### BB-023 — Bloom feedback stack

- visible progress;
- staged flower opening;
- pollen/VFX;
- audio hook;
- completion reaction;
- reward attribution.

### BB-024 — Honey transaction

- one currency;
- non-negative invariant;
- single-reward completion;
- HUD feedback.

### BB-025 — Save v1

Persist minimal progression through the storage abstraction.

## Exit criteria

A player can fly, understand how to pollinate without explanation, complete a patch, receive Honey, reload safely and see preserved state.

### Autonomous milestone gate

Before P3 complexity begins, P2 requires the actual build, motion/rendered evidence, objective measurements, structured evidence, reference scorecard, passing acceptance/test results and a separate evaluation verdict. `ITERATE` blocks progression. Human review is optional and cannot block the phase.

---

# P3 — Progression

## Goal

Create a reward-to-power loop with meaningful choices and no mathematically compulsory filler stat.

### BB-030 — Validated upgrade set

- implement **Flight + Buzz** as the validated vertical-slice upgrade tracks (`D-007`);
- Yield is excluded from the vertical slice unless a new player problem and new evidence explicitly reopen the decision;
- do not add a replacement third track merely to fill a screen;
- tune final effect curves and costs against production movement/pollination feel.

### BB-031 — Hive/progression interaction

Research the relevant competitor upgrade interaction, then implement one-action purchasing with clear current/next effect and input isolation.

### BB-032 — Progression UI

Number/layout of cards follows the validated two-track set, not the original fixed three-card assumption.

### BB-033 — Flower gates

Use soft/hard Buzz/progression gates only where they create aspiration and remain explicit.

### BB-034 — Economy regression simulation

CI/dev command re-runs key no-grind scenarios when values change.

## Exit criteria

- each shipped stat has an obvious experiential/economic purpose;
- no upgrade is consistently mandatory or consistently ignored in simulation/playtest;
- no negative Honey;
- customization spending cannot create a progression dead-end;
- reload preserves progression.

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

### Autonomous milestone gate

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

### Autonomous milestone gate

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
