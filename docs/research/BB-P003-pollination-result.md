# BB-P003 — Pollination interaction result

Result date: **2026-08-28**.

Decision recommendation: **C — movement-through / sweep** becomes the validated primary pollination interaction pattern. This validates the ownership rule, not the current prototype's exact `245 px` work target or final production tuning.

## Problem restated

The core pollination verb must stay understandable and comfortable over many repetitions, work with touch, begin feedback quickly and preserve the fantasy that controlling the bee matters. The original proximity-auto design was a hypothesis, not a requirement.

The experiment plan and reference observations live in [`BB-P003-pollination-interaction.md`](BB-P003-pollination-interaction.md). The recorded browser run lives in [`../../evidence/BB-P003/browser-run-2026-08-28.json`](../../evidence/BB-P003/browser-run-2026-08-28.json).

## Controlled comparison

All variants use the same movement model, three patch positions/radii and visual feedback. The only core rule changed is how progress is earned.

| Metric | A — Proximity | B — Hold | C — Sweep |
|---|---:|---:|---:|
| Completion | 3/3 | 3/3 | 3/3 |
| Scripted browser run | 16.0 s | 15.1 s | 13.7 s |
| Stationary inside patch | 6.1 s | 5.0 s | **0.0 s** |
| Share of run stationary in patch | 38.1% | 33.1% | **0.0%** |
| Extra pollination presses/holds | **0** | 3 | **0** |
| Movement distance | 1083 px | 1127 px | 1436 px |
| Separate touch pollination control | no | **yes** | no |

The exact completion timings include travel/controller correction and are not treated as balance targets. The structural measurements are more important: auto and hold reward remaining in the patch while stationary; sweep cannot progress while stationary.

## Touch result

At the tested 640×820 page viewport the rendered gameplay canvas measured 614×383.75 CSS px.

- movement stick: 120×120, approximately 6.11% of canvas area;
- Hold's additional `POLLINATE` button: 108×108, approximately 4.95% of canvas area;
- raw simultaneous control-overlay area: approximately 6.11% for Auto/Sweep vs 11.06% for Hold.

The additional Hold control is not automatically unacceptable, but it spends significant touch-space solely to make an interaction explicit that Sweep can express through the already-required movement control.

## Evaluation

### A — Proximity auto-pollination

Strength:

- lowest explicit input burden;
- simplest rule to explain.

Observed weakness:

- 6.1 seconds of the 16.0 second browser run were stationary inside patches;
- the prototype's intrinsic rule continues progress while standing still;
- entering a patch starts progress regardless of deliberate pollination intent.

This reproduces the exact “move, wait, move, wait” risk identified before implementation. More VFX would not fix the ownership problem.

Verdict: **reject as the primary verb**. It may remain useful later for accessibility assistance only if such a mode is deliberately researched.

### B — Hold-to-pollinate

Strength:

- explicit start/stop ownership;
- faster intrinsic time rate than Auto in the current diagnostic tuning.

Observed weakness:

- still allows/encourages stationary completion;
- required three separate holds in the three-patch run;
- touch adds a second persistent high-frequency control and roughly five percent of canvas area as another control surface.

This solves ambiguity by adding input rather than by making flying meaningful.

Verdict: **reject as the primary verb**. It is a useful counterexample and could become an accessibility/alternate-input option only with separate evidence.

### C — Movement-through / sweep

Strength:

- zero stationary progress by construction and in the browser run;
- no second pollination button;
- movement itself owns progress;
- completed the same three patches with no extra interaction presses;
- maps directly to the bee fantasy: flying through/around flowers causes pollination.

Cost/risk:

- the scripted run moved about 32.6% farther than Auto;
- a poorly tuned work target could cause pointless oscillation inside a patch;
- passing through a patch may create some incidental progress.

These are tuning problems rather than reasons to add waiting or another input channel. Production should tune coverage/work so a natural pass/loop is enough at intended tier, use forgiving bounds, begin feedback immediately on valid movement and avoid requiring tiny repeated circles.

Verdict: **VALIDATE as primary interaction pattern**.

## Separate evaluator pass

Inputs were limited to the original player problem, pre-implementation reference observations, prototype rules, recorded browser measurements and rendered touch/desktop captures.

Finding 1 — **material**: Auto converts a large observable share of the tested loop into stationary patch time, conflicting with the requirement that flying matters.

Finding 2 — **material**: Hold restores explicit intent but preserves stationary interaction and adds a second touch action/control surface.

Finding 3 — **positive**: Sweep is the only candidate that simultaneously removes stationary progress and avoids a second high-frequency action channel.

Finding 4 — **follow-up**: Sweep's current distance target must not be promoted into production balance. P2 must tune required movement against natural approach/pass trajectories and check accidental-progress behavior.

Evaluator verdict: **PASS WITH DEVIATION** — select Sweep, but validate the *movement-owned rule*, not the prototype's exact `245 px` constant.

## Decision boundary

Validated:

> While the bee is inside a pollinatable patch, meaningful movement through/around the flowers advances pollination; standing still does not. Pollination does not require a separate high-frequency action button in the default control scheme.

Still open/tunable:

- exact movement-distance/work target;
- coverage falloff/forgiving edge distance;
- whether very slow motion counts fully;
- accidental fly-through threshold;
- species/difficulty multipliers;
- accessibility alternatives;
- final Defold input/collision implementation.

## Production consequences

P2 `FlowerPatch` implementation should treat pollination work as movement-owned input and expose tuning as data. It must not hard-code the prototype's pixels as production world units.

The interaction should preserve these invariants:

- no progress while stationary;
- immediate visible feedback after qualifying motion starts;
- no mandatory second pollination button;
- forgiving patch bounds;
- normal completion path does not require tiny repetitive circles;
- accessibility alternatives, if added, do not silently replace the validated default.
