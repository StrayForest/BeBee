export const MODES = Object.freeze({
  NATIVE_FIRST: 'native-first',
  PLAYER_SHAPED: 'player-shaped',
  HYBRID: 'hybrid',
});

export const SEEDS = Object.freeze(['daisy', 'clover', 'lavender']);

export function createMeadow(mode) {
  if (!Object.values(MODES).includes(mode)) throw new Error(`Unknown mode: ${mode}`);
  const native = [
    { id: 'n1', kind: 'native', nativeSpecies: 'daisy', campaignComplete: false, plantedSpecies: 'daisy' },
    { id: 'n2', kind: 'native', nativeSpecies: 'clover', campaignComplete: false, plantedSpecies: 'clover' },
    { id: 'n3', kind: 'native', nativeSpecies: 'lavender', campaignComplete: false, plantedSpecies: 'lavender' },
  ];
  const player = [
    { id: 'p1', kind: 'player', campaignComplete: null, plantedSpecies: null },
    { id: 'p2', kind: 'player', campaignComplete: null, plantedSpecies: null },
  ];
  return {
    mode,
    native,
    player,
    actionCount: 0,
    ownershipActions: 0,
    ownershipActionsBeforeRestore: 0,
    firstOwnershipAction: null,
  };
}

export function restorationComplete(state) {
  return state.native.every((plot) => plot.campaignComplete === true);
}

export function restorationProgress(state) {
  const done = state.native.filter((plot) => plot.campaignComplete).length;
  return done / state.native.length;
}

export function canPlant(state, plotId) {
  const restored = restorationComplete(state);
  const nativePlot = state.native.find((plot) => plot.id === plotId);
  const playerPlot = state.player.find((plot) => plot.id === plotId);
  if (!nativePlot && !playerPlot) return false;

  if (state.mode === MODES.NATIVE_FIRST) return restored;
  if (state.mode === MODES.PLAYER_SHAPED) return true;
  if (state.mode === MODES.HYBRID) return Boolean(playerPlot) || restored;
  return false;
}

export function pollinateNative(state, plotId) {
  const plot = state.native.find((item) => item.id === plotId);
  if (!plot || plot.campaignComplete) return false;
  plot.campaignComplete = true;
  state.actionCount += 1;
  return true;
}

export function plantSeed(state, plotId, seed) {
  if (!SEEDS.includes(seed) || !canPlant(state, plotId)) return false;
  const plot = [...state.native, ...state.player].find((item) => item.id === plotId);
  if (!plot) return false;
  const beforeRestore = !restorationComplete(state);
  plot.plantedSpecies = seed;
  state.actionCount += 1;
  state.ownershipActions += 1;
  if (beforeRestore) state.ownershipActionsBeforeRestore += 1;
  if (state.firstOwnershipAction === null) state.firstOwnershipAction = state.actionCount;
  return true;
}

export function summary(state) {
  return {
    mode: state.mode,
    restoration_progress: Number(restorationProgress(state).toFixed(2)),
    restored: restorationComplete(state),
    action_count: state.actionCount,
    ownership_actions: state.ownershipActions,
    ownership_actions_before_restore: state.ownershipActionsBeforeRestore,
    first_ownership_action: state.firstOwnershipAction,
    native_rules_visible_during_restoration: state.native.some((plot) => !plot.campaignComplete),
    player_choice_available_during_restoration: !restorationComplete(state) && (
      state.player.some((plot) => canPlant(state, plot.id)) ||
      state.native.some((plot) => canPlant(state, plot.id))
    ),
    native_campaign_state: Object.fromEntries(state.native.map((plot) => [plot.id, plot.campaignComplete])),
    planted_species: Object.fromEntries([...state.native, ...state.player].map((plot) => [plot.id, plot.plantedSpecies])),
  };
}
