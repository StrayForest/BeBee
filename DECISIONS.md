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
| D-001 | LOCKED | Core fantasy: a cute bee restores a planet by pollinating flowers and shaping what blooms. | Product brief. |
| D-002 | LOCKED | MVP uses one core currency: Honey. | Simplicity/product pillar. |
| D-003 | LOCKED | No mandatory combat, hard energy timer, premium currency, multiplayer or backend account in the vertical slice. | Scope control. |
| D-004 | LOCKED | World is authored as regions/meadows/patches; not an infinite procedural world. | Pacing/readability/performance. |
| D-005 | VALIDATED | Hybrid seed/restoration topology: during restoration, authored native campaign plots keep their native/campaign identity while dedicated player-shaped plots may accept owned seeds; player-shaped plots never gate campaign completion. After restoration, completed native plots may become replantable where content allows. Campaign/native identity and current planted species remain separate state. | BB-P004 deterministic A/B/C structural experiment + reference analysis. Native-first produced no ownership before restoration; fully player-shaped allowed an incomplete native campaign plot to display a conflicting chosen species; Hybrid preserves early ownership without overloading active native objectives. Evidence strength MEDIUM; P5 must validate rendered comprehension, exact plot count/placement, planting input and seed pacing. |
| D-006 | VALIDATED | Primary pollination interaction is movement-through/sweep: qualifying movement while inside a pollinatable patch advances progress; standing still does not, and the default scheme has no separate high-frequency pollination button. Exact movement/work target remains tunable. | BB-P003 A/B/C browser experiment + reference analysis. Auto produced substantial stationary patch time; Hold retained stationary time and added a second touch control; Sweep preserved movement ownership with zero stationary progress and no extra pollination input. Evidence strength MEDIUM; P2 tunes forgiving bounds/work target and accidental fly-through behavior. |
| D-007 | VALIDATED | Vertical-slice bee upgrade tracks are **Flight + Buzz**. Yield is excluded from the vertical slice; do not add a replacement track merely to preserve three cards. Exact Flight/Buzz effect curves remain tunable. | BB-P005 deterministic economy analysis. Removing Yield still gives 5040/5040 full retained-sink purchase-priority orders reaching region completion with zero replay and non-negative balance. Historical 1.15x Yield repays only at M06: earliest timing ends +11 Honey vs no Yield, mid -1 and late -15; sensitivity shifts it between no-payback and stronger-opener behavior. Evidence strength MEDIUM; P1/P3 tune direct Flight/Buzz feel and final costs. |
| D-008 | HYPOTHESIS | Sparse HUD: one objective plus Honey, with contextual world-space interaction. | V-001 validates the default density ceiling (one objective + Honey); exact contextual/world-space interaction behavior still requires runtime screen benchmark and visual QA. |
| D-009 | LOCKED | Progress/customization choices must not create an unrecoverable grind or punish aesthetics. | Product rule. |
| D-010 | LOCKED | MVP world gates should use restoration/progression/Buzz by default, not Honey payments. | Prevents spending seeds from blocking campaign progress. Any Honey gate requires new evidence. |
| D-011 | HYPOTHESIS | Six-meadow first-region structure: First Patch, Clover Bend, Lavender Bank, Creek Garden, Tulip Rise, Lily Clearing. | Validate pacing after core loop prototype. |
| D-012 | LOCKED | Canonical proposed region order is Sunny Meadows → Golden Fields → Wetland Garden → Rosewood → Alpine Bloom → Moon Garden. | Resolves previous Lavender Hills/Rosewood contradiction. Later regions remain content proposals, not production commitments. |

## Visual decisions

| ID | Status | Decision | Evidence / next gate |
|---|---|---|---|
| V-001 | VALIDATED | BB-P007 visual production baseline uses a 1280×720 / 16:9 landscape reference surface, an ordinary bee height of 12–15% of viewport height, orthographic Auto Cover camera semantics with a narrow zoom band, linear filtering, selective outlines, broad low-frequency terrain, and a default maximum of one objective + Honey as persistent HUD clusters. Canonical UI/motion/VFX tokens live in `config/visual-style.json`. | BB-P007 current Poki/Defold constraints + multi-product public visual benchmark + deterministic original BeBee blocking-frame generation. Evidence strength MEDIUM. BB-P008/P0 must prove/tune the contract against retained Defold HTML5 captures; final font family and final illustration/animation assets remain OPEN. |

## Technical decisions

| ID | Status | Decision | Evidence / next gate |
|---|---|---|---|
| T-001 | LOCKED | Engine: Defold; gameplay language: Lua. | Appropriate for small 2D HTML5/mobile game. |
| T-002 | LOCKED | HTML5-first, with touch compatibility from the start. | Product target. |
| T-003 | LOCKED | Persistent content uses authored stable IDs and versioned migrations. | Save safety. |
| T-004 | LOCKED | Gameplay state/economy/progression are not owned by GUI scripts. | Testability and separation. |
| T-005 | LOCKED | Platform SDKs are adapters; gameplay cannot depend directly on Poki/CrazyGames APIs. | Portability. |
| T-006 | LOCKED | Save access goes through a storage abstraction. `sys.save/sys.load` are a local adapter, not the domain API. | HTML5/platform storage differences. |
| T-007 | LOCKED | `sys.load` recovery uses protected calls and validation; public save formats are migration-tested. | Current Defold file API behavior. |
| T-008 | LOCKED | Serialized `sys.save` payload must stay well below Defold's ~512 KB output limit; CI/dev diagnostics track serialized size. | Current Defold API constraint. |
| T-009 | LOCKED | HTML5 save tests include persistence-delay cases because Defold's IndexedDB-backed virtual filesystem can persist writes asynchronously. | Current Defold HTML5 documentation. |
| T-010 | HYPOTHESIS | Major region/screen lifecycle uses collection proxies. | Valid pattern, but P0 must verify memory/input ownership before scaling. |
| T-011 | LOCKED | If collection proxies are used, the proxy owner participates in input focus routing; modal UI must consume/release input explicitly. | Defold input/proxy behavior. |
| T-012 | LOCKED | Significant player-facing work requires deterministic rendered evidence before merge. | Quality workflow. |

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
| R-018 | LOCKED | Player-facing/economy reference diversity is based on shipped-product identity (`product_id`), not URL count; multiple pages for one product cannot satisfy independent-reference counts. |
| R-019 | LOCKED | Required status checks on `main` must use strict/up-to-date enforcement; the existing loose ruleset remains a P-1 settings blocker until GitHub reports strict required status checks enabled. |
| R-020 | LOCKED | BeBee's normal autonomous development path must not depend on maintaining a second human GitHub account/collaborator. Human review may be requested deliberately, but absence of a second reviewer is not a merge blocker. |

See `docs/16-ci-trust-boundary.md` for the enforcement design and bootstrap boundary.

## Change rule

Any PR that changes a `LOCKED` decision must:

1. state the old decision;
2. show new research/evidence;
3. explain migration/product impact;
4. update this file in the same PR.
