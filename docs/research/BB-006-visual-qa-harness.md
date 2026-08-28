# BB-006 — Visual QA harness foundation

Checked: 2026-08-29

## Scope

BB-006 implements the already-validated BB-P008 runtime evidence contract far
enough to prove one deterministic Defold HTML5 QA state on canonical desktop and
mobile-landscape viewports.

Delivered scope:

- a development-only `?qa=<state>&qa_seed=<integer>` runtime router;
- `window.__bebeeQA` readiness/provenance bridge with fail-closed unknown-state
  behavior;
- exact source SHA embedded into Defold configuration at bundle time;
- a local HTML5 serve command with explicit WebAssembly MIME registration;
- pinned Playwright Python + Chromium capture tooling;
- isolated browser contexts for every independent capture;
- repeated capture of `movement_empty` at `desktop_reference` and
  `mobile_landscape`, with byte-hash equality required for determinism;
- machine-readable report, console/page/network evidence and capture SHA-256;
- release guard proving that QA parameters do not expose the bridge or alter the
  captured release output;
- retained exact-head CI artifact under the canonical visual-QA artifact root.

BB-006 does **not** claim that `movement_empty` already satisfies its eventual P1
player-facing assertion such as "bee visible". At P0 it is an infrastructure
fixture bound to the minimal bootstrap. P1 owns the real movement scene/content and
must upgrade the fixture before using it as movement-quality evidence.

## Canonical contract consumed

The authoritative pre-existing design is `config/visual-qa.json` from BB-P008 and
`docs/18-deterministic-visual-qa.md`.

BB-006 deliberately implements that contract instead of inventing a second QA
schema. In particular it preserves:

- development/CI-only QA state injection;
- release bridge/injection prohibition;
- default seed `88008`;
- bridge fields `schemaVersion`, `stateId`, `seed`, `engineReady`,
  `captureReady`, `simulationFrame`, `buildCommitSha`;
- fresh browser state per independent capture;
- canonical desktop `1280×720` and mobile-landscape `844×390` viewports;
- exact-head/capture hash provenance;
- no universal pixel-diff tolerance at this stage.

## Official documentation checked

### Defold automated testing

Source: https://defold.com/manuals/automated-testing/

Verified constraints/patterns:

- HTML5 browser automation is an appropriate runtime-test path;
- browser automation can inspect JavaScript/console errors and take runtime
  screenshots;
- a JavaScript testing bridge is the reliable boundary for browser-to-game
  synchronization rather than arbitrary fixed sleeps.

### Defold HTML5 extension API

Source: https://defold.com/ref/stable/html5-lua/

Verified constraint:

- `html5.run()` can execute browser JavaScript from the HTML5 runtime, so the
  development-only Defold router can publish an explicit readiness object without
  adding a production portal dependency.

### Defold project settings / Bob

Sources:

- https://defold.com/manuals/project-settings/
- https://defold.com/manuals/bob/

Verified constraints:

- custom project properties may be defined in `game.properties` and read through
  `sys.get_config_*` at runtime;
- Bob supports multiple `--settings` files and applies them from left to right;
- BB-006 can therefore keep authored development/release settings immutable while
  applying an ephemeral exact-commit provenance override as the final settings
  file.

### Playwright isolation / browser contexts

Source: https://playwright.dev/docs/browser-contexts

Verified constraint:

- BrowserContext provides isolated clean-slate browser state appropriate for
  order-independent deterministic captures.

### Playwright Python package and license

Sources:

- https://pypi.org/project/playwright/1.62.0/
- https://github.com/microsoft/playwright-python

Verified constraints:

- Playwright Python `1.62.0` is pinned for this implementation;
- the official package/repository declares Apache-2.0;
- Playwright is a development/CI QA dependency only and is not included in the
  produced game bundle.

## Alternatives

### A — Playwright implementation of the validated BB-P008 contract — selected

Why:

- BB-P008 already selected Playwright BrowserContext as the intended clean-state
  capture boundary;
- it gives viewport, console/page-error, screenshot and isolated-context behavior
  through one maintained API;
- it avoids extending the small BB-005 raw-CDP smoke helper into a second bespoke
  browser-testing framework.

### B — extend the dependency-free raw Chromium CDP client — rejected for visual QA

The BB-005 CDP helper remains valuable for a small startup/input smoke with no
third-party Python dependency. Reusing it for full deterministic capture would
require BeBee to maintain context isolation, browser lifecycle, screenshot and page
error plumbing that Playwright already provides and BB-P008 already validated.

### C — screenshot after a fixed sleep — rejected

A sleep can hide resource/state timing races and does not prove which game state was
captured. `captureReady` is authoritative and reports exact state, seed, simulation
frame and build SHA.

### D — expose QA router in release and merely hide UI affordances — rejected

This conflicts with the validated release contract and creates an unnecessary
production debug surface. Release explicitly sets `bebee.qa_enabled=0`; the capture
runner proves both bridge absence and no rendered response to QA query parameters.

## Runtime router

`game.properties` defines custom BeBee build settings:

- `bebee.qa_enabled` — default false;
- `bebee.build_commit_sha` — default `unknown`.

Development settings enable the QA router. Release settings disable it.

`tools/defold/bundle_html5.py` accepts `--build-commit-sha`. It validates a full
40-character hexadecimal Git SHA and writes a temporary final Bob settings override
containing that SHA. Runtime code reads it through `sys.get_config_string`, binding
browser evidence to the exact source candidate without editing tracked source files.

`app/qa_router.lua` currently implements the minimum P0 fixture
`movement_empty`. Unknown/unimplemented IDs publish an error bridge and never set
`captureReady=true`. The known fixture sets `captureReady=true` only at its declared
stable simulation frame.

## Capture runner

`tools/visual_qa/capture.py`:

1. loads the canonical state/viewport registry;
2. validates an exact 40-character head SHA;
3. hashes the complete development and release bundle trees;
4. launches pinned Playwright Chromium;
5. creates a fresh BrowserContext for each capture;
6. navigates to the exact QA state/seed;
7. waits for a non-zero canvas and the engine bridge;
8. asserts state, seed and embedded build SHA;
9. captures the full viewport and verifies PNG dimensions;
10. rejects actionable HTTP, request, console and page errors;
11. repeats each required capture in a new BrowserContext and requires identical
    PNG SHA-256 plus identical simulation frame;
12. probes the release build with and without QA query parameters and requires no
    bridge plus identical release capture hashes;
13. writes `capture-report.json` and `console.log` under the exact-head artifact
    root.

As in BB-005, Chromium's automatic `/favicon.ico` 404 is ignored only when
structured browser evidence identifies that exact browser-generated request. Other
HTTP 4xx/5xx remain fatal.

## Local usage

Build with the exact source provenance when available:

```text
python3 tools/defold/bundle_html5.py --mode development --build-commit-sha <40-char-sha>
python3 tools/defold/bundle_html5.py --mode release --build-commit-sha <40-char-sha>
```

Install the pinned QA tool/browser:

```text
python3 -m venv .tmp/visual-qa-venv
.tmp/visual-qa-venv/bin/python -m pip install -r tools/visual_qa/requirements.txt
.tmp/visual-qa-venv/bin/python -m playwright install chromium
```

Serve the bundles:

```text
.tmp/visual-qa-venv/bin/python tools/visual_qa/serve.py --directory build/html5
```

Then capture in another shell:

```text
.tmp/visual-qa-venv/bin/python tools/visual_qa/capture.py \
  --development-bundle build/html5/development/BeBee \
  --release-bundle build/html5/release/BeBee \
  --head-sha <40-char-sha> \
  --state movement_empty \
  --viewports desktop_reference,mobile_landscape \
  --output-root artifacts/visual-qa/<40-char-sha>
```

## CI / trust boundary

BB-006 extends the existing unprivileged exact-source `HTML5 CI` workflow. Candidate
runtime/build code executes only in the read-only `pull_request`/`push` workflow.
The trusted `pull_request_target` evidence workflow remains unchanged and does not
execute candidate code.

The HTML5 CI job now embeds the exact source SHA in both development and release
bundles, runs the existing BB-005/BB-003 smokes, installs pinned Playwright +
Chromium, runs deterministic visual capture, then retains three distinct artifact
classes:

- playable release bundle;
- deterministic visual-QA package;
- build/browser diagnostics.

## Decision impact

No `DECISIONS.md` status changes.

Relevant decisions remain:

- `V-001 VALIDATED` — visual baseline to be proved/tuned by runtime captures;
- `T-002 LOCKED` — HTML5 first;
- `T-012 LOCKED` — significant player-facing work requires deterministic rendered
  evidence;
- `R-001 LOCKED` — rendered evidence is part of the development chain;
- `R-014 LOCKED` — player-facing visual evidence is exact-head/provenance bound;
- `R-016 LOCKED` — governance workflow changes require explicit trust-boundary and
  rollback analysis.

Provenance: `TECH_CONSTRAINT` plus implementation of the already validated BB-P008
contract.
Evidence strength before runtime CI: `MEDIUM`; it becomes `HIGH` for the technical
capture-path claim only after exact-head repeated capture and release guard pass.

## Closeout gate

BB-006 is complete only when an exact final PR head proves all of the following:

- development and release HTML5 bundles contain the exact source SHA in toolchain
  evidence;
- `movement_empty` reaches `captureReady` with matching state/seed/SHA;
- desktop `1280×720` and mobile-landscape `844×390` PNGs exist;
- a second isolated capture of each viewport produces the same SHA-256 and
  simulation frame;
- capture report contains exact-head, bundle, browser and capture provenance;
- browser console/page/resource checks are clean;
- release exposes no QA bridge and QA query parameters do not alter the captured
  release output;
- the visual-QA artifact is retained by CI;
- Test/data, repository standards and trusted-base evidence checks also pass;
- the merged `main` repeats the production CI checks.
