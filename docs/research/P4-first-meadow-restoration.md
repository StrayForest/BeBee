# P4 — First Meadow Restoration research

Date checked: **2026-08-29**

## Player problem

The first BeBee meadow must make the player's existing pollination actions visibly improve the place. A new player should be able to distinguish dormant, partially recovering and restored states from the world itself, not from a modal explanation or a HUD label. Restoration must remain part of the existing movement-through-pollination loop and survive reload.

This is not research for a new restoration minigame, a new currency, a seed system or a second progression surface. P4 is specifically the visual/system payoff for the P2/P3 loop already in production.

## Candidate pool

| Product | Why it is plausible | Source | Disposition |
|---|---|---|---|
| Terra Nil | Entire product is built around a legible barren → thriving ecosystem transformation. | https://www.terranil.com/ | selected deep reference |
| The Gunk | Explicit corruption/regrowth loop; restoring nature transforms the traversed world. | https://www.xbox.com/en-US/games/store/the-gunk/9p008l2ls87f | selected deep reference |
| Flower | Movement itself causes landscapes to wake up, with very little explanatory UI. | https://store.playstation.com/fi-fi/product/EP9000-CUSA00077_00-FLOWERPS4000FULL | supporting candidate |
| Okami | Restoring nature is a strongly staged world-state payoff and is tied to existing player powers. | https://static.capcom.com/okami/manuals/PS2_Okami_Manual.pdf | supporting candidate |
| Alba: A Wildlife Adventure | Small environmental good deeds improve a local place; useful at BeBee's compact scale. | https://apps.apple.com/us/app/alba-a-wildlife-adventure/id1528014682 | anti-pattern / materially different interaction |

Candidate-pool exception: none. Five shipped references with relevant restoration/environment-repair behavior were available.

## Deep reference 1 — Terra Nil

**Direct observation from official product page:** Terra Nil describes transforming a barren, lifeless landscape into a thriving ecosystem by turning dead soil into grassland, cleaning pollution, planting forests and creating animal habitat. Its official screenshots and region descriptions present restoration as a material world-state change rather than a HUD-only completion flag.

**What transfers to BeBee:** the result must change several visual channels together. A first meadow that only changes a label or recolors completed flowers would under-deliver the restoration premise. For P4, ground saturation, vegetation/detail density and ambient life should all rise with restoration contribution.

**What does not transfer:** Terra Nil's terrain tools, ecological resource systems and large-scale planning are not evidence for adding new BeBee mechanics. BeBee already has its cause: movement-through pollination.

## Deep reference 2 — The Gunk

**Direct observation from Xbox's product description:** The Gunk explicitly frames its loop as "Corruption & Regrowth": remove the corruption, restore nature and transform the world around the player; revived plant life then changes how the environment reads and supports exploration.

**What transfers to BeBee:** restoration feedback should occupy the same world in which the action happened. It should not cut to a separate results screen. The before/after should remain readable while moving through the meadow.

**What does not transfer:** BeBee P4 does not need combat, resource extraction, a separate cleanse tool or restored traversal gates. Those would be new player problems, not solutions to P4's problem.

## Supporting candidate — Flower

The PlayStation Store description says the player carries flower petals through each landscape and sees those landscapes come alive. This is useful because the cause/effect is expressed through movement and world reaction with little mandatory explanatory UI.

Inference for BeBee: keep the P2 movement-through control intact and make the meadow respond to completion automatically. Do not add a "restore" confirmation button after pollination.

## Supporting candidate — Okami

Capcom's manual explicitly describes life withering from the land and nature being restored through the player's existing divine powers. It is a useful example of restoration as a staged payoff attached to established verbs rather than a separate meta screen.

Inference for BeBee: P4 should use already completed patch IDs as the restoration source of truth. The meadow does not need a second independently persisted "restoration task" state.

## Anti-pattern / materially different solution — Alba

A review surfaced on the App Store praises the environmental theme but specifically criticizes several repair tasks for collapsing into a single icon tap rather than letting the player perform the activity. That is anecdotal user evidence, not a universal finding, but it exposes a relevant risk for BeBee.

**Lesson:** do not put an extra hammer/restore/confirm icon on a completed patch. The player has already performed the meaningful action by flying through and pollinating. P4 should make the world transformation the consequence of that action, not require a second one-tap administrative action.

Source: https://apps.apple.com/us/app/alba-a-wildlife-adventure/id1528014682

## Official technical documentation

- Defold GUI API: https://defold.com/ref/stable/gui-lua/ — GUI scripts can create box/text nodes dynamically and update node color/position/size at runtime; appropriate for the current primitive production surface without introducing a parallel renderer.
- Defold GUI manual: https://defold.com/manuals/gui/ — GUI presentation remains separate from gameplay/domain state; restoration stage calculation therefore lives in a domain module rather than in presentation code.
- Defold `sys` API: https://defold.com/ref/stable/sys/ — persistence continues through the existing storage abstraction. P4 does not add direct `sys.save` calls or a new save schema.

## Alternatives

### A — Selected: derived four-stage world transformation

`campaign_completion` remains authoritative. Each completed authored patch contributes its existing `restoration_contribution`; a stable meadow model maps total contribution to `DORMANT → WAKING → GROWING → RESTORED`. Presentation increases ground saturation, vegetation/detail density and ambient life, then plays a bounded non-blocking final accent.

Why selected:

- uses the already validated P2 player verb;
- gives the strong multi-channel world change supported by Terra Nil/The Gunk observations;
- preserves D-008's sparse HUD and D-009's no-punishment/no-grind direction;
- avoids save-state duplication because stage is derivable from stable completion IDs;
- fits V-001's explicit dormant/restored palette and 1200–2000 ms major-reveal token.

### B — Rejected: completion banner / HUD meter only

Cheaper, but it fails P4's central acceptance criterion: before/after must be obvious with HUD hidden. It would report restoration instead of showing it.

### C — Rejected: separate restore interaction after pollination

Would add an action with no validated player problem and reproduce the one-tap administrative failure mode surfaced in Alba. It also weakens the causal connection between pollination and world recovery.

### D — Rejected: new restoration currency or seed gate in P4

Would overlap P5 and contradict the milestone boundary. P4 needs payoff from the current Honey/Flight/Buzz/pollination loop, not another economy.

## Selected P4 contract

1. First Patch has exactly four authored stages: Dormant, Waking, Growing, Restored.
2. Stage is derived from completed patch IDs and authored restoration contributions; no save-schema change.
3. Each stage materially changes the world through at least ground value/saturation and detail density; later stages add ambient life.
4. Final restoration adds a bounded 1.5 s accent inside V-001's 1.2–2.0 s band and never blocks movement.
5. Ordinary gameplay retains one objective plus Honey; no modal tutorial or second restoration control is added.
6. Exact-head browser evidence must capture HUD-hidden dormant/mid/restored states, desktop + small/mobile restored coverage, movement during the reveal and reload persistence.
7. P4 cannot close until the separate evidence-first evaluation returns PASS or PASS WITH DEVIATION.

## Implementation and evidence outcome

Accepted runtime head before closeout-only source-of-truth changes: `a45f9dac2f9d7136c3da51dc5b761eb0c05ce739`.

- Repository standards `33249086788` — PASS;
- Test/data `33249086793` — PASS;
- Pages preview `33249086822` — PASS;
- HTML5 CI `33249086913` — PASS;
- retained movement/P4 artifact `9713808008`, digest `sha256:7385f1161ad2c68a91027bbc5585b6246abb14fdc56c42929ade4f158d8369ec`;
- canonical fixtures independently produce `DORMANT/0`, `GROWING/2`, `RESTORED/3` from clean contexts;
- ground mix `0.00 → 0.68 → 1.00`;
- detail count `8 → 22 → 28` and full ladder `8 → 14 → 22 → 28`;
- ambient-life count `0 → 2 → 6` and full ladder `0 → 1 → 2 → 6`;
- HUD-hidden before/after remains readable at 1280×720 and 640×360;
- final 1.5 s accent permits `86.644` design units of movement during the reveal;
- midpoint reload returns `GROWING`, final reload returns `RESTORED`;
- final reload does not replay the one-shot celebration;
- desktop/mobile/canonical P4 browser errors are zero;
- P1 movement, P2 pollination, P3 progression and storage regressions remain green inside the same HTML5 run.

Two evidence/runtime defects were found and fixed before acceptance rather than normalized:

1. an already-restored save initially replayed the final celebration on reload;
2. canonical `meadow_*` QA state names initially could inherit storage state instead of guaranteeing a clean deterministic fixture.

The accepted implementation separates canonical clean fixtures from the real `p4_storage_lifecycle=reset/reload` path, so deterministic visual evidence cannot substitute for persistence evidence.

Independent evaluation: `evidence/P4-FIRST-MEADOW-RESTORATION/evaluation.md` — **PASS**, no open `ITERATE` finding. Evidence strength remains **MEDIUM** because P4 has autonomous rendered/runtime evidence but does not claim an external novice playtest or final production art/audio.

Complete machine-readable evidence: `evidence/P4-FIRST-MEADOW-RESTORATION/manifest.json`.
