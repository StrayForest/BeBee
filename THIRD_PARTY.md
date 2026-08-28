# Third-Party Software & Assets

This file is the human-readable license ledger for external code, engines, extensions, fonts, art, audio and other assets used by BeBee. The machine-readable companion is `config/dependencies.json`.

## Rule

Nothing third-party is considered approved for production merely because it is public on GitHub or free to download.

Before adding or changing a dependency/asset:

1. identify the exact source URL;
2. identify the exact version/commit/file set;
3. verify the license text and commercial-use terms from an authoritative source;
4. record redistribution and attribution requirements;
5. add/update the machine-readable entry in `config/dependencies.json`;
6. add/update the matching human-readable entry in this file;
7. pin Defold library URLs in `game.project` rather than using moving branches/latest archives;
8. run `python3 scripts/check_repository_standards.py`;
9. keep required license/copyright notices with the shipped distribution.

If license status is unclear, commercial use is not allowed, redistribution requirements cannot be met, or the version cannot be pinned, do not import it.

## Incorporated / required third-party technology

### Defold Engine

- Source: https://github.com/defold/defold/releases/tag/1.13.1
- Version: `1.13.1`
- Role: game engine/runtime included in produced application bundles
- License: Defold License 1.0 — https://defold.com/license/
- Commercial use: allowed under the license
- Redistribution: allowed subject to the license and bundled third-party runtime notices
- Compliance note: release packaging must follow Defold's engine third-party license requirements for the pinned version.

### Defold Bob

- Source: https://github.com/defold/defold/releases/tag/1.13.1
- Version: `1.13.1`
- Role: build-time command-line tool; downloaded and SHA-256 verified by `tools/defold/bundle_html5.py`
- License: Defold License 1.0 — https://defold.com/license/
- Commercial use: allowed under the license
- Redistribution: allowed; BeBee does not currently redistribute `bob.jar`
- Compliance note: review Defold tool licenses whenever the pinned engine/tool version changes.

## Defold library dependency rule

Any future `game.project` dependency must have a matching `kind: "defold-library"` entry in `config/dependencies.json`, including its exact library URL, pinned version/commit/tag, license source, commercial-use decision, redistribution decision, attribution and review date. The repository standards validator rejects an unregistered Defold library URL or a stale registered library no longer present in `game.project`.

## Assets and other incorporated material

No external fonts, art, audio, native extensions or third-party gameplay libraries are incorporated yet.

The documentation references external games/repositories for research only. Those references are not incorporated code/assets.

## Research-only references (not dependencies)

| Project | Purpose | Incorporated? |
|---|---|---|
| Cow Bay / 7Spot Games | gameplay/UX research | No |
| Cow Castle / 7Spot Games | gameplay/UX research | No |
| Olly the Paw / 7Spot Games | progression research | No |
| Elixpur Idle / 7Spot Games | automation research | No |
| My Little Universe | progression/world-restoration research | No |
| Dreamdale | progression/UX research | No |
| Forager | system-loop research | No |
| PurrNet Incremental Sample | architecture/mechanic research | No |
| benjames-171/defold-games | Defold implementation research | No |
| Godot Valley | farming/foraging research | No |

## Approved dependency template

Every incorporated item belongs in `config/dependencies.json` and should also be summarized here with:

```text
Name:
Kind:
Source:
Version / commit:
Files used / runtime role:
License:
License source:
Commercial use allowed: Yes/No
Modification allowed: Yes/No/N/A
Redistribution conditions:
Attribution required:
License file/notices included at:
Reason for inclusion:
Reviewed by/date:
```

## License review reminder

Open-source code license and art/audio asset license may differ even when they appear in the same repository. Review each relevant asset source separately. A validator can enforce that review fields exist; it cannot decide whether a license interpretation is legally correct.
