"""R-015 locked prospective prediction utilities for ASH.

This module implements repository-side validation for the R-015 lock package:
three immutable prospective/held-out prediction entries, hash-locked CSV
vectors, and falsification metadata.

Scientific boundary:
    The functions here validate finite/synthetic lock artifacts only. They do
    not analyze external cosmological data and do not claim empirical support
    for ASH cosmology.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import csv


LOCK_SCHEMA = "ash.r015.locked_prediction_ledger.v1"
LOCKED_PREDICTION_IDS = ("ASH-R015-P001", "ASH-R015-P002", "ASH-R015-P003")


@dataclass(frozen=True)
class LockedFileHash:
    """A path/hash pair for an immutable locked artifact."""

    path: str
    sha256: str


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 digest for a file."""

    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def repository_paths(repo_root: str | Path) -> dict[str, Path]:
    """Return canonical R-015 repository paths rooted at ``repo_root``."""

    root = Path(repo_root)
    return {
        "ledger": root / "predictions/locked/r015_prediction_ledger.locked.json",
        "certificate": root / "predictions/locked/r015_lock_certificate.json",
        "data_dir": root / "data/ash-cosmology/locked-predictions/v0.1",
        "validation": root
        / "validation/locked-predictions/roadmap-015/outputs/verification.json",
    }


def load_locked_ledger(repo_root: str | Path) -> dict[str, Any]:
    """Load the immutable R-015 prediction ledger."""

    path = repository_paths(repo_root)["ledger"]
    return json.loads(path.read_text(encoding="utf-8"))


def load_lock_certificate(repo_root: str | Path) -> dict[str, Any]:
    """Load the R-015 lock certificate."""

    path = repository_paths(repo_root)["certificate"]
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return sum(1 for _ in reader)


def validate_prediction_ledger(ledger: dict[str, Any]) -> list[str]:
    """Return ledger schema/metadata validation errors."""

    errors: list[str] = []
    if ledger.get("schema") != LOCK_SCHEMA:
        errors.append(f"unexpected schema: {ledger.get('schema')!r}")
    if ledger.get("roadmap_item") != "R-015 Locked prospective or held-out scientific predictions":
        errors.append("roadmap_item does not identify R-015")
    if not ledger.get("freeze_date"):
        errors.append("freeze_date is missing")
    if ledger.get("timezone") != "America/Chicago":
        errors.append("timezone must be America/Chicago for this lock")

    predictions = ledger.get("predictions")
    if not isinstance(predictions, list):
        errors.append("predictions must be a list")
        return errors

    ids = [p.get("prediction_id") for p in predictions if isinstance(p, dict)]
    if tuple(ids) != LOCKED_PREDICTION_IDS:
        errors.append(f"prediction IDs must be exactly {LOCKED_PREDICTION_IDS!r}")

    for pred in predictions:
        if not isinstance(pred, dict):
            errors.append("prediction entry is not an object")
            continue
        pid = pred.get("prediction_id", "<missing>")
        for key in ("title", "observable", "domain", "locked_numeric_claim", "falsification_rule", "held_out_data_classes"):
            if key not in pred:
                errors.append(f"{pid}: missing {key}")
        if not pred.get("falsification_rule"):
            errors.append(f"{pid}: falsification_rule is empty")
        if not pred.get("held_out_data_classes"):
            errors.append(f"{pid}: held_out_data_classes is empty")
    if "mutation_policy" not in ledger:
        errors.append("mutation_policy is missing")
    return errors


def verify_lock(repo_root: str | Path) -> dict[str, Any]:
    """Verify ledger and locked CSV hashes against the certificate."""

    paths = repository_paths(repo_root)
    ledger = load_locked_ledger(repo_root)
    certificate = load_lock_certificate(repo_root)
    ledger_hash = sha256_file(paths["ledger"])
    ledger_errors = validate_prediction_ledger(ledger)

    file_results: dict[str, dict[str, Any]] = {}
    for filename, expected_hash in sorted(certificate.get("locked_files", {}).items()):
        path = paths["data_dir"] / filename
        exists = path.exists()
        actual_hash = sha256_file(path) if exists else None
        file_results[filename] = {
            "exists": exists,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "matches": exists and actual_hash == expected_hash,
            "rows": _csv_row_count(path) if exists else 0,
        }

    return {
        "schema": LOCK_SCHEMA,
        "roadmap_item": ledger.get("roadmap_item"),
        "freeze_date": ledger.get("freeze_date"),
        "prediction_ids": [p.get("prediction_id") for p in ledger.get("predictions", [])],
        "locked_prediction_count": len(ledger.get("predictions", [])),
        "ledger_sha256_expected": certificate.get("ledger_sha256"),
        "ledger_sha256_actual": ledger_hash,
        "ledger_hash_matches": ledger_hash == certificate.get("ledger_sha256"),
        "locked_files": file_results,
        "all_locked_files_match": all(result["matches"] for result in file_results.values()),
        "ledger_errors": ledger_errors,
        "passed": ledger_hash == certificate.get("ledger_sha256")
        and all(result["matches"] for result in file_results.values())
        and not ledger_errors,
        "scientific_boundary": (
            "R-015 validates lock mechanics and immutable synthetic prediction "
            "templates only; it does not analyze external data or validate empirical cosmology."
        ),
    }


def write_verification(repo_root: str | Path) -> dict[str, Any]:
    """Write the R-015 verification JSON and return its content."""

    paths = repository_paths(repo_root)
    result = verify_lock(repo_root)
    paths["validation"].parent.mkdir(parents=True, exist_ok=True)
    paths["validation"].write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result
