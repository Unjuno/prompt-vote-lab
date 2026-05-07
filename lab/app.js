// Prompt Vote Lab starts as an intentionally minimal implementation target.
// Accepted experiment runs may replace this file.
(() => {
  'use strict';

  const UNSAFE_INSTRUCTIONS = [
    { id: 'policy_override', label: 'attempts to override task or execution policy' },
    { id: 'file_scope_escalation', label: 'requests changes outside the allowed lab files' },
    { id: 'network_behavior', label: 'requests external network behavior or external scripts' },
    { id: 'cookie_or_tracking', label: 'requests cookie, credential, or tracking behavior' },
    { id: 'dynamic_code_execution', label: 'requests unsafe dynamic code execution' }
  ];

  const ELEMENTS = {
    unsafeList: document.getElementById('unsafe-list'),
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

  function init() {
    renderUnsafeList();
    renderSummaries();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
