# Feature Research Template

Use for substantial gameplay, UX/UI, economy, input, rendering, save, platform or performance work.

## Task

- Ticket:
- Feature/problem:
- Player/system outcome:
- Relevant decision IDs from `DECISIONS.md`:
- Current status (`LOCKED` / `VALIDATED` / `HYPOTHESIS` / `OPEN`):

## 1. Problem definition

- What is the player/system trying to accomplish?
- What friction/uncertainty exists now?
- What observable behavior means the problem is solved?
- What is intentionally out of scope?

## 2. Comparable shipped references

### Reference A
- Game / feature:
- Platform/version/date if relevant:
- Source/link:
- Directly observed behavior:
- Measurable notes (actions/timing/HUD/state/etc.):
- Useful pattern:
- What must not be copied:

### Reference B
- Game / feature:
- Platform/version/date if relevant:
- Source/link:
- Directly observed behavior:
- Measurable notes:
- Useful pattern:
- What must not be copied:

If only one meaningful reference exists, explain why.

Do not use only one developer's catalog when a different game solves the exact problem better.

## 3. Official technical documentation

- Official source 1:
- Official source 2:
- Relevant constraints/API behavior:
- Version/date-sensitive details:
- Error/lifecycle cases to test:

## 4. BeBee decision

- Pattern adopted:
- Intentional deviations from references:
- Why this fits BeBee:
- Decision status after this work should become:
- `DECISIONS.md` update required? yes/no

## 5. Acceptance criteria

- [ ]
- [ ]
- [ ]

## 6. Technical plan

- Modules/files affected:
- Data model impact:
- Save/migration impact:
- Analytics impact:
- Platform/SDK impact:
- Performance/load risks:
- Accessibility/input considerations:
- Dependency/license impact:

## 7. Verification plan

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

## 8. Visual QA plan

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

## 9. Post-implementation comparison

| Criterion | Reference A | Reference B | BeBee | Finding |
|---|---:|---:|---:|---|
| Actions to primary result | | | | |
| Time to first feedback | | | | |
| Persistent HUD count | | | | |
| Objective clarity (1–5) | | | | |
| State readability (1–5) | | | | |
| Feedback quality (1–5) | | | | |
| Mobile comfort (1–5) | | | | |
| World transformation (1–5) | | | | |
| Original BeBee expression (1–5) | n/a | n/a | | |

Mark non-applicable rows rather than inventing measurements.

### Qualitative notes

- Hierarchy:
- Simplicity/action cost:
- Readability:
- Feedback/timing:
- Playfield obstruction:
- Mobile/platform behavior:
- Original BeBee expression:

## 10. Conclusion

Choose one:

- [ ] PASS — problem solved with no meaningful reference-quality gap
- [ ] PASS WITH DEVIATION — intentionally different and evidence-backed
- [ ] ITERATE — not ready to merge

For P2/P4/P6 milestone gates:

- Human approval required? yes/no
- Human approval evidence/link:

## 11. Evidence

- BeBee screenshots/video:
- Reference links/captures used during research:
- Test/build evidence:
- Simulation/profile evidence:
- Known limitations:
- Follow-up tickets:
