# 08 — Reference Analysis

This document records the product/engineering references used to shape BeBee. It distinguishes reusable **patterns** from copyrighted/proprietary implementation and content.

Research snapshot: 2026-08-28.

---

## 1. Cow Bay — primary interaction reference

Developer: 7Spot Games  
Poki: https://poki.com/en/g/cow-bay  
Google Play: https://play.google.com/store/apps/details?id=com.sevenspotgames.cowbay  
App Store: https://apps.apple.com/us/app/cow-bay/id6446347428

### Observed product structure

Cow Bay starts with extremely basic gathering — berries and logs — then evolves into cutting trees, sowing seeds and crafting equipment. Quests from the governor push the player forward. Coins unlock additional islands and new facilities such as crafting benches, campfire and storage. Individual actions consume energy. Poki describes world interaction as tapping/clicking an object to harvest/use it.

### What BeBee should learn from it

- first meaningful action happens immediately;
- complexity is layered rather than dumped at the beginning;
- small local tasks point toward a visible larger settlement/world goal;
- new areas introduce new capability/content;
- interaction is intentionally simple enough for desktop and mobile;
- one pinned objective is sufficient to pull the player through early progression;
- world objects themselves are the main interaction surface.

### What BeBee changes

- movement + proximity becomes the primary interaction because flying through flowers fits the fantasy better than clicking individual objects;
- no crafting tree in MVP;
- one honey currency instead of resource/crafting inventory;
- no hard action-energy system in MVP;
- player customization is about what flowers the restored planet contains.

### What must not be copied

- cow/cat characters;
- exact maps/islands;
- UI assets/layout pixel-for-pixel;
- quest text;
- sounds;
- proprietary code/data/economy values.

---

## 2. Cow Castle — area unlock and direct movement reference

Developer: 7Spot Games  
Poki: https://poki.com/en/g/cow-castle

### Observed product structure

The player controls a cow with WASD/arrow movement, gathers wood/stone, constructs a castle, earns coins and unlocks new locations/facilities.

### Useful patterns

- character movement can remain the only required control in a casual production loop;
- resources directly feed visible world construction;
- location unlocks create short-range aspiration;
- the long-term goal is concrete and visual: build the castle.

### BeBee translation

```text
Cow Castle: gather -> build -> unlock castle/world
BeBee:      pollinate -> honey -> improve/unlock -> bloom planet
```

The equivalent of castle construction is ecosystem restoration.

---

## 3. Olly the Paw — simple macro-goal reference

Developer: 7Spot Games  
Poki: https://poki.com/en/g/olly-the-paw

### Observed product structure

A cute bear gathers apples and other materials, sells products, upgrades skills, gains helper support and repairs an airplane piece by piece. New areas are unlocked as the player advances.

### Useful patterns

- give the entire game one sentence-level objective;
- show progress toward that macro objective physically;
- introduce helpers/automation only after the player understands the manual loop;
- cute characters can carry a straightforward economy without heavy narrative.

### BeBee translation

Macro objective:

> Cover the whole planet in flowers.

The planet restoration view is BeBee's equivalent of the gradually repaired airplane.

---

## 4. Elixpur Idle — automation reference, not MVP requirement

Developer: 7Spot Games  
Poki: https://poki.com/en/g/elixpur-idle

### Observed product structure

Players accelerate mushroom growth, helpers harvest, ingredients feed potion production, profits upgrade the operation and potion quality.

### Useful lesson

Automation can extend a proven manual loop later.

### BeBee implication

A future helper-insect system could tend/re-bloom restored meadows or generate small optional honey income, but **only after active pollination is fun**. Do not start BeBee as an idle automation game.

---

## 5. My Little Universe — world-restoration and spatial progression reference

Developer/publisher ecosystem: Estoty / SayGames  
Official: https://say.games/games/my-little-universe/

### Observed product structure

The player gathers resources, upgrades tools/equipment and expands/terraform worlds. SayGames describes the mobile hit as having tens of millions of players and emphasizes turning a small sterile area into a large developed planet. Resources and upgraded tools are the engine of access to new areas.

### Useful patterns

- the next locked world chunk is often physically visible;
- power upgrades reduce friction against stronger resource nodes;
- spatial expansion makes economic progress tangible;
- world transformation is more emotionally legible than a number alone;
- later biomes can reuse the same fundamental verbs with different visual/content layers.

### BeBee translation

- Buzz replaces tool strength;
- flower tier replaces resource hardness;
- honey replaces the multi-resource economy in MVP;
- blooming terrain replaces terraforming/build construction;
- regions replace planets/worlds at the first production scale.

### Critical simplification

Do not import My Little Universe's large resource/tool matrix. BeBee's differentiation is a much cleaner one-currency ecosystem restoration loop.

---

## 6. Dreamdale — upgrade readability and anti-pattern reference

Google Play: https://play.google.com/store/apps/details?id=com.dream.dale  
App Store: https://apps.apple.com/us/app/dreamdale-fairy-adventure/id1517564300

### Observed product structure

Dreamdale uses gathering, tool upgrades, buildings, map expansion, storage, helpers, quests/XP and multiple islands. It demonstrates how upgrades can create clearer efficiency gains and how new spaces introduce new resources.

### Useful patterns

- player upgrades should visibly change gathering efficiency;
- map expansion should introduce fresh visual/resource identity;
- storage/automation can be layered after the manual loop;
- clear quest progression can guide a complex economy.

### Anti-pattern to avoid

App Store feedback includes complaints about aggressive objective camera movement that pulls the camera away and back, causing disorientation. BeBee therefore uses edge arrows/world highlights and explicitly forbids routine camera stealing for guidance.

Also avoid expanding the economy until the core loop becomes a chore that requires excessive upgrade materials. BeBee's economy should remain progression-supporting rather than grind-producing.

---

## 7. Forager — compact systems feeding expansion

Steam: https://store.steampowered.com/app/751780/Forager/

### Observed structure

Forager is a 2D open-world gathering/crafting/progression game where resource collection feeds base growth, land purchase and skill/equipment progression.

### Useful patterns

- small spaces can become compelling when resources, upgrades and expansion reinforce each other;
- land itself can be a progression reward;
- a compact core loop can support completionist goals;
- visible future land creates motivation.

### BeBee difference

Do not recreate crafting/building complexity. Use the compact spatial-progression lesson only.

---

# Open-source implementation references

## 8. PurrNet Incremental Sample

Repository: https://github.com/PurrNet/PurrNet-Incremental-Sample  
Guide: https://github.com/PurrNet/PurrDocs/blob/main/full-game-guides/incremental-game-sample.md  
License: MIT at research time.

### Relevant implementation ideas

The sample demonstrates a complete incremental loop:

- resource nodes with health;
- harvest interaction;
- dropped loot;
- inventory/base handoff;
- upgrades;
- layer-based resource spawning;
- object pooling;
- state-machine-driven player behavior.

Upgrade examples include movement speed, damage, dash distance, inventory space and yield per tree.

### What BeBee should borrow conceptually

- upgrades defined as data rather than hard-coded screen logic;
- resource/patch state isolated from player control;
- spawn/effect pooling where it genuinely matters;
- explicit player behavior states when complexity warrants them;
- complete end-to-end loop before broad content production.

### What BeBee should not borrow

- PurrNet networking dependency;
- Unity architecture;
- multiplayer ownership model;
- wood/inventory/base loop literally.

BeBee is single-player Defold in MVP.

---

## 9. defold-games

Repository: https://github.com/benjames-171/defold-games  
License: MIT at research time.

A large collection of complete small 2D Defold games. It is useful as a code-organization and engine-usage reference.

Important research note: the repository warns that Defold engine changes can break older samples. Do not cargo-cult old APIs; verify against current Defold documentation.

Use cases:

- inspect small scene/controller patterns;
- input handling examples;
- GUI patterns;
- animation/state organization;
- build/project layout inspiration.

Do not bulk-copy unrelated systems into BeBee.

---

## 10. Godot Valley / other farming repositories

Example: https://github.com/RezaTaheri01/godot-valley

Useful only as a conceptual reference for:

- farming/foraging decomposition;
- tool/upgrade ideas;
- save/load concerns;
- HUD/inventory questions.

BeBee is not adopting Godot as its engine. Cross-engine code should not be pasted into the project.

---

# Defold official references

## 11. Engine repository

https://github.com/defold/defold

Defold is free to use and supports desktop, mobile and web targets. Current engine/version compatibility must be checked before implementation dependencies are pinned.

## 12. Input

https://defold.com/manuals/input/

Relevant facts:

- keyboard, mouse, touch and gamepads are supported;
- raw device input is mapped to named actions through project-wide input bindings;
- scripts/GUI scripts receive actions through `on_input()` after acquiring focus.

BeBee uses semantic input actions and keeps gameplay independent of raw input devices.

## 13. GUI

https://defold.com/manuals/gui/

Defold GUI is rendered independently from the camera view and provides layout tools suitable for resolution/aspect-ratio adaptation.

BeBee uses GUI scenes for HUD/menu surfaces and world objects for local gameplay affordances.

## 14. Collection proxies

https://defold.com/manuals/collection-proxy/

Collection proxies allow separate game worlds/collections to be dynamically loaded/unloaded.

BeBee uses this concept for region/major-screen lifecycle rather than keeping every region active.

## 15. Save API

https://defold.com/ref/sys-lua/#sys.save

`sys.save()` / `sys.load()` plus `sys.get_save_file()` provide the local-save foundation. BeBee adds its own versioning, validation, migration and backup layer around them.

## 16. Profiling

https://defold.com/manuals/profiling/

Defold provides runtime profiling tools and can expose HTML5 profiling information through browser performance tooling. BeBee's performance work should be measurement-driven.

## 17. HTML5/platform manuals

https://defold.com/manuals/

The Defold manual index includes HTML5 development and platform SDK extensions, including Poki/CrazyGames integrations. Distribution SDKs should be added behind a platform adapter only when the core game is already validated.

---

# Decision summary

| Question | Decision |
|---|---|
| Primary reference fantasy | Cow Bay simplicity + planet restoration |
| Engine | Defold |
| Runtime language | Lua |
| Main interaction | movement + proximity auto-pollination |
| Currency | Honey only in MVP |
| Primary upgrades | Flight / Buzz / Yield |
| Difficulty | flower tiers + soft/hard Buzz gates |
| World progression | authored regions/meadows |
| Customization | permanent seed unlocks + reversible planting |
| Combat | not core / excluded from MVP |
| Hard energy timer | excluded from MVP |
| Multiplayer | excluded from MVP |
| Save | versioned local with backup/migrations |
| UI philosophy | sparse HUD, shallow task-specific menus |
| Guidance | objective strip + world markers, no routine camera stealing |
| Open-source reuse | compatible-license code only after explicit review |

---

# Reference-use rule

When implementing a feature from a reference:

1. state the player problem being solved;
2. identify the pattern, not the competitor's exact asset/layout/code;
3. implement it using BeBee's own content and architecture;
4. verify third-party code/assets separately for license compatibility;
5. record any imported asset/library in `THIRD_PARTY.md`.

If the only justification for a feature is “the competitor has it,” that is not enough. The feature must strengthen BeBee's core loop.
