# BB-003 — Input and proxy-focus proof

Checked: 2026-08-28

## Scope

BB-003 is a technical runtime proof, not a player-facing control-layout decision. It establishes:

- device-independent semantic action IDs for movement and primary actions;
- keyboard aliases for the same movement semantics;
- a browser single-touch / mouse-primary abstraction through one semantic pointer action;
- explicit ownership of input focus by the game object containing a collection proxy;
- input delivery into the loaded proxy world;
- modal acquisition, consumption, release and restoration of input focus;
- consumption inside the proxy world prevents delivery to gameplay and to listeners lower on the main-world stack.

It does **not** select the final touch joystick geometry, movement acceleration, camera feel, pollination timing, region lifecycle policy, or proxy memory budget. Those remain later gameplay/lifecycle decisions.

## Research gate

Comparable shipped-game research is intentionally not used for this ticket. The risk is an engine/runtime routing contract, not a player-facing design choice. Product comparisons cannot establish whether Defold propagates and consumes input across collection-proxy worlds.

The authoritative references are Defold's current technical documentation plus an exact-head runtime experiment.

## Official documentation checked

### Defold collection proxy manual

Source: https://defold.com/manuals/collection-proxy/

Verified constraint:

- a collection proxy loads a separate game world;
- if objects in the loaded collection require input, the game object containing the proxy must acquire input focus so input can propagate through the proxy.

### Defold input manual

Source: https://defold.com/manuals/input/

Verified constraint:

- `acquire_input_focus` adds input-capable components on a game object to its world's input stack;
- each proxy-loaded world has its own stack and the proxy component is the bridge from the main-world stack;
- listeners in a loaded world are handled before dispatch continues further down the main stack;
- `on_input()` returning `true` consumes an action across the nested stack traversal, preventing lower proxy-world and lower main-world listeners from receiving it;
- `release_input_focus` removes the listener from the stack.

### Defold mouse and touch input manual

Source: https://defold.com/manuals/input-mouse-and-touch/

Verified constraint:

- a single touch is mapped through the mouse-button-one input path;
- this permits HTML5 mouse and single-touch to share one semantic pointer action without choosing the final touch movement UI in P0.

### Chromium DevTools Protocol — Input domain

Source: https://chromedevtools.github.io/devtools-protocol/tot/Input/

Verified constraint:

- the browser can receive deterministic `dispatchKeyEvent` and `dispatchTouchEvent` calls in CI;
- keyboard/touch states must be held across browser animation frames so the Defold frame loop can sample their pressed/released edges reliably;
- therefore BB-003 can test the actual HTML5 input path rather than invoking Lua callbacks directly.

## Alternatives

### A — native Defold input stack with explicit proxy owner focus — selected

A lower main-world sentinel acquires focus first. The bootstrap game object containing the proxy then acquires focus above it. The loaded gameplay listener acquires focus in the proxy world. A modal listener joins the proxy-world stack only while open and consumes input by returning `true`.

This topology matters: the proxy owner's controller script intentionally has no `on_input()` callback. The sentinel below the proxy proves whether dispatch continues back into the main stack after the proxy world finishes handling an action.

Why selected:

- matches documented engine semantics;
- proves the exact risk called out by `T-011`;
- demonstrates both proxy propagation and cross-stack modal consumption;
- avoids a custom forwarding protocol;
- is observable end-to-end in HTML5 CI.

### B — custom input router forwards messages into proxy world — rejected

A main-world singleton could consume raw input and forward custom messages to loaded collections. This would duplicate Defold's native focus stack and could hide, rather than prove, proxy propagation behavior.

### C — avoid proxies until later — rejected for this proof

Avoiding collection proxies would remove the immediate failure mode but leave `T-010` untested. A small isolated proof is cheaper than discovering routing assumptions after regions/screens scale up.

## Semantic input contract

Production-facing gameplay code should consume semantic actions rather than raw device keys:

| Semantic action | Keyboard aliases | Pointer/touch path |
|---|---|---|
| `move_up` | W, Up | later touch movement adapter |
| `move_down` | S, Down | later touch movement adapter |
| `move_left` | A, Left | later touch movement adapter |
| `move_right` | D, Right | later touch movement adapter |
| `primary_action` | Space, Enter | later contextual mapping |
| `modal_toggle` | Esc | later UI mapping |
| `pointer_primary` | mouse button 1 | single touch via Defold's documented mapping |

This ticket intentionally does not equate `pointer_primary` with final movement. P1 may implement a floating joystick or another evidence-backed touch movement control while preserving the same semantic gameplay boundary.

## Exact-head runtime proof

`tools/defold/chromium_input_proxy_smoke.py` is activated by the runtime-evidence workflow when `app/input_probe.collectionproxy` exists.

The required sequence is:

1. establish a lower main-world sentinel, then the main-world proxy-owner focus, then the proxied gameplay focus;
2. dispatch W and require proxied gameplay plus the lower main-world sentinel to observe `move_up`, proving traversal into and back out of the proxy stack;
3. dispatch Esc and require the modal listener to acquire focus;
4. dispatch W and require the modal to observe/consume `move_up`, while forbidding delivery to proxied gameplay and the lower main-world sentinel;
5. dispatch Esc and require modal focus release;
6. dispatch W and require normal proxied gameplay plus lower-main-stack delivery again;
7. dispatch a browser touch event and require it to arrive as `pointer_primary` through the same proxy path and continue to the lower main stack;
8. fail on browser runtime exceptions.

Key and touch states are held across browser animation frames so `pressed`/`released` edges are sampled by Defold rather than relying on sub-frame CDP timing.

The retained `runtime-evidence/input-proxy-smoke.json` artifact records the exact assertions and observed console markers for the PR head.

## Decision impact

- `T-011` remains **LOCKED** and gains a runtime proof implementation.
- `T-010` remains **HYPOTHESIS**. BB-003 proves input ownership/propagation only; it does not yet validate memory cost or the complete lifecycle policy for using collection proxies as the major region/screen architecture.
- No player-facing control layout is promoted to VALIDATED by this ticket.
