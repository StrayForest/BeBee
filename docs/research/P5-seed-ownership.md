# P5 — Seed Ownership During Restoration

Checked: 2026-08-29
Status: production implementation contract

## Problem

P5 must make seed ownership visible inside the recovering Meadow without turning native campaign patches into arbitrary player decoration. The player needs to understand two categories by looking at the world:

1. **native campaign patches** — authored Daisy/Clover/Lavender areas whose identity remains stable while they drive restoration and progression;
2. **player-shaped plots** — separate authored spaces where owned seed species may be planted and later replanted without changing campaign completion.

This implements the Hybrid topology already selected by D-005 / BB-P004 rather than reopening the topology decision.

## Reference pattern carried forward from BB-P004

The P-1 candidate pool remains applicable: Garden Life, Wildmender, Cloud Gardens, Terra Nil and Grow: Song of the Evertree. The selected structural lesson is not to copy their content, but to combine authored restoration progression with clearly bounded player-expression spaces. P5 narrows the unresolved prototype questions to exact plot placement, seed pacing, input and rendered comprehension.

## Official Defold documentation checked

- https://defold.com/manuals/input/ — checked 2026-08-29. Input is delivered to focused scripts through `on_input`; the existing focus stack must remain authoritative rather than adding an input-owning seed GUI.
- https://defold.com/manuals/input-mouse-and-touch/ — checked 2026-08-29. Single-touch can use the same left-mouse trigger path, so P5 can reuse the existing pointer-primary route instead of creating a touch-only planting action.
- https://defold.com/ref/stable/sys-lua/ — checked 2026-08-29. Save/load remains behind the existing versioned A/B storage service. The player species choice is independent state and therefore requires a schema migration instead of being inferred from campaign completion.

## Selected implementation

### Topology

- keep all three first-Meadow native patch IDs and flower identities unchanged;
- add two visually bounded player plots with stable IDs:
  - `r01_m01_player_plot_01` at `(1410, 1110)`, available after native patch 01;
  - `r01_m01_player_plot_02` at `(1780, 1310)`, available after native patch 02;
- player plots are never restoration contributors and never appear in `world.campaign_completion`.

Two plots are enough to prove ownership/expression in the first Meadow without competing visually with the three campaign patches. Additional plot count is future content tuning, not a hidden P5 dependency.

### Seed pacing

Production first-Meadow unlock prices reuse the previously simulated P3 customization-shadow costs and the P-1 candidate values:

| Seed | Available after | One-time unlock | Replant after ownership |
|---|---|---:|---:|
| Daisy | M01 / native patch 01 | 15 Honey | 0 Honey |
| Clover | M02 / native patch 02 | 18 Honey | 0 Honey |
| Lavender | M03 / native patch 03 | 22 Honey | 0 Honey |

Unlock-and-plant is one transaction. Once a seed is owned, switching a player plot to that species is free in P5. This keeps seed ownership meaningful while preventing reversible aesthetics from becoming a repeat tax.

The P5 economy regression exhaustively evaluates all `5! = 120` priority orders across Flight 2 (30), Buzz 2 (35), Daisy (15), Clover (18) and Lavender (22). Any order must still fund Buzz 2 before the Lavender campaign gate with zero replay rewards and non-negative Honey.

### Interaction

- keyboard/controller semantic: reuse existing `PRIMARY_ACTION` (Space/Enter in current HTML5 proof);
- pointer/touch semantic: tap the visible player plot while the bee is inside its interaction radius;
- contextual priority: nearby player plot first, otherwise existing Hive primary action;
- no seed modal, inventory screen, confirmation dialog or new persistent HUD;
- world-space plot label and action prompt appear at the plot, only while relevant/nearby.

### Persistence

Save schema increases from v2 to v3:

- `player.seed_unlocks` stores owned stable seed IDs;
- `world.player_plants` maps stable player-plot IDs to flower IDs;
- `world.campaign_completion` remains exclusively campaign/native completion.

Migration v2 -> v3 adds empty seed/plant tables and preserves Honey, Flight/Buzz levels and native completion exactly.

## Rejected alternatives

1. **Replant native campaign patches during restoration** — rejected because it contradicts D-005 and makes the required campaign path visually ambiguous while the Meadow is still recovering.
2. **Seed inventory/modal picker for the first slice** — rejected because two plots and three first species do not justify an additional modal/input-focus surface; it would increase friction and compete with the existing Hive modal.
3. **Consumable seed purchases on every replant** — rejected because a reversible aesthetic choice would become a repeat Honey drain and can conflict with D-009 anti-grind requirements.
4. **Free automatic ownership on native completion** — rejected because it removes the planned Honey sink and makes seed ownership indistinguishable from campaign completion rather than a player choice.
5. **Separate touch-only planting action** — rejected because current Defold touch/mouse input supports the existing pointer-primary route and a second mobile-only semantic would create unnecessary divergence.
6. **Persist a duplicate restoration/seed stage** — rejected because campaign completion and seed ownership already provide the required independent source data; a duplicate stage would create synchronization risk.

## Required proof before P5 can close

- deterministic `seed_locked` and `seed_unlocked` world captures on desktop, plus mobile-landscape unlocked capture;
- real browser path: native patch 01 -> Daisy unlock/plant -> native patch 02 -> Clover unlock/plant -> free Daisy replant;
- reload preserves owned Daisy/Clover, selected Daisy, Honey and native patch completion;
- replant does not alter campaign completion or charge Honey;
- direct touch/pointer planting is exercised on mobile-landscape;
- exhaustive economy regression passes all 120 purchase priorities with no replay;
- v2 -> v3 migration preserves P4/P3 state;
- P1-P4 browser proof remains green in the same exact-head retained artifact;
- independent evidence evaluation has no open `ITERATE` finding.
