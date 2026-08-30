# BeBee Decision Registry

This is the shortest authoritative record of product and technical decisions.

## Precedence

When documentation conflicts, use this order:

1. `DECISIONS.md`
2. `docs/11-blueprint-hardening.md`
3. task-specific approved research record / ADR
4. numbered design/technical docs
5. old PR descriptions, comments and informal notes

Do not silently resolve a contradiction. Update the decision registry or open a finding.

## Status vocabulary

- `LOCKED` — may be implemented as specified; changing it requires an explicit decision update.
- `VALIDATED` — supported by research/prototype/playtest evidence; may still be tuned.
- `HYPOTHESIS` — working direction only; do not build dependent complexity until the validation task passes.
- `OPEN` — decision intentionally not made yet.
- `DEPRECATED` — no longer authoritative.

## Provenance vocabulary

Status says how settled a decision is. Provenance says why the decision exists.

- `OWNER_CONSTRAINT` — explicit project-owner direction.
- `REFERENCE_PATTERN` — supported by shipped-product observation.
- `TECH_CONSTRAINT` — required or strongly constrained by current official technical documentation.
- `EXPERIMENT_RESULT` — selected after direct prototype/variant comparison.
- `SIMULATION_RESULT` — supported by deterministic modeling.
- `TELEMETRY_RESULT` — supported by production telemetry.
- `PLAYTEST_RESULT` — supported by observed user testing.
- `SUBJECTIVE_DIRECTION` — explicit aesthetic/tone choice that should not be presented as objectively proven.

Substantial new decisions should also record evidence strength (`LOW`, `MEDIUM`, `HIGH`) in their research/evidence record. See `docs/15-agent-evidence-governance.md`.

## Product decisions

| ID | Status | Decision | Evidence / next gate |
|---|---|---|---|
| D-001 | LOCKED | Core fantasy: a cute bee restores a planet by pollinating flowers and shaping what blooms. | Product brief plus P4 exact-head runtime evidence: the first meadow now visibly progresses DORMANT → WAKING → GROWING → RESTORED from existing pollination completions, with HUD-hidden before/after and separate PASS evaluation. Production art/audio richness remains later P6 work. |
| D-002 | LOCKED | MVP uses one core currency: Honey. | Simplicity/product pillar. |
| D-003 | LOCKED | No mandatory combat, hard energy timer, premium currency, multiplayer or backend account in the vertical slice. | Scope control. |
| D-004 | LOCKED | World is authored as regions/meadows/patches; not an infinite procedural world. | Pacing/readability/performance plus P4 production proof. Meadow `r01_m01` uses an authored four-stage restoration ladder derived from stable authored patch completion IDs; exact-head browser evidence proves deterministic before/mid/after and save-safe recovery without a duplicate persisted stage. |
| D-005 | VALIDATED | Hybrid seed/restoration topology: during restoration, authored native campaign plots keep their native/campaign identity while dedicated player-shaped plots may accept owned seeds; player-shaped plots never gate campaign completion. After restoration, completed native plots may become replantable where content allows. Campaign/native identity and current planted species remain separate state. | BB-P004 deterministic A/B/C structural experiment + reference analysis. Native-first produced no ownership before restoration; fully player-shaped allowed an incomplete native campaign plot to display a conflicting chosen species; Hybrid preserves early ownership without overloading active native objectives. Evidence strength MEDIUM; P5 must validate rendered comprehension, exact plot count/placement, planting input and seed pacing against the now-productionized P4 restoration states. |
| D-006 | VALIDATED | Primary pollination interaction is movement-through/sweep: qualifying movement while inside a pollinatable patch advances progress; standing still does not, and the default scheme has no separate high-frequency pollination button. P2 production baseline uses Daisy radius 145 + 24 forgiveness / work 410 and Clover radius 160 + 28 forgiveness / work 480; values remain tunable rather than LOCKED. | BB-P003 A/B/C experiment plus P2 exact-head production evidence. On accepted P2 runtime, standing adds 0 work; one first-patch straight pass reaches 337.56/410 (82.33%) desktop and 339.99/410 (82.92%) mobile without completing; a return sweep completes. P4 retains the same verb as the sole restoration cause rather than adding a second restore action. Evidence strength MEDIUM. |
| D-007 | VALIDATED | Vertical-slice bee upgrade tracks are **Flight + Buzz**. Yield is excluded from the vertical slice; do not add a replacement track merely to preserve three cards. P3 productionizes the first level as Flight `300 -> 330 u/s` for `30 Honey` and Buzz `1.00x -> 1.35x` pollination work for `35 Honey`; later levels/effect curves remain tunable. | BB-P005 deterministic economy analysis plus P3 exact-head runtime/economy evidence. Removing Yield still gives 5040/5040 full retained-sink purchase-priority orders reaching region completion with zero replay and non-negative balance. P3 proves both first choices are affordable from 45 Honey, Flight changes real movement to 330 u/s, Buzz changes real work to 1.35x and unlocks the explicit Lavender `Buzz 2` gate; both purchase orders and the customization-heavy regression remain progression-safe. P4 reuses Buzz 2 on the real restoration path and reload retains it. Evidence strength MEDIUM; later levels require later pacing/playtest evidence. |
| D-008 | VALIDATED | Sparse HUD: one persistent objective plus Honey, with contextual pollination state/progress in world space and redundant non-color state cues where needed. | V-001 density ceiling plus P2/P4 exact-head rendered evidence and separate evaluations. P2 established the two-cluster HUD and explicit locked cue; P4 retains persistent objective count 1, adds no modal tutorial, and proves the meadow transformation remains materially readable with the HUD hidden. Evidence strength MEDIUM; later UI polish may tune expression without increasing default persistent density absent new evidence. |
| D-009 | LOCKED | Progress/customization choices must not create an unrecoverable grind or punish aesthetics. | Product rule. P4 adds no new currency/spend or restoration confirmation, so existing economy safety is unchanged. |
| D-010 | LOCKED | MVP world gates should use restoration/progression/Buzz by default, not Honey payments. | Prevents spending seeds from blocking campaign progress. P3/P4 production path uses the Lavender Buzz-2 capability gate and restoration completion, not a Honey world payment. Any Honey gate requires new evidence. |
| D-011 | VALIDATED | Six-meadow first-region structure: First Patch, Clover Bend, Lavender Bank, Creek Garden, Tulip Rise, Lily Clearing. | P6 exact-head clean-save browser evidence restores all 6/6 Sunny Meadows in one continuous authored region, proves Flight/Buzz 3 and Lily's Buzz-3 climax gate, save-v4 reload, settings/analytics and target viewport/performance budgets. Independent verdict is PASS WITH DEVIATION only for final illustration/typography polish; no structural `ITERATE` remains. Evidence strength MEDIUM. |
| D-012 | LOCKED | Canonical proposed region order is Sunny Meadows → Golden Fields → Wetland Garden → Rosewood → Alpine Bloom → Moon Garden. | P7 real browser evidence accepts Golden Fields, Wetland Garden, Rosewood, Alpine Bloom and Moon Garden as sequential authored regions in the same continuous world without a new navigation system. The six-region chain remains data-driven, bounded by the pooled renderer and uses no new core verb or per-region lifecycle. |
| D-013 | VALIDATED | Baseline bee traversal uses one normalized direct-intent controller for keyboard and a floating touch joystick, bounded acceleration/deceleration, authored field bounds, bounded orthographic follow and a reduced-motion direct-follow path. The P1 accepted **level-1** baseline uses 300 design units/s max speed, 1500 acceleration, 1900 deceleration, 2100 reversal acceleration, a 96 px floating-joystick radius, 12 px dead zone and a left-58% touch acquisition surface. P3 Flight progression changes the computed max speed to 330 u/s at Flight 2 without changing those controller semantics. These values are validated but tunable, not locked. | P1-BEE-MOVEMENT research + exact-head HTML5 motion evidence + separate evaluation establish the controller. Desktop/touch both reach normalized 300-unit/s level-1 movement and return to zero; modal displacement and reduced-motion camera lag are 0. P3 exact-head evidence measures real Flight-2 cruise at 330/330 u/s. P4 exact-head evidence additionally proves the restoration reveal does not capture control: the bee moves 86.644 design units during the 1.5 s completion accent. Evidence strength MEDIUM. |

## Visual decisions

| ID | Status | Decision | Evidence / next gate |
|---|---|---|---|
| V-001 | VALIDATED | BB-P007 visual production baseline uses a 1280×720 / 16:9 landscape reference surface, an ordinary bee height of 12–15% of viewport height, orthographic Auto Cover camera semantics with a narrow zoom band, linear filtering, selective outlines, broad low-frequency terrain, and a default maximum of one objective + Honey as persistent HUD clusters. Canonical UI/motion/VFX tokens live in `config/visual-style.json`. | BB-P007 current Poki/Defold constraints + multi-product public visual benchmark + deterministic original BeBee blocking-frame generation. P1 applies bee-scale/camera, P2 validates sparse HUD/contextual world state, and P4 validates the 1.5 s major-reveal band plus HUD-hidden dormant/restored readability at desktop/Poki-small/mobile scope. Evidence strength MEDIUM; final font family and production illustration/animation/audio remain OPEN. |

### P8 release-candidate visual certification

V-001 remains VALIDATED. The P8 release candidate explicitly approves the current code-native illustrative geometry as the release-quality art direction for this scoped build: selective outlines, readable two-tone silhouettes, distinct flower families, region palettes and restrained motion/state redundancy. This is SUBJECTIVE_DIRECTION with MEDIUM evidence strength, supported by exact-head rendered captures and numeric V-001 constraints; it is not presented as an objective claim about market-wide art quality.

## Technical decisions

| ID | Status | Decision | Evidence / next gate |
|---|---|---|---|
| T-001 | LOCKED | Engine: Defold; gameplay language: Lua. | Appropriate for small 2D HTML5/mobile game. |
| T-002 | LOCKED | HTML5-first, with touch compatibility from the start. | Product target. |
| T-003 | LOCKED | Persistent content uses authored stable IDs and versioned migrations. | Save safety. P4 derives meadow stage from existing stable patch completion IDs and authored restoration contributions, so no duplicate restoration field or schema v3 is introduced. |
| T-004 | LOCKED | Gameplay state/economy/progression are not owned by GUI scripts. | Testability and separation. P4 stage evaluation is a pure domain module/data model; GUI scripts consume the derived status for presentation only. |
| T-005 | LOCKED | Platform SDKs are adapters; gameplay cannot depend directly on Poki/CrazyGames APIs. | Portability. |
| T-006 | LOCKED | Save access goes through a storage abstraction. `sys.save/sys.load` are a local adapter, not the domain API. | HTML5/platform storage differences. P4 midpoint/final lifecycle proof uses the same abstraction and restores derived GROWING/RESTORED state without a new persistence path. |
| T-007 | LOCKED | `sys.load` recovery uses protected calls and validation; public save formats are migration-tested. | Current Defold file API behavior. |
| T-008 | LOCKED | Serialized `sys.save` payload must stay well below Defold's ~512 KB output limit; CI/dev diagnostics track serialized size. | Current Defold API constraint. |
| T-009 | LOCKED | HTML5 save tests include persistence-delay cases because Defold's IndexedDB-backed virtual filesystem can persist writes asynchronously. | Current Defold HTML5 documentation. |
| T-010 | DEPRECATED | Major region/screen lifecycle uses collection proxies. | P6 and P7 show that the current authored campaign scales across two regions inside one continuous gameplay world without per-region proxy lifecycle. Replaced for current production by T-013; a separate game world may still be introduced later only from measured lifecycle/memory evidence. |
| T-011 | LOCKED | If collection proxies are used, the proxy owner participates in input focus routing; modal UI must consume/release input explicitly. | Defold input/proxy behavior. P1 retains the native nested stack: movement lives inside the proxied gameplay world instead of adding owner-side custom input forwarding. |
| T-012 | LOCKED | Significant player-facing work requires deterministic rendered evidence before merge. | Quality workflow. P4 retained exact-head HUD-hidden before/mid/after, motion, persistence and mobile evidence and passed an independent evaluation before closeout. |
| T-013 | VALIDATED | Current authored-region expansion stays data-driven inside one continuous gameplay world: active region derives from the first incomplete authored region, and patch presentation is bounded by visible complexity through a reusable visual pool rather than total catalog patch count. A separate region game world is introduced only if measured lifecycle/memory evidence requires it. | P6 validates one continuous six-Meadow Sunny Meadows region. P7 now derives Golden Fields, Wetland Garden, Rosewood, Alpine Bloom and Moon Garden sequentially after persisted completion of the preceding regions. The naive multi-region HTML5 run failed at `Out of nodes (max 512)` and later catalog growth exposed a `2040`-byte view_state limit; accepted repairs keep `max_nodes: 512`, use six reusable nearby-patch visual slots, sparsely serialize transient patch state, pass exact-head Chromium and retain P1-P7 regressions. Evidence strength MEDIUM. |

## Platform decisions

| ID | Status | Decision | Evidence / next gate |
|---|---|---|---|
| P-001 | VALIDATED | Primary external validation/distribution target is Poki; CrazyGames is the secondary/fallback portal; direct web remains the owned development/QA target and optional distribution channel. | BB-P006 current official platform/Defold comparison. If Poki access or external playtesting is unavailable when first portal audience testing is needed, switch that validation target to CrazyGames without changing gameplay-domain code. |
| P-002 | LOCKED | Architecture must support portal requirements without infecting gameplay logic. | Adapter boundary. |
| P-003 | LOCKED | First-session UX must support landing directly in gameplay or reaching gameplay with at most one intentional action when a selected portal requires it. | Current portal requirements/guidelines. |

## Process decisions

| ID | Status | Decision |
|---|---|---|
| R-001 | LOCKED | Research → official docs → implementation brief → code → build/test → screenshots/video → comparison → iteration → merge. |
| R-002 | LOCKED | Existing pre-workflow design choices are hypotheses until retroactively benchmarked or explicitly locked here. |
| R-003 | LOCKED | Subjective milestones cannot be accepted by prose alone; P2/P4/P6 require rendered evidence, objective measurements and a separate evaluation pass. Human review is optional unless the owner explicitly requests it for a specific milestone. |
| R-004 | LOCKED | Routine competitor screenshots are research material and are not committed without a compatible license. |
| R-005 | LOCKED | Substantial decisions record both decision status and decision provenance; subjective/owner choices must not be presented as externally proven facts. |
| R-006 | LOCKED | Substantial player-facing research builds a candidate pool, deeply inspects at least two problem-specific references when reasonably available, and includes a materially different solution or anti-pattern. |
| R-007 | LOCKED | Substantial player-facing/economy PRs use a machine-readable `evidence/<ticket>/manifest.json` changed in the same PR; PR prose is only a summary. |
| R-008 | LOCKED | Objective measurements are recorded before subjective scoring where observable; invented measurements are prohibited. |
| R-009 | LOCKED | Substantial player-facing changes require a separate post-implementation evaluation record; `ITERATE` blocks merge. No second human account is required by default. |
| R-010 | LOCKED | `main` must be protected by a ruleset requiring pull requests and required status checks before normal autonomous production begins. Recording an issue/blocker is not a substitute for this P-1 exit condition. |
| R-011 | LOCKED | PR `Change class` is constrained by the actual diff. An agent-declared class may never downgrade gameplay/UI/economy/high-risk runtime changes to `process`, `trivial`, or a weaker evidence class. |
| R-012 | LOCKED | High-risk technical runtime work (including core Lua, storage, platform/adapters and equivalent lifecycle-critical changes) requires a same-PR evidence manifest with official-doc constraints, alternatives, acceptance criteria and verification, even when competitor research is not applicable. |
| R-013 | LOCKED | Non-trivial acceptance criteria must all be explicitly passed before merge, and the evidence-policy validator requires adversarial negative tests for bypass cases rather than only happy-path self-validation. |
| R-014 | LOCKED | Player-facing visual/evaluation evidence is bound to the exact PR head SHA and records capture/evaluator provenance. An `independent_pass` evaluator identity must differ from the implementation-author identity. Runtime artifact existence/hash verification becomes mandatory once the P0 deterministic capture pipeline exists. |
| R-015 | LOCKED | Required PR evidence is judged by policy code from the trusted PR base/default branch; candidate PR policy code is never the authority that validates the same candidate. |
| R-016 | LOCKED | Governance-critical workflow/policy/source-of-truth changes require a same-PR governance evidence manifest with explicit trust-boundary impact, bypass analysis and rollback; they do not require a second GitHub account. |
| R-017 | DEPRECATED | Mandatory exact-head approval from a second human GitHub account for P2/P4/P6 or governance changes. | Replaced by R-003, R-009, R-016 and R-020. |
| R-018 | LOCKED | Player-facing/economy reference diversity is based on shipped-product identity (`product_id`), not URL count; multiple pages for one game cannot satisfy independent-reference counts. |
| R-019 | LOCKED | Required status checks on `main` use strict/up-to-date enforcement. **Verified satisfied 2026-08-28:** active `Protect main` ruleset 21741136 targets the default branch, requires `validate-pr-evidence`, and reports `strict_required_status_checks_policy=true`; evidence: `evidence/BB-P017-RULESET-CLOSEOUT/ruleset-snapshot.json`. |
| R-020 | LOCKED | BeBee's normal autonomous development path must not depend on maintaining a second human GitHub account/collaborator. Human review may be requested deliberately, but absence of a second reviewer is not a merge blocker. |

See `docs/16-ci-trust-boundary.md` for the enforcement design and bootstrap boundary.

## Change rule

Any PR that changes a `LOCKED` decision must:

1. state the old decision;
2. show new research/evidence;
3. explain migration/product impact;
4. update this file in the same PR.
