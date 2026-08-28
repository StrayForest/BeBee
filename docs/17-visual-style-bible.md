# 17 — Visual Style Bible

Status: **V-001 VALIDATED baseline (BB-P007)**.

This document is the human-readable contract for BeBee's measurable visual baseline. Exact numeric tokens live in [`config/visual-style.json`](../config/visual-style.json). If this prose and the config disagree, update both in the same evidence-backed PR rather than choosing silently.

The qualitative intent remains in [`docs/09-art-direction.md`](09-art-direction.md). Research/provenance is in [`docs/research/BB-P007-visual-style-bible.md`](research/BB-P007-visual-style-bible.md).

## 1. Reference composition

- Reference design surface: **1280×720**.
- Primary gameplay orientation: **landscape 16:9**.
- Required smaller portal checks: 640×360, 836×470, 1031×580.
- Representative landscape-mobile QA viewport: **844×390**.
- Do not place required objective/player-state information only in crop-sensitive outer margins.
- Use a 32 px reference safe edge for persistent UI; required gameplay composition should preserve at least the config safe-margin ratio.

The game should fill the 16:9 canvas. Supporting portrait-specific gameplay later is allowed, but is a separate layout decision rather than permission to shrink the landscape composition blindly.

## 2. World and bee scale

### Bee

At ordinary gameplay zoom the bee should occupy **12–15% of viewport height**, nominally **13.5%**. At 720 px reference height this is approximately 97 px.

The purpose is behavioral readability:

- the player finds the bee immediately;
- eye/head/body motion can carry personality;
- pollination effects can relate visibly to the bee;
- enough local meadow remains visible to plan the next movement.

Do not shrink the bee merely to fit more content. Do not enlarge it beyond the range to make one screenshot cuter without checking navigation/context cost.

### Flowers

- ordinary gameplay flower silhouette: 34–58 reference px tall;
- harder/premium flower silhouette: 52–76 reference px tall;
- species must differ by silhouette/cluster/state, not only hue.

Harder flowers may be larger/more elaborate but must not visually overpower the bee as the controllable subject.

## 3. Camera

- Orthographic 2D projection.
- Adaptive baseline: **Auto Cover** semantics.
- Ordinary user/design zoom multiplier: **0.95–1.10**, default 1.0.
- A transient reveal may zoom out to 0.90, but must not become the normal gameplay scale.
- Camera impulse: at most 10 reference px and 220 ms for ordinary feedback; reduced motion removes it.

A feature PR may not invent a dramatically different camera scale to make its own scene work. If content does not read inside the range, fix composition/content first or update V-001 with evidence.

## 4. Rendering language

BeBee is **not pixel art**.

- Texture filtering: linear.
- Terrain: broad, low-frequency forms; no contour required.
- Bee: strongest selective outline, 3 reference px target.
- Critical interactables: lighter 2 reference px target where needed.
- Decoration: must not gain the same contour/contrast priority as required interactables.
- Shadows: soft ellipse/contact family, restrained 0.16–0.28 opacity.

Outlines are a hierarchy tool, not a global shader identity.

## 5. Palette and state hierarchy

Canonical semantic colors are defined in config, including:

- warm dark ink;
- cream UI surface;
- amber Honey + darker Honey text/detail;
- grass / grass-dark;
- cyan active feedback;
- green success;
- muted violet/gray locked state;
- subdued dormant ground.

Rules:

- dormant terrain is less saturated and less detailed, not ugly/gray punishment;
- restored terrain increases color range, vegetation and ambient life;
- active/locked/completed gameplay states must use **shape/value/motion redundancy**; hue alone is insufficient;
- Honey uses the Honey family consistently rather than switching to generic coin imagery.

The dormant/restored difference must remain meaningful with HUD hidden.

## 6. UI tokens

### Persistent gameplay HUD

Default maximum: **2 persistent clusters**:

1. one current objective;
2. Honey.

A temporary third surface is allowed only for short contextual feedback. One persistent objective is the maximum in ordinary gameplay.

### Spacing / shape

Canonical spacing scale: 4 / 8 / 12 / 16 / 24 / 32 / 48 reference px.

Canonical radius family: 8 / 12 / 16 / 24 / pill.

Panel padding:

- compact 16;
- standard 24;
- large 32.

### Touch and controls

- visual button height: minimum 64, preferred 72 reference px;
- touch hitbox: minimum 80 reference px at the 720-high design surface;
- decorative shape may be smaller than the hitbox, but the hitbox may not be smaller than the minimum.

### Icons / type sizes

Use the token families in config; do not invent arbitrary sizes per screen.

The **font family itself remains OPEN** until redistribution license and localization coverage are verified. The reference-frame generator uses system text only as a blocking placeholder and is not a typography decision.

## 7. Motion tokens

- ordinary UI transition: 120–200 ms;
- reward pop: 260–420 ms;
- completion accent: 450–800 ms;
- major restoration reveal: 1200–2000 ms.

Reduced motion:

- transitions cap at 150 ms;
- camera impulse disabled;
- decorative particle count reduced to 30% baseline.

These are starting production bands. Runtime/player evidence can tune them; arbitrary per-feature timing is not allowed.

## 8. VFX budget

Normal pollination:

- max 3 simultaneous effect groups;
- max 18 particles per group;
- target max 64 live particles total;
- low-end fallback max 32;
- normal particle lifetime 0.25–0.80 s;
- particle alpha max 0.65;
- effects may cover at most ~20% of the bee area at once;
- completion burst <=0.8 s.

If a satisfying effect needs more density, prove the need with runtime capture/profiling rather than silently raising the budget.

## 9. Approved composition anchors

`config/visual-style.json` defines and hashes eight deterministic pre-runtime reference frames:

- `gameplay_default`;
- `pollination_active`;
- `hard_flower_locked`;
- `meadow_dormant`;
- `meadow_restored`;
- `hive_improvement`;
- `seed_choice`;
- `mobile_gameplay`.

Generate them with:

```bash
python3 tools/visual_style/generate_reference_frames.py --out /tmp/bebee-bbp007-frames
python3 tools/visual_style/check_visual_style.py
```

These SVGs are **blocking composition references**, generated from original primitives. They do not license tracing a competitor and they do not define final sprite illustration quality.

## 10. Production acceptance

A future visual implementation must either respect V-001 or explicitly update it with evidence. At minimum check:

- bee within target scale at ordinary camera zoom;
- current objective + Honey do not become a dashboard;
- interactables outrank decoration;
- hard/active/complete states remain legible without color alone;
- required information survives 16:9 portal scale/crop behavior;
- motion/VFX remain inside budget or have a documented exception;
- dormant/restored meadow reads without HUD;
- exact runtime screenshots supersede blocking SVGs once BB-P008/P0 exists.

## 11. What remains open

BB-P007 intentionally does **not** lock:

- final font family;
- exact production bee illustration/proportions beyond screen-scale/readability constraints;
- exact species illustrations;
- final animation curves;
- final particle textures;
- portrait gameplay support;
- screenshot-regression thresholds.

Those decisions require licensed assets, real Defold runtime evidence or later playtest data.
