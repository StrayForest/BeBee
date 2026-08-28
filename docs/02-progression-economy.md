# 02 — Progression & Economy

## 1. Authority

This document owns canonical economy values and progression math. Other docs should not duplicate exact costs/rewards.

Decision status lives in `DECISIONS.md`. Until `BB-P005` passes, all numeric curves below are balancing hypotheses.

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

- validated bee upgrades;
- seed/species unlocks or other validated flower-expression unlocks.

Area/road Honey gates are removed from the default model after the blueprint audit.

## 6. Upgrade candidates

### Flight — strong candidate

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

Final curve depends on P1 movement/camera validation.

### Buzz — strong candidate

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

### Yield — HYPOTHESIS

Effect: multiplies Honey reward.

Risk:

A pure income multiplier can become either mathematically mandatory or obviously inferior. It must pass `BB-P005` economy simulation before shipping.

If retained, measure payback for every purchase point:

```text
payback_future_base_honey = upgrade_cost / (new_multiplier - old_multiplier)
```

A Yield level fails design review if:

- rational players are nearly always required to buy it early;
- it almost never repays before relevant campaign completion;
- it exists only to fill a third upgrade card.

Possible alternatives are researched only if Yield fails. Do not automatically add another stat.

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
| Yield (if retained) | 40 | 1.90 |

Do not ship these because they were written first. `BB-P005` must produce the actual first-region table.

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

## 9. First-region economy target

The first region should:

- fund the first meaningful Buzz improvement early;
- make Flight attractive when travel grows;
- let players use seeds without fearing a campaign lock;
- require no intentional replay grind on a normal route;
- leave some purchase-order freedom.

The old hand-authored first-region reward/cost table is no longer considered production balance. It becomes an input to `BB-P005`, not a conclusion.

## 10. Seed economy

Locked principles:

- seeds are affordable enough to be used, not hoarded forever;
- aesthetic experimentation is encouraged;
- replanting an already unlocked species should default to free or very cheap unless testing proves a consumable model more enjoyable;
- native/campaign completion remains separate from current planted species.

The exact first seed grant/unlock is not duplicated here until `BB-P004` selects the restoration flow.

## 11. Replay/regrowth

Replay income is optional and may be omitted entirely from the vertical slice.

If included:

- first completion remains the dominant reward;
- replay reward is intentionally lower;
- campaign balance assumes the player does not need replay farming;
- no timer/idle system is added merely to support replay.

## 12. Economy simulation — mandatory before production values

`BB-P005` must be executable/reproducible rather than an intuition-only spreadsheet.

Simulate at minimum:

- minimum required campaign actions;
- typical campaign path;
- upgrade-first spending;
- seed/customization-heavy spending;
- Flight-first;
- Buzz-first;
- every plausible Yield purchase timing if Yield remains;
- poor-but-valid purchase ordering;
- replay disabled;
- replay used as optional top-up.

For each path record:

- Honey earned;
- Honey spent;
- balance before each progression gate;
- time/actions between meaningful purchases;
- whether replay becomes required;
- Yield payback point if applicable.

## 13. Economy acceptance criteria

Before P3 values are locked:

- no simulated intended path goes negative;
- no normal seed-heavy path becomes unable to progress without excessive replay;
- no single upgrade track is an obvious universal first purchase across all meaningful states unless intentionally designed as tutorial progression;
- no shipped stat is consistently dominated/ignored;
- region completion does not depend on farming starter content repeatedly;
- meaningful upgrades remain affordable within a few minutes of appropriate-tier play rather than arbitrary waiting.

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
