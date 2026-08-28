# BB-P004 — Seed/restoration flow result

Result date: **2026-08-28**.

Decision recommendation: **C — Hybrid** becomes the validated seed/restoration topology for BeBee. This validates the separation of authored campaign plots and player-shaped plots during restoration, not final production UI, plot counts, seed economy, placement gestures or art treatment.

## Problem restated

Seed choice must contribute to ownership before a meadow is already finished, while campaign-native objectives remain understandable and cannot be damaged by aesthetic choices.

The experiment plan and reference analysis live in [`BB-P004-seed-restoration-flow.md`](BB-P004-seed-restoration-flow.md). The deterministic model run is retained in [`../../evidence/BB-P004/model-run-2026-08-28.json`](../../evidence/BB-P004/model-run-2026-08-28.json).

## Controlled comparison

All three variants use the same three native campaign objectives, two player-shaped positions and the same invariant that campaign completion is derived only from native completion state.

| Structural metric | A — Native first | B — Player-shaped | C — Hybrid |
|---|---:|---:|---:|
| Ownership actions before restoration in scripted protocol | 0 | 2 | 1 |
| First ownership action | after native restoration | first action | first action |
| Player plot plantable before restoration | no | yes | yes |
| Native plot plantable before restoration | no | yes | no |
| Incomplete native plot can show a chosen species different from its native identity | no | **yes** | no |
| Campaign completion survives replanting | yes | yes | yes |
| Native identity survives replanting | yes | yes | yes |

The action counts are diagnostic, not production pacing targets. The material differences are timing of ownership and whether one incomplete native plot is asked to carry both authored campaign identity and a different chosen appearance at the same time.

## Evaluation

### A — Native first

Strengths:

- simplest restoration language;
- native objectives stay visually authoritative;
- no dual-role patch during restoration.

Observed weakness:

- the deterministic protocol produces zero ownership actions before restoration;
- the first possible ownership action occurs only after all native objectives are complete.

This fails the locked product principle that customization participates in the restoration journey instead of arriving only as an epilogue.

Verdict: **reject as the default model**.

### B — Player-shaped restoration

Strengths:

- player expression is available immediately;
- maximum flexibility during restoration;
- campaign state remains safe because `campaignComplete` is independent from `plantedSpecies`.

Observed weakness:

- an incomplete native plot can simultaneously retain one `nativeSpecies` for campaign meaning while displaying another player-chosen `plantedSpecies`;
- the player therefore has to understand two identities on the same active campaign object before restoration is complete.

The model is progression-safe, but it creates the exact comprehension ambiguity identified before the experiment. Solving it would require additional labels, overlays or other UI explanation that BeBee is explicitly trying to avoid.

Verdict: **reject as the default model**. It remains a useful fallback if later runtime testing proves dedicated player-shaped plots visually incoherent.

### C — Hybrid

Strengths:

- a player-owned planting action is available from the first restoration phase;
- native campaign plots remain authored and visually stable until their campaign role is finished;
- dedicated player-shaped plots carry chosen identity during restoration instead of overloading native campaign patches;
- after restoration, native plots may become replantable without erasing campaign completion;
- aesthetic state and campaign state remain structurally independent.

Cost/risk:

- two plot roles exist during restoration and must be communicated visually without a management-heavy tutorial;
- the current disposable prototype does not prove that a new human player will immediately understand that distinction;
- exact plot count, placement, seed acquisition and planting interaction remain unvalidated.

Verdict: **VALIDATE the Hybrid topology**.

## Separate evaluator pass

Inputs were limited to the original product problem, pre-implementation reference observations, A/B/C model rules, deterministic experiment output and the locked low-cognitive-load/no-soft-lock principles.

Finding 1 — **material**: Native-first is structurally safe but violates the ownership-during-restoration requirement because it provides no pre-restoration seed action.

Finding 2 — **material**: Player-shaped provides the most early freedom but permits a still-active native campaign object to display a chosen species different from its native identity, increasing semantic load on one object.

Finding 3 — **positive**: Hybrid is the only tested model that simultaneously provides pre-restoration ownership and prevents an incomplete native campaign plot from carrying conflicting authored/chosen identities.

Finding 4 — **follow-up**: the experiment is a deterministic structural test, not a human comprehension playtest. P5 must prove that native plots and player-shaped plots are visually distinguishable without persistent explanatory UI.

Evaluator verdict: **PASS WITH DEVIATION** — select Hybrid as the production topology, but keep its presentation, plot count and interaction details open until runtime evidence exists.

## Decision boundary

Validated:

> During restoration, authored native campaign plots keep their campaign/native identity, while dedicated player-shaped plots may accept owned seeds. Player-shaped plots never gate native campaign completion. After restoration, completed native plots may become replantable where the content design allows it. Campaign completion/native identity and current planted species are separate persistent state concepts.

Still open/tunable:

- number and placement of player-shaped plots;
- whether every meadow exposes them immediately or after a short onboarding beat;
- exact planting gesture/input;
- seed unlock/cost pacing;
- visual language distinguishing native vs player-shaped plots;
- whether native plots are always replantable after restoration or only selected ones;
- establishment/pollination behavior for newly planted seeds;
- save schema details beyond the already-validated separation of campaign and planted state.

## Production consequences

P5 should implement the Hybrid topology, not the Native-first or fully Player-shaped model by default.

Production must preserve these invariants:

- at least one meaningful seed/ownership opportunity occurs before full meadow restoration in the intended flow;
- incomplete native campaign plots cannot silently lose or visually contradict their authored campaign identity through seed choice;
- player-shaped plots do not block campaign restoration;
- replanting cannot erase completed campaign progress;
- native/campaign identity and current planted species remain separate state;
- the distinction between native and player-shaped plots must be understandable from the rendered world with minimal UI.

If P5 human/runtime evidence shows that two plot roles cannot be communicated cleanly, reopen the presentation/model boundary rather than adding permanent explanatory clutter.
