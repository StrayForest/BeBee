# Skill — Official Documentation Research

Use before implementing engine, browser, storage, input, rendering, audio, lifecycle, SDK, analytics or dependency behavior.

## Source order

1. Current official Defold manual/API/examples.
2. Current official portal/platform documentation.
3. Current official dependency/library documentation and source.
4. Reputable secondary technical material only when official sources are insufficient.

## Required output

- exact pages consulted;
- current date and version-sensitive details;
- APIs/constraints actually verified;
- chosen implementation approach;
- alternatives rejected and why;
- edge cases/lifecycle behavior to test;
- whether `DECISIONS.md` or architecture docs need updating.

## Rules

- Never invent API names from memory.
- Distinguish documentation facts from BeBee design choices.
- Re-check portal requirements before integration even if they were researched earlier.
- Use protected/error paths described by the API rather than assuming happy-path behavior.
