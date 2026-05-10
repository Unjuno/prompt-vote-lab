#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUPPORT_DIR = ROOT / "data" / "support-unlocks"

REQUIRED_KEYS = {
    "schema_version",
    "week_id",
    "generated_at",
    "source",
    "window",
    "thresholds",
    "support_total_cents",
    "support_total_usd",
    "counted_event_count",
    "ignored_event_count",
    "rank_2_unlocked",
    "rank_3_unlocked",
    "privacy",
}

PRIVACY_FLAGS = {
    "sponsor_identity_included",
    "raw_sponsor_logins_included",
    "raw_sponsor_emails_included",
    "event_level_amounts_included",
}

FORBIDDEN_KEYS = {
    "sponsor",
    "sponsors",
    "sponsorable",
    "sponsorEntity",
    "sponsor_login",
    "sponsorLogin",
    "login",
    "email",
    "name",
    "user",
    "account",
}

FORBIDDEN_STRING_VALUE_FRAGMENTS = [
    "@",
    "private-sponsor",
    "sponsor_login",
    "sponsorLogin",
]


def contains_forbidden_key(value: Any) -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_KEYS:
                return key
            nested = contains_forbidden_key(child)
            if nested:
                return nested
    if isinstance(value, list):
        for child in value:
            nested = contains_forbidden_key(child)
            if nested:
                return nested
    return None


def contains_forbidden_string_value(value: Any) -> str | None:
    if isinstance(value, str):
        for fragment in FORBIDDEN_STRING_VALUE_FRAGMENTS:
            if fragment in value:
                return fragment
    if isinstance(value, dict):
        for child in value.values():
            nested = contains_forbidden_string_value(child)
            if nested:
                return nested
    if isinstance(value, list):
        for child in value:
            nested = contains_forbidden_string_value(child)
            if nested:
                return nested
    return None


def validate_unlock(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: support unlock JSON must be an object")

    missing = sorted(REQUIRED_KEYS - set(data))
    if missing:
        raise SystemExit(f"{path}: missing required keys: {missing}")

    extra = sorted(set(data) - REQUIRED_KEYS)
    if extra:
        raise SystemExit(f"{path}: unexpected public keys: {extra}")

    forbidden_key = contains_forbidden_key(data)
    if forbidden_key:
        raise SystemExit(f"{path}: forbidden identity key found: {forbidden_key}")

    leaked_fragment = contains_forbidden_string_value(data)
    if leaked_fragment:
        raise SystemExit(f"{path}: forbidden string value fragment found: {leaked_fragment}")

    if data["schema_version"] != "support-unlock.v1":
        raise SystemExit(f"{path}: unexpected schema_version")

    thresholds = data["thresholds"]
    if not isinstance(thresholds, dict):
        raise SystemExit(f"{path}: thresholds must be an object")
    for key in ("rank_2_cents", "rank_3_cents"):
        if not isinstance(thresholds.get(key), int) or thresholds[key] < 0:
            raise SystemExit(f"{path}: invalid threshold {key}")

    total_cents = data["support_total_cents"]
    total_usd = data["support_total_usd"]
    if not isinstance(total_cents, int) or total_cents < 0:
        raise SystemExit(f"{path}: support_total_cents must be a non-negative integer")
    if not isinstance(total_usd, (int, float)) or total_usd < 0:
        raise SystemExit(f"{path}: support_total_usd must be a non-negative number")
    if round(total_cents / 100, 2) != round(float(total_usd), 2):
        raise SystemExit(f"{path}: support_total_usd does not match support_total_cents")

    if data["rank_2_unlocked"] != (total_cents >= thresholds["rank_2_cents"]):
        raise SystemExit(f"{path}: rank_2_unlocked does not match threshold")
    if data["rank_3_unlocked"] != (total_cents >= thresholds["rank_3_cents"]):
        raise SystemExit(f"{path}: rank_3_unlocked does not match threshold")

    for key in ("counted_event_count", "ignored_event_count"):
        if not isinstance(data[key], int) or data[key] < 0:
            raise SystemExit(f"{path}: {key} must be a non-negative integer")

    window = data["window"]
    if not isinstance(window, dict) or set(window) != {"since", "until"}:
        raise SystemExit(f"{path}: window must contain only since/until")

    privacy = data["privacy"]
    if not isinstance(privacy, dict):
        raise SystemExit(f"{path}: privacy must be an object")
    if set(privacy) != PRIVACY_FLAGS:
        raise SystemExit(f"{path}: privacy flags mismatch")
    for key in PRIVACY_FLAGS:
        if privacy[key] is not False:
            raise SystemExit(f"{path}: privacy flag {key} must be false")


def main() -> int:
    if not SUPPORT_DIR.exists():
        print("No public support unlock files found.")
        return 0

    files = sorted(SUPPORT_DIR.glob("*.json"))
    for path in files:
        validate_unlock(path)

    print(f"public support unlock file validation passed: {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
