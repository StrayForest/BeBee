# BeBee

BeBee is a cozy 2D pollination-and-restoration game about a tiny bee bringing a barren planet back to life.

The product direction deliberately uses proven interaction patterns from accessible resource/progression games such as Cow Bay, Cow Castle, Olly the Paw, My Little Universe, Dreamdale and open-source incremental-game references, while keeping BeBee's theme, mechanics, art, content and code original.

## Core fantasy

You are a small bee. You fly through compact meadows, pollinate flower patches, earn honey, upgrade the bee, unlock harder flowers, buy seeds and redesign restored meadows. The long-term objective is visible and simple: make the whole planet bloom.

## Product principles

1. **One obvious loop:** pollinate -> earn honey -> upgrade -> unlock -> customize -> restore.
2. **Movement should feel good before content is added.** No feature may compensate for weak movement/feedback.
3. **Very low cognitive load.** The player should understand the next useful action without reading a manual.
4. **Visible restoration.** Every meaningful action changes the world visually.
5. **Customization is progression, not decoration-only.** Seeds let players decide what restored land becomes.
6. **No mandatory combat in the core game.** Difficulty comes from flower requirements, terrain and efficiency.
7. **No hard energy timer in MVP.** Session pacing comes from goals, unlocks and spatial progression rather than waiting.
8. **HTML5 first, mobile-ready.** Desktop and touch controls are first-class from the start.
9. **Data-driven content.** Flower types, zones, upgrades, seed recipes and rewards live in data definitions rather than scattered game logic.
10. **Ship a vertical slice early.** One polished region is more valuable than ten unfinished systems.
11. **Research before implementation.** Significant features begin with competitor/reference research and current official developer documentation, not immediate coding.
12. **Look at the rendered result.** Player-facing changes require screenshots/video, inspection and comparison with the selected references before merge.

## Technology decision

- Engine: **Defold**
- Language: **Lua**
- Primary launch target: **HTML5**
- Secondary targets: Android / iOS after the browser vertical slice is validated
- Rendering: 2D top-down / slight 3/4 presentation
- Save: versioned local save in MVP; cloud/account layer only if product metrics justify it
- Analytics: event abstraction from day one; provider selected before public beta

Defold is selected because BeBee is a small, interaction-heavy 2D title targeting web and mobile, and the engine has a small runtime, direct HTML5/mobile support and a workflow well suited to a data-driven Lua game.

## Mandatory development method

For meaningful features, the repository uses this order:

```text
problem definition
 -> shipped-game reference research
 -> official developer documentation
 -> implementation brief + acceptance criteria
 -> implementation
 -> tests + HTML5 build
 -> screenshots/video of actual BeBee build
 -> visual/interaction comparison against references
 -> iteration
 -> PR evidence
 -> merge
```

A coding agent must not jump directly from a ticket to code. Full rules live in [`docs/10-development-workflow.md`](docs/10-development-workflow.md), and substantial work should use [`docs/templates/feature-research.md`](docs/templates/feature-research.md).

Competitor references are used to learn proven interaction, information hierarchy, controls, feedback and pacing. They are not permission to copy proprietary assets, code, maps, text or pixel-identical UI.

## Documentation

- [`docs/00-product-vision.md`](docs/00-product-vision.md) — product vision, audience, pillars and scope
- [`docs/01-game-design.md`](docs/01-game-design.md) — moment-to-moment gameplay and complete game loop
- [`docs/02-progression-economy.md`](docs/02-progression-economy.md) — honey economy, upgrades, flowers, seeds and balancing model
- [`docs/03-ux-ui-controls.md`](docs/03-ux-ui-controls.md) — HUD, menus, controls, onboarding and interaction rules
- [`docs/04-world-content.md`](docs/04-world-content.md) — planet structure, biomes, meadow templates and customization
- [`docs/05-technical-architecture.md`](docs/05-technical-architecture.md) — Defold architecture, modules, state, saves and performance budgets
- [`docs/06-production-roadmap.md`](docs/06-production-roadmap.md) — milestones and ticket IDs from empty repository to production
- [`docs/07-qa-analytics-release.md`](docs/07-qa-analytics-release.md) — tests, telemetry, release gates and live-quality rules
- [`docs/08-reference-analysis.md`](docs/08-reference-analysis.md) — competitor/open-source research and reuse boundaries
- [`docs/09-art-direction.md`](docs/09-art-direction.md) — bee, flowers, restoration visuals, UI skin, animation and audio direction
- [`docs/10-development-workflow.md`](docs/10-development-workflow.md) — mandatory research-first implementation and visual comparison process
- [`docs/templates/feature-research.md`](docs/templates/feature-research.md) — reusable evidence/decision template for substantial features
- [`AGENTS.md`](AGENTS.md) — implementation contract for Codex/AI-assisted development
- [`THIRD_PARTY.md`](THIRD_PARTY.md) — mandatory dependency/asset license ledger

## MVP definition

The MVP is not “the whole planet.” It is one polished region proving the complete loop:

- controllable bee;
- 3 flower difficulties;
- 6 meadows in the vertical-slice region;
- pollination feedback;
- honey currency;
- 3 upgrade tracks;
- 4+ seed types;
- meadow replanting/customization;
- region/planet restoration progress;
- save/load;
- desktop + touch controls;
- sound, particles and basic accessibility;
- analytics events;
- production HTML5 build.

If that slice is not fun, understandable and visually satisfying, content production stops until the loop is fixed.

## Non-goals for the first release

No multiplayer, guilds, PvP, procedural infinite world, complex crafting tree, equipment inventory, loot rarity treadmill, mandatory daily quests, backend account system or live-service battle pass.

## Current status

**Phase 0 — product blueprint complete.** The next implementation step is `P0 / BB-001`: create the Defold project bootstrap and a reproducible HTML5 build, then follow `docs/06-production-roadmap.md` in order. Every substantial implementation task must also follow `docs/10-development-workflow.md`.
