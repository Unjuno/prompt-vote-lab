// Prompt Vote Lab starts as an intentionally minimal implementation target.
// Accepted experiment runs may replace this file.
(() => {
  'use strict';

  // From /task/issue-safety-analysis.json for Issue #191:
  // unsafe_instruction_count: 0, unsafe_instructions_detected: []
  const UNSAFE_INSTRUCTIONS = [];

  const ELEMENTS = {
    unsafeList: document.getElementById('unsafe-list'),
    unsafeDetails: document.getElementById('unsafe-details'),
    unsafeSummary: document.getElementById('unsafe-summary'),
    gateSummary: document.getElementById('gate-summary'),

    decisionSelected: document.getElementById('decision-selected'),
    decisionButtons: document.querySelectorAll('.decision-button[data-decision]'),
    decisionOptions: document.querySelectorAll('.decision-option[data-decision]')
  };

  const DECISION_STORAGE_KEY = 'pvl_participant_decision_v1';
  const DECISION_LABELS = {
    trust: 'Trust the run',
    inspect: 'Inspect more evidence',
    propose: 'Propose a better prompt'
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

  function safeLocalStorageGet(key) {
    try {
      return window.localStorage.getItem(key);
    } catch {
      return null;
    }
  }

  function safeLocalStorageSet(key, value) {
    try {
      window.localStorage.setItem(key, value);
    } catch {
      // Ignore storage failures; the UI will still work for the current page load.
    }
  }

  function applyDecisionUI(decision) {
    const safeDecision = decision && DECISION_LABELS[decision] ? decision : null;

    if (ELEMENTS.decisionSelected) {
      ELEMENTS.decisionSelected.textContent = safeDecision
        ? DECISION_LABELS[safeDecision]
        : 'Not selected';
    }

    for (const optionEl of ELEMENTS.decisionOptions) {
      const isSelected = optionEl.dataset.decision === safeDecision;
      optionEl.classList.toggle('is-selected', isSelected);

      const btn = optionEl.querySelector('.decision-button[data-decision]');
      if (btn) btn.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
    }
  }

  function initDecisionCard() {
    const hasDecisionUI = ELEMENTS.decisionOptions && ELEMENTS.decisionOptions.length > 0;
    if (!hasDecisionUI) return;

    // Restore previous choice (if any).
    const storedDecision = safeLocalStorageGet(DECISION_STORAGE_KEY);
    if (storedDecision && DECISION_LABELS[storedDecision]) {
      applyDecisionUI(storedDecision);
    } else {
      applyDecisionUI(null);
    }

    for (const btn of ELEMENTS.decisionButtons) {
      btn.addEventListener('click', () => {
        const decision = btn.dataset.decision;
        applyDecisionUI(decision);
        if (DECISION_LABELS[decision]) safeLocalStorageSet(DECISION_STORAGE_KEY, decision);
      });
    }
  }

  function init() {
    renderUnsafeList();
    renderUnsafeDetailsVisibility();
    renderSummaries();
    initDecisionCard();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
