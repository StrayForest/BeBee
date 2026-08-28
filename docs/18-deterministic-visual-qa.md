# 18 — Deterministic Visual QA

Status: **BB-P008 design VALIDATED; P0/`BB-006` foundation IMPLEMENTED.**

Canonical machine-readable contract: [`config/visual-qa.json`](../config/visual-qa.json).

## 1. Problem

BeBee requires agents to inspect the actual rendered game, but an instruction to “take screenshots” is not enough. Without deterministic state injection, exact-build provenance, fixed viewports, readiness signaling and retained artifacts, screenshots from two runs may represent different state, timing, storage, browser or code.

BB-P008 defined the contract P0 had to implement so later visual evidence is reproducible and bound to the exact commit being evaluated. BB-006 now proves that foundation in the real Defold HTML5 runtime.

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

Examples for future player-facing fixtures:

```text
?qa=movement_empty
?qa=pollination_active_50
?qa=flower_hard_gate
?qa=hud_default
?qa=meadow_restored
```

The P0 infrastructure proof uses:

```text
?qa=foundation_probe&qa_seed=88008
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

Development/CI exposes a bridge named:

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

BB-006 binds `buildCommitSha` through the canonical Bob build command rather than PR prose. Root `game.properties` declares the QA runtime settings; development explicitly enables the bridge and release explicitly disables it.

## 5. State registry

The canonical **player-facing** registry contains 15 states covering the evidence classes required by the roadmap and scorecard:

- movement: `movement_empty`, `movement_dense`;
- pollination: `pollination_idle`, `pollination_active_50`, `pollination_complete`;
- gates: `flower_soft_gate`, `flower_hard_gate`;
- HUD: `hud_default`;
- Hive: `hive_affordable`, `hive_unaffordable`;
- seeds: `seed_locked`, `seed_unlocked`;
- restoration: `meadow_dormant`, `meadow_mid`, `meadow_restored`.

P0 additionally defines one non-player-facing infrastructure fixture:

- foundation: `foundation_probe`.

`foundation_probe` exists only to prove the router/readiness/provenance/capture machinery before P1 gameplay exists. It does **not** count as implementation of `movement_empty` or any other player-facing state.

The exact state-to-viewport matrix and observable assertions live in `config/visual-qa.json`. Adding a player-facing system normally adds or implements its QA fixture rather than creating an ad-hoc screenshot script.

## 6. Viewports

BB-P008 consumes V-001 rather than duplicating independent dimensions.

Canonical baseline:

- `desktop_reference`: 1280×720;
- `poki_small`: 640×360;
- `poki_medium`: 836×470;
- `poki_large`: 1031×580;
- `mobile_landscape`: 844×390.

`hud_default` covers all five because responsive HUD drift can appear even when world composition is unchanged. Other states use only the smallest viewport set needed to prove their target problem.

The BB-006 foundation proof uses `desktop_reference` and `mobile_landscape`.

These dimensions are synchronized by `tools/visual_qa/check_visual_qa_plan.py` against `config/visual-style.json` so visual QA cannot silently diverge from V-001.

## 7. Implemented P0 capture pipeline

The exact-head flow is now:

```text
checkout exact PR head
 -> Bob builds development + release HTML5 bundles
 -> bind exact source SHA and hash bundle/provenance
 -> serve locally over HTTP with scripts/serve_html5.py
 -> launch pinned Playwright Chromium
 -> create isolated BrowserContext
 -> set exact viewport
 -> navigate to ?qa=<state>&qa_seed=<seed>
 -> wait for engineReady + captureReady
 -> assert stateId + seed + buildCommitSha
 -> collect console/page errors
 -> capture PNG
 -> repeat unchanged foundation fixture in a fresh context
 -> require exact repeated PNG SHA-256 equality
 -> verify release exposes neither bridge nor probe
 -> write capture-report.json + console.log
 -> retain CI artifact
```

Defold's automated-testing documentation treats HTML5 browser automation and runtime screenshots as valid runtime evidence and recommends an explicit JavaScript testing bridge for reliable browser testing. Bob is the command-line build/bundle tool for CI. HTML5 bundles are served over HTTP rather than opened from `file://`; the canonical server explicitly serves WebAssembly as `application/wasm`.

Playwright BrowserContexts are used for independent captures because they isolate cookies, local/session storage and other browser state, reducing order-dependent evidence.

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

Motion where required later:

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

BB-006 CI retains this directory as a dedicated `visual-qa-<head_sha>` Actions artifact alongside the separate playable HTML5 and HTML5 diagnostic artifacts.

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

For `foundation_probe`, unchanged repeated captures also fail when exact PNG SHA-256 values differ. This is an observed stability assertion for that controlled fixture, not a universal golden-image policy.

After P0, a substantial player-facing PR declares its affected QA states. Missing required exact-head artifacts becomes a merge failure where the repository can enforce it.

## 10. Why there is still no universal pixel-diff threshold

P-1 deliberately did **not** invent a global screenshot-diff percentage. BB-006 now proves that one controlled infrastructure fixture is exactly stable across fresh contexts, but that does not justify applying an arbitrary threshold to gameplay art, animation or world transformations.

Later stable surfaces such as HUD or locked-state UI may use thresholded golden comparison after their own repeated-capture behavior is measured. Art changes and world transformations still require semantic/evidence evaluation rather than treating every pixel change as a regression.

## 11. Current official technical basis

Checked 2026-08-29:

- Defold automated testing: https://defold.com/manuals/automated-testing/
- Defold Bob: https://defold.com/manuals/bob/
- Defold HTML5 API: https://defold.com/ref/stable/html5-lua/
- Defold project settings: https://defold.com/manuals/project-settings/?lang=en
- Playwright BrowserContext isolation: https://playwright.dev/python/docs/browser-contexts
- Playwright Python library/browser installation: https://playwright.dev/python/docs/library and https://playwright.dev/python/docs/browsers

Current relevant constraints:

- Defold distinguishes build evidence from runtime/browser evidence;
- browser automation can resize viewport, collect console/JavaScript errors and capture screenshots;
- an explicit JS testing bridge is the reliable browser-test boundary;
- Bob supports multiple settings and command-line CI bundling for `wasm-web`;
- HTML5 testing requires HTTP serving and correct `.wasm` MIME handling;
- Playwright BrowserContexts provide isolated clean-slate browser sessions.

## 12. BB-006 runtime proof

The first complete capture proof is Actions run `33214438370` on exact candidate head `56fa405c48d7c193c5e9888b825c48a0779c93a2`.

`capture-report.json` recorded:

- Playwright Chromium `151.0.7922.34`;
- Defold `1.13.1`;
- seed `88008`;
- exact candidate `buildCommitSha`;
- bundle SHA-256 `fd0f30b989f1d65dc493a7128897a9d671b8b665303236ec944fd8c2e4c0cdf0`;
- desktop 1280×720 repeated hash `9efcf3f167dad760168b6d3fe14dc3b5126115960bda827260ac4687a8cc1f11` twice;
- mobile 844×390 repeated hash `046b359c483baeb1cae2240dd0c8a01000dab6509047b41e99197e746de2c471` twice;
- zero console errors and zero page errors;
- release `bridge_present=false`, `probe_present=false`.

The retained visual artifact is `9702826036` with Actions digest `sha256:cabb48fd669f9f55e1482a55413538da6d33fbfb2c8fdeb9dfb22301d997593d`.

Therefore the BB-P008 implementation contract is no longer hypothetical infrastructure: the P0 still-capture foundation is operational. Motion capture and the fifteen player-facing fixture implementations remain scoped to the systems that need them.
