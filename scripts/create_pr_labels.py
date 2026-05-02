#!/usr/bin/env python3
"""Create Prompt Vote Lab labels if they do not exist."""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen


LABELS = {
    "pvl:implementation": "0E8A16",
    "pvl:mock": "BFD4F2",
    "pvl:merged": "8250DF",
    "pvl:rejected": "D73A4A",
    "pvl:unsafe": "B60205",
    "pvl:failed": "D93F0B",
    "pvl:no-change": "6A737D",
    "pvl:report-needed": "FBCA04",
}


def request(method: str, url: str, token: str, payload: dict | None = None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "prompt-vote-lab-label-setup",
        },
    )
    with urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8") or "{}")


def main() -> int:
    repo = os.getenv("GITHUB_REPOSITORY")
    token = os.getenv("GITHUB_TOKEN")
    if not repo or not token:
        print("GITHUB_REPOSITORY and GITHUB_TOKEN are required", file=sys.stderr)
        return 2

    base = f"https://api.github.com/repos/{repo}/labels"
    for name, color in LABELS.items():
        payload = {
            "name": name,
            "color": color,
            "description": "Prompt Vote Lab workflow label",
        }
        try:
            request("POST", base, token, payload)
            print(f"created {name}")
        except HTTPError as exc:
            if exc.code == 422:
                patch_url = f"{base}/{name.replace(':', '%3A')}"
                request("PATCH", patch_url, token, payload)
                print(f"updated {name}")
            else:
                raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
