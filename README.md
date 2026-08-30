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
- [`config/privacy-contract.json`](config/privacy-contract.json) — deny-by-default optional telemetry and release privacy boundary
- [`config/telemetry-contract.json`](config/telemetry-contract.json) — platform lifecycle/optional telemetry field contract
- [`config/release-qa.json`](config/release-qa.json) — bundle, startup, device and negative-release QA budgets
- [`release/portal-metadata.json`](release/portal-metadata.json) — selected Poki/fallback CrazyGames launch metadata
- [`docs/visual/P8-art-certification.md`](docs/visual/P8-art-certification.md) — scoped release-candidate art certification
- [`evidence/P8-RELEASE-CANDIDATE/manifest.json`](evidence/P8-RELEASE-CANDIDATE/manifest.json) — exact-head release-candidate evidence

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
- [`docs/research/P4-first-meadow-restoration.md`](docs/research/P4-first-meadow-restoration.md) — P4 restoration reference analysis, implementation contract and accepted runtime trace
- [`evidence/P4-FIRST-MEADOW-RESTORATION/manifest.json`](evidence/P4-FIRST-MEADOW-RESTORATION/manifest.json) — P4 restoration closeout evidence and independent evaluation provenance
- [`docs/research/P5-seed-ownership.md`](docs/research/P5-seed-ownership.md) — P5 Hybrid seed ownership production contract and runtime trace
- [`evidence/P5-SEED-OWNERSHIP/manifest.json`](evidence/P5-SEED-OWNERSHIP/manifest.json) — P5 economy/runtime/visual closeout evidence and independent evaluation provenance
- [`docs/research/P6-first-region-vertical-slice.md`](docs/research/P6-first-region-vertical-slice.md) — P6 six-Meadow region, platform, settings, analytics and performance contract
- [`evidence/P6-FIRST-REGION-VERTICAL-SLICE/manifest.json`](evidence/P6-FIRST-REGION-VERTICAL-SLICE/manifest.json) — P6 full-region runtime/visual closeout evidence and independent evaluation provenance
- [`docs/research/P7-golden-fields-production-expansion.md`](docs/research/P7-golden-fields-production-expansion.md) — P7 Golden Fields content-scaling research, initial node-budget failure and bounded-renderer repair
- [`evidence/P7-GOLDEN-FIELDS/manifest.json`](evidence/P7-GOLDEN-FIELDS/manifest.json) — first P7 region-expansion runtime/economy/visual closeout evidence and independent evaluation provenance
- [`docs/research/P7-rosewood-production-expansion.md`](docs/research/P7-rosewood-production-expansion.md) — P7 Rosewood woodland expansion research and bounded content-scaling contract
- [`docs/templates/feature-research.md`](docs/templates/feature-research.md)
- [`docs/templates/evidence-manifest.example.json`](docs/templates/evidence-manifest.example.json)
- [`.agents/skills/`](.agents/skills/) — reusable agent execution checklists

### Legal

- [`THIRD_PARTY.md`](THIRD_PARTY.md)

## Validated product structure vs open tuning

`D-006` is `VALIDATED`: default pollination is movement-through/sweep — qualifying movement inside a pollinatable patch advances progress, standing still does not, and the default scheme has no separate high-frequency pollination button. P2 productionizes this with forgiving authored bounds and work targets above one full forgiving-zone diameter; the first Daisy straight pass reaches 82.33% desktop / 82.92% mobile rather than completing incidentally. These values remain tunable rather than LOCKED.

`D-008` is `VALIDATED`: the default persistent HUD remains one objective plus Honey, while pollination state/progress lives in world space with redundant cues. P2 exact-head desktop/Poki/mobile evidence specifically iterated a mobile `LOCKED`/Honey overlap before accepting the baseline. P4 retains the same density and proves the restoration change remains legible with the HUD hidden.

`D-005` is `VALIDATED`: seed ownership uses the Hybrid restoration topology and P5 now productionizes it. Authored native campaign patches keep their native identity/progression, while two dedicated `YOUR PLOT` spaces carry player-owned Daisy/Clover/Lavender species before full restoration. Ownership costs `15 / 18 / 22 Honey` once, owned replant is free, and save v3 keeps `player.seed_unlocks` / `world.player_plants` independent from native `world.campaign_completion`. Exact-head desktop/touch evidence proves real planting, replant and reload without mutating campaign truth.

`D-007` is `VALIDATED`: the vertical slice uses **Flight + Buzz** as its bee upgrade tracks and Yield remains excluded. P3 productionizes level 2 as Flight `300 → 330 u/s` for `30 Honey` and Buzz `1.00× → 1.35×` pollination work for `35 Honey`; P6 extends the tested first-region curve to Flight 3 `330 → 360 u/s` and Buzz 3 `1.35× → 1.65×`, with Lily as the explicit `REQUIRES BUZZ 3` climax gate. Exact later-region tuning remains open rather than locked by the vertical slice.

`D-013` is `VALIDATED`: P1 uses one normalized direct-intent movement controller for keyboard and floating touch, with bounded acceleration/deceleration, authored bounds, bounded orthographic follow and a reduced-motion direct-follow path. The 300-unit/s value is the Flight-level-1 baseline; P3 Flight 2 raises the computed maximum to 330 u/s and P6 Flight 3 to 360 u/s without changing controller semantics. P4 also proves the final restoration reveal is non-blocking: browser input moves the bee 86.644 design units during the 1.5-second accent.

P4 productionizes the first visible restoration ladder without adding a new currency, restoration button or save field. `r01_m01` derives `DORMANT → WAKING → GROWING → RESTORED` from stable completed patch IDs. Accepted HUD-hidden evidence measures ground mix `0.00 → 0.68 → 1.00`, detail count `8 → 22 → 28`, ambient life `0 → 2 → 6`, midpoint/final reload safety and zero P4 browser errors. Evidence strength is MEDIUM because this is autonomous runtime/rendered proof, not an external novice playtest or final production-art evaluation.

P5 adds player ownership without weakening that restoration contract. Its deterministic economy regression covers all `120/120` priority orders across Flight 2, Buzz 2 and the three first seed unlocks; no order requires replay/grind and all first sinks leave `50 Honey`. Accepted browser evidence shows Daisy `45→30`, Daisy+Clover retained at `67 Honey`, free Daisy replant `67→67`, native completion unchanged, save v3 reload intact and direct mobile-touch planting with zero P5 browser errors.

P6 validates `D-011` as one continuous authored **six-Meadow Sunny Meadows** region rather than six collection-proxy screens. The exact-head clean-save proof restores 6/6 Meadows, reaches Flight/Buzz 3, exercises seed ownership, settings, analytics and save-v4 reload, keeps browser errors and external requests at zero, measures `59.92 fps` against the `≥50` budget and packages a `2,813,096`-byte release bundle against the 12 MiB budget. Desktop canvas coverage is exactly `1280×720`, with retained 844×390 mobile and 640×360 / 836×470 / 1031×580 Poki checks. The independent closeout verdict is **PASS WITH DEVIATION**: the region/system structure is validated, while final rounded bee/species-silhouette/typography illustration polish remains below the long-term art-direction target and is explicitly carried into P7/P8.

P7 Golden Fields validates the first **multi-region production-expansion seam**. A persisted P6-complete state derives `region_02` automatically, then the normal runtime restores Sun Gate, Poppy Run, Windmill Loop and Harvest Crown from 0/4 to 4/4 with the same movement-through pollination verb. Honey moves `346 → 891` with no new mandatory spend/replay, campaign state reloads at 2/2 regions complete, analytics stays platform-neutral, P7 browser errors/external requests are `0/0/0`, and current performance remains `59.87 fps` with a `2,815,539`-byte bundle. The first Golden Fields HTML5 run exposed `Out of nodes (max 512)`; the accepted architecture repair keeps `max_nodes: 512` and uses six reusable nearby-patch visual slots instead of permanent per-patch GUI trees. Independent verdict is **PASS WITH DEVIATION** for the Golden Fields slice; P7 as a milestone remains IN PROGRESS.

P7 Moon Garden completes the authored chain as the sixth region: Lumen Orchard, Starfall Glade, Comet Clearing and Moon Crown restore from 0/4 to 4/4 through the existing movement-through pollination path. The exact journey starts at `3636 Honey` and ends at `4846 Honey`, derives the six-region campaign, preserves save v4 and the six-slot GUI pool, and carries only the documented geometric-art deviation into P8. Research and evidence are [`docs/research/P7-moon-garden-production-expansion.md`](docs/research/P7-moon-garden-production-expansion.md), [`evidence/P7-MOON-GARDEN/manifest.json`](evidence/P7-MOON-GARDEN/manifest.json) and [`evidence/P7-MOON-GARDEN/evaluation.md`](evidence/P7-MOON-GARDEN/evaluation.md).

Still open/tunable before downstream milestones lock production values:

- Honey rewards/cost tables and pacing beyond the accepted Golden Fields path;
- later Flight/Buzz effect curves and gate cadence beyond Buzz 3;
- later player-plot count/placement and seed catalog/pacing beyond the validated first-region topology;
- exact-head P7 evidence and closeout records for the accepted Alpine Bloom and Moon Garden slices;
- external novice comprehension/playtest evidence;
- final production illustration/animation/typography and full-scene visual polish required to clear the P6/P7 art-direction deviation before release certification.

The objective-evidence hardening in `BB-P013`–`BB-P017` is in place. `BB-P006` validated Poki as the primary external target, `BB-P007` defined V-001, `BB-P008` defined the deterministic visual-QA runtime contract, and `BB-P009` defined the HTML5 A/B generation storage/recovery contract.

At P-1 closeout, repository enforcement was verified through ruleset `Protect main`: pull requests plus `validate-pr-evidence`, strict/up-to-date checks, zero approvals and no bypass actors. The retained closeout evidence is [`docs/research/BB-P017-ruleset-closeout.md`](docs/research/BB-P017-ruleset-closeout.md) and [`evidence/BB-P017-RULESET-CLOSEOUT/ruleset-snapshot.json`](evidence/BB-P017-RULESET-CLOSEOUT/ruleset-snapshot.json). If enforcement is temporarily disabled for repository maintenance, it must be restored before normal protected development continues.

## Vertical-slice target

P6 now proves the structural vertical-slice target: controllable movement, several flower difficulty tiers, one compact authored region, movement-through pollination, Honey economy, Flight/Buzz progression, seed ownership, visible restoration, save/reload, desktop + touch controls, local audio, accessibility settings, analytics abstraction and a production HTML5 build path. P7 Golden Fields, Wetland Garden, Rosewood, Alpine Bloom and Moon Garden prove that the same architecture scales into authored regions without a new core system or per-region game-world lifecycle. Exact stat/pacing values remain runtime-validated tunings rather than immutable values simply because they appeared in an early GDD.

The remaining explicitly documented deviation is final illustration/animation/typography/full-scene polish; it does not invalidate the functional region architecture but must be resolved before release-candidate visual certification.

## Non-goals for the vertical slice

No multiplayer, guilds, PvP, procedural infinite world, complex crafting tree, equipment loot treadmill, mandatory daily quests, backend account system, premium currency or battle pass.

## Current status

**P0 — Foundation is COMPLETE. `BB-001` through `BB-007` are complete and all P0 exit criteria pass.**

BB-001 establishes a minimal `app/` bootstrap, explicit development/release settings and a reproducible editor-independent HTML5 path. The toolchain is pinned to Defold **1.13.1**, OpenJDK **25**, `wasm-web` and the published Bob SHA-256. Exact-head CI successfully built both development and release bundles and rendered the bootstrap in Chromium before merge.

BB-002 adds Defold-aware generated-file rules, explicit text/Lua conventions, canonical production resource roots, machine-readable dependency/license inventory, a dependency-free repository validator and PR/main CI enforcement. It does not claim semantic input, proxy lifecycle, storage, gameplay, UI, test/data harness or deterministic gameplay QA.

BB-003 replaces the empty binding with device-independent semantic actions, proves keyboard and HTML5 single-touch/pointer paths, explicitly owns collection-proxy input focus, and retains an exact-head Chromium proof that unconsumed actions traverse the proxy world while an open modal consumes them before proxied gameplay and lower main-world listeners. That input/focus contract remains valid; the older separate-region proxy hypothesis `T-010` is later deprecated by the P6/P7 multi-region evidence in favor of `T-013`.

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

**P3 — Progression is COMPLETE; `BB-030` through `BB-034` pass the P3 milestone gate.**

P3 turns Honey into permanent, immediately observable power without reopening Yield: the Hive contains exactly two upgrade cards; Flight level 2 costs 30 Honey and raises real movement from 300 to 330 u/s; Buzz level 2 costs 35 Honey and raises pollination work from 1.00× to 1.35×; Lavender is the first explicit `REQUIRES BUZZ 2` gate; purchase input is isolated; save schema v2 migrates P2 v1 state and persists upgrades/gate eligibility; economy regression covers both purchase orders plus minimal-required/customization-heavy paths.

Accepted runtime head before closeout-only source-of-truth changes is `3b4b990923851217d9a25e2954a86443dea3916f`. It passed Repository standards (`33247411592`), Test/data (`33247411586`), Pages preview (`33247411600`) and HTML5 CI (`33247411645`). Retained movement/P3 artifact `9713299114`, digest `sha256:f7e1ce37eba04ecec26a23b42991f7bea4681ecdde64feaec8d225a1f7101ef9`, proves Flight `45→15 Honey / 330 u/s`, modal displacement `0.0`, Flight reload, Buzz `100→65 Honey / 1.35×`, Lavender `LOCKED requires_buzz 2 → AVAILABLE`, Buzz/gate reload and zero P3 browser errors. The previous mechanically green head was deliberately rejected for mobile card/gate readability; the accepted head resolves both findings. Complete evidence and independent PASS are in [`evidence/P3-PROGRESSION/manifest.json`](evidence/P3-PROGRESSION/manifest.json) and `evaluation.md`.

**P4 — First Meadow Restoration is COMPLETE for milestone closeout; the P4 exit criteria pass.**

P4 turns the existing P2/P3 journey into a visible world payoff. The first authored meadow now derives four stages — `DORMANT → WAKING → GROWING → RESTORED` — from stable campaign patch completion IDs, with no schema v3 and no duplicated persisted meadow-stage field. The environment changes through ground mix, detail density and ambient life; the final 1.5-second accent remains non-blocking; no modal tutorial or second restoration button is introduced.

Accepted runtime head before closeout-only source-of-truth changes is `a45f9dac2f9d7136c3da51dc5b761eb0c05ce739`. It passed Repository standards (`33249086788`), Test/data (`33249086793`), Pages preview (`33249086822`) and HTML5 CI (`33249086913`). Retained movement/P4 artifact `9713808008`, digest `sha256:7385f1161ad2c68a91027bbc5585b6246abb14fdc56c42929ade4f158d8369ec`, records ground mix `0.00→0.68→1.00`, details `8→22→28`, ambient life `0→2→6`, HUD-hidden desktop/Poki-small readability, mobile restored coverage, `86.644` units of movement during the reveal, midpoint/final reload safety, no replayed celebration after restored reload, deterministic clean canonical fixtures and zero P4 browser errors. Two pre-acceptance defects — restored-reload celebration replay and storage-dependent canonical fixture ambiguity — were fixed before evidence acceptance. Complete evidence and independent PASS are in [`evidence/P4-FIRST-MEADOW-RESTORATION/manifest.json`](evidence/P4-FIRST-MEADOW-RESTORATION/manifest.json) and `evaluation.md`.

**P5 — Seed Ownership During Restoration is COMPLETE for milestone closeout; the P5 exit criteria pass.**

P5 productionizes the validated Hybrid topology with two dedicated player-shaped plots and three one-time seed unlocks. Native Daisy/Clover/Lavender campaign patches remain authored and progression-bearing; player plots independently hold chosen species. Daisy/Clover/Lavender cost `15 / 18 / 22 Honey`, owned replant costs `0`, and save v3 adds `player.seed_unlocks` plus `world.player_plants` while leaving native `world.campaign_completion` separate.

Accepted runtime head before closeout-only source-of-truth changes is `8967ab565bc9ff9c7838344676587fbf0a6d2ae0`. It passed Repository standards (`33251552722`), Test/data (`33251552769`, `92/92`), Pages preview (`33251552723`) and HTML5 CI (`33251552740`). Retained movement/P5 artifact `9714546464`, digest `sha256:64a04641fbd44542217ded406f785115b5939c8cd593436ec094f1b452e5e4ce`, proves Daisy `45→30`, Clover ownership, free Daisy replant at Honey `67→67`, unchanged native completion, save v3 reload, direct 844×390 touch planting and zero P5 browser errors. P5 economy regression passes all `120/120` first-sink priority orders with final Honey `50`. CI also found and forced fixes for a real mobile coordinate double-conversion bug and a stale v2 BB-007 storage-probe fixture before acceptance. Complete evidence and independent PASS are in [`evidence/P5-SEED-OWNERSHIP/manifest.json`](evidence/P5-SEED-OWNERSHIP/manifest.json) and `evaluation.md`.

**P6 — First Region Vertical Slice is COMPLETE for milestone closeout with independent verdict `PASS WITH DEVIATION`; all functional P6 exit gates pass.**

P6 turns the retained P1–P5 systems into one continuous authored Sunny Meadows region with six Meadow beats, Tulip/Lily late-region species, Flight/Buzz 3, Lily's Buzz-3 capability gate, region-level progress, save v4 settings, local completion audio and a platform-neutral analytics adapter. No world-map menu or per-Meadow collection-proxy architecture is added.

Accepted runtime evidence head before closeout-only source-of-truth changes is `1001783236aac0ca2052bf6b4498c600a5dbf6fb`. It passed Repository standards (`33269124642`), Test/data (`33269124670`, `102/102`), Pages preview (`33269124643`) and HTML5 CI (`33269124636`). Retained movement/P6 artifact `9719600537`, digest `sha256:77f0b0972eb7ba12bac3e292f429a6c1689820e9984b0d28bee5f2e527e3c9de`, proves a clean-save 6/6 region journey, Flight/Buzz 3, Lily `LOCKED requires_buzz 3 → AVAILABLE`, seed-system use, reduced motion + audio mute, deterministic analytics, completed-region reload, browser errors `0/0` and external requests `0`. Measured engine FPS is `59.92` against `≥50`; release bundle is `2,813,096` bytes against a 12 MiB budget; retained canvas proof is exactly `1280×720` plus mobile and three Poki viewports.

The independent evaluator records **PASS WITH DEVIATION**, not plain PASS: the current original geometric runtime presentation is coherent/readable but still falls short of the long-term rounded bee, species-silhouette and final typography/illustration direction. That deviation is explicit P7/P8 work and may not be silently treated as release-candidate art. Complete evidence is in [`evidence/P6-FIRST-REGION-VERTICAL-SLICE/manifest.json`](evidence/P6-FIRST-REGION-VERTICAL-SLICE/manifest.json) and `evaluation.md`.

**P7 — Production Expansion is IN PROGRESS; Golden Fields is accepted as the first P7 slice with independent verdict `PASS WITH DEVIATION`.**

Golden Fields adds `region_02` with Sun Gate, Poppy Run, Windmill Loop and Harvest Crown, plus Sunflower/Poppy presentation and authored landmarks, while reusing the existing movement/pollination/Honey/Flight/Buzz/restoration/save/analytics systems. The active region is data-driven from the first incomplete campaign region; P6 QA fixtures remain explicitly pinned to `region_01`.

Accepted runtime evidence head before closeout-only source-of-truth changes is `8d9640522ffc742ffe79178718fa2df0517dd6bc`. It passed Repository standards (`33271607224`), Test/data (`33271607179`, `108/108`), Pages preview (`33271607241`) and HTML5 CI (`33271607193`). Retained movement/P7 artifact `9720322590`, digest `sha256:b58dc0c217aa1845a3f42a2b1cf2fcb4685f2a548f452d09be50d00cbeb0fd80`, starts from persisted P6 completion, removes the QA route, derives Golden Fields at 0/4, completes 4/4, moves Honey `346→891`, records 11 P7 analytics events, reloads at 2/2 campaign regions complete, and reports browser errors `0/0` plus external requests `0`. Current combined performance is `59.87 fps` and a `2,815,539`-byte release bundle.

The first P7 HTML5 attempt failed with `Out of nodes (max 512)`. That failure was treated as a real scalability defect: the accepted implementation keeps the GUI budget at `512` and replaces permanent per-authored-patch flower trees with a six-slot nearby-patch visual pool. The independent evaluator records **PASS WITH DEVIATION** because the multi-region architecture is validated but rounded character/species illustration, typography and full-scene polish are still below release-art target.

Complete evidence is in [`docs/research/P7-golden-fields-production-expansion.md`](docs/research/P7-golden-fields-production-expansion.md), [`evidence/P7-GOLDEN-FIELDS/manifest.json`](evidence/P7-GOLDEN-FIELDS/manifest.json) and `evaluation.md`.

**P7 — Production Expansion is IN PROGRESS; Golden Fields, Wetland Garden and Rosewood are accepted with independent verdict `PASS WITH DEVIATION`.**

Rosewood adds `region_04` with Rose Glade, Bluebell Hollow, Cedar Turn and Woodland Crown. It reuses movement-through pollination, Honey, Flight/Buzz 3, restoration, save v4 and platform-neutral analytics. Exact retained evidence derives Rosewood at `0/4` from persisted regions 01–03, completes `4/4`, reloads all four campaign regions, moves Honey `1596→2506`, and records zero browser/page/external errors. The GUI budget remains `max_nodes: 512`, the nearby patch pool remains six slots, movement reaches the expanded bounds and the release bundle remains `2,818,788` bytes under the 12 MiB budget.

The Rosewood research, manifest and independent evaluation are [docs/research/P7-rosewood-production-expansion.md](docs/research/P7-rosewood-production-expansion.md), [evidence/P7-ROSEWOOD/manifest.json](evidence/P7-ROSEWOOD/manifest.json) and [evidence/P7-ROSEWOOD/evaluation.md](evidence/P7-ROSEWOOD/evaluation.md). The remaining P7 region sequence is Alpine Bloom, then Moon Garden; final geometric illustration/animation/typography certification remains P8 work.
