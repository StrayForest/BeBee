# P2 — Pollination Core Loop production research

Status: **implementation candidate under exact-head runtime evaluation**.

## Problem

P1 proved that keyboard and floating-touch movement are stable, readable and input-safe. P2 must turn that traversal into the first complete production game loop without adding a high-frequency pollination button or allowing passive standing to become optimal.

The observable P2 target is:

```text
move → enter/recognize a patch → movement advances visible progress → bloom/completion reaction
→ one Honey transaction → dependent content unlock → reload preserves completion and Honey
```

The production tuning problem left open by D-006 is narrower than the original BB-P003 choice: select forgiving patch bounds and a work target that reward deliberate sweep movement while preventing one incidental straight fly-through from completing the patch.

## Existing direct BeBee evidence

BB-P003 already compared three controlled interaction variants:

- proximity auto-pollination;
- hold-to-pollinate;
- movement-through/sweep.

Sweep was selected because it produced zero stationary progress and no extra pollination input while preserving movement ownership. P2 does not reopen that validated interaction without contrary evidence; it productionizes and tunes it.

## Reference candidate pool

| Product | Source | Relevance |
|---|---|---|
| Cow Bay | https://poki.com/en/g/cow-bay | Browser/mobile gathering loop with explicit tap/click object interaction; strong contrast for action count. |
| Dreamdale | https://dreamdale.fandom.com/wiki/Game_Mechanics | Proximity/walk-over harvesting reference; exposes the risk of passive collection becoming optimal. |
| My Little Universe | https://news.xbox.com/en-us/2025/04/07/my-little-universe-survival-guide/ | Shipped automatic/manual-control contrast; demonstrates the additional action channel created by explicit resource interaction. |
| Forager | https://forager.fandom.com/wiki/How_to_play_guide_for_Forager | Movement plus explicit resource-hit input; high-agency but higher repetition cost. |
| Cow Castle | https://poki.com/en/g/cow-castle | Movement-centric browser/mobile resource loop in the same low-friction portal space. |
| Olly the Paw | https://poki.com/en/g/olly-the-paw | Low-friction keyboard and click/hold movement reference for portal/mobile control expectations. |

This pool is inherited from BB-P003 because P2 is the production gate for the same exact interaction problem; current source availability was rechecked on 2026-08-29 rather than cherry-picking a new confirming set after implementation.

## Deep observations used by P2

### Cow Bay — explicit object action

Direct observation: Poki documents tapping/clicking objects to use or harvest them.

P2 inference: this makes intent explicit, but importing a second high-frequency action would undo the BB-P003 result and compete with the validated one-surface touch movement scheme. BeBee should instead make movement-owned activation visually obvious.

### Dreamdale — proximity / walk-over collection

Direct observation: the mechanics reference describes resources that can be harvested while standing near them or walking over them without repeated tapping.

P2 inference: low input cost is useful, but pure proximity can reward waiting. BeBee keeps zero work while stationary and measures this explicitly in browser evidence.

### My Little Universe — automatic vs manual contrast

Direct observation: Xbox Wire describes a Manual Controls option where chopping/mining actions require explicit button presses.

P2 inference: explicit action ownership is a valid alternative, not a universal requirement. For a traversal-first bee fantasy, the extra action is rejected unless later playtests show movement-owned interaction is ambiguous.

## Materially different solution / anti-pattern

Forager's movement + explicit hit/tool action offers strong intentionality, but repeated resource actions consume a second input channel. For BeBee that would add a permanent touch affordance to a loop already proven with movement alone. P2 treats this as a useful anti-pattern for repetition cost, not as evidence that explicit input is inherently bad.

## Production alternatives

### A — proximity timer

Progress is based on time inside the patch, including while stationary.

**Rejected:** contradicts the BB-P003 measured zero-stationary target and can make stopping optimal.

### B — movement sweep with target <= one forgiving-zone diameter

Progress remains movement-owned, but a straight pass through the center can complete the patch.

**Rejected:** too permissive for the first authored patch; completion can become incidental rather than deliberate.

### C — movement sweep with target > one forgiving-zone diameter

Progress is actual travelled distance while inside `radius + edge_forgiveness`; work persists after leaving; one center fly-through gives substantial partial progress but cannot complete; a return pass/curve can finish.

**Selected:** preserves D-006, gives immediate local progress, mathematically prevents one ideal straight pass from completing, and requires no tiny-circle precision or second action.

### D — persist partial work every frame

**Rejected for P2:** completion/Honey durability is the milestone requirement. Saving high-frequency partial work would add unnecessary write pressure and lifecycle complexity. Partial patch work remains session-local; completion is the durable checkpoint.

## Authored P2 candidate values

These are **validated only if the exact-head browser evidence and separate evaluation pass**. They remain tunable, not LOCKED balance:

| Patch | Radius | Edge forgiveness | Effective diameter | Work target | Honey |
|---|---:|---:|---:|---:|---:|
| `r01_m01_patch_01` / Daisy | 145 | 24 | 338 | 410 | 45 |
| `r01_m01_patch_02` / Clover | 160 | 28 | 376 | 480 | 55 |

The invariant `work_target > 2 × (radius + edge_forgiveness)` is unit-tested for every authored P2 patch. Therefore even a perfect straight traversal through the full forgiving zone cannot complete the patch from zero work.

The 45/55 Honey rewards reuse `tools/economy/first_region_candidate.json` M01/M02 values. That source already marks them as hypothesis values. P2 proves transaction semantics and reward attribution, **not** final economy balance.

## State model

A patch owns only its local interaction state:

```text
LOCKED → AVAILABLE → ACTIVE → COMPLETED
```

- `LOCKED`: prerequisite not met; no work accepted.
- `AVAILABLE`: eligible, zero or no active work yet.
- `ACTIVE`: at least one qualifying movement sample has contributed work; progress persists within the session after leaving.
- `COMPLETED`: terminal for the campaign completion record; emits completion once.

`FlowerPatch` does not mutate Honey or save data. Completion is consumed by Progression/Economy, preserving T-004.

## Feedback design

P2 deliberately uses a small feedback stack rather than adding UI complexity:

- world-space flower cluster and local halo distinguish the target from decoration;
- movement inside the effective patch immediately advances the progress bar and staged flower opening;
- active uses V-001 cyan plus progress/shape redundancy;
- locked uses V-001 muted violet plus explicit `LOCKED` text;
- completion expands the flower state and changes the local success treatment;
- six low-alpha pollen markers appear only while movement is currently qualifying;
- completion emits an audio semantic hook for later licensed audio content;
- `+N HONEY` is shown at the completed patch for a 380 ms reward-pop window;
- persistent HUD remains exactly two clusters: one objective + Honey.

The temporary reward surface does not block movement.

## Official Defold documentation checked 2026-08-29

Project engine baseline: Defold 1.13.1.

### GUI runtime nodes and text

- https://defold.com/manuals/gui-script/
- https://defold.com/ref/stable/gui-lua/

Verified constraints used by P2:

- GUI scripts may create runtime box/text nodes with `gui.new_box_node()` / `gui.new_text_node()` and retain returned node references;
- `gui.set_size`, `gui.set_color`, `gui.set_enabled` and `gui.set_text` are the supported mutation path;
- a runtime text node's font must be mapped into the GUI scene before `gui.set_font()` selects it.

Implementation consequence: P2's primitive flower/HUD presentation remains presentation-only and is created inside the existing GUI scene; the GUI file maps Defold's built-in default font as a placeholder because V-001 explicitly leaves the final font family OPEN.

### Save API

- https://defold.com/ref/stable/sys/

Verified constraints used by P2:

- `sys.save()` should use a path from `sys.get_save_file()`;
- `sys.save()` can raise a Lua error on failure;
- its output workspace/file limit is approximately 512 KB.

Implementation consequence: P2 does not call `sys.save` from gameplay. It uses the existing storage service/A-B local adapter, which already protects calls, validates payloads, measures serialized size and handles HTML5 persistence semantics.

## Alternatives rejected on technical grounds

- direct `sys.save` from `FlowerPatch`: violates T-004/T-006 and couples interaction to platform storage;
- GUI-owned Honey: violates T-004 and makes idempotent reward tests harder;
- one game object per decorative flower: unnecessary entity/state overhead for P2; authored patch remains the logical interaction object and presentation can render a small cluster from it;
- changing P1 input/camera parameters without evidence: rejected because P1 already validated them and P2 has no observed movement defect requiring retuning.

## Acceptance criteria for P2 closeout

1. Data validator accepts the production flower/patch catalog and rejects bad IDs/references/numeric fields.
2. `LOCKED / AVAILABLE / ACTIVE / COMPLETED` transitions are deterministic and completion emits once.
3. Stationary time inside a patch adds zero work.
4. A full straight center fly-through cannot complete an untouched authored patch.
5. Keyboard and floating-touch movement can both complete the same interaction without a pollination button.
6. First completion awards exactly 45 Honey once, unlocks the dependent patch and emits one completion audio hook.
7. Reload preserves campaign completion, Honey and the dependent unlock without replaying the reward.
8. Canonical `pollination_idle`, `pollination_active_50`, `pollination_complete` and `hud_default` states render without browser errors at their required P2 viewports.
9. Persistent HUD stays at two clusters and required UI respects V-001 safe margins.
10. P1 movement/modal/reduced-motion and P0 storage browser proofs remain green.
11. Separate evidence-first visual/runtime evaluation returns `PASS` or an explicit justified `PASS WITH DEVIATION`, never `ITERATE`.

## Open limitations

- exact Honey values remain economy hypotheses until later region pacing evidence;
- P2 uses original repository-authored primitive development presentation, not final species illustration/audio assets;
- partial pollination work is not durable across reload; only campaign completion/Honey is durable in this milestone;
- no Buzz difficulty gate is added here; P3 owns Flight/Buzz upgrades and later flower difficulty application;
- audience comprehension still requires future external playtest/telemetry; autonomous exact-build evidence has MEDIUM confidence, not HIGH.
