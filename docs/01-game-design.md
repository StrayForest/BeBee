# 01 — Game Design Specification

## 1. Authority and status

Canonical decision status lives in `DECISIONS.md`.

This document describes the intended gameplay model, but any item marked `HYPOTHESIS` must be validated before dependent production complexity is built.

## 2. Player fantasy

The player controls a small expressive bee that makes damaged/dormant spaces bloom, earns Honey, improves its capabilities and influences which flowers become part of the recovering world.

The game is not a farming spreadsheet. The primary fantasy is:

> I fly around, make things bloom, become more capable and leave the planet visibly more beautiful and more mine.

## 3. Core loop

```text
move/explore
 -> interact with a flower patch through the validated pollination verb
 -> make visible progress
 -> bloom/complete
 -> receive Honey
 -> improve capability and/or unlock flower expression
 -> access/restore more of the meadow
 -> plant/shape parts of the recovering world
 -> increase region/planet restoration
```

Honey is the only core MVP currency.

## 4. Core interaction — HYPOTHESIS until P-1 validation

The original blueprint assumed proximity auto-pollination. That remains a candidate, not a locked rule.

`BB-P003` must compare at least:

### A — Proximity auto-pollination

Enter/stay near a patch and progress begins automatically.

Strengths to test:

- one-control simplicity;
- strong mobile accessibility;
- low interaction friction.

Risks:

- can become “move, wait, move, wait”;
- weak sense of agency if timing/position does not matter.

### B — Hold-to-pollinate

Near a patch, hold one semantic interaction action while moving/hovering.

Strengths:

- stronger ownership over action start/stop;
- explicit feedback relationship.

Risks:

- extra input may add unnecessary friction;
- touch UI can become cluttered.

### C — Movement-through / sweep pollination

Pollination comes from flying through/around the flower area rather than waiting in one point.

Strengths:

- makes flying itself the verb;
- potentially more expressive and active.

Risks:

- harder to explain/control;
- collision/coverage tuning may be fiddly on touch.

The winner becomes `VALIDATED` in `DECISIONS.md` before the permanent FlowerPatch interaction is locked.

## 5. Controls

### Locked principle

Gameplay consumes semantic actions, not raw device checks.

Desktop baseline:

- `WASD` / arrows — movement;
- semantic `interact` only if the validated core verb needs it;
- `Esc` / semantic back — pause/settings.

Touch baseline:

- movement scheme chosen after P-1/P1 research;
- virtual joystick is a strong candidate, not an immutable UI decision;
- the pollination action must not require precision tapping on individual flower sprites.

## 6. Bee movement

Movement should be smooth, light and responsive rather than grid-based.

Required qualities:

- acceleration/deceleration rather than harsh velocity switching unless testing proves otherwise;
- readable facing/lean;
- wing animation linked to movement state;
- no snagging on decorative flowers;
- collision only against meaningful obstacles;
- camera does not routinely steal control for objective guidance.

Initial tuning values may be prototyped, but exact speed/acceleration/camera numbers are not source-of-truth balance until validated in P1.

## 7. FlowerPatch domain model

The gameplay progression object is a logical **FlowerPatch**, not every decorative flower.

Minimum domain states:

```text
LOCKED
AVAILABLE
ACTIVE
COMPLETED
```

Optional presentation substates may include `CELEBRATING`, `PLANTED_BUDS`, `REPLAY_READY`, etc., but persistent campaign state must remain simpler than visual state.

Minimum data:

- stable `patch_id`;
- native/campaign flower identity where relevant;
- difficulty/requirements;
- pollination work target;
- Honey reward;
- unlock rule;
- restoration contribution;
- planted/customization state stored separately when applicable.

## 8. Difficulty

Difficulty is efficiency/aspiration, not punishment.

Use a mix of:

- normal intended-tier patches;
- soft gates that are possible but noticeably inefficient;
- occasional explicit hard gates where the requirement creates a clear future goal.

No hidden failure chance, death penalty or currency loss in the vertical slice.

Harder flowers should communicate difficulty through silhouette/state/feedback as well as numbers.

## 9. Pollination timing

A patch should resolve in seconds, not become a long idle bar.

The exact target duration depends on the validated interaction model. The old 2–10 second ranges are design starting points only.

Rules:

- feedback begins quickly after a valid interaction starts;
- repeated intended-tier interactions must not feel like waiting;
- progress/reset behavior is selected to support the chosen verb;
- no random failure.

If a prototype relies on stationary waiting for long periods, reject or redesign it rather than compensating with more effects.

## 10. Honey reward

Honey is awarded at meaningful completion boundaries.

Domain rules:

- reward is non-negative;
- a campaign completion cannot double-reward accidentally;
- reward presentation is connected visibly to the source action;
- control is not blocked while reward animation finishes.

Exact reward values live in `02-progression-economy.md` / data, not here.

## 11. Bee improvement

### Strong candidates

- **Flight** — movement/travel feel;
- **Buzz** — pollination capability / flower access.

### HYPOTHESIS

- **Yield** — Honey multiplier.

Yield must pass economy/payback validation before shipping. If it becomes mathematically mandatory or consistently unattractive, remove or redesign it. Do not preserve three upgrade tracks for visual symmetry.

Upgrade UI shape/card count follows the validated upgrade set.

## 12. Meadow restoration

A meadow changes visually as required restoration work is completed.

Typical authored stages:

```text
DORMANT -> WAKING -> GROWING -> RESTORED
```

Progress should be understandable from the world without opening a menu.

Restoration may add:

- richer ground/grass;
- flower bloom density;
- ambient pollen/insects;
- landmark recovery;
- music/ambience layers.

The before/after difference must remain obvious with the HUD hidden.

## 13. Seeds and customization — corrected direction

The previous GDD treated customization mostly as something unlocked only after full meadow completion. That is no longer authoritative.

Locked principle:

> Seed choice must contribute to player ownership during the restoration journey while remaining safe for campaign progression.

`BB-P004` compares:

1. native restoration first, customize later;
2. owned seeds can be planted during restoration;
3. hybrid native objectives + player-shaped plots.

Campaign-native completion and current planted visual species must be separate state concepts so planting cannot erase progression.

Replanting should be reversible where promised. Aesthetic choices must not create a soft-lock.

## 14. World gates

Default campaign gates use:

- meadow/restoration completion;
- explicit objective completion;
- Buzz/progression requirements.

Honey-payment world gates are not part of the default MVP model after the audit because spending Honey on seeds must not punish world access.

Any future Honey gate requires new research/economy evidence and a decision update.

## 15. Objectives/onboarding

Use minimal contextual guidance.

Principles:

- teach in gameplay;
- one obvious current objective is usually enough;
- remove instruction as soon as behavior is demonstrated;
- prefer world cues/edge guidance over camera hijacking;
- avoid modal tutorial page stacks.

The title/entry flow remains adaptable to the primary portal selected in P-1. Do not architecturally require an unnecessary `Title -> Play` click.

## 16. Planet goal

The macro goal is visual and sentence-simple:

> Make the planet bloom.

Regions contain compact authored meadows. Completing meaningful restoration increases visible regional/planet progress. Later regions introduce new visual identities and flower challenges without introducing a new currency each time.

## 17. No-frustration invariants

- no negative Honey;
- no progression erased by planting a different flower;
- no mandatory replay farming in the intended campaign path;
- requirements explain what is missing;
- no forced camera guidance during normal play;
- no death/currency-loss loop in the vertical slice;
- upgrade/customization decisions do not create irreversible trap states.

## 18. Vertical-slice proposal

Proposed first region remains six meadows:

1. First Patch;
2. Clover Bend;
3. Lavender Bank;
4. Creek Garden;
5. Tulip Rise;
6. Lily Clearing.

This structure is a `HYPOTHESIS` until P-1/P2 pacing evidence supports it.

Exact flower roster and canonical region order live in `04-world-content.md` and `DECISIONS.md`.

## 19. Product validation questions

Before scaling content, answer with evidence:

- Is flying itself pleasant?
- Is the chosen pollination verb pleasant after many repetitions?
- Does feedback start fast enough?
- Does a harder flower create aspiration rather than waiting?
- Does upgrading visibly change experience?
- Do seeds feel like ownership during restoration?
- Can customization spending ever create grind?
- Is the world transformation strong enough without UI?
- Can a new player state the long-term goal?

If the answer is unclear, prototype/test instead of writing more downstream systems.
