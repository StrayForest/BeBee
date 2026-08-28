# 00 — Product Vision

## Working title

**BeBee**

## One-sentence pitch

A cozy 2D progression game where a tiny bee pollinates increasingly difficult flower meadows, earns honey, improves itself, replants restored land with chosen flowers, and gradually turns an empty planet into a living garden.

## Player fantasy

The player should feel three things repeatedly:

1. **I am useful.** The bee makes dead/empty land bloom.
2. **I am getting stronger.** Previously slow or inaccessible flowers become easy.
3. **This world is becoming mine.** The restored planet reflects the player's seed choices.

The fantasy is not “farm spreadsheet management.” It is “I fly around and make the planet beautiful.”

## Audience

Primary:

- casual players who like Cow Bay, Olly the Paw, My Little Universe, Dreamdale, Forager-like gathering loops and cozy restoration;
- players comfortable with short 5–20 minute sessions;
- desktop browser and mobile users;
- broad age suitability; no dependence on reading-heavy narrative.

Secondary:

- completionists who want 100% planet restoration;
- decorators/customizers who care which flowers cover each meadow;
- efficiency players who enjoy optimizing upgrades and routes.

## Product pillars

### P1 — Immediate readability

Within the first 20 seconds, a player must understand:

- “I am the bee.”
- “Those flowers need pollination.”
- “Doing that gives honey.”
- “Honey lets me become better.”
- “Better bee = harder/new meadows.”

No opening lore dump and no tutorial window longer than one short sentence.

### P2 — Satisfying transformation

Every meadow starts visually incomplete: sparse buds, muted soil, closed flowers, low insect life. Pollination transforms it in stages. Completion creates a strong final “bloom” moment: color, petals, particles, ambience and small fauna return.

Progress must be visible in the world without opening a menu.

### P3 — Simple power progression

The bee improves along a small number of understandable axes. MVP uses three permanent tracks:

- **Flight** — movement speed;
- **Buzz** — pollination power / time to complete flower nodes;
- **Yield** — honey earned from completed pollination.

A fourth stat, **Reach** (pollination interaction radius), is reserved for later only if playtests show it improves feel rather than trivializes movement.

### P4 — Player-authored restoration

Native flowers define each meadow's initial challenge, but after restoration the player can buy seeds and redesign that meadow.

Customization has three rules:

- it is easy to understand;
- changing flowers is reversible;
- the player never permanently ruins progression by choosing “wrong” seeds.

### P5 — One planet, obvious long-term goal

The main meta-goal is a planet restoration percentage from 0% to 100%.

The planet is divided into regions; regions contain compact meadows. Each completed meadow fills the regional and planetary restoration meter. New regions introduce harder flowers, new seed families and visual biomes.

## Core loop

```text
Explore meadow
  -> pollinate available flowers
  -> complete patch
  -> receive honey
  -> spend honey on bee upgrades and/or seeds
  -> access harder patches
  -> restore meadow
  -> choose/replant flower composition
  -> unlock next meadow/region
  -> increase planet restoration %
```

This loop is intentionally closer to proven casual gather/upgrade/unlock structures than to a farming simulator.

## Session loop

A normal short session should provide at least one of these outcomes:

- finish a patch;
- buy an upgrade;
- unlock a meadow;
- plant a new flower combination;
- finish a region milestone;
- discover a new flower species.

The player should rarely leave a session with “nothing changed.”

## Emotional curve

1. **Curiosity:** gray/sparse world, obvious nearby daisies.
2. **Pleasure:** first flowers open rapidly and honey pops toward the HUD.
3. **Agency:** first upgrade makes movement/pollination visibly better.
4. **Aspiration:** player sees lilies or another high-tier flower that is currently inefficient/locked.
5. **Mastery:** upgrade makes that formerly difficult patch manageable.
6. **Ownership:** player replants the finished meadow with preferred seeds.
7. **Scale:** camera/map reveals that this is one small part of a whole planet.

## Tone and art direction

- soft, rounded silhouettes;
- friendly saturated colors against initially muted terrain;
- readable shapes rather than detailed realism;
- expressive bee animation: wing speed, squash/stretch, tiny turn lean, happy completion reaction;
- flowers should be recognizable by silhouette and color family;
- no visual clutter around interactable patches;
- restoration should visibly increase biodiversity: butterflies, ladybugs, ambient pollen motes and richer grass appear progressively.

The game should look “toy-like and alive,” not like a UI-heavy management game.

## Difficulty philosophy

Difficulty is **efficiency friction**, not punishment.

A harder flower can require more pollination work and/or a minimum Buzz tier. The game should not kill the bee, destroy currency or force retries in MVP.

Failure states are not required for engagement. The tension comes from seeing desirable content slightly ahead of current power.

## Currency philosophy

MVP has **one economy currency: honey**.

Honey pays for:

- permanent bee upgrades;
- seeds;
- selected meadow unlocks/bridges if needed for pacing.

Do not introduce coins, gems, pollen tokens or tickets during MVP unless metrics demonstrate a concrete need.

## What we deliberately borrow as patterns

From Cow Bay / other 7Spot games:

- immediate resource interaction;
- short objective chains;
- unlockable compact areas;
- visible progression from basic to more complex tasks;
- readable single-screen objectives;
- broad desktop/mobile accessibility.

From My Little Universe / Dreamdale:

- show future gated content near current play;
- improve gathering efficiency with permanent upgrades;
- spatial progression through unlockable world chunks;
- world restoration/construction as a visual reward.

From Forager-like loops:

- gathering should naturally feed expansion;
- the map itself communicates progress;
- a small set of systems can recombine into long-term goals.

From open incremental samples:

- data-driven upgrade definitions;
- modular resource node logic;
- clear separation of player state, resources, rewards and spawning.

## What we explicitly do not copy

- proprietary source code;
- exact maps;
- Cow Bay characters, UI art, text, quest wording, sounds or sprites;
- competitor economy values;
- pixel-perfect screen layouts;
- forced ad cadence or monetization patterns before gameplay is proven.

We use observed interaction conventions because they are familiar, but BeBee must have original content and implementation.

## MVP scope

### Included

- 1 biome/region;
- 6 meadows;
- 3 native difficulty tiers;
- 4 seed species;
- 3 permanent upgrade tracks;
- 1 hive upgrade screen;
- region map/progress screen;
- save/load;
- sound and VFX pass;
- keyboard + touch controls;
- basic settings/accessibility;
- analytics event layer;
- production HTML5 build.

### Excluded

- multiplayer;
- combat;
- complex crafting;
- NPC worker automation;
- social systems;
- backend account system;
- premium currency;
- battle pass;
- daily streak pressure;
- procedural world generation;
- user-generated arbitrary terrain editing.

## Product success criteria for the vertical slice

Before producing the rest of the planet, the slice must demonstrate:

- first-time players can identify what to do without external instruction;
- pollination feels satisfying for repeated actions;
- an upgrade produces an obvious improvement;
- players understand why a harder patch should be revisited later;
- seed customization is discoverable and reversible;
- the meadow restoration before/after difference is emotionally noticeable;
- the game performs smoothly in target desktop and representative mobile browsers;
- save/load survives refresh/relaunch without progression loss.

## North-star design question

For every proposed feature ask:

> Does this make flying, blooming, upgrading, choosing flowers or restoring the planet more satisfying?

If not, it probably does not belong in the first release.
