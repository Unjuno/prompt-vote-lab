#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

SAFE_CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none';"


def labels(item: dict[str, Any]) -> set[str]:
    return {str(x) for x in item.get('labels', [])}


def rank_from_issue(issue: dict[str, Any]) -> int | None:
    text = f"{issue.get('title', '')}\n{issue.get('body', '')}".lower()
    for n in (1, 2, 3):
        if f'rank {n}' in text or f'rank-{n}' in text or f'rank:{n}' in text:
            return n
    return None


def pr_rank(pr: dict[str, Any]) -> int | None:
    body = str(pr.get('body', ''))
    for n in (1, 2, 3):
        if f'- Rank: {n}' in body or f'candidate_rank: {n}' in body:
            return n
    return None


def pr_issue(pr: dict[str, Any]) -> int | None:
    body = str(pr.get('body', ''))
    for marker in ('- Issue: #', 'Issue: #'):
        if marker in body:
            tail = body.split(marker, 1)[1]
            digits = []
            for ch in tail:
                if ch.isdigit():
                    digits.append(ch)
                else:
                    break
            return int(''.join(digits)) if digits else None
    return None


def pr_number(pr: dict[str, Any]) -> int:
    try:
        return int(pr.get('number') or 0)
    except (TypeError, ValueError):
        return 0


def state_score(state: str) -> int:
    state = state.upper()
    if state == 'MERGED':
        return 3
    if state == 'OPEN':
        return 2
    if state == 'CLOSED':
        return 1
    return 0


def best_prs(prs: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for pr in prs:
        issue_no = pr_issue(pr)
        if issue_no is None:
            continue
        old = out.get(issue_no)
        key = (state_score(str(pr.get('state', ''))), pr_number(pr))
        old_key = (state_score(str(old.get('state', ''))), pr_number(old)) if old else (-1, -1)
        if key > old_key:
            out[issue_no] = pr
    return out


def issue_safety(issue: dict[str, Any]) -> str:
    safety = issue.get('safety') or {}
    if safety.get('blocked'):
        return 'blocked'
    if safety.get('review'):
        return 'review'
    if safety.get('clear'):
        return 'clear'
    return 'unknown'


def vote_count(issue: dict[str, Any], pr: dict[str, Any] | None) -> int:
    if pr:
        marker = '- Votes: '
        body = str(pr.get('body', ''))
        if marker in body:
            tail = body.split(marker, 1)[1]
            digits = []
            for ch in tail:
                if ch.isdigit():
                    digits.append(ch)
                else:
                    break
            if digits:
                return int(''.join(digits))
    return int(issue.get('reaction_plus_one_count') or 0)


def changed_files(pr: dict[str, Any] | None) -> list[str]:
    if not pr:
        return []
    return [str(f.get('path')) for f in pr.get('files', []) if f.get('path')]


def decision(issue_labels: set[str], pr: dict[str, Any] | None) -> str:
    if 'outcome:blocked' in issue_labels:
        return 'blocked'
    if 'outcome:not-selected' in issue_labels:
        return 'not selected'
    if 'outcome:implemented' in issue_labels:
        return 'implemented'
    if pr and str(pr.get('state', '')).upper() == 'MERGED':
        return 'implemented'
    return 'pending'


def rows(data: dict[str, Any], week_id: str) -> list[dict[str, Any]]:
    prs_by_issue = best_prs(list(data.get('pull_requests', [])))
    best_by_rank: dict[int, dict[str, Any]] = {}
    for issue in data.get('issues', []):
        if f'week:{week_id}' not in labels(issue):
            continue
        pr = prs_by_issue.get(int(issue.get('number')))
        rank = pr_rank(pr) if pr else None
        if rank is None:
            rank = rank_from_issue(issue)
        if rank is None:
            continue
        issue_labels = labels(issue)
        row = {
            'rank': rank,
            'issue_no': int(issue.get('number')),
            'issue_title': str(issue.get('title', '')),
            'issue_url': str(issue.get('url', '')),
            'issue_state': str(issue.get('state', '')),
            'votes': vote_count(issue, pr),
            'safety': issue_safety(issue),
            'runtime': bool((issue.get('safety') or {}).get('runtime_detected')),
            'pr_no': pr_number(pr) if pr else None,
            'pr_url': str(pr.get('url', '')) if pr else '',
            'pr_state': str(pr.get('state', 'not run')) if pr else 'not run',
            'files': changed_files(pr),
            'decision': decision(issue_labels, pr),
        }
        old = best_by_rank.get(rank)
        key = (state_score(row['pr_state']), row['pr_no'] or 0, row['issue_no'])
        old_key = (state_score(old['pr_state']), old['pr_no'] or 0, old['issue_no']) if old else (-1, -1, -1)
        if key > old_key:
            best_by_rank[rank] = row
    return [best_by_rank[n] for n in sorted(best_by_rank)]


def link(url: str, label: str) -> str:
    label = html.escape(label)
    return f'<a href="{html.escape(url, quote=True)}">{label}</a>' if url else label


def render_dashboard(data: dict[str, Any], week_id: str) -> str:
    cards = []
    for row in rows(data, week_id):
        files = ''.join(f'<li><code>{html.escape(name)}</code></li>' for name in row['files']) or '<li>not run yet</li>'
        pr_label = f"PR #{row['pr_no']}" if row['pr_no'] else 'not run yet'
        cards.append(f'''
      <article class="rank-card" aria-labelledby="rank-{row['rank']}-title">
        <p class="rank-eyebrow">Rank {row['rank']}</p>
        <h2 id="rank-{row['rank']}-title">{html.escape(row['issue_title'])}</h2>
        <dl class="facts">
          <div><dt>Issue</dt><dd>{link(row['issue_url'], f"Issue #{row['issue_no']}")} · {html.escape(row['issue_state'])}</dd></div>
          <div><dt>Votes</dt><dd>{row['votes']}</dd></div>
          <div><dt>Safety</dt><dd>{html.escape(row['safety'])}</dd></div>
          <div><dt>Runtime scan</dt><dd>{'detected' if row['runtime'] else 'not recorded'}</dd></div>
          <div><dt>Implementation PR</dt><dd>{link(row['pr_url'], pr_label)} · {html.escape(row['pr_state'])}</dd></div>
          <div><dt>Output root</dt><dd><code>lab/comparisons/{html.escape(week_id)}/rank-{row['rank']}/</code></dd></div>
          <div><dt>Run record</dt><dd><code>runs/{html.escape(week_id)}-rank-{row['rank']}-issue-{row['issue_no']}.md</code></dd></div>
          <div><dt>Decision</dt><dd>{html.escape(row['decision'])}</dd></div>
        </dl>
        <h3>Changed files</h3>
        <ul class="changed-files">{files}</ul>
      </article>''')
    cards_html = '\n'.join(cards) if cards else '<p>No comparison rows found for this week.</p>'
    generated = html.escape(str(data.get('generated_at', 'unknown')))
    return f'''<!doctype html>
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
      <p>Generated from <code>data/public-results.json</code> at <code>{generated}</code>.</p>
    </section>
    <section class="rank-grid" aria-label="Comparison candidates">
{cards_html}
    </section>
  </main>
</body>
</html>
'''


def render_css() -> str:
    return ''':root {
  color-scheme: light;
  --bg: #f7f5ef;
  --text: #171717;
  --muted: #62615c;
  --line: #d9d3c5;
  --card: #fffdf7;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); }
.comparison-root { width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 40px 0; }
.status { color: var(--muted); font-size: 0.95rem; margin: 0 0 8px; }
h1 { margin: 0 0 12px; font-size: clamp(2rem, 5vw, 4rem); line-height: 1; }
.note, .method { color: var(--muted); max-width: 780px; }
.method { border: 1px solid var(--line); background: var(--card); padding: 16px; border-radius: 18px; margin: 24px 0; }
.rank-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.rank-card { border: 1px solid var(--line); background: var(--card); border-radius: 20px; padding: 18px; }
.rank-eyebrow { margin: 0 0 6px; color: var(--muted); font-weight: 700; }
.rank-card h2 { margin: 0 0 14px; font-size: 1.25rem; }
.facts { display: grid; gap: 10px; margin: 0; }
.facts div { border-top: 1px solid var(--line); padding-top: 8px; }
dt { font-weight: 700; }
dd { margin: 2px 0 0; color: var(--muted); }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.9em; }
a { color: inherit; text-underline-offset: 0.18em; }
.changed-files { padding-left: 1.1rem; color: var(--muted); }
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--public-results', default='data/public-results.json')
    parser.add_argument('--week-id', required=True)
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.public_results).read_text(encoding='utf-8'))
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(render_dashboard(data, args.week_id), encoding='utf-8')
    (out / 'style.css').write_text(render_css(), encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
