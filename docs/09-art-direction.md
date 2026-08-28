# 09 — Art, Animation & Audio Direction

## 1. Visual goal

BeBee should read as a small living toy world: soft, friendly, colorful, readable at a glance and satisfying when the land changes from dormant to blooming.

The target is **cozy casual clarity**, not detailed botanical realism.

---

## 2. Camera and presentation

- top-down with a slight 3/4 feel;
- character always readable against ground;
- camera close enough that the bee has personality, far enough to show several nearby objectives;
- avoid strong perspective distortion;
- world composition should work on desktop landscape and phone portrait crops;
- no camera angle change between gameplay and normal pollination.

The screen should visually prioritize:

1. bee;
2. active/available flower patches;
3. route toward next content;
4. HUD.

---

## 3. Bee character

### Shape language

- rounded body;
- oversized head/eyes relative to real anatomy;
- short soft limbs;
- two readable wings;
- simple stripe pattern;
- silhouette identifiable even at small scale.

Avoid:

- realistic insect anatomy;
- sharp mandibles/stingers as dominant features;
- highly detailed texture noise.

### Personality through movement

Required animation states:

- idle hover;
- fly;
- turn/lean;
- pollinating;
- upgrade reaction;
- meadow-restored celebration.

Optional later:

- sleepy idle;
- seed-plant reaction;
- cosmetics.

### Movement animation

- body lags movement direction slightly;
- wings accelerate with movement;
- gentle vertical hover motion at rest;
- pollination creates a focused “buzz” pose without freezing the bee rigidly;
- completion gives a tiny upward pop or happy spin, short enough not to block control.

---

## 4. Flower readability

Every species needs distinct:

- silhouette;
- dominant color family;
- bud shape;
- bloom motion.

Examples:

### Daisy

- small round center;
- white radial petals;
- quick multi-flower pop.

### Clover

- clustered tiny rounded blossoms/leaves;
- dense carpet feel.

### Lavender

- tall thin purple spikes;
- sequential glow/opening from bottom to top.

### Tulip

- large cup-shaped bud;
- strong single pop/open animation;
- saturated red/pink/orange variants.

### Lily

- large elegant closed bud;
- visibly “premium/difficult” scale;
- slower multi-petal opening;
- stronger pollen burst.

Later regions follow the same silhouette-first rule.

---

## 5. Dormant-to-restored color strategy

Dormant land must not be ugly; it should be intentionally subdued.

### Dormant

- lower saturation;
- fewer ground details;
- closed buds;
- sparse ambience;
- less movement.

### Progressing

- grass gains saturation;
- small ground cover appears;
- ambient pollen/fauna increases;
- landmarks gain decorative life.

### Restored

- full intended color;
- richer flowers;
- animated ambient insects;
- gentle spark/pollen layer;
- stronger music arrangement.

The restoration effect should be visible even if the HUD is hidden.

---

## 6. Palette philosophy

Use a coherent family rather than arbitrary rainbow saturation.

Recommended direction:

- warm grass greens;
- creamy/off-white UI panels rather than pure white;
- honey amber/yellow for progression/currency;
- bee yellow/black softened by brown/dark navy rather than absolute black if visually appropriate;
- each region has one dominant accent palette.

Do not rely on exact competitor colors.

Color decisions should be validated for readable state contrast and common color-vision deficiencies.

---

## 7. Terrain

Terrain should support flower visibility.

Good:

- broad low-frequency shapes;
- restrained ground texture;
- soft path edges;
- clustered decoration at boundaries;
- landmarks used for navigation.

Bad:

- equally detailed texture under every patch;
- tall decoration covering gameplay flowers;
- high-contrast grass blades everywhere;
- tiny decorative sprites that look interactable.

Interactable patches must remain the visually richest local objects.

---

## 8. Patch composition

Each logical patch visually contains multiple flowers.

Composition rules:

- irregular organic cluster rather than a perfect grid;
- center remains readable for progress feedback;
- patch edge communicates interaction radius approximately;
- flower count can increase visually as restoration progresses;
- decorative petals/leaves can extend outside logical trigger without changing gameplay bounds.

Avoid making every flower a separate gameplay entity.

---

## 9. Pollination VFX

Pollination must feel alive but remain lightweight.

Layering:

1. subtle pollen motes around active bee;
2. tiny curved particle movement between bee and patch;
3. flower-by-flower opening feedback;
4. completion pulse/burst;
5. honey reward arc toward HUD.

Do not cover the bee in opaque particles.

### Difficulty expression

Harder flowers can show:

- denser/slower pollen response;
- stronger closed-bud anticipation;
- richer completion burst;

Difficulty should not require violent effects.

---

## 10. Honey visual language

Honey is the only core currency, so it needs consistent identity.

Use:

- droplet/hex/honey-pot icon family;
- amber/golden movement trail;
- short elastic counter animation;
- subtle sticky/sparkle sound character.

Do not introduce coin imagery for the same currency.

---

## 11. UI visual style

UI should feel like the same world, not a generic mobile app layered on top.

### Shapes

- rounded cards/buttons;
- soft shadows/outline;
- large icons;
- restrained borders;
- generous spacing.

### Information density

- one currency persistent;
- one primary objective persistent;
- menus show only information necessary for that decision.

### Upgrade icons

- Flight: wing;
- Buzz: pollen/buzz rings;
- Yield: honey droplet/honeycomb.

Icons must be recognizable without reading labels after the first few uses.

---

## 12. Typography

Use a friendly rounded sans-serif with strong readability at small sizes and broad language support.

Requirements:

- Cyrillic support if Russian localization is planned;
- Latin/Finnish diacritics support if Finnish localization is planned;
- readable numerals;
- multiple weights only if needed;
- license compatible with commercial distribution.

Do not commit font files until license is verified and recorded in `THIRD_PARTY.md`.

---

## 13. Screen hierarchy mockups

These are structural wireframes, not pixel-perfect art.

### Gameplay

```text
┌─────────────────────────────────────┐
│ [Objective: Restore meadow 4/6] 🍯185│
│                                     │
│          flower patch              │
│             ◌ 65%                  │
│                                     │
│                🐝                   │
│                                     │
│  (mobile joystick)                  │
└─────────────────────────────────────┘
```

### Hive

```text
┌───────────────────────────────┐
│ Improve your bee        🍯185 │
│                               │
│ [Wing] Flight Lv2      🍯56   │
│ Fly 10% faster        [BUY]   │
│                               │
│ [Buzz] Buzz Lv2        🍯68   │
│ Pollinate faster      [BUY]   │
│                               │
│ [Drop] Yield Lv1       🍯40   │
│ Earn 12% more honey   [BUY]   │
│                               │
│             [Back]            │
└───────────────────────────────┘
```

### Seeds

```text
┌───────────────────────────────┐
│ Plant flowers                 │
│ [Daisy ✓] [Clover] [Lavender]│
│ [Tulip 🔒 140] [Lily 🔒]      │
│                               │
│        [Plant selected]       │
└───────────────────────────────┘
```

---

## 14. Audio identity

Sound should make small actions pleasant enough to repeat hundreds of times.

### Bee

- soft wing buzz loop with restrained volume;
- pitch/intensity can change slightly with movement;
- avoid realistic loud insect buzzing that becomes irritating.

### Pollination

- tiny soft chimes/plucks as flowers open;
- pollen shimmer texture;
- completion chord/popup.

### Honey

- warm sticky/plink reward sound;
- distinct from flower bloom.

### Upgrade

- short ascending flourish;
- stronger Buzz purchase can add a brief energetic flutter.

### Restoration

- layered bloom sound with ambient nature entering;
- region finale has a unique but still gentle musical payoff.

---

## 15. Music

Music should be light, loopable and non-fatiguing.

Preferred system:

- one base theme per region or small family of themes;
- optional additional instrumentation layer as restoration advances;
- music does not restart for every meadow if regions are continuous;
- menus/hive may duck or lightly filter rather than hard-cut music.

Avoid long cinematic tracks that fight short casual sessions.

---

## 16. Haptics

Mobile only where supported.

- light pulse: patch completion;
- slightly stronger pulse: upgrade or meadow restoration;
- no continuous vibration while pollinating.

Haptics must be disableable.

---

## 17. Asset production order

Do not commission/create the entire planet before gameplay is validated.

Order:

1. bee placeholder -> production bee;
2. Daisy production patch;
3. core terrain kit;
4. pollen/honey VFX;
5. Hive/UI production skin;
6. first meadow restoration set;
7. Clover/Lavender/Tulip/Lily;
8. first-region landmarks;
9. only after vertical-slice approval, remaining regions.

---

## 18. Art acceptance tests

An asset set passes when:

- bee is immediately distinguishable from flowers/terrain;
- available vs locked vs completed patch can be recognized without relying only on color;
- flower species are distinguishable at gameplay zoom;
- dormant vs restored meadow screenshots are clearly different;
- portrait crop does not hide required interaction behind UI;
- VFX makes completion feel stronger without hiding gameplay;
- UI looks coherent with world art;
- all imported assets have documented licenses.

---

## 19. Originality rule

Competitor screenshots may be used internally to understand hierarchy and readability, but production assets must not trace or reconstruct proprietary artwork.

BeBee needs its own:

- bee proportions/design;
- flower sprite language;
- terrain shapes;
- icons;
- panel skin;
- animations;
- sound effects;
- music;
- world landmarks.

The goal is to inherit proven **clarity**, not competitor identity.
