# BB-P003 — Pollination A/B/C interaction lab

Disposable browser prototype used to decide `D-006`. It is deliberately outside the production Defold architecture.

## Variants

- **A / Proximity** — progress while the bee remains inside a flower patch.
- **B / Hold** — progress only while inside the patch and the explicit pollinate action is held.
- **C / Sweep** — progress is proportional to distance travelled inside the patch; standing still produces no progress.

All variants share the same bee movement, patch positions and completion target.

## Run

Serve this directory over HTTP, for example:

```bash
python3 -m http.server 8080 --directory prototypes/pollination
```

Then open `http://localhost:8080/?mode=auto`, `?mode=hold`, or `?mode=sweep`.

Desktop: WASD/arrow keys. Variant B uses Space for pollination.
Touch: drag on the field to move. Variant B exposes a POLLINATE button.

## Deterministic observations to record

For each mode complete the same three-patch route and save:

- first feedback latency;
- completion time;
- stationary time while inside a patch;
- explicit pollinate presses;
- movement distance;
- subjective agency (1–5);
- repetition comfort after repeated runs (1–5);
- mobile comfort (1–5);
- accidental/progress-without-intent notes.

Do not tune movement or patch geometry between modes during the first comparison pass.

## Deterministic QA states

Add `qa=active` or `qa=complete` to a mode URL to render stable evidence states without affecting the normal experiment path.

Examples:

- `?mode=auto&qa=active`
- `?mode=hold&qa=complete`

## Tests

```bash
node prototypes/pollination/model.test.mjs
```

The test file verifies that the three interaction rules stay mechanically distinct and that metrics remain deterministic.
