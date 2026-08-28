# 04 — World & Content Design

## 1. World structure

BeBee uses an authored planet made from regions, not an infinite procedural world.

```text
Planet
 ├─ Region
 │   ├─ Meadow
 │   │   ├─ FlowerPatch
 │   │   ├─ FlowerPatch
 │   │   └─ UnlockGate / Landmark
 │   └─ Meadow...
 └─ Region...
```

Authoring the world gives us better pacing, visual composition, tutorial control and performance predictability than procedural generation.

---

## 2. Region design rules

Each region must have:

- a distinct color/biome identity;
- 4–8 compact meadows;
- 1–2 newly introduced flower species;
- at least one visible landmark;
- one modest navigation variation;
- a clear restoration finale;
- a seed reward or flower discovery that makes the region memorable.

A region should not introduce multiple unrelated systems at once.

---

## 3. Proposed planet progression

### Region 1 — Sunny Meadows

Purpose: teach the complete game.

Visuals:

- warm green grass;
- soft dirt paths;
- shallow creek;
- small hive/home tree;
- white/yellow/purple flower palette.

Flowers:

- Daisy;
- Clover;
- Lavender;
- Tulip;
- Lily finale.

Navigation idea: simple creek/bridge and blocked vine paths.

### Region 2 — Golden Fields

Purpose: increase scale and route planning.

Visuals:

- tall grass;
- wheat-like ground cover;
- amber afternoon lighting;
- windmill/old garden marker.

Flowers:

- Sunflower;
- Poppy;
- carried-over Tulip/Lily.

Navigation idea: patches arranged in larger open loops.

### Region 3 — Wetland Garden

Purpose: stronger spatial identity.

Visuals:

- ponds;
- reeds;
- stepping roots;
- reflected sky.

Flowers:

- Water Lily / Lotus;
- Iris;
- carried-over Lavender.

Navigation idea: narrow dry routes around water and island patches.

### Region 4 — Rosewood

Purpose: introduce richer aesthetic customization.

Visuals:

- forest edges;
- moss;
- shaded clearings;
- softer pink/red palette.

Flowers:

- Rose;
- Bluebell;
- Foxglove-like fictionalized species if needed for readability.

Navigation idea: curved woodland corridors and clearings.

### Region 5 — Alpine Bloom

Purpose: advanced pollination requirements.

Visuals:

- pale rock;
- snow edges;
- alpine grass;
- wind effects.

Flowers:

- Edelweiss-like alpine flower;
- Crocus;
- rare blue/purple species.

Navigation idea: elevation communicated visually but gameplay remains effectively 2D.

### Region 6 — Moon Garden

Purpose: finale and visual reward.

Visuals:

- dusk/night palette;
- glowing pollen;
- bioluminescent plants;
- restored planet vistas.

Flowers:

- Orchid;
- Moonflower;
- fictional exotic finale species.

Navigation idea: glowing bloom gates opened by overall restoration progress.

---

## 4. Meadow template

A typical meadow should fit mostly within a few camera screens and contain:

- entrance/reveal;
- 3–7 required patches;
- 0–2 optional decorative/replay patches;
- one visual focal point;
- one path toward future content;
- one safe space for customization viewing;
- minimal empty travel.

### Good layout

```text
Entrance
   ↓
Easy patch ── visible harder patch
   │                 │
Hive/path        soft gate
   │                 │
Easy patch ── medium patch
          ↓
     restoration focal point
```

The player should frequently see something they will be able to access soon.

---

## 5. First-region meadow specs

### M01 — First Patch

Role: tutorial.

- 3 Daisy patches.
- Hive within short travel distance.
- First Lily bud visible behind a decorative boundary but not interactable.
- No navigation obstacle.
- Completion unlocks Clover seeds and next meadow path.

### M02 — Clover Bend

Role: first choice and first customization demonstration.

- 4 patches.
- Mix Daisy/Clover.
- Curved path around a small stone/tree landmark.
- Restoring it enables seed replanting tutorial.

### M03 — Lavender Bank

Role: first soft gate.

- 4 patches.
- 2 easy, 2 Lavender.
- Player can attempt Lavender underpowered but sees slow progress.
- Buzz upgrade makes difference obvious.

### M04 — Creek Garden

Role: movement feel.

- 5 patches.
- Creek divides the meadow.
- Short bridge loop.
- Travel distance makes Flight upgrade attractive without requiring it.

### M05 — Tulip Rise

Role: mixed-tier efficiency.

- 5 patches.
- Tulips visually large and satisfying.
- Route forks so player chooses order.
- One optional replay/customization nook.

### M06 — Lily Clearing

Role: region climax.

- 6 patches.
- Final Lily cluster hard-gated by Buzz 3.
- Completion triggers the strongest region-scale restoration sequence.
- Lily seeds become permanent reward.
- Planet map expands/reveals Region 2 silhouette.

---

## 6. Flower content model

Each flower definition should contain data, not bespoke game logic unless necessary.

Suggested schema:

```lua
{
  id = "daisy",
  display_name_key = "flower.daisy",
  tier = 1,
  pollination_required = 3,
  base_honey = 10,
  min_buzz_level = 1,
  soft_gate = false,
  seed_unlock_cost = 0,
  palette_id = "daisy_white_yellow",
  patch_prefab = "/flowers/daisy/daisy_patch.collection",
  bloom_sfx = "daisy_bloom",
  tags = { "meadow", "starter" }
}
```

Do not encode progression by checking species names in scripts.

---

## 7. Flower roster principles

A new flower is worth adding when it contributes at least two of:

- new silhouette;
- new dominant color;
- new biome association;
- new difficulty tier;
- new reward/collection identity;
- new subtle pollination animation.

Avoid adding 30 near-identical flowers purely to inflate a collection list.

---

## 8. Native flowers vs planted flowers

Each patch has a **native flower** used for campaign difficulty and first restoration.

After meadow restoration:

- native challenge is considered completed permanently;
- player may replant an unlocked species;
- replant choice affects appearance and optional replay behavior, not campaign gate history.

This separation prevents customization from breaking progression rules.

---

## 9. Combination system

At meadow level, combinations already happen by planting different primary species into different patches.

Post-vertical-slice optional Accent system:

```text
Patch
  Primary: Lavender
  Accent: Daisy
```

Visual spawn ratio recommendation:

- primary 70–80%;
- accent 20–30%.

No negative compatibility table. Every unlocked flower can coexist unless art readability proves otherwise.

---

## 10. Restoration staging

Every meadow defines authored visual stages.

Example:

### Stage 0 — Dormant

- muted grass;
- closed buds;
- little ambient motion;
- sparse soundscape.

### Stage 1 — Waking

- stronger grass color;
- a few butterflies/pollen particles;
- subtle music layer added.

### Stage 2 — Growing

- ground flowers/grass tufts increase;
- landmark visually improves;
- more ambient insects.

### Stage 3 — Restored

- full color;
- all required flowers open;
- restoration burst;
- richer ambience;
- customization becomes available.

The change should be obvious in screenshots before/after.

---

## 11. Planet-level restoration

Completing regions should alter the meta planet visual.

At 0%:

- mostly muted surface;
- a few dim regions.

At milestones such as 25/50/75/100%:

- colored areas expand;
- cloud/atmosphere treatment becomes warmer;
- tiny visible bloom patterns appear;
- final completion gives a unique planet-scale bloom animation.

The final reward is primarily visual ownership, not a stat popup.

---

## 12. Environmental hazards

MVP has obstacles, not punishment hazards.

Allowed:

- water edges;
- rocks;
- tree trunks;
- vines/gates;
- narrow paths;
- wind zone later that gently affects steering.

Not in MVP:

- damage spikes;
- enemies;
- lethal water;
- durability loss;
- resource theft.

---

## 13. Landmarks

Landmarks help orientation and emotional memory.

Examples:

- home hive tree;
- little pond;
- abandoned watering can reclaimed by flowers;
- stone arch;
- old garden sign;
- tiny greenhouse ruin;
- windmill;
- glowing moon tree.

Landmarks should become prettier as surrounding restoration progresses.

---

## 14. Ambient life

Ambient fauna communicates ecosystem recovery.

Progressive additions:

- butterflies;
- ladybugs;
- tiny birds in background;
- dragonflies near water;
- floating pollen;
- fireflies in late/night regions.

These are visual actors, not simulation-heavy NPC systems in MVP.

---

## 15. Art production constraints

Every gameplay flower needs:

- closed/bud state;
- 2–3 intermediate bloom states or equivalent animation;
- full bloom state;
- readable patch arrangement;
- icon/seed card illustration;
- optional accent-compatible version later.

Every patch must remain readable when partially obscured by particles/UI.

---

## 16. Content authoring workflow

1. define flower data;
2. create patch prefab/collection;
3. place in meadow collection;
4. assign stable patch IDs;
5. define unlock requirement;
6. define reward;
7. author restoration stage effects;
8. run economy validation;
9. run navigation/readability playtest;
10. capture before/after screenshots for review.

No meadow ships with auto-generated IDs that can change and corrupt saves.

---

## 17. Content acceptance criteria

A finished meadow must have:

- obvious entrance and progression direction;
- no collision trap;
- no required patch hidden by decoration;
- at least one visually satisfying vista/focal area;
- patch rewards defined in data;
- save IDs stable;
- restoration stages authored;
- objective marker targets assigned;
- desktop and portrait-mobile framing checked;
- completion reachable without grind outside intended progression.
