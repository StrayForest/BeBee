# 14 — Economy Validation Specification

## 1. Purpose

Economy values are not accepted because they look plausible in a table. They must be tested as complete player paths.

This specification supports `BB-P005` and later balance regression tests.

## 2. Inputs

A deterministic model consumes:

- campaign sequence / available patches;
- first-time Honey rewards;
- milestone rewards;
- upgrade costs/effects;
- seed unlock costs;
- progression requirements;
- optional replay rewards if that system exists.

Production values should be read from the same data definitions used by the game where practical.

## 3. Required strategies

Simulate at least:

- `minimal_progression` — buys only what is required;
- `buzz_first`;
- `flight_first`;
- `balanced`;
- `customization_heavy` — buys available seeds/flower expression early;
- `poor_but_valid` — intentionally inefficient but legal spending;
- every relevant `yield_early/mid/late` path if Yield is retained;
- `no_replay`;
- `optional_replay_topup` if replay exists.

## 4. Required outputs

For each step/path:

- cumulative Honey earned;
- cumulative Honey spent;
- current balance;
- purchases made;
- progression gate encountered;
- replay actions required;
- remaining new-content rewards;
- time/actions estimate where the model has one.

For Yield-like income multipliers:

- purchase cost;
- incremental multiplier;
- future base Honey needed to break even;
- actual campaign point where break-even occurs;
- whether that purchase delays a required/meaningful capability.

## 5. Failure conditions

The model fails the proposed balance when:

- a normal customization-heavy path becomes stuck without disproportionate replay;
- intended progression requires repetitive starter farming;
- a stat is an obvious universal purchase because its compounding dominates alternatives;
- a stat never repays/provides meaningful value before relevant content ends;
- a required upgrade becomes affordable only after long idle/replay behavior unrelated to new content;
- Honey can go negative;
- a legal purchase order creates an unrecoverable soft-lock.

## 6. Targets

These are product targets to validate, not sacred constants:

- first meaningful reward quickly after gameplay starts;
- first capability improvement within the onboarding window;
- frequent visible progression in short sessions;
- new content funds most new-content progression;
- seeds are cheap enough to be used rather than treated as a trap;
- replay is optional.

## 7. CI/regression use

After P0/P3 tooling exists, a deterministic command should fail CI for hard invariants and print scenario summaries for review.

Hard assertions can include:

```text
balance >= 0
required campaign path completable without replay
customization-heavy representative path completable without excessive replay
all referenced costs/rewards non-negative
no unknown content IDs
```

Dominant-strategy findings may be warnings requiring design review rather than a simple numeric build failure.

## 8. Evidence

Economy PRs attach:

- scenario output/table;
- changed values;
- before/after scenario comparison;
- reason for change;
- telemetry/playtest evidence when available;
- Yield payback analysis if Yield is involved.
