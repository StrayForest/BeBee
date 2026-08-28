# 13 — Visual QA & Reference Comparison Scorecard

## 1. Purpose

A player-facing feature is not accepted because the code works or because an agent says it looks good. It must produce reproducible rendered evidence and be compared against the exact player problem researched before implementation.

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

For each researched reference and BeBee, record values where observable.

### Interaction cost

- actions/clicks/taps before primary result;
- time from reaching target to feedback start;
- time to completion at intended progression tier;
- number of confirmations/modals;
- whether control is blocked during reward animation.

### UI density

- persistent HUD element count;
- number of simultaneous attention animations;
- approximate screen area obscured by modal/panel;
- lines of instructional text shown at once;
- minimum touch-target compliance.

### Readability

Score 1–5 with a note:

- primary objective discoverability;
- player-character readability;
- interactive-vs-decoration distinction;
- locked-vs-available distinction;
- reward/currency attribution;
- next-action clarity.

### Feedback

Score 1–5 with a note:

- immediacy;
- cause/effect connection;
- completion satisfaction;
- world-state change strength;
- audio/motion redundancy without clutter.

## 6. Scorecard

Use this table in feature research/PR evidence:

| Criterion | Reference A | Reference B | BeBee | Target / finding |
|---|---:|---:|---:|---|
| Actions to result | | | | |
| Feedback begins within | | | | |
| Persistent HUD items | | | | |
| Objective clarity (1–5) | | | | |
| State readability (1–5) | | | | |
| Feedback quality (1–5) | | | | |
| Mobile comfort (1–5) | | | | |
| World transformation (1–5) | | | | |
| Original BeBee expression (1–5) | n/a | n/a | | |

Not every row applies to every feature. Do not invent measurements that cannot be observed.

## 7. Comparison outcomes

- `PASS` — acceptance criteria met and no meaningful reference-quality gap for the stated problem.
- `PASS WITH DEVIATION` — intentionally different; evidence shows the deviation better fits BeBee.
- `ITERATE` — meaningful gap remains; task is not merge-ready.

The comparison is not a license to copy pixel layout. BeBee can score better through a different composition.

## 8. Human approval gates

At the end of P2, P4 and P6, the agent cannot close the milestone solely by self-scoring. It must provide:

- runnable build/artifact;
- representative captures/video;
- completed scorecards;
- known deviations;
- automated/manual test evidence.

A designated human approves the subjective product bar before mass content or the next major phase.

## 9. Visual regression automation

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
