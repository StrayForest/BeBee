# BeBee

BeBee is a cozy 2D pollination-and-restoration game about a tiny bee bringing a barren planet back to life.

## Core fantasy

You are a small bee. You fly through compact meadows, pollinate flowers, earn Honey, improve the bee, unlock harder ecological challenges, buy seeds and influence what the recovering world becomes. The long-term goal is simple: make the whole planet bloom.

## Product principles

1. **One readable loop:** pollinate -> earn Honey -> improve/unlock -> plant/shape -> restore.
2. **Movement and the core pollination verb must feel good before content is scaled.**
3. **Very low cognitive load.** The next useful action should usually be understandable from the world.
4. **Visible restoration.** Meaningful progress changes the environment, not only a meter.
5. **Customization is progression/ownership, not a disconnected decoration screen.**
6. **Aesthetic choices must not create an unrecoverable grind or campaign soft-lock.**
7. **No mandatory combat or hard energy timer in the vertical slice.**
8. **HTML5 first, touch-compatible from the start.**
9. **Data-driven content and versioned persistent state.**
10. **Validate one polished vertical slice before mass-producing regions.**
11. **Research before implementation.** Study relevant shipped solutions and current official developer documentation first.
12. **Look at the real rendered result.** Screenshots/video and comparison evidence are part of player-facing definition of done.
13. **Separate confidence from persuasion.** A substantial decision records status, provenance and evidence strength rather than relying on an agent's prose.
14. **Measure before judging.** Observable interaction/UI/economy evidence comes before subjective scoring.

## Technology

- Engine: **Defold 1.13.1**, pinned for production bootstrap in `tools/defold/toolchain.json`
- Gameplay language: **Lua**
- Runtime target: **HTML5-first** (`wasm-web`)
- Primary external validation/distribution target: **Poki** (`P-001 VALIDATED`)
- Secondary/fallback portal: **CrazyGames**
- Owned development/QA target: **direct web**
- Secondary native targets: mobile/native only after browser validation
- Storage: versioned domain state behind a storage abstraction
- Platform integrations: adapters, never gameplay dependencies

## Decision model

The project deliberately distinguishes facts from hypotheses.

Read [`DECISIONS.md`](DECISIONS.md) before relying on a design choice.

Statuses:

- `LOCKED` — safe to implement/depend on;
- `VALIDATED` — supported by evidence, still tunable;
- `HYPOTHESIS` — must be researched/prototyped before dependent complexity;
- `OPEN` — intentionally undecided;
- `DEPRECATED` — no longer authoritative.

Substantial decisions also record **provenance**: owner constraint, reference pattern, technical constraint, experiment/simulation/playtest/telemetry result, or subjective direction. This prevents an aesthetic preference from being mislabeled as an objective fact.

When older documentation conflicts with `DECISIONS.md`, the decision registry wins.

## Mandatory development method

```text
problem
 -> decision status/provenance check
 -> reference candidate pool
 -> deep shipped-reference research + different solution/anti-pattern
 -> current official developer docs
 -> alternatives + implementation brief + acceptance criteria
 -> smallest complete implementation/prototype
 -> tests + HTML5 build
 -> screenshots/video + objective measurements
 -> separate evaluation pass
 -> iteration
 -> structured evidence + PR summary
 -> merge
```

Player-facing work is not accepted merely because code runs. See [`docs/10-development-workflow.md`](docs/10-development-workflow.md), [`docs/13-visual-qa-scorecard.md`](docs/13-visual-qa-scorecard.md) and [`docs/15-agent-evidence-governance.md`](docs/15-agent-evidence-governance.md).

For substantial player-facing/economy work, machine-readable evidence lives at:

```text
evidence/<ticket>/manifest.json
```

Use [`docs/templates/evidence-manifest.example.json`](docs/templates/evidence-manifest.example.json). The PR description summarizes evidence; it does not replace it.

## Documentation map

### Always-read

- [`README.md`](README.md)
- [`AGENTS.md`](AGENTS.md)
- [`DECISIONS.md`](DECISIONS.md)

### Product/design

- [`docs/00-product-vision.md`](docs/00-product-vision.md)
- [`docs/01-game-design.md`](docs/01-game-design.md)
- [`docs/02-progression-economy.md`](docs/02-progression-economy.md)
- [`docs/03-ux-ui-controls.md`](docs/03-ux-ui-controls.md)
- [`docs/04-world-content.md`](docs/04-world-content.md)
- [`docs/09-art-direction.md`](docs/09-art-direction.md)
- [`docs/17-visual-style-bible.md`](docs/17-visual-style-bible.md) — measurable V-001 visual baseline

### Engineering/production

- [`docs/05-technical-architecture.md`](docs/05-technical-architecture.md)
- [`docs/06-production-roadmap.md`](docs/06-production-roadmap.md)
- [`docs/07-qa-analytics-release.md`](docs/07-qa-analytics-release.md)
- [`docs/12-platform-storage.md`](docs/12-platform-storage.md)
- [`docs/13-visual-qa-scorecard.md`](docs/13-visual-qa-scorecard.md)
- [`docs/18-deterministic-visual-qa.md`](docs/18-deterministic-visual-qa.md)
- [`docs/19-repository-tooling-standards.md`](docs/19-repository-tooling-standards.md) — canonical repository/source/dependency/command contract
- [`config/repository-standards.json`](config/repository-standards.json) — machine-readable source and repository rules
- [`config/dependencies.json`](config/dependencies.json) — machine-readable third-party dependency/license inventory
- [`config/web-targets.json`](config/web-targets.json)
- [`config/visual-style.json`](config/visual-style.json) — canonical numeric style tokens
- [`config/visual-qa.json`](config/visual-qa.json) — canonical deterministic QA-state/capture contract
- [`config/storage-contract.json`](config/storage-contract.json) — HTML5 persistence/recovery contract
- [`tools/defold/toolchain.json`](tools/defold/toolchain.json) — pinned Defold/Bob/Java/HTML5 build contract

### Research/process

- [`docs/08-reference-analysis.md`](docs/08-reference-analysis.md)
- [`docs/10-development-workflow.md`](docs/10-development-workflow.md)
- [`docs/11-blueprint-hardening.md`](docs/11-blueprint-hardening.md)
- [`docs/15-agent-evidence-governance.md`](docs/15-agent-evidence-governance.md)
- [`docs/16-ci-trust-boundary.md`](docs/16-ci-trust-boundary.md)
- [`docs/research/BB-P017-ruleset-closeout.md`](docs/research/BB-P017-ruleset-closeout.md) — P-1 exit / strict ruleset verification
- [`docs/research/BB-001-defold-bootstrap.md`](docs/research/BB-001-defold-bootstrap.md) — P0 runtime/bootstrap evidence
- [`docs/research/BB-002-repository-tooling.md`](docs/research/BB-002-repository-tooling.md) — P0 repository/tooling evidence and alternatives
- [`docs/research/BB-003-input-proxy-focus.md`](docs/research/BB-003-input-proxy-focus.md) — P0 semantic input, proxy-focus and modal-consumption proof
- [`docs/research/BB-004-test-data-harness.md`](docs/research/BB-004-test-data-harness.md) — P0 deterministic test/data harness evidence and alternatives
- [`docs/research/BB-005-html5-ci.md`](docs/research/BB-005-html5-ci.md) — P0 exact-source playable HTML5 CI/browser-smoke contract
- [`docs/research/BB-006-visual-qa-harness.md`](docs/research/BB-006-visual-qa-harness.md) — P0 deterministic exact-build visual-QA runtime/capture proof
- [`evidence/BB-007-CLOSEOUT/manifest.json`](evidence/BB-007-CLOSEOUT/manifest.json) — P0 storage lifecycle/browser closeout evidence
- [`docs/research/P1-bee-movement.md`](docs/research/P1-bee-movement.md) — P1 movement research, implementation and failure/iteration trace
- [`evidence/P1-BEE-MOVEMENT/manifest.json`](evidence/P1-BEE-MOVEMENT/manifest.json) — P1 movement closeout evidence
- [`docs/research/P2-pollination-core-loop.md`](docs/research/P2-pollination-core-loop.md) — P2 pollination production research, tuning and iteration trace
- [`evidence/P2-POLLINATION-CORE-LOOP/manifest.json`](evidence/P2-POLLINATION-CORE-LOOP/manifest.json) — P2 pollination/economy closeout evidence
- [`docs/research/P3-progression.md`](docs/research/P3-progression.md) — P3 Flight/Buzz production research, economy and visual iteration trace
- [`evidence/P3-PROGRESSION/manifest.json`](evidence/P3-PROGRESSION/manifest.json) — P3 progression/economy closeout evidence
- [`docs/templates/feature-research.md`](docs/templates/feature-research.md)
- [`docs/templates/evidence-manifest.example.json`](docs/templates/evidence-manifest.example.json)
- [`.agents/skills/`](.agents/skills/) — reusable agent execution checklists

### Legal

- [`THIRD_PARTY.md`](THIRD_PARTY.md)

## Validated product structure vs open tuning

`D-006` is `VALIDATED`: default pollination is movement-through/sweep — qualifying movement inside a pollinatable patch advances progress, standing still does not, and the default scheme has no separate high-frequency pollination button. P2 productionizes this with forgiving authored bounds and work targets above one full forgiving-zone diameter; the first Daisy straight pass reaches 82.33% desktop / 82.92% mobile rather than completing incidentally. These values remain tunable rather than LOCKED.

`D-008` is `VALIDATED`: the default persistent HUD remains one objective plus Honey, while pollination state/progress lives in world space with redundant cues. P2 exact-head desktop/Poki/mobile evidence specifically iterated a mobile `LOCKED`/Honey overlap before accepting the baseline.

`D-005` is `VALIDATED`: seed ownership uses a Hybrid restoration topology. Authored native campaign plots keep their native identity during restoration, dedicated player-shaped plots allow seed ownership before full completion, and campaign/native state remains separate from planted species. P5 still must prove that the two roles are understandable in the rendered game and tune the exact plot count, placement, planting input and seed economy.

`D-007` is `VALIDATED`: the vertical slice uses **Flight + Buzz** as its bee upgrade tracks and Yield remains excluded. P3 productionizes the first level as Flight `300 → 330 u/s` for `30 Honey` and Buzz `1.00× → 1.35×` pollination work for `35 Honey`. Both choices are affordable from the first 45-Honey reward; runtime evidence proves the real movement/work effects, and Lavender becomes the first explicit `REQUIRES BUZZ 2` capability gate. Later levels and final pacing remain tunable rather than locked.

`D-013` is `VALIDATED`: P1 uses one normalized direct-intent movement controller for keyboard and floating touch, with bounded acceleration/deceleration, authored bounds, bounded orthographic follow and a reduced-motion direct-follow path. The 300-unit/s value is now explicitly the Flight-level-1 baseline; P3 Flight 2 raises the computed maximum to 330 u/s without changing controller semantics. The accepted P3 runtime captures 330/330 u/s after purchase while retaining zero modal displacement and zero reduced-motion camera lag.

Still open/tunable before downstream milestones lock production values:

- later Honey reward/cost tables and minutes/actions between meaningful purchases;
- later Flight/Buzz effect curves and Buzz-gate cadence beyond the first P3 level/gate;
- rendered comprehension/input/seed pacing for the Hybrid restoration flow;
- final production illustration/animation/audio and later full-scene visual polish.

The objective-evidence hardening in `BB-P013`–`BB-P017` is in place. `BB-P006` validated Poki as the primary external target, `BB-P007` defined V-001, `BB-P008` defined the deterministic visual-QA runtime contract, and `BB-P009` defined the HTML5 A/B generation storage/recovery contract.

At P-1 closeout, repository enforcement was verified through ruleset `Protect main`: pull requests plus `validate-pr-evidence`, strict/up-to-date checks, zero approvals and no bypass actors. The retained closeout evidence is [`docs/research/BB-P017-ruleset-closeout.md`](docs/research/BB-P017-ruleset-closeout.md) and [`evidence/BB-P017-RULESET-CLOSEOUT/ruleset-snapshot.json`](evidence/BB-P017-RULESET-CLOSEOUT/ruleset-snapshot.json). If enforcement is temporarily disabled for repository maintenance, it must be restored before normal protected development continues.

## Vertical-slice target

The intended slice still aims to prove:

- controllable expressive bee;
- several flower difficulty tiers;
- one compact authored region;
- satisfying movement-through pollination/bloom feedback;
- Honey economy;
- meaningful Flight/Buzz improvement;
- seeds that let players influence the recovering meadow;
- visible meadow/planet restoration;
- save/reload;
- desktop + touch controls;
- sound/VFX/accessibility basics;
- analytics abstraction;
- production-quality HTML5 build.

Exact stat/pacing values are validated through runtime milestones rather than treated as immutable because they appeared in an early GDD.

## Non-goals for the vertical slice

No multiplayer, guilds, PvP, procedural infinite world, complex crafting tree, equipment loot treadmill, mandatory daily quests, backend account system, premium currency or battle pass.

## Current status

**P0 — Foundation is COMPLETE. `BB-001` through `BB-007` are complete and all P0 exit criteria pass.**

BB-001 establishes a minimal `app/` bootstrap, explicit development/release settings and a reproducible editor-independent HTML5 path. The toolchain is pinned to Defold **1.13.1**, OpenJDK **25**, `wasm-web` and the published Bob SHA-256. Exact-head CI successfully built both development and release bundles and rendered the bootstrap in Chromium before merge.

BB-002 adds Defold-aware generated-file rules, explicit text/Lua conventions, canonical production resource roots, machine-readable dependency/license inventory, a dependency-free repository validator and PR/main CI enforcement. It does not claim semantic input, proxy lifecycle, storage, gameplay, UI, test/data harness or deterministic gameplay QA.

BB-003 replaces the empty binding with device-independent semantic actions, proves keyboard and HTML5 single-touch/pointer paths, explicitly owns collection-proxy input focus, and retains an exact-head Chromium proof that unconsumed actions traverse the proxy world while an open modal consumes them before proxied gameplay and lower main-world listeners. `T-010` remains a hypothesis because proxy memory/full lifecycle are still unproven.

BB-004 adds a dependency-free deterministic Lua test runner, a dedicated Defold headless test bootstrap, a canonical content catalog plus stable-ID/reference validation, and initial deterministic cases. The editor-independent runner verifies the pinned Bob/Java toolchain, requires a structured suite completion event, propagates failures through process exit status and retains diagnostic output. Subsequent work extends the suite without changing the BB-004 harness contract.

BB-005 provides exact-source HTML5 CI for every PR and `main` update: pinned development/release `wasm-web` builds, release Chromium startup/resource/console smoke, retained BB-003 keyboard/touch/proxy smoke, a playable release artifact and diagnostics.

BB-006 provides development-only deterministic QA routing, exact source-SHA binding, pinned Playwright capture, fresh BrowserContexts, release-negative proof and retained desktop/mobile visual artifacts.

BB-007 provides versioned local storage, A/B generation journal/recovery, protected corrupt-load handling, persistent delete and real HTML5 lifecycle proofs including the previously discovered Defold VFS → IndexedDB rapid-navigation race. Full evidence is retained in [`evidence/BB-007-CLOSEOUT/manifest.json`](evidence/BB-007-CLOSEOUT/manifest.json).

**P1 — Bee Movement is COMPLETE; all P1 exit criteria pass.**

P1 implements the first production traversal slice: a pure-Lua normalized controller with acceleration/deceleration/reversal, keyboard and floating-touch parity, authored bounds, bounded orthographic Auto Cover follow, reduced-motion direct follow, simple idle/fly/turn presentation and deterministic `movement_empty` / `movement_dense` HTML5 QA states. The movement runtime stays inside the proxied gameplay world so the BB-003 native Defold focus/modal contract remains authoritative rather than being replaced by owner-side custom forwarding.

The accepted runtime evidence head `2e1098ac10596d02ad7d8b71e6034b5e778a7315` passed Repository standards (`33240599831`), Test/data (`33240599809`) and HTML5 CI (`33240599811`). Retained movement artifact `9711246614` records desktop 61.40 fps, keyboard/touch normalized 300-unit/s movement, zero release speed, zero bound hits in the central exercises, zero modal displacement, zero reduced-motion camera lag and zero browser errors. A first successful-motion artifact was deliberately rejected by evaluation because the bee rendered at only ~6.7–6.9% viewport height; the final presentation iteration measures 13.33–14.17%, inside V-001's 12–15% band. The complete evidence and independent PASS are in [`evidence/P1-BEE-MOVEMENT/manifest.json`](evidence/P1-BEE-MOVEMENT/manifest.json).

**P2 — Pollination Core Loop is COMPLETE; `BB-020` through `BB-025` pass the P2 milestone gate.**

P2 turns traversal into the first complete production loop: data-driven flowers/patches; deterministic `LOCKED → AVAILABLE → ACTIVE → COMPLETED`; work from actual distance travelled inside forgiving bounds; zero work while stationary; one Honey transaction and one completion/audio event; dependent patch unlock; and durable completion/Honey through the existing A/B storage abstraction. No separate high-frequency pollination control was added.

Accepted runtime head `bc3f878254d800063822377d57e99e7e5d42efd7` passed Repository standards (`33244624975`), Test/data (`33244624972`) and HTML5 CI (`33244624996`). Retained movement/P2 artifact `9712446750` records desktop straight pass `337.56/410 = 82.33%`, mobile `339.99/410 = 82.92%`, stationary work `0.0`, Honey `+45` exactly once, patch #2 unlock, zero replayed reward after reload, representative movement `60.98 fps`, modal displacement `0.0`, reduced-motion camera lag `0.0/0.0` and zero P2 browser errors. Two green-CI visual candidates were deliberately rejected before acceptance: first for flowers hidden by the bee, then for mobile `LOCKED` overlapping the Honey HUD. The final retained stills resolve both. Complete evidence and independent PASS are in [`evidence/P2-POLLINATION-CORE-LOOP/manifest.json`](evidence/P2-POLLINATION-CORE-LOOP/manifest.json) and `evaluation.md`.

**P3 — Progression is COMPLETE for closeout; `BB-030` through `BB-034` pass the P3 milestone gate.**

P3 turns Honey into permanent, immediately observable power without reopening Yield: the Hive contains exactly two upgrade cards; Flight level 2 costs 30 Honey and raises real movement from 300 to 330 u/s; Buzz level 2 costs 35 Honey and raises pollination work from 1.00× to 1.35×; Lavender is the first explicit `REQUIRES BUZZ 2` gate; purchase input is isolated; save schema v2 migrates P2 v1 state and persists upgrades/gate eligibility; economy regression covers both purchase orders plus minimal-required/customization-heavy paths.

Accepted runtime head before closeout-only source-of-truth changes is `3b4b990923851217d9a25e2954a86443dea3916f`. It passed Repository standards (`33247411592`), Test/data (`33247411586`), Pages preview (`33247411600`) and HTML5 CI (`33247411645`). Retained movement/P3 artifact `9713299114`, digest `sha256:f7e1ce37eba04ecec26a23b42991f7bea4681ecdde64feaec8d225a1f7101ef9`, proves Flight `45→15 Honey / 330 u/s`, modal displacement `0.0`, Flight reload, Buzz `100→65 Honey / 1.35×`, Lavender `LOCKED requires_buzz 2 → AVAILABLE`, Buzz/gate reload and zero P3 browser errors. The previous mechanically green head was deliberately rejected for mobile card/gate readability; the accepted head resolves both findings. Complete evidence and independent PASS are in [`evidence/P3-PROGRESSION/manifest.json`](evidence/P3-PROGRESSION/manifest.json) and `evaluation.md`.

**Next production task after P3 merge: `P4 — First Meadow Restoration`.**
