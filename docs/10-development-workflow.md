# 10 — Research-First Development Workflow

## 1. Purpose

BeBee is developed with a mandatory **research -> design -> implementation -> evidence -> comparison** loop.

No player-facing feature should be implemented from memory, intuition or a vague prompt when a comparable pattern already exists in shipped games or when the engine/platform has official guidance.

The goal is not to clone competitors. The goal is to avoid relearning solved UX, interaction and technical lessons while keeping BeBee's theme, assets, code, maps, text and final expression original.

This workflow applies to humans and coding agents.

---

## 2. Mandatory feature pipeline

For every meaningful gameplay, UX, UI, rendering, save, input, economy, performance or platform task, follow these gates in order.

```text
0. Define the player/system problem
        ↓
1. Study comparable shipped games
        ↓
2. Read official technical documentation
        ↓
3. Write the implementation brief + acceptance criteria
        ↓
4. Implement the smallest complete version
        ↓
5. Build and run automated/manual checks
        ↓
6. Capture BeBee screenshots/video
        ↓
7. Compare against references and product rules
        ↓
8. Iterate until the comparison is acceptable
        ↓
9. PR with evidence
        ↓
10. Merge only after gates pass
```

Skipping a gate requires an explicit written reason in the PR.

---

# Gate 0 — Define the problem before the solution

Before research, state:

- what the player is trying to do;
- what currently prevents or weakens that experience;
- what behavior should exist when the task is complete;
- whether the task is primarily gameplay, UX/UI, content, technical infrastructure or performance;
- how the result will be verified.

Bad task:

> Add a flower popup.

Better task:

> When the bee reaches a flower that requires more Buzz, the player must understand within one second why pollination cannot begin and what upgrade solves it, without opening another menu.

Research should answer that problem rather than merely search for a visually similar screen.

---

# Gate 1 — Competitor/reference research

## 1.1 Minimum reference requirement

For player-facing work, inspect **at least two relevant shipped references when reasonably available**.

Prefer references in this order:

1. Cow Bay / Cow Castle for compact resource-progression interactions;
2. other successful accessible resource/restoration games such as Olly the Paw, My Little Universe or Dreamdale;
3. other games that solve the exact interaction better;
4. open-source projects for implementation structure, not visual authority.

One reference is acceptable when the behavior is unusually specific and no meaningful second comparison exists. Record that fact.

## 1.2 What to inspect

Do not stop at “it looks nice.” Record concrete observations relevant to the task:

- screen composition;
- HUD placement;
- visible information count;
- control method;
- interaction radius/forgiveness;
- number of actions required;
- animation timing;
- reward timing;
- feedback layers: motion, particles, sound, number changes, world change;
- locked/available/complete states;
- how the next action is communicated;
- camera behavior;
- text amount and wording density;
- tap/click target size;
- failure or blocked state;
- whether the player must open a menu;
- how the pattern changes on mobile if observable.

For economy/progression work also inspect:

- cost growth;
- reward cadence;
- time to first upgrade;
- when gates appear;
- whether the player sees the benefit before paying;
- how grind is prevented or introduced.

## 1.3 Research captures

When visual evidence matters, capture or obtain screenshots/video frames of the exact reference state being studied.

Examples:

- competitor upgrade screen;
- locked resource node;
- reward pickup feedback;
- first-session HUD;
- map unlock state;
- before/after restoration state.

Third-party screenshots are research material only.

**Do not commit competitor screenshots, ripped assets, proprietary sprites, sounds or extracted game files into this repository unless their license explicitly permits it.**

Instead, PR/research notes should contain source links, game/version/platform where known, and a short written observation. Temporary local comparison captures may be used during development.

## 1.4 What we may learn vs what we may not copy

We may reuse general patterns such as:

- sparse top HUD;
- proximity interaction;
- clear upgrade affordance;
- one-action purchasing;
- visible resource gates;
- world restoration feedback;
- joystick placement conventions.

We must not reproduce:

- maps or level layouts;
- proprietary code;
- exact art;
- exact icons;
- exact UI skin;
- dialogue/text;
- audio;
- unique character designs;
- pixel-identical screen composition where it would amount to copying expression rather than learning a pattern.

The desired outcome is **familiar interaction + original BeBee expression**.

---

# Gate 2 — Official documentation research

After understanding how users expect the feature to behave, determine how the technology should implement it.

## 2.1 Source priority

Use sources in this order:

1. official Defold manual/API/examples;
2. official platform/browser/store SDK documentation;
3. official dependency/library documentation;
4. dependency source repository and maintained examples;
5. reputable technical references only when official documentation is insufficient.

Forum posts, snippets and AI-generated answers are not the primary technical authority when official documentation exists.

## 2.2 Topics that require official-doc review

Examples include:

- Defold input and input focus;
- GUI layouts and anchors;
- collection proxies/collection factories;
- sprite/atlas animation;
- particle effects;
- sound lifecycle;
- save paths and `sys.save` / `sys.load` behavior;
- HTML5 platform behavior;
- browser storage constraints;
- mobile lifecycle/backgrounding;
- touch input;
- render predicates/materials;
- performance profiling;
- external SDK integration;
- privacy/analytics SDK behavior.

## 2.3 Research record

For each task, record:

- official pages read;
- relevant API/engine constraints;
- implementation approach selected;
- alternatives rejected and why;
- version/date when an API is version-sensitive.

Do not invent an API because its name seems plausible. Verify it.

---

# Gate 3 — Implementation brief

Before editing production code, write a compact implementation brief using `docs/templates/feature-research.md` or equivalent PR notes.

It must include:

1. problem;
2. competitor observations;
3. official documentation consulted;
4. BeBee design decision;
5. acceptance criteria;
6. technical approach;
7. save/data impact;
8. analytics impact;
9. test plan;
10. visual QA plan if player-facing.

This can live in the issue/PR rather than becoming a permanent document for every tiny task, but the evidence must exist.

For large or foundational systems, preserve the research in `docs/`.

---

# Gate 4 — Implement the smallest complete version

Implementation rules:

- solve the stated player/system problem first;
- do not add speculative adjacent systems;
- use existing BeBee architecture and data contracts;
- keep temporary assets clearly temporary;
- do not tune ten variables before one representative case works;
- prefer one polished interaction over several incomplete variants.

For visual systems, first implement the smallest state set necessary for comparison:

```text
normal
interactive/active
blocked/locked when relevant
completed/rewarded when relevant
```

---

# Gate 5 — Functional validation

Before visual judgement:

- run relevant unit tests;
- run data validation;
- build HTML5;
- execute the manual QA recipe;
- verify keyboard/touch behavior where relevant;
- verify save/reload where relevant;
- check browser console/runtime errors;
- confirm acceptance criteria mechanically where possible.

Do not polish a feature that is still logically incorrect.

---

# Gate 6 — Screenshot and video evidence

Player-facing work is not complete without looking at the rendered result.

## 6.1 Required BeBee captures

Capture representative screenshots after implementation.

Default viewports when relevant:

- desktop gameplay: **1440x900** or closest supported deterministic test viewport;
- narrow/mobile portrait: **390x844** or equivalent representative viewport;
- landscape mobile/tablet where the feature changes materially.

Use additional states when necessary:

- before interaction;
- during interaction;
- after completion;
- locked state;
- menu open;
- dense/worst-case layout.

Animation/timing work should also use short video/GIF or frame sequence where tooling permits.

## 6.2 Evidence retention

Our own screenshots may be attached to PRs or stored as CI artifacts.

Do not permanently fill the repository with routine screenshot output unless the image is an approved golden/reference asset used by visual regression tests.

---

# Gate 7 — Visual comparison review

Compare the implemented BeBee state with the researched references and with BeBee's own art/UX rules.

The question is not “are they identical?” The questions are:

### Hierarchy

- Can the eye find the current objective immediately?
- Is currency/status visible without dominating the world?
- Is the primary interaction more obvious than secondary UI?

### Simplicity

- Are we requiring more taps/clicks than the reference without a good reason?
- Is there text the world itself could communicate?
- Are there unnecessary panels, badges or persistent icons?

### Readability

- Is the bee readable against the terrain?
- Are flower states distinguishable at gameplay zoom?
- Are locked/active/completed states unmistakable?
- Are mobile targets comfortably tappable?

### Feedback

- Does interaction begin immediately enough?
- Does progress visibly change?
- Does reward arrival feel connected to the completed action?
- Does the world visibly improve after restoration?

### Composition

- Does HUD obscure play space?
- Is empty space intentional?
- Are important elements too close to screen edges/notches?
- Is the camera framing useful rather than decorative?

### Character and originality

- Does the result feel like BeBee rather than a reskin of Cow Bay?
- Are bee, honey, pollen, flower and restoration motifs doing meaningful work?
- Have we learned the interaction pattern without copying proprietary expression?

## 7.1 Required comparison conclusion

Record one of:

- `PASS — at or above reference quality for the target problem`;
- `PASS WITH DEVIATION — intentionally different; reason documented`;
- `ITERATE — visible/interaction gap remains`.

If the result is `ITERATE`, the task is not done.

---

# Gate 8 — Iterate

Typical reasons to iterate:

- UI is denser than references;
- interaction requires unnecessary confirmation;
- feedback is late or weak;
- objective is less obvious;
- mobile layout collapses;
- bee/flowers are too small;
- reward is visually disconnected from the action;
- camera framing wastes useful space;
- restoration before/after difference is weak;
- implementation technically works but feels slower or less legible.

Change the smallest thing likely to fix the observed gap, rebuild, capture again and compare again.

Avoid random polish passes without a stated deficiency.

---

# Gate 9 — Pull request evidence

Every meaningful PR must answer:

### Research

- Which comparable games/features were inspected?
- What relevant behavior was observed?
- Which official docs were read?

### Decision

- What pattern did BeBee adopt?
- What did we deliberately do differently?

### Verification

- Which tests/builds passed?
- Which manual cases were checked?
- Which save/data migrations apply?

### Visual evidence

For player-facing work:

- BeBee screenshots/video attached;
- reference links or descriptions included;
- comparison conclusion included;
- notable visual differences explained.

A PR description that only says “implemented feature X” is insufficient.

---

# Gate 10 — Merge gate

Do not merge meaningful feature work when any of the following is true:

- no competitor/reference research was performed where relevant;
- an engine/platform behavior was implemented from assumption rather than official docs;
- acceptance criteria are missing;
- HTML5 build is broken;
- relevant tests fail;
- player-facing work has no rendered screenshot/video evidence;
- obvious visual/interaction regression remains compared with the selected references;
- copyright/license provenance is unclear;
- save compatibility is knowingly broken without migration/explicit reset decision.

---

## 3. Exceptions

The full workflow is unnecessary for trivial work such as:

- typo fixes;
- internal comments;
- mechanical renames with no behavior change;
- isolated test maintenance;
- CI metadata changes that do not affect product behavior.

However, “small code diff” does not automatically mean “trivial.” A two-line input or save change can have major player impact and still requires research/testing.

---

## 4. Research depth by task type

| Task | Competitor research | Official docs | Screenshots/comparison |
|---|---|---|---|
| Player-facing gameplay | Required | Required when technical API involved | Required |
| UI/HUD/menu | Required | Required | Required |
| Economy/progression | Required | As applicable | Required for visible UX states |
| Input/camera | Required | Required | Required; video preferred for feel |
| Save/data | Optional competitor research | Required | Not required unless UI changes |
| Performance/rendering | Reference targets useful | Required | Required when rendering changes |
| CI/tooling | Usually not required | Required for tool/API behavior | Not required |
| Art/VFX/audio | Required | Tool docs as applicable | Required |

---

## 5. Feature research template

Use:

`docs/templates/feature-research.md`

The template is intentionally short enough to complete for every substantial feature. The goal is disciplined thinking, not paperwork.

---

## 6. Core rule for AI agents

An agent working autonomously on BeBee must not interpret “implement BB-xxx” as permission to immediately write code.

The expected behavior is:

1. read the relevant BeBee docs;
2. research the exact competitor pattern;
3. read the relevant current official developer documentation;
4. record the intended implementation;
5. code;
6. build/test;
7. render the game;
8. capture screenshots/video;
9. inspect the captures;
10. compare with references;
11. revise when needed;
12. only then propose merge.

**Code generation is the middle of the task, not the beginning or the end.**
