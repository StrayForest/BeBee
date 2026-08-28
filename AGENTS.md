# AGENTS.md — BeBee implementation contract

This file defines how coding agents work in BeBee.

## 1. Always-read core

Before substantial work, read only these three first:

1. `README.md`
2. `AGENTS.md`
3. `DECISIONS.md`

Then read the task-specific documents below. Do not load every large document by default.

## 2. Documentation precedence

When two documents conflict:

1. `DECISIONS.md` wins;
2. `docs/11-blueprint-hardening.md` wins over older numbered design assumptions;
3. an approved task research/ADR wins for that scoped feature;
4. otherwise use the domain-owner document.

Do not silently choose between contradictions. Record the finding and update the source of truth.

## 3. Task reading matrix

| Task | Required domain docs |
|---|---|
| movement / pollination / core gameplay | `01-game-design.md`, `03-ux-ui-controls.md`, `05-technical-architecture.md`, relevant research |
| economy / upgrades / rewards / seeds | `02-progression-economy.md`, `01-game-design.md`, `14-economy-validation.md` when present |
| HUD / menu / onboarding / input presentation | `03-ux-ui-controls.md`, `09-art-direction.md`, `13-visual-qa-scorecard.md` |
| world / meadow / flower content | `04-world-content.md`, `09-art-direction.md` |
| save / browser / platform / SDK | `05-technical-architecture.md`, `07-qa-analytics-release.md`, `12-platform-storage.md` |
| art / VFX / audio | `09-art-direction.md`, `13-visual-qa-scorecard.md` |
| roadmap / milestone | `06-production-roadmap.md`, `11-blueprint-hardening.md` |
| research process | `10-development-workflow.md`, `15-agent-evidence-governance.md`, relevant `.agents/skills/.../SKILL.md` |

Read additional docs only when the task crosses domains.

## 4. Decision-state rule

`DECISIONS.md` uses:

- `LOCKED`
- `VALIDATED`
- `HYPOTHESIS`
- `OPEN`
- `DEPRECATED`

Rules:

- a `LOCKED` decision may be implemented and depended on;
- a `VALIDATED` decision may be tuned but not casually replaced;
- a `HYPOTHESIS` must be researched/prototyped before dependent complexity is built;
- an `OPEN` item is not permission for the agent to choose silently;
- changing a `LOCKED` decision requires evidence and an update to `DECISIONS.md` in the same PR.

Existing design text written before the research-first workflow does not automatically override this rule.

### Decision provenance

For every substantial new or changed decision, record why it exists using the provenance taxonomy in `docs/15-agent-evidence-governance.md`:

- `OWNER_CONSTRAINT`
- `REFERENCE_PATTERN`
- `TECH_CONSTRAINT`
- `EXPERIMENT_RESULT`
- `SIMULATION_RESULT`
- `TELEMETRY_RESULT`
- `PLAYTEST_RESULT`
- `SUBJECTIVE_DIRECTION`

Also record evidence strength (`LOW`, `MEDIUM`, `HIGH`). Do not present owner preference or subjective art direction as objective external evidence.

## 5. Mandatory research-first workflow

Do not begin a meaningful feature by writing production code.

Required order:

1. define the exact player/system problem;
2. check `DECISIONS.md` status;
3. inspect relevant shipped-game references when player-facing;
4. read current official Defold/platform/library documentation for technical behavior;
5. record the design/technical decision and acceptance criteria;
6. implement the smallest complete version;
7. build and run relevant tests/manual checks;
8. render the actual game;
9. capture screenshots/video for player-facing work;
10. compare the result against references and BeBee rules;
11. run a separate evaluation pass for substantial player-facing work;
12. iterate when evidence exposes a gap;
13. open/finalize PR with evidence;
14. merge only after gates pass.

Use `docs/templates/feature-research.md`, `docs/templates/evidence-manifest.example.json` and repository-local skills under `.agents/skills/`.

## 6. Research rules

- References are used for interaction/UX/quality patterns, not proprietary expression.
- Prefer problem-specific shipped references; do not use only one developer's games when broader references exist.
- For substantial player-facing work, build a candidate pool of at least five plausible shipped references when reasonably available, then inspect at least two deeply.
- Include a materially different solution or anti-pattern so research is not only confirming the preferred idea.
- Record why references were selected and why notable candidates were rejected or considered less relevant.
- Prefer official technical documentation over snippets, forum answers or model memory.
- Verify APIs and current portal requirements; never invent names or assume an old integration still applies.
- Record observed facts separately from inference.
- Prefer measurable observations before subjective ratings.
- Do not commit competitor screenshots/assets unless their license explicitly permits it.

## 7. Visual QA rules

Player-facing work is incomplete until the rendered result is inspected.

Follow `docs/13-visual-qa-scorecard.md` and `.agents/skills/visual-qa/SKILL.md`.

At minimum where applicable:

- capture before/active/after states;
- capture blocked/locked state;
- check desktop and affected mobile layout;
- use motion evidence for movement/camera/timing;
- compare interaction cost, hierarchy, state readability, feedback timing and playfield obstruction;
- mark `PASS`, `PASS WITH DEVIATION`, or `ITERATE`.

`ITERATE` means not merge-ready.

For substantial player-facing work, the implementation pass must not be the only evaluation authority. Run a separate evaluation pass using primarily the problem, acceptance criteria, selected reference observations, rendered evidence and measurements. Record its findings/verdict in the evidence manifest.

At the ends of P2, P4 and P6, require a complete milestone evidence package and separate evaluation pass. Human review is optional and must never be a prerequisite for CI, merge or phase progression unless the owner explicitly requests review for that specific change.

## 8. Product guardrails

- Core fantasy: cute bee restores a planet with flowers.
- Core economy currency: Honey.
- Seeds/customization are part of player ownership and must not punish campaign progression.
- No mandatory combat, hard energy timer, premium currency, multiplayer or backend account in the vertical slice.
- World gates default to restoration/progression/Buzz, not Honey payments.
- Do not add systems for hypothetical future content before the current validated milestone needs them.
- A feature must improve flying, pollinating, blooming, upgrading, choosing flowers or restoring the world.
- Do not add a feature merely because it would make the game feel richer; identify the player problem and evidence first.

## 9. Technical guardrails

- Engine: Defold; gameplay language: Lua.
- HTML5 first; touch compatibility must not be knowingly broken.
- Content/balance is data-driven.
- Stable authored IDs for persistent objects.
- Save format is versioned and migration-tested.
- GUI does not own economy/progression state.
- Platform SDKs live behind adapters.
- Storage lives behind an adapter; gameplay does not call portal/cloud APIs directly.
- If collection proxies are used, proxy/input focus routing is explicitly tested.
- Avoid giant manager scripts, premature frameworks and speculative ECS layers.
- Optimize from profiling, not from reference-project cargo culting.

## 10. Implementation order

Current repository status is **P-1 blueprint hardening**, not normal gameplay production.

Complete `docs/11-blueprint-hardening.md` exit criteria, including the objective-evidence hardening tasks in `docs/06-production-roadmap.md`, before treating P0/BB-001 onward as the normal production path.

After P-1, build vertically:

1. bootstrap/build/test infrastructure;
2. movement/camera;
3. validated pollination interaction;
4. one complete reward path;
5. one validated upgrade;
6. save/load;
7. one full meadow restoration;
8. validated seed/restoration flow;
9. touch/portal-specific shell;
10. only then scale content.

## 11. Definition of done

A meaningful task is done only when:

- required research exists or a justified exception is recorded;
- relevant official docs were consulted;
- the decision has explicit provenance/evidence strength when substantial;
- acceptance criteria pass;
- tests/data validation/build pass where relevant;
- save/migration impact is handled;
- no new runtime/console errors are introduced;
- player-facing states have rendered evidence;
- a substantial player-facing change has a separate evaluation record;
- comparison conclusion is not `ITERATE`;
- third-party provenance is clear;
- `DECISIONS.md` is updated if decision status changed.

For substantial player-facing/economy work, the evidence source of truth is `evidence/<ticket>/manifest.json`, changed in the same PR. PR prose summarizes it but does not replace it.

## 12. Git workflow

- `main` is intended to stay releasable.
- Use focused branches and PRs.
- One concern per PR where practical.
- PR must include research, official docs, decision status/provenance, verification evidence, visual evidence where relevant, save impact and known limitations.
- Do not merge knowingly broken HTML5 builds.
- `main` should be protected by a GitHub ruleset requiring PRs and required status checks; direct push is not the normal workflow.
- Required workflow gates must be fully autonomous. No reviewer, approval, second GitHub account or manual interaction is part of the normal merge path.
- Once CI/rulesets exist, do not bypass required checks except through an explicit emergency decision documented in the PR.

## 13. Local agent skills

Use these when relevant:

- `.agents/skills/competitor-research/SKILL.md`
- `.agents/skills/official-doc-research/SKILL.md`
- `.agents/skills/visual-qa/SKILL.md`
- `.agents/skills/economy-validation/SKILL.md`

They are execution checklists. `DECISIONS.md` and domain docs remain authoritative.
