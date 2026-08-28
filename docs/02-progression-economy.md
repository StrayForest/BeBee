# 02 — Progression & Economy

## 1. Authority

This document owns canonical economy values and progression math. Other docs should not duplicate exact costs/rewards.

Decision status lives in `DECISIONS.md`. `BB-P005` validates the **structural** first-region no-grind envelope and the Flight + Buzz upgrade set. Exact numeric reward/cost curves remain balancing hypotheses until production gameplay timing and playtests calibrate them.

## 2. Economy objective

Honey exists to create two understandable categories of choice:

1. improve the bee;
2. unlock/express flower choices.

The economy must not punish a player for making the planet prettier.

MVP uses one core currency: **Honey**.

## 3. Locked rules

- Honey cannot become negative.
- New campaign content should fund progression primarily through new campaign content.
- Replay/regrowth is optional top-up activity, not the intended funding source.
- Seed/customization spending must not create an unrecoverable campaign grind.
- Default world gates do not directly charge Honey in the vertical slice.
- No premium currency/energy/crafting-resource economy in the vertical slice.

## 4. Honey sources

Primary:

- first-time completion of meaningful flower/restoration work.

Possible milestone sources:

- meadow restoration;
- first discovery of a species;
- region completion.

Avoid login rewards/passive faucets until active gameplay is validated.

## 5. Honey sinks

Default sinks:

- **Flight** and **Buzz** upgrades;
- seed/species unlocks or other validated flower-expression unlocks.

Area/road Honey gates are removed from the default model after the blueprint audit.

Yield is not a vertical-slice sink after `BB-P005`.

## 6. Validated upgrade set

`D-007` validates an intentionally small vertical-slice set: **Flight + Buzz**. Validation applies to the role/topology of the tracks, not their final numeric curves.

### Flight — VALIDATED track, tuning open

Purpose:

- reduces travel friction;
- makes later/larger spaces more comfortable;
- gives a directly felt improvement.

Initial hypothesis curve:

| Level | Speed multiplier |
|---:|---:|
| 1 | 1.00x |
| 2 | 1.10x |
| 3 | 1.20x |
| 4 | 1.30x |
| 5 | 1.40x |
| 6 | 1.50x |
| 7 | 1.60x |
| 8 | 1.70x |

Final curve depends on P1 movement/camera validation and P3 direct feel testing.

### Buzz — VALIDATED track, tuning open

Purpose:

- increases pollination capability;
- provides readable aspiration/gates;
- makes formerly difficult flowers feel easier.

Initial hypothesis curve:

| Level | Power multiplier | Typical access idea |
|---:|---:|---|
| 1 | 1.00x | starter flowers |
| 2 | 1.35x | first medium tier |
| 3 | 1.70x | Lily-style gate |
| 4 | 2.10x | later region |
| 5 | 2.55x | later region |
| 6 | 3.05x | late game |

Exact species mapping belongs to content data after flower progression is validated.

### Yield — EXCLUDED from the vertical slice

Historical candidate: 40 Honey for a 1.15x Honey multiplier after M03.

`BB-P005` found:

- no-Yield comparison final balance: 382;
- earliest allowed Yield purchase: 393 (**+11**);
- mid purchase: 381 (**-1**);
- late purchase: 367 (**-15**);
- 1.15x mathematical break-even only at M06;
- 1.10x never repays inside Region 1;
- 1.20x moves toward a stronger economic opener.

Yield is therefore not shipped in the vertical slice. It is not required for no-grind progression and its tested role is primarily purchase-timing/payback optimization rather than a direct change to flying or pollination.

Do **not** replace it with another stat merely to preserve three upgrade cards. A third track must start from a concrete player problem and new evidence.

## 7. Upgrade cost scaffolding

Authored tables are the production source of truth. A formula may generate starting proposals:

```text
cost(level -> level+1) = round(base_cost * growth^(level-1))
```

Old starting proposals remain useful for simulation only:

| Track | Base cost | Growth |
|---|---:|---:|
| Flight | 30 | 1.85 |
| Buzz | 35 | 1.95 |

The historical Yield proposal (40 / 1.90 growth) is retained only in BB-P005 research evidence for regression comparison, not as production content.

Do not ship these values because they appear in the blueprint. P3 must tune the actual first-region table against production gameplay.

## 8. Flower difficulty/reward model

Flower tiers communicate increasing work/capability.

Initial proposal:

| Tier | Example families | Relative work | Relative Honey | Buzz behavior |
|---:|---|---:|---:|---|
| 1 | Daisy / Clover | low | low | available |
| 2 | Lavender / Tulip | medium | medium | soft/recommended gate |
| 3 | Lily / Sunflower | higher | higher | explicit gate candidate |
| 4+ | later-region species | increasing | increasing | later progression |

Exact values are data-owned and simulation-tested.

Difficulty must not become a 30-second idle bar. The validated core interaction determines acceptable work duration.

## 9. First-region economy — VALIDATED structure, HYPOTHESIS values

The first region should:

- fund the first meaningful Buzz improvement early;
- make Flight attractive when travel grows;
- let players use seeds without fearing a campaign lock;
- require no intentional replay grind on a normal route;
- leave purchase-order freedom.

`BB-P005` validates the current **staging shape** as an arithmetic safety envelope after removing Yield from the production set. The deterministic stress run covers every full priority ordering of the seven retained sinks (Buzz 2/3, Flight 2/3 and three seeds):

- **5040 / 5040** orders reach region completion;
- **0** replay actions;
- **0** negative-balance paths;
- after purchasing all seven retained sinks, **271 Honey** remains under the current candidate values.

This proves no-grind arithmetic safety for the candidate structure. It does **not** prove that 45/55/70/etc. Honey rewards feel correctly paced in seconds/minutes.

## 10. Seed economy

Locked principles:

- seeds are affordable enough to be used, not hoarded forever;
- aesthetic experimentation is encouraged;
- replanting an already unlocked species should default to free or very cheap unless testing proves a consumable model more enjoyable;
- native/campaign completion remains separate from current planted species;
- Hybrid player-shaped plots may participate before full meadow completion without gating campaign progress.

The exact seed grant/unlock/cost table remains tunable in P5 against the rendered Hybrid flow.

## 11. Replay/regrowth

Replay income is optional and may be omitted entirely from the vertical slice.

If included:

- first completion remains the dominant reward;
- replay reward is intentionally lower;
- campaign balance assumes the player does not need replay farming;
- no timer/idle system is added merely to support replay.

## 12. Economy simulation — retained regression gate

The economy model is executable/reproducible rather than an intuition-only spreadsheet.

Run:

```bash
python3 -m unittest discover -s tools/economy -p 'test_*.py' -v
python3 tools/economy/simulate.py
python3 tools/economy/upgrade_set_analysis.py
```

The historical simulator retains Yield cases only as a regression comparison for the BB-P005 decision. Production P3 scenarios should treat Flight + Buzz as the shipped upgrade set.

When production values move into game data, the simulator should consume those same definitions and continue covering at minimum:

- minimum required campaign actions;
- typical campaign path;
- upgrade-first spending;
- seed/customization-heavy spending;
- Flight-first;
- Buzz-first;
- poor-but-valid purchase ordering;
- replay disabled;
- all relevant purchase-priority stress cases.

For each path record:

- Honey earned;
- Honey spent;
- balance before each progression gate;
- time/actions between meaningful purchases;
- whether replay becomes required.

## 13. Economy acceptance criteria

Before P3 numeric values are locked:

- no simulated intended path goes negative;
- no normal seed-heavy path becomes unable to progress without excessive replay;
- no single upgrade track is an obvious universal first purchase across all meaningful states unless intentionally designed as tutorial progression;
- no shipped stat is consistently dominated/ignored;
- region completion does not depend on farming starter content repeatedly;
- meaningful upgrades remain affordable within a few minutes of appropriate-tier play rather than arbitrary waiting;
- Flight/Buzz effect sizes are noticeable enough to justify purchase without breaking level design.

The first three arithmetic safety requirements already pass for the BB-P005 structural candidate; the time/feel requirements remain P2/P3 runtime work.

## 14. Telemetry

Track at minimum:

- Honey earned by source;
- Honey spent by sink;
- balances at progression points;
- upgrade purchased/level;
- seed unlock/use;
- time since previous progression event;
- gate seen / session ended around a gate;
- replay dependence.

Interpret telemetry with observed playtests. High session length may mean engagement or confusion; high replay may mean fun or underfunded progression.

## 15. Monetization boundary

Do not balance core progression around paid acceleration or frustration relief.

If monetization is later required, it must be researched against the selected distribution platform after the core loop is validated. Cosmetics/convenience may be considered; campaign power must not be intentionally made miserable to sell a solution.
