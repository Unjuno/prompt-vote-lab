(() => {
  'use strict';

  const DEFAULT_DURATION_SECONDS = 5 * 60;

  const elDisplay = document.getElementById('sprint-timer-display');
  const elStart = document.getElementById('sprint-timer-start');
  const elPause = document.getElementById('sprint-timer-pause');
  const elReset = document.getElementById('sprint-timer-reset');

  // If the timer markup isn't present (e.g., during partial experiments), do nothing.
  if (!elDisplay || !elStart || !elPause || !elReset) return;

  let status = 'idle'; // 'idle' | 'running' | 'paused' | 'finished'
  let remainingMs = DEFAULT_DURATION_SECONDS * 1000;
  let endTimeMs = null; // timestamp when the timer reaches 0 (only meaningful while running)
  let tickerId = null;
  let lastRenderedSeconds = null;

  const formatTime = (totalSeconds) => {
    const s = Math.max(0, totalSeconds);
    const minutes = Math.floor(s / 60);
    const seconds = s % 60;
    return `${minutes}:${String(seconds).padStart(2, '0')}`;
  };

  const syncButtons = () => {
    elStart.disabled = status === 'running';
    elPause.disabled = status !== 'running';
  };

  const render = () => {
    const remainingSeconds = Math.max(0, Math.ceil(remainingMs / 1000));
    if (remainingSeconds === lastRenderedSeconds) return;

    lastRenderedSeconds = remainingSeconds;
    elDisplay.textContent = formatTime(remainingSeconds);
  };

  const stopTicker = () => {
    if (tickerId !== null) {
      clearInterval(tickerId);
      tickerId = null;
    }
  };

  const tick = () => {
    if (status !== 'running' || endTimeMs === null) return;

    remainingMs = endTimeMs - Date.now();
    if (remainingMs <= 0) {
      remainingMs = 0;
      status = 'finished';
      endTimeMs = null;
      stopTicker();
    }

    render();
    syncButtons();
  };

  const start = () => {
    if (status === 'running') return;

    // If the prior sprint finished, starting should begin a fresh sprint.
    if (remainingMs <= 0) {
      remainingMs = DEFAULT_DURATION_SECONDS * 1000;
    }

    status = 'running';
    endTimeMs = Date.now() + remainingMs;

    stopTicker();
    render();
    syncButtons();

    tickerId = setInterval(tick, 250);
    tick();
  };

  const pause = () => {
    if (status !== 'running' || endTimeMs === null) return;

    remainingMs = endTimeMs - Date.now();
    if (remainingMs < 0) remainingMs = 0;

    status = 'paused';
    endTimeMs = null;
    stopTicker();

    render();
    syncButtons();
  };

  const reset = () => {
    status = 'idle';
    remainingMs = DEFAULT_DURATION_SECONDS * 1000;
    endTimeMs = null;
    stopTicker();

    lastRenderedSeconds = null;
    render();
    syncButtons();
  };

  elStart.addEventListener('click', start);
  elPause.addEventListener('click', pause);
  elReset.addEventListener('click', reset);

  render();
  syncButtons();
})();
