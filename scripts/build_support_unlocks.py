#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RANK_2_THRESHOLD_CENTS = 500
RANK_3_THRESHOLD_CENTS = 1000

ACTION_ALLOWLIST = {
    "NEW_SPONSORSHIP",
    "SPONSORSHIP_STARTED",
}

IDENTITY_KEYS = {
    "sponsor",
    "sponsors",
    "sponsorable",
    "sponsorEntity",
    "sponsor_login",
    "sponsorLogin",
    "login",
    "email",
    "name",
}


def parse_iso8601(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def iter_activity_nodes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(payload.get("nodes"), list):
        return [node for node in payload["nodes"] if isinstance(node, dict)]

    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    candidates = []
    if isinstance(data, dict):
        candidates.extend([data.get("user"), data.get("organization"), data.get("viewer")])

    for owner in candidates:
        if not isinstance(owner, dict):
            continue
        activities = owner.get("sponsorsActivities")
        if isinstance(activities, dict) and isinstance(activities.get("nodes"), list):
            return [node for node in activities["nodes"] if isinstance(node, dict)]
    return []


def get_nested(mapping: dict[str, Any], path: list[str]) -> Any:
    cursor: Any = mapping
    for key in path:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(key)
    return cursor


def event_time(node: dict[str, Any]) -> datetime | None:
    for key in ("timestamp", "createdAt", "occurredAt", "created_at"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            return parse_iso8601(value)
    return None


def tier_object(node: dict[str, Any]) -> dict[str, Any]:
    for path in (["sponsorsTier"], ["tier"], ["sponsorship", "tier"], ["sponsorship", "sponsorsTier"]):
        value = get_nested(node, path)
        if isinstance(value, dict):
            return value
    return {}


def tier_amount_cents(tier: dict[str, Any]) -> int:
    for key in ("monthlyPriceInCents", "amountInCents", "priceInCents", "oneTimePaymentInCents"):
        value = tier.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    return 0


def tier_is_one_time(tier: dict[str, Any], node: dict[str, Any]) -> bool:
    for source in (tier, node, node.get("sponsorship") if isinstance(node.get("sponsorship"), dict) else {}):
        if not isinstance(source, dict):
            continue
        for key in ("isOneTime", "oneTime", "is_one_time"):
            if isinstance(source.get(key), bool):
                return bool(source[key])
    return False


def contains_identity_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in IDENTITY_KEYS:
                return True
            if contains_identity_key(child):
                return True
    if isinstance(value, list):
        return any(contains_identity_key(child) for child in value)
    return False


def build_unlocks(payload: dict[str, Any], week_id: str, since: str, until: str, source: str) -> dict[str, Any]:
    since_dt = parse_iso8601(since)
    until_dt = parse_iso8601(until)
    support_total_cents = 0
    counted_event_count = 0
    ignored_event_count = 0

    for node in iter_activity_nodes(payload):
        action = str(node.get("action", ""))
        occurred_at = event_time(node)
        tier = tier_object(node)
        amount_cents = tier_amount_cents(tier)
        one_time = tier_is_one_time(tier, node)

        if action and action not in ACTION_ALLOWLIST:
            ignored_event_count += 1
            continue
        if occurred_at is None or occurred_at < since_dt or occurred_at >= until_dt:
            ignored_event_count += 1
            continue
        if not one_time:
            ignored_event_count += 1
            continue
        if amount_cents <= 0:
            ignored_event_count += 1
            continue

        support_total_cents += amount_cents
        counted_event_count += 1

    return {
        "schema_version": "support-unlock.v1",
        "week_id": week_id,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": source,
        "window": {
            "since": since_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
            "until": until_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
        },
        "thresholds": {
            "rank_2_cents": RANK_2_THRESHOLD_CENTS,
            "rank_3_cents": RANK_3_THRESHOLD_CENTS,
        },
        "support_total_cents": support_total_cents,
        "support_total_usd": round(support_total_cents / 100, 2),
        "counted_event_count": counted_event_count,
        "ignored_event_count": ignored_event_count,
        "rank_2_unlocked": support_total_cents >= RANK_2_THRESHOLD_CENTS,
        "rank_3_unlocked": support_total_cents >= RANK_3_THRESHOLD_CENTS,
        "privacy": {
            "sponsor_identity_included": False,
            "raw_sponsor_logins_included": False,
            "raw_sponsor_emails_included": False,
            "event_level_amounts_included": False,
        },
    }


def validate_public_unlock(payload: dict[str, Any]) -> None:
    if contains_identity_key(payload):
        raise SystemExit("Support unlock output must not contain sponsor identity keys")
    total = int(payload.get("support_total_cents", -1))
    thresholds = payload.get("thresholds") or {}
    if payload.get("rank_2_unlocked") != (total >= int(thresholds.get("rank_2_cents", RANK_2_THRESHOLD_CENTS))):
        raise SystemExit("rank_2_unlocked does not match the configured threshold")
    if payload.get("rank_3_unlocked") != (total >= int(thresholds.get("rank_3_cents", RANK_3_THRESHOLD_CENTS))):
        raise SystemExit("rank_3_unlocked does not match the configured threshold")


def write_outputs(unlock: dict[str, Any], out_dir: str, week_id: str) -> None:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    json_path = out_path / f"{week_id}.json"
    json_path.write_text(json.dumps(unlock, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="GraphQL sponsorship activity JSON")
    parser.add_argument("--week-id", required=True)
    parser.add_argument("--since", required=True)
    parser.add_argument("--until", required=True)
    parser.add_argument("--source", default="github-sponsors-graphql")
    parser.add_argument("--out-dir", default="data/support-unlocks")
    args = parser.parse_args()

    unlock = build_unlocks(load_json(args.input), args.week_id, args.since, args.until, args.source)
    validate_public_unlock(unlock)
    write_outputs(unlock, args.out_dir, args.week_id)
    print(f"support unlocks written: {args.out_dir}/{args.week_id}.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
