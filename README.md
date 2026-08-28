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

- Engine: **Defold**
- Gameplay language: **Lua**
- Runtime target: **HTML5-first**
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

### Engineering/production

- [`docs/05-technical-architecture.md`](docs/05-technical-architecture.md)
- [`docs/06-production-roadmap.md`](docs/06-production-roadmap.md)
- [`docs/07-qa-analytics-release.md`](docs/07-qa-analytics-release.md)
- [`docs/12-platform-storage.md`](docs/12-platform-storage.md)
- [`docs/13-visual-qa-scorecard.md`](docs/13-visual-qa-scorecard.md)
- [`config/web-targets.json`](config/web-targets.json)

### Research/process

- [`docs/08-reference-analysis.md`](docs/08-reference-analysis.md)
- [`docs/10-development-workflow.md`](docs/10-development-workflow.md)
- [`docs/11-blueprint-hardening.md`](docs/11-blueprint-hardening.md)
- [`docs/15-agent-evidence-governance.md`](docs/15-agent-evidence-governance.md)
- [`docs/templates/feature-research.md`](docs/templates/feature-research.md)
- [`docs/templates/evidence-manifest.example.json`](docs/templates/evidence-manifest.example.json)
- [`.agents/skills/`](.agents/skills/) — reusable agent execution checklists

### Legal

- [`THIRD_PARTY.md`](THIRD_PARTY.md)

## Current product hypotheses that must not be mistaken for locked design

Before normal production, P-1 still needs product evidence for:

- the best repeatable pollination input model (auto / hold / movement-through);
- how seed choice participates in restoration;
- whether `Yield` deserves to remain an upgrade track;
- first-region pacing/no-grind behavior beyond the current deterministic arithmetic simulation;
- reproducible visual style and screenshot QA pipeline.

The objective-evidence hardening in `BB-P013`–`BB-P017` is already in place. `BB-P006` has validated Poki as the primary external target, with CrazyGames as fallback; see [`docs/research/BB-P006-primary-web-target.md`](docs/research/BB-P006-primary-web-target.md).

See [`docs/11-blueprint-hardening.md`](docs/11-blueprint-hardening.md) for the remaining P-1 exit criteria.

## Vertical-slice target

The intended slice still aims to prove:

- controllable expressive bee;
- several flower difficulty tiers;
- one compact authored region;
- satisfying pollination/bloom feedback;
- Honey economy;
- meaningful bee improvement;
- seeds that let players influence the recovering meadow;
- visible meadow/planet restoration;
- save/reload;
- desktop + touch controls;
- sound/VFX/accessibility basics;
- analytics abstraction;
- production-quality HTML5 build.

Exact interaction, stat and pacing values are validated through P-1/P2 rather than treated as immutable because they appeared in an early GDD.

## Non-goals for the vertical slice

No multiplayer, guilds, PvP, procedural infinite world, complex crafting tree, equipment loot treadmill, mandatory daily quests, backend account system, premium currency or battle pass.

## Current status

**P-1 — Blueprint Hardening.**

The repository now has enforceable evidence governance, a protected autonomous merge path, disposable BB-P003/BB-P004 product experiment harnesses, a deterministic BB-P005 economy simulator, and a validated primary web target. Remaining P-1 work is to collect/compare the core interaction and seed-flow evidence, settle the upgrade set, and establish reproducible visual style/capture constraints before normal production begins.

After P-1 exit criteria pass, continue with P0/BB-001 and the production roadmap.
