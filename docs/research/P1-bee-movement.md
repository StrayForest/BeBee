# P1 — Bee Movement research and implementation brief

Checked: 2026-08-29

## Task

- Ticket: `P1-BEE-MOVEMENT`
- Change class: `player-facing`
- Feature/problem: make an empty BeBee field enjoyable to traverse before resource content is added.
- Player outcome: the bee responds immediately enough to feel controllable, retains a light sense of momentum, stays readable in the camera, and produces the same directional intent from keyboard and touch.
- Relevant decisions: `D-006`, `D-007`, `T-002`, `T-011`, `T-012`, `V-001`, `R-001`, `R-006`, `R-007`, `R-009`, `R-014`.
- Status before: exact speed/acceleration/camera/touch scheme are `HYPOTHESIS`/tunable inside an otherwise validated movement-first product direction.
- Decision provenance: `REFERENCE_PATTERN` + `TECH_CONSTRAINT`; final tuning requires `EXPERIMENT_RESULT` from BeBee runtime evidence.
- Evidence strength before runtime: `MEDIUM`.

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

Lifecycle/error cases to test: input focus ownership, simultaneous opposite keys, touch release outside the original anchor, touch start on the reserved non-movement side, window/aspect resize under Auto Cover, frame-time spikes, and camera clamping at field edges.

## 5. Alternatives and BeBee decision

| Alternative | Disposition | Evidence-backed reason |
|---|---|---|
| normalized velocity target + bounded acceleration/deceleration; keyboard and floating touch joystick feed one semantic intent; soft bounded camera follow | selected | Preserves continuous player control required by D-006, maps cleanly from both desktop and touch, and keeps Flight tuning as a later parameter change instead of a second movement system |
| direct position step / instant full-speed movement | rejected | Technically simple but removes the light momentum requested by the game-design baseline and leaves Flight with less room to change movement quality |
| tap-to-move/pathfinding | rejected | Adds path ownership and rerouting behavior that conflicts with continuous sweep control; shipped mobile evidence shows blocker/precision failure modes |
| physics-force-driven bee with decorative collision | rejected | Makes tuning/cross-device determinism harder and risks the exact collision snagging P1 is meant to eliminate |

Selected starting tuning for the first real-runtime candidate (explicitly tunable by evidence):

- max speed: 300 design units/s;
- acceleration: 1500 units/s²;
- deceleration: 1900 units/s²;
- turn acceleration: 2100 units/s² when intent opposes current velocity;
- floating joystick radius: 96 reference px;
- joystick dead zone: 12 reference px;
- movement touch surface: left 58% of canvas, leaving the right side available for later contextual interaction;
- camera normal follow: small dead zone + bounded follow speed, no look-ahead and no automatic zoom pulses;
- reduced motion: camera follows/clamps directly with no lag or impulse.

These numbers are not promoted to permanent balance merely by this brief. P1 runtime evidence may change them before merge.

Pattern adopted: continuous normalized directional movement with light momentum and unobtrusive floating touch control.

Intentional deviation from references: BeBee has no independent camera gesture in P1 because V-001 calls for a stable top-down follow camera and the product problem is sweep navigation, not 3D sightseeing.

Decision status after successful P1 evidence: movement controller/touch/camera baseline becomes `VALIDATED`; exact future upgrade curves remain tunable.

## 6. Acceptance criteria

- [ ] Cardinal and diagonal input share the same maximum speed within deterministic tolerance.
- [ ] Opposite keys cancel cleanly; release decelerates to idle without drift.
- [ ] Keyboard and touch feed the same normalized intent contract.
- [ ] Touch floating joystick can begin anywhere on the movement surface, has dead-zone handling and returns to zero on release.
- [ ] Bee position remains inside authored field bounds with no decorative collision dependency.
- [ ] Camera remains inside field bounds, uses orthographic Auto Cover and preserves V-001 bee readability at required viewports.
- [ ] Reduced-motion camera behavior removes nonessential lag/impulse.
- [ ] `movement_empty` and `movement_dense` are real deterministic HTML5 QA states.
- [ ] Exact-head desktop and mobile still captures plus 2–6 second motion evidence are retained with zero unexpected console/page errors.
- [ ] A deterministic 5-minute scripted movement soak exposes no bound escape, non-finite state, stuck input, or camera instability.
- [ ] Separate evidence-first evaluation returns `PASS` or an explicitly justified `PASS WITH DEVIATION`; `ITERATE` blocks merge.

## 7. Technical plan

- `gameplay/bee/movement.lua`: pure deterministic controller state and bounds.
- `gameplay/bee/input.lua`: keyboard/touch aggregation into normalized intent.
- `gameplay/camera/follow.lua`: pure camera target/bounds logic.
- Defold movement test field collection and thin runtime script: owns game objects, input focus, presentation state and QA bridge updates.
- primitive development presentation uses repository-authored Defold/GUI shapes only; final bee art remains out of scope.
- tests cover normalization, acceleration, deceleration, reversal, bounds, touch dead zone/release and camera bounds/reduced motion.
- HTML5 movement proof extends the existing exact-source CI/capture path and retains motion clips as CI artifacts.

Save/migration impact: none. Analytics impact: none. Platform SDK impact: none. Dependency impact: none planned.

Performance risks: per-frame movement/camera math must stay allocation-light; motion QA records representative browser frame samples and a five-minute deterministic soak runs in pure Lua/headless form.

Accessibility/input: reduced-motion camera path; touch control has a large floating acquisition region rather than requiring a small fixed target.

## 8. Verification plan

Automated:

- pure Lua movement/input/camera tests;
- existing test/data suite;
- development and release HTML5 builds;
- browser keyboard movement path;
- browser touch movement path at 844×390;
- deterministic movement states and exact-head capture;
- release-negative QA bridge check;
- five-minute-equivalent deterministic soak simulation.

Runtime/evidence:

- `movement_empty`: desktop 1280×720 and mobile 844×390;
- `movement_dense`: desktop 1280×720, Poki small 640×360 and mobile 844×390;
- motion clip for desktop keyboard sweep and mobile touch sweep;
- inspect full-size captures and motion record against V-001 and the selected reference patterns;
- separate evaluator record bound to exact PR head.

## 9. Evidence-first evaluation questions

The evaluator receives the player problem, criteria above, reference observations, exact-head captures/video and objective metrics first. It must specifically look for:

- sluggish start/stop or uncontrolled coast;
- camera lag that hides the next movement direction;
- bee scale/readability loss at 640×360 or 844×390;
- touch surface obscuring or fighting movement;
- keyboard/touch intent mismatch;
- bound jitter/snags;
- presentation motion that remains active in reduced-motion mode.

`ITERATE` is mandatory if any of those materially affects the five-minute movement goal.
