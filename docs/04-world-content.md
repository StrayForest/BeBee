# 04 — World & Content Design

## 1. Authority

This document owns canonical region/meadow/flower content structure. Economy values belong in `02-progression-economy.md`; global decision status belongs in `DECISIONS.md`.

Later-region content remains proposal-level until its own P7 slice is accepted.

## 2. World structure

BeBee uses an authored planet:

```text
Planet
 └─ Region
     └─ Meadow
         ├─ FlowerPatch
         ├─ Player-shaped / seed-capable plot where validated
         └─ UnlockGate / Landmark
```

Authoring gives better pacing, visual composition, tutorial control and performance predictability than an infinite procedural world.

## 3. Canonical proposed region order

To resolve the previous documentation contradiction, the current canonical proposal is:

1. **Sunny Meadows** — first-region tutorial/vertical slice;
2. **Golden Fields** — larger open loops, sunflower/poppy identity;
3. **Wetland Garden** — water/roots/islands, lotus/iris identity;
4. **Rosewood** — woodland clearings, rose/bluebell identity;
5. **Alpine Bloom** — rock/snow/wind, alpine flower identity;
6. **Moon Garden** — glowing/exotic finale.

This order is recorded in `DECISIONS.md` as the current canonical proposal. Regions remain proposal-level until their own P7 slice is accepted; the accepted slices are tracked in `docs/06-production-roadmap.md`.

## 4. Region design rules

A region should have:

- distinct biome/color identity;
- compact authored meadows;
- 1–2 new flower families rather than an unrelated system dump;
- at least one orientation landmark;
- one modest navigation variation;
- visible restoration finale;
- a seed/flower-expression reward or discovery.

New regions should mostly reuse proven systems. If a region needs major new architecture, stop and question the architecture/content scope.

## 5. First-region proposal — HYPOTHESIS until pacing validation

### M01 — First Patch

Role: teach movement, the validated pollination verb, first Honey and first improvement.

- small number of starter patches;
- Hive/home nearby if Hive remains the validated upgrade surface;
- visibly harder future flower nearby;
- no meaningful navigation obstacle.

Do not lock the first seed grant here until `BB-P004` chooses the seed/restoration flow.

### M02 — Clover Bend

Role: first route choice and first player-ownership/seed demonstration if the validated flow introduces it here.

- starter flower mix;
- curved route/landmark;
- at least one space where player choice can visibly alter the recovering meadow.

### M03 — Lavender Bank

Role: first soft difficulty aspiration.

- easy + medium patches;
- underpowered interaction remains understandable;
- relevant improvement visibly changes efficiency.

### M04 — Creek Garden

Role: movement/navigation feel.

- shallow creek/bridge loop;
- slightly longer traversal that makes movement upgrades desirable without hard-requiring them.

### M05 — Tulip Rise

Role: mixed-tier efficiency and route order.

- clear fork/order choice;
- large readable bloom payoff;
- room for visible player-selected flower composition.

### M06 — Lily Clearing

Role: region climax.

- explicit high-tier gate candidate;
- strongest first-region restoration sequence;
- region-completion reward/reveal;
- next-region silhouette rather than a full new production area.

The old exact patch counts are no longer locked. `BB-P005`/P2/P4 playtests determine final counts and pacing.

## 6. Flower content model

Each flower definition is data-driven.

Conceptual schema:

```lua
{
  id = "flower_daisy",
  display_name_key = "flower.daisy",
  tier = 1,
  pollination_required = 3,
  base_honey = 10,
  min_buzz_level = 1,
  gate_mode = "none",
  palette_id = "daisy_white_yellow",
  patch_prefab = "/flowers/daisy/daisy_patch.collection",
  tags = { "starter", "meadow" }
}
```

Canonical values live in data/economy ownership, not copied into multiple docs.

Do not encode progression by checking species names in behavior scripts.

## 7. Flower roster principles

A new species should add at least two meaningful dimensions:

- silhouette;
- dominant color;
- biome identity;
- difficulty vocabulary;
- reward/collection identity;
- subtle bloom/pollination presentation.

Avoid adding near-identical species merely to inflate a collection count.

## 8. Native challenge vs planted expression

This separation is required regardless of the final seed flow.

Each campaign patch/plot may have:

- `native_flower_id` or campaign objective identity;
- campaign completion state;
- current planted/display species;
- optional player-choice state.

Changing a planted species must not erase campaign-native completion or lock the player out of progression.

## 9. Seed/restoration flow — HYPOTHESIS

The old rule “finish the whole meadow, then customization begins” is no longer authoritative.

`BB-P004` evaluates:

### Model A — Native first

All required native work completes before the player replants.

Pros: simple campaign language.
Risk: ownership arrives too late.

### Model B — Player-shaped restoration

Owned seeds can be planted while the meadow is still being restored.

Pros: closest to the original fantasy of choosing what the planet becomes.
Risk: native difficulty/progression language may become unclear.

### Model C — Hybrid

Some authored native patches establish biome/challenge identity while dedicated/optional plots can be shaped by the player during restoration.

Pros: likely best separation of campaign readability and ownership.
Risk: must not feel like two unrelated patch systems.

The selected model becomes `VALIDATED` in `DECISIONS.md` before P5 is implemented permanently.

## 10. Combination system

Player-requested flower combinations can exist without arbitrary tile editing.

Baseline approach:

- different plots/patches in one meadow may use different primary species;
- optional Accent species is post-vertical-slice only if readability/performance remain strong.

If Accent exists later:

- primary remains visually dominant;
- accent is cosmetic-first;
- no negative compatibility table;
- no aesthetic punishment.

## 11. Restoration staging

Every meadow has authored stages such as:

### Dormant

- lower saturation;
- fewer ground details;
- sparse ambience;
- closed/limited flower life.

### Waking

- stronger ground color;
- first ambient insects/pollen;
- small landmark improvements.

### Growing

- more ground cover/flowers;
- richer ambience/music layer;
- player choices increasingly visible.

### Restored

- full authored color/vegetation target;
- strongest local bloom moment;
- richer fauna/ambience;
- player's chosen flower composition remains visible where the validated seed model allows it.

The state difference must be obvious in deterministic screenshots with HUD hidden.

## 12. Planet-level restoration

Completing required meadow/region restoration alters the meta planet visual.

The exact percentage model should move meaningfully after major work. Avoid tiny percentage changes that make a completed meadow feel numerically irrelevant.

The final 100% reward is primarily visual/world ownership, not another stat popup.

## 13. Environmental obstacles

Vertical-slice obstacles are navigation, not punishment:

Allowed:

- water edges;
- rocks/tree trunks;
- vines/restoration gates;
- narrow paths;
- gentle wind later if validated.

Excluded:

- lethal water;
- enemy damage;
- durability/resource theft;
- punishment hazards that contradict the cozy core.

## 14. Landmarks and orientation

Use landmarks to make compact spaces memorable and navigable:

- Hive/home tree;
- pond/creek;
- watering can reclaimed by flowers;
- stone arch;
- old garden sign;
- greenhouse ruin;
- windmill;
- glowing finale tree.

Landmarks should improve visually with surrounding restoration where feasible.

## 15. Ambient life

Ambient fauna communicates ecosystem recovery:

- butterflies;
- ladybugs;
- dragonflies near water;
- background birds;
- pollen/fireflies.

These are lightweight presentation actors, not simulation-heavy NPC systems in the vertical slice.

## 16. Content authoring workflow

For each new meadow/flower:

1. read `DECISIONS.md` and relevant feature research;
2. research problem-specific references when introducing a new player-facing pattern;
3. define stable data/IDs;
4. author minimal layout/prefab;
5. validate progression/economy references;
6. run navigation/readability test;
7. capture deterministic before/active/after states;
8. compare against reference and BeBee visual rules;
9. only then scale/duplicate the pattern.

## 17. Content acceptance criteria

A production meadow must have:

- obvious entrance/progression readability;
- no collision trap;
- no required interaction hidden by decoration;
- stable persistent IDs;
- authored restoration stages;
- validated objective targets;
- desktop + relevant mobile framing evidence;
- completion possible without unintended replay grind;
- player flower choices preserved safely where supported;
- approved reference/visual comparison evidence.
