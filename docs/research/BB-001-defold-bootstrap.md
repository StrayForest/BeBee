# BB-001 — Defold bootstrap

Date checked: 2026-08-28

## Problem

BeBee needs the smallest production runtime that can be built outside the Defold editor in a reproducible HTML5 pipeline. The bootstrap must establish engine/version/build boundaries without prematurely implementing input, storage, collection-proxy lifecycle, gameplay, UI or content owned by later P0 tasks.

## Decision status

Relevant existing decisions:

- `T-001 LOCKED` — Defold + Lua.
- `T-002 LOCKED` — HTML5-first and touch-compatible architecture.
- `R-012 LOCKED` — high-risk runtime work requires same-PR technical evidence.

No product or technical decision status changes in BB-001.

## Official documentation checked

1. Defold — Bob command line tool: https://defold.com/manuals/bob/
   - Bob is the editor-independent command-line build tool.
   - The current Bob tool requires OpenJDK 25.
   - Build variants include `debug` and `release`.
   - HTML5 uses platform/architecture `wasm-web`.
   - Settings overlays can be supplied with `--settings`.
2. Defold — Project settings: https://defold.com/manuals/project-settings/
   - `game.project` is the project root configuration.
   - Resource-valued project settings use compiled resource paths, hence `/app/bootstrap.collectionc` for the bootstrap collection.
3. Defold — Automated testing: https://defold.com/manuals/automated-testing/
   - Bob is suitable for CI/editor-independent builds and supports scripted resolve/build/bundle flows.
4. Defold stable release 1.13.1: https://github.com/defold/defold/releases/tag/1.13.1
   - Stable release published 2026-08-17.
   - Published `bob.jar` digest used by BeBee: `sha256:8f2b1381fd4d0fb92816403cd0056cb7db5ad4083615be8dcc2d868fb4939938`.

## Alternatives

### A — Pin a stable Defold release and Bob digest — selected

Store the exact Defold version, Bob URL, Bob SHA-256, Java major and HTML5 platform in a machine-readable repository file. The build helper verifies Java, Bob digest and Bob-reported engine version before building.

Why selected:

- a fresh environment does not silently move to a newer engine;
- a replaced/corrupt Bob artifact fails before compilation;
- local and CI paths use the same contract;
- upgrading Defold becomes an explicit reviewable repository change.

### B — Download `latest` Bob — rejected

A floating release would make historical commits non-reproducible and could introduce new engine/build behavior without a BeBee code change.

### C — Commit `bob.jar` into the repository — rejected

The binary is large, duplicates upstream distribution, increases repository size and is unnecessary when the exact upstream artifact is addressable and checksum-verified.

## Bootstrap boundary

Selected source path:

```text
game.project
app/bootstrap.collection
app/bootstrap.go
app/bootstrap.script
```

`app/` is the long-lived application/bootstrap layer already described by `docs/05-technical-architecture.md`. No collection proxy is introduced, so `T-010` remains a hypothesis for BB-003 rather than being silently decided here.

The bootstrap controller only proves that the Defold lifecycle reaches Lua initialization. It does not own gameplay, progression, GUI, input or storage.

## Development / release configuration

- development: Bob `--variant debug` + `config/defold/development.settings`;
- release: Bob `--variant release` + `config/defold/release.settings`.

Both target `wasm-web` and write isolated outputs under `build/html5/<mode>/BeBee`.

## Reproduction commands

With Java 25 available:

```text
python3 tools/defold/bundle_html5.py --mode development
python3 tools/defold/bundle_html5.py --mode release
```

The helper downloads the pinned Bob artifact into a user cache by default, verifies SHA-256, verifies the Bob/Defold version, builds an archive, bundles HTML5 and requires `index.html` to exist. `--bob /path/to/bob.jar` may be used only when that local file matches the pinned digest.

## Acceptance criteria

- root `game.project` boots `/app/bootstrap.collectionc`;
- the collection contains one minimal controller object and no speculative gameplay systems;
- development and release modes are explicit and isolated;
- Defold 1.13.1 / Java 25 / `wasm-web` / Bob SHA-256 are machine-readable and enforced by the build helper;
- exact-head CI can produce development and release HTML5 bundles from the PR branch;
- no save format, input behavior, collection-proxy lifecycle or player-facing design is claimed as implemented.
