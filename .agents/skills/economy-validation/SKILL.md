# Skill — Economy Validation

Use for Honey faucets/sinks, upgrades, seed costs, gates, replay income and balance changes.

## Sequence

1. Read `DECISIONS.md` and `docs/02-progression-economy.md`.
2. State the intended player decision, not only the formula.
3. Model every relevant first-region faucet and sink.
4. Simulate multiple purchase orders, including greedy and cosmetic-heavy paths.
5. Verify that campaign progression does not require unintended replay farming.
6. Calculate payback for multiplicative economy upgrades such as Yield.
7. Identify dominant/obviously bad choices.
8. Test minimum, typical and high-balance paths.
9. Check that aesthetic seed spending cannot soft-lock progression.
10. Record assumptions and produce tables/plots or deterministic script output.
11. Tune only after the model exposes a specific problem.

## Invariants

- Honey never goes negative.
- Progression is fundable primarily by new content.
- Seeds/customization do not create an unrecoverable grind.
- A stat is removed or redesigned if it is consistently mandatory or ignored.
- Replay income is optional, not the intended campaign funding source.
