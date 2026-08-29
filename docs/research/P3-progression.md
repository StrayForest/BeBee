# P3 — Progression production research

Status: **IMPLEMENTATION CANDIDATE — exact-head runtime/evidence gate pending.**

## Problem

P2 proves the first complete `move -> pollinate -> Honey -> unlock -> reload` loop. P3 must make Honey create immediately understandable permanent power without adding a filler stat, a second currency, a delayed purchase timer, or a Honey-paid world gate.

The P3 target is:

```text
complete first patch -> 45 Honey -> visit Hive -> choose Flight or Buzz -> one-action purchase
-> effect is immediately observable -> later Buzz-gated flower is explicit -> reload preserves upgrade and gate state
```

D-007 already validates the **two-track set: Flight + Buzz**. P3 does not reopen Yield. The remaining production question is the smallest effect/cost/gate slice that makes both tracks useful while keeping either first purchase viable.

## Existing direct BeBee evidence

- P1 validates a 300-unit/s direct-intent movement baseline on keyboard and floating touch.
- P2 validates movement-owned pollination, Daisy/Clover work targets, first rewards of 45/55 Honey and durable completion/Honey.
- BB-P005 already found a no-Yield economy family in which Flight 2 costs 30 Honey and Buzz 2 costs 35 Honey, with both purchase orders able to progress without replay.

P3 therefore uses those values as the candidate to test against the real P1/P2 runtime rather than inventing a new price table after seeing the implementation.

## Reference candidate pool

| Product | Source | Relevance |
|---|---|---|
| Slime Rancher | https://slimerancher.fandom.com/wiki/Vacpack_Upgrades | Dedicated ranch/home upgrade terminal; permanent upgrades expose cost and concrete effect. |
| Dave the Diver | https://dave-the-diver.fandom.com/wiki/iDiver | Upgrade surface shows current level/stat, next value and price; useful for compact card information hierarchy. |
| A Short Hike | https://ashorthike.fandom.com/wiki/Golden_Feather | Permanent upgrade directly changes traversal feel, demonstrating value of immediately perceivable movement progression. |
| Hades | https://hades.fandom.com/wiki/Mirror_of_Night | Broad many-row meta-progression; useful complexity counterexample for BeBee's low-cognitive-load vertical slice. |
| Stardew Valley | https://stardewvalleywiki.com/Blacksmith | Tool upgrades use materials/currency plus a multi-day delay; useful anti-pattern for a tiny immediate-feedback browser loop. |
| Spiritfarer | https://spiritfarer.fandom.com/wiki/Albert%27s_Shipyard | Home-base improvement surface and capability-oriented unlocks; secondary structural reference. |

## Deep observations

### Slime Rancher — dedicated home upgrade surface

**Observed:** Vacpack upgrades are bought at the ranch through a dedicated upgrade interface; entries communicate a permanent capability and a price.

**Inference for BeBee:** put permanent bee progression at a recognizable Hive/home interaction rather than on top of a flower. Keep the interaction low-frequency: enter the Hive panel, see the effect/cost, buy once.

### Dave the Diver — current/next/price hierarchy

**Observed:** iDiver equipment upgrades present a level/stat progression and a price, making the before/after change legible at the purchase point.

**Inference for BeBee:** each card should show current level/effect, next effect and Honey price before purchase. With only two validated tracks, two cards are sufficient; a third empty/filler slot would weaken the evidence-backed set.

### A Short Hike — traversal upgrade is felt immediately

**Observed:** Golden Feathers change the player's movement capability rather than only changing a hidden score.

**Inference for BeBee:** Flight must affect the already-validated movement runtime itself. A purchase that only increments a save value is not acceptable evidence.

## Materially different solution / anti-pattern

Hades' Mirror supports many rows, ranks and alternative talents. It is a valid solution for a larger long-run meta-progression game, but it is intentionally the wrong density for BeBee P3: the vertical slice has only two evidence-backed bee stats and a low-cognitive-load target.

Stardew Valley's Blacksmith adds a meaningful time delay to tool upgrades. BeBee rejects that delay for P3 because the milestone needs an immediate `reward -> purchase -> feel effect` loop and has no validated waiting/calendar problem to solve.

## Production alternatives

### A — Flight + Buzz cards, immediate purchase, no confirmation

- dedicated Hive panel;
- two cards only;
- current -> next effect and price visible;
- primary action buys selected affordable upgrade immediately;
- modal consumes movement while open;
- permanent effect applies as soon as the transaction succeeds.

**Selected.** It matches D-007, keeps action count low and makes exact runtime effects testable.

### B — three-card screen with a replacement Yield/filler stat

**Rejected.** D-007 explicitly excludes Yield and forbids adding another track merely to preserve a three-card layout.

### C — purchase confirmation dialog after selecting a card

**Rejected for P3.** The purchase is low-frequency, reversible only through future balancing rather than destructive inventory loss, and the extra modal adds interaction cost without a demonstrated error problem.

### D — passive/automatic upgrade when Honey threshold is reached

**Rejected.** It removes the meaningful Flight-vs-Buzz choice and makes Honey spending invisible.

## P3 candidate values

| Track | Level 1 | Level 2 | Cost | Unlock |
|---|---:|---:|---:|---|
| Flight | 300 u/s | 330 u/s | 30 Honey | after patch #1 |
| Buzz | 1.00x work | 1.35x work | 35 Honey | after patch #1 |

The first completed Daisy gives 45 Honey. Therefore both first choices are individually affordable.

If Flight is bought first:

```text
45 - 30 = 15
15 + 55 Clover reward = 70
70 - 35 Buzz = 35
```

So Flight-first cannot strand the player before the first required Buzz gate. Buzz-first likewise leaves 10 Honey after the first purchase and still permits Flight after Clover. The machine regression checks both orders, all two-upgrade permutations, a minimal-required path and a customization-heavy shadow-spend path.

## First explicit Buzz gate

P3 adds Lavender patch #3 as the first authored capability gate:

- prerequisite: patch #2 completed;
- required Buzz: level 2;
- work target: 620;
- reward: 70 Honey;
- world state must explicitly report `requires_buzz` and required level while locked.

The gate is not a Honey payment. Honey buys the permanent Buzz capability at the Hive; the flower checks capability, preserving D-010.

## Runtime architecture

- `systems/progression.lua` owns upgrade levels, availability, atomic purchase and patch capability eligibility.
- `systems/economy.lua` remains the Honey transaction primitive.
- movement receives a computed `max_speed`; it does not know Honey or upgrade prices.
- flower work receives a computed Buzz multiplier; `FlowerPatch` does not own progression/economy.
- the Hive GUI renders state and emits purchase intent only; it never mutates Honey/levels directly.
- the existing modal input-focus stack consumes movement while the Hive is open.

## Save compatibility

P3 increments the domain save version from 1 to 2 and introduces explicit `player.upgrades` state.

The required migration is `v1 -> v2`:

- preserve Honey and campaign completions;
- initialize missing Flight/Buzz to level 1;
- reject future versions and invalid authored levels;
- continue using the existing A/B storage adapter and HTML5 durability semantics.

A regression fixture loads a representative P2 save with 45 Honey and completed patch #1 and verifies no data loss after migration.

## Official Defold documentation checked 2026-08-29

### Input focus / modal isolation

- https://defold.com/manuals/input/
- https://defold.com/manuals/input-gamepads/ (input stack semantics are shared with the input system; P3 uses keyboard/touch actions already defined by P0/P1)

Verified constraints used by P3:

- game objects acquire/release input focus explicitly;
- focused components are evaluated through the input stack;
- returning `true` consumes an action and prevents lower recipients from acting on it.

Implementation consequence: the Hive uses the existing modal controller. Opening it clears movement, acquires modal focus and consumes subsequent movement/primary/pointer actions until close.

### GUI hit testing / presentation

- https://defold.com/ref/stable/gui-lua/#gui.pick_node
- https://defold.com/manuals/gui-script/

Verified constraints used by P3:

- GUI scripts own presentation nodes and supported hit testing can use GUI node bounds;
- runtime text/box nodes can be updated without moving economy/progression ownership into GUI.

Implementation consequence: the Hive panel shows two presentation cards and routes intent back to the gameplay controller; the domain transaction stays in `systems/progression.lua`.

### Persistence

- https://defold.com/ref/stable/sys/

Verified constraint: platform persistence can fail and has size/error constraints, so P3 does not bypass the existing protected storage abstraction with direct gameplay `sys.save` calls.

## Acceptance criteria for P3

1. Production catalog contains exactly the validated Flight/Buzz tracks for the P3 slice; no Yield/replacement filler track.
2. After patch #1, both Level-2 choices are available and individually affordable from the same 45-Honey state.
3. Flight purchase spends exactly 30 once and changes real movement max speed from 300 to 330 u/s.
4. Buzz purchase spends exactly 35 once and changes real pollination work multiplier from 1.00x to 1.35x.
5. Hive panel displays current/next effect and price for both cards and consumes movement while open.
6. Lavender patch #3 remains explicitly locked by `Buzz 2` after patch #2 and becomes available immediately after Buzz 2 purchase.
7. Economy regression passes Flight-first, Buzz-first, exhaustive order, minimal-required and customization-heavy scenarios with no replay/negative Honey/dead-end.
8. v1 P2 saves migrate to v2 with Honey/completions intact and Flight/Buzz initialized to level 1.
9. Reload preserves purchased Flight/Buzz and resulting gate eligibility without duplicate spend/reward.
10. Desktop and 844x390 mobile progression states render without browser console/page errors; P1/P2 movement, modal, pollination and storage proofs remain green.
11. Separate evidence-first evaluation returns PASS or justified PASS WITH DEVIATION; any ITERATE blocks closeout.

## Current implementation-candidate status

Local deterministic economy regression: **PASS** for the candidate values above. New Python capture scripts compile and JSON data parses. The authoritative Defold/headless/browser result is intentionally not claimed here yet; it must come from GitHub exact-head CI and a retained `movement-qa-$PR_HEAD` artifact before P3 can be marked COMPLETE.
