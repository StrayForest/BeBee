import assert from 'node:assert/strict';
import {
  MODES,
  createMeadow,
  restorationComplete,
  canPlant,
  pollinateNative,
  plantSeed,
  summary,
} from './model.mjs';

{
  const state = createMeadow(MODES.NATIVE_FIRST);
  assert.equal(canPlant(state, 'p1'), false);
  state.native.forEach((plot) => assert.equal(pollinateNative(state, plot.id), true));
  assert.equal(restorationComplete(state), true);
  assert.equal(canPlant(state, 'p1'), true);
  assert.equal(plantSeed(state, 'p1', 'lavender'), true);
  assert.equal(summary(state).ownership_actions_before_restore, 0);
}

{
  const state = createMeadow(MODES.PLAYER_SHAPED);
  assert.equal(canPlant(state, 'n1'), true);
  assert.equal(plantSeed(state, 'n1', 'lavender'), true);
  assert.equal(pollinateNative(state, 'n1'), true);
  assert.equal(plantSeed(state, 'n1', 'clover'), true);
  assert.equal(state.native[0].campaignComplete, true, 'replanting must not erase campaign completion');
  assert.equal(state.native[0].nativeSpecies, 'daisy', 'native identity remains stable');
  assert.equal(state.native[0].plantedSpecies, 'clover', 'visual planted species is separate state');
}

{
  const state = createMeadow(MODES.HYBRID);
  assert.equal(canPlant(state, 'n1'), false);
  assert.equal(canPlant(state, 'p1'), true);
  assert.equal(plantSeed(state, 'p1', 'clover'), true);
  assert.equal(summary(state).ownership_actions_before_restore, 1);
  state.native.forEach((plot) => pollinateNative(state, plot.id));
  assert.equal(restorationComplete(state), true);
  assert.equal(canPlant(state, 'n1'), true, 'native plots become replantable after campaign restoration');
  assert.equal(state.native.every((plot) => plot.campaignComplete), true);
}

for (const mode of Object.values(MODES)) {
  const state = createMeadow(mode);
  state.native.forEach((plot) => pollinateNative(state, plot.id));
  assert.equal(restorationComplete(state), true, `${mode} must restore from native campaign state only`);
}

console.log('BB-P004 seed/restoration model tests passed');
