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
9. `docs/08-reference-analysis.md`
10. `docs/09-art-direction.md`
11. `docs/10-development-workflow.md`

If implementation conflicts with the docs, either implement the docs or update the design decision explicitly. Do not silently invent a second design.

## 2. Mandatory research-first workflow

**Do not begin a meaningful feature by writing code.**

Before implementation, follow `docs/10-development-workflow.md`.

For every substantial player-facing feature, the required order is:

1. define the exact player/system problem;
2. inspect at least two relevant shipped-game references when reasonably available;
3. record what those references do well and what BeBee should deliberately do differently;
4. read the relevant current official Defold/platform/library documentation;
5. write acceptance criteria and a compact implementation brief;
6. implement the smallest complete version;
7. build and run relevant automated/manual checks;
8. render the actual game and capture screenshots/video;
9. inspect the captures rather than assuming the result looks correct;
10. compare BeBee with the selected references for hierarchy, simplicity, readability, interaction cost, feedback, timing and mobile behavior;
11. iterate when the comparison exposes a gap;
12. only then open/finalize the PR for merge.

Use `docs/templates/feature-research.md` for substantial work.

### Research rules

- Competitors are behavioral/UX references, not assets to copy.
- Prefer shipped products over speculative design articles for player-facing patterns.
- Prefer official technical documentation over snippets, forum answers or AI memory for engine/API behavior.
- Verify APIs instead of inventing names or relying on stale knowledge.
- Record source links and relevant version/date when behavior is version-sensitive.
- If competitor research or official-doc research is genuinely not applicable, state why in the PR rather than silently skipping it.

### Visual QA rules

Player-facing code is not done until the rendered result has been inspected.

- Capture representative BeBee screenshots for visual work.
- Use video/GIF/frame sequences when timing, camera or motion is the important variable.
- Compare against reference behavior, not pixel identity.
- Desktop default comparison viewport: `1440x900` where practical.
- Mobile portrait default comparison viewport: `390x844` where practical.
- Check at least before/active/after states when the interaction has those states.
- Include locked/blocked state when applicable.
- Do not commit competitor screenshots or proprietary assets unless their license explicitly permits it; use links/notes and temporary research captures instead.

A visual feature with no screenshot/video evidence is incomplete.

## 3. Product rules

- BeBee must remain a cozy, readable, low-friction game.
- The primary loop is `pollinate -> honey -> upgrade -> unlock -> customize -> restore`.
- The world must become visibly more alive as the player progresses.
- Do not add combat to solve a content problem.
- Do not add currencies without a written economic reason.
- Do not add a hard energy/wait timer to MVP.
- Do not create feature systems for hypothetical future content before the current milestone needs them.
- Every new feature must answer: what player problem does this solve, and how is success measured?

## 4. Technical rules

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

## 5. Implementation order

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

Each item still follows the mandatory research-first workflow before implementation.

## 6. Definition of done for gameplay work

A gameplay task is not done when the code compiles. It is done when:

- acceptance criteria are met;
- competitor/reference research is recorded when applicable;
- relevant official technical documentation has been consulted;
- keyboard and touch paths both work where relevant;
- save/load behavior is covered;
- player-facing states have feedback (visual and, when appropriate, audio/haptic);
- no new warnings/errors are introduced;
- deterministic logic has tests where practical;
- the task includes a short manual QA recipe;
- analytics events are added for economy/progression changes when required by `docs/07-qa-analytics-release.md`;
- player-facing changes include rendered screenshot/video evidence;
- a post-implementation reference comparison has been performed;
- any visible gap marked `ITERATE` in the comparison has been addressed before merge.

## 7. UX guardrails

- Keep the playfield unobstructed. Persistent HUD must be sparse.
- Never require the player to open a menu to understand the immediate next objective.
- Important interactions require one primary action, not a chain of confirmations.
- Do not steal the camera for mission guidance. Use world markers/edge arrows instead.
- Avoid tiny text and tiny tap targets. Touch target baseline: 44 logical px minimum.
- Avoid modal popups during active movement except pause/settings or explicit player actions.
- Currency changes and unlocks need immediate, legible feedback.

## 8. Art/content guardrails

- Competitor games are references for patterns, not assets to copy.
- Do not copy Cow Bay/7Spot art, maps, characters, text, sounds, layouts pixel-for-pixel or proprietary code.
- Imported third-party assets require a compatible license and attribution record in `THIRD_PARTY.md`.
- Prefer original bee/flower/world assets or explicitly licensed packs.
- All flower silhouettes must remain distinguishable at gameplay zoom.
- A competitor comparison should ask whether BeBee solves the same player problem at comparable quality, not whether the screen is visually identical.

## 9. Git workflow

- `main` is releasable documentation/code.
- Feature work uses focused branches such as `feat/pollination-loop`.
- One concern per PR where practical.
- PR description includes: research references, official docs consulted, behavior change, test evidence, screenshots/video for visual work, comparison conclusion, save migration impact, and known limitations.
- Do not merge if HTML5 build is broken.
- Do not merge player-facing work with no rendered evidence.

## 10. Scope discipline

If a requested change does not improve the current milestone, add it to a backlog document/issue instead of implementing it immediately. The goal is a released game, not maximum code volume.
