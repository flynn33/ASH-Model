#!/usr/bin/env python3
"""Repository-readiness gate for final ASH repository handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_PATHS = [
    "README.md",
    "src/ash_model/physics.py",
    "src/ash_model/cosmology.py",
    "src/ash_model/empirical.py",
    "theory/microscopic-state-and-dynamics.md",
    "theory/coarse-graining-and-bridge-map.md",
    "theory/cosmological-background.md",
    "theory/linear-perturbations.md",
    "theory/continuum-limit.md",
    "validation/status.json",
    "predictions/prediction-ledger.json",
    "docs/ash-physics-validation/scripts/check_claim_language.py",
    "docs/ash-physics-validation/scripts/check_sensitive_language.py",
    "docs/ash-physics-validation/scripts/run_repository_gate.py",
    ".github/workflows/ai-contributor-check.yml",
]

SCIENCE_BLOCKER_PHRASES = [
    "No reviewed physical calibration constants",
    "No metric, light-cone, or relativistic spacetime interpretation",
    "No unit-bearing bridge",
    "No ASH-derived standard cosmological background",
    "No external data product",
    "No scientific prospective or held-out prediction",
]

FORBIDDEN_COMPLETION_WITHOUT_EVIDENCE = {
    "empirical cosmology",
    "observational confirmation",
    "observed spacetime dynamics",
    "physical cosmological background equations",
    "metric perturbations",
    "cosmic power spectrum",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_status(root: Path, failures: list[str]) -> None:
    status_path = root / "validation/status.json"
    if not status_path.exists():
        return

    status = load_json(status_path)
    blockers = status.get("open_blockers", [])
    if not isinstance(blockers, list) or not blockers:
        failures.append("validation/status.json must contain non-empty open_blockers")
    blocker_text = "\n".join(str(item) for item in blockers)
    for phrase in SCIENCE_BLOCKER_PHRASES:
        if phrase not in blocker_text:
            failures.append(f"validation/status.json open_blockers missing: {phrase}")

    for task in status.get("tasks", []):
        if not isinstance(task, dict):
            continue
        notes = str(task.get("notes", "")).lower()
        completion_type = task.get("completion_type")
        if completion_type == "empirical_gate_passed":
            failures.append(
                f"task {task.get('id')} uses empirical_gate_passed without a locked external empirical gate"
            )
        if task.get("status") != "complete":
            continue
        for phrase in FORBIDDEN_COMPLETION_WITHOUT_EVIDENCE:
            if (
                phrase in notes
                and "outside proved scope" not in notes
                and "blocked" not in notes
                and "not present" not in notes
                and "not empirical" not in notes
            ):
                failures.append(f"task {task.get('id')} may overclaim science completion: {phrase}")


def validate_prediction_ledger(root: Path, failures: list[str]) -> None:
    ledger_path = root / "predictions/prediction-ledger.json"
    if not ledger_path.exists():
        return
    ledger = load_json(ledger_path)
    status = ledger.get("status")
    entries = ledger.get("entries", [])
    if status == "no_locked_predictions" and entries:
        failures.append("prediction ledger cannot have entries when status is no_locked_predictions")
    if status != "no_locked_predictions" and not entries:
        failures.append("prediction ledger status implies predictions, but entries are empty")


def validate_readme(root: Path, failures: list[str]) -> None:
    readme_path = root / "README.md"
    if not readme_path.exists():
        return
    readme = " ".join(readme_path.read_text(encoding="utf-8").lower().split())
    if "not a claim of observed spacetime dynamics or empirical cosmology" not in readme:
        failures.append("README should preserve finite-observer scientific boundary language")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (root / relative).exists():
            failures.append(f"missing required path: {relative}")

    validate_status(root, failures)
    validate_prediction_ledger(root, failures)
    validate_readme(root, failures)

    if failures:
        for failure in failures:
            print(failure)
        return 1

    print("live repository readiness audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
