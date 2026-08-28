# BB-P003 — Pollination interaction research and experiment plan

Status: **experiment in progress**. This document does not validate `D-006` yet.

## Problem

BeBee needs a repeatable pollination verb that remains pleasant after many repetitions, works on desktop and touch, gives fast feedback, and preserves the fantasy that flying the bee matters. The current proximity-auto model is only a hypothesis.

## Reference candidate pool

| Product | Source | Direct observation relevant to BB-P003 | Why it matters |
|---|---|---|---|
| Cow Bay | https://poki.com/en/g/cow-bay | Poki states that objects are harvested/used by tapping or clicking them. | Strong explicit-action reference with very low control complexity. |
| Dreamdale | https://dreamdale.fandom.com/wiki/Game_Mechanics | The community mechanics reference describes some harvesting as standing near objects or walking over plants, with no idle tapping required. | Direct analogue for proximity/automatic collection. |
| My Little Universe | https://news.xbox.com/en-us/2025/04/07/my-little-universe-survival-guide/ | Xbox Wire describes an optional Manual Controls mode in which chopping/mining actions require explicit button presses. | Useful contrast between automatic and explicit action ownership. |
| Forager | https://forager.fandom.com/wiki/How_to_play_guide_for_Forager | The control guide uses movement plus an explicit left-click hit action for resource objects. | High-agency active collection reference; also shows added input cost. |
| Cow Castle | https://poki.com/en/g/cow-castle | Poki exposes movement as the primary control while the game centers on chopping/mining/gathering. | Useful movement-centric reference from the same accessible browser/mobile design space. |
| Olly the Paw | https://poki.com/en/g/olly-the-paw | Poki supports keyboard movement and click-and-hold movement on desktop/mobile. | Useful for low-friction movement/input expectations, even though it is not an exact pollination analogue. |

## Deep references selected for the first experiment

### 1. Cow Bay — explicit action

Direct observation: Poki documents tap/click on an object as the harvest/use action.

Inference for BeBee: an explicit pollination action can make intent unambiguous, but repeating a separate action for every flower patch may add unnecessary input burden. Variant **B / Hold** tests whether continuous hold preserves agency without turning pollination into repeated clicking.

### 2. Dreamdale — proximity/automatic action

Direct observation: the mechanics reference describes harvesting certain resources by standing near them or walking over them, without idle tapping.

Inference for BeBee: proximity can minimize control overhead, but a stationary bee may become the optimal interaction. Variant **A / Proximity** measures stationary time explicitly so passive waiting is visible rather than hidden by subjective judgement.

### 3. My Little Universe — automatic vs manual contrast

Direct observation: Xbox Wire describes a Manual Controls option where each chopping/mining/dodging action requires button presses.

Inference for BeBee: action ownership is not binary; a game can support an automatic baseline while explicit actions create a different feel. BB-P003 therefore compares both and adds a third movement-owned variant instead of assuming one pattern is universally superior.

## Materially different solution / anti-pattern

Forager uses movement plus explicit resource-hit input. It gives strong action ownership, but this pattern also demonstrates the cost of requiring an extra action channel for a high-frequency gathering loop. BeBee should not import an attack/tool verb merely because it is familiar in resource games.

## Experiment variants

### A — Proximity auto-pollination

- progress while inside patch radius;
- standing still continues progress;
- no explicit pollination action.

### B — Hold-to-pollinate

- bee must be inside patch radius;
- player must hold Space / the touch POLLINATE control;
- release immediately stops progress.

### C — Movement-through / sweep

- progress is proportional to movement distance while inside the patch;
- standing still produces zero progress;
- no second action button.

## Controlled variables

The first pass keeps these equal across all variants:

- movement acceleration/deceleration;
- maximum movement speed;
- three patch positions and radii;
- completion target;
- camera/viewport;
- visual feedback hierarchy.

Do not balance individual variants before the first comparison run; otherwise interaction quality becomes confounded with tuning.

## Measurements

The prototype records:

- `first_feedback_ms`;
- `completion_ms`;
- `active_seconds`;
- `stationary_inside_seconds`;
- `movement_distance_px`;
- `pollinate_presses`;
- `completed_patches`.

Separate evaluation should additionally score:

- agency / intentionality, 1–5;
- repetition comfort, 1–5;
- mobile comfort, 1–5;
- accidental progress frequency;
- whether the bee's movement remains the primary expressive verb.

## Official technical documentation

Prototype input uses W3C Pointer Events Level 3:

- https://www.w3.org/TR/pointerevents3/
- checked: 2026-08-28;
- relevant constraint: Pointer Events provide one hardware-agnostic input model for mouse, pen and touchscreen; pointer capture keeps an active pointer routed to the element while dragging outside its original hit target.

This is a disposable browser experiment. It does **not** establish the production Defold input implementation; Defold input remains a P0/P1 concern and must be verified against current Defold documentation before production code.

## Acceptance for the experiment harness

The harness is ready to collect evidence when:

- all three variants share the same movement and field geometry;
- all three have mechanically distinct progress rules;
- desktop controls work;
- touch movement is represented through Pointer Events;
- hold mode exposes an explicit touch action;
- metrics can be copied as JSON;
- deterministic `qa=active` and `qa=complete` states exist for later capture automation;
- model tests pass.

## Decision gate

Do **not** change `D-006` from `HYPOTHESIS` until runs have been performed and the results/evaluation are recorded. The winner may be A, B, C, or a narrowly justified hybrid discovered from the evidence.
