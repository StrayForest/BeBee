# 18 — Deterministic Visual QA

Status: **BB-P008 design VALIDATED**. Runtime implementation belongs to P0/`BB-006`.

Canonical machine-readable contract: [`config/visual-qa.json`](../config/visual-qa.json).

## 1. Problem

BeBee requires agents to inspect the actual rendered game, but an instruction to “take screenshots” is not enough. Without deterministic state injection, exact-build provenance, fixed viewports, readiness signaling and retained artifacts, screenshots from two runs may represent different state, timing, storage, browser or code.

BB-P008 defines the contract P0 must implement so later visual evidence is reproducible and bound to the exact commit being evaluated.

## 2. Evidence hierarchy

Use the narrowest evidence that proves the claim:

1. static/model tests for pure rules;
2. running-engine assertions for engine behavior;
3. deterministic still captures for hierarchy/readability/layout;
4. deterministic motion evidence for camera, interaction timing, VFX and transitions;
5. target-device/portal checks when browser emulation is insufficient.

A successful Defold build is not evidence that gameplay or rendering is correct. A still image is not sufficient proof for timing or motion behavior.

## 3. QA state injection

Development and CI HTML5 builds expose a development-only state router:

```text
?qa=<state_id>&qa_seed=<integer>
```

Examples:

```text
?qa=movement_empty
?qa=pollination_active_50
?qa=flower_hard_gate
?qa=hud_default
?qa=meadow_restored
```

Rules:

- QA fixtures are repository-authored and do not depend on a player's save;
- random behavior uses the supplied fixed seed;
- wall-clock time is not an input to captured state;
- required captures have no runtime network dependency;
- independent captures use fresh isolated browser contexts;
- unknown states fail closed;
- release builds ignore QA parameters and must not expose the testing bridge.

## 4. JavaScript readiness bridge

P0 exposes a development-only bridge named:

```text
window.__bebeeQA
```

The bridge reports at minimum:

```text
schemaVersion
stateId
seed
engineReady
captureReady
simulationFrame
buildCommitSha
```

`captureReady=true` is authoritative. It is set only after:

- the requested fixture is fully applied;
- state-local asynchronous resources are ready;
- transient setup animation/effects are finished;
- the simulation is frozen or has reached the fixture's declared deterministic capture frame.

The browser runner must not replace this with arbitrary sleep-based capture.

## 5. Canonical state registry

The initial P0 registry contains 15 states covering the evidence classes already required by the roadmap and scorecard:

- movement: `movement_empty`, `movement_dense`;
- pollination: `pollination_idle`, `pollination_active_50`, `pollination_complete`;
- gates: `flower_soft_gate`, `flower_hard_gate`;
- HUD: `hud_default`;
- Hive: `hive_affordable`, `hive_unaffordable`;
- seeds: `seed_locked`, `seed_unlocked`;
- restoration: `meadow_dormant`, `meadow_mid`, `meadow_restored`.

The exact state-to-viewport matrix and observable assertions live in `config/visual-qa.json`. Adding a player-facing system normally adds or updates a QA fixture rather than creating an ad-hoc screenshot script.

## 6. Viewports

BB-P008 consumes V-001 rather than duplicating independent dimensions.

Canonical baseline:

- `desktop_reference`: 1280×720;
- `poki_small`: 640×360;
- `poki_medium`: 836×470;
- `poki_large`: 1031×580;
- `mobile_landscape`: 844×390.

`hud_default` covers all five because responsive HUD drift can appear even when world composition is unchanged. Other states use only the smallest viewport set needed to prove their target problem.

These dimensions are synchronized by `tools/visual_qa/check_visual_qa_plan.py` against `config/visual-style.json` so visual QA cannot silently diverge from V-001.

## 7. Capture pipeline required in P0

The intended exact-head flow is:

```text
checkout exact PR head
 -> Bob builds one HTML5 bundle
 -> hash bundle/provenance
 -> serve locally over HTTP
 -> launch pinned Playwright Chromium
 -> create isolated BrowserContext
 -> set exact viewport
 -> navigate to ?qa=<state>&qa_seed=<seed>
 -> wait for engineReady + captureReady
 -> assert stateId + seed + buildCommitSha
 -> collect console/page errors
 -> capture PNG and required motion evidence
 -> hash captures
 -> write capture-report.json
 -> retain CI artifact
```

Defold's current automated-testing documentation explicitly treats HTML5 browser automation and runtime screenshots as valid runtime evidence and recommends an explicit JavaScript testing bridge for reliable browser testing. Bob is the command-line build/bundle tool for CI. HTML5 bundles must be served over HTTP rather than opened from `file://`; the server must serve WebAssembly with the correct MIME type.

Playwright BrowserContexts are intentionally used for independent states because they isolate cookies, local/session storage and other browser state, reducing order-dependent evidence.

## 8. Artifact contract

CI artifact root:

```text
artifacts/visual-qa/<head_sha>/
```

Required top-level evidence:

```text
capture-report.json
console.log
```

Still:

```text
<state_id>/<viewport_id>.png
```

Motion where required:

```text
<state_id>/<viewport_id>.webm
```

Every capture report binds the artifact to at least:

- PR head SHA;
- bundle SHA-256;
- Defold version;
- browser name/version;
- state ID and seed;
- viewport ID/dimensions;
- simulation frame;
- capture path and capture SHA-256;
- console/page error counts.

## 9. Failure rules

Capture fails rather than silently falling back when:

- the requested state is unknown;
- the QA bridge is absent in a development/CI build;
- readiness times out;
- state, seed or build SHA does not match the request;
- required still/motion evidence is absent;
- capture dimensions differ from the configured viewport;
- hashes disagree with the report;
- unexpected page/console errors occur;
- a release bundle exposes the QA bridge or accepts QA state injection.

After P0, a substantial player-facing PR declares its affected QA states. Missing required exact-head artifacts becomes a merge failure where the repository can enforce it.

## 10. Why no universal pixel-diff threshold yet

P-1 deliberately does **not** invent a global screenshot-diff percentage. Before the production renderer, browser version, asset pipeline and deterministic fixtures exist, such a threshold would be arbitrary.

P0 first proves stable repeated capture. Later, stable surfaces such as HUD or locked-state UI may use thresholded golden comparison. Art changes and world transformations still require semantic/evidence evaluation rather than treating every pixel change as a regression.

## 11. Current official technical basis

Checked 2026-08-28:

- Defold automated testing: https://defold.com/manuals/automated-testing/
- Defold Bob: https://defold.com/manuals/bob/
- Defold HTML5: https://defold.com/manuals/html5/
- Playwright isolation: https://playwright.dev/docs/browser-contexts

Current relevant constraints:

- Defold distinguishes build evidence from runtime/browser evidence;
- browser automation can resize viewport, collect console/JavaScript errors and capture screenshots;
- an explicit JS testing bridge is the recommended reliable browser-test boundary;
- Bob supports command-line CI bundling for `wasm-web`;
- HTML5 testing requires HTTP serving and correct `.wasm` MIME handling;
- Playwright BrowserContexts provide isolated clean-slate browser sessions.

## 12. P0 implementation acceptance

`BB-006` cannot claim the visual-QA foundation complete until:

- a real Defold HTML5 bundle exposes the dev-only QA bridge;
- at least one deterministic state is captured at desktop and mobile-landscape sizes;
- repeated runs of that unchanged state are stable enough to support later regression work;
- exact-head SHA and artifact hashes are present in the report;
- browser console/page errors are captured;
- CI retains the playable build and visual evidence;
- a release build proves the QA injection/bridge is absent.

Until then BB-P008 is a validated **implementation contract**, not evidence that runtime capture already exists.
