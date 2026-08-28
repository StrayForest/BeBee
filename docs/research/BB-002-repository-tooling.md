# BB-002 — Repository/tooling standards

Date checked: 2026-08-28

## Problem

After the minimal Defold bootstrap, BeBee needs a stable repository contract before more runtime systems are added. A fresh contributor/agent must be able to tell which files are generated, where production resources belong, which text/lint conventions apply, how third-party material is reviewed, and which commands are authoritative. These rules also need a mechanical CI check so they do not depend on memory.

## Task classification

This is technical/tooling work. Shipped-game competitor research is not relevant: the problem is repository correctness and Defold tool integration rather than player-facing behavior. Current Defold documentation/source and the repository's existing architecture are the primary authorities.

## Official documentation/source checked

1. Defold editor Git integration — current `editor/src/clj/editor/git.clj`
   - https://github.com/defold/defold/blob/dev/editor/src/clj/editor/git.clj
   - The editor requires `/.editor_settings`, `/.internal` and `/build` to be ignored and additionally suggests common OS metadata ignores.
2. Defold — Writing code
   - https://defold.com/manuals/writing-code/
   - The editor integrates Luacheck and supports a project-root `.luacheckrc`; Defold documents its baseline Luacheck settings.
3. Defold — Library projects
   - https://defold.com/manuals/libraries/
   - Project dependencies are URL-addressed library archives; release URLs/tags provide a stable versioned dependency shape.
4. Defold License
   - https://defold.com/license/
   - Defold is distributed under the Defold License and license/redistribution obligations must be considered for shipped use.
5. Defold tools third-party licenses
   - https://github.com/defold/defold/blob/dev/TOOLS_LICENSES.md
   - Defold tools include third-party components, so build-tool provenance cannot be treated as "no third party" merely because BeBee does not vendor `bob.jar`.

The already-pinned engine/build contract remains `tools/defold/toolchain.json` from BB-001.

## Alternatives

### A — Add a conventional external formatter/linter stack immediately

Examples would be standalone Luacheck plus a Lua formatter and Python formatting/lint packages.

Rejected for BB-002 because:

- it creates several new installation/version/license surfaces before the codebase needs them;
- a fresh-clone standards check would depend on a package resolver and external registry availability;
- repository hygiene, JSON validity, Python syntax, generated roots and source placement can be checked deterministically with the Python standard library;
- Defold already exposes Luacheck during editor work and supports `.luacheckrc`.

This remains reopenable when a concrete formatting/lint problem justifies the dependency cost.

### B — Documentation-only conventions

Rejected because an autonomous-agent repository will drift if the rules are only prose. Generated output, dependency registration and source placement need mechanical failure modes.

### C — Machine-readable contract + stdlib validator + Defold editor lint — selected

Selected structure:

- `.gitignore` for generated/editor/build state;
- `.editorconfig` for editor-facing text conventions;
- `.luacheckrc` for explicit Defold-compatible Lua lint settings;
- `config/repository-standards.json` for canonical paths/rules/commands;
- `config/dependencies.json` + `THIRD_PARTY.md` for dependency/license intake;
- `scripts/check_repository_standards.py` as a dependency-free executable gate;
- pull-request/main CI for the executable gate.

This creates one reviewable source of truth and does not require a new package solely to validate the policy.

## Stable source-layout decision

`docs/05-technical-architecture.md` already proposed a dependency-oriented source tree. BB-002 converts its production runtime roots into an explicit validator contract:

```text
app/
input/
main/
data/
gameplay/
ui/
systems/
adapters/
levels/
art/
audio/
```

`prototypes/` remains explicitly non-production. Empty roots are not created until needed.

The gate checks known Defold/runtime resource extensions, not arbitrary documentation/tool files, so the rule protects production placement without forcing all repository content into runtime directories.

## Dependency/license decision

The dependency manifest begins with the technology already used by the bootstrap:

- Defold Engine 1.13.1;
- Defold Bob 1.13.1.

Future Defold library URLs in `game.project` must match a reviewed `kind: defold-library` manifest entry exactly. Unknown commercial-use/redistribution status fails the intake process rather than being assumed safe.

## Commands

```text
python3 scripts/check_repository_standards.py
python3 tools/defold/bundle_html5.py --mode development
python3 tools/defold/bundle_html5.py --mode release
```

The standards command needs only Python 3 and Git. The build commands retain BB-001's pinned Java/Bob requirements.

## Acceptance criteria

- `.gitignore` covers Defold-required and BeBee-generated roots;
- UTF-8/LF/final-newline/whitespace and indentation conventions are explicit;
- Lua lint settings are explicit in project root;
- production runtime roots are explicit and mechanically checked;
- dependency/license intake has machine + human ledgers;
- existing Defold/Bob third-party technology is no longer mislabeled as "none";
- `game.project` dependencies cannot silently bypass the dependency ledger;
- standards command is documented and CI-executed;
- existing development/release build commands remain documented;
- no BB-003–BB-007 runtime capability is claimed by this task.

## Verification plan

1. Run `python3 scripts/check_repository_standards.py` on the exact PR head.
2. Run the existing trusted PR evidence policy against the exact PR head.
3. Keep the existing Defold runtime evidence workflow green so repository hygiene changes do not regress the BB-001 bootstrap/build path.
4. Review the diff specifically for accidental gameplay/input/storage scope expansion.

Player-facing screenshot comparison is not applicable to this tooling-only task.
