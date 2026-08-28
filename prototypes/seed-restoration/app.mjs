import {
  MODES,
  SEEDS,
  createMeadow,
  restorationComplete,
  restorationProgress,
  canPlant,
  pollinateNative,
  plantSeed,
  summary,
} from './model.mjs';

const meadowEl = document.querySelector('#meadow');
const notice = document.createElement('div');
notice.className = 'notice';
document.body.appendChild(notice);

const labels = {
  [MODES.NATIVE_FIRST]: 'A · Native first',
  [MODES.PLAYER_SHAPED]: 'B · Player-shaped',
  [MODES.HYBRID]: 'C · Hybrid',
};

const explanations = {
  [MODES.NATIVE_FIRST]: 'Finish all authored native objectives first. Seed choice unlocks only after restoration.',
  [MODES.PLAYER_SHAPED]: 'Any plot may be replanted during restoration. Native campaign identity remains separate from what is currently displayed.',
  [MODES.HYBRID]: 'Authored native challenge plots stay visually stable during restoration; dedicated player plots accept seeds immediately.',
};

const emoji = { daisy: '🌼', clover: '☘️', lavender: '🪻' };
const query = new URLSearchParams(location.search);
let mode = query.get('mode');
if (!Object.values(MODES).includes(mode)) mode = MODES.NATIVE_FIRST;
let state;
let selectedSeed = 'daisy';
let safetyTested = false;

function flash(text) {
  notice.textContent = text;
  notice.classList.add('show');
  clearTimeout(flash.timer);
  flash.timer = setTimeout(() => notice.classList.remove('show'), 1200);
}

function reset() {
  state = createMeadow(mode);
  selectedSeed = 'daisy';
  safetyTested = false;
  render();
}

function setMode(next) {
  mode = next;
  const url = new URL(location.href);
  url.searchParams.set('mode', mode);
  history.replaceState({}, '', url);
  reset();
}

function plantOrExplain(plotId) {
  if (!canPlant(state, plotId)) {
    flash(mode === MODES.NATIVE_FIRST
      ? 'Seed choice unlocks after native restoration.'
      : 'This native challenge stays authored until restoration is complete.');
    return;
  }
  const plot = state.native.find((p) => p.id === plotId);
  const wasComplete = plot?.campaignComplete === true;
  if (plantSeed(state, plotId, selectedSeed)) {
    if (wasComplete && plot?.campaignComplete === true) safetyTested = true;
    flash(`Planted ${selectedSeed}.`);
    render();
  }
}

function nativeCard(plot) {
  const plantingAllowed = canPlant(state, plot.id);
  const current = plot.plantedSpecies ?? plot.nativeSpecies;
  const dualIdentity = state.mode === MODES.PLAYER_SHAPED && current !== plot.nativeSpecies;
  const buttonText = plot.campaignComplete ? 'Native objective complete' : 'Pollinate native objective';
  return `
    <article class="plot native ${plot.campaignComplete ? 'complete' : ''}" data-plot="${plot.id}">
      <span class="kind">Native campaign patch</span>
      <div class="flower">${emoji[current] ?? '🌱'}</div>
      <strong>${current}</strong>
      <small>${dualIdentity ? `Campaign identity: ${plot.nativeSpecies} · appearance: ${current}` : `Native identity: ${plot.nativeSpecies}`}</small>
      <button class="action native-action" data-native="${plot.id}" ${plot.campaignComplete ? 'disabled' : ''}>${buttonText}</button>
      <button class="action plant-action" data-plant="${plot.id}" ${plantingAllowed ? '' : 'disabled'}>Plant ${selectedSeed}</button>
    </article>`;
}

function playerCard(plot) {
  const plantingAllowed = canPlant(state, plot.id);
  const current = plot.plantedSpecies;
  return `
    <article class="plot player ${plantingAllowed ? '' : 'locked'}" data-plot="${plot.id}">
      <span class="kind">Player-shaped plot</span>
      <div class="flower">${current ? emoji[current] : '＋'}</div>
      <strong>${current ?? 'Empty plot'}</strong>
      <small>${plantingAllowed ? 'Aesthetic state; never required for native campaign completion.' : 'Locked until native restoration completes.'}</small>
      <button class="action plant-action" data-plant="${plot.id}" ${plantingAllowed ? '' : 'disabled'}>Plant ${selectedSeed}</button>
    </article>`;
}

function stageLabel() {
  const p = restorationProgress(state);
  if (p === 0) return 'DORMANT';
  if (p < 0.67) return 'WAKING';
  if (p < 1) return 'GROWING';
  return 'RESTORED';
}

function render() {
  meadowEl.innerHTML = [
    ...state.native.map(nativeCard),
    ...state.player.map(playerCard),
  ].join('');

  document.querySelector('#modeTitle').textContent = labels[mode];
  document.querySelector('#modeExplanation').textContent = explanations[mode];
  document.querySelector('#stage').textContent = stageLabel();
  const done = state.native.filter((p) => p.campaignComplete).length;
  document.querySelector('#progress').textContent = `${done} / ${state.native.length}`;
  document.querySelector('#ownershipBefore').textContent = `${state.ownershipActionsBeforeRestore} actions`;
  document.querySelector('#actions').textContent = `${state.actionCount}`;
  document.querySelector('#firstOwnership').textContent = state.firstOwnershipAction ?? '—';
  document.querySelector('#campaignSafety').textContent = safetyTested ? 'PASS · preserved' : 'Not tested';
  const s = summary(state);
  document.querySelector('#choiceNow').textContent = s.player_choice_available_during_restoration ? 'Yes' : 'No';
  document.querySelector('#seedHint').textContent = restorationComplete(state)
    ? 'Meadow restored. Replanting remains reversible and campaign completion stays separate.'
    : 'Choose a seed, then choose an available plot.';

  document.querySelectorAll('[data-mode]').forEach((button) => {
    button.setAttribute('aria-selected', String(button.dataset.mode === mode));
  });
  document.querySelectorAll('[data-seed]').forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.seed === selectedSeed));
  });

  document.querySelectorAll('[data-native]').forEach((button) => {
    button.addEventListener('click', () => {
      pollinateNative(state, button.dataset.native);
      flash('Native objective completed.');
      render();
    });
  });
  document.querySelectorAll('[data-plant]').forEach((button) => {
    button.addEventListener('click', () => plantOrExplain(button.dataset.plant));
  });
}

document.querySelectorAll('[data-mode]').forEach((button) => button.addEventListener('click', () => setMode(button.dataset.mode)));
document.querySelectorAll('[data-seed]').forEach((button) => button.addEventListener('click', () => {
  selectedSeed = button.dataset.seed;
  render();
}));
document.querySelector('#reset').addEventListener('click', reset);
document.querySelector('#copy').addEventListener('click', async () => {
  const result = JSON.stringify({ ...summary(state), campaign_safety_replant_tested: safetyTested }, null, 2);
  try {
    await navigator.clipboard.writeText(result);
    flash('Result JSON copied.');
  } catch {
    console.log(result);
    flash('Clipboard unavailable; result logged to console.');
  }
});

reset();
