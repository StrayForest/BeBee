# BB-004 — Test/data harness

Checked: 2026-08-28

## Scope

BB-004 creates the smallest deterministic test/data boundary needed before gameplay
systems scale:

- a dependency-free Lua unit test runner;
- a dedicated Defold headless test bootstrap, separate from the production bootstrap;
- a canonical data catalog plus deterministic structural/reference validation;
- first deterministic tests against merged production input semantics and the data
  validator's positive/negative cases;
- an editor-independent command that builds and runs the suite with the repository-
  pinned Defold/Bob/Java toolchain;
- structured machine-readable test completion and a non-zero process result on
  failure.

This implementation PR does not change production gameplay, HTML5 artifact
retention, visual capture, storage, economy values or authored flower/region
content. CI wiring is intentionally isolated into the BB-004 follow-up process PR
because the trusted repository policy requires workflow changes to use the
`process` change class while runtime Lua requires `technical`.

## Official documentation checked

### Defold automated testing and verification

Source: https://defold.com/manuals/automated-testing/

Verified constraints and recommendations:

- reusable deterministic logic should be exercised with module-level tests;
- engine-dependent tests should use a dedicated test collection/bootstrap;
- CI should build a headless bundle with Bob using dedicated settings;
- the process controller should capture exit status/logs, enforce a timeout and
  require a structured suite-completion event;
- a small project-local runner is an acceptable alternative to a community test
  library.

### Defold Bob project builder

Source: https://defold.com/manuals/bob/

Verified constraints:

- `x86_64-linux` is a supported target;
- `--variant headless` selects the headless engine for bundling;
- `--settings` applies the dedicated test bootstrap without replacing the normal
  production `game.project`;
- the bundle output is named from the project title.

### Defold sys API

Source: https://defold.com/ref/stable/sys-lua/

Verified constraint:

- `sys.exit(code)` terminates the application and provides the process exit code,
  allowing deterministic suite failure to propagate to CI.

## Alternatives

### A — small repository-local Defold runner — selected

Use plain Lua modules for assertions/suites, a dedicated test collection, Bob
headless bundling and a Python process controller that reuses the already pinned
Bob verification helpers.

Why selected:

- matches current official Defold guidance;
- runs inside the real Defold Lua environment, including `hash()`;
- adds no third-party framework or license surface for the initial eleven-case
  foundation;
- produces an explicit structured completion record plus OS exit status;
- can grow incrementally without coupling production code to a test framework.

### B — add a community Defold test framework — rejected for BB-004

A mature library could become useful later, but the current requirement is small.
Adding a dependency now would create version/license/maintenance work before the
project has enough tests to justify it. Revisit only if the local runner becomes a
maintenance burden.

### C — host-only Lua/Python tests — rejected as the primary runner

Host tests are fast, but they can miss Defold-specific globals and runtime Lua
behavior. In particular the first production module under test uses Defold
`hash()` values. The headless engine therefore provides a stronger foundation.
Python remains only the deterministic process/build controller.

## Data contract

`data/catalog.lua` is the canonical entry point. BB-004 deliberately starts with
empty production arrays; later content tickets populate them.

`data/validator.lua` currently rejects:

- unsupported catalog schema versions;
- missing/non-array content collections;
- malformed authored IDs;
- duplicate stable IDs across the catalog;
- seed references to unknown flowers;
- meadow references to unknown regions;
- region references to unknown meadows.

The validator returns sorted errors so the same invalid catalog produces stable
diagnostics.

## Test contract

The suite emits console events prefixed with `BEBEE_TEST `. The final event is one
JSON object with `event = "suite_end"`, pass/fail status and deterministic counts.

`tools/defold/run_tests.py`:

1. verifies the pinned Java major and Bob SHA/version;
2. builds a dedicated `x86_64-linux` headless bundle using `tests/test.settings`;
3. runs the resulting headless engine with a timeout;
4. retains the complete process log;
5. parses structured `BEBEE_TEST` events;
6. requires exactly one passing `suite_end` event and process exit code `0`;
7. writes `build/test-results/summary.json`.

Any build error, timeout, malformed/missing completion event, failed test or
non-zero engine exit fails the command.

## First deterministic coverage

`tests/test_input_semantics.lua` covers:

- semantic action-name lookup;
- movement membership;
- pointer defaults;
- strict pointer normalization.

`tests/test_data_validation.lua` covers:

- the production catalog;
- a valid referenced catalog;
- duplicate stable IDs;
- invalid ID format;
- broken region reference;
- broken seed/flower reference;
- sparse arrays.

## Repository impact

`tests` becomes an explicit `allowed_nonproduction_runtime_root` in
`config/repository-standards.json`. It is not added to
`canonical_runtime_roots`, so test Defold resources remain visibly separate from
production resources.

The canonical local command is:

```text
bash scripts/test.sh
```

## Decision impact

No `DECISIONS.md` status changes.

Provenance: `TECH_CONSTRAINT`.
Evidence strength: `HIGH` for the harness architecture because it follows current
official Defold headless-test/process guidance and is exercised in the actual
Defold runtime. Exact production gameplay test breadth remains intentionally small
at this foundation stage.

## Follow-up boundary

The second BB-004 PR adds CI wiring only. It must make test/data errors fail an
exact-source PR/main workflow without weakening the existing trusted PR evidence
boundary. BB-005 remains responsible for the broader playable HTML5 PR artifact
contract.
