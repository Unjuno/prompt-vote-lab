#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SAFE_CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none';"


@dataclass(frozen=True)
class ComparisonRow:
    rank: int
    issue_number: int
    issue_title: str
    issue_url: str
    issue_state: str
    vote_count: int
    safety_status: str
    runtime_detected: bool
    pr_number: int | None
    pr_title: str
    pr_url: str
    pr_state: str
    changed_files: tuple[str, ...]
    run_record_path: str
    output_root: str
    decision: str


def _labels(item: dict[str, Any]) -> set[str]:
    return {str(label) for label in item.get("labels", [])}


def _issue_safety(item: dict[str, Any]) -> str:
    safety = item.get("safety") or {}
    if safety.get("blocked"):
        return "blocked"
    if safety.get("review"):
        return "review"
    if safety.get("clear"):
        return "clear"
    return "unknown"


def _rank_from_issue(item: dict[str, Any]) -> int | None:
    title = str(item.get("title", ""))
    body = str(item.get("body", ""))
    text = f"{title}\n{body}".lower()
    for rank in (1, 2, 3):
        if f"rank {rank}" in text or f"rank-{rank}" in text or f"rank:{rank}" in text:
            return rank
    return None


def _pr_rank(item: dict[str, Any]) -> int | None:
    body = str(item.get("body", ""))
    for rank in (1, 2, 3):
        if f"- Rank: {rank}" in body or f"candidate_rank: {rank}" in body:
            return rank
    return None


def _pr_issue_number(item: dict[str, Any]) -> int | None:
    body = str(item.get("body", ""))
    for marker in ("- Issue: #", "Issue: #"):
        if marker in body:
            tail = body.split(marker, 1)[1]
            digits = []
            for ch in tail:
                if ch.isdigit():
                    digits.append(ch)
                else:
                    break
            if digits:
                return int("".join(digits))
    return None


def _vote_count(issue: dict[str, Any], pr: dict[str, Any] | None) -> int:
    if pr:
        body = str(pr.get("body", ""))
        marker = "- Votes: "
        if marker in body:
            tail = body.split(marker, 1)[1]
            digits = []
            for ch in tail:
                if ch.isdigit():
                    digits.append(ch)
                else:
                    break
            if digits:
                return int("".join(digits))
    return int(issue.get("reaction_plus_one_count") or 0)


def _changed_files(pr: dict[str, Any] | None) -> tuple[str, ...]:
    if not pr:
        return ()
    files = pr.get("files") or []
    return tuple(str(item.get("path", "")) for item in files if item.get("path"))


def build_rows(public_results: dict[str, Any], week_id: str) -> list[ComparisonRow]:
    issues = [item for item in public_results.get("issues", []) if f"week:{week_id}" in _labels(item)]
    prs = list(public_results.get("pull_requests", []))
    prs_by_issue: dict[int, dict[str, Any]] = {}
    for pr in prs:
        issue_number = _pr_issue_number(pr)
        if issue_number is not None:
            prs_by_issue[issue_number] = pr

    rows: list[ComparisonRow] = []
    for issue in issues:
        rank = _rank_from_issue(issue)
        pr = prs_by_issue.get(int(issue.get("number")))
        if pr and _pr_rank(pr) is not None:
            rank = _pr_rank(pr)
        if rank is None:
            continue
        issue_number = int(issue.get("number"))
        run_record_path = f"runs/{week_id}-rank-{rank}-issue-{issue_number}.md"
        output_root = f"lab/comparisons/{week_id}/rank-{rank}/"
        labels = _labels(issue)
        decision = "implemented" if "outcome:implemented" in labels else "pending"
        if "outcome:blocked" in labels:
            decision = "blocked"
        elif "outcome:not-selected" in labels:
            decision = "not selected"
        rows.append(
            ComparisonRow(
                rank=rank,
                issue_number=issue_number,
                issue_title=str(issue.get("title", "")),
                issue_url=str(issue.get("url", "")),
                issue_state=str(issue.get("state", "")),
                vote_count=_vote_count(issue, pr),
                safety_status=_issue_safety(issue),
                runtime_detected=bool((issue.get("safety") or {}).get("runtime_detected")),
                pr_number=int(pr.get("number")) if pr else None,
                pr_title=str(pr.get("title", "")) if pr else "not run yet",
                pr_url=str(pr.get("url", "")) if pr else "",
                pr_state=str(pr.get("state", "not run")) if pr else "not run",
                changed_files=_changed_files(pr),
                run_record_path=run_record_path,
                output_root=output_root,
                decision=decision,
            )
        )
    return sorted(rows, key=lambda row: row.rank)


def _link(url: str, label: str) -> str:
    safe_label = html.escape(label)
    if not url:
        return safe_label
    return f'<a href="{html.escape(url, quote=True)}">{safe_label}</a>'


def render_dashboard(public_results: dict[str, Any], week_id: str) -> str:
    rows = build_rows(public_results, week_id)
    generated_at = html.escape(str(public_results.get("generated_at", "unknown")))
    cards = []
    for row in rows:
        changed = "".join(f"<li><code>{html.escape(name)}</code></li>" for name in row.changed_files) or "<li>not run yet</li>"
        pr_label = f"PR #{row.pr_number}" if row.pr_number is not None else "not run yet"
        cards.append(
            f"""
      <article class="rank-card" aria-labelledby="rank-{row.rank}-title">
        <p class="rank-eyebrow">Rank {row.rank}</p>
        <h2 id="rank-{row.rank}-title">{html.escape(row.issue_title)}</h2>
        <dl class="facts">
          <div><dt>Issue</dt><dd>{_link(row.issue_url, f'Issue #{row.issue_number}')} · {html.escape(row.issue_state)}</dd></div>
          <div><dt>Votes</dt><dd>{row.vote_count}</dd></div>
          <div><dt>Safety</dt><dd>{html.escape(row.safety_status)}</dd></div>
          <div><dt>Runtime scan</dt><dd>{'detected' if row.runtime_detected else 'not recorded'}</dd></div>
          <div><dt>Implementation PR</dt><dd>{_link(row.pr_url, pr_label)} · {html.escape(row.pr_state)}</dd></div>
          <div><dt>Output root</dt><dd><code>{html.escape(row.output_root)}</code></dd></div>
          <div><dt>Run record</dt><dd><code>{html.escape(row.run_record_path)}</code></dd></div>
          <div><dt>Decision</dt><dd>{html.escape(row.decision)}</dd></div>
        </dl>
        <h3>Changed files</h3>
        <ul class="changed-files">{changed}</ul>
      </article>"""
        )
    cards_html = "\n".join(cards) if cards else "<p>No comparison rows found for this week.</p>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Prompt Vote Lab comparison {html.escape(week_id)}</title>
  <link rel="stylesheet" href="./style.css">
  <meta http-equiv="Content-Security-Policy" content="{SAFE_CSP}">
</head>
<body>
  <main class="comparison-root" aria-labelledby="comparison-title">
    <p class="status">Comparison dashboard · generated from public results</p>
    <h1 id="comparison-title">Prompt Vote Lab comparison: {html.escape(week_id)}</h1>
    <p class="note">GitHub Issues, PRs, commits, public bundles, and run records remain the source of truth. This page is an index that makes the evidence readable.</p>
    <section class="method" aria-labelledby="method-title">
      <h2 id="method-title">Evaluation focus</h2>
      <p>Primary: participant evidence comprehension. Secondary: constrained static implementation quality, small diffs, and no forbidden runtime behavior.</p>
      <p>Generated from <code>data/public-results.json</code> at <code>{generated_at}</code>.</p>
    </section>
    <section class="rank-grid" aria-label="Comparison candidates">
{cards_html}
    </section>
  </main>
</body>
</html>
"""


def render_css() -> str:
    return """:root {
  color-scheme: light;
  --bg: #f7f5ef;
  --text: #171717;
  --muted: #62615c;
  --line: #d9d3c5;
  --card: #fffdf7;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
}
.comparison-root {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
  padding: 40px 0;
}
.status {
  color: var(--muted);
  font-size: 0.95rem;
  margin: 0 0 8px;
}
h1 { margin: 0 0 12px; font-size: clamp(2rem, 5vw, 4rem); line-height: 1; }
.note, .method { color: var(--muted); max-width: 780px; }
.method {
  border: 1px solid var(--line);
  background: var(--card);
  padding: 16px;
  border-radius: 18px;
  margin: 24px 0;
}
.rank-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}
.rank-card {
  border: 1px solid var(--line);
  background: var(--card);
  border-radius: 20px;
  padding: 18px;
}
.rank-eyebrow { margin: 0 0 6px; color: var(--muted); font-weight: 700; }
.rank-card h2 { margin: 0 0 14px; font-size: 1.25rem; }
.facts { display: grid; gap: 10px; margin: 0; }
.facts div { border-top: 1px solid var(--line); padding-top: 8px; }
dt { font-weight: 700; }
dd { margin: 2px 0 0; color: var(--muted); }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.9em; }
a { color: inherit; text-underline-offset: 0.18em; }
.changed-files { padding-left: 1.1rem; color: var(--muted); }
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-results", default="data/public-results.json")
    parser.add_argument("--week-id", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    public_results = json.loads(Path(args.public_results).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(render_dashboard(public_results, args.week_id), encoding="utf-8")
    (out_dir / "style.css").write_text(render_css(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
