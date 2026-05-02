#!/usr/bin/env python3
"""Render Prompt Vote Lab JSONL events into a Markdown summary."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_path", default=".tmp/events.jsonl")
    parser.add_argument("--out", default=".tmp/events-summary.md")
    parser.add_argument("--title", default="Prompt Vote Lab event summary")
    args = parser.parse_args()

    events = read_events(Path(args.in_path))
    counter = Counter((e.get("event_type", "unknown"), e.get("status", "unknown")) for e in events)

    lines = [
        f"# {args.title}",
        "",
        f"- events: {len(events)}",
        "",
        "## Counts",
        "",
        "| Event type | Status | Count |",
        "|---|---|---:|",
    ]
    for (event_type, status), count in sorted(counter.items()):
        lines.append(f"| {event_type} | {status} | {count} |")

    lines += [
        "",
        "## Events",
        "",
        "| Time | Type | Source | Status | Week | Rank | Payload |",
        "|---|---|---|---|---|---:|---|",
    ]
    for e in events:
        payload = json.dumps(e.get("payload", {}), ensure_ascii=False, sort_keys=True)
        if len(payload) > 180:
            payload = payload[:177] + "..."
        lines.append(
            "| {time} | {typ} | {source} | {status} | {week} | {rank} | `{payload}` |".format(
                time=e.get("timestamp_utc", ""),
                typ=e.get("event_type", ""),
                source=e.get("source", ""),
                status=e.get("status", ""),
                week=e.get("week", ""),
                rank=e.get("candidate_rank", ""),
                payload=payload.replace("|", "\\|"),
            )
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
