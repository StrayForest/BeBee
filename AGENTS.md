# AGENTS.md — BeBee implementation contract

This file is the operating contract for humans and coding agents working in this repository.

## 1. Source of truth

Read these before implementing gameplay:

1. `docs/00-product-vision.md`
2. `docs/01-game-design.md`
3. `docs/02-progression-economy.md`
4. `docs/03-ux-ui-controls.md`
5. `docs/04-world-content.md`
6. `docs/05-technical-architecture.md`
7. `docs/06-production-roadmap.md`
8. `docs/07-qa-analytics-release.md`

If implementation conflicts with the docs, either implement the docs or update the design decision explicitly. Do not silently invent a second design.

## 2. Product rules

- BeBee must remain a cozy, readable, low-friction game.
- The primary loop is `pollinate -> honey -> upgrade -> unlock -> customize -> restore`.
- The world must become visibly more alive as the player progresses.
- Do not add combat to solve a content problem.
- Do not add currencies without a written economic reason.
- Do not add a hard energy/wait timer to MVP.
- Do not create feature systems for hypothetical future content before the current milestone needs them.
- Every new feature must answer: what player problem does this solve, and how is success measured?

## 3. Technical rules

- Engine: Defold.
- Gameplay language: Lua.
- HTML5 is the primary development target; Android/iOS compatibility must not be knowingly broken.
- Use data-driven definitions for flowers, patches, seeds, upgrades, regions and rewards.
- Core simulation modules must not depend directly on GUI nodes.
- GUI reads state through presentation/view-model modules and sends commands/events back.
- Save data is versioned from the first playable build.
- Randomness that affects persistent state must be seedable/deterministic where practical.
- Prefer small explicit modules over broad service locators or giant manager scripts.
- Avoid premature ECS/framework construction. Defold collections/game objects/components are sufficient until profiling proves otherwise.
- Avoid per-frame allocation in hot loops and resource-node spawning.
- Pool frequently spawned VFX/collectible feedback when profiling shows pressure.

## 4. Implementation order

Never build the full content set first. Follow this order:

1. movement/camera;
2. one flower patch;
3. pollination feedback;
4. honey reward;
5. one upgrade;
6. one unlock gate;
7. save/load;
8. one complete meadow transformation;
9. touch controls;
10. only then scale content.

## 5. Definition of done for gameplay work

A gameplay task is not done when the code compiles. It is done when:

- acceptance criteria are met;
- keyboard and touch paths both work where relevant;
- save/load behavior is covered;
- player-facing states have feedback (visual and, when appropriate, audio/haptic);
- no new warnings/errors are introduced;
- deterministic logic has tests where practical;
- the task includes a short manual QA recipe;
- analytics events are added for economy/progression changes when required by `docs/07-qa-analytics-release.md`.

## 6. UX guardrails

- Keep the playfield unobstructed. Persistent HUD must be sparse.
- Never require the player to open a menu to understand the immediate next objective.
- Important interactions require one primary action, not a chain of confirmations.
- Do not steal the camera for mission guidance. Use world markers/edge arrows instead.
- Avoid tiny text and tiny tap targets. Touch target baseline: 44 logical px minimum.
- Avoid modal popups during active movement except pause/settings or explicit player actions.
- Currency changes and unlocks need immediate, legible feedback.

## 7. Art/content guardrails

- Competitor games are references for patterns, not assets to copy.
- Do not copy Cow Bay/7Spot art, maps, characters, text, sounds, layouts pixel-for-pixel or proprietary code.
- Imported third-party assets require a compatible license and attribution record in `THIRD_PARTY.md`.
- Prefer original bee/flower/world assets or explicitly licensed packs.
- All flower silhouettes must remain distinguishable at gameplay zoom.

## 8. Git workflow

- `main` is releasable documentation/code.
- Feature work uses focused branches such as `feat/pollination-loop`.
- One concern per PR where practical.
- PR description includes: behavior change, test evidence, screenshots/video for visual work, save migration impact, and known limitations.
- Do not merge if HTML5 build is broken.

## 9. Scope discipline

If a requested change does not improve the current milestone, add it to a backlog document/issue instead of implementing it immediately. The goal is a released game, not maximum code volume.
