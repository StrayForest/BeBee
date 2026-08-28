# Feature Research Template

Use for substantial gameplay, UX/UI, economy, input, rendering, save, platform or performance work.

For substantial player-facing/economy work, also create `evidence/<ticket>/manifest.json` using `docs/templates/evidence-manifest.example.json`. The manifest is the machine-readable source of truth; this document/PR note is the human-readable working record.

## Task

- Ticket:
- Change class (`player-facing` / `economy` / `technical` / `process` / `trivial`):
- Feature/problem:
- Player/system outcome:
- Relevant decision IDs from `DECISIONS.md`:
- Current status (`LOCKED` / `VALIDATED` / `HYPOTHESIS` / `OPEN`):
- Decision provenance type:
- Evidence strength (`LOW` / `MEDIUM` / `HIGH`):

## 1. Problem definition

- What is the player/system trying to accomplish?
- What friction/uncertainty exists now?
- What observable behavior means the problem is solved?
- What is intentionally out of scope?

## 2. Reference search space

For substantial player-facing/economy work, build a candidate pool before choosing deep references.

| Candidate | Source | Why plausible | Deep inspect? | Rejection/selection note |
|---|---|---|---:|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

Candidate-pool exception if fewer than five reasonable shipped references exist:

Materially different solution / anti-pattern:

- Source:
- Direct observation:
- Lesson for BeBee:

## 3. Comparable shipped references

### Reference A
- Game / feature:
- Platform/version/date if relevant:
- Source/link:
- Why selected:
- Directly observed behavior:
- Inference (kept separate):
- Measurable notes (actions/timing/stationary wait/HUD/state/etc.):
- Useful pattern:
- What must not be copied:

### Reference B
- Game / feature:
- Platform/version/date if relevant:
- Source/link:
- Why selected:
- Directly observed behavior:
- Inference (kept separate):
- Measurable notes:
- Useful pattern:
- What must not be copied:

If only one meaningful reference exists, explain why.

Do not use only one developer's catalog when a different game solves the exact problem better. Do not select only evidence that confirms the initially preferred solution.

## 4. Official technical documentation

- Official source 1:
- Official source 2:
- Relevant constraints/API behavior:
- Version/date-sensitive details:
- Error/lifecycle cases to test:

If not applicable, state the reason rather than inventing technical citations.

## 5. Alternatives and BeBee decision

List credible alternatives before selecting one.

| Alternative | Selected/rejected | Evidence-backed reason |
|---|---|---|
| | | |
| | | |

- Pattern adopted:
- Intentional deviations from references:
- Why this fits BeBee:
- Decision provenance type:
- Evidence strength:
- Decision status after this work should become:
- `DECISIONS.md` update required? yes/no

## 6. Acceptance criteria

- [ ]
- [ ]
- [ ]

## 7. Technical plan

- Modules/files affected:
- Data model impact:
- Save/migration impact:
- Analytics impact:
- Platform/SDK impact:
- Performance/load risks:
- Accessibility/input considerations:
- Dependency/license impact:

## 8. Verification plan

### Automated
- [ ] unit/data tests
- [ ] HTML5 build
- [ ] migration/storage tests if relevant
- [ ] economy simulation if relevant
- [ ] deterministic visual state/capture if relevant

### Manual/runtime
- [ ] keyboard path if relevant
- [ ] touch path if relevant
- [ ] save/reload if relevant
- [ ] blocked/error state if relevant
- [ ] browser console/runtime errors checked
- [ ] selected portal/device-specific case if relevant

## 9. Visual QA plan

Required for player-facing work. Follow `docs/13-visual-qa-scorecard.md`.

Capture states:
- [ ] idle/before
- [ ] active interaction
- [ ] completed/reward
- [ ] locked/error if relevant
- [ ] dense/worst case if relevant
- [ ] mobile/portal layout if relevant
- [ ] video/frame sequence for motion/timing when relevant

Development defaults until portal-specific sizes are selected:
- desktop: 1440x900
- mobile portrait: 390x844

## 10. Post-implementation comparison

### Objective measurements first

| Measurement | Reference A | Reference B | BeBee | Finding |
|---|---:|---:|---:|---|
| Actions to primary result | | | | |
| Feedback latency | | | | |
| Completion time | | | | |
| Stationary wait | | | | |
| Persistent HUD count | | | | |
| Instruction lines | | | | |
| Modal depth / playfield obstruction | | | | |
| Simultaneous touch controls | | | | |

### Anchored subjective scores

Use the anchors in `docs/13-visual-qa-scorecard.md`; every score needs a note.

| Criterion | Reference A | Reference B | BeBee | Finding/note |
|---|---:|---:|---:|---|
| Objective clarity (1–5) | | | | |
| State readability (1–5) | | | | |
| Feedback quality (1–5) | | | | |
| Mobile comfort (1–5) | | | | |
| World transformation (1–5) | | | | |
| Original BeBee expression (1–5) | n/a | n/a | | |

Mark non-applicable rows rather than inventing measurements.

## 11. Separate evaluation pass

Required for substantial player-facing work after captures exist.

Evaluator should begin primarily from:

- original player problem;
- acceptance criteria;
- selected reference observations;
- rendered BeBee evidence;
- objective measurements;
- BeBee product guardrails.

Record:

- Evaluation mode (`independent_pass` / human):
- Findings/severity:
- Acceptance/reference gaps:
- Required iteration:
- Verdict (`PASS` / `PASS WITH DEVIATION` / `ITERATE`):

Do not use the implementer's persuasive rationale as proof that the rendered result succeeds.

## 12. Conclusion

Choose one:

- [ ] PASS — problem solved with no meaningful reference-quality gap
- [ ] PASS WITH DEVIATION — intentionally different and evidence-backed
- [ ] ITERATE — not ready to merge

For P2/P4/P6 milestone gates:

- Human approval required? yes/no
- Human approval evidence/link:

## 13. Evidence

- Evidence manifest:
- BeBee screenshots/video:
- Reference links/captures used during research:
- Test/build evidence:
- Simulation/profile evidence:
- Known limitations:
- Follow-up tickets:
