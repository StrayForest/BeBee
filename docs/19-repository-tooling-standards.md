# 19 — Repository and Tooling Standards

## 1. Scope

`BB-002` establishes the repository contract that later production work must follow. It standardizes generated-file handling, text/lint conventions, dependency/license intake, source placement and reproducible commands without implementing gameplay owned by later P0 tasks.

Authoritative machine-readable rules live in:

- `config/repository-standards.json`;
- `config/dependencies.json`;
- `.gitignore`;
- `.editorconfig`;
- `.luacheckrc`.

The executable gate is:

```text
python3 scripts/check_repository_standards.py
```

## 2. Generated and local files

Defold editor/build state must not enter source control. The repository ignores at minimum:

```text
/.editor_settings
/.internal
/build
```

BeBee also reserves local/generated roots:

```text
/.cache
/.tmp
/dist
/out
```

The standards validator rejects any tracked file under those configured generated roots.

## 3. Text and formatting contract

Repository text files use:

- UTF-8;
- LF line endings;
- one final newline;
- no trailing spaces/tabs;
- spaces rather than leading indentation tabs in Lua and Python;
- four-space indentation for Lua/Python;
- two-space indentation for JSON/YAML.

`.editorconfig` expresses the editor-facing defaults. The validator mechanically enforces the portable subset that does not require an external formatting package.

No auto-formatter is added in BB-002 solely for cosmetic rewriting. That would add another dependency/version surface without solving a current production problem. If a formatter is adopted later, it must be pinned and entered through the same dependency/tooling review process.

## 4. Lua lint convention

Defold's editor uses Luacheck for Lua linting and recognizes a project-root `.luacheckrc`.

BeBee keeps the documented Defold-compatible baseline explicit:

```text
unused_args = false
max_line_length = false
ignore = 611, 612, 614
```

Whitespace remains owned by the repository standards gate, so Luacheck does not need to duplicate those findings.

A separate command-line Luacheck binary is not made a mandatory fresh-clone dependency in BB-002. Defold editor lint remains useful, while CI uses the dependency-free repository gate. If standalone Luacheck becomes required later, its exact install/version must be pinned before CI depends on it.

## 5. Stable source layout

Production Defold/runtime resources belong under one of these canonical roots:

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

`prototypes/` is the only configured non-production runtime-resource root.

Directories are created when the scoped task first needs them; empty placeholder directories are not committed merely to make the tree look complete.

The validator recognizes Defold/runtime resource extensions and fails if such a resource appears outside the configured roots. Documentation, tooling, evidence, tests and repository metadata remain outside this runtime-source rule.

The dependency direction in `docs/05-technical-architecture.md` remains authoritative. Source layout does not grant permission for UI/platform code to bypass domain boundaries.

## 6. Dependency and license intake

`config/dependencies.json` is the machine-readable inventory. `THIRD_PARTY.md` is the human-readable license ledger.

Before incorporating third-party code, engine/tool versions, libraries, assets, fonts, audio or native extensions:

1. establish the exact need;
2. identify an authoritative HTTPS source;
3. pin the exact version/tag/commit where applicable;
4. read the authoritative license terms;
5. determine commercial-use and redistribution compatibility;
6. record attribution/notice obligations;
7. update `config/dependencies.json`;
8. update `THIRD_PARTY.md`;
9. run the standards gate before merge.

Unclear licensing means the material is not approved for production.

### Defold libraries

Any URL declared through `game.project` `dependencies` / `dependencies#N` must have an exact matching dependency record with:

```text
kind = defold-library
source = exact project dependency URL
```

The standards gate compares both directions and rejects:

- a `game.project` library URL with no reviewed manifest entry;
- a stale `defold-library` manifest entry no longer declared by the project.

Moving branches or `latest` archives are not accepted as a versioning strategy for production dependencies.

## 7. Current reviewed third-party baseline

The initial dependency manifest records the already-selected Defold 1.13.1 engine/runtime and Bob build tool. It does not claim that BeBee currently incorporates external gameplay libraries, fonts, art or audio.

The dependency validator checks presence and consistency of review fields; it is not a substitute for legal interpretation. License review remains a substantive step when a new dependency is proposed.

## 8. Standard commands

Run repository standards from the repository root:

```text
python3 scripts/check_repository_standards.py
```

Build the current pinned Defold HTML5 development bundle:

```text
python3 tools/defold/bundle_html5.py --mode development
```

Build the current pinned Defold HTML5 release bundle:

```text
python3 tools/defold/bundle_html5.py --mode release
```

The build commands require the Java major pinned by `tools/defold/toolchain.json`; the helper downloads/verifies the matching Bob artifact unless an exact checksum-matching local Bob path is supplied.

## 9. CI behavior

`.github/workflows/repository-standards.yml` runs the repository standards gate on pull requests and on pushes to `main`.

The gate intentionally uses only the Python standard library plus Git. This keeps a fresh-clone policy check independent of package installation and prevents the lint policy itself from floating through an unpinned package resolver.

This workflow complements, rather than replaces, the trusted PR evidence gate and Defold runtime/build evidence.

## 10. BB-002 boundary

BB-002 does **not** implement:

- semantic keyboard/touch input or input focus — `BB-003`;
- collection-proxy focus/lifecycle proof — `BB-003`;
- unit/data test harness — `BB-004`;
- complete PR HTML5 artifact CI — `BB-005`;
- deterministic gameplay screenshot routing/capture — `BB-006`;
- storage adapter and browser persistence proof — `BB-007`.

Repository/tooling standards are therefore complete only as a foundation contract. They must not be cited as evidence that those later runtime capabilities already exist.
