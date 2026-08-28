# BB-P007 — Visual style bible research

Research snapshot: **2026-08-28**.

Decision: establish a **soft, non-pixel 2D toy-meadow baseline** at a 1280×720 / 16:9 reference viewport, with a deliberately large readable bee, sparse HUD, selective outlines, smooth filtering, low-frequency terrain and strict state/readability budgets. Exact production art remains original BeBee work; this task validates the measurable composition/tokens that future art must target.

Canonical machine-readable values: [`config/visual-style.json`](../../config/visual-style.json).
Human-readable implementation contract: [`docs/17-visual-style-bible.md`](../17-visual-style-bible.md).
Blocking-frame generator: [`tools/visual_style/generate_reference_frames.py`](../../tools/visual_style/generate_reference_frames.py).

## Problem

`docs/09-art-direction.md` describes the intended feeling but deliberately leaves camera scale, character size, filtering, UI tokens, motion timings and VFX density unresolved. If production starts from prose alone, every later agent can invent a different scale/palette/UI density and still claim to follow the same direction. BB-P007 must turn that qualitative intent into reproducible constraints before P0/P1 player-facing production.

The target is not to prove that one art style is universally best. It is to reduce arbitrary degrees of freedom while preserving enough room for actual art iteration.

## Evidence boundary

Three evidence types are intentionally separated:

1. **Hard technical/platform constraints** — current Poki and Defold documentation.
2. **Reference patterns** — public shipped-game/store screenshots used for hierarchy, character/world scale and clutter comparisons; screenshots are observed but not committed.
3. **BeBee subjective direction** — cute soft toy world, original bee/flowers/UI and the exact palette family. These are project choices, not external facts.

The resulting V-001 decision is `VALIDATED`, evidence strength `MEDIUM`: it is strong enough to constrain P0–P2 production, but BB-P008/P0 runtime captures and later playtests may tune numeric bands.

## Candidate pool

| Product | Why it is relevant | Why it is not the answer by itself |
|---|---|---|
| Cow Bay | Compact cute top-down world, large readable character, broad terrain shapes, low interaction complexity. | Its click-to-harvest interaction, energy economy and exact outline language are not BeBee requirements. |
| Olly the Paw | Cute browser/mobile presentation, bold silhouette hierarchy, simple top-level UI and movement-first scene readability. | Same developer family as Cow Bay, so it cannot be the only aesthetic evidence. |
| My Little Universe | Compact colorful world chunks with a materially smaller character and mostly outline-free low-poly rendering. | 3D resource/action structure is more complex than BeBee and includes combat. |
| Dreamdale | Mobile-friendly colorful world, readable player/world scale and strong upgrade/resource presentation. | Denser resource/economy UI is a poor default for BeBee's low cognitive load. |
| Forager | Highly readable 2D silhouettes and strong state/resource visibility. | Deliberately useful anti-pattern for BeBee: dense scene + dense HUD/tool/resource information. |

## Deep reference observations

### Cow Bay — clarity through large character + broad shapes

Source: https://poki.com/en/g/cow-bay

Public Poki presentation and current gameplay imagery show a compact, top-down/three-quarter cartoon world built from broad land masses and a visually dominant animal character. The player character remains easy to locate even when surrounded by harvestable objects. The screenshot pass also shows strong contour separation and relatively low terrain micro-noise.

Direct observation used by BeBee:

- character is deliberately large relative to the visible local world;
- broad color masses do more work than high-frequency texture;
- interactable/resource silhouettes are stronger than background decoration;
- persistent UI stays concentrated near edges rather than covering the playfield.

Inference:

- BeBee should keep the bee larger than a typical action-RPG avatar because personality/readability is a core fantasy, but should leave more world context than an extreme mascot close-up.

Manual screenshot estimate used only as a range check: Cow Bay's player character reads at roughly the **mid-teens percent of screenshot height** in representative public imagery. This is not treated as a canonical competitor measurement.

### My Little Universe — useful counterexample: smaller character, outline-free world

Source: https://store.steampowered.com/app/2328750/My_Little_Universe/

Public screenshots show a compact colorful world with a noticeably smaller player character and an outline-light/outline-free low-poly rendering language. The world remains readable because large geometric surfaces and color grouping establish hierarchy rather than heavy contours.

Direct observation used by BeBee:

- readable worlds do not require a contour around every object;
- lower-detail broad geometry can preserve strong spatial comprehension;
- a smaller character buys more world context, but loses some facial/personality presence.

Inference:

- BeBee should adopt **selective**, not universal, outlines: strongest on the bee and critical interactables, absent on terrain masses.
- Bee scale should sit above the smaller-character end of this comparison because expressive bee readability matters more than showing a very large harvesting radius.

Manual screenshot estimate used only as a range check: representative public imagery places the player around the **high-single-digits to low-teens percent of screenshot height**, depending on shot.

### Olly the Paw — same browser/mobile constraint, useful for hierarchy

Source: https://poki.com/en/g/olly-the-paw

The current Poki page confirms desktop/phone/tablet support, while public imagery uses bold cartoon shapes and keeps the controllable character immediately identifiable. It is useful as a browser/mobile hierarchy reference but is not independent of Cow Bay at the developer-family level, so it does not carry the decision alone.

Direct observation used by BeBee:

- a cute character can remain visually dominant without turning the world into a portrait screen;
- high-contrast edge treatment is useful around the player and important objects;
- top-level UI can remain compact while the world carries most instruction.

## Anti-pattern / materially different solution

### Forager — dense success that conflicts with BeBee's target load

Source: https://store.steampowered.com/app/751780/Forager/

Forager intentionally supports a busier progression/crafting loop. Public screenshots can contain many world objects, resource nodes, tools and persistent status elements at once. The result is appropriate for Forager's systems-rich loop but is a bad default for BeBee's one-clear-action / one-core-currency product rule.

Lesson for BeBee:

- do not equate “more visible progression” with “more simultaneous HUD”;
- keep the default persistent gameplay surface to one objective + Honey;
- decoration density must not make every object look actionable;
- VFX cannot become another permanent information layer.

## Official constraints checked

### Poki quality requirements

Source: https://developers.poki.com/guide/requirements-quality

Current requirements checked 2026-08-28:

- desktop, mobile and tablet support;
- full-screen mobile in portrait or landscape;
- **16:9** canvas;
- proportional scaling examples include **640×360, 836×470 and 1031×580**;
- external resources are restricted by default, reinforcing bundled/local font/asset planning.

BB-P007 consequence: use 16:9 landscape as the production reference composition and test smaller 16:9 portal scales explicitly. Portrait is not the primary composition for this game; responsive portrait-specific UI can be added only if later evidence justifies supporting both orientations.

### Defold GUI layouts

Source: https://defold.com/manuals/gui-layouts/

Current Defold defaults include a **Landscape 1280×720** display profile and a Portrait 720×1280 profile. GUI layouts can adapt to display profiles, while in-game content needs its own render/camera behavior.

BB-P007 consequence: 1280×720 is the natural reference-design surface because it matches both Defold's default landscape design profile and Poki's required 16:9 ratio.

### Defold camera

Source: https://defold.com/manuals/camera/

For 2D, Defold supports orthographic projection. `Auto Cover` fills the window while potentially cropping; `Orthographic Zoom` remains an extra multiplier on top of the automatically calculated zoom.

BB-P007 consequence:

- use orthographic camera semantics;
- use Auto Cover as the baseline adaptive behavior;
- keep required gameplay/objective information out of crop-only margins;
- allow only a narrow ordinary zoom multiplier band so asset scale remains stable.

### Defold texture filtering

Source: https://defold.com/manuals/texture-filtering/

Defold's current default min/mag filter is linear. Linear filtering supports smooth subpixel motion; nearest filtering is suited to strict pixel mapping but can visibly snap during slow movement.

BB-P007 consequence: choose **linear filtering** for the non-pixel BeBee style. Nearest filtering would contradict the intended soft continuous flight unless the art direction later changes to deliberate pixel art.

## Alternatives

### A — pixel-perfect / nearest / tiny sprite world

Rejected. It can be crisp and cheap but conflicts with the soft illustrated toy-world direction, expressive bee target and continuous subpixel flight.

### B — fully outlined mobile-cartoon world

Rejected as the canonical baseline. Thick contours everywhere make the bee readable, but they flatten terrain/interactable hierarchy and risk borrowing too much visual identity from the strongest 7Spot reference family.

### C — selective-outline soft 2D world

**Selected.** The bee and critical interactables receive stronger contour/value separation, while terrain/background use broad outline-free shapes. This combines the clarity lesson from Cow Bay/Olly with the low-outline counterexample from My Little Universe and keeps BeBee's expression distinct.

## Selected measurable baseline

Exact values are canonical only in `config/visual-style.json`; this table explains intent.

| Area | BB-P007 baseline | Reason |
|---|---|---|
| Reference viewport | 1280×720, 16:9 landscape | Defold default landscape + Poki hard aspect ratio |
| Bee height | 12–15% of screen height, nominal 13.5% | large enough for personality/control, between large mascot and smaller world-avatar references |
| Ordinary camera zoom multiplier | 0.95–1.10 | prevents per-feature camera invention; small tuning room |
| Adaptive camera | orthographic Auto Cover + safe composition margin | fills portal canvas while protecting required content from crop margins |
| Filtering | linear | smooth non-pixel flight; Defold default |
| Outlines | selective: strongest bee, lighter critical interactables, none on terrain | preserves hierarchy/originality |
| HUD | default max 2 persistent clusters; max 1 persistent objective | BeBee low-load rule + Forager anti-pattern |
| UI spacing/radii | tokenized in config | prevents per-panel invention |
| Motion | short UI/reward/completion bands + reduced-motion path | consistent feedback without long control lockouts |
| VFX | 64 live target / 32 low-end; max 3 normal groups | explicit density ceiling before content scales |

## Original BeBee blocking frames

The repository generator creates eight deterministic, original SVG blocking frames from primitives and system text:

1. default gameplay;
2. active pollination;
3. harder flower locked;
4. dormant meadow;
5. restored meadow;
6. Hive improvement;
7. seed choice;
8. landscape-mobile gameplay.

The generated output is not production art and is not committed as a game asset. Exact SHA-256 hashes are stored in `config/visual-style.json`; the checker regenerates the frames twice and fails on XML/dimension/hash drift. This keeps the pre-runtime composition anchors reproducible without pretending they are P0 runtime screenshots.

During BB-P007 the eight SVGs were rendered locally and inspected as one set. The seed-choice blocking frame was iterated after its first layout showed overlap; the regenerated frame passed the second inspection. The dormant/restored pair remains distinguishable without relying on HUD text, and the locked flower uses closed shape + lock treatment rather than hue alone.

## Acceptance / next gate

BB-P007 validates a production **style contract**, not final art quality.

P0/BB-P008 must next:

- implement matching deterministic Defold states;
- capture exact-build desktop + representative landscape-mobile screenshots;
- compare runtime scale against V-001;
- record actual safe-area/crop behavior at Poki-sized 16:9 viewports;
- retain visual artifacts in CI;
- tune V-001 only with a same-PR evidence update when runtime evidence exposes a mismatch.

Final font family remains intentionally `OPEN_PENDING_REDISTRIBUTION_LICENSE`; no font file enters the repository until license and planned script coverage are verified.
