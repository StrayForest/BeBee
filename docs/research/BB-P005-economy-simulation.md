# BB-P005 — First-region economy simulation

Status: **structural decision VALIDATED; numeric balance remains HYPOTHESIS**.

Decision result: [`BB-P005-economy-result.md`](BB-P005-economy-result.md). The vertical-slice upgrade set is **Flight + Buzz**; Yield is excluded. The current staged first-region candidate demonstrates no-grind arithmetic safety but does not lock final Honey values or time pacing.

## Problem

The first-region Honey economy must fund required Buzz progression, leave room for Flight and seeds, avoid replay grind, and avoid a purchase order that can soft-lock the campaign. Yield was especially risky because an income multiplier can become either a universal spreadsheet answer or a trap.

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

Inference for BeBee: the compact cadence is relevant, but BeBee should not solve pacing by hard energy scarcity. The simulator disables mandatory replay/energy-style top-ups and treats new campaign content as the primary faucet.

### Forager

Direct observation: gathered resources/economic activity feed both capability growth and land expansion.

Inference for BeBee: when one economy funds multiple useful sinks, bad ordering can delay progression. BB-P005 therefore tests purchase-order safety rather than only a single designer-authored path.

### Dreamdale

Direct observation: tool upgrades improve resource production.

Inference for BeBee: production multipliers are familiar, but familiarity does not prove that Yield creates an interesting decision. BB-P005 calculates payback explicitly and runs multiplier sensitivity.

## Materially different solution / anti-pattern

Cow Bay's per-task energy cost is intentionally rejected for the vertical slice. BeBee should not hide an underfunded economy behind mandatory waiting/energy. The simulator fails paths that require replay to recover normal progression.

## Candidate model history

The checked-in `tools/economy/first_region_candidate.json` remains a **research candidate**, not production balance. It intentionally retains the rejected Yield candidate so regression tooling can reproduce the decision evidence.

The first pass exposed a failure: with Flight 3 and Yield available too early, **12 / 120** upgrade-priority permutations could spend enough optional Honey to reach M03 without the 35 Honey required for Buzz 2.

The correction was structural, not a hidden cash injection:

- Buzz 2, Flight 2 and the cheapest seed appear after M01;
- the second seed appears after M02;
- Flight 3, historical Yield 2 and the third seed appear only after M03;
- Buzz 3 appears after M04 and is required before M06.

This staging removed the early soft-lock envelope.

## No-Yield structural result

After BB-P004 validated the Hybrid seed topology, BB-P005 re-ran the economy with Yield removed and exhaustively tested every priority ordering across the retained seven sinks:

- Buzz 2 / Buzz 3;
- Flight 2 / Flight 3;
- Daisy / Clover / Lavender seed sinks.

Result from `evidence/BB-P005/upgrade-set-summary.json`:

- **5040 / 5040** full purchase-priority orders reach region completion;
- **0** replay actions;
- **0** negative-balance paths;
- final balance after purchasing all seven retained sinks: **271 Honey**.

This validates a no-grind **structural envelope**, not final fun pacing.

## Yield decision evidence

Historical candidate: 40 Honey, available after M03, 1.15x future rewards.

| Timing | Final balance | Difference vs no Yield |
|---|---:|---:|
| No Yield | 382 | — |
| Earliest allowed | 393 | +11 |
| Mid | 381 | -1 |
| Late | 367 | -15 |

Mathematical break-even occurs only at M06. Sensitivity also flips the role sharply: 1.10x never repays in Region 1, while 1.20x raises the early result to 411 and moves toward an obvious economic opener.

Decision: **exclude Yield from the vertical slice**. Flight and Buzz have direct experiential roles; Yield is not required for progression and its tested value is primarily a timing/payback calculation. Do not add a replacement stat just to preserve three cards.

## Official technical documentation

The simulator uses Python standard-library behavior:

- https://docs.python.org/3/library/itertools.html#itertools.permutations — exhaustive permutation generation;
- https://docs.python.org/3/library/json.html — deterministic JSON input/output.

Checked 2026-08-28.

## Run

```bash
python3 -m unittest discover -s tools/economy -p 'test_*.py' -v
python3 tools/economy/simulate.py
python3 tools/economy/upgrade_set_analysis.py
python3 tools/economy/upgrade_set_analysis.py --output /tmp/bebee-upgrade-set.json
```

The decision-analysis command returns non-zero when hard assertions fail.

## Remaining validation before production values

- production movement/pollination pacing must establish Honey-per-minute and meaningful purchase cadence;
- P3 must tune final Flight/Buzz effects through direct gameplay evidence;
- P5 must tune seed unlock/cost pacing in the rendered Hybrid flow;
- production values should later move into the same data definitions consumed by the game and simulator.

Reopening Yield or adding a third track requires a concrete player problem and new evidence; the burden is not "fill the third card."
