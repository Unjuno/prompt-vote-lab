#!/usr/bin/env bash
set -euo pipefail

BASE_REF="${1:-origin/main}"
HEAD_REF="${2:-HEAD}"

if git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
  git diff --name-only "$BASE_REF...$HEAD_REF" > changed_files.txt
else
  git diff --name-only > changed_files.txt
fi

echo "Changed files:"
cat changed_files.txt || true

if [ -s changed_files.txt ]; then
  if grep -v '^lab/' changed_files.txt | grep .; then
    echo "ERROR: Found changes outside lab/."
    exit 1
  fi
fi

if [ ! -d lab ]; then
  echo "ERROR: lab/ does not exist."
  exit 1
fi

forbidden='fetch\(|XMLHttpRequest|WebSocket|EventSource|eval\(|new Function|document\.cookie|<script[^>]+src=|<iframe|navigator\.sendBeacon'

if grep -R -n -E "$forbidden" lab/; then
  echo "ERROR: Forbidden pattern detected."
  exit 1
fi

echo "Safety check passed."
