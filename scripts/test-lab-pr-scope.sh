#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

copy_repo() {
  local target="$1"
  mkdir -p "$target"
  tar \
    --exclude='.git' \
    --exclude='tmp' \
    --exclude='.DS_Store' \
    -C "$root_dir" \
    -cf - . | tar -C "$target" -xf -
}

init_case_repo() {
  local repo_dir="$1"
  copy_repo "$repo_dir"
  git -C "$repo_dir" init -q
  git -C "$repo_dir" config user.email "scope-test@example.invalid"
  git -C "$repo_dir" config user.name "Scope Test"
  git -C "$repo_dir" add .
  git -C "$repo_dir" commit -q -m "base"
  git -C "$repo_dir" branch -M main
  git -C "$repo_dir" checkout -q -b case-branch
}

run_case() {
  local name="$1"
  local expected="$2"
  local mutate_fn="$3"
  local repo_dir="$work_dir/$name"

  echo "CASE: $name expects $expected"
  init_case_repo "$repo_dir"
  "$mutate_fn" "$repo_dir"

  set +e
  (
    cd "$repo_dir"
    BASE_REF=main HEAD_REF=HEAD bash scripts/check-lab-pr-scope.sh
  ) >"$repo_dir/out.log" 2>"$repo_dir/err.log"
  local status=$?
  set -e

  cat "$repo_dir/out.log"
  cat "$repo_dir/err.log" >&2

  if [ "$expected" = "pass" ] && [ "$status" -ne 0 ]; then
    echo "ERROR: $name should pass but failed with status $status"
    exit 1
  fi

  if [ "$expected" = "fail" ] && [ "$status" -eq 0 ]; then
    echo "ERROR: $name should fail but passed"
    exit 1
  fi

  echo "CASE OK: $name"
}

mutate_root_lab_only() {
  local repo_dir="$1"
  printf '\n<!-- scope test root lab only -->\n' >> "$repo_dir/lab/index.html"
  git -C "$repo_dir" add lab/index.html
  git -C "$repo_dir" commit -q -m "change root lab only"
}

mutate_docs_only() {
  local repo_dir="$1"
  printf '\nScope test docs only.\n' >> "$repo_dir/docs/README.md"
  git -C "$repo_dir" add docs/README.md
  git -C "$repo_dir" commit -q -m "change docs only"
}

mutate_generated_comparison_only() {
  local repo_dir="$1"
  mkdir -p "$repo_dir/lab/comparisons/2099-W01/rank-2"
  printf '<!doctype html>\n<title>scope test</title>\n' > "$repo_dir/lab/comparisons/2099-W01/rank-2/index.html"
  git -C "$repo_dir" add lab/comparisons/2099-W01/rank-2/index.html
  git -C "$repo_dir" commit -q -m "change generated comparison only"
}

mutate_generated_history_only() {
  local repo_dir="$1"
  mkdir -p "$repo_dir/lab/history"
  printf '<!doctype html>\n<title>history scope test</title>\n' > "$repo_dir/lab/history/index.html"
  git -C "$repo_dir" add lab/history/index.html
  git -C "$repo_dir" commit -q -m "change generated history only"
}

mutate_generated_week_only() {
  local repo_dir="$1"
  mkdir -p "$repo_dir/lab/weeks/2099-W01"
  printf '<!doctype html>\n<title>week scope test</title>\n' > "$repo_dir/lab/weeks/2099-W01/index.html"
  git -C "$repo_dir" add lab/weeks/2099-W01/index.html
  git -C "$repo_dir" commit -q -m "change generated week only"
}

mutate_root_lab_and_docs() {
  local repo_dir="$1"
  printf '\n<!-- scope test mixed -->\n' >> "$repo_dir/lab/index.html"
  printf '\nScope test mixed docs.\n' >> "$repo_dir/docs/README.md"
  git -C "$repo_dir" add lab/index.html docs/README.md
  git -C "$repo_dir" commit -q -m "change root lab and docs"
}

mutate_root_lab_and_generated_evidence() {
  local repo_dir="$1"
  mkdir -p "$repo_dir/lab/comparisons/2099-W01/rank-1"
  printf '\n<!-- scope test root lab plus evidence -->\n' >> "$repo_dir/lab/index.html"
  printf '<!doctype html>\n<title>mixed evidence</title>\n' > "$repo_dir/lab/comparisons/2099-W01/rank-1/index.html"
  git -C "$repo_dir" add lab/index.html lab/comparisons/2099-W01/rank-1/index.html
  git -C "$repo_dir" commit -q -m "change root lab and generated evidence"
}

mutate_extra_lab_file() {
  local repo_dir="$1"
  printf 'console.log("scope test extra file");\n' > "$repo_dir/lab/extra.js"
  git -C "$repo_dir" add lab/extra.js
  git -C "$repo_dir" commit -q -m "add extra lab file"
}

run_case "root-lab-only" "pass" mutate_root_lab_only
run_case "docs-only" "pass" mutate_docs_only
run_case "generated-comparison-only" "pass" mutate_generated_comparison_only
run_case "generated-history-only" "pass" mutate_generated_history_only
run_case "generated-week-only" "pass" mutate_generated_week_only
run_case "root-lab-and-docs" "fail" mutate_root_lab_and_docs
run_case "root-lab-and-generated-evidence" "fail" mutate_root_lab_and_generated_evidence
run_case "extra-lab-file" "fail" mutate_extra_lab_file

echo "Lab PR scope guard self-test passed."
