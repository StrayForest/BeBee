import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';

const output = execFileSync(
  process.execPath,
  ['prototypes/seed-restoration/experiment.mjs'],
  { encoding: 'utf8' },
);
const report = JSON.parse(output);
const byMode = Object.fromEntries(report.results.map((item) => [item.mode, item]));

assert.equal(report.structural_conclusion.selected, 'hybrid');
assert.equal(byMode['native-first'].ownership_actions_before_restore, 0);
assert.equal(byMode['player-shaped'].native_visual_can_diverge_before_completion, true);
assert.equal(byMode.hybrid.ownership_actions_before_restore, 1);
assert.equal(byMode.hybrid.native_visual_can_diverge_before_completion, false);
assert.equal(report.results.every((item) => item.campaign_preserved_after_replant), true);

console.log('BB-P004 seed/restoration experiment tests passed');
