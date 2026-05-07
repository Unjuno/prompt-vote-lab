#!/usr/bin/env bash
set -euo pipefail

scan_json=""
comment_md=""
issue_number=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --scan-json)
      scan_json="${2:-}"
      shift 2
      ;;
    --comment-md)
      comment_md="${2:-}"
      shift 2
      ;;
    --issue-number)
      issue_number="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [ -z "$scan_json" ] || [ ! -f "$scan_json" ]; then
  echo "--scan-json must point to an existing file" >&2
  exit 2
fi
if [ -z "$comment_md" ] || [ ! -f "$comment_md" ]; then
  echo "--comment-md must point to an existing file" >&2
  exit 2
fi
if [ -z "$issue_number" ] || [ "$issue_number" = "0" ]; then
  echo "--issue-number must be positive" >&2
  exit 2
fi
if [ -z "${GITHUB_REPOSITORY:-}" ]; then
  echo "GITHUB_REPOSITORY is required" >&2
  exit 2
fi
if [ -z "${GH_TOKEN:-}" ]; then
  echo "GH_TOKEN is required" >&2
  exit 2
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

python - "$scan_json" "$workdir" <<'PY'
from __future__ import annotations
import json
import sys
from pathlib import Path
scan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
out = Path(sys.argv[2])
(out / "labels.tsv").write_text(
    "".join(
        f"{name}\t{meta['color']}\t{meta['description']}\n"
        for name, meta in sorted(scan["label_metadata"].items())
    ),
    encoding="utf-8",
)
(out / "labels_to_add.txt").write_text("\n".join(scan["labels_to_add"]) + "\n", encoding="utf-8")
(out / "labels_to_remove.txt").write_text("\n".join(scan["labels_to_remove"]) + "\n", encoding="utf-8")
(out / "comment-marker.txt").write_text(scan["comment_marker"], encoding="utf-8")
PY

while IFS=$'\t' read -r name color description; do
  if [ -z "$name" ]; then
    continue
  fi
  gh label create "$name" --color "$color" --description "$description" --force >/dev/null 2>&1 || true
done < "$workdir/labels.tsv"

while IFS= read -r label; do
  if [ -z "$label" ]; then
    continue
  fi
  gh issue edit "$issue_number" --remove-label "$label" >/dev/null 2>&1 || true
done < "$workdir/labels_to_remove.txt"

while IFS= read -r label; do
  if [ -z "$label" ]; then
    continue
  fi
  gh issue edit "$issue_number" --add-label "$label" >/dev/null
done < "$workdir/labels_to_add.txt"

python - "$comment_md" "$workdir/comment-body.json" <<'PY'
from __future__ import annotations
import json
import sys
from pathlib import Path
body = Path(sys.argv[1]).read_text(encoding="utf-8")
Path(sys.argv[2]).write_text(json.dumps({"body": body}) + "\n", encoding="utf-8")
PY

gh api "repos/$GITHUB_REPOSITORY/issues/$issue_number/comments" --paginate > "$workdir/comments.json"
comment_id="$(python - "$workdir/comments.json" "$workdir/comment-marker.txt" <<'PY'
from __future__ import annotations
import json
import sys
from pathlib import Path
comments = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8") or "[]")
marker = Path(sys.argv[2]).read_text(encoding="utf-8")
for comment in comments:
    if marker in str(comment.get("body") or ""):
        print(comment.get("id") or "")
        break
PY
)"

if [ -n "$comment_id" ]; then
  gh api --method PATCH "repos/$GITHUB_REPOSITORY/issues/comments/$comment_id" --input "$workdir/comment-body.json" >/dev/null
else
  gh api --method POST "repos/$GITHUB_REPOSITORY/issues/$issue_number/comments" --input "$workdir/comment-body.json" >/dev/null
fi

echo "Applied Issue safety feedback for #$issue_number."
