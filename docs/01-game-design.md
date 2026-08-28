# 01 — Game Design Specification

## 1. Moment-to-moment gameplay

BeBee is a top-down 2D movement game. The player directly controls a bee moving through compact meadows. Flower patches are world objects with a clear pollination state.

The core verb is **pollinate**.

The player should spend most active playtime doing one of four things:

1. moving toward a visible objective;
2. pollinating a patch;
3. collecting the resulting honey feedback;
4. choosing an upgrade/seed/unlock.

Menus are support surfaces, not the game itself.

---

## 2. Controls

### Desktop

- `WASD` / arrow keys — move.
- Mouse movement does not steer the bee.
- `E` / Space — optional explicit interact fallback where needed.
- `Esc` — pause/settings.
- Mouse/touch click on HUD elements only; world interaction should not require precision clicking during normal movement.

### Mobile

- Floating virtual joystick on lower-left.
- Pollination is automatic when the player deliberately enters an active patch radius and remains near flowers.
- UI buttons occupy lower-right/top edges without overlapping joystick travel.

### Why auto-pollination

Cow Bay succeeds with extremely direct interaction, but BeBee's fantasy is movement through flowers. Requiring repeated taps on individual blossoms would turn flying into cursor work. BeBee therefore keeps the competitor principle (“one obvious action”) while adapting it to the bee: movement itself initiates pollination.

---

## 3. Bee movement

### Feel target

Movement must feel smooth, light and slightly elastic rather than grid-based.

Required behavior:

- acceleration to target velocity rather than instant teleport-like velocity changes;
- short deceleration when input is released;
- subtle body lean into movement direction;
- wing animation rate responds to movement state;
- tiny squash/pop on patch completion;
- no collision snagging on decorative flowers;
- collision only against meaningful terrain boundaries/obstacles.

### Initial tuning values

These are starting values, not sacred balance:

- base speed: `180 world units/s`;
- acceleration time to ~90% speed: `0.12–0.18 s`;
- deceleration time: `0.08–0.15 s`;
- camera follow smoothing: `0.12–0.20 s`;
- pollination activation grace after entering radius: `0.10 s`;

Movement speed upgrades should be felt immediately but should not make steering frustrating.

---

## 4. Flower patch model

The atomic progression object is a **FlowerPatch**, not an individual decorative flower.

A patch contains multiple visible flower sprites but has one gameplay progress meter.

### Patch states

```text
LOCKED
  -> AVAILABLE
  -> POLLINATING
  -> BLOOMED
  -> CUSTOMIZABLE
```

Optional presentation sub-state:

```text
BLOOMED -> CELEBRATING -> CUSTOMIZABLE
```

### Patch data

Each patch has at minimum:

- `patch_id`
- `native_flower_id`
- `difficulty_tier`
- `pollination_required`
- `base_honey_reward`
- `unlock_rule`
- `seed_slots`
- `visual_stage_count`
- `completion_flags`

### Interaction

When the bee is inside the active patch radius:

1. the patch gets a soft outline/glow;
2. pollination progress begins automatically;
3. small pollen particles travel between bee and flowers;
4. flowers open progressively rather than all at once;
5. a compact progress ring/bar appears near the patch, not in the center of the screen;
6. on completion, all remaining buds bloom in a short celebration;
7. honey droplets/icons stream toward the honey HUD counter;
8. regional restoration visuals update.

Leaving the patch pauses progress; progress does **not** reset.

This lets players move naturally and avoids punishing accidental exits.

---

## 5. Pollination formula

The simulation should use a transparent data-driven relationship:

```text
progress_per_second = base_pollination_rate * buzz_multiplier * situational_multiplier
```

For MVP:

- `base_pollination_rate = 1.0`
- `buzz_multiplier` comes from permanent Buzz level.
- `situational_multiplier = 1.0` unless a future flower/biome modifier is explicitly introduced.

Completion time:

```text
seconds_to_complete = pollination_required / progress_per_second
```

Do not create hidden random failure chance.

### Difficulty target

A patch at the player's intended tier should generally take:

- early game: 2–5 seconds;
- mid progression: 3–7 seconds;
- high-tier showcase patch: up to ~10 seconds before upgrades;

Longer stationary holds become boring. Difficulty should come from a sequence/route of patches and power gating, not 30-second progress bars.

---

## 6. Flower difficulty

Difficulty tier controls two things:

1. how much pollination work is required;
2. the recommended/minimum Buzz level.

MVP example:

| Tier | Example | Player message | Intended behavior |
|---|---|---|---|
| 1 | Daisy / Clover | no warning | fast and welcoming |
| 2 | Lavender / Tulip | “Buzz 2 recommended” | possible but slower at low level |
| 3 | Lily | “Buzz 3 required” | hard gate for progression clarity |

Use a mix of **soft gates** and **hard gates**:

- soft gate: player can pollinate, but inefficiently;
- hard gate: patch remains closed with a clear upgrade requirement.

Do not use only hard gates; seeing progress on a difficult flower creates aspiration.

---

## 7. Honey reward

Honey is awarded at meaningful completion boundaries, not every simulation tick.

Default:

```text
honey_reward = round(base_honey_reward * yield_multiplier * optional_combo_bonus)
```

Feedback sequence:

1. flowers bloom;
2. honey reward number appears near the patch;
3. honey droplets arc toward HUD;
4. HUD number counts upward quickly;
5. if the amount enables an affordable upgrade, the hive/upgrade affordance subtly pulses once.

Never block control while reward animation finishes.

---

## 8. Upgrade interaction

The Hive is the home/upgrade location for MVP.

Entering its interaction radius reveals a single clear button/affordance: **Improve Bee**.

Upgrade screen contains three large cards:

- Flight;
- Buzz;
- Yield.

Each card shows:

- icon;
- current level;
- one-line effect;
- next numeric improvement;
- honey cost;
- buy button/state.

No skill tree in MVP.

When an upgrade is bought:

- honey counter animates down;
- bee gives a short reaction;
- stat card animates once;
- if an upgrade unlocks a hard-gated flower, show a concise “Lilies are now pollinatable” toast.

---

## 9. Meadow restoration

A meadow contains several patches and has a restoration meter.

Example six-patch MVP meadow:

```text
0/6  sparse grass, muted ambience
2/6  greener grass, first ambient insects
4/6  richer ground cover, stronger music layer
6/6  full bloom event + seed customization unlocked
```

The exact visual changes should be authored rather than purely percentage-based so the transformation is readable.

Completing every required native patch marks the meadow **Restored**.

---

## 10. Seed customization

After a meadow is restored, its patches become customizable.

### Core rule

A player can replace a restored patch's native flower with an owned seed type.

Flow:

1. approach restored patch;
2. interaction says `Plant` / shows current flower;
3. seed selector opens as a small bottom sheet/panel;
4. choose an owned/unlocked seed;
5. short planting transition (soil swirl / seed pop);
6. patch becomes buds of the chosen species;
7. bee pollinates it once to establish the new bloom;
8. meadow permanently displays that flower until changed again.

### Seed slots and combinations

MVP should support composition without arbitrary tile editing.

Each customizable patch has:

- **Primary flower** — main visual species;
- optional **Accent flower** slot introduced after the vertical slice if performance/readability is good.

Region-level flower diversity bonuses may be added later, but customization must not punish aesthetics. If bonuses exist, they should be small and visible.

### Replant cost

The player buys seed unlocks/seed packets with honey. Replanting should either be free after permanent species unlock or consume a cheap packet. Vertical-slice recommendation: **permanent seed unlock + free replanting** so experimentation is encouraged.

---

## 11. Objectives

BeBee uses a lightweight objective strip rather than a traditional quest log.

Examples:

- `Pollinate 3 daisy patches · 1/3`
- `Improve Buzz to level 2`
- `Restore Sunny Meadow · 4/6`
- `Plant your first lavender patch`

Only one primary objective is pinned at a time. Optional secondary objectives can exist later.

Objectives guide the player through the loop but should mostly reward actions the player already wants to perform.

---

## 12. Unlocking space

New space should be visible before it is available whenever possible.

A blocked path can use:

- thick unbloomed vines;
- sleepy giant bud;
- dry bridge roots;
- fog/pollen cloud;

Unlock requirements should be simple:

- restore X patches;
- reach Buzz level Y;
- pay a modest honey amount;

Avoid compound requirements such as “17 daisies + 4 seeds + level 6 + 300 honey.”

Unlock animation must physically change the world and reveal the new route.

---

## 13. World map and planet goal

The local game is continuous meadow exploration. The meta view is a simple planet/region map.

Map displays:

- current region;
- restored regions;
- next region silhouette;
- overall planet bloom percentage;
- flower species discovered.

The map is not an open-world teleport menu during the first minutes. It becomes available after the player restores the tutorial meadow.

---

## 14. Tutorial sequence

Target: teach the complete premise in ~3 minutes without a tutorial modal stack.

### Beat 1 — Move

- Bee starts beside a visibly pulsing daisy patch.
- Small prompt: `Fly to the flowers`.
- Input hints appear contextually.

### Beat 2 — Pollinate

- Entering patch starts automatic progress.
- Prompt disappears immediately after activation.
- Patch blooms and awards first honey.

### Beat 3 — Repeat

- Two nearby patches become highlighted one after another.
- No new text unless player is inactive.

### Beat 4 — Upgrade

- Hive pulses.
- Objective: `Improve your Buzz`.
- Player has exactly enough honey for first upgrade.

### Beat 5 — Aspirational flower

- A higher-tier flower sits near the path.
- Before upgrade it is inefficient/locked; after upgrade it becomes practical.

### Beat 6 — Restore

- Final patch completes the meadow.
- Strong bloom celebration.

### Beat 7 — Choose

- Player receives/unlocks a second seed species and replants one restored patch.

### Beat 8 — Reveal planet

- Map view reveals many gray regions and shows first progress percentage.
- Objective becomes `Make the planet bloom`.

---

## 15. Feedback stack

Every pollination completion should combine at least three feedback channels:

- animation;
- particles;
- audio;

Optional mobile haptic: one light pulse on patch completion, stronger pulse on meadow restoration.

Do not spam screen shake. The bee is small and cozy; feedback should feel crisp, not explosive.

---

## 16. No-frustration rules

- Patch progress never decays while the player is away.
- Replanting is reversible.
- Permanent upgrades cannot be misallocated because there are only beneficial linear tracks.
- No currency is lost on quit/death because MVP has no death.
- If the player lacks requirements, the UI says exactly what is missing.
- Objective guidance uses arrows/world highlights; do not forcibly pan the camera away from the bee.
- A player can always return to the hive/map without traversing an unnecessarily long empty route.

---

## 17. Vertical-slice content

One region, six meadows:

1. **First Patch** — daisies, tutorial.
2. **Clover Bend** — introduces route choice and seed unlock.
3. **Lavender Bank** — first soft difficulty gate.
4. **Creek Garden** — movement around water/bridge geometry.
5. **Tulip Rise** — combines tier 1/2 patches and stronger economy decision.
6. **Lily Clearing** — first hard Buzz gate and region finale.

A region should be completable in roughly 25–45 minutes during balancing, then adjusted using playtest data.

---

## 18. Future systems that are compatible but not required

Only after vertical-slice validation:

- friendly helper insects;
- bee cosmetics;
- regional weather;
- special flower combos;
- rare decorative seeds;
- light idle/offline hive production;
- seasonal regions;
- optional challenge meadows;
- local collections/flower journal.

None of these should be implemented before the core loop proves fun.
