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
- [`config/visual-qa.json`](config/visual-qa.json) — deterministic QA-state/capture contract
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
- [`docs/templates/feature-research.md`](docs/templates/feature-research.md)
- [`docs/templates/evidence-manifest.example.json`](docs/templates/evidence-manifest.example.json)
- [`.agents/skills/`](.agents/skills/) — reusable agent execution checklists

### Legal

- [`THIRD_PARTY.md`](THIRD_PARTY.md)

## Validated product structure vs open tuning

`D-006` is `VALIDATED`: default pollination is movement-through/sweep — qualifying movement inside a pollinatable patch advances progress, standing still does not, and the default scheme has no separate high-frequency pollination button. Exact movement/work tuning remains a P2 task.

`D-005` is `VALIDATED`: seed ownership uses a Hybrid restoration topology. Authored native campaign plots keep their native identity during restoration, dedicated player-shaped plots allow seed ownership before full completion, and campaign/native state remains separate from planted species. P5 still must prove that the two roles are understandable in the rendered game and tune the exact plot count, placement, planting input and seed economy.

`D-007` is `VALIDATED`: the vertical slice uses **Flight + Buzz** as its bee upgrade tracks. Yield is excluded rather than preserved as a third card. BB-P005 showed that the current no-Yield structure reaches region completion across all **5040 / 5040** full retained-sink purchase-priority orders with zero replay and non-negative balance. Exact Flight/Buzz effects, Honey costs/rewards and real-time purchase cadence remain P1/P3 tuning work.

Still open/tunable before downstream milestones lock production values:

- exact movement/pollination work and timing;
- exact Honey reward/cost table and minutes/actions between meaningful purchases;
- final Flight/Buzz effect curves and flower-gate tuning;
- rendered comprehension/input/seed pacing for the Hybrid restoration flow;
- runtime proof that the validated V-001 style/crop rules survive the deterministic Defold HTML5 capture pipeline once P0 creates the production runtime.

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

**P0 — Foundation is in progress. `BB-001` through `BB-005` are complete.**

BB-001 establishes a minimal `app/` bootstrap, explicit development/release settings and a reproducible editor-independent HTML5 path. The toolchain is pinned to Defold **1.13.1**, OpenJDK **25**, `wasm-web` and the published Bob SHA-256. Exact-head CI successfully built both development and release bundles and rendered the bootstrap in Chromium before merge.

BB-002 adds Defold-aware generated-file rules, explicit text/Lua conventions, canonical production resource roots, machine-readable dependency/license inventory, a dependency-free repository validator and PR/main CI enforcement. It does not claim semantic input, proxy lifecycle, storage, gameplay, UI, test/data harness or deterministic gameplay QA.

BB-003 replaces the empty binding with device-independent semantic actions, proves keyboard and HTML5 single-touch/pointer paths, explicitly owns collection-proxy input focus, and retains an exact-head Chromium proof that unconsumed actions traverse the proxy world while an open modal consumes them before proxied gameplay and lower main-world listeners. `T-010` remains a hypothesis because proxy memory/full lifecycle are still unproven, and final touch movement UX remains a later player-facing decision.

BB-004 adds a dependency-free deterministic Lua test runner, a dedicated Defold headless test bootstrap, a canonical content catalog plus stable-ID/reference validation, and 11 initial deterministic cases covering input semantics and data-validation success/failure paths. The editor-independent runner verifies the pinned Bob/Java toolchain, requires a structured suite completion event, propagates failures through process exit status and retains diagnostic output. GitHub Actions runs the same command on PRs and `main` with read-only permissions.

BB-005 turns the existing runtime evidence path into exact-source **HTML5 CI** for every PR and `main` update: pinned development/release `wasm-web` builds, release Chromium startup/resource/console smoke, retained BB-003 keyboard/touch/proxy smoke, a dedicated playable release artifact and separate diagnostic evidence. The first strict smoke correctly stopped on Chromium's automatic favicon 404; retained network evidence proved all game resources healthy, so the check was narrowed only for that browser-generated request while all other HTTP 4xx/5xx remain fatal. Candidate run `33213154271` then passed and retained playable artifact `9702369697` plus evidence artifact `9702370265` on exact head `3c50ca49…`.

**Next production task: `P0 / BB-006 — Visual QA harness foundation`.**
