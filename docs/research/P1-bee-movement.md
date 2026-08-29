# P1 — Bee Movement research and implementation brief

Checked: 2026-08-29

## Task

- Ticket: `P1-BEE-MOVEMENT`
- Change class: `player-facing`
- Feature/problem: make an empty BeBee field enjoyable to traverse before resource content is added.
- Player outcome: the bee responds immediately enough to feel controllable, retains a light sense of momentum, stays readable in the camera, and produces the same directional intent from keyboard and touch.
- Relevant decisions: `D-006`, `D-007`, `D-013`, `T-002`, `T-011`, `T-012`, `V-001`, `R-001`, `R-006`, `R-007`, `R-009`, `R-014`.
- Status before: exact speed/acceleration/camera/touch scheme were `HYPOTHESIS`/tunable inside an otherwise validated movement-first product direction.
- Decision provenance: `REFERENCE_PATTERN` + `TECH_CONSTRAINT` + final `EXPERIMENT_RESULT` from BeBee runtime evidence.
- Evidence strength after runtime evaluation: `MEDIUM`.

## 1. Problem definition

BeBee's core pollination loop depends on continuous movement-through rather than standing still or repeatedly pressing an action button. Before flowers and economy are layered on top, movement itself must be comfortable for several minutes and predictable enough for later sweep-pollination tuning.

Solved means:

- a direction change begins without a perceptible dead period;
- releasing input decelerates without a long uncontrolled coast;
- diagonal input is normalized rather than faster than cardinal input;
- desktop and touch resolve to the same normalized movement intent;
- camera follow preserves orientation and never takes control away from the player;
- field bounds stop the bee cleanly without decorative collision snagging;
- reduced-motion removes nonessential camera lag/impulse;
- the deterministic `movement_empty` / `movement_dense` QA states can be rendered and motion-captured from the real HTML5 build.

Out of scope: pollination, Honey, upgrades, final bee art, final animation curves, audio, final meadow collision authored around real content, and final Flight upgrade curves.

## 2. Reference search space

| Candidate | Source | Why plausible | Deep inspect? | Selection note |
|---|---|---|---:|---|
| Stardew Valley mobile | https://stardewvalleywiki.com/Mobile_Controls | Mature top-down game with multiple touch movement schemes including invisible joystick | yes | Directly documents floating joystick behavior and tap-to-move failure modes |
| Sky: Children of the Light | https://sky-children-of-the-light.fandom.com/wiki/Menus_and_Controls | Touch-first movement/flight with screen-region control and camera separation | yes | Strong mobile control comparison despite 3D movement being more complex than BeBee |
| A Short Hike | https://www.playstation.com/en-us/games/a-short-hike/ | Shipped cozy traversal game where movement/soaring is itself enjoyable | no | Useful product-level traversal reference, but 3D platforming/camera makes exact controls less transferable |
| Chicory: A Colorful Tale | https://www.playstation.com/en-us/games/chicory-a-colorful-tale/ | Shipped top-down exploration with high character/world readability | no | Useful scale/readability reference; paint interaction is more central than movement feel |
| Haven Park | https://store.steampowered.com/app/1549550/Haven_Park/ | Small cozy exploration world with WASD/joystick movement | no | Relevant low-pressure exploration, but third-person 3D camera differs materially |
| Bee Simulator | https://store.playstation.com/en-us/concept/234347 | Direct bee-flight fantasy | no | Species fantasy is relevant, but six-axis/3D camera complexity is the wrong control target for BeBee's top-down 2D loop |

Candidate-pool exception: none; six plausible shipped products were found.

### Materially different solution / anti-pattern

Source: https://stardewvalleywiki.com/Mobile_Controls

Direct observation: Stardew mobile supports tap-to-move, but the documentation records cases where moving blockers can make the character stop, reroute or head in an unexpected direction. It also notes that some precise-positioning tasks require switching to a joystick scheme.

Lesson for BeBee: do not make pathfinding/tap destinations the primary movement abstraction for a game whose core verb is continuous directional sweeping. BeBee should preserve direct intent and immediate recovery from direction changes.

## 3. Deep reference observations

### Reference A — Stardew Valley mobile invisible joystick

- Platform/date: mobile control documentation checked 2026-08-29.
- Source: https://stardewvalleywiki.com/Mobile_Controls
- Why selected: it compares several shipped touch schemes inside one mature top-down game.
- Direct observation: the invisible joystick uses a press anywhere on the left half as the joystick center, then thumb displacement determines movement direction. Other variants combine joystick and buttons. Tap-to-move can be disrupted by blockers and is insufficient for some precise positioning.
- Inference: a floating origin reduces the need to acquire a fixed tiny control while preserving continuous analog intent.
- Measurable notes: one continuous touch surface is sufficient for movement; no movement confirmation/modal is required; stationary waiting is zero by design.
- Transferable pattern: floating directional surface on the movement half of the screen.
- Must not copy: Stardew's pixel UI, exact zones, icons, tool/action button layout, movement constants, or art.

### Reference B — Sky: Children of the Light touch movement

- Platform/date: iOS/Android control documentation checked 2026-08-29.
- Sources: https://sky-children-of-the-light.fandom.com/wiki/Menus_and_Controls and https://developer.apple.com/news/?id=zm47it7t
- Why selected: touch was a first-class design constraint and the shipped game explicitly separates direct movement and camera surfaces while trying not to obscure the playfield.
- Direct observation: two-handed mode uses one side for player movement and the other for camera; the D-pad is activated by pressing/holding on the movement surface. Apple Developer's design interview records that the team explicitly treated touchscreen obstruction and one-handed casual use as constraints.
- Inference: BeBee should reserve a clear movement surface without adding permanent control chrome when no second gameplay button is yet needed.
- Measurable notes: movement can begin from a touch region without a modal; the shipped design supports alternative one-/two-handed modes, showing that touch ergonomics are a distinct problem rather than a keyboard skin.
- Transferable pattern: direct touch direction and low persistent UI obstruction.
- Must not copy: Sky's 3D camera gestures, flight modes, cape-energy systems, UI icons, or control-specific animation.

## 4. Official technical documentation

Checked 2026-08-29.

1. https://defold.com/manuals/input/
   - Defold translates raw keyboard/mouse/touch/gamepad input into named actions before scripts receive it.
   - HTML5 supports single- and multi-touch.
   - Touch action names have documented limitations when reused with other input types, so BeBee keeps touch pointer handling distinct before normalizing to semantic movement intent.

2. https://defold.com/manuals/input-mouse-and-touch/
   - `MOUSE_BUTTON_LEFT` also supplies single-touch events.
   - pointer coordinates are available to input listeners.
   - a multi-touch trigger must not reuse the same action as the left-mouse/single-touch action.
   - P1 therefore needs only a single-touch movement surface and no dependency; future simultaneous action buttons can introduce a separately named multi-touch path if P2 requires it.

3. https://defold.com/manuals/camera/
   - 2D games can use orthographic camera projection.
   - `Auto Cover` fills the window from the design resolution and may crop edges.
   - `Orthographic Zoom` remains a multiplier on automatic zoom.
   - a camera may follow by updating its game-object position each frame.
   - P1 uses the existing V-001 1280×720 baseline and Auto Cover rather than custom resize math.

4. https://defold.com/manuals/render/
   - enabled Camera components take precedence in the default render pipeline.
   - camera projection is therefore kept in a real Camera component rather than faked with GUI-only transforms.

Lifecycle/error cases tested: input focus ownership, simultaneous opposite keys, touch release, right-side touch rejection, aspect/window resize under Auto Cover, frame-time spikes, field/camera clamping and modal focus consumption.

## 5. Alternatives and BeBee decision

| Alternative | Disposition | Evidence-backed reason |
|---|---|---|
| normalized velocity target + bounded acceleration/deceleration; keyboard and floating touch joystick feed one semantic intent; soft bounded camera follow | selected | Preserves continuous player control required by D-006, maps cleanly from both desktop and touch, and keeps Flight tuning as a later parameter change instead of a second movement system |
| direct position step / instant full-speed movement | rejected | Technically simple but removes the light momentum requested by the game-design baseline and leaves Flight with less room to change movement quality |
| tap-to-move/pathfinding | rejected | Adds path ownership and rerouting behavior that conflicts with continuous sweep control; shipped mobile evidence shows blocker/precision failure modes |
| physics-force-driven bee with decorative collision | rejected | Makes tuning/cross-device determinism harder and risks the exact collision snagging P1 is meant to eliminate |

Validated P1 baseline, still tunable by later evidence:

- max speed: 300 design units/s;
- acceleration: 1500 units/s²;
- deceleration: 1900 units/s²;
- turn acceleration: 2100 units/s² when intent opposes current velocity;
- floating joystick radius: 96 reference px;
- joystick dead zone: 12 reference px;
- movement touch surface: left 58% of canvas, leaving the right side available for later contextual interaction;
- camera normal follow: small dead zone + bounded follow speed, no look-ahead and no automatic zoom pulses;
- reduced motion: camera follows/clamps directly with no lag or impulse.

These values are `VALIDATED`, not `LOCKED`: P2/P3 may tune them if new pollination/Flight evidence creates a concrete reason.

Pattern adopted: continuous normalized directional movement with light momentum and unobtrusive floating touch control.

Intentional deviation from references: BeBee has no independent camera gesture in P1 because V-001 calls for a stable top-down follow camera and the product problem is sweep navigation, not 3D sightseeing.

## 6. Acceptance criteria

- [x] Cardinal and diagonal input share the same maximum speed within deterministic tolerance.
- [x] Opposite keys cancel cleanly; release decelerates to idle without drift.
- [x] Keyboard and touch feed the same normalized intent contract.
- [x] Touch floating joystick can begin on the movement surface, has dead-zone handling and returns to zero on release.
- [x] Bee position remains inside authored field bounds with no decorative collision dependency.
- [x] Camera remains inside field bounds, uses orthographic Auto Cover and preserves V-001 bee readability at required viewports.
- [x] Reduced-motion camera behavior removes nonessential lag/impulse.
- [x] `movement_empty` and `movement_dense` are real deterministic HTML5 QA states.
- [x] Exact-head desktop and mobile still captures plus 2–6 second motion evidence are retained with zero unexpected console/page errors.
- [x] A deterministic 5-minute scripted movement soak exposes no bound escape, non-finite state, stuck input, or camera instability.
- [x] Separate evidence-first evaluation returns `PASS`; the initial undersized-bee finding was iterated before closeout.

## 7. Implemented architecture

- `gameplay/bee/movement.lua`: pure deterministic controller state and bounds.
- `gameplay/bee/input.lua`: keyboard/touch aggregation into normalized intent.
- `gameplay/camera/follow.lua`: pure camera target/bounds logic.
- the movement object lives inside the proxied gameplay collection, not on the main-world owner;
- the existing proxied gameplay input listener forwards semantic intent to movement inside that same world, so Defold's native modal consumption remains authoritative;
- modal open clears held movement intent before acquiring focus, preventing stuck-key/touch state;
- deterministic movement QA readiness is exposed through the development-only HTML5 QA bridge instead of a cross-world gameplay message;
- primitive development presentation uses repository-authored Defold/GUI shapes only; final bee art remains out of scope.

This preserves the BB-003 contract that the main-world collection-proxy owner participates in focus routing without implementing its own `on_input()` forwarding layer.

Save/migration impact: none. Analytics impact: none. Platform SDK impact: none. Dependency impact: none.

## 8. Verification result

Accepted evidence head before the closeout-only documentation commit: `2e1098ac10596d02ad7d8b71e6034b5e778a7315`.

- Repository standards run `33240599831`: PASS.
- Test/data run `33240599809`: PASS, including 18,000-frame / five-minute-equivalent deterministic soak and modal-clear regression.
- HTML5 CI run `33240599811`: PASS.
- movement artifact `9711246614`, `movement-qa-2e1098ac…`: PASS; artifact digest `sha256:c7ce6fb028ea0e4a44bdfe66a4f5764be0e313af2e3b416381ea843b9dfda62e`.
- playable artifact `9711245985`; visual artifact `9711246280`; storage artifact `9711246878`; HTML5 diagnostics `9711247199`.
- desktop browser motion: 61.40 observed fps over the 2.313 s exercise, cardinal cruise 300 units/s, normalized diagonal speed 300 units/s, release speed 0, bound hits 0, console/page errors 0.
- mobile touch motion: 2.451 s exercise, horizontal speed 300 units/s, normalized diagonal speed 300 units/s, release speed 0, bound hits 0, console/page errors 0.
- reduced motion: horizontal/vertical camera lag 0.0.
- modal isolation: measured movement displacement while modal owned focus 0.0.
- retained still measurement after visual iteration: bee height 102/720 = 14.17% desktop, 48/360 = 13.33% Poki small, 52/390 = 13.33% mobile landscape, all inside V-001's 12–15% band.

Failure/iteration trace retained by Actions:

- `a9758f9…`: real keyboard hold exposed Defold action-update semantics; fixed by edge-only pressed/released state.
- `b13b302…`: keyboard passed; modal test exposed sub-frame Escape dispatch; proof switched to the already-proven CDP held-edge shape.
- `09599f2…`: modal opened but owner-side custom movement forwarding leaked through focus; architecture was rejected rather than patched around.
- `400fda6…`: attempted cross-world block message exposed an invalid socket assumption; also rejected.
- `5f2a32f…`: movement moved into the native proxied input world; complete runtime gate PASS.
- visual evaluation of that artifact found bee height only ~6.7–6.9% of viewport, below V-001; `2e1098a…` doubled presentation geometry and final retained captures land at 13.33–14.17%.

## 9. Independent evaluation result

The separate evidence-first evaluation record is `evidence/P1-BEE-MOVEMENT/evaluation.md`.

Verdict: **PASS**.

Evidence strength remains `MEDIUM`: the deterministic/browser evidence is strong for routing, parity, bounds, camera and frame pacing, while final art/audio and downstream pollination/Flight feel remain later milestones rather than being falsely claimed by P1.
