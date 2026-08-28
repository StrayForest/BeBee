# 02 — Progression & Economy

## 1. Economy goals

The economy exists to support one readable decision:

> Spend honey now to become better at pollinating, or spend some of it to make restored land look the way I want.

MVP uses one currency: **Honey**.

No secondary premium currency, XP currency, energy currency or crafting resource is required for the first release.

---

## 2. Honey sources

Primary source:

- completing a flower patch.

Secondary milestone sources:

- restoring a meadow;
- completing the first-time discovery of a flower species;
- finishing a region.

Avoid faucets that bypass gameplay, such as passive login rewards, until the active loop is validated.

---

## 3. Honey sinks

MVP sinks:

1. permanent bee upgrades;
2. permanent seed unlocks;
3. optional area gates when pacing needs them.

The dominant sink should be bee upgrades. Seeds are important but should not make a player regret customizing the world.

Recommended spend share during normal first-region progression:

- 65–80% upgrades;
- 15–30% seeds/customization;
- 0–15% world unlock gates.

This is a balancing target, not a hard accounting rule.

---

## 4. Bee stats

### Flight

Effect: movement speed.

Design purpose:

- reduces travel friction;
- creates an immediately perceptible upgrade;
- makes later, larger meadows comfortable.

Suggested multiplier curve:

| Level | Speed multiplier |
|---:|---:|
| 1 | 1.00x |
| 2 | 1.10x |
| 3 | 1.20x |
| 4 | 1.30x |
| 5 | 1.40x |
| 6 | 1.50x |
| 7 | 1.60x |
| 8 | 1.70x |

Do not push normal movement much above ~1.7x base without retuning camera/collision.

### Buzz

Effect: pollination progress per second and hard-gate eligibility.

Suggested multiplier curve:

| Level | Power multiplier | Typical flower access |
|---:|---:|---|
| 1 | 1.00x | Daisy, Clover |
| 2 | 1.35x | Lavender |
| 3 | 1.70x | Tulip, Lily entry |
| 4 | 2.10x | Sunflower |
| 5 | 2.55x | Bluebell / Rose |
| 6 | 3.05x | Lotus |
| 7 | 3.60x | Orchid |
| 8 | 4.20x | late-game exotic flowers |

Buzz is the main progression gate.

### Yield

Effect: honey reward multiplier.

Suggested curve:

| Level | Honey multiplier |
|---:|---:|
| 1 | 1.00x |
| 2 | 1.12x |
| 3 | 1.25x |
| 4 | 1.40x |
| 5 | 1.56x |
| 6 | 1.73x |
| 7 | 1.91x |
| 8 | 2.10x |

Yield should compound progression without making old content absurdly profitable relative to new regions.

---

## 5. Upgrade costs

Use authored tables for shipped balance, even if a formula generates the starting proposal.

Starting formula:

```text
cost(level -> level+1) = round(base_cost * growth^(level-1))
```

Initial parameters:

| Track | Base cost | Growth |
|---|---:|---:|
| Flight | 30 | 1.85 |
| Buzz | 35 | 1.95 |
| Yield | 40 | 1.90 |

Example approximate early costs:

| Purchase | Flight | Buzz | Yield |
|---|---:|---:|---:|
| L1 -> L2 | 30 | 35 | 40 |
| L2 -> L3 | 56 | 68 | 76 |
| L3 -> L4 | 103 | 133 | 144 |
| L4 -> L5 | 190 | 259 | 274 |

Final values must be tuned from telemetry/playtests; formulas are scaffolding.

---

## 6. Flower progression

Flower species are both content and difficulty vocabulary.

### Proposed global ladder

| Tier | Species examples | Pollination required | Base honey | Buzz gate |
|---:|---|---:|---:|---:|
| 1 | Daisy, Clover | 3–5 | 8–12 | 1 |
| 2 | Lavender, Tulip | 7–10 | 16–24 | 2 soft |
| 3 | Lily, Sunflower | 12–16 | 30–42 | 3 |
| 4 | Rose, Bluebell | 18–24 | 50–70 | 4 |
| 5 | Lotus, Hibiscus | 28–36 | 85–115 | 5 |
| 6 | Orchid, rare alpine/exotic species | 40–52 | 135–180 | 6+ |

These values are deliberately compact. A flower patch should resolve in seconds, not become an idle bar.

### Species identity

Difficulty should not be communicated only by numbers. Each family needs an easy visual/behavior cue.

Examples:

- Daisy — tiny, quick opening chain.
- Clover — many small heads, dense patch.
- Lavender — long stems light sequentially.
- Tulip — fewer large buds, strong pop animation.
- Lily — large closed blossoms, strong Buzz-gate icon.
- Sunflower — broad ring; rotates toward the bee as progress rises.

Mechanical differences should remain mild in MVP. Do not create a bespoke minigame for every flower.

---

## 7. First-region balance proposal

The first region should teach the economy without grind.

### Meadow 1 — First Patch

- 3 Daisy patches.
- Base rewards: 10 / 10 / 15 honey.
- Total: 35.
- First Buzz upgrade costs 35.
- Player is intentionally able to purchase it immediately.

### Meadow 2 — Clover Bend

- 4 patches: Daisy, Clover, Clover, Daisy.
- Total base honey target: ~55–65.
- First seed unlock is introduced at ~20 honey.

### Meadow 3 — Lavender Bank

- 4 patches, including first Tier 2.
- Base honey target: ~80–95.
- Demonstrates value of Buzz 2 and begins choice between Flight/Yield/Buzz.

### Meadow 4 — Creek Garden

- 5 patches.
- Base honey target: ~115–135.
- Slightly longer travel makes Flight attractive.

### Meadow 5 — Tulip Rise

- 5 patches.
- Base honey target: ~150–180.
- Player should be approaching Buzz 3.

### Meadow 6 — Lily Clearing

- 6 patches including Lily finale.
- Hard requirement: Buzz 3 for final Lily cluster.
- Base honey target: ~230–280 plus region-completion bonus.

Total region economy should fund several upgrades plus at least 2–3 seed unlocks without requiring replay grind.

---

## 8. Replaying restored patches

A major balance decision: restored patches should not become an infinite high-rate honey exploit.

Recommended MVP behavior:

- first completion grants 100% base reward;
- after restoration, a patch can periodically become **Ready to Bloom Again**;
- replay reward is 20–35% of original value;
- replay exists for relaxing optional activity and small top-ups, not primary progression.

Alternative if even this adds complexity: restored patches stop being an economy source in the vertical slice. Test both versions.

---

## 9. Seeds

### Philosophy

Seeds are the expression system. They must be affordable enough that players actually use them.

Recommended MVP: purchasing a seed species permanently unlocks it for restored patches; replanting thereafter is free.

### First seed set

| Seed | Unlock cost | Role |
|---|---:|---|
| Daisy | free | starter/native |
| Clover | 20 honey | first customization choice |
| Lavender | 70 honey | first aspirational color/style |
| Tulip | 140 honey | premium first-region choice |

Lily may be unlocked as the region-completion reward rather than purchased.

This gives completion an aesthetic trophy.

---

## 10. Flower combinations

The player wants to combine flowers. We should support this without turning BeBee into a tile editor.

### Vertical slice

One primary species per patch.

Different patches in the same meadow can use different species, so the meadow already supports combinations.

### Post-slice expansion

Each patch can optionally have an Accent species. Accent plants occupy ~20–30% of visual spawn points.

Rules:

- Primary controls dominant color/silhouette.
- Accent is cosmetic first.
- Any gameplay bonus is small (<=10%) and clearly displayed.
- No “wrong combination” penalties.

Potential positive bonuses later:

- diverse meadow: +5% replay honey;
- native + chosen accent: slightly faster regrowth;
- all-one-species meadow: cosmetic “carpet bloom” effect rather than numerical punishment/reward.

Aesthetic freedom is more important than optimization pressure.

---

## 11. Region progression

A region unlocks the next one when its required meadows are restored.

Recommended structure:

```text
Region 1: Sunny Meadows
Region 2: Lavender Hills
Region 3: Wetland Garden
Region 4: Golden Fields
Region 5: Alpine Bloom
Region 6: Moon Garden / Exotic Finale
```

Each region should introduce:

- 1–2 new flower families;
- one environmental visual theme;
- one minor navigation idea;
- higher Buzz requirement;
- new seed aesthetics.

Do not introduce a new currency every region.

---

## 12. Planet restoration percentage

The percentage should reflect authored restoration work rather than raw flower count.

Simple model:

```text
planet_progress = completed_required_meadows / total_required_meadows
```

Optional weighted regions can be introduced only if needed.

Use rounded display values that always move after meaningful completion. Avoid situations where completing a meadow visibly changes 42.1% to 42.2% and feels meaningless.

---

## 13. Pacing rules

Healthy progression:

- first reward: <30 seconds;
- first upgrade: 1–3 minutes;
- first new flower: 3–6 minutes;
- first seed customization: 5–10 minutes;
- first completed meadow transformation: <10 minutes;
- first region completion: target 25–45 minutes for the slice;
- first full release should support several hours without artificial waiting.

These are product targets to validate, not promises.

---

## 14. Anti-grind rules

- Never require the player to repeat the same early meadow dozens of times to unlock a new region.
- New content should be funded primarily by progressing through new content.
- A single upgrade should not require more than a few minutes of appropriate-tier play in the main campaign.
- Replay farming is optional optimization, not mandatory progression.
- If telemetry shows players are farming old patches because current-tier rewards are insufficient, rebalance before adding boosters.

---

## 15. Economy telemetry requirements

Record at minimum:

- honey earned by source;
- honey spent by sink;
- upgrade level purchased;
- seed unlocked;
- meadow restored;
- player honey balance at region gates;
- time since previous progression event;
- abandoned session while facing a gate;

Key diagnostics:

```text
median time to first upgrade
median time to first customization
honey earned / honey spent ratio by meadow
% players blocked at each Buzz gate
upgrade selection distribution
seed unlock adoption
```

If most players ignore a stat, improve or remove it rather than simply making it mandatory.

---

## 16. Monetization boundary

Do not balance the core campaign around paid acceleration.

If ads/IAP are later required for a distribution platform, acceptable directions include:

- optional rewarded cosmetic seed pack;
- optional temporary convenience bonus;
- ad-free purchase;
- cosmetic bee appearances.

Do not make late flowers intentionally miserable to sell power. The game's retention proposition is restoration and ownership, not frustration relief.
