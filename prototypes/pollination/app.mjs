import {
  MODES,
  clamp,
  distance,
  insidePatch,
  pollinationDelta,
  updatePatchProgress,
  createMetrics,
  recordFeedback,
  metricsSummary,
} from './model.mjs';

const canvas = document.querySelector('#game');
const ctx = canvas.getContext('2d');
const resetButton = document.querySelector('#resetButton');
const copyButton = document.querySelector('#copyButton');
const pollinateButton = document.querySelector('#pollinateButton');
const touchStick = document.querySelector('#touchStick');
const hint = document.querySelector('#hint');

const labels = {
  [MODES.AUTO]: 'A · Proximity',
  [MODES.HOLD]: 'B · Hold',
  [MODES.SWEEP]: 'C · Sweep',
};

const hints = {
  [MODES.AUTO]: 'Enter a flower patch and remain near it.',
  [MODES.HOLD]: 'Enter a patch, then hold Space / POLLINATE.',
  [MODES.SWEEP]: 'Keep flying through the flowers; stopping stops progress.',
};

const basePatches = [
  { id: 'daisy', x: 270, y: 185, radius: 76, color: '#fff7db' },
  { id: 'clover', x: 690, y: 245, radius: 88, color: '#d5f3be' },
  { id: 'lily', x: 505, y: 455, radius: 94, color: '#f1c7f3' },
];

const query = new URLSearchParams(location.search);
let mode = query.get('mode');
const qaState = query.get('qa');
if (!Object.values(MODES).includes(mode)) mode = MODES.AUTO;

let bee;
let patches;
let keys = new Set();
let pollinateHeld = false;
let lastTs = performance.now();
let metrics;
let completed = false;
let touchPointer = null;
let touchOrigin = null;
let touchVector = { x: 0, y: 0 };

function reset() {
  bee = { x: 110, y: 300, vx: 0, vy: 0, radius: 18 };
  patches = basePatches.map((patch) => ({ ...patch, progress: 0, complete: false }));
  metrics = createMetrics(mode, performance.now());
  completed = false;
  pollinateHeld = false;
  lastTs = performance.now();

  if (qaState === 'active') {
    bee.x = patches[0].x;
    bee.y = patches[0].y;
    patches[0].progress = 0.58;
    metrics.firstFeedbackAt = metrics.startedAt + 140;
    metrics.activeSeconds = 1.7;
  } else if (qaState === 'complete') {
    patches.forEach((patch) => { patch.progress = 1; patch.complete = true; });
    metrics.completedPatches = patches.length;
    metrics.firstFeedbackAt = metrics.startedAt + 140;
    metrics.activeSeconds = 7.4;
    metrics.completedAt = metrics.startedAt + 11800;
    completed = true;
  }

  updateUi();
}

function setMode(nextMode) {
  mode = nextMode;
  const url = new URL(location.href);
  url.searchParams.set('mode', mode);
  history.replaceState({}, '', url);
  reset();
}

function updateUi() {
  document.querySelector('#modeLabel').textContent = labels[mode];
  hint.textContent = hints[mode];
  document.querySelector('#completed').textContent = `${metrics.completedPatches} / ${patches.length}`;
  document.querySelector('#objective').textContent = completed ? 'Run complete — save the metrics' : 'Bloom all 3 patches';
  document.querySelector('#mFeedback').textContent = metrics.firstFeedbackAt === null ? '—' : `${Math.round(metrics.firstFeedbackAt - metrics.startedAt)} ms`;
  const now = metrics.completedAt ?? performance.now();
  document.querySelector('#mTime').textContent = `${Math.max(0, (now - metrics.startedAt) / 1000).toFixed(1)} s`;
  document.querySelector('#mWait').textContent = `${metrics.stationaryInsideSeconds.toFixed(1)} s`;
  document.querySelector('#mPresses').textContent = `${metrics.pollinatePresses}`;
  document.querySelector('#mDistance').textContent = `${Math.round(metrics.movementDistance)} px`;
  document.querySelectorAll('[data-mode]').forEach((button) => {
    button.setAttribute('aria-selected', String(button.dataset.mode === mode));
  });
  pollinateButton.classList.toggle('visible', mode === MODES.HOLD);
}

function movementInput() {
  let x = 0;
  let y = 0;
  if (keys.has('KeyA') || keys.has('ArrowLeft')) x -= 1;
  if (keys.has('KeyD') || keys.has('ArrowRight')) x += 1;
  if (keys.has('KeyW') || keys.has('ArrowUp')) y -= 1;
  if (keys.has('KeyS') || keys.has('ArrowDown')) y += 1;
  x += touchVector.x;
  y += touchVector.y;
  const length = Math.hypot(x, y);
  if (length > 1) { x /= length; y /= length; }
  return { x, y };
}

function update(ts) {
  const dt = Math.min(0.04, Math.max(0, (ts - lastTs) / 1000));
  lastTs = ts;

  if (!completed) {
    const input = movementInput();
    const acceleration = 1050;
    const maxSpeed = 235;
    const damping = Math.pow(0.0009, dt);
    bee.vx = (bee.vx + input.x * acceleration * dt) * damping;
    bee.vy = (bee.vy + input.y * acceleration * dt) * damping;
    const speed = Math.hypot(bee.vx, bee.vy);
    if (speed > maxSpeed) {
      bee.vx = bee.vx / speed * maxSpeed;
      bee.vy = bee.vy / speed * maxSpeed;
    }

    const before = { x: bee.x, y: bee.y };
    bee.x = clamp(bee.x + bee.vx * dt, bee.radius, canvas.width - bee.radius);
    bee.y = clamp(bee.y + bee.vy * dt, bee.radius, canvas.height - bee.radius);
    const moved = distance(before, bee);
    metrics.movementDistance += moved;

    let anyInside = false;
    for (const patch of patches) {
      if (patch.complete) continue;
      const inside = insidePatch(bee, patch);
      anyInside ||= inside;
      const delta = pollinationDelta({
        mode,
        dt,
        inside,
        pollinateHeld,
        distanceMoved: moved,
      });
      if (delta > 0) {
        recordFeedback(metrics, ts);
        metrics.activeSeconds += dt;
        const prior = patch.progress;
        patch.progress = updatePatchProgress(patch.progress, delta);
        if (prior < 1 && patch.progress >= 1) {
          patch.complete = true;
          metrics.completedPatches += 1;
        }
      }
    }

    if (anyInside && moved < 0.35) metrics.stationaryInsideSeconds += dt;

    if (metrics.completedPatches === patches.length) {
      metrics.completedAt = ts;
      completed = true;
    }
  }

  draw();
  updateUi();
  requestAnimationFrame(update);
}

function drawFlower(x, y, scale, color, open) {
  ctx.save();
  ctx.translate(x, y);
  for (let i = 0; i < 6; i += 1) {
    ctx.rotate(Math.PI / 3);
    ctx.beginPath();
    ctx.ellipse(0, -7 * scale, 4.5 * scale, (open ? 9 : 5) * scale, 0, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
  }
  ctx.beginPath();
  ctx.arc(0, 0, 4.2 * scale, 0, Math.PI * 2);
  ctx.fillStyle = '#e8b82c';
  ctx.fill();
  ctx.restore();
}

function drawPatch(patch) {
  const glow = patch.complete ? 0.28 : 0.10 + patch.progress * 0.14;
  ctx.beginPath();
  ctx.arc(patch.x, patch.y, patch.radius, 0, Math.PI * 2);
  ctx.fillStyle = `rgba(255,255,255,${glow})`;
  ctx.fill();
  ctx.lineWidth = 3;
  ctx.strokeStyle = patch.complete ? '#fff7a8' : 'rgba(39,70,27,.42)';
  ctx.stroke();

  for (let i = 0; i < 11; i += 1) {
    const angle = i * 2.399;
    const ring = 22 + (i % 4) * 12;
    drawFlower(
      patch.x + Math.cos(angle) * ring,
      patch.y + Math.sin(angle) * ring,
      0.76 + (i % 3) * 0.08,
      patch.color,
      patch.complete || patch.progress > i / 12,
    );
  }

  if (!patch.complete) {
    ctx.fillStyle = 'rgba(13,21,9,.74)';
    ctx.fillRect(patch.x - 48, patch.y + patch.radius + 12, 96, 9);
    ctx.fillStyle = '#f7d34b';
    ctx.fillRect(patch.x - 48, patch.y + patch.radius + 12, 96 * patch.progress, 9);
  }
}

function drawBee() {
  ctx.save();
  ctx.translate(bee.x, bee.y);
  const heading = Math.atan2(bee.vy, bee.vx || 0.01);
  ctx.rotate(heading);
  ctx.globalAlpha = .72;
  ctx.fillStyle = '#e8f4f0';
  ctx.beginPath(); ctx.ellipse(-3, -15, 13, 8, -.35, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(-3, 15, 13, 8, .35, 0, Math.PI * 2); ctx.fill();
  ctx.globalAlpha = 1;
  ctx.fillStyle = '#f7cf3f';
  ctx.beginPath(); ctx.ellipse(0, 0, 22, 15, 0, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#2a2615';
  ctx.fillRect(-8, -14, 6, 28);
  ctx.fillRect(5, -12, 5, 24);
  ctx.beginPath(); ctx.arc(17, 0, 8, 0, Math.PI * 2); ctx.fill();
  ctx.restore();
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, '#b8d97b');
  gradient.addColorStop(1, '#82b55d');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = 'rgba(38,76,31,.18)';
  for (let i = 0; i < 38; i += 1) {
    const x = (i * 157) % canvas.width;
    const y = (i * 83) % canvas.height;
    ctx.beginPath(); ctx.arc(x, y, 2 + (i % 4), 0, Math.PI * 2); ctx.fill();
  }

  patches.forEach(drawPatch);
  drawBee();
}

function pointerToCanvas(event) {
  const rect = canvas.getBoundingClientRect();
  return {
    x: (event.clientX - rect.left) / rect.width * canvas.width,
    y: (event.clientY - rect.top) / rect.height * canvas.height,
  };
}

canvas.addEventListener('pointerdown', (event) => {
  if (event.pointerType === 'mouse') return;
  touchPointer = event.pointerId;
  touchOrigin = pointerToCanvas(event);
  canvas.setPointerCapture(event.pointerId);
});

canvas.addEventListener('pointermove', (event) => {
  if (event.pointerId !== touchPointer || !touchOrigin) return;
  const point = pointerToCanvas(event);
  const dx = point.x - touchOrigin.x;
  const dy = point.y - touchOrigin.y;
  const length = Math.hypot(dx, dy) || 1;
  const capped = Math.min(70, length);
  touchVector = { x: dx / length * (capped / 70), y: dy / length * (capped / 70) };
  const knob = touchStick.querySelector('span');
  knob.style.transform = `translate(${touchVector.x * 28}px, ${touchVector.y * 28}px)`;
});

function releaseTouch(event) {
  if (event.pointerId !== touchPointer) return;
  touchPointer = null;
  touchOrigin = null;
  touchVector = { x: 0, y: 0 };
  touchStick.querySelector('span').style.transform = '';
}
canvas.addEventListener('pointerup', releaseTouch);
canvas.addEventListener('pointercancel', releaseTouch);

function pressPollinate() {
  if (!pollinateHeld) metrics.pollinatePresses += 1;
  pollinateHeld = true;
}
function releasePollinate() { pollinateHeld = false; }

pollinateButton.addEventListener('pointerdown', (event) => {
  event.preventDefault();
  pollinateButton.setPointerCapture(event.pointerId);
  pressPollinate();
});
pollinateButton.addEventListener('pointerup', releasePollinate);
pollinateButton.addEventListener('pointercancel', releasePollinate);

window.addEventListener('keydown', (event) => {
  keys.add(event.code);
  if (event.code === 'Space') {
    event.preventDefault();
    pressPollinate();
  }
});
window.addEventListener('keyup', (event) => {
  keys.delete(event.code);
  if (event.code === 'Space') releasePollinate();
});
window.addEventListener('blur', () => {
  keys.clear();
  releasePollinate();
});

document.querySelectorAll('[data-mode]').forEach((button) => {
  button.addEventListener('click', () => setMode(button.dataset.mode));
});
resetButton.addEventListener('click', reset);
copyButton.addEventListener('click', async () => {
  const result = JSON.stringify(metricsSummary(metrics), null, 2);
  try {
    await navigator.clipboard.writeText(result);
    copyButton.textContent = 'Copied';
    setTimeout(() => { copyButton.textContent = 'Copy result JSON'; }, 900);
  } catch {
    console.log(result);
    copyButton.textContent = 'Logged to console';
  }
});

reset();
requestAnimationFrame(update);
