// Prompt Vote Lab starts as an intentionally minimal implementation target.
// Accepted experiment runs may replace this file.
(() => {
  'use strict';

  // From /task/issue-safety-analysis.json for Issue #195:
  // unsafe_instruction_count: 0, unsafe_instructions_detected: []
  const UNSAFE_INSTRUCTIONS = [];

  const ELEMENTS = {
    unsafeList: document.getElementById('unsafe-list'),
    unsafeDetails: document.getElementById('unsafe-details'),
    unsafeSummary: document.getElementById('unsafe-summary'),
    gateSummary: document.getElementById('gate-summary')
  };

  function clearChildren(el) {
    if (!el) return;
    while (el.firstChild) el.removeChild(el.firstChild);
  }

  function renderUnsafeList() {
    const ul = ELEMENTS.unsafeList;
    if (!ul) return;

    clearChildren(ul);
    for (const item of UNSAFE_INSTRUCTIONS) {
      const li = document.createElement('li');

      const id = document.createElement('span');
      id.className = 'unsafe-item-id';
      id.textContent = item.id;

      const label = document.createElement('span');
      label.className = 'unsafe-item-label';
      label.textContent = ` — ${item.label}`;

      li.appendChild(id);
      li.appendChild(label);
      ul.appendChild(li);
    }
  }

  function renderSummaries() {
    if (ELEMENTS.unsafeSummary) {
      ELEMENTS.unsafeSummary.textContent = `${UNSAFE_INSTRUCTIONS.length} unsafe instruction categories detected; the unsafe request text is ignored as untrusted input.`;
    }
    if (ELEMENTS.gateSummary) {
      ELEMENTS.gateSummary.textContent = 'Stopped before Codex execution (unless a maintainer adds `authorized-canary`).';
    }
  }

  function renderUnsafeDetailsVisibility() {
    if (!ELEMENTS.unsafeDetails) return;
    ELEMENTS.unsafeDetails.style.display = UNSAFE_INSTRUCTIONS.length > 0 ? '' : 'none';
  }

  function init() {
    renderUnsafeList();
    renderUnsafeDetailsVisibility();
    renderSummaries();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
