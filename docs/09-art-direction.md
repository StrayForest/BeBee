# 09 — Art, Animation & Audio Direction

## 1. Visual goal

BeBee should feel like a small living toy world: soft, friendly, colorful, readable at a glance and satisfying when the land changes from dormant to blooming.

Target: **cozy casual clarity**, not botanical realism.

This document defines direction. `BB-P007` must convert the qualitative direction into a measurable style bible before mass asset production.

## 2. Locked visual principles

- bee is always readable against terrain;
- gameplay flowers read by silhouette/state, not color alone;
- interactable objects are clearer than decoration;
- dormant land is subdued but still appealing;
- restored land is visibly richer even with HUD hidden;
- UI belongs to the same visual world and remains sparse;
- production art must be original or properly licensed;
- competitor screenshots may inform hierarchy/clarity but are not tracing references.

## 3. Camera/presentation — HYPOTHESIS details

Direction:

- top-down / slight 3/4 feel;
- bee large enough to show personality;
- enough nearby world visible to understand goals;
- no strong perspective distortion;
- composition survives desktop and selected mobile/portal crops.

Exact camera zoom, bee screen size and world scale are **not locked** until P1/`BB-P007` visual tests.

## 4. Bee design

Shape language:

- rounded body;
- oversized expressive head/eyes relative to real anatomy;
- short soft limbs;
- readable wings;
- simple stripes;
- no threatening realistic insect anatomy.

Required production-state family after movement is validated:

- idle hover;
- fly;
- turn/lean;
- validated pollination state;
- improvement reaction;
- restoration celebration.

Optional later:

- cosmetics;
- extra idles;
- special reactions.

## 5. Flower readability

Every gameplay species should differ in several ways:

- silhouette;
- dominant color family;
- bud/locked shape;
- bloom motion;
- density/cluster shape where useful.

Examples remain direction only:

- Daisy — small radial white/yellow, quick opening;
- Clover — dense rounded carpet identity;
- Lavender — tall thin purple spikes;
- Tulip — large cup-shaped saturated bud;
- Lily — large elegant premium/difficult silhouette.

Do not add species that are distinguishable only by minor hue changes.

## 6. Dormant -> restored language

### Dormant

- lower saturation;
- fewer ground details;
- fewer ambient actors;
- closed/limited flowers;
- quieter ambience.

### Waking/Growing

- richer grass/ground cover;
- ambient pollen/insects increase;
- landmark recovery;
- player-planted choices become more visible where validated.

### Restored

- full intended color range;
- richer vegetation;
- ambient ecosystem life;
- strongest local bloom/ambience state.

Deterministic before/after screenshots must show a meaningful difference without HUD.

## 7. Terrain

Terrain supports gameplay readability.

Prefer:

- broad low-frequency shapes;
- restrained ground texture;
- decoration concentrated around boundaries/landmarks;
- soft route edges;
- clear local contrast around flower patches.

Avoid:

- equally detailed noise everywhere;
- tall decoration hiding required flowers;
- tiny decoration that looks interactable;
- terrain patterns competing with progress feedback.

## 8. Pollination/bloom VFX

The final effect depends on the validated core verb, but likely layers include:

- light pollen around bee/patch;
- directional relation between bee and flowers;
- staged flower opening;
- short completion accent;
- Honey attribution toward the currency surface.

Do not bury the bee/flowers under opaque particles.

Harder flowers may have richer anticipation/completion, not violent effects.

## 9. Honey visual language

Honey is the only core currency.

Keep a consistent family:

- amber/golden identity;
- droplet/honeycomb/pot motifs where appropriate;
- source-to-counter reward motion;
- distinct reward sound.

Do not use coin imagery for the same currency without a specific reason.

## 10. UI direction

- rounded, friendly shapes;
- large clear icons;
- restrained shadows/outlines;
- generous spacing;
- few persistent elements;
- no generic mobile-dashboard clutter.

Exact panel radius, spacing scale, shadow parameters, icon size and typography are produced by `BB-P007` rather than invented per PR.

## 11. Typography

Requirements:

- high small-size readability;
- readable numerals;
- scripts required by planned localization;
- commercial redistribution license;
- license recorded before font files enter repository.

Do not select a font based only on cuteness.

## 12. Audio direction

Bee:

- soft non-irritating wing buzz;
- movement intensity may subtly affect it.

Pollination/bloom:

- light, pleasant repeated feedback;
- completion distinct from progress ticks.

Honey:

- warm reward identity distinct from bloom.

Improvement:

- short upward/positive response.

Restoration:

- layered world/nature payoff rather than generic coin fanfare.

Audio must remain non-fatiguing over repeated actions.

## 13. Music

- light, loopable, low-fatigue;
- region identity rather than a new track for every tiny meadow;
- restoration layers may enrich arrangement if simple enough;
- menus should not cause unnecessary hard restarts.

## 14. Haptics

Where supported:

- light completion pulse;
- slightly stronger major restoration/improvement pulse;
- no continuous pollination vibration;
- user can disable haptics.

## 15. BB-P007 — Visual Style Bible deliverables

Before production art scales, lock or validate these with actual BeBee reference frames:

### World scale

- target bee screen-height range at gameplay zoom;
- gameplay camera zoom range;
- world-unit / sprite-resolution / PPU convention;
- supported camera crop behavior.

### Asset rendering

- texture filtering choice;
- atlas/native source resolution rules;
- outline/no-outline rule;
- shadow direction/softness/opacity range;
- foreground/background saturation/contrast hierarchy.

### UI tokens

- spacing scale;
- corner-radius scale;
- panel padding;
- button heights;
- icon size family;
- typography sizes/weights;
- shadow/border tokens;
- Honey/progression semantic colors.

### Motion tokens

- ordinary UI transition duration range;
- reward pop duration range;
- completion accent duration range;
- reduced-motion alternatives;
- camera reveal limits.

### VFX budgets

- max normal simultaneous pollination effects;
- density/opacity targets;
- particle lifetime bands;
- low-end fallback rules.

### Approved frames

Create a small set of **our own** approved visual reference frames:

- default gameplay;
- active pollination;
- locked harder flower;
- dormant meadow;
- restored meadow;
- improvement/Hive surface;
- seed choice surface;
- representative mobile layout.

These become internal visual anchors for later agent work.

## 16. Asset production order

Do not produce the whole planet first.

1. movement-test bee;
2. one production-quality bee direction;
3. starter flower + terrain kit;
4. pollination/Honey feedback;
5. one improvement surface;
6. one meadow dormant/restored set;
7. validated seed-flow visuals;
8. remaining first-region content;
9. only after P6 approval, later-region production.

## 17. Art acceptance

An art/visual task passes only when:

- state remains readable at gameplay zoom;
- bee remains visually dominant enough to control;
- interactable vs decorative content is clear;
- locked/active/completed states do not rely on color alone;
- mobile/portal crops preserve required information;
- effects reinforce cause/effect without hiding gameplay;
- style tokens/approved frames are respected or intentionally updated;
- all third-party material has verified provenance;
- `docs/13-visual-qa-scorecard.md` evidence is attached.

## 18. Originality

BeBee requires its own:

- bee proportions/design;
- flower rendering language;
- terrain shapes;
- UI skin/icons;
- animations;
- VFX treatment;
- sounds/music;
- landmarks/world composition.

Borrow clarity, not identity.
