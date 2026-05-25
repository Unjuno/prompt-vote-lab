#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "script-check.yml"
PAGES_SMOKE_WORKFLOW = ROOT / ".github" / "workflows" / "pages-smoke-check.yml"
PAGES_SMOKE_SCRIPT = ROOT / "scripts" / "pages-smoke-check.py"
INDEX = ROOT / "index.html"
LAB_INDEX = ROOT / "lab" / "index.html"

REQUIRED_TEXT = [
    "name: Script Check",
    "pull_request:",
    "paths:",
    "lab/comparisons/**",
    "runs/**",
    "docs/canonical-runner-evidence-guide.md",
    "docs/canonical-status-drift-check.md",
    "docs/repository-5s-and-language-policy.md",
    "docs/repository-cleanup-inventory.md",
    "docs/workflow-family-map.md",
    "docs/canary-archive-inventory.md",
    "docs/local-release-verification.md",
    "docs/README.md",
    "docs/operator-runbook.md",
    "docs/weekly-automation.md",
    "docs/for-participants.md",
    "docs/how-to-participate.md",
    "docs/no-change-baseline.md",
    ".github/workflows/codex-selected-prompt-run.yml",
    "workflow_dispatch:",
    "contents: read",
    "Run actionlint",
    "raven-actions/actionlint@v2",
    "Run current Codex path doc test",
    "python scripts/test_current_codex_path_doc.py",
    "Run canonical runner evidence guide test",
    "python scripts/test_canonical_runner_evidence_guide.py",
    "Run canonical status drift test",
    "python scripts/test_canonical_status_drift.py",
    "Run repository language policy test",
    "python scripts/test_repository_language_policy.py",
    "Run repository cleanup inventory test",
    "python scripts/test_repository_cleanup_inventory.py",
    "Run workflow family map test",
    "python scripts/test_workflow_family_map.py",
    "Run canary archive inventory test",
    "python scripts/test_canary_archive_inventory.py",
    "Run local release verification test",
    "python scripts/test_local_release_verification.py",
    "Run OpenAI lab runner legacy contract test",
    "python scripts/test_openai_lab_run_legacy_contract.py",
    "Run weekly operator docs test",
    "python scripts/test_weekly_operator_docs.py",
    "Run participant baseline support docs test",
    "python scripts/test_participant_baseline_support_docs.py",
    "Run comparison dashboard builder test",
    "python scripts/test_build_comparison_dashboard.py",
    "Run comparison dashboard decision test",
    "python scripts/test_comparison_dashboard_decision.py",
    "Run generated comparison dashboard test",
    "python scripts/test_generated_comparison_dashboards.py",
    "Run public results export workflow contract test",
    "python scripts/test_public_results_export_workflow_contract.py",
    "Run script-check workflow contract test",
    "python scripts/test_script_check_workflow_contract.py",
    "Run public agent run bundle verifier test",
    "python scripts/test_verify_public_agent_run_bundle.py",
    "Run policy agent public bundle contract test",
    "python scripts/test_policy_agent_public_bundle_contract.py",
    "Run task packet runner contract test",
    "python scripts/test_task_packet_runner_contract.py",
    "Run selected prompt runner contract test",
    "python scripts/test_selected_prompt_runner_contract.py",
    "Run selected prompt workflow contract test",
    "python scripts/test_selected_prompt_workflow_contract.py",
    "Run weekly auto-run workflow contract test",
    "python scripts/test_weekly_auto_run_workflow_contract.py",
    "Run fixed Issue instruction packet generator test",
    "python scripts/test_create_codex_issue_instruction_packet.py",
    "Run lab PR scope guard self-test",
    "bash scripts/test-lab-pr-scope.sh",
]

PAGES_SMOKE_REQUIRED_TEXT = [
    "ROOT_EXPECTED_TEXT",
    "LAB_EXPECTED_TEXT",
    "20-vote baseline",
    "require_all(base + \"/\", ROOT_EXPECTED_TEXT)",
    "require_all(base + \"/lab/\", LAB_EXPECTED_TEXT)",
]

PAGES_SMOKE_WORKFLOW_REQUIRED_TEXT = [
    "name: GitHub Pages Smoke Check",
    "python scripts/pages-smoke-check.py --base-url \"https://unjuno.github.io/prompt-vote-lab\"",
]

FORBIDDEN_TEXT = [
    "contents: write",
    "pull-requests: write",
    "issues: write",
    "secrets.OPENAI",
    "OPENAI_API_KEY",
    "codex exec",
    "gh pr merge",
]

PAGES_SMOKE_FORBIDDEN_TEXT = [
    "20 virtual votes",
]


def require_all(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing script-check workflow text: {missing}")


def reject_all(text: str, forbidden: list[str]) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden script-check workflow text found: {found}")


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    pages_smoke_workflow = PAGES_SMOKE_WORKFLOW.read_text(encoding="utf-8")
    pages_smoke_script = PAGES_SMOKE_SCRIPT.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    lab_index = LAB_INDEX.read_text(encoding="utf-8")

    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)

    require_all(pages_smoke_workflow, PAGES_SMOKE_WORKFLOW_REQUIRED_TEXT)
    require_all(pages_smoke_script, PAGES_SMOKE_REQUIRED_TEXT)
    require_all(index, ["Prompt Vote Lab", "20-vote baseline"])
    require_all(lab_index, ["Prompt Vote Lab"])
    reject_all(pages_smoke_workflow, PAGES_SMOKE_FORBIDDEN_TEXT)
    reject_all(pages_smoke_script, PAGES_SMOKE_FORBIDDEN_TEXT)
    reject_all(index, PAGES_SMOKE_FORBIDDEN_TEXT)

    if text.index("Checkout") > text.index("Run actionlint"):
        raise SystemExit("actionlint should run after checkout")

    if text.index("Run actionlint") > text.index("Setup Node"):
        raise SystemExit("actionlint should run before language-specific script checks")

    if text.index("lab/comparisons/**") > text.index("runs/**"):
        raise SystemExit("runs/** should be tracked near generated/evidence paths")

    if text.index("docs/current-codex-implementation-path.md") > text.index("docs/canonical-runner-evidence-guide.md"):
        raise SystemExit("canonical runner evidence guide should be tracked near current Codex path docs")

    if text.index("docs/canonical-runner-evidence-guide.md") > text.index("docs/canonical-status-drift-check.md"):
        raise SystemExit("canonical status drift check should be tracked after the canonical runner evidence guide")

    if text.index("docs/canonical-status-drift-check.md") > text.index("docs/repository-5s-and-language-policy.md"):
        raise SystemExit("repository 5S language policy should be tracked after the canonical status drift check")

    if text.index("docs/repository-5s-and-language-policy.md") > text.index("docs/repository-cleanup-inventory.md"):
        raise SystemExit("repository cleanup inventory should be tracked after the repository 5S language policy")

    if text.index("docs/repository-cleanup-inventory.md") > text.index("docs/workflow-family-map.md"):
        raise SystemExit("workflow family map should be tracked after the repository cleanup inventory")

    if text.index("docs/workflow-family-map.md") > text.index("docs/canary-archive-inventory.md"):
        raise SystemExit("canary archive inventory should be tracked after the workflow family map")

    if text.index("docs/canary-archive-inventory.md") > text.index("docs/local-release-verification.md"):
        raise SystemExit("local release verification should be tracked after the canary archive inventory")

    if text.index("docs/local-release-verification.md") > text.index("docs/README.md"):
        raise SystemExit("docs README should be tracked after local release verification")

    if text.index("docs/local-release-verification.md") > text.index("docs/operator-runbook.md"):
        raise SystemExit("operator runbook should be tracked after local release verification")

    if text.index("docs/operator-runbook.md") > text.index("docs/weekly-automation.md"):
        raise SystemExit("weekly automation doc should be tracked after the operator runbook")

    if text.index("docs/weekly-automation.md") > text.index("docs/for-participants.md"):
        raise SystemExit("participant-facing docs should be tracked after weekly automation")

    if text.index("docs/for-participants.md") > text.index("docs/how-to-participate.md"):
        raise SystemExit("how-to-participate should be tracked after participant guide")

    if text.index("docs/how-to-participate.md") > text.index("docs/no-change-baseline.md"):
        raise SystemExit("no-change baseline should be tracked after how-to-participate")

    if text.index("Run current Codex path doc test") > text.index("Run canonical runner evidence guide test"):
        raise SystemExit("Canonical runner evidence guide test should run after the current Codex path doc test")

    if text.index("Run canonical runner evidence guide test") > text.index("Run canonical status drift test"):
        raise SystemExit("Canonical status drift test should run after the canonical runner evidence guide test")

    if text.index("Run canonical status drift test") > text.index("Run repository language policy test"):
        raise SystemExit("Repository language policy test should run after the canonical status drift test")

    if text.index("Run repository language policy test") > text.index("Run repository cleanup inventory test"):
        raise SystemExit("Repository cleanup inventory test should run after the repository language policy test")

    if text.index("Run repository cleanup inventory test") > text.index("Run workflow family map test"):
        raise SystemExit("Workflow family map test should run after the repository cleanup inventory test")

    if text.index("Run workflow family map test") > text.index("Run canary archive inventory test"):
        raise SystemExit("Canary archive inventory test should run after the workflow family map test")

    if text.index("Run canary archive inventory test") > text.index("Run local release verification test"):
        raise SystemExit("Local release verification test should run after the canary archive inventory test")

    if text.index("Run local release verification test") > text.index("Run OpenAI lab runner legacy contract test"):
        raise SystemExit("OpenAI lab runner legacy contract test should run after the local release verification test")

    if text.index("Run OpenAI lab runner legacy contract test") > text.index("Run weekly operator docs test"):
        raise SystemExit("Weekly operator docs test should run after the OpenAI lab runner legacy contract test")

    if text.index("Run weekly operator docs test") > text.index("Run participant baseline support docs test"):
        raise SystemExit("Participant baseline support docs test should run after the weekly operator docs test")

    if text.index("Run participant baseline support docs test") > text.index("Run usable experiment ops doc test"):
        raise SystemExit("Usable experiment ops doc test should run after the participant baseline support docs test")

    if text.index("Run public agent run bundle enrichment test") > text.index("Run public agent run bundle verifier test"):
        raise SystemExit("Public bundle verifier test should run after enrichment test")

    if text.index("Run public agent run bundle verifier test") > text.index("Run policy agent public bundle contract test"):
        raise SystemExit("Policy agent public bundle contract test should run after verifier test")

    if text.index("Run task packet runner contract test") > text.index("Run selected prompt runner contract test"):
        raise SystemExit("Selected prompt runner contract test should run after task packet runner contract test")

    if text.index("Run selected prompt runner contract test") > text.index("Run selected prompt workflow contract test"):
        raise SystemExit("Selected prompt workflow contract test should run after selected prompt runner contract test")

    if text.index("Run selected prompt workflow contract test") > text.index("Run weekly auto-run workflow contract test"):
        raise SystemExit("Weekly auto-run workflow contract test should run after selected prompt workflow contract test")

    if text.index("Run weekly auto-run workflow contract test") > text.index("Run fixed Issue instruction packet generator test"):
        raise SystemExit("Fixed Issue generator test should run after weekly auto-run workflow contract test")

    if text.index("Run comparison dashboard builder test") > text.index("Run comparison dashboard decision test"):
        raise SystemExit("Comparison dashboard decision test should run after the builder test")

    if text.index("Run comparison dashboard decision test") > text.index("Run generated comparison dashboard test"):
        raise SystemExit("Generated comparison dashboard test should run after the decision test")

    if text.index("Run generated comparison dashboard test") > text.index("Run weekly Issue finalizer test"):
        raise SystemExit("Generated dashboard test should run before later weekly finalizer tests")

    print("script-check workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
