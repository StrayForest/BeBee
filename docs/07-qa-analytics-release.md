# 07 — QA, Analytics & Release Quality

## 1. Quality objective

BeBee must be easy to understand, difficult to break and safe to return to after closing the browser/app.

For this project, the most serious defects are:

1. save/progression loss;
2. progression blockers/softlocks;
3. broken controls/input;
4. unclear next action;
5. severe frame pacing/loading problems;
6. economy states that force unintended grind.

Visual polish issues matter, but they rank below these.

All required QA/release gates must be executable by agents and automation. Human playtests/reviews may add evidence later, but their absence never blocks CI, merge, milestone completion or release readiness under the default process.

---

## 2. Test layers

### Layer A — Pure logic tests

Run without a full gameplay scene where possible.

Cover:

- upgrade cost tables;
- honey reward calculation;
- affordability and spending;
- no-negative-balance invariant;
- flower gate rules;
- meadow completion rules;
- region completion rules;
- planet percentage;
- seed unlock state;
- native vs planted flower separation;
- save migrations;
- duplicate/invalid data references.

### Layer B — Integration/smoke checks

Run a real build or scripted scene path for critical behavior:

- boot;
- new game;
- movement;
- patch trigger;
- pollination complete;
- honey HUD update;
- upgrade purchase;
- save;
- reload;
- seed replant;
- meadow restoration;
- region unlock.

### Layer C — Rendered/experiential QA

Agents evaluate what pure logic tests cannot reliably judge by using deterministic captures, motion evidence, objective measurements, reference comparison and a separate evaluation pass:

- movement feel proxies such as responsiveness, acceleration and recovery time;
- camera comfort proxies such as framing, motion and obstruction;
- flower readability;
- reward feedback strength/timing;
- before/after restoration impact;
- UI hierarchy;
- mobile control reach/target geometry;
- audio-level/trigger consistency where measurable;
- reduced-motion behavior.

Any subjective conclusion must be tied to inspected rendered evidence and anchored criteria. Optional human feedback may be recorded as `PLAYTEST_RESULT`, but is not required.

### Layer D — Real-browser/device QA

Before public beta, automate or agent-execute representative coverage where infrastructure permits:

- current Chrome desktop;
- current Firefox desktop;
- current Chromium-based Android browser/emulation;
- iOS Safari/WebKit automation when iOS/web is a target;
- representative low/mid hardware or calibrated performance profiles;
- portrait and landscape phone checks where supported.

If a target cannot be exercised in available automation, record the coverage limitation and use the nearest reproducible environment. Do not replace the missing environment with an invented pass.

---

## 3. Core invariants

These should become automated assertions/validation where practical.

### Economy

```text
honey >= 0
upgrade_level >= 1
spent_honey <= available_honey at transaction start
reward >= 0
```

### Progression

```text
restored meadow => all required native objectives completed
planted cosmetic species does not erase native completion
unlocked region never becomes locked after save/reload
planet progress never decreases because of customization
```

### Save

```text
save_version always present
stable persistent IDs unique
unknown optional fields tolerated where safe
corrupt primary must not overwrite valid backup
migration is sequential and repeatable
```

### Patch

```text
completion event fires once per campaign-native completion
pollination progress cannot exceed configured max after clamp
leaving radius pauses; does not reset
hard-gated patch cannot complete below requirement
```

---

## 4. Save test matrix

Every public build should test:

1. new save -> progress -> reload;
2. save during early meadow;
3. save immediately after patch completion;
4. save immediately after upgrade purchase;
5. save after seed planting;
6. save after meadow restoration;
7. save after region unlock;
8. migrate previous public save version;
9. corrupted primary + valid backup;
10. missing optional setting fields;
11. duplicate launch/reload does not duplicate rewards.

A save-loss bug blocks release.

---

## 5. First-session comprehension test

Use a deterministic clean-save scenario with no hidden debug assistance and evaluate the first-session path from observable game state/captures/telemetry hooks.

Measure:

- time/actions to first movement;
- time/actions to first pollination;
- whether Honey is visibly attributable to the action;
- whether Hive affordance/current-next upgrade effect is discoverable;
- whether Buzz gate requirement is explicit;
- whether seed customization is distinguishable from campaign completion;
- whether the long-term restoration goal is visible from game presentation.

Record states where the agent/evaluator cannot infer a unique next action, where pathing loops without progress, or where menus are required only to discover basic intent.

The preferred fix is environmental/UI communication, not another paragraph of tutorial text.

Optional later playtests with real players may strengthen evidence but are not a prerequisite for autonomous development or release gating.

---

## 6. Analytics event taxonomy

Analytics is an observation layer, never a gameplay dependency.

### Session

- `session_start`
- `session_end` where reliably available
- `new_game_started`
- `save_loaded`

### Tutorial/funnel

- `tutorial_step_started`
- `tutorial_step_completed`
- `first_patch_completed`
- `first_upgrade_purchased`
- `first_meadow_restored`
- `first_seed_planted`
- `planet_map_revealed`

### Pollination

- `patch_pollination_started`
- `patch_completed`
- `patch_gate_seen`

Suggested fields:

```text
patch_id
flower_id
meadow_id
region_id
buzz_level
seconds_active
reward
```

### Economy

- `honey_earned`
- `honey_spent`
- `upgrade_purchased`
- `seed_unlocked`

Fields:

```text
amount
source_or_sink
balance_after
upgrade_or_seed_id
level_after
```

### Progression

- `meadow_restored`
- `region_unlocked`
- `region_completed`
- `planet_progress_changed`

### Customization

- `seed_selector_opened`
- `seed_planted`
- `patch_replanted`

### UX/system

- `settings_changed`
- `reduced_motion_enabled`
- `save_recovery_used`
- `content_validation_error` development builds only

---

## 7. Privacy rules for analytics

Do not send:

- player names unless a future account feature genuinely requires them;
- email addresses;
- precise location;
- device identifiers beyond what the selected provider/platform legitimately needs;
- raw free-text input;
- secrets/auth tokens.

Use random installation/session identifiers only when justified and handled under the target privacy policy.

Document the chosen provider and payloads before public release.

---

## 8. Product metrics

### First-session funnel

Track conversion through:

```text
start
 -> first pollination
 -> first honey
 -> first upgrade
 -> first meadow restored
 -> first seed planted
 -> planet reveal
```

A sharp drop identifies comprehension/friction problems.

### Economy health

Monitor:

- median honey balance by meadow;
- time between affordable and purchased upgrades;
- upgrade track selection share;
- percentage of honey spent on seeds;
- old-meadow replay dependence;
- time spent blocked by Buzz gates.

### Customization health

Monitor:

- % players planting at least one non-native flower;
- average number of replants per restored meadow;
- seed unlock popularity;
- whether one species dominates due to unintended numerical advantage.

### Progression health

Monitor:

- completion rate by meadow/region;
- median time per meadow;
- sessions between region unlocks;
- abandon rate shortly after a gate is shown.

---

## 9. Metric interpretation rules

Do not optimize a metric in isolation.

Examples:

- longer session length can mean engagement or confusion;
- high replay count can mean satisfying play or underfunded economy;
- high upgrade purchase conversion can mean good clarity or forced choice;
- low seed spending can mean customization is undiscoverable, unattractive or too expensive.

Before live telemetry exists, combine deterministic simulation, rendered evidence and separate evaluation. After players exist, telemetry and optional playtest feedback may strengthen or overturn earlier conclusions.

---

## 10. Performance QA

Measure these scenarios separately:

### Cold start

- time until interactive title;
- time until first playable meadow;
- asset/download size.

### Dense meadow

Worst representative state:

- all patches restored;
- maximum normal flower density;
- ambient insects active;
- multiple VFX events;
- HUD animations.

### Transition

- region load/unload;
- no multi-second frozen frame;
- no memory/entity leak after repeated transitions.

### Save

- save operation must not create noticeable gameplay hitch.

### Mobile

- thermal/performance behavior during sustained 15–30 minute run where measurable;
- virtual joystick responsiveness;
- browser UI/resizing/orientation behavior.

---

## 11. Performance gates

Targets are measured on representative devices/environments and may be refined.

- 60 FPS target on normal supported devices;
- stable 30 FPS is preferable to unstable 40–60 on low-end devices;
- no repeated frame spikes during normal pollination;
- no progressive memory growth from revisiting meadows;
- no long main-thread stall on autosave;
- no critical UI layout overlap at supported aspect ratios.

Any regression should include a before/after profile if the cause is nontrivial.

---

## 12. CI quality gates

Every PR should eventually run:

1. data validation;
2. Lua unit tests;
3. save migration tests;
4. HTML5 build;
5. static checks/lint/format check once tooling is selected;
6. artifact upload for playable/evidence builds where relevant;
7. deterministic capture/evaluation checks for substantial player-facing work.

`main` must not accept a change that knowingly breaks the HTML5 build.

No CI quality gate may depend on a human approval or manual reviewer action.

---

## 13. Content validation

Create a validator that checks:

- unique IDs;
- referenced flower IDs exist;
- meadow references valid patch IDs;
- region references valid meadow IDs;
- numeric rewards/costs non-negative;
- hard gate references valid Buzz level;
- seed references valid flower definition;
- localized keys exist for required player-facing names;
- no duplicate stable save identifiers.

Prefer build-time failure to a broken late-game meadow.

---

## 14. Bug severity

### S0 — Release blocker

- data loss;
- game cannot boot;
- progression cannot be completed;
- purchase/economy corruption;
- widespread crash.

### S1 — High

- broken controls on a target platform;
- severe performance regression;
- incorrect gate preventing intended progress;
- major UI unusable on common resolution.

### S2 — Medium

- visible state mismatch fixed by reload;
- minor objective guidance error;
- noticeable but nonblocking animation/audio defect.

### S3 — Low

- cosmetic overlap;
- tiny polish discrepancy;
- noncritical text issue.

Do not ship with known S0. S1 requires an explicit recorded release decision and normally blocks public launch.

---

## 15. Regression checklist per gameplay PR

- New game still works.
- Existing save still loads or migration exists.
- Honey cannot become negative.
- Patch completion cannot double-reward.
- Hive can open/close.
- Keyboard movement still works.
- Touch movement still works where relevant.
- Pause/settings do not leak input to gameplay.
- Current meadow can still complete.
- HTML5 build starts.

Add task-specific checks rather than relying only on this list.

---

## 16. Release candidate checklist

### Gameplay

- all required regions completable;
- final 100% restoration reachable;
- no required objective relies on debug commands;
- economy does not require unintended repetitive farming.

### Save

- fresh save;
- old supported save migration;
- backup recovery;
- reset flow;
- relaunch persistence.

### UX

- onboarding passes deterministic first-session comprehension gates;
- all gates explain requirements;
- all major screens work at supported resolutions;
- no forced camera guidance causing disorientation;
- optional real-player feedback, if available, has no unresolved blocker.

### Performance

- startup measured;
- dense meadow measured;
- long session measured;
- repeated region transitions measured.

### Legal/platform

- third-party licenses inventoried;
- privacy policy matches analytics/platform behavior;
- distribution SDK configuration validated;
- no repository secrets shipped;
- store/portal screenshots and descriptions correspond to current game.

### Observability

- production analytics receives expected events;
- analytics failure does not break gameplay;
- build/version identifier visible in diagnostic context.

---

## 17. Launch principle

Launch quality is not “zero bugs.” It is:

- no known catastrophic failure;
- core loop is understandable and satisfying by the defined evidence gates;
- saves are trustworthy;
- performance is stable;
- scope is coherent;
- telemetry can tell us where real players struggle next.
