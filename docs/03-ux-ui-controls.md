# 03 — UX, UI & Controls

## 1. Objective

BeBee should be understandable by watching the world for a few seconds. UI supports play; it must not become the game.

Primary rule:

> The world communicates the next useful action first; UI confirms it second.

Decision status lives in `DECISIONS.md`. Exact HUD positions, joystick style and pollination input remain hypotheses until research/visual validation.

## 2. Reference requirement

Before implementing a player-facing surface, inspect problem-specific shipped references. Cow Bay/7Spot games are useful but are not the only visual/UX authority.

Use different references when they solve a problem better, for example:

- movement/touch feel;
- cozy HUD hierarchy;
- garden customization;
- locked-node communication;
- restoration feedback;
- upgrade purchasing;
- map/progress presentation.

Record measurable observations in the feature research template and use `13-visual-qa-scorecard.md` after implementation.

## 3. Gameplay HUD — HYPOTHESIS

The current sparse concept remains:

- one primary objective/status surface;
- one persistent Honey display;
- contextual actions only when needed;
- no premium-currency/shop/event clutter.

The old fixed rule “objective top-left, Honey top-right” is a **starting layout**, not a locked decision. Final placement is chosen after desktop/mobile/portal reference comparison.

### Objective surface

Requirements:

- one primary objective at a time;
- minimal text;
- no scrolling quest log during normal play;
- can briefly indicate direction without stealing the camera;
- collapses/fades when the world already communicates the goal clearly.

### Honey

Requirements:

- always understandable when relevant;
- gain/spend visibly attributed;
- no constant attention pulse;
- readable across selected portal/device sizes.

## 4. Movement controls

Gameplay consumes semantic movement intent.

Desktop baseline:

- WASD/arrows are supported;
- no precision clicking required for ordinary flower interaction.

Touch:

- floating joystick remains a strong candidate;
- alternative touch movement is allowed if research/prototype evidence is better;
- movement surface must avoid collision with contextual UI/safe areas.

The touch scheme is validated with real-device/browser testing before lock.

## 5. Pollination input — follows P-1 decision

Do not hard-code UI around auto-pollination before `BB-P003` selects the core verb.

If the winner is:

- proximity: no permanent pollination button is needed;
- hold: use one clear semantic action with large touch affordance;
- sweep/movement-through: movement itself carries most interaction and UI should show coverage/progress rather than another button.

UX must follow the validated verb, not force the verb to fit an early HUD sketch.

## 6. World-space interaction

Prefer local world feedback for local states:

- active patch highlight/progress;
- locked requirement near the target;
- restoration/unlock change physically in the world.

Avoid permanent labels above every flower.

A locked state should communicate the missing requirement with icon + concise value rather than a paragraph.

## 7. Improvement/Hive surface

The Hive remains the leading progression-hub concept, but exact card count/layout follows the validated upgrade set.

Requirements:

- current level/effect;
- next effect;
- Honey cost;
- clear affordability;
- one intentional purchase action;
- no confirmation dialog for ordinary non-destructive improvement;
- gameplay movement cannot leak through an open modal/panel.

If Yield is removed, do not leave an empty third card or invent a filler stat.

## 8. Seed/flower choice UI

This UI follows the `BB-P004` seed/restoration flow.

Requirements regardless of flow:

- locked/unlocked/current state obvious;
- player can preview/understand the flower choice;
- planting is one clear action after selection;
- current planted species is visible;
- replant/undo rules are clear;
- campaign progress cannot be accidentally reset through this surface.

Mobile bottom-sheet and desktop anchored-panel patterns are candidates, not fixed law. Compare alternatives against playfield obstruction and action count.

## 9. Region / planet progress

The map/progress surface should answer:

- where am I;
- what has been restored;
- what is next;
- how much of the planet is alive;
- which flower identities have been discovered/unlocked if useful.

Do not turn it into a strategy dashboard.

Fast travel is optional later; first-session map behavior is chosen after the selected portal/onboarding flow is known.

## 10. Entry/title flow — corrected

The old fixed sequence `Title -> Play -> Tutorial` is no longer a universal requirement.

The primary distribution target is selected in P-1. Current portal guidance may favor landing directly in gameplay or allowing at most one click.

Architecture/UI must support:

- direct-to-gameplay onboarding;
- one-click entry when appropriate;
- standalone title/continue for direct hosting if useful.

Do not build mandatory splash/menu friction that must later be bypassed for a portal.

## 11. Pause/settings

Keep one shallow panel:

- resume;
- music/SFX;
- reduced motion;
- haptics where supported;
- text/accessibility controls when validated;
- controls help;
- return/exit appropriate to platform.

Avoid custom fullscreen controls when a selected portal forbids/owns fullscreen behavior.

## 12. Onboarding

Teach inside gameplay.

Rules:

- use visuals/motion before text;
- one short contextual instruction at a time;
- remove it as soon as behavior is demonstrated;
- no lore/tutorial page stack before first interaction;
- player reaches the core verb quickly.

## 13. Direction guidance

Use subtle world markers/edge guidance.

Routine objective guidance must not yank the camera away from the bee.

Short authored reveals are allowed only when they preserve orientation and reduced-motion behavior.

## 14. Input focus and modal behavior

UI and gameplay use Defold input focus intentionally.

When a modal/task-specific panel is active:

- it consumes the relevant input;
- bee movement/pollination does not continue behind it;
- closing returns focus predictably.

If gameplay is loaded through a collection proxy, the proxy owner's input routing is part of the test plan.

## 15. Responsive targets

Development default captures:

- desktop `1440x900`;
- mobile portrait `390x844`.

After P-1 selects the primary portal, add its actual required/representative sizes. Do not treat development defaults as portal certification.

Critical UI must survive:

- desktop landscape;
- narrow/wide browser windows allowed by target;
- relevant mobile/tablet orientation(s);
- safe areas/browser UI changes.

## 16. Touch target/readability baseline

- minimum interactive touch target: 44 logical px baseline unless target-platform research specifies stricter needs;
- state cannot rely on color alone;
- text requires background/outline/shadow treatment sufficient for world contrast;
- interactive flowers must look different from decoration at gameplay zoom.

## 17. Motion/feedback

UI/world motion should reinforce cause and effect:

- pollination begins -> immediate local response;
- completion -> flower/world response;
- Honey -> source-to-counter attribution;
- improvement -> effect/level change;
- planting -> visible world change;
- restoration -> strong environment transition.

Avoid perpetual badges/bounces competing for attention.

Reduced-motion mode preserves state clarity while reducing nonessential camera/UI motion.

## 18. UX acceptance questions

A new player should be able to answer without external explanation:

- what character do I control;
- what do I do with flowers;
- what do I earn;
- what changed when I improved the bee;
- why is this harder flower unavailable/slow;
- how can I influence which flowers grow;
- what is the long-term goal.

If answers are unclear, improve the interaction/world/UI rather than adding a help encyclopedia.

## 19. Evidence requirement

Every significant UX PR includes:

- researched references;
- official Defold/platform docs where relevant;
- actual BeBee captures/video;
- action/timing/readability scorecard;
- mobile evidence where affected;
- `PASS`, `PASS WITH DEVIATION`, or `ITERATE` conclusion.
