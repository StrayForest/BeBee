# 15 — Agent Evidence Governance

## 1. Purpose

BeBee is intended to be developed largely by autonomous coding agents without allowing the agent's taste, memory or post-hoc justification to become the product specification.

The governing rule is:

> A substantial decision is accepted because its provenance and evidence are inspectable, not because the implementing agent can write a convincing explanation.

This document turns the research-first workflow into a stricter evidence model.

---

## 2. Two separate dimensions: status and provenance

Decision status answers **how settled is this?**

- `LOCKED`
- `VALIDATED`
- `HYPOTHESIS`
- `OPEN`
- `DEPRECATED`

Decision provenance answers **why are we allowed to believe or require this?**

Use one primary provenance type for each substantial decision:

- `OWNER_CONSTRAINT` — explicit product direction chosen by the project owner; not presented as objective market evidence.
- `REFERENCE_PATTERN` — supported by observation of shipped products solving the same player problem.
- `TECH_CONSTRAINT` — follows from current official engine/platform/library behavior.
- `EXPERIMENT_RESULT` — selected after comparing prototypes or variants against defined criteria.
- `SIMULATION_RESULT` — selected because deterministic modeling/economy analysis supports it.
- `TELEMETRY_RESULT` — supported by production/player telemetry.
- `PLAYTEST_RESULT` — supported by observed user tests.
- `SUBJECTIVE_DIRECTION` — intentional art/tone/composition direction that cannot honestly be reduced to an objective measurement.

Do not relabel an owner preference or art choice as `REFERENCE_PATTERN` merely because a similar example can be found later.

---

## 3. Evidence strength

Every substantial decision record should state confidence/evidence strength:

- `LOW` — plausible direction; significant uncertainty remains.
- `MEDIUM` — multiple relevant observations or one direct experiment support it, but important uncertainty remains.
- `HIGH` — multiple independent evidence sources and/or direct BeBee experiment/playtest support the decision.

`HYPOTHESIS` normally cannot be `HIGH`.

`VALIDATED` should not be declared from popularity, one screenshot, one developer's catalog, or model intuition alone.

---

## 4. Research selection protocol

For substantial player-facing gameplay, UX/UI, progression, onboarding, art/VFX or restoration work:

1. define the exact problem before searching;
2. build a candidate pool of at least **five** plausible shipped references when reasonably available;
3. record the candidate pool even when only two or three are inspected deeply;
4. select at least **two problem-specific references** for deep observation;
5. include at least one materially different solution or anti-pattern;
6. state why each selected reference is relevant;
7. state why notable candidates were rejected or considered less relevant;
8. distinguish direct observation from inference;
9. record measurable facts where observable;
10. only then recommend a BeBee solution.

If five reasonable candidates do not exist, the research record must contain an explicit exception and explain the search limitation.

The purpose is to reduce cherry-picking and confirmation bias. The target is not consensus for its own sake; the target is to understand the solution space before committing.

---

## 5. Required alternative analysis

A substantial design decision must not jump directly from problem to chosen implementation.

Record at least:

- the selected alternative;
- one credible rejected alternative;
- why each was selected/rejected;
- the evidence or constraint behind that reason.

For high-impact unresolved mechanics, prefer three variants where practical.

"The competitor uses it" is not sufficient rationale.

A good rationale has this shape:

```text
problem
+ observed reference behavior
+ BeBee product constraint
+ technical constraint if relevant
+ prototype/simulation result if relevant
= selected alternative
```

---

## 6. Machine-readable feature evidence

For substantial feature/economy work, create a machine-readable evidence record under:

```text
evidence/<ticket>/manifest.json
```

Use `docs/templates/evidence-manifest.example.json` as the schema example.

The record must include enough structured information for CI to validate that the required process occurred. The PR body may summarize this evidence, but prose in the PR is not the source of truth.

The evidence manifest should be changed in the same PR as the implementation it evaluates.

Routine screenshots/video should normally remain CI/PR artifacts rather than repository files. The manifest records their artifact names/links when available.

---

## 7. Measure first, judge second

Prefer observable measures before subjective scores.

Examples for interaction work:

- actions/taps/clicks to primary result;
- feedback latency;
- completion duration;
- stationary waiting time;
- number of simultaneous touch controls;
- cancellation/recovery behavior;
- modal depth.

Examples for HUD/UI:

- persistent element count;
- lines of instructional text;
- approximate playfield obstruction;
- minimum touch target;
- simultaneous attention animations;
- number of visible objectives.

Subjective 1–5 ratings may remain, but they require a note and should not replace measurable evidence.

---

## 8. Independent evaluation pass

The implementation author must not be the only authority that a player-facing feature is good enough.

For substantial player-facing work, perform a separate evaluation pass after implementation and capture.

The evaluator should receive primarily:

- the original player problem;
- acceptance criteria;
- selected reference observations;
- BeBee rendered screenshots/video;
- objective measurements;
- relevant product guardrails.

Where tooling permits, do not begin the evaluation with the implementer's persuasive rationale. The evaluator should first identify gaps from the evidence.

The evaluation records:

- findings;
- severity;
- comparison outcome;
- required iteration if any;
- evaluator mode (`independent_pass` or designated human review).

`ITERATE` blocks merge.

This separation does not prove perfect independence when the same underlying model performs both passes, but it reduces post-hoc self-justification and creates a review boundary that can later be assigned to another agent/model/human without changing the workflow.

Human approval at P2, P4 and P6 remains mandatory.

---

## 9. Merge-gate philosophy

Instructions are not enforcement.

The repository should progressively enforce the workflow through GitHub checks:

- meaningful PRs must have required structured sections;
- player-facing/economy PRs must point to a changed evidence manifest;
- manifests must parse and contain required fields;
- reference URLs must be syntactically valid;
- required candidate/reference counts must pass or include an explicit exception;
- alternatives must contain exactly one selected option;
- `ITERATE` cannot merge;
- player-facing work must declare visual evidence or a valid non-applicability exception;
- acceptance/verification evidence cannot be entirely blank.

As runtime tooling appears, add required checks for HTML5 build, tests, deterministic capture and economy simulation.

GitHub `main` should be protected by a ruleset requiring pull requests and required status checks. Direct push should not be the normal path.

---

## 10. Evidence is not proof of quality by itself

Structured evidence prevents omission and makes reasoning auditable. It does not guarantee that observations are true or that a score is correct.

Therefore BeBee uses multiple layers:

```text
source-of-truth decisions
+ structured research
+ official technical docs
+ prototypes/simulation
+ automated tests
+ rendered evidence
+ separate evaluation pass
+ human milestone gates
```

No single layer replaces the others.

---

## 11. Anti-neuroslop rules

An autonomous agent must not:

- invent a feature because it would make the game "richer" without identifying a player problem;
- add a system because several games have it without showing why BeBee needs it;
- treat a familiar genre convention as mandatory;
- select only confirming references while ignoring a credible alternative;
- invent measurements that were not observed;
- turn an `OPEN` item into implementation by silent choice;
- turn a `HYPOTHESIS` into dependent architecture before its gate passes;
- call an artistic preference objective;
- self-award `PASS` without a separate evaluation record for substantial player-facing work;
- compensate for weak interaction with extra UI, particles, rewards or complexity instead of fixing the underlying problem.

The default response to insufficient evidence is **prototype/research more or keep the decision unresolved**, not invent certainty.
