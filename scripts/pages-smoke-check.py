#!/usr/bin/env python3
"""Check GitHub Pages root and lab URLs.

This script is intentionally small and uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def fetch(url: str) -> tuple[int, str, str]:
    req = Request(url, headers={"User-Agent": "prompt-vote-lab-pages-smoke-check"})
    with urlopen(req, timeout=30) as res:
        body = res.read(200_000).decode("utf-8", "replace")
        return int(res.status), str(res.headers.get("content-type") or ""), body


def require(url: str, expected: str) -> None:
    try:
        status, content_type, body = fetch(url)
    except HTTPError as exc:
        raise SystemExit(f"ERROR: {url} returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise SystemExit(f"ERROR: {url} failed: {exc}") from exc

    if status != 200:
        raise SystemExit(f"ERROR: {url} returned status {status}")
    if "text/html" not in content_type:
        raise SystemExit(f"ERROR: {url} content-type is {content_type}, expected text/html")
    if expected not in body:
        raise SystemExit(f"ERROR: {url} did not contain expected text: {expected!r}")
    print(f"OK: {url}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True, help="Example: https://unjuno.github.io/prompt-vote-lab")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    require(base + "/", "Prompt Vote Lab")
    require(base + "/", "20 virtual votes")
    require(base + "/lab/", "Prompt Vote Lab")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
