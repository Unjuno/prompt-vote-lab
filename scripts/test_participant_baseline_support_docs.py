#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTICIPANT = ROOT / "docs" / "for-participants.md"
HOW_TO = ROOT / "docs" / "how-to-participate.md"
BASELINE = ROOT / "docs" / "no-change-baseline.md"
SUPPORT = ROOT / "docs" / "support-policy.md"

SHARED_REQUIRED_TEXT = [
    "no-change baseline",
    "20",
    "rank 1",
    "rank 2",
    "rank 3",
]

PARTICIPANT_REQUIRED_TEXT = [
    "baseline ranks first -> no implementation candidates",
    "real prompt ranks first -> baseline passed -> rank 1 is eligible",
    "5 USD weekly support -> rank 2 can also be attempted",
    "10 USD weekly support -> rank 2 and rank 3 can also be attempted",
    "Rank 2 and rank 3 do not independently need 20+ votes after rank 1 beats the baseline.",
    "Support does not help if the baseline ranks first.",
    "Support increases comparison capacity. It does not override the no-change baseline.",
    "Can rank 2 or rank 3 run without 20 votes?",
    "If the baseline ranks first, support unlocks nothing.",
]

HOW_TO_REQUIRED_TEXT = [
    "beat the 20-vote no-change baseline as a candidate set",
    "receive one bounded agent attempt, or support-unlocked comparison attempts",
    "Baseline passing is a candidate-set rule:",
    "no-change baseline ranks first -> no implementation candidates",
    "real prompt ranks first -> rank 1 is eligible",
    "5 USD weekly support -> rank 2 may also receive a bounded attempt",
    "10 USD weekly support -> rank 2 and rank 3 may also receive bounded attempts",
    "Rank 2 and rank 3 do not independently need 20+ votes after rank 1 beats the baseline.",
    "Support does not override a baseline win.",
]

BASELINE_REQUIRED_TEXT = [
    "Baseline passing is decided by the weekly candidate set after the baseline is inserted and candidates are sorted by votes:",
    "no-change baseline ranks first -> no implementation candidates",
    "real prompt ranks first -> baseline passed -> rank 1 is eligible",
    "Support only opens additional comparison runs among real prompt candidates after the weekly candidate set has passed the baseline rule.",
    "baseline ranks first -> support unlocks nothing",
    "real prompt ranks first and support is 0 USD -> rank 1 only",
    "real prompt ranks first and support is at least 5 USD -> rank 1 and rank 2",
    "real prompt ranks first and support is at least 10 USD -> rank 1, rank 2, and rank 3",
    "Rank 2 and rank 3 do not independently need 20+ votes after rank 1 beats the baseline.",
    "Issue #1 | 25 | rank 1, normal weekly candidate",
    "Issue #2 | 12 | rank 2, support-unlocked at 5 USD",
    "Issue #3 | 8 | rank 3, support-unlocked at 10 USD",
    "No change baseline | 20 | wins",
    "No implementation PR is created.",
]

SUPPORT_REQUIRED_TEXT = [
    "Rank 2 and rank 3 do not independently need to exceed 20 votes after the candidate set has passed the baseline rule.",
    "Support unlocks additional comparison runs only after the prompt candidate set beats the no-change baseline.",
]

FORBIDDEN_TEXT = [
    "Rank 2 and rank 3 must independently exceed 20 votes",
    "rank 2 must independently exceed 20 votes",
    "rank 3 must independently exceed 20 votes",
    "Support overrides the no-change baseline",
    "Support buys an implementation run when the baseline wins",
    "If no real prompt beats 20, support can still unlock rank 2",
]


def require_all(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing {label} text: {missing}")


def reject_all(text: str, forbidden: list[str], label: str) -> None:
    lowered = text.lower()
    found = [item for item in forbidden if item.lower() in lowered]
    if found:
        raise SystemExit(f"Forbidden {label} text found: {found}")


def main() -> int:
    participant = PARTICIPANT.read_text(encoding="utf-8")
    how_to = HOW_TO.read_text(encoding="utf-8")
    baseline = BASELINE.read_text(encoding="utf-8")
    support = SUPPORT.read_text(encoding="utf-8")
    combined = "\n".join([participant, how_to, baseline, support])

    for label, text in [
        ("participant guide", participant),
        ("how-to-participate", how_to),
        ("no-change baseline", baseline),
    ]:
        require_all(text, SHARED_REQUIRED_TEXT, label)

    require_all(participant, PARTICIPANT_REQUIRED_TEXT, "participant guide")
    require_all(how_to, HOW_TO_REQUIRED_TEXT, "how-to-participate")
    require_all(baseline, BASELINE_REQUIRED_TEXT, "no-change baseline")
    require_all(support, SUPPORT_REQUIRED_TEXT, "support policy")
    reject_all(combined, FORBIDDEN_TEXT, "participant-facing baseline/support docs")

    if participant.index("Why voting matters") > participant.index("What support can and cannot do"):
        raise SystemExit("participant guide should define voting and baseline before support")

    if how_to.index("Beat the no-change baseline") > how_to.index("Review outcomes"):
        raise SystemExit("how-to should define baseline before outcome review")

    if baseline.index("## Rule") > baseline.index("## Support interaction"):
        raise SystemExit("baseline rule should appear before support interaction")

    print("participant baseline support docs test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
