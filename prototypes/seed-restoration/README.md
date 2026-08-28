# BB-P004 — Seed / restoration flow lab

Disposable browser prototype used to compare the three seed/restoration models from `docs/11-blueprint-hardening.md`. It is intentionally not production Defold code and does not validate a winner by itself.

## Variants

- **A / Native first** — all native campaign objectives complete before any seed choice becomes available.
- **B / Player-shaped** — seed choice is available on every plot during restoration; native campaign identity and planted appearance are separate states.
- **C / Hybrid** — authored native campaign plots remain stable during restoration, while dedicated player-shaped plots accept seeds immediately. Native plots become replantable after restoration.

All modes use the same three native campaign objectives and two player-shaped positions. Campaign completion is based only on native completion state in every mode.

## Run

```bash
python3 -m http.server 8080 --directory prototypes/seed-restoration
```

Then open:

- `http://localhost:8080/?mode=native-first`
- `http://localhost:8080/?mode=player-shaped`
- `http://localhost:8080/?mode=hybrid`

## Test protocol

For each mode:

1. attempt a seed choice immediately;
2. complete one native objective;
3. attempt/perform another seed choice;
4. finish all native objectives;
5. replant a completed native plot where the model permits it;
6. verify campaign completion is preserved;
7. copy the result JSON.

Record objective measurements:

- action count to native restoration;
- first ownership action index;
- ownership actions before restoration;
- whether choice exists before restoration;
- whether campaign completion survives replanting.

Then separately score:

- can a new player explain `native objective` vs `chosen appearance` after one run?;
- ownership timing, 1–5;
- cognitive load, 1–5 (lower is better);
- reversibility clarity, 1–5;
- whether the world feels authored enough to communicate biome/challenge identity;
- whether the world feels personal before the meadow is already finished.

Do not treat the number of clicks alone as the product winner. The intended decision balances comprehension, agency and progression safety.

## Tests

```bash
node prototypes/seed-restoration/model.test.mjs
```

The tests enforce the key domain invariant: `campaignComplete` / native identity and `plantedSpecies` are independent, so replanting cannot erase campaign progress.
