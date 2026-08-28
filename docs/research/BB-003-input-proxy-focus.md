# BB-003 — Input and proxy-focus proof

Checked: 2026-08-28

## Scope

BB-003 is a technical runtime proof, not a player-facing control-layout decision. It establishes:

- device-independent semantic action IDs for movement and primary actions;
- keyboard aliases for the same movement semantics;
- a browser single-touch / mouse-primary abstraction through one semantic pointer action;
- explicit ownership of input focus by the game object containing a collection proxy;
- input delivery into the loaded proxy world;
- modal acquisition, consumption, release and restoration of input focus.

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

### Defold game object API

Source: https://defold.com/ref/stable/go-lua/

Verified constraint:

- `acquire_input_focus` adds the game object to the input stack;
- the most recently focused listener is processed first;
- `on_input()` may return `true` to consume an action and stop propagation to lower listeners;
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
- therefore BB-003 can test the actual HTML5 input path rather than invoking Lua callbacks directly.

## Alternatives

### A — native Defold input stack with explicit proxy owner focus — selected

The bootstrap proxy owner acquires focus in the main world. The loaded gameplay listener acquires focus in the proxy world. A modal listener joins the proxy-world stack only while open and consumes input by returning `true`.

Why selected:

- matches documented engine semantics;
- proves the exact risk called out by `T-011`;
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

1. wait until the main-world proxy owner and proxied gameplay listener have acquired input focus;
2. dispatch W and require both proxied gameplay and the main-world owner to observe `move_up`;
3. dispatch Esc and require the modal listener to acquire focus;
4. dispatch W and require the modal to observe/consume `move_up`, while forbidding the same action at proxied gameplay and the main-world owner;
5. dispatch Esc and require modal focus release;
6. dispatch W and require normal gameplay/owner delivery again;
7. dispatch a browser touch event and require it to arrive as `pointer_primary` through the same proxy path;
8. fail on browser runtime exceptions.

The retained `runtime-evidence/input-proxy-smoke.json` artifact records the exact assertions and observed console markers for the PR head.

## Decision impact

- `T-011` remains **LOCKED** and gains a runtime proof implementation.
- `T-010` remains **HYPOTHESIS**. BB-003 proves input ownership/propagation only; it does not yet validate memory cost or the complete lifecycle policy for using collection proxies as the major region/screen architecture.
- No player-facing control layout is promoted to VALIDATED by this ticket.
