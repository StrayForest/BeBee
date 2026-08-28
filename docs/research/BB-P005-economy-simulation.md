# BB-P005 — First-region economy simulation

Status: **simulation candidate only**. This does not lock production values and does not change `D-007` from `HYPOTHESIS`.

## Problem

The first-region Honey economy must fund required Buzz progression, leave room for Flight and seeds, avoid replay grind, and avoid a purchase order that can soft-lock the campaign. Yield is especially risky because an income multiplier can become either a universal spreadsheet answer or a trap.

## Reference candidate pool

The research is qualitative rather than a source for copying numeric values.

| Product | Source | Direct observation | Relevance |
|---|---|---|---|
| Cow Bay | https://poki.com/en/g/cow-bay | Gathering/crafting unlocks islands; Poki also documents an energy cost per task. | Compact resource→progression loop; energy is an explicit BeBee anti-pattern. |
| Forager | https://en.wikipedia.org/wiki/Forager_%28video_game%29 | Resources and economic activity fund skills, tools and purchasable land expansion. | Shows the risk/benefit of currency feeding both capability and expansion. |
| Dreamdale | https://dreamdale.fandom.com/wiki/Tools | Tools are upgraded to improve resource output. | Useful comparison for capability spending and output-increase upgrades. |
| My Little Universe | https://news.xbox.com/en-us/2025/04/07/my-little-universe-survival-guide/ | Resource gathering and world expansion are tightly coupled to repeated active play. | Useful for short-session progression cadence, not exact values. |
| Cow Castle | https://poki.com/en/g/cow-castle | Gathering resources and earning coins unlock new locations/facilities. | Another low-complexity resource→world-progress pattern. |

## Selected references

### Cow Bay

Direct observation: the game uses a compact gather/craft/unlock structure and Poki explicitly says each task costs energy.

Inference for BeBee: the compact cadence is relevant, but BeBee should not solve pacing by hard energy scarcity. The simulator therefore disables replay/energy-style mandatory top-ups and treats new campaign content as the primary faucet.

### Forager

Direct observation: gathered resources/economic activity feed both capability growth and land expansion.

Inference for BeBee: when one economy funds multiple useful sinks, bad ordering can delay progression. BB-P005 therefore tests purchase-order safety rather than only a single designer-authored path.

### Dreamdale

Direct observation: tool upgrades improve resource production.

Inference for BeBee: production multipliers are familiar, but familiarity does not prove that Yield creates an interesting decision. BB-P005 calculates payback explicitly and runs multiplier sensitivity.

## Materially different solution / anti-pattern

Cow Bay's per-task energy cost is intentionally rejected for the vertical slice. BeBee should not hide an underfunded economy behind mandatory waiting/energy. The simulator fails paths that require replay to recover normal progression.

## Candidate model

The checked-in `tools/economy/first_region_candidate.json` is deliberately tagged `HYPOTHESIS`.

First pass exposed a failure: with Flight 3 and Yield available too early, **12 / 120** upgrade-priority permutations could spend enough optional Honey to reach M03 without the 35 Honey required for Buzz 2.

The correction was structural, not a hidden cash injection:

- Buzz 2, Flight 2 and the cheapest seed appear after M01;
- the second seed appears after M02;
- Flight 3, Yield 2 and the third seed appear only after M03;
- Buzz 3 appears after M04 and is required before M06.

This keeps desirable future purchases visible later without allowing the early shop to offer more optional spending than the campaign can safely fund.

## Current deterministic result

From `evidence/BB-P005/first-region-summary.json`:

- all named strategies pass required gates;
- all named strategies stay non-negative;
- all named strategies require **0 replay actions**;
- customization-heavy path passes with 327 Honey remaining;
- poor-but-valid path passes with 270 Honey remaining;
- **120 / 120** upgrade-priority permutations reach region completion;
- minimum final balance among those exhaustive upgrade-priority permutations is 337 Honey.

These results prove arithmetic safety for this candidate shape. They do **not** prove fun pacing.

## Yield sensitivity

Candidate cost: 40 Honey, available after M03. Future base Honey after that point is 345.

| Yield multiplier | Base Honey needed to repay | Break-even | Early-purchase final balance | Interpretation |
|---:|---:|---|---:|---|
| 1.10x | 400 | never in Region 1 | 377 | likely too weak |
| 1.15x | 266.67 | M06 | 393 | late payback; still needs playtest opportunity-cost evidence |
| 1.20x | 200 | M06 | 411 | stronger dominance risk |

No-Yield comparison path ends with 382 Honey.

Therefore `Yield` remains `HYPOTHESIS`. Arithmetic alone does not justify shipping it.

## Official technical documentation

The simulator intentionally uses only Python standard-library behavior:

- https://docs.python.org/3/library/itertools.html#itertools.permutations — exhaustive permutation generation;
- https://docs.python.org/3/library/json.html — deterministic JSON input/output.

Checked 2026-08-28.

## Run

```bash
python3 -m unittest discover -s tools/economy -p 'test_*.py' -v
python3 tools/economy/simulate.py
python3 tools/economy/simulate.py --output /tmp/bebee-economy-report.json
```

The command returns non-zero when hard assertions fail.

## Remaining validation before production values

- BB-P004 must decide how seeds participate in restoration; seed timing/costs may change afterward.
- BB-P003/P1 must establish pollination/movement pacing before Honey-per-minute can be judged.
- Yield needs observed opportunity-cost/playtest evidence before it can become `VALIDATED`.
- Production values should later move into the same data definitions consumed by the game and simulator.
