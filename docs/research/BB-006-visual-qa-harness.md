# BB-006 — Visual QA harness foundation

Checked: 2026-08-29

## Scope

BB-006 implements the previously validated BB-P008 deterministic visual-QA contract far enough to prove one real exact-build HTML5 capture path before player-facing systems scale.

This harness PR adds:

- a development/CI-only Defold QA router and `window.__bebeeQA` readiness bridge;
- exact source-commit binding injected by the pinned Bob build command;
- one infrastructure-only `foundation_probe` fixture in addition to the fifteen canonical future gameplay/UI states;
- a canonical local HTML5 HTTP server with explicit WebAssembly MIME handling;
- pinned Playwright-for-Python capture tooling using isolated Chromium BrowserContexts;
- desktop-reference and mobile-landscape capture definitions with exact repeated-capture stability checks;
- release-bundle proof logic that rejects any exposed QA bridge or probe;
- deterministic tests for state/seed request handling.

`foundation_probe` deliberately does not pretend that `movement_empty`, HUD, pollination, hive, seed or restoration gameplay already exists. Those canonical states retain their original semantic assertions and become implementable only when their owning systems exist.

CI wiring and retained visual artifacts are a separate BB-006 process PR so this high-risk runtime change does not mix candidate Lua with governance/workflow authority changes.

## Official documentation checked

### Defold automated testing

Source: https://defold.com/manuals/automated-testing/

Verified:

- HTML5 browser automation may wait for application readiness, resize viewports, collect console/JavaScript errors and capture screenshots;
- an explicit JavaScript testing bridge is the reliable browser-test boundary;
- Defold HTML5 Lua can communicate with that bridge through `html5.run()`.

### Defold HTML5 API

Source: https://defold.com/ref/stable/html5-lua/

Verified:

- `html5.run(code)` executes browser JavaScript synchronously and returns its result;
- the HTML5 namespace is platform-specific, so production code guards access and the dedicated headless test bootstrap does not depend on it.

### Defold project settings

Source: https://defold.com/manuals/project-settings/?lang=en

Verified:

- project-local custom settings are declared through root `game.properties`;
- runtime code can read them through `sys.get_config_*`;
- Bob accepts multiple `--settings` files applied left-to-right, allowing the build tool to inject exact provenance separately from committed mode settings.

### Playwright isolation and browser install

Sources:

- https://playwright.dev/python/docs/browser-contexts
- https://playwright.dev/python/docs/library
- https://playwright.dev/python/docs/browsers

Verified:

- BrowserContexts are isolated clean-slate sessions;
- Python Playwright installs its managed browser binaries separately;
- Chromium can be installed alone and the exact browser version can be recorded from the running browser.

Playwright Python is pinned to `1.62.0`, published 2026-07-31, and is licensed Apache-2.0. It is test tooling only and is not included in BeBee release bundles.

## Alternatives

### A — Playwright + explicit engine bridge — selected

Use the BB-P008 contract directly: engine-owned readiness/state provenance, Playwright isolated contexts, exact viewport screenshots, machine-readable report and release-negative proof.

Why selected:

- follows the already validated repository contract rather than creating a second capture architecture;
- separates state readiness from arbitrary browser sleeps;
- provides browser/version/context semantics needed for later player-facing evidence;
- allows repeated captures to establish actual stability before any golden threshold is invented.

### B — extend the dependency-free CDP smoke into the visual harness — rejected

The BB-003/BB-005 CDP scripts remain appropriate narrow runtime smokes, but using them as the visual-QA framework would contradict the validated BB-P008 Playwright BrowserContext contract and would require rebuilding isolation/screenshot ergonomics already provided by Playwright.

### C — screenshot after a fixed delay — rejected

A fixed sleep cannot prove that a requested fixture has been applied, transient setup has ended or the captured build/state matches the request. The engine bridge therefore owns `captureReady`.

## Runtime contract

Root `game.properties` defines:

- `bebee.qa_enabled` — false by default, explicitly true in development settings and false in release settings;
- `bebee.build_commit_sha` — exact source provenance injected by `tools/defold/bundle_html5.py` through a second temporary Bob settings file.

Development HTML5 always exposes `window.__bebeeQA`; a requested supported fixture becomes capture-ready only after the bootstrap proxy has loaded. Unknown states fail closed with `error=unknown_state` and never become capture-ready.

Release builds do not execute QA initialization because `bebee.qa_enabled=false`; the capture runner explicitly verifies that `window.__bebeeQA` and the probe DOM node are absent even when QA query parameters are supplied.

## Foundation fixture

`foundation_probe` is an infrastructure fixture, not a game-design state. It overlays a fixed diagnostic marker on the actual development HTML5 page after the engine starts and binds readiness to the real Defold bootstrap/proxy lifecycle.

Its default viewports are:

- `desktop_reference` — 1280×720;
- `mobile_landscape` — 844×390.

The capture runner opens a fresh BrowserContext for every capture, captures each configured viewport at least twice and requires identical PNG SHA-256 values for this unchanged fixture. This is intentionally narrower than a universal image-regression threshold.

## Local commands

After building development and release bundles:

```text
python3 scripts/serve_html5.py --root build/html5 --port 8000
python3 -m pip install -r tools/visual_qa/requirements.txt
python3 -m playwright install chromium
python3 tools/visual_qa/capture_visual_qa.py --head-sha <FULL_SHA>
```

The server explicitly serves `.wasm` as `application/wasm` and answers only Chromium's implicit root `/favicon.ico` request with 204 so browser chrome noise does not masquerade as a game-resource error.

## Decision impact

No `DECISIONS.md` status changes. `T-002`, `T-012`, `R-001`, `R-014` and the validated BB-P008 contract are implemented rather than reopened.

Provenance: `TECH_CONSTRAINT`.
Evidence strength: `HIGH` for the harness architecture and release isolation; actual repeatability/retained-artifact proof is completed by the separate BB-006 CI process PR.

## Follow-up boundary

The process PR must install the pinned Playwright package/Chromium, use the canonical server, run exact-head desktop/mobile captures, retain `artifacts/visual-qa/<sha>/`, verify repeated stability and release QA absence, then update README/roadmap to BB-006 COMPLETE. BB-007 remains responsible for browser storage persistence/reload.
