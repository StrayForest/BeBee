# 11 — Blueprint Hardening

This document records the audit corrections that had to be completed before normal gameplay production could begin.

**P-1 status: COMPLETE. P0 / BB-001 may begin.**

Closeout evidence: `docs/research/BB-P017-ruleset-closeout.md` and `evidence/BB-P017-RULESET-CLOSEOUT/`.

## 1. Why P-1 existed

The first blueprint established a coherent direction, but several product choices were written as decisions before the repository adopted research-first development. P-1 converted those assumptions into explicit `VALIDATED`, `LOCKED`, `HYPOTHESIS` or `OPEN` decisions and established an autonomous evidence/merge path before Defold production work.

P-1 completion validates the **blueprint structure and governance**, not final runtime tuning. Exact feel, timing, production values and rendered comprehension still belong to the milestones that have a runnable game.

## 2. Audit correction results

### 2.1 Pollination — VALIDATED movement-through / sweep

BB-P003 compared proximity auto-pollination, hold-to-pollinate and movement-through/sweep.

`D-006 VALIDATED`:

> Qualifying movement while inside a pollinatable patch advances progress; standing still does not, and the default scheme has no separate high-frequency pollination button.

Why the old assumption was rejected:

- proximity Auto produced the predicted stationary `move -> wait -> move` behavior;
- Hold restored explicit intent but still allowed stationary completion and added another touch control;
- Sweep preserved movement ownership without a separate pollination action.

P2 still tunes forgiving bounds, work target, incidental fly-through progress and accessibility alternatives in the production runtime.

### 2.2 Seeds/restoration — VALIDATED Hybrid topology

BB-P004 compared native-first, fully player-shaped and Hybrid restoration models.

`D-005 VALIDATED`:

> During restoration, authored native campaign plots keep native/campaign identity while dedicated player-shaped plots may accept owned seeds. Player-shaped plots never gate campaign completion. Campaign/native identity and current planted species are separate state concepts.

Hybrid was selected because it provides ownership during restoration without making an active native objective carry conflicting native and player-selected identities.

P5 still validates rendered comprehension, exact plot count/placement, planting input, establishment behavior and seed pacing.

### 2.3 Honey gates — LOCKED out of default MVP world progression

Honey is for:

- improving the bee;
- unlocking flower/seed expression where applicable.

Campaign/world gates default to:

- restoration completion;
- Buzz/progression requirements;
- authored objective completion.

This remains `D-010 LOCKED`: aesthetic spending must not punish world access.

### 2.4 Upgrade set — VALIDATED Flight + Buzz; Yield excluded

BB-P005 resolved the previous three-track hypothesis.

`D-007 VALIDATED`:

- vertical-slice upgrade tracks are **Flight + Buzz**;
- Yield is excluded from the vertical slice;
- no replacement track is added merely to preserve three cards.

Economy evidence after removing Yield:

- **5040 / 5040** full purchase-priority orders across Buzz 2/3, Flight 2/3 and three seed sinks reach region completion;
- required replay actions: **0**;
- negative-balance paths: **0**;
- buying all seven retained sinks leaves **271 Honey** under the current structural candidate.

Historical Yield evidence is retained as a regression counterexample: the 1.15x candidate only beats no-Yield when bought at the earliest allowed timing, repays at M06, and becomes worse when bought later. It remains research-only.

Exact Flight/Buzz effects and Honey values are runtime tuning, not P-1 production constants.

### 2.5 Open tuning is intentional, not a P-1 failure

The following remain intentionally tunable/open for downstream milestones:

- movement acceleration/speed/camera feel;
- pollination work target and forgiving bounds;
- exact Honey rewards/costs and time/actions between purchases;
- final Flight/Buzz effect curves and flower gates;
- rendered Hybrid plot language and seed interaction;
- production Defold proof of V-001 visual/crop rules;
- production HTML5 storage timing/recovery behavior.

These are not disguised as completed facts in `DECISIONS.md`.

## 3. Source-of-truth ownership

| Concern | Owner |
|---|---|
| Product pillars and scope | `00-product-vision.md` + `DECISIONS.md` |
| Core interaction rules | `01-game-design.md` |
| Costs/rewards/stat curves | `02-progression-economy.md` |
| HUD/screens/input presentation | `03-ux-ui-controls.md` |
| Region/meadow/flower roster | `04-world-content.md` |
| Technical contracts | `05-technical-architecture.md` |
| Execution order | `06-production-roadmap.md` |
| Test/release criteria | `07-qa-analytics-release.md` |
| Evidence/provenance governance | `15-agent-evidence-governance.md` |
| CI trust boundary | `16-ci-trust-boundary.md` |
| Global decisions/status | `DECISIONS.md` |

Do not duplicate canonical numeric values in multiple documents. Other documents should link to the owner.

## 4. P-1 mandatory work — completion record

| Task | Result |
|---|---|
| BB-P001 — Documentation consistency | COMPLETE — decision registry, precedence and ownership model in place; unresolved assumptions explicitly classified. |
| BB-P002 — Retroactive competitor benchmark | COMPLETE — problem-specific reference analysis and research-first workflow established. |
| BB-P003 — Pollination prototypes | COMPLETE — `D-006 VALIDATED` movement-through/sweep. |
| BB-P004 — Seed/restoration prototype | COMPLETE — `D-005 VALIDATED` Hybrid topology. |
| BB-P005 — Economy simulation | COMPLETE — `D-007 VALIDATED` Flight + Buzz; no-Yield 5040-order safety envelope. |
| BB-P006 — Primary web distribution | COMPLETE — `P-001 VALIDATED`: Poki primary, CrazyGames fallback, direct web owned QA target. |
| BB-P007 — Visual style bible | COMPLETE — `V-001 VALIDATED` measurable baseline and `config/visual-style.json`. |
| BB-P008 — Deterministic visual QA design | COMPLETE — runtime QA/capture contract specified for P0 implementation. |
| BB-P009 — HTML5 storage specification | COMPLETE — save/recovery contract and browser-risk matrix specified. |
| BB-P010 — Agent context/decision model | COMPLETE — always-read and task-specific context rules established. |
| BB-P011 — Reusable agent skills | COMPLETE — repository-local research/Defold/visual/economy checklists in place. |
| BB-P012 — Quality-gate enforcement design | COMPLETE — autonomous evidence/merge architecture defined. |
| BB-P013 — Machine-readable evidence schema | COMPLETE — substantial evidence uses `evidence/<ticket>/manifest.json`. |
| BB-P014 — Research selection protocol | COMPLETE — candidate-pool, deep-reference and anti-confirmation requirements enforced. |
| BB-P015 — Decision provenance model | COMPLETE — status, provenance and evidence strength separated. |
| BB-P016 — Independent evaluator protocol | COMPLETE — separate evaluation and `ITERATE` blocking semantics established. |
| BB-P017 — Hard merge gates | COMPLETE — trusted-base evidence validation and strict protected-main ruleset verified. |

## 5. P-1 exit criteria — PASS

| Exit criterion | Evidence | Status |
|---|---|---|
| Audit contradictions resolved or explicitly classified | `DECISIONS.md` precedence/status model; stale pollination/seed/Yield assumptions resolved | PASS |
| Pollination validation decision | `D-006`, BB-P003 | PASS |
| Seed/restoration validation decision | `D-005`, BB-P004 | PASS |
| No-grind first-region economy | BB-P005; 5040/5040 retained-sink orders, zero replay/negative paths | PASS |
| Intentional upgrade set | `D-007`: Flight + Buzz, Yield excluded | PASS |
| Primary distribution target selected | `P-001`: Poki primary | PASS |
| Visual style/QA approach defined | `V-001`, `config/visual-style.json`, `docs/18-deterministic-visual-qa.md` | PASS |
| Storage abstraction / HTML5 save risks specified | `T-006`–`T-009`, `config/storage-contract.json`, `docs/12-platform-storage.md` | PASS |
| Agent reading/decision rules | `AGENTS.md` + evidence governance docs | PASS |
| Provenance/evidence-strength rules | `R-005`, BB-P015 | PASS |
| Machine-readable substantial evidence | `R-007`, BB-P013/017 | PASS |
| Anti-confirmation research discipline | `R-006`, `R-018`, BB-P014 | PASS |
| Separate player-facing evaluation | `R-009`, BB-P016 | PASS |
| Semantic PR evidence CI | trusted-base validators + adversarial policy tests | PASS |
| Protected `main` with required PR/check | active `Protect main` ruleset 21741136 | PASS |
| Strict/up-to-date required checks | `strict_required_status_checks_policy=true` | PASS |
| No mandatory human merge dependency | required approvals `0`, required reviewers none, bypass actors none | PASS |

Ruleset evidence is retained in `evidence/BB-P017-RULESET-CLOSEOUT/ruleset-snapshot.json`. The live GitHub ruleset remains the authority for current external repository-setting state.

**P-1 exit verdict: PASS.**

## 6. Autonomous milestone checkpoints

P2, P4 and P6 are evidence checkpoints before scaling:

- end of P2 — core pollination loop;
- end of P4 — first full restoration transformation;
- end of P6 — shippable vertical slice.

For each checkpoint the agent supplies the runnable artifact, deterministic captures/motion evidence, objective measurements, comparison scorecard, acceptance/test results, known deviations and a separate evaluation verdict. `ITERATE` blocks progression.

No human review or approval is required. A human may inspect or comment when desired, but the absence of a human action cannot block CI, merge or the next phase.

## 7. Handoff to P0

Normal production may now proceed to **P0 / BB-001 — Defold bootstrap**.

P0 should implement the runtime contracts P-1 specified rather than reopening them without evidence. Where P-1 deliberately left a runtime value tunable, P0/P1/P2/P3/P5 should measure it in the actual Defold build instead of treating a prototype number as production truth.
