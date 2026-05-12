#!/usr/bin/env bash
set -euo pipefail

bundle_dir=""
report_path=""
findings_path=""

usage() {
  cat <<'USAGE'
Usage: scripts/run_gitleaks_public_bundle_scan.sh --bundle-dir DIR --report REPORT_JSON [--findings FINDINGS_JSON]

Scans a generated public agent run bundle directory with Gitleaks. This is deliberately
scoped to the public bundle directory, not the whole repository, to avoid false positives
from intentional test fixtures.
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --bundle-dir)
      bundle_dir="${2:-}"
      shift 2
      ;;
    --report)
      report_path="${2:-}"
      shift 2
      ;;
    --findings)
      findings_path="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ -z "$bundle_dir" ] || [ -z "$report_path" ]; then
  usage >&2
  exit 2
fi

if [ ! -d "$bundle_dir" ]; then
  echo "Bundle directory not found: $bundle_dir" >&2
  exit 2
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required for the public bundle Gitleaks scan" >&2
  exit 2
fi

GITLEAKS_IMAGE="${GITLEAKS_IMAGE:-ghcr.io/gitleaks/gitleaks:v8.30.1}"

report_dir="$(dirname "$report_path")"
mkdir -p "$report_dir"

if [ -z "$findings_path" ]; then
  findings_path="${report_path%.json}.findings.json"
fi
findings_dir="$(dirname "$findings_path")"
mkdir -p "$findings_dir"

bundle_abs="$(cd "$bundle_dir" && pwd -P)"
report_dir_abs="$(cd "$report_dir" && pwd -P)"
findings_dir_abs="$(cd "$findings_dir" && pwd -P)"
findings_base="$(basename "$findings_path")"

# Gitleaks returns exit code 1 by default when leaks are found. We set a distinct
# exit code so this wrapper can distinguish findings from runtime errors.
set +e
docker run --rm \
  -v "$bundle_abs:/scan:ro" \
  -v "$findings_dir_abs:/findings:rw" \
  "$GITLEAKS_IMAGE" detect \
    --no-git \
    --redact \
    --source=/scan \
    --report-format=json \
    --report-path="/findings/$findings_base" \
    --exit-code=2
scan_rc=$?
set -e

if [ ! -f "$findings_path" ]; then
  printf '[]\n' > "$findings_path"
fi

python - "$report_path" "$findings_path" "$bundle_abs" "$GITLEAKS_IMAGE" "$scan_rc" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
findings_path = Path(sys.argv[2])
bundle_dir = sys.argv[3]
image = sys.argv[4]
scan_rc = int(sys.argv[5])

try:
    findings = json.loads(findings_path.read_text(encoding="utf-8"))
except json.JSONDecodeError:
    findings = []

if not isinstance(findings, list):
    findings = []

report = {
    "schema_version": "prompt-vote-lab-public-bundle-gitleaks-scan-v1",
    "ok": scan_rc == 0 and len(findings) == 0,
    "scanner": "gitleaks",
    "scanner_image": image,
    "bundle_dir": bundle_dir,
    "gitleaks_exit_code": scan_rc,
    "finding_count": len(findings),
    "findings_file": str(findings_path),
    "scan_scope": "public-agent-run-bundle-only",
    "repo_wide_scan": False,
}
report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

if [ "$scan_rc" -eq 0 ]; then
  echo "public bundle Gitleaks scan passed"
  exit 0
fi

if [ "$scan_rc" -eq 2 ]; then
  echo "public bundle Gitleaks scan found potential secrets" >&2
  exit 1
fi

echo "public bundle Gitleaks scan failed with exit code $scan_rc" >&2
exit "$scan_rc"
