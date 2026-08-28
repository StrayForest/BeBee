# BB-P005 — Economy / upgrade-set result

Result date: **2026-08-28**.

Decision recommendation: **validate Flight + Buzz as the vertical-slice upgrade set and exclude Yield**. This validates the structural upgrade set and the current candidate's no-grind arithmetic envelope; it does not lock final Honey values or real-time pacing.

## Problem restated

BeBee needs upgrades that create understandable choices without turning the cozy loop into an optimization spreadsheet. The first region also has to remain completable after seed/customization spending without replay farming.

`Yield` was the unresolved track because an income multiplier can be a trap when bought too late, an obvious universal purchase when tuned too strongly, or meaningless when tuned too weakly.

The pre-decision research and original candidate simulation live in [`BB-P005-economy-simulation.md`](BB-P005-economy-simulation.md). The deterministic decision report lives in [`../../evidence/BB-P005/upgrade-set-summary.json`](../../evidence/BB-P005/upgrade-set-summary.json).

## Controlled decision test

The checked-in candidate retains the historical 1.15x Yield option for regression comparison. `tools/economy/upgrade_set_analysis.py` then removes only Yield and exhaustively permutes every remaining purchase priority:

- Buzz 2;
- Buzz 3;
- Flight 2;
- Flight 3;
- Daisy seed;
- Clover seed;
- Lavender seed.

That produces **7! = 5040** full purchase-priority orders.

Result:

| Metric | Result |
|---|---:|
| Purchase-priority orders tested | 5040 |
| Region completions | **5040 / 5040** |
| Failed required gates | **0** |
| Replay actions required | **0** |
| Negative-balance paths | **0** |
| Final balance after all seven sinks | **271 Honey** |

Because every full order eventually buys all seven retained sinks, the final balance is the same 271 Honey in each full-order run. The important result is that no ordering can spend enough optional Honey to make required Buzz progression impossible under this candidate structure.

## Yield result

Historical candidate: **40 Honey for 1.15x future Honey**, available after M03.

- no-Yield comparison final balance: **382**;
- earliest allowed Yield purchase: **393** — net +11 vs no Yield;
- mid purchase: **381** — net -1;
- late purchase: **367** — net -15;
- mathematical payback occurs only at **M06**;
- 1.10x never repays inside Region 1;
- 1.20x improves the early-purchase result to 411, increasing the risk that the mathematically correct answer becomes "buy income first".

This is not a stability property we want from the vertical-slice upgrade set. Small tuning/timing changes flip Yield between weak/trap and increasingly dominant, while the stat does not directly change flying or pollination capability.

## Alternatives

### A — keep 1.15x Yield

Rejected for the vertical slice.

It is not needed to make the economy safe and only the earliest allowed timing beats the no-Yield comparison in Region 1. The player-facing choice is largely a payback calculation.

### B — retune Yield stronger/weaker

Rejected for the vertical slice.

The sensitivity run demonstrates the underlying problem rather than solving it: weaker tuning fails to repay, stronger tuning moves toward a universal economic opener. More numerical tuning does not create a direct experiential purpose.

### C — Flight + Buzz only

**Selected.**

Flight changes traversal feel. Buzz changes pollination capability/access. Both can be judged through direct gameplay experience. The shop is intentionally allowed to have two upgrade tracks rather than preserving a third card for symmetry.

Yield may be reconsidered after the vertical slice only if new playtest/telemetry evidence identifies a concrete player problem that an economy-output track solves better than simpler alternatives.

## Separate evaluator pass

Inputs: original BB-P005 problem, reference observations, locked no-soft-lock/simplicity principles, the existing first-region simulation, Yield sensitivity/payback, and the 5040-order no-Yield stress run.

Finding 1 — **positive**: removing Yield does not threaten campaign funding; every tested retained-sink priority reaches region completion without replay.

Finding 2 — **material**: the 1.15x Yield candidate is timing-sensitive. Early purchase produces +11 final Honey, mid purchase -1 and late purchase -15 against the same no-Yield comparison.

Finding 3 — **material**: multiplier sensitivity changes the answer substantially without changing the player's direct action capability. This makes the track primarily an economy optimization problem.

Finding 4 — **scope limit**: arithmetic safety does not prove the exact reward/cost table feels well paced in minutes. Production movement/pollination timing and human playtests must tune those values later.

Evaluator verdict: **PASS WITH DEVIATION** — validate the two-track vertical-slice upgrade set and no-grind structural envelope; keep exact numeric pacing as HYPOTHESIS.

## Decision boundary

Validated:

> The vertical slice uses Flight and Buzz as bee upgrade tracks. Yield is not part of the vertical-slice upgrade set. The current staged first-region economy shape demonstrates a replay-free arithmetic path even under all 5040 full priority orders across retained upgrades and seed sinks.

Still open/tunable:

- exact Honey rewards and costs;
- Flight effect curve;
- Buzz effect curve and exact flower gates;
- real-time minutes/actions between purchases;
- exact seed unlock/cost values after P5 runtime validation;
- whether a later post-vertical-slice system needs a new economy-oriented upgrade at all.

## Production consequences

P3 must build upgrade UI around the validated **two-track** set rather than a fixed three-card assumption.

Do not introduce a replacement stat merely to make the screen symmetrical. A third track requires its own player problem, research, alternatives and evidence.

The deterministic economy harness remains a regression tool. When production values become data-owned, the simulator should consume those same definitions and continue checking no-negative/no-replay/purchase-order safety.
