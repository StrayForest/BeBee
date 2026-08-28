# BB-006 — Visual QA harness foundation

Checked: 2026-08-29

## Scope

BB-006 implements the previously validated BB-P008 deterministic visual-QA contract far enough to prove one real exact-build HTML5 capture path before player-facing systems scale.

The completed foundation provides:

- a development/CI-only Defold QA router and `window.__bebeeQA` readiness bridge;
- exact source-commit binding injected by the pinned Bob build command;
- one infrastructure-only `foundation_probe` fixture in addition to the fifteen canonical future gameplay/UI states;
- a canonical local HTML5 HTTP server with explicit WebAssembly MIME handling;
- pinned Playwright-for-Python capture tooling using isolated Chromium BrowserContexts;
- desktop-reference and mobile-landscape capture with exact repeated-capture stability checks;
- release-bundle proof that rejects any exposed QA bridge or probe;
- deterministic tests for state/seed request handling;
- exact-source HTML5 CI execution and a retained `visual-qa-<sha>` artifact.

`foundation_probe` deliberately does not pretend that `movement_empty`, HUD, pollination, hive, seed or restoration gameplay already exists. Those canonical states retain their original semantic assertions and become implementable only when their owning systems exist.

The runtime/tooling implementation was merged separately from workflow wiring so high-risk candidate Lua did not share a PR with governance-sensitive Actions changes.

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

- matches the already validated repository contract rather than creating a second capture architecture;
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

Development HTML5 exposes `window.__bebeeQA` only when the QA runtime flag is enabled. A requested supported fixture becomes capture-ready only after the bootstrap proxy has loaded. Unknown states fail closed with `error=unknown_state` and never become capture-ready.

Release builds do not execute QA initialization because `bebee.qa_enabled=false`; the capture runner verifies that `window.__bebeeQA` and the probe DOM node are absent even when QA query parameters are supplied.

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

The CI command uses `python3 -m playwright install --with-deps chromium` so the hosted runner also receives required Linux browser dependencies.

The server explicitly serves `.wasm` as `application/wasm` and answers only Chromium's implicit root `/favicon.ico` request with 204 so browser chrome noise does not masquerade as a game-resource error.

## Exact runtime proof

The first complete BB-006 CI proof is GitHub Actions run `33214438370` on candidate head `56fa405c48d7c193c5e9888b825c48a0779c93a2`.

Observed capture report:

- browser: Playwright Chromium `151.0.7922.34`;
- Defold: `1.13.1`;
- QA seed: `88008`;
- reported build SHA exactly matched the candidate head;
- development bundle SHA-256: `fd0f30b989f1d65dc493a7128897a9d671b8b665303236ec944fd8c2e4c0cdf0`;
- desktop 1280×720: both isolated repeats SHA-256 `9efcf3f167dad760168b6d3fe14dc3b5126115960bda827260ac4687a8cc1f11`;
- mobile-landscape 844×390: both isolated repeats SHA-256 `046b359c483baeb1cae2240dd0c8a01000dab6509047b41e99197e746de2c471`;
- `console_error_count=0` and `page_error_count=0` for both captures;
- release proof: `bridge_present=false`, `probe_present=false`.

Retained artifacts from that run:

- `visual-qa-56fa405c48d7c193c5e9888b825c48a0779c93a2` — artifact `9702826036`, Actions digest `sha256:cabb48fd669f9f55e1482a55413538da6d33fbfb2c8fdeb9dfb22301d997593d`;
- `html5-playable-56fa405c48d7c193c5e9888b825c48a0779c93a2` — artifact `9702825800`, digest `sha256:18acb76a3040cc348216bcbd020f50c6fd7d6e9b9a9aaeefe3d2ea62583741f9`;
- `html5-ci-evidence-56fa405c48d7c193c5e9888b825c48a0779c93a2` — artifact `9702826312`, digest `sha256:f3aea48e7519f221f0c98f8d35f50fd832add15cb737fea70d985ec87e3fc503`.

The downloaded visual artifact was also inspected directly: both images show only the intended centered infrastructure probe on the real development HTML5 surface. The report/log contains warning-level Chromium WebGL `ReadPixels` performance diagnostics during screenshot capture, but no error/assert/page exception, and the exact repeated image hashes remain identical.

The same candidate head also passed `Repository standards` run `33214438383`, `Test and data` run `33214438431` and trusted `validate-pr-evidence` check `98994811068`.

## Decision impact

No `DECISIONS.md` status changes. `T-002`, `T-012`, `R-001`, `R-014` and the validated BB-P008 contract are implemented rather than reopened.

Provenance: `TECH_CONSTRAINT`.
Evidence strength: `HIGH` for the harness architecture, exact-build binding, release isolation and observed repeatability of the foundation fixture.

## Closeout boundary

BB-006 proves the P0 visual-QA infrastructure contract and one deterministic still fixture; it does **not** claim that the future player-facing state registry is implemented. Player-facing states and required motion evidence are added by the milestones that own those systems.

BB-007 remains responsible for the storage abstraction, corrupt-load recovery and browser save/reload persistence proof.
