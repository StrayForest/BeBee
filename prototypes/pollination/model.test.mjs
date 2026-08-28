import assert from 'node:assert/strict';
import {
  MODES,
  pollinationDelta,
  updatePatchProgress,
  metricsSummary,
  createMetrics,
} from './model.mjs';

assert.equal(pollinationDelta({ mode: MODES.AUTO, dt: 1, inside: true, pollinateHeld: false, distanceMoved: 0 }), 0.34);
assert.equal(pollinationDelta({ mode: MODES.AUTO, dt: 1, inside: false, pollinateHeld: false, distanceMoved: 0 }), 0);
assert.equal(pollinationDelta({ mode: MODES.HOLD, dt: 1, inside: true, pollinateHeld: false, distanceMoved: 0 }), 0);
assert.equal(pollinationDelta({ mode: MODES.HOLD, dt: 1, inside: true, pollinateHeld: true, distanceMoved: 0 }), 0.52);
assert.equal(pollinationDelta({ mode: MODES.SWEEP, dt: 1, inside: true, pollinateHeld: false, distanceMoved: 245 }), 1);
assert.equal(updatePatchProgress(0.9, 0.4), 1);

const metrics = createMetrics(MODES.AUTO, 1000);
metrics.firstFeedbackAt = 1125;
metrics.completedAt = 2500;
metrics.activeSeconds = 1.234;
metrics.movementDistance = 99.6;
metrics.completedPatches = 3;
assert.deepEqual(metricsSummary(metrics), {
  mode: 'auto',
  first_feedback_ms: 125,
  completion_ms: 1500,
  active_seconds: 1.23,
  stationary_inside_seconds: 0,
  movement_distance_px: 100,
  pollinate_presses: 0,
  completed_patches: 3,
});

console.log('BB-P003 pollination model tests passed');
