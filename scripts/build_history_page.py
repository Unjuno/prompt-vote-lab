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
class WeekSummary:
    week_id: str
    total_issues: int
    clear_count: int
    blocked_count: int
    review_count: int
    runtime_count: int
    implemented_count: int
    not_selected_count: int
    open_count: int
    adopted_rank: str
    comparison_href: str


def _labels(item: dict[str, Any]) -> set[str]:
    return {str(label) for label in item.get("labels", [])}


def _week_labels(issue: dict[str, Any]) -> set[str]:
    return {label.split(":", 1)[1] for label in _labels(issue) if label.startswith("week:")}


def _rank_from_text(issue: dict[str, Any]) -> int | None:
    text = f"{issue.get('title', '')}\n{issue.get('body', '')}".lower()
    for rank in (1, 2, 3):
        if f"rank {rank}" in text or f"rank-{rank}" in text or f"rank:{rank}" in text:
            return rank
    return None


def build_week_summaries(public_results: dict[str, Any]) -> list[WeekSummary]:
    issues = list(public_results.get("issues", []))
    week_ids = sorted({week for issue in issues for week in _week_labels(issue)}, reverse=True)
    summaries: list[WeekSummary] = []

    for week_id in week_ids:
        week_issues = [issue for issue in issues if week_id in _week_labels(issue)]
        clear_count = 0
        blocked_count = 0
        review_count = 0
        runtime_count = 0
        implemented_count = 0
        not_selected_count = 0
        open_count = 0
        adopted_rank: str | None = None

        for issue in week_issues:
            labels = _labels(issue)
            safety = issue.get("safety") or {}
            if safety.get("clear") or "issue-safety:clear" in labels:
                clear_count += 1
            if safety.get("blocked") or "issue-safety:blocked" in labels:
                blocked_count += 1
            if safety.get("review") or "issue-safety:review" in labels:
                review_count += 1
            if safety.get("runtime_detected") or "issue-safety:runtime-detected" in labels:
                runtime_count += 1
            if "outcome:implemented" in labels:
                implemented_count += 1
                rank = _rank_from_text(issue)
                if rank is not None:
                    adopted_rank = f"rank {rank}"
            if "outcome:not-selected" in labels:
                not_selected_count += 1
            if str(issue.get("state", "")).upper() == "OPEN":
                open_count += 1

        summaries.append(
            WeekSummary(
                week_id=week_id,
                total_issues=len(week_issues),
                clear_count=clear_count,
                blocked_count=blocked_count,
                review_count=review_count,
                runtime_count=runtime_count,
                implemented_count=implemented_count,
                not_selected_count=not_selected_count,
                open_count=open_count,
                adopted_rank=adopted_rank or "not decided",
                comparison_href=f"../comparisons/{week_id}/",
            )
        )
    return summaries


def render_history(public_results: dict[str, Any]) -> str:
    summaries = build_week_summaries(public_results)
    generated_at = html.escape(str(public_results.get("generated_at", "unknown")))
    cards: list[str] = []
    for summary in summaries:
        cards.append(
            f"""
      <article class="week-card" aria-labelledby="week-{html.escape(summary.week_id)}">
        <div class="week-card-head">
          <p class="week-kicker">Week</p>
          <h2 id="week-{html.escape(summary.week_id)}">{html.escape(summary.week_id)}</h2>
        </div>
        <dl class="facts">
          <div><dt>Candidates</dt><dd>{summary.total_issues}</dd></div>
          <div><dt>Clear</dt><dd>{summary.clear_count}</dd></div>
          <div><dt>Runtime scans</dt><dd>{summary.runtime_count}</dd></div>
          <div><dt>Blocked</dt><dd>{summary.blocked_count}</dd></div>
          <div><dt>Review</dt><dd>{summary.review_count}</dd></div>
          <div><dt>Implemented</dt><dd>{summary.implemented_count}</dd></div>
          <div><dt>Not selected</dt><dd>{summary.not_selected_count}</dd></div>
          <div><dt>Open</dt><dd>{summary.open_count}</dd></div>
          <div><dt>Adopted</dt><dd>{html.escape(summary.adopted_rank)}</dd></div>
        </dl>
        <p class="week-link"><a href="{html.escape(summary.comparison_href, quote=True)}">Open weekly comparison</a></p>
      </article>"""
        )
    cards_html = "\n".join(cards) if cards else "<p>No week records found yet.</p>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Prompt Vote Lab history</title>
  <link rel="stylesheet" href="./style.css">
  <meta http-equiv="Content-Security-Policy" content="{SAFE_CSP}">
</head>
<body>
  <main class="history-root" aria-labelledby="history-title">
    <p class="status">History · generated from public results</p>
    <h1 id="history-title">Prompt Vote Lab history</h1>
    <p class="note">This page summarizes weekly progression. GitHub Issues, PRs, commits, public bundles, and run records remain the source of truth.</p>
    <section class="method" aria-labelledby="flow-title">
      <h2 id="flow-title">Candidate state flow</h2>
      <ol class="flow">
        <li>Issue posted</li>
        <li>submission safety scan</li>
        <li>clear / review / blocked</li>
        <li>rank selected</li>
        <li>comparison run</li>
        <li>PR created</li>
        <li>merged / not selected / blocked</li>
        <li>finalizer close</li>
      </ol>
      <p>Generated from <code>data/public-results.json</code> at <code>{generated_at}</code>.</p>
    </section>
    <section class="week-grid" aria-label="Weekly experiment history">
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
.history-root {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
  padding: 40px 0;
}
.status {
  color: var(--muted);
  font-size: 0.95rem;
  margin: 0 0 8px;
}
h1 { margin: 0 0 12px; font-size: clamp(2.2rem, 5vw, 4.5rem); line-height: 1; }
.note, .method { color: var(--muted); max-width: 820px; }
.method {
  border: 1px solid var(--line);
  background: var(--card);
  padding: 16px;
  border-radius: 18px;
  margin: 24px 0;
}
.flow {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0;
  list-style: none;
}
.flow li {
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 8px 10px;
  background: #fff;
}
.week-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}
.week-card {
  border: 1px solid var(--line);
  background: var(--card);
  border-radius: 20px;
  padding: 18px;
}
.week-kicker { color: var(--muted); font-weight: 700; margin: 0 0 4px; }
.week-card h2 { margin: 0 0 14px; font-size: 1.8rem; }
.facts { display: grid; gap: 10px; margin: 0; }
.facts div { border-top: 1px solid var(--line); padding-top: 8px; }
dt { font-weight: 700; }
dd { margin: 2px 0 0; color: var(--muted); }
.week-link { margin: 16px 0 0; font-weight: 700; }
a { color: inherit; text-underline-offset: 0.18em; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.9em; }
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-results", default="data/public-results.json")
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    public_results = json.loads(Path(args.public_results).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(render_history(public_results), encoding="utf-8")
    (out_dir / "style.css").write_text(render_css(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
