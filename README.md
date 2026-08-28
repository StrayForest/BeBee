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

## Technology

- Engine: **Defold**
- Gameplay language: **Lua**
- Runtime target: **HTML5-first**
- Secondary targets: mobile/native only after browser validation
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

When older documentation conflicts with `DECISIONS.md`, the decision registry wins.

## Mandatory development method

```text
problem
 -> decision status check
 -> shipped reference research
 -> current official developer docs
 -> implementation brief + acceptance criteria
 -> smallest complete implementation/prototype
 -> tests + HTML5 build
 -> screenshots/video of the actual build
 -> reference/quality scorecard
 -> iteration
 -> PR evidence
 -> merge
```

Player-facing work is not accepted merely because code runs. See [`docs/10-development-workflow.md`](docs/10-development-workflow.md) and [`docs/13-visual-qa-scorecard.md`](docs/13-visual-qa-scorecard.md).

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

### Research/process

- [`docs/08-reference-analysis.md`](docs/08-reference-analysis.md)
- [`docs/10-development-workflow.md`](docs/10-development-workflow.md)
- [`docs/11-blueprint-hardening.md`](docs/11-blueprint-hardening.md)
- [`docs/templates/feature-research.md`](docs/templates/feature-research.md)
- [`.agents/skills/`](.agents/skills/) — reusable agent execution checklists

### Legal

- [`THIRD_PARTY.md`](THIRD_PARTY.md)

## Current product hypotheses that must not be mistaken for locked design

Before normal production, P-1 must validate:

- the best repeatable pollination input model (auto / hold / movement-through);
- how seed choice participates in restoration;
- whether `Yield` deserves to remain an upgrade track;
- first-region economy/no-grind paths;
- primary web distribution target;
- reproducible visual style and screenshot QA pipeline.

See [`docs/11-blueprint-hardening.md`](docs/11-blueprint-hardening.md).

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

The repository is not yet declaring the original blueprint “complete.” The immediate work is to convert the highest-impact assumptions into validated decisions, remove remaining contradictions, select the primary web target, specify deterministic visual QA/storage behavior and prove the core interaction/economy before normal production begins.

After P-1 exit criteria pass, continue with P0/BB-001 and the production roadmap.
