# BB-P007 visual style lab

This folder documents how to generate **original BeBee blocking/reference frames**. They are not competitor screenshots and they are not production art.

Purpose:

- turn qualitative art direction into inspectable composition anchors;
- give future agents a deterministic target for bee scale, sparse HUD, flower readability, dormant/restored contrast and modal density;
- keep the exact approved frame hashes in `config/visual-style.json` while the Defold runtime does not yet exist;
- seed BB-P008, where equivalent states will be captured and retained from the real HTML5 build.

Canonical numeric rules live in `config/visual-style.json`. The Python generator is the source for the temporary SVG blocking frames; do not infer canonical values from a screenshot by eye.

## Generate and validate

```bash
python3 tools/visual_style/generate_reference_frames.py --out /tmp/bebee-bbp007-frames
python3 tools/visual_style/check_visual_style.py
```

The generator uses only the Python standard library and emits eight deterministic SVGs:

- `gameplay_default.svg`
- `pollination_active.svg`
- `hard_flower_locked.svg`
- `meadow_dormant.svg`
- `meadow_restored.svg`
- `hive_improvement.svg`
- `seed_choice.svg`
- `mobile_gameplay.svg`

The generated files are intentionally **not** committed as runtime/player-facing assets. Their SHA-256 values are committed in the style contract, and `check_visual_style.py` regenerates them twice, validates their dimensions/XML and fails if any byte differs from the approved hashes. BB-P008/P0 will replace this pre-runtime proof with retained exact-build screenshots.

## Status and limitations

These frames validate **composition and token direction**, not final illustration quality. They intentionally use primitive shapes and system text. Production sprites, final font family, animation curves and VFX art remain future work.

The current blocking frames were also rendered locally during BB-P007 to inspect default gameplay, active pollination, locked flower, dormant/restored meadow, Hive, seed choice and landscape-mobile composition. Once P0/BB-P008 provides deterministic Defold HTML5 states, runtime captures become the higher-authority visual evidence.
