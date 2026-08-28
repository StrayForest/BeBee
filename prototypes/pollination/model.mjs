export const MODES = Object.freeze({
  AUTO: 'auto',
  HOLD: 'hold',
  SWEEP: 'sweep',
});

export function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

export function distance(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

export function insidePatch(bee, patch) {
  return distance(bee, patch) <= patch.radius;
}

export function pollinationDelta({
  mode,
  dt,
  inside,
  pollinateHeld,
  distanceMoved,
  autoRate = 0.34,
  holdRate = 0.52,
  sweepDistance = 245,
}) {
  if (!inside || dt <= 0) return 0;

  if (mode === MODES.AUTO) {
    return autoRate * dt;
  }

  if (mode === MODES.HOLD) {
    return pollinateHeld ? holdRate * dt : 0;
  }

  if (mode === MODES.SWEEP) {
    return Math.max(0, distanceMoved) / sweepDistance;
  }

  throw new Error(`Unknown pollination mode: ${mode}`);
}

export function updatePatchProgress(progress, delta) {
  return clamp(progress + delta, 0, 1);
}

export function createMetrics(mode, now = 0) {
  return {
    mode,
    startedAt: now,
    firstFeedbackAt: null,
    completedAt: null,
    activeSeconds: 0,
    stationaryInsideSeconds: 0,
    movementDistance: 0,
    pollinatePresses: 0,
    completedPatches: 0,
  };
}

export function recordFeedback(metrics, now) {
  if (metrics.firstFeedbackAt === null) metrics.firstFeedbackAt = now;
}

export function metricsSummary(metrics) {
  const firstFeedbackMs = metrics.firstFeedbackAt === null
    ? null
    : Math.max(0, Math.round(metrics.firstFeedbackAt - metrics.startedAt));
  const completionMs = metrics.completedAt === null
    ? null
    : Math.max(0, Math.round(metrics.completedAt - metrics.startedAt));

  return {
    mode: metrics.mode,
    first_feedback_ms: firstFeedbackMs,
    completion_ms: completionMs,
    active_seconds: Number(metrics.activeSeconds.toFixed(2)),
    stationary_inside_seconds: Number(metrics.stationaryInsideSeconds.toFixed(2)),
    movement_distance_px: Math.round(metrics.movementDistance),
    pollinate_presses: metrics.pollinatePresses,
    completed_patches: metrics.completedPatches,
  };
}
