#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

QUERY = """
query PromptVoteLabSupportActivities($login: String!, $since: DateTime!, $until: DateTime!, $after: String) {
  user(login: $login) {
    sponsorsActivities(
      first: 100
      after: $after
      since: $since
      until: $until
      actions: [NEW_SPONSORSHIP]
      includePrivate: true
      includeAsSponsor: false
      period: ALL
      orderBy: {field: TIMESTAMP, direction: DESC}
    ) {
      nodes {
        action
        timestamp
        sponsorsTier {
          isOneTime
          monthlyPriceInCents
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
""".strip()


def gh_graphql(query: str, variables: dict[str, str]) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value:
            cmd.extend(["-F", f"{key}={value}"])
    completed = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr)
        raise SystemExit(completed.returncode)
    return json.loads(completed.stdout)


def collect(login: str, since: str, until: str) -> dict:
    all_nodes = []
    after = ""
    while True:
        payload = gh_graphql(QUERY, {"login": login, "since": since, "until": until, "after": after})
        user = (payload.get("data") or {}).get("user") or {}
        activities = user.get("sponsorsActivities") or {}
        nodes = activities.get("nodes") or []
        all_nodes.extend(nodes)
        page_info = activities.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        after = str(page_info.get("endCursor") or "")
        if not after:
            break
    return {"data": {"user": {"sponsorsActivities": {"nodes": all_nodes}}}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", default=os.getenv("SPONSORS_LOGIN", "Unjuno"))
    parser.add_argument("--since", required=True)
    parser.add_argument("--until", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    payload = collect(args.login, args.since, args.until)
    Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"support activity payload written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
