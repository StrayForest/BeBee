# 11 — Blueprint Hardening

This document records the audit corrections that must be completed before normal gameplay production begins.

## 1. Why P-1 exists

The first blueprint established a coherent direction, but some product choices were written as decisions before the repository adopted the research-first workflow. They are therefore not automatically validated.

`P-1` converts assumptions into evidence-backed decisions before `BB-001` begins normal production.

## 2. Product corrections from the audit

### 2.1 Pollination is not locked yet

Current working hypothesis: entering/remaining near a patch automatically pollinates it.

Before locking it, prototype and compare at least:

- A — proximity auto-pollination;
- B — hold-to-pollinate while near a patch;
- C — movement-through/sweep pollination where coverage depends on flying through the flower area.

Evaluate repeatability, mobile comfort, control ownership, feedback timing and whether 100 repetitions would remain pleasant.

### 2.2 Seeds belong inside restoration

The previous spec pushed seed choice mostly after a meadow was already restored. That weakens the original fantasy.

The target rule is now:

> The player should be able to influence what the recovering world becomes during the restoration journey, while campaign progression remains safe and understandable.

Prototype at least these flows:

1. native completion first, customization second;
2. player may plant owned seeds during restoration;
3. hybrid: some native objectives establish biome identity while optional/player-owned plots are shaped during restoration.

Choose based on comprehension, agency and economy—not implementation convenience.

### 2.3 Honey gates are removed from the default MVP progression model

Honey is for:

- improving the bee;
- unlocking flower/seed expression where applicable.

Campaign/world gates default to:

- restoration completion;
- Buzz/progression requirements;
- authored objective completion.

This prevents a player from being punished for spending Honey on customization.

### 2.4 Yield is a hypothesis, not a guaranteed upgrade track

Flight and Buzz have direct experiential effects. Yield changes economy output and can become either mathematically mandatory or unattractive.

Before Yield ships:

- simulate payback time by purchase point;
- compare player-facing alternatives;
- verify that it creates an interesting choice rather than an obvious spreadsheet answer.

Potential replacements to test if Yield fails:

- `Pollen Reach` — slightly more forgiving pollination radius;
- `Bloom Flow` — faster transition between nearby patches / short chaining bonus;
- `Nectar Sense` — guidance/visibility quality improvement only if it materially improves play.

Do not add a replacement stat merely to preserve three cards.

## 3. Source-of-truth ownership

To avoid repeated contradictory values:

| Concern | Owner |
|---|---|
| Product pillars and scope | `00-product-vision.md` + `DECISIONS.md` |
| Core interaction rules | `01-game-design.md` |
| Costs/rewards/stat curves | `02-progression-economy.md` |
| HUD/screens/input presentation | `03-ux-ui-controls.md` |
| Region/meadow/flower roster | `04-world-content.md` |
| Technical contracts | `05-technical-architecture.md` |
| Execution order | `06-production-roadmap.md` |
| Test/release criteria | `07-qa-analytics-release.md` |
| Evidence/provenance governance | `15-agent-evidence-governance.md` |
| Global decisions/status | `DECISIONS.md` |

Do not duplicate canonical numeric values in multiple documents. Other documents should link to the owner.

## 4. P-1 mandatory work

### BB-P001 — Documentation consistency

- create/maintain `DECISIONS.md`;
- resolve duplicated region/seed/economy contradictions;
- tag assumptions as `HYPOTHESIS`;
- define document ownership.

### BB-P002 — Retroactive competitor benchmark

For the current proposed core:

- capture/research first-session flow;
- movement/control model;
- HUD hierarchy;
- resource/pollination equivalent feedback;
- upgrade interaction;
- locked-node communication;
- world expansion;
- customization/garden expression.

Use problem-specific references, not only games from one developer.

Output: structured benchmark notes with links, observations and measurable comparisons.

### BB-P003 — Pollination interaction prototypes

Build three intentionally disposable micro-prototypes and compare them before implementing the permanent FlowerPatch system.

Exit: one interaction becomes `VALIDATED` in `DECISIONS.md`.

### BB-P004 — Seed/restoration flow prototype

Test the three restoration/customization models described above.

Exit: player can explain what native flowers mean, what seeds do and whether a seed choice can hurt progression.

### BB-P005 — Economy simulation

Create a deterministic simulation/spreadsheet/script covering:

- first-region honey faucets;
- every upgrade purchase order;
- seed purchases;
- minimum and typical balances before gates;
- Yield payback if retained;
- no-grind constraints.

No campaign progression may depend on farming restored early patches in the intended path.

### BB-P006 — Primary web distribution decision

Compare direct web, Poki and CrazyGames at minimum for:

- first-session entry requirements;
- aspect ratios/device support;
- initial/total download budgets;
- storage/account expectations;
- SDK events;
- ads/monetization constraints;
- external request restrictions;
- analytics/privacy implications.

Select a primary target and keep the others behind platform adapters.

### BB-P007 — Visual style bible

Turn qualitative art direction into reproducible constraints:

- gameplay reference viewport;
- bee screen-size target;
- camera/zoom range;
- PPU/native art resolution decision;
- texture filtering;
- outline/shadow rule;
- spacing/radius scale for UI;
- approved palette families;
- animation timing ranges;
- VFX density limits;
- approved BeBee reference frames.

### BB-P008 — Deterministic visual QA design

Specify the implementation needed for an agent to capture reproducible player-facing states.

Target dev routes/state injection such as:

```text
?qa=movement
?qa=pollination_idle
?qa=pollination_active
?qa=flower_locked
?qa=meadow_before
?qa=meadow_after
?qa=hive
```

Once a runnable build exists, automated tooling should:

1. build HTML5;
2. serve locally;
3. launch deterministic state;
4. capture desktop/mobile viewports;
5. retain artifacts in CI;
6. fail when a required player-facing evidence artifact is missing where enforceable.

### BB-P009 — HTML5 storage specification

The storage layer must account for current Defold HTML5 behavior:

- `sys.get_save_file()` maps HTML5 save paths into the browser virtual filesystem backed by IndexedDB;
- persistence may lag slightly after a write;
- `sys.save()` output must remain under its documented size ceiling;
- corrupt `sys.load()` paths must be recoverable through protected calls and validation.

Test matrix must include:

- normal save/reload;
- save then immediate refresh;
- save then immediate tab close/reopen where automation permits;
- corrupt primary/valid backup;
- storage unavailable/failure path;
- incognito/private mode on the selected distribution target;
- old-version migrations.

### BB-P010 — Agent context/decision model

Agent always reads:

1. `README.md`;
2. `AGENTS.md`;
3. `DECISIONS.md`.

Then it reads only the task-specific documents defined in `AGENTS.md` unless the feature crosses domains.

### BB-P011 — Reusable agent skills

Create repository-local skill checklists for:

- competitor research;
- Defold official-doc research;
- visual QA;
- economy validation.

These are checklists/workflows, not permission to bypass the main docs.

### BB-P012 — Quality-gate enforcement plan

Once CI exists:

- required HTML5 build status;
- test status;
- PR-body validation for meaningful changes;
- evidence/artifact checks where automatable;
- protected `main`/ruleset;
- human approval gates for subjective product milestones.

### BB-P013 — Machine-readable evidence schema

Create and enforce `evidence/<ticket>/manifest.json` for substantial player-facing/economy changes.

The schema must cover:

- player/system problem;
- decision IDs/status/provenance/evidence strength;
- reference candidate pool and selected references;
- direct observation vs inference;
- anti-pattern/materially different solution;
- alternatives and selection/rejection reasons;
- official documentation;
- acceptance criteria and verification;
- visual artifacts/measurements where applicable;
- separate evaluation verdict.

### BB-P014 — Research selection protocol

Prevent cherry-picking by requiring, when reasonably available:

- at least five plausible candidate references;
- at least two deeply observed problem-specific references;
- one materially different solution or anti-pattern;
- reasons for selection/rejection;
- explicit exception when the candidate pool is genuinely smaller.

### BB-P015 — Decision provenance model

Every substantial decision records both:

- decision status (`LOCKED`, `VALIDATED`, etc.);
- provenance (`OWNER_CONSTRAINT`, `REFERENCE_PATTERN`, `TECH_CONSTRAINT`, `EXPERIMENT_RESULT`, `SIMULATION_RESULT`, `TELEMETRY_RESULT`, `PLAYTEST_RESULT`, `SUBJECTIVE_DIRECTION`).

Also record evidence strength (`LOW`, `MEDIUM`, `HIGH`).

### BB-P016 — Independent evaluator protocol

Substantial player-facing implementation is followed by a separate evaluation pass using primarily the original problem, acceptance criteria, reference observations, rendered evidence and measurements.

The evaluator records findings and `PASS` / `PASS WITH DEVIATION` / `ITERATE`.

`ITERATE` blocks merge. P2/P4/P6 still require designated human approval.

### BB-P017 — Hard merge gates

Strengthen CI so a convincing PR body alone is insufficient:

- parse/validate the evidence manifest;
- require the manifest to be changed in the same feature/economy PR;
- validate URL syntax and required counts/exceptions;
- validate one selected alternative;
- reject empty verification/acceptance evidence;
- reject `ITERATE`;
- require visual evidence declaration for player-facing changes.

Configure a GitHub ruleset for `main` requiring pull requests and required status checks once repository settings are available.

## 5. P-1 exit criteria

Do not start normal production milestone P0 until:

- contradictions identified by the audit are resolved or explicitly marked HYPOTHESIS;
- pollination interaction has a validation decision;
- seed/restoration flow has a validation decision;
- economy model demonstrates a no-grind first-region path;
- primary distribution target is selected;
- visual style/QA approach is defined;
- storage abstraction and HTML5 save risks are specified;
- agent reading/decision rules are in place;
- decision provenance/evidence strength rules are in place;
- machine-readable evidence is required for substantial player-facing/economy work;
- research selection/anti-confirmation rules are in place;
- separate player-facing evaluation is part of definition of done;
- PR evidence CI performs semantic structural checks beyond heading presence;
- `main` protection/ruleset is configured, or an explicit repository-settings blocker is recorded before autonomous production begins.

P-1 may use disposable prototypes and research scripts. It is intentionally allowed to discover that an earlier idea was wrong.

## 6. Human review points

Autonomous implementation is encouraged, but subjective gates require human review before scaling:

- end of P2 — core pollination loop;
- end of P4 — first full restoration transformation;
- end of P6 — shippable vertical slice.

The agent supplies evidence and its comparison scorecard; the human approves whether the experiential bar is actually met.
