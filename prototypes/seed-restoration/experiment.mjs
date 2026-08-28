import assert from 'node:assert/strict';
import {
  MODES,
  createMeadow,
  canPlant,
  pollinateNative,
  plantSeed,
  restorationComplete,
  summary,
} from './model.mjs';

function run(mode) {
  const state = createMeadow(mode);
  const observations = {
    mode,
    initial_player_plot_plantable: canPlant(state, 'p1'),
    initial_native_plot_plantable: canPlant(state, 'n1'),
    native_visual_can_diverge_before_completion: false,
    blocked_actions: 0,
  };

  if (!plantSeed(state, 'p1', 'lavender')) observations.blocked_actions += 1;
  pollinateNative(state, 'n1');

  if (canPlant(state, 'n1')) {
    plantSeed(state, 'n1', 'clover');
    observations.native_visual_can_diverge_before_completion = !restorationComplete(state)
      && state.native[0].nativeSpecies !== state.native[0].plantedSpecies;
  } else {
    observations.blocked_actions += 1;
  }

  pollinateNative(state, 'n2');
  pollinateNative(state, 'n3');
  assert.equal(restorationComplete(state), true, `${mode}: native objectives must restore meadow`);

  assert.equal(
    plantSeed(state, 'n1', 'lavender'),
    true,
    `${mode}: completed native plot must be replantable after restoration`,
  );
  assert.equal(
    state.native[0].campaignComplete,
    true,
    `${mode}: replanting must preserve campaign completion`,
  );

  return {
    ...summary(state),
    ...observations,
    campaign_preserved_after_replant: state.native[0].campaignComplete,
    native_identity_preserved_after_replant: state.native[0].nativeSpecies === 'daisy',
    pre_restore_role_model: mode === MODES.PLAYER_SHAPED
      ? 'native plots can carry campaign identity and a different planted identity simultaneously'
      : mode === MODES.HYBRID
        ? 'native plots carry campaign identity; dedicated player plots carry chosen identity'
        : 'only native campaign identity is actionable until restoration is complete',
  };
}

const results = Object.values(MODES).map(run);
const byMode = Object.fromEntries(results.map((item) => [item.mode, item]));

assert.equal(byMode[MODES.NATIVE_FIRST].ownership_actions_before_restore, 0);
assert.equal(byMode[MODES.NATIVE_FIRST].initial_player_plot_plantable, false);
assert.equal(byMode[MODES.PLAYER_SHAPED].ownership_actions_before_restore >= 2, true);
assert.equal(byMode[MODES.PLAYER_SHAPED].native_visual_can_diverge_before_completion, true);
assert.equal(byMode[MODES.HYBRID].ownership_actions_before_restore, 1);
assert.equal(byMode[MODES.HYBRID].initial_player_plot_plantable, true);
assert.equal(byMode[MODES.HYBRID].initial_native_plot_plantable, false);
assert.equal(byMode[MODES.HYBRID].native_visual_can_diverge_before_completion, false);
assert.equal(results.every((item) => item.campaign_preserved_after_replant), true);

const report = {
  ticket: 'BB-P004',
  run_date: '2026-08-28',
  protocol: 'deterministic-model-abc',
  results,
  structural_conclusion: {
    selected: 'hybrid',
    reason: 'Hybrid is the only tested model that provides an ownership action before restoration while preventing an incomplete native campaign plot from simultaneously presenting a conflicting chosen species.',
    human_comprehension_status: 'not directly playtested; requires later runtime/player validation',
  },
};

console.log(JSON.stringify(report, null, 2));
