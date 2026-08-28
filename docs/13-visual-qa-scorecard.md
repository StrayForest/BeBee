# 13 — Visual QA & Reference Comparison Scorecard

## 1. Purpose

A player-facing feature is not accepted because the code works or because an agent says it looks good. It must produce reproducible rendered evidence and be compared against the exact player problem researched before implementation.

Use objective measurements before subjective ratings. A subjective score without a concrete note is not evidence.

## 2. Evidence classes

Use the smallest evidence type that proves the behavior:

- screenshot — layout, hierarchy, readability, before/after world state;
- short video/GIF/frame sequence — movement, camera, timing, VFX, interaction start/stop;
- numeric capture — timing, action count, viewport obstruction, FPS/load metrics;
- real-device note — touch comfort, browser chrome/orientation, haptics/audio lifecycle.

## 3. Deterministic QA states

Once a runnable HTML5 build exists, create a development-only deterministic state loader. Suggested cases:

```text
movement_empty
movement_dense
pollination_idle
pollination_active_50
pollination_complete
flower_soft_gate
flower_hard_gate
hud_default
hive_affordable
hive_unaffordable
seed_locked
seed_unlocked
meadow_dormant
meadow_mid
meadow_restored
mobile_portrait_hud
```

Production builds must not expose unsafe debug controls.

## 4. Default capture matrix

Player-facing PRs capture only relevant rows, but omission must be deliberate.

| State | Desktop | Mobile portrait | Motion evidence |
|---|---:|---:|---:|
| Idle/default | yes | when affected | optional |
| Active interaction | yes | when affected | recommended |
| Completion/reward | yes | when affected | recommended |
| Locked/blocked | when applicable | when applicable | optional |
| Dense/worst case | for HUD/render changes | for HUD changes | optional |

Default comparison viewports until the primary portal overrides them:

- desktop development: `1440x900`;
- mobile portrait development: `390x844`;
- portal-specific resolutions are added after `BB-P006`.

## 5. Objective comparison metrics

Record applicable observable values before assigning 1–5 scores.

### Interaction cost

- actions/clicks/taps before primary result;
- time from reaching target to feedback start;
- time to completion at intended progression tier;
- stationary waiting time;
- number of confirmations/modals;
- number of simultaneous touch controls;
- whether the action can be cancelled/recovered immediately;
- whether control is blocked during reward animation.

### UI density

- persistent HUD element count;
- number of simultaneous attention animations;
- approximate screen area obscured by modal/panel;
- lines of instructional text shown at once;
- minimum touch target where applicable;
- number of visible simultaneous objectives.

### Readability

Record direct observations for:

- primary objective discoverability;
- player-character readability;
- interactive-vs-decoration distinction;
- locked-vs-available distinction;
- reward/currency attribution;
- next-action clarity.

### Feedback

Record direct observations for:

- latency/immediacy;
- cause/effect connection;
- completion reaction;
- world-state change strength;
- audio/motion redundancy without clutter.

## 6. Anchored subjective scoring

Subjective scores are allowed only after objective observations and require a note.

Use these anchors consistently:

### 1 — Fails the target problem

- frequent confusion or unreadability;
- core state/action is hard to identify;
- major obstruction/friction;
- clearly below the selected references for the target problem.

### 2 — Material weakness

- usable only with noticeable friction or explanation;
- multiple visible deficiencies remain;
- reference-quality gap is obvious.

### 3 — Acceptable baseline

- target problem is solved;
- some non-blocking weakness remains;
- comparable to an ordinary competent implementation, but not clearly strong.

### 4 — Strong

- target problem is solved clearly and with low friction;
- no meaningful weakness is visible in the tested states;
- at or above the selected references on the important dimensions, or intentionally different with evidence.

### 5 — Exceptional for this scope

- unusually clear/satisfying without added complexity;
- evidence shows a meaningful advantage over relevant references;
- use rarely; a 5 requires an explicit reason beyond "looks polished".

A score is not averaged into automatic acceptance. A single severe target-problem failure can still require `ITERATE`.

## 7. Scorecard

Use this table in feature research/PR evidence:

| Criterion | Reference A | Reference B | BeBee | Target / finding |
|---|---:|---:|---:|---|
| Actions to result | | | | |
| Feedback begins within | | | | |
| Stationary wait | | | | |
| Persistent HUD items | | | | |
| Instruction lines | | | | |
| Objective clarity (1–5 + note) | | | | |
| State readability (1–5 + note) | | | | |
| Feedback quality (1–5 + note) | | | | |
| Mobile comfort (1–5 + note) | | | | |
| World transformation (1–5 + note) | | | | |
| Original BeBee expression (1–5 + note) | n/a | n/a | | |

Not every row applies to every feature. Do not invent measurements that cannot be observed. Mark them N/A with a reason where the omission could otherwise be ambiguous.

## 8. Separate evaluation pass

For substantial player-facing work, the implementation authoring pass is not the final quality authority.

Run a separate evaluation after screenshots/video/measurements exist. The evaluator should begin primarily from:

- the original player problem;
- acceptance criteria;
- selected reference observations;
- BeBee rendered evidence;
- objective measurements;
- relevant BeBee product rules.

Where practical, do not front-load the implementer's persuasive rationale. First ask the evaluator to identify gaps from the evidence.

Record:

- findings and severity;
- which acceptance criterion/reference dimension is affected;
- `PASS`, `PASS WITH DEVIATION`, or `ITERATE`;
- required iteration.

The evidence manifest is authoritative for substantial player-facing work.

## 9. Comparison outcomes

- `PASS` — acceptance criteria met and no meaningful reference-quality gap for the stated problem.
- `PASS WITH DEVIATION` — intentionally different; evidence shows the deviation better fits BeBee.
- `ITERATE` — meaningful gap remains; task is not merge-ready.

The comparison is not a license to copy pixel layout. BeBee can score better through a different composition.

## 10. Human approval gates

At the end of P2, P4 and P6, the agent cannot close the milestone solely by self-scoring. It must provide:

- runnable build/artifact;
- representative captures/video;
- completed scorecards;
- known deviations;
- automated/manual test evidence;
- separate evaluation findings.

A designated human approves the subjective product bar before mass content or the next major phase.

## 11. Visual regression automation

After stable QA states exist, add screenshot regression for deterministic surfaces where useful.

Use it for accidental regressions, not artistic stagnation. Golden images must be intentionally updated when approved design changes.

Recommended automated coverage:

- HUD default;
- locked flower state;
- Hive screen;
- seed selector;
- dormant/restored meadow framing;
- representative mobile layout.

Large intentional world-art variations may require thresholded or manual review rather than brittle pixel equality.
