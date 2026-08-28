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

### Layer C — Visual/manual QA

Humans verify what tests cannot reliably judge:

- movement feel;
- camera comfort;
- flower readability;
- reward satisfaction;
- before/after restoration impact;
- UI hierarchy;
- mobile thumb reach;
- audio balance;
- reduced-motion behavior.

### Layer D — Real-device/browser QA

At minimum before public beta:

- current Chrome desktop;
- current Firefox desktop;
- current Chromium-based Android browser;
- iOS Safari if iOS/web is a target;
- representative low/mid Android hardware;
- portrait and landscape phone checks where supported.

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

## 5. First-session usability test

Give the build to someone who has not read the documentation.

Do not explain controls unless they become truly stuck.

Observe:

- time to first movement;
- time to first pollination;
- whether they notice honey;
- whether they understand the hive;
- whether Buzz gate meaning is clear;
- whether they understand seed customization;
- whether they can state the long-term goal.

Record where the player pauses, circles aimlessly or opens menus looking for answers.

The correct fix is usually environmental/UI communication, not another paragraph of tutorial text.

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

Use telemetry + observed playtests + qualitative feedback together.

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

- thermal/performance behavior during sustained 15–30 minute play;
- virtual joystick responsiveness;
- browser UI/resizing/orientation behavior.

---

## 11. Performance gates

Targets are measured on representative devices and may be refined.

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
6. optionally artifact upload for playable PR build.

`main` must not accept a change that knowingly breaks the HTML5 build.

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

Do not ship with known S0. S1 requires explicit release decision and normally blocks public launch.

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

- onboarding validated with new players;
- all gates explain requirements;
- all major screens work at supported resolutions;
- no forced camera guidance causing disorientation.

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
- core loop is understandable and satisfying;
- saves are trustworthy;
- performance is stable;
- scope is coherent;
- telemetry can tell us where real players struggle next.
