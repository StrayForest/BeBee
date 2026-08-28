# 00 — Product Vision

## Working title

**BeBee**

## One-sentence pitch

A cozy 2D progression game where a tiny bee pollinates increasingly challenging flower spaces, earns Honey, improves its abilities, chooses what grows in recovering meadows and gradually turns a dormant planet into a living garden.

## Player fantasy

The player should repeatedly feel:

1. **I am useful.** My actions make damaged land visibly recover.
2. **I am becoming more capable.** Flowers/areas that once felt difficult become easy or accessible.
3. **This world is becoming mine.** The recovering planet reflects my flower choices, not only a fixed authored checklist.

The fantasy is not spreadsheet farming. It is:

> I fly around, make things bloom and leave the world more alive and more personal than I found it.

## Audience

Primary:

- casual players who enjoy simple gather/upgrade/restore loops;
- desktop browser and mobile players;
- players comfortable with short sessions and low reading load;
- broad age suitability.

Secondary:

- completionists pursuing 100% planet restoration;
- decorators/customizers who care which flowers dominate a meadow;
- efficiency players who enjoy route/upgrade choices.

## Product pillars

### P1 — Immediate readability

A new player should quickly understand:

- I control the bee;
- flowers are the main world interaction;
- successful pollination/restoration gives Honey/progress;
- Honey improves capability and/or flower expression;
- stronger capability opens harder opportunities;
- the long-term goal is to make the planet bloom.

No opening lore dump or tutorial-page stack.

### P2 — Satisfying transformation

Every important meadow begins visually incomplete and changes in authored stages.

Progress should be visible in the world through:

- flower state;
- richer ground/vegetation;
- ambient insects/pollen;
- landmark recovery;
- stronger ambience/music;
- the player's own planted choices where the validated seed flow allows it.

A completed restoration must look meaningfully different with the HUD hidden.

### P3 — Simple, felt progression

The bee improves along a small number of understandable axes.

Current status:

- **Flight** — strong candidate;
- **Buzz** — strong candidate;
- **Yield** — hypothesis pending economy validation.

Do not preserve an upgrade just because the original mockup had three cards.

### P4 — Player-authored restoration

This pillar is corrected after the blueprint audit.

Seeds/customization should not be only a post-completion decoration feature. The player should influence what the recovering world becomes **during the restoration journey** in a way that remains clear and progression-safe.

Exact flow is validated in `BB-P004` from several models (native-first, player-shaped, hybrid).

Locked rules:

- flower choices are understandable;
- choices are reversible where promised;
- customization never erases campaign progress;
- spending Honey on aesthetics does not create an unrecoverable progression grind.

### P5 — One planet, obvious macro goal

The global objective is a visible restoration journey from dormant toward 100% bloom.

Regions contain compact authored meadows. Later regions introduce new visual identities and flower challenges without multiplying currencies/systems unnecessarily.

## Core loop

The exact pollination input remains a hypothesis until P-1, but the product loop is:

```text
Explore/move
 -> pollinate through the validated core verb
 -> bloom/restore
 -> earn Honey and visible world progress
 -> improve the bee and/or unlock flower expression
 -> shape recovering plots/meadows with seed choices
 -> access harder/new restoration work
 -> increase planet restoration
```

## Session outcomes

A normal short session should usually produce at least one visible change:

- complete meaningful flower/restoration work;
- buy a felt improvement;
- open a new path/meadow;
- plant/change a flower choice;
- reach a restoration stage;
- discover a new flower identity;
- complete a region milestone.

The player should rarely leave feeling that nothing changed.

## Emotional curve

1. **Curiosity** — dormant world and an obvious nearby opportunity.
2. **Pleasure** — first bloom and immediate reward/world response.
3. **Agency** — capability and/or seed choice changes what the player can do or see.
4. **Aspiration** — desirable harder flower/space visible ahead.
5. **Mastery** — improvement makes the former obstacle manageable.
6. **Ownership** — player-selected flowers become part of the recovering landscape.
7. **Scale** — local progress contributes to a planet-sized transformation.

## Difficulty philosophy

Difficulty is primarily **efficiency/aspiration friction**, not punishment.

Use:

- harder flower work;
- soft capability recommendations;
- occasional clear hard gates when they create a good future goal;
- navigation variation.

Do not use:

- random failure chance;
- death/currency loss;
- resource theft/durability;
- long idle waiting bars as the main challenge.

## Economy philosophy

Vertical slice: **one core currency — Honey**.

Default Honey sinks:

- validated bee improvements;
- validated seed/flower-expression unlocks.

World progression should default to restoration/capability/objective gates rather than charging Honey directly, so choosing flowers cannot punish access to the campaign.

## Reference philosophy

We learn from shipped games such as Cow Bay, Cow Castle, Olly the Paw, My Little Universe, Dreamdale and other problem-specific references.

Useful broad patterns include:

- fast first meaningful action;
- layered complexity;
- visible future goals;
- clear permanent improvement;
- shallow task-specific menus;
- spatial/world transformation as progression;
- browser/mobile accessibility.

But exact interaction, HUD placement, timing and economy are not copied or treated as validated merely because a competitor uses them.

## What we do not copy

- proprietary source code;
- exact maps/levels;
- competitor characters/art/icons;
- dialogue/quest wording;
- sounds/music;
- distinctive pixel-identical UI composition;
- competitor economy values;
- extracted assets/files.

BeBee must have original content and implementation.

## Vertical-slice intent

The slice should prove, not merely contain:

- expressive bee movement;
- a validated repeatable pollination verb;
- satisfying bloom/reward feedback;
- Honey economy with meaningful, non-trap choices;
- capability progression;
- a seed/restoration ownership flow;
- one strong meadow transformation;
- one compact coherent region;
- safe save/reload;
- desktop/touch usability;
- production-quality HTML5 behavior on the selected primary target.

## Explicit non-goals for the vertical slice

- multiplayer/PvP;
- mandatory combat;
- complex crafting;
- backend account system;
- premium currency;
- hard energy timer;
- daily streak pressure;
- battle pass;
- procedural infinite world;
- heavy worker/automation simulation.

## Success criteria before mass content

Evidence must show:

- new players understand the core verb without external explanation;
- the verb remains pleasant after repetition;
- movement/camera feel good;
- improvement is felt, not only displayed numerically;
- harder flowers create aspiration rather than boredom;
- seed choice feels like ownership during restoration;
- seed spending does not create grind/soft-locks;
- before/after restoration is emotionally legible;
- saves survive target browser lifecycle tests;
- target performance/load/portal requirements pass.

## North-star question

For every proposed feature ask:

> Does this make flying, pollinating, blooming, improving, choosing flowers or restoring the planet more satisfying and understandable?

If not, it probably does not belong in the vertical slice.
