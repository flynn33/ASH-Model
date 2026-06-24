import importlib.util
from pathlib import Path

from ash_model.prediction_ledger import (
    canonical_prediction_hash,
    ledger_lock_status,
    validate_prediction_ledger,
)


def _frozen_entry():
    return {
        "id": "PRED-EXAMPLE-001",
        "model_version": "ash-physics-v0.2",
        "commit": "0123456789abcdef",
        "frozen_utc": "2026-06-24T12:00:00Z",
        "observable": "example_length",
        "prediction": {"value": 14.5, "unit": "m"},
        "uncertainty": {"standard_deviation": 0.2, "unit": "m"},
        "data_product": "example-held-out-data-product",
        "statistic": "diagonal_gaussian_log_likelihood",
        "rejection_rule": "reject if chi_square exceeds preregistered threshold",
        "test_status": "frozen",
        "artifact_hashes": {
            "proofs/computational-certificate.json": "a" * 64,
        },
    }


def test_canonical_prediction_hash_is_independent_of_key_order_and_existing_hash():
    entry = _frozen_entry()
    first = canonical_prediction_hash(entry)

    shuffled = dict(reversed(list(entry.items())))
    shuffled["entry_hash"] = "0" * 64
    second = canonical_prediction_hash(shuffled)

    assert len(first) == 64
    assert first == second


def test_validate_prediction_ledger_accepts_matching_locked_entry_hash():
    entry = _frozen_entry()
    entry["entry_hash"] = canonical_prediction_hash(entry)
    ledger = {
        "schema_version": "1.0",
        "model_version": "ash-physics-v0.2",
        "status": "has_locked_predictions",
        "entries": [entry],
    }

    assert validate_prediction_ledger(ledger) == ()
    assert ledger_lock_status(ledger["entries"]) == "has_locked_predictions"


def test_validate_prediction_ledger_rejects_mismatched_locked_entry_hash():
    entry = _frozen_entry()
    entry["entry_hash"] = "0" * 64
    ledger = {
        "schema_version": "1.0",
        "model_version": "ash-physics-v0.2",
        "status": "has_locked_predictions",
        "entries": [entry],
    }

    failures = validate_prediction_ledger(ledger)

    assert failures == ("entries/0/entry_hash does not match canonical entry hash",)


def test_validate_prediction_ledger_requires_entries_for_locked_status():
    ledger = {
        "schema_version": "1.0",
        "model_version": "ash-physics-v0.2",
        "status": "has_locked_predictions",
        "entries": [],
    }

    assert validate_prediction_ledger(ledger) == (
        "entries must be non-empty when status is has_locked_predictions",
    )


def test_repository_gate_uses_prediction_lock_validation(tmp_path):
    root = Path(__file__).resolve().parents[1]
    gate_path = root / "docs/ash-physics-validation/scripts/run_repository_gate.py"
    spec = importlib.util.spec_from_file_location("ash_repository_gate", gate_path)
    assert spec is not None and spec.loader is not None
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)

    entry = _frozen_entry()
    entry["entry_hash"] = "0" * 64
    ledger = {
        "schema_version": "1.0",
        "model_version": "ash-physics-v0.2",
        "status": "has_locked_predictions",
        "entries": [entry],
    }

    failures = gate.validate_prediction_ledger(tmp_path / "prediction-ledger.json", ledger)

    ledger_path = tmp_path / "prediction-ledger.json"
    assert failures == [
        f"{ledger_path}: entries/0/entry_hash does not match canonical entry hash",
    ]
