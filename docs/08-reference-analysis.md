# 08 — Reference Analysis

## 1. Purpose

References are used to learn proven interaction, information hierarchy, pacing and technical decomposition. They are not permission to copy proprietary code, art, maps, text, audio or distinctive expression.

Research snapshot: 2026-08-28.

Important audit correction: the original reference pass was useful for broad product direction but was **not deep enough to validate exact BeBee interaction/UI decisions**. Those decisions are now hypotheses until problem-specific research/prototypes pass.

## 2. Primary broad references

### Cow Bay — 7Spot Games

Useful for:

- immediate simple action;
- compact objective progression;
- gathering -> improvement -> new area cadence;
- browser/mobile accessibility;
- gradual addition of systems.

Do not infer from Cow Bay alone that BeBee should use its exact interaction method, HUD placement, economy values or progression timing.

### Cow Castle — 7Spot Games

Useful for:

- simple movement-centric control;
- resources feeding visible world construction;
- compact spatial unlocks;
- concrete long-term visual goal.

### Olly the Paw — 7Spot Games

Useful for:

- cute/simple presentation;
- one sentence-level macro objective;
- physical visualization of long-term completion;
- delayed helper/automation complexity.

### My Little Universe

Useful for:

- visible future gated areas;
- power/efficiency progression;
- spatial expansion;
- world transformation as reward.

Do not import its multi-resource/tool complexity by default.

### Dreamdale

Useful for:

- upgrade readability;
- map expansion;
- observing grind/attention/camera anti-patterns.

### Forager

Useful for:

- compact loop feeding expansion;
- land/world as progression reward;
- completionist structure.

Do not import crafting-system complexity.

## 3. Open-source implementation references

### PurrNet Incremental Sample

Research-only unless separately licensed/imported.

Useful concepts:

- data-driven upgrades;
- resource-node state separated from player/economy;
- end-to-end loop before content scale;
- pooling only where useful.

Do not import networking/Unity architecture into production BeBee.

### benjames-171/defold-games

Useful as small Defold implementation examples.

Rules:

- verify every API/pattern against current Defold docs;
- old samples are not authority for current engine behavior;
- do not bulk-copy unrelated systems.

### Godot/farming projects

Use only for conceptual decomposition questions. Cross-engine code is not pasted into BeBee.

## 4. Official technical authorities

For implementation behavior, prefer current official docs:

- Defold manuals/API/examples;
- selected portal's official requirements/SDK docs;
- official dependency/library docs.

Relevant Defold topics include:

- input focus;
- collection proxies;
- GUI/layout;
- HTML5 lifecycle/file behavior;
- `sys.save/sys.load`;
- profiling;
- audio/particles/rendering;
- official Poki/CrazyGames extensions if selected.

## 5. Problem-specific benchmark matrix

P-1 must create research for each problem rather than treating “Cow Bay” as the answer to every question.

| Problem | Minimum benchmark focus |
|---|---|
| movement feel | responsiveness, acceleration, camera, obstacle forgiveness, touch scheme |
| pollination/core verb | action count, agency, waiting, repeatability, mobile ergonomics, feedback start |
| locked/harder flowers | aspiration, requirement clarity, soft vs hard gate behavior |
| Honey reward | reward attribution, timing, animation, counter feedback |
| improvements | purchase actions, current/next effect clarity, affordability, immediate felt benefit |
| HUD | persistent element count, objective hierarchy, obstruction, mobile adaptation |
| onboarding | time to first input/core verb, text amount, direct-to-gameplay behavior |
| restoration | strength of before/after world change, staging, celebration |
| seeds/customization | when choice occurs, preview, reversibility, ownership, progression safety |
| planet/map | macro-goal clarity, region progression, next-goal visibility |

For each row, references may come from different games. Choose the best solver of the problem rather than the most superficially similar title.

## 6. What to record

For player-facing research capture observable facts where possible:

- platform/version/date;
- actions required;
- approximate time to first feedback;
- time to result;
- persistent HUD element count;
- modal/panel depth;
- locked/active/complete states;
- camera behavior;
- reward timing;
- mobile behavior;
- what is directly observed vs inferred.

Use `docs/templates/feature-research.md` and `docs/13-visual-qa-scorecard.md`.

## 7. Current broad lessons that remain valid

These are patterns, not exact implementations:

- first meaningful interaction should happen quickly;
- complexity should be layered;
- future desirable content should be visible where useful;
- permanent capability improvements should be felt, not only described;
- one clear objective can outperform a dense quest system;
- world transformation is stronger than a number alone;
- task-specific menus should remain shallow;
- gameplay should remain understandable on desktop and touch;
- a cute simple macro goal can carry a lightweight economy.

## 8. Decisions explicitly reopened after audit

The following are **not validated merely because the original reference analysis mentioned them**:

- movement + proximity auto-pollination;
- exact HUD placement;
- fixed three-card Flight/Buzz/Yield upgrade screen;
- title screen before onboarding;
- post-restoration-only customization;
- exact first-region timing/economy values.

Their current status lives in `DECISIONS.md`.

## 9. Reuse/legal boundary

When learning from a reference:

1. state the player problem;
2. identify the general pattern;
3. build BeBee's own expression and code;
4. separately review any third-party code/asset license before incorporation;
5. record incorporated material in `THIRD_PARTY.md`.

Do not commit competitor screenshots, ripped assets, proprietary sprites, sounds or extracted files unless their license explicitly permits redistribution.

## 10. Reference quality rule

A reference is useful only if it helps answer a concrete question. “The competitor has it” is not a product justification.

A BeBee feature may intentionally differ when evidence shows the difference better supports:

- bee movement fantasy;
- restoration ownership;
- simpler Honey economy;
- lower interaction cost;
- better mobile behavior;
- clearer visual hierarchy;
- stronger originality.
