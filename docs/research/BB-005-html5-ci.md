# BB-005 — HTML5 CI

Checked: 2026-08-29

## Scope

BB-005 turns the existing narrow Defold runtime-evidence workflow into the
production HTML5 CI contract for P0:

- every pull request and `main` update checks out the exact source revision;
- the repository-pinned Defold 1.13.1 / Bob / OpenJDK 25 toolchain builds both
  development and release `wasm-web` bundles;
- the existing `Test and data` workflow remains the canonical independent unit/data
  validation gate and continues to run on every PR and `main` update;
- the release bundle is retained as a dedicated playable GitHub Actions artifact;
- the release bundle is served over HTTP and exercised in headless Chromium;
- browser smoke requires a usable non-zero canvas, WebAssembly availability, a
  successful `.wasm` response with `application/wasm`, no non-cancelled resource
  load failures, no error-level browser console entries and no runtime exceptions;
- the already-proven BB-003 keyboard/touch/proxy-focus smoke remains active against
  the development bundle;
- build reports, browser logs, smoke JSON, screenshot, exact head SHA and release
  file hashes are retained separately from the playable artifact.

BB-005 does not implement deterministic QA-state routing/capture, storage, gameplay,
new input behavior or player-facing content. Those remain BB-006 and BB-007.

## Official documentation checked

### Defold HTML5

Source: https://defold.com/manuals/html5/

Verified constraints:

- an HTML5 bundle must be served over HTTP rather than opened directly from
  `index.html`;
- modern Defold HTML5 uses WebAssembly and the served `.wasm` response must use the
  `application/wasm` MIME type;
- `wasm-web` is a supported normal WebAssembly engine target.

### Defold Bob

Source: https://defold.com/manuals/bob/

Verified constraints:

- Bob is the supported editor-independent build/bundle tool for CI;
- `wasm-web` is a supported HTML5 platform architecture;
- the pinned repository builder may continue to produce distributable bundles from
  the command line with the configured build reports.

### GitHub Actions pull-request events

Source: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows

Verified constraint:

- `pull_request` normally exposes a synthetic merge ref; checking out
  `github.event.pull_request.head.sha` is required when CI intentionally validates
  the exact proposed head rather than the merge ref.

### GitHub Actions artifacts

Source: https://docs.github.com/en/actions/tutorials/store-and-share-data?apiVersion=2022-11-28

Verified constraints:

- build output can be retained after a workflow as an artifact;
- `upload-artifact` supports named artifacts and custom retention periods;
- build/test artifacts are appropriate for proposed changes and later diagnosis.

## Alternatives

### A — evolve the existing candidate-source Defold runtime workflow — selected

Keep one unprivileged `pull_request`/`push` HTML5 workflow, broaden it from the
BB-001/BB-003 bootstrap evidence path into the stable P0 artifact contract, and
retain the separate BB-004 `Test and data` workflow.

Why selected:

- avoids two independent HTML5 builds for the same PR;
- preserves exact-head behavior already proven in BB-001/BB-003;
- keeps candidate runtime execution outside the trusted `pull_request_target`
  governance workflow;
- produces a clearly named playable release artifact while retaining development
  diagnostics separately;
- keeps unit/data validation independently diagnosable instead of coupling the
  headless Linux test engine to the browser bundle job.

### B — add a second new HTML5 workflow and keep `Defold runtime evidence` — rejected

This would duplicate Bob downloads/builds and allow the two browser contracts to
drift. The old workflow has no separate long-term purpose once BB-005 owns the
HTML5 contract.

### C — move build/smoke execution into trusted PR evidence validation — rejected

The trusted workflow is governance authority and runs from the trusted base. It
must not execute candidate runtime code under its privileged trust model. Candidate
HTML5 execution remains an unprivileged `pull_request` workflow with read-only
contents.

## Browser smoke contract

`tools/defold/chromium_html5_smoke.py` uses Chromium DevTools Protocol through the
Python standard library and the repository's existing WebSocket helper. It launches
Chromium on `about:blank`, enables Runtime/Log/Page/Network observation before
navigation, then navigates to the served release artifact.

The smoke passes only when all of these are true:

1. the page emits a load event;
2. `document.readyState` becomes `complete`;
3. a canvas exists with non-zero backing dimensions;
4. WebAssembly is available;
5. at least one `.wasm` request completes with HTTP 200 and MIME
   `application/wasm`;
6. no actionable network load failure is observed (cancelled requests and favicon
   noise are ignored);
7. no error/assert browser console event is observed;
8. no JavaScript runtime exception is observed.

The smoke writes machine-readable JSON even on failure so CI does not lose the
reason for rejection.

## Artifact contract

Successful HTML5 CI retains two artifacts for the exact source SHA:

- `html5-playable-<sha>` — only the release `BeBee` bundle, directly suitable for
  local HTTP serving/playback;
- `html5-ci-evidence-<sha>` — smoke JSON/logs, release screenshot, exact SHA,
  release file SHA-256 list and Defold build/toolchain reports.

Artifacts are retained for 14 days. The playable artifact is uploaded only after
the complete build/browser step succeeds; diagnostics use `if: always()`.

## Unit/data validation boundary

BB-004 already established `bash scripts/test.sh` and the read-only `Test and data`
workflow on every PR and `main` update. BB-005 deliberately does not run that same
headless bundle a second time inside the browser job. The P0 PR contract is the
conjunction of the dedicated `Test and data` signal and `HTML5 CI` signal.

## Decision impact

No `DECISIONS.md` status changes.

Relevant locked process/technical constraints remain `T-002`, `R-001`, `R-015` and
`R-016`.

Provenance: `TECH_CONSTRAINT`.
Evidence strength: `HIGH` for the CI/artifact architecture because it follows the
current Defold HTML5/Bob serving requirements and GitHub exact-head/artifact model.
The browser smoke's exact runtime behavior must still be proven by candidate CI
before BB-005 is marked complete.

## Closeout gate

BB-005 is complete only after an exact candidate head proves:

- `HTML5 CI` passes development/release builds and both browser smokes;
- `Test and data` passes the deterministic 11-case suite;
- a dedicated playable release artifact and HTML5 evidence artifact exist;
- repository standards and trusted-base evidence/trust-boundary validation pass;
- the final merge head repeats all required checks successfully.
