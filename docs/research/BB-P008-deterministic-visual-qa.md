# BB-P008 — Deterministic visual QA design research

Research snapshot: **2026-08-28**.

## Problem

Rendered evidence must represent a known state from the exact code being evaluated. A screenshot taken after an arbitrary delay is insufficient because build identity, browser storage, async loading and simulation timing may differ between runs.

## Technical alternatives

### A — Manual screenshots only

Useful for exploratory review, but weak for autonomous merge gates. It does not enforce exact-head provenance, repeatable state setup or required state coverage.

### B — Browser navigation + fixed sleep

Easy to automate, but a timeout such as “wait 2 seconds then capture” does not prove engine readiness. CI machine load or resource timing can move the frame being captured.

### C — Explicit engine/browser readiness bridge + exact-head artifact binding

Selected.

The HTML5 build exposes a development-only QA router and JavaScript bridge. A requested state is captured only after the engine reports that the fixture has been applied and a deterministic capture frame/checkpoint is ready. The browser runner asserts state ID, fixed seed and build commit SHA before capture.

## Official documentation observations

### Defold automated testing

Source: https://defold.com/manuals/automated-testing/

Checked 2026-08-28.

Current Defold guidance separates build/bundle evidence from runtime evidence. For HTML5 browser tests it explicitly describes external browser automation for viewport/input/console/screenshot checks and recommends an explicit JavaScript testing bridge for reliable browser-side automation.

Consequence: BB-P008 does not treat `bob bundle` success as rendered QA and does not use a fixed sleep as the primary readiness contract.

### Defold Bob

Source: https://defold.com/manuals/bob/

Checked 2026-08-28.

Bob is Defold's command-line project builder/bundler and supports `wasm-web`, making it the correct future P0 CI build boundary.

Consequence: each visual-QA package is produced from one exact PR-head HTML5 bundle rather than editor-local output of unknown provenance.

### Defold HTML5

Source: https://defold.com/manuals/html5/

Checked 2026-08-28.

HTML5 content must be tested through an HTTP server rather than opening `index.html` with `file://`; `.wasm` needs the correct MIME handling.

Consequence: the capture runner has an explicit serve phase and rejects `file://`.

### Playwright isolation

Source: https://playwright.dev/docs/browser-contexts

Checked 2026-08-28.

BrowserContexts provide isolated clean-slate sessions, including separate cookies and browser storage.

Consequence: independent QA states use fresh contexts so capture order does not silently modify later state through cookies/local storage/session storage.

## State design

The initial registry comes from already-defined BeBee quality questions rather than arbitrary screen enumeration:

- movement readability/camera;
- pollination idle/active/complete;
- soft/hard flower gating;
- sparse HUD scaling;
- affordable/unaffordable Hive state;
- seed locked/unlocked ownership state;
- dormant/mid/restored meadow transformation.

This gives 15 canonical initial states. Runtime implementation can add states as production systems become real, but IDs are repository-authored fixtures rather than ephemeral test code.

## Viewport design

BB-P008 imports V-001 dimensions from `config/visual-style.json`:

- 1280×720 canonical landscape;
- Poki scale examples 640×360, 836×470 and 1031×580;
- representative mobile landscape 844×390.

The static validator rejects drift between the visual style and visual QA contracts.

## Readiness design

The development-only `window.__bebeeQA` bridge reports:

- state ID;
- seed;
- engine readiness;
- capture readiness;
- deterministic simulation frame;
- build commit SHA.

The capture runner waits for `captureReady`, then checks state/seed/SHA before retaining evidence.

This is intentionally fail-closed. An unknown state, timeout or identity mismatch is an invalid capture, not a request to fall back to a default scene.

## Provenance design

Every report includes exact head SHA, bundle hash, Defold version, browser version, fixture ID/seed/viewport, simulation frame, capture hash and browser error counts.

Later evidence-policy enforcement can therefore verify that a player-facing manifest points to artifacts from the exact evaluated build rather than an older visually similar run.

## Pixel-regression decision

No universal image-diff threshold is selected in P-1.

Reason: renderer/browser/assets and real deterministic states do not exist yet. Choosing a percentage now would create fake objectivity. P0 must first demonstrate repeated stable captures. Thresholded golden-image checks can then be introduced selectively for stable surfaces while art/world changes remain semantic evaluation tasks.

## Result

Selected technical pattern: **exact-head bridge-driven deterministic capture**.

BB-P008 is complete when the contract is internally consistent and implementation-ready. It does **not** assert that runtime capture already works; the actual Defold bridge, Playwright runner and retained HTML5 artifact belong to P0/BB-006.
