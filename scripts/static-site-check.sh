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
  "docs/automation-map.md"
  "rules/static-ui-v1.0.md"
  "rules/agent-run-policy-v1.0.md"
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
if grep -R -n -E "<script[^>]+src=['\"]https?://|fetch\(|XMLHttpRequest|WebSocket|EventSource|eval\(|new Function|document\.cookie|navigator\.sendBeacon" lab/; then
  echo "ERROR: forbidden network/script pattern detected in lab implementation files."
  exit 1
fi

if ! grep -q "href=\"./lab/\"" index.html; then
  echo "ERROR: root landing page must link to ./lab/."
  exit 1
fi

if ! grep -q -E "20-vote gate|20 virtual votes|virtual votes baseline" index.html; then
  echo "ERROR: landing page must explain the 20-vote no-change baseline."
  exit 1
fi

if ! grep -q "agent PR" index.html; then
  echo "ERROR: landing page should describe the public concept as an agent PR, not an API-first flow."
  exit 1
fi

# Hard-block removed support tiers and service-like positive framing.
# Negative boundary statements such as "There is no general support tier" are allowed.
if grep -R -n -i -E "\$20|20 USD|Support the Experiment|workflow maintenance" README.md index.html docs/ rules/; then
  echo "ERROR: obsolete or service-like support language detected."
  exit 1
fi

if grep -R -n -i -E "\b(general support tier|general support|support tier)\b.*\b(includes|provides|guarantees|covers|funds|buys|purchases|grants)\b" README.md index.html docs/ rules/; then
  echo "ERROR: general support must not be described as an active offered tier or service."
  exit 1
fi

# Detect affirmative service-like claims without failing on explicit negative boundary statements.
if grep -R -n -i -E "\bsupport (creates|includes|provides|guarantees)\b.*\b(maintenance|review|support work|delivery|service)\b|\bsupporters (get|receive|gain)\b.*\b(maintenance|review|support work|delivery|service)\b" README.md index.html docs/ rules/; then
  echo "ERROR: support must not be described as buying maintenance, review, service, or delivery."
  exit 1
fi

# Detect affirmative claims that support buys control. Do not fail on negative safety statements
# such as "not a paid merge system" or "does not guarantee merge".
if grep -R -n -i -E "\bsupport (buys|purchases|grants)\b.*\b(merge|adoption|specification control|control)\b|\bsupporters (get|receive|gain)\b.*\b(merge|adoption|specification control|control)\b|\b(buy|buys|purchase|purchases)\b.*\bmerge rights\b" index.html README.md docs/ rules/; then
  echo "ERROR: public docs must not describe support as buying merge, adoption, or control."
  exit 1
fi

echo "Static site structure check passed."
