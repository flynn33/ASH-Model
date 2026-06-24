"""Prediction ledger locking and validation utilities."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
LEDGER_STATUSES = {
    "no_locked_predictions",
    "has_locked_predictions",
    "testing_in_progress",
    "archived",
}
ENTRY_STATUSES = {"frozen", "tested_pass", "tested_fail", "withdrawn_before_test"}
ENTRY_REQUIRED = {
    "id",
    "model_version",
    "commit",
    "frozen_utc",
    "observable",
    "prediction",
    "uncertainty",
    "data_product",
    "statistic",
    "rejection_rule",
    "test_status",
}
ENTRY_ALLOWED = ENTRY_REQUIRED | {"artifact_hashes", "entry_hash", "notes"}


def canonical_prediction_hash(entry: Mapping[str, Any]) -> str:
    """Return the deterministic SHA-256 digest for a prediction entry."""

    payload = dict(entry)
    payload.pop("entry_hash", None)
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def ledger_lock_status(entries: Sequence[Mapping[str, Any]]) -> str:
    """Return the ledger status implied by the entry list."""

    return "has_locked_predictions" if entries else "no_locked_predictions"


def _validate_string(value: Any, label: str, failures: list[str]) -> None:
    if not isinstance(value, str) or not value:
        failures.append(f"{label} must be a non-empty string")


def _validate_entry(index: int, entry: Any, failures: list[str]) -> None:
    label = f"entries/{index}"
    if not isinstance(entry, dict):
        failures.append(f"{label} must be an object")
        return
    missing = sorted(ENTRY_REQUIRED - set(entry))
    unexpected = sorted(set(entry) - ENTRY_ALLOWED)
    failures.extend(f"{label} missing required property {key}" for key in missing)
    failures.extend(f"{label} has unexpected property {key}" for key in unexpected)
    for key in (
        "id",
        "model_version",
        "commit",
        "frozen_utc",
        "observable",
        "data_product",
        "statistic",
        "rejection_rule",
    ):
        if key in entry:
            _validate_string(entry[key], f"{label}/{key}", failures)
    if entry.get("test_status") not in ENTRY_STATUSES:
        failures.append(f"{label}/test_status has unsupported value")
    artifact_hashes = entry.get("artifact_hashes")
    if "artifact_hashes" in entry:
        if not isinstance(artifact_hashes, dict) or not artifact_hashes:
            failures.append(f"{label}/artifact_hashes must be a non-empty object")
        else:
            for artifact, digest in artifact_hashes.items():
                _validate_string(artifact, f"{label}/artifact_hashes key", failures)
                if not isinstance(digest, str) or not HEX_SHA256.fullmatch(digest):
                    failures.append(f"{label}/artifact_hashes/{artifact} must be a SHA-256 hex digest")
    if entry.get("test_status") == "frozen" and "entry_hash" not in entry:
        failures.append(f"{label}/entry_hash is required for frozen entries")
    if "entry_hash" in entry:
        digest = entry["entry_hash"]
        if not isinstance(digest, str) or not HEX_SHA256.fullmatch(digest):
            failures.append(f"{label}/entry_hash must be a SHA-256 hex digest")
        elif digest != canonical_prediction_hash(entry):
            failures.append(f"{label}/entry_hash does not match canonical entry hash")


def validate_prediction_ledger(payload: Mapping[str, Any]) -> tuple[str, ...]:
    """Validate ledger locking consistency beyond the JSON schema checks."""

    failures: list[str] = []
    for key in ("schema_version", "model_version", "status"):
        if key in payload:
            _validate_string(payload[key], key, failures)
        else:
            failures.append(f"{key} is required")
    status = payload.get("status")
    if isinstance(status, str) and status not in LEDGER_STATUSES:
        failures.append("status has unsupported value")
    entries = payload.get("entries")
    if not isinstance(entries, list):
        failures.append("entries must be an array")
        return tuple(failures)
    if status == "no_locked_predictions" and entries:
        failures.append("entries must be empty when status is no_locked_predictions")
    if status in {"has_locked_predictions", "testing_in_progress"} and not entries:
        failures.append(f"entries must be non-empty when status is {status}")
    for index, entry in enumerate(entries):
        _validate_entry(index, entry, failures)
    return tuple(failures)
