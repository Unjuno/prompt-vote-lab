#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "index.html"
  "lab/index.html"
  "lab/style.css"
  "lab/app.js"
  "README.md"
  "docs/README.md"
  "docs/experiment-model.md"
  "docs/how-to-participate.md"
  "docs/no-change-baseline.md"
  "docs/support-policy.md"
  "docs/report-policy.md"
  "docs/pre-api-freeze.md"
  "docs/current-features.md"
  "docs/canary-policy.md"
  "docs/canary-report-template.md"
  "docs/stop-rules.md"
  "docs/automation-map.md"
  "rules/static-ui-v1.0.md"
  "rules/agent-run-policy-v1.0.md"
  "rules/report-generation-v1.0.md"
  "rules/support-unlocked-runs-v1.1.md"
  "rules/initial-lab-state-v1.0.md"
  "rules/no-change-baseline-v1.0.md"
  "rules/public-site-v1.0.md"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "ERROR: required file missing: $file"
    exit 1
  fi
done

# Root landing page may describe forbidden behavior in prose, but must not load external scripts.
if grep -n -E "<script[^>]+src=['\"]https?://" index.html; then
  echo "ERROR: root landing page must not load external scripts."
  exit 1
fi

# The changing lab is the implementation target and must be strict.
if grep -R -n -E "<script[^>]+src=['\"]https?://|fetch\(|XMLHttpRequest|WebSocket|EventSource|eval\(|document\.cookie|navigator\.sendBeacon" lab/; then
  echo "ERROR: forbidden network/script pattern detected in lab implementation files."
  exit 1
fi

# Controlled new Function is allowed, but obvious dynamic-source patterns are blocked.
if grep -R -n -E "new Function\s*\([^)]*(user|input|textarea|location|hash|search|params|localStorage|sessionStorage|indexedDB|imported|json|body|prompt|innerText|textContent|value)" lab/; then
  echo "ERROR: new Function appears to use dynamic or user-controlled input."
  exit 1
fi

if ! grep -q "href=\"./lab/\"" index.html; then
  echo "ERROR: root landing page must link to ./lab/."
  exit 1
fi

if ! grep -qi -E "20-vote gate|20 virtual votes|virtual votes baseline|votes against doing nothing" index.html; then
  echo "ERROR: landing page must explain the 20-vote no-change baseline."
  exit 1
fi

if ! grep -qi -E "agent PR|Agent PR" index.html; then
  echo "ERROR: landing page should describe the public concept as an agent PR, not an API-first flow."
  exit 1
fi

if ! grep -qi -E "prompt game|Competitive prompt game|game loop|Risk trust|reputation|trust" index.html; then
  echo "ERROR: landing page must frame the project as a prompt game, not only as an experiment."
  exit 1
fi

if ! grep -qi -E "report policy|weekly report draft|model-free" docs/README.md; then
  echo "ERROR: docs index must expose the model-free report draft policy."
  exit 1
fi

if ! grep -qi -E "Pre-API freeze|pre-API freeze|paid implementation-agent canary" docs/README.md; then
  echo "ERROR: docs index must expose the pre-API freeze checklist."
  exit 1
fi

echo "Static site structure check passed."
