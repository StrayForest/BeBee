# 03 — UX, UI & Controls

## 1. UX objective

BeBee should be understandable by watching the screen for a few seconds. The interface supports play; it must not dominate it.

Primary UX principle:

> The world tells the player what to do first; UI confirms it second.

---

## 2. Reference pattern synthesis

The useful pattern shared by Cow Bay, Cow Castle, Olly the Paw, My Little Universe and Dreamdale is not a specific pixel layout. It is a low-friction hierarchy:

1. character and nearby resource are visually dominant;
2. one obvious current objective is visible;
3. currency is always readable;
4. unlock/upgrade affordances appear when relevant;
5. most progression happens directly in the world;
6. menus are shallow and task-specific.

BeBee follows that hierarchy while using original visual design.

---

## 3. Gameplay HUD

### Top-left: objective

Compact objective card:

```text
🌼 Restore Sunny Meadow
4 / 6 patches
```

Rules:

- maximum two lines;
- no scrolling quest log during normal play;
- collapses further after several seconds if the player is actively progressing;
- tapping/clicking it can briefly highlight the target direction.

### Top-right: honey

Single persistent currency display:

```text
🍯 185
```

Rules:

- number animates on gain/spend;
- no separate premium icon in MVP;
- briefly show `+24` beside it after reward;
- affordability pulse occurs once, not continuously.

### Bottom-left: movement

Mobile only: floating joystick.

- joystick origin appears where thumb first presses inside a safe zone;
- deadzone prevents micro-jitter;
- joystick fades when inactive;
- do not place permanent decoration underneath it.

Desktop has no movement HUD after onboarding.

### Bottom-right

Normally empty during active play.

Contextual action can appear for:

- Hive interaction;
- seed customization;
- map/portal interaction;
- accessibility fallback interact button.

Automatic pollination does not need an action button.

### Bottom-center

Reserved for short contextual messages/toasts only:

- `Buzz 3 required`
- `Lavender seeds unlocked`
- `Sunny Meadow restored`

Do not stack more than two.

---

## 4. World-space interaction UI

World-space UI is preferred for local actions.

### Flower patch

When relevant:

- thin circular/organic progress ring near patch center;
- small flower-tier icon if gated;
- no permanent labels above every patch.

### Locked patch

Show the reason directly:

```text
Buzz 3
```

with one icon and number. Avoid sentences like “Your pollination level is insufficient to interact with this resource.”

### World unlock gate

Display one concise requirement near the blocked route:

```text
Restore 4 meadows
```

or

```text
🍯 120
```

---

## 5. Hive screen

The Hive is the main progression hub.

### Layout

Header:

```text
Improve your bee          🍯 185
```

Main body: three vertically stacked or responsive cards.

Card example:

```text
[wing icon] Flight       Lv. 2
Fly 10% faster
Next: 1.20x speed

            🍯 56  [Upgrade]
```

Equivalent cards for Buzz and Yield.

### Behavior

- affordable cards have a clear primary button;
- unaffordable cards show cost, not a disabled mystery state;
- if a Buzz purchase unlocks a flower family, show the unlock in the same confirmation moment;
- one tap/click buys; do not add an “Are you sure?” dialog for normal upgrades;
- close/back returns directly to gameplay.

---

## 6. Seed selector

Opened only from a restored customizable patch.

### Mobile

Bottom sheet occupying roughly lower 35–45% of screen.

### Desktop

Small anchored panel near the patch or centered lower panel.

Each seed card shows:

- flower illustration;
- name;
- locked/unlocked state;
- unlock honey cost if locked;
- current selection mark.

Actions:

- locked seed: `Unlock`;
- unlocked seed: `Plant`;
- current seed: `Planted`.

Replanting an unlocked seed is free in the vertical slice.

---

## 7. Region / planet map

The map is a progress overview, not a strategy game screen.

Shows:

- stylized planet or region ribbon;
- current region highlighted;
- completed regions in color;
- future regions muted;
- large `Planet in bloom: XX%`;
- discovered flower count.

Region card:

```text
Sunny Meadows
5 / 6 restored
Native flowers: Daisy · Clover · Lavender · Lily
```

Selecting a previously unlocked region may fast-travel later; during the first vertical slice, map navigation can be limited to the current region.

---

## 8. Main menu

Keep it minimal.

### New player

- `Play`
- `Settings`
- small version/build identifier

### Returning player

- `Continue`
- `New Game` in secondary/options location to prevent accidental reset
- `Settings`

No carousel of shops, events, inbox, quests, passes and offers on launch.

---

## 9. Pause / settings

One simple panel:

- Resume
- Music volume
- SFX volume
- Haptics on/off (mobile)
- Reduced motion on/off
- Text scale: normal/large
- Controls help
- Return to title

Optional later:

- language selector;
- color accessibility presets if flower-state readability needs them.

---

## 10. Onboarding UI

Tutorial instructions are contextual and disposable.

Allowed examples:

```text
Fly to the flowers
```

```text
Stay close to pollinate
```

```text
Spend honey at the hive
```

Each instruction disappears as soon as the behavior is demonstrated.

Do not darken the entire screen and force the player to tap through tutorial pages.

---

## 11. Direction guidance

When the objective is off-screen:

- show a subtle edge arrow/petal marker;
- fade it when close;
- never yank the camera away from the bee.

This explicitly avoids a common frustration in comparable games where objective guidance can interrupt spatial orientation.

---

## 12. Input abstraction

Gameplay code consumes semantic actions:

- `move_x`
- `move_y`
- `interact`
- `pause`
- `ui_accept`
- `ui_back`

Do not spread raw key/touch checks across gameplay scripts.

Touch and keyboard produce the same normalized movement vector.

---

## 13. Responsive layout targets

Support at minimum:

- 16:9 desktop;
- wide desktop/browser window;
- portrait phone;
- landscape phone/tablet.

Gameplay camera can show more/less world, but critical UI remains in safe zones.

No gameplay requirement may depend on a flower being visible at a fixed absolute screen coordinate.

---

## 14. Tap/click target rules

- minimum touch target: 44 logical px;
- primary buttons should generally be 48–56 px high on mobile layouts;
- avoid placing two destructive/important controls directly adjacent;
- seed cards and upgrade cards can be tapped anywhere on the card where unambiguous;
- close/back must be reachable with one obvious action.

---

## 15. Color and readability

Gameplay state cannot be color-only.

Examples:

- locked flower = closed silhouette + lock/Buzz icon, not merely gray;
- completed patch = open bloom + particles/ground change, not merely greener;
- selected seed = check mark + border/state, not merely hue.

Text should maintain readable contrast over world scenes via panels/shadows, not hard-coded white text over every background.

---

## 16. Animation rules

UI motion should reinforce cause and effect:

- honey flies from source to counter;
- upgrade card expands/pops once;
- unlock gate physically opens;
- seed choice transforms the patch;
- objective completion ticks and transitions to next objective.

Avoid perpetual bouncing badges and competing attention animations.

Reduced-motion mode should shorten or remove nonessential camera/UI motion while preserving state feedback.

---

## 17. Audio UX

Distinct short sounds for:

- pollination progress ticks/flower openings;
- patch completion;
- honey gain;
- upgrade purchase;
- seed planting;
- meadow restoration;
- failed affordability/locked requirement.

Do not reuse one “coin” sound for every event.

---

## 18. First-session screen flow

```text
Title
 -> Play
 -> Tutorial Meadow
 -> first honey
 -> Hive upgrade
 -> first gated flower becomes available
 -> meadow restoration
 -> first seed choice
 -> planet reveal
 -> continue into region
```

The first session should contain no account creation, newsletter prompt, rating prompt or monetization interruption.

---

## 19. UX acceptance tests

A new playtester should answer these without explanation:

- What character are you controlling?
- What are you supposed to do to the flowers?
- What do you earn?
- Where do you improve the bee?
- Why can't you efficiently pollinate the Lily yet?
- How do you change flowers in a restored meadow?
- What is the long-term goal?

If two or more answers are unclear, revise the game/UI rather than adding a help page.
