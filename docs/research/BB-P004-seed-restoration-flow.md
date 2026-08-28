# BB-P004 — Seed ownership during restoration

Status: **validated**. `BB-P004` selects the Hybrid topology: authored native campaign plots remain stable during restoration while dedicated player-shaped plots accept seeds early; completed native plots may become replantable after restoration where content allows. Exact presentation, plot counts, planting input and seed economy remain open for P5 runtime validation.

## Problem

BeBee must communicate two ideas without turning a cozy loop into a management screen:

1. some flowers/patches represent authored ecological challenge and campaign completion;
2. the player should influence what the recovering meadow becomes before all restoration is already over.

The old `restore everything -> customize afterward` model is safe but risks making ownership feel like an epilogue. The opposite extreme—letting every campaign patch change identity immediately—may blur what the player is actually restoring.

## Reference candidate pool

| Product | Source | Direct observation relevant to BB-P004 | Why it matters |
|---|---|---|---|
| Garden Life: A Cozy Simulator | https://store.steampowered.com/app/1915380/Garden_Life_A_Cozy_Simulator/ | The player restores an abandoned community garden, unlocks seeds/areas through tasks, and freely chooses where plants go. | Strong reference for restoration and personal planting existing in the same journey. |
| Wildmender | https://www.wildmender.com/ | The player brings a deserted world back to life by collecting plants, planting seeds, tending a garden and shaping terrain; the site explicitly frames restoration as happening one seed at a time. | Strong reference for ownership being inseparable from restoration. |
| Cloud Gardens | https://store.steampowered.com/app/1372320/Cloud_Gardens | The player plants seeds to overgrow abandoned scenes; the campaign still has progression conditions while the resulting vegetation composition is player-shaped. | Useful integrated challenge + expression reference. |
| Terra Nil | https://www.terranil.com/ | Restoration proceeds through ecological transformation goals such as fertile grassland, forests and animal habitats. | Strong authored/ecological-goal reference and a materially different solution from personal gardening. |
| Grow: Song of the Evertree | https://store.steampowered.com/app/1380420/Grow_Song_of_the_Evertree/ | The player crafts World Seeds, grows new worlds and tends them as they rejuvenate. | Useful macro reference for player-generated identity being tied to world recovery. |

## Deep references

### Garden Life — restoration + free planting

Direct observation: the store description says the player takes charge of an abandoned community garden, completes tasks to restore it, unlocks seeds/tools/areas, and can place plants without a grid.

Inference for BeBee: player-authored flower placement does not need to wait until restoration is complete. However, Garden Life supports a much deeper gardening simulation than BeBee wants, so BeBee should borrow the timing of ownership rather than its management depth.

### Wildmender — player choice is the restoration verb

Direct observation: the official site describes bringing a deserted world back to life by collecting plants, planting seeds, shaping earth, channeling water and growing an oasis into the player's own garden.

Inference for BeBee: ownership can be visible from the beginning rather than added afterward. The survival/crafting/combat complexity is out of scope; the useful pattern is that planted species visibly participate in recovery.

### Terra Nil — authored ecological restoration

Direct observation: the official site frames progression as transforming barren land into specific ecological states such as fertile grassland, forests and animal habitats.

Inference for BeBee: authored ecological targets can make restoration legible and meaningful without asking the player to design every square metre. This is the strongest counterweight to a fully player-shaped model.

### Cloud Gardens — campaign condition + player expression

Direct observation: the store page describes planting seeds and placing objects to overgrow scenes while campaign stages still have progression conditions.

Inference for BeBee: a hybrid can preserve a clear campaign target while allowing the player's planting choices to be visible before completion.

## Materially different solution

`Terra Nil` is deliberately included as a materially different solution: restoration is primarily about satisfying ecological transformation goals, not preserving a personal flower composition. BeBee should retain enough authored/native identity that the player can understand biome/challenge progression even if ownership testing favors early seed choice.

## A/B/C models

### A — Native first

- three authored native campaign patches;
- player-shaped plots locked until all native objectives complete;
- after restoration, seeds can be planted/replanted freely.

Expected advantage: simplest campaign language.

Risk: first meaningful ownership action happens after the meadow is already restored.

### B — Player-shaped restoration

- all plots can receive a chosen seed during restoration;
- native campaign identity is stored separately from current planted/display species;
- replanting never erases campaign completion.

Expected advantage: maximum early ownership.

Risk: the player may need to understand two identities on one patch: `native challenge` and `current planted appearance`.

### C — Hybrid

- native campaign patches stay authored during restoration;
- dedicated player-shaped plots accept seeds immediately;
- after native restoration, native plots may also be replanted;
- player plots never block native campaign completion.

Expected advantage: early ownership with a visible separation between challenge and expression.

Risk: two plot types may themselves create cognitive overhead or feel like unrelated systems.

## Controlled invariant

All three prototype variants use:

- the same three native objectives;
- the same two player-shaped positions;
- campaign completion derived only from native completion state;
- reversible `plantedSpecies` state separate from campaign/native identity.

This keeps progression safety constant while the timing/location of ownership changes.

## Measurements

The prototype records:

- action count;
- first ownership action index;
- ownership actions before restoration;
- whether player choice is available before restoration;
- native campaign completion state;
- planted/display species state.

The experiment must also explicitly replant a completed native plot where allowed and verify completion is preserved.

Separate observation/evaluation should answer:

- can a new player explain native objective vs chosen appearance?;
- does ownership arrive early enough to support the fantasy?;
- does the mode require extra labels/instructions?;
- do player choices remain obviously reversible?;
- does the meadow retain an authored biome/challenge identity?;
- does customization feel part of restoration rather than a separate decoration menu?

## Official technical documentation

The disposable browser lab uses standard DOM events and HTML controls only. Pointer/touch-specific production behavior is not being locked here.

Relevant browser input authority for later touch interaction checks:

- https://www.w3.org/TR/pointerevents3/
- checked 2026-08-28.

Production implementation must still be re-verified against current Defold input/GUI documentation after the model is selected.

## Decision result

The deterministic A/B/C run and separate evaluator are recorded in [`BB-P004-seed-restoration-result.md`](BB-P004-seed-restoration-result.md) and [`../../evidence/BB-P004/model-run-2026-08-28.json`](../../evidence/BB-P004/model-run-2026-08-28.json).

Selected: **C — Hybrid**.

Why:

- A produced no ownership action before native restoration and therefore fails the ownership-during-restoration product requirement;
- B provides early ownership but allows an incomplete native campaign plot to carry a chosen display species different from its authored native identity;
- C provides an early ownership action through dedicated player-shaped plots while keeping incomplete native campaign plots authored and unambiguous at the state-model level;
- all variants preserve campaign completion across replanting, so safety alone does not decide the winner.

Validation scope is intentionally narrow. Human comprehension of the two plot roles, final visual language, exact plot count/placement, planting input and seed pacing remain P5 runtime/player validation tasks.
