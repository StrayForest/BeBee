# 18 — Deterministic Visual QA

Status: **BB-P008 design VALIDATED; P0 / BB-006 runtime foundation IMPLEMENTED.**

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

BB-006 implements only the minimum technical `movement_empty` fixture required to prove the pipeline. That fixture does not yet satisfy future P1 player-facing assertions such as the real bee being visible; P1 owns that scene/content upgrade.

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

The implemented exact-head flow is:

```text
checkout exact PR head
 -> Bob builds development + release HTML5 bundles with embedded source SHA
 -> hash bundle/provenance
 -> serve locally over HTTP
 -> launch pinned Playwright Chromium
 -> create isolated BrowserContext
 -> set exact viewport
 -> navigate to ?qa=<state>&qa_seed=<seed>
 -> wait for engineReady + captureReady
 -> assert stateId + seed + buildCommitSha
 -> collect HTTP/request/console/page errors
 -> capture PNG
 -> repeat in a fresh BrowserContext and require identical hash/frame
 -> adversarially probe release with and without QA query parameters
 -> hash captures
 -> write capture-report.json + console.log
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
- repeated unchanged captures disagree;
- hashes disagree with the report;
- unexpected HTTP/request/page/console errors occur;
- a release bundle exposes the QA bridge or responds to QA state injection.

After P0, a substantial player-facing PR declares its affected QA states. Missing required exact-head artifacts becomes a merge failure where the repository can enforce it.

## 10. Why no universal pixel-diff threshold yet

P-1 deliberately does **not** invent a global screenshot-diff percentage. Before the production renderer, browser version, asset pipeline and deterministic fixtures exist, such a threshold would be arbitrary.

P0 first proves stable repeated capture. Later, stable surfaces such as HUD or locked-state UI may use thresholded golden comparison. Art changes and world transformations still require semantic/evidence evaluation rather than treating every pixel change as a regression.

## 11. Current official technical basis

Checked 2026-08-29:

- Defold automated testing: https://defold.com/manuals/automated-testing/
- Defold Bob: https://defold.com/manuals/bob/
- Defold HTML5: https://defold.com/manuals/html5/
- Defold HTML5 Lua API: https://defold.com/ref/stable/html5-lua/
- Defold project settings: https://defold.com/manuals/project-settings/
- Playwright isolation: https://playwright.dev/docs/browser-contexts

Current relevant constraints:

- Defold distinguishes build evidence from runtime/browser evidence;
- browser automation can resize viewport, collect console/JavaScript errors and capture screenshots;
- an explicit JS testing bridge is the recommended reliable browser-test boundary;
- Bob supports command-line CI bundling for `wasm-web` and multiple ordered settings files;
- HTML5 testing requires HTTP serving and correct `.wasm` MIME handling;
- Playwright BrowserContexts provide isolated clean-slate browser sessions.

## 12. BB-006 runtime proof

Exact candidate `997d9a12465f01bb71de6adba5bbe6290c7caf72` passed HTML5 CI run `33214094696`.

Observed retained proof:

- Defold `1.13.1`;
- Chromium `151.0.7922.34`;
- QA state `movement_empty`, seed `88008`, `simulationFrame=2`;
- embedded runtime `buildCommitSha` matched the exact candidate;
- desktop `1280×720` capture SHA-256 `c0899c9a375828992b3c78363b13b699c455d9a4366c861dc3555ae83a46de3a`;
- second isolated desktop capture produced the same hash;
- mobile-landscape `844×390` capture SHA-256 `a10aaefb247a47d6044c3dc6c66dc3ece8b974e16ebaa170d2c0b269be5d6c5d`;
- second isolated mobile capture produced the same hash;
- both required captures recorded zero actionable console/page errors;
- release exposed no `window.__bebeeQA` in plain or QA-query contexts;
- plain release and QA-query release captures both hashed to `7a5175f59992a07616d58b06a310b2a3909c43df6d406a736ef54995563a09ed`;
- retained visual artifact: `9702710185`, digest `sha256:884a1d62dff6641a0859887e18203e3afe41e032831921a1610b2facd7e8a0cb`.

The retained desktop/mobile PNGs were opened and visually inspected. They show the expected P0 technical bootstrap: a black Defold canvas plus development footer. No bee/game content is present, so these frames prove the capture/crop/provenance pipeline only; they are not accepted as P1 movement-quality evidence.

Repository standards run `33214094704` and Test/data run `33214094702` also passed on that exact candidate. The final closeout head must repeat the full candidate/trusted gate set before merge.

## 13. P0 implementation acceptance

The BB-006 implementation foundation is accepted when the final merge head repeats:

- a real Defold HTML5 development bundle exposing the dev-only QA bridge;
- deterministic `movement_empty` capture at desktop and mobile-landscape sizes;
- exact repeated capture hash/frame equality in clean BrowserContexts;
- exact-head SHA, bundle, browser and capture hashes in the report;
- retained browser console/page/error evidence;
- retained playable build and visual evidence artifacts;
- release proof that QA injection/bridge is absent;
- repository standards, Test/data and trusted-base evidence validation.

BB-006 satisfies the technical implementation contract. Later milestones still own the real state content and player-facing visual assertions for each canonical fixture.
