#!/usr/bin/env bash
set -euo pipefail

base_ref="${BASE_REF:-origin/main}"
head_ref="${HEAD_REF:-HEAD}"

if ! git rev-parse --verify "$base_ref" >/dev/null 2>&1; then
  echo "ERROR: base ref not found: $base_ref"
  exit 1
fi

mapfile -t changed_files < <(git diff --name-only "$base_ref"..."$head_ref" | sort)

if [ "${#changed_files[@]}" -eq 0 ]; then
  echo "No changed files."
  exit 0
fi

echo "Changed files:"
printf '  - %s\n' "${changed_files[@]}"

lab_changed=false
non_lab_changes=()
invalid_lab_changes=()

for file in "${changed_files[@]}"; do
  case "$file" in
    lab/index.html|lab/style.css|lab/app.js)
      lab_changed=true
      ;;
    lab/*)
      lab_changed=true
      invalid_lab_changes+=("$file")
      ;;
    *)
      non_lab_changes+=("$file")
      ;;
  esac
done

if [ "$lab_changed" != "true" ]; then
  echo "No lab files changed. Lab PR scope guard passes."
  exit 0
fi

if [ "${#invalid_lab_changes[@]}" -gt 0 ]; then
  echo "ERROR: lab implementation PRs may only change these files:"
  echo "  - lab/index.html"
  echo "  - lab/style.css"
  echo "  - lab/app.js"
  echo "Invalid lab path changes:"
  printf '  - %s\n' "${invalid_lab_changes[@]}"
  exit 1
fi

if [ "${#non_lab_changes[@]}" -gt 0 ]; then
  echo "ERROR: PR changes lab files and non-lab files together."
  echo "Codex/agent implementation PRs must keep evidence, workflow, docs, and policy files untouched."
  echo "Move non-lab changes to a separate human-reviewed PR."
  echo "Non-lab changes detected:"
  printf '  - %s\n' "${non_lab_changes[@]}"
  exit 1
fi

echo "Lab PR scope guard passes: only approved lab files changed."
