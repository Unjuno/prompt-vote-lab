#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "index.html"
  "lab/index.html"
  "lab/style.css"
  "lab/app.js"
  "README.md"
  "docs/experiment-model.md"
  "docs/how-to-participate.md"
  "docs/no-change-baseline.md"
  "docs/support-policy.md"
  "docs/automation-map.md"
  "rules/static-ui-v1.0.md"
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

if grep -R -n -E "<script[^>]+src=['\"]https?://|fetch\(|XMLHttpRequest|WebSocket|EventSource|eval\(|new Function|document\.cookie|navigator\.sendBeacon" index.html lab/; then
  echo "ERROR: forbidden network/script pattern detected in public static pages."
  exit 1
fi

if ! grep -q "href=\"./lab/\"" index.html; then
  echo "ERROR: root landing page must link to ./lab/."
  exit 1
fi

if ! grep -q "20 virtual votes" index.html; then
  echo "ERROR: landing page must explain the 20-vote no-change baseline."
  exit 1
fi

if grep -R -n -i -E "support (buys|purchases|grants).*merge|paid merge system|buy.*merge rights" index.html README.md docs/ rules/; then
  echo "ERROR: public docs must not describe support as buying merge or adoption."
  exit 1
fi

echo "Static site structure check passed."
