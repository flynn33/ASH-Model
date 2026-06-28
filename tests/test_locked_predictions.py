from pathlib import Path

from ash_model.locked_predictions import (
    LOCKED_PREDICTION_IDS,
    load_locked_ledger,
    validate_prediction_ledger,
    verify_lock,
)

ROOT = Path(__file__).resolve().parents[1]


def test_r015_locked_ledger_schema_and_ids():
    ledger = load_locked_ledger(ROOT)
    assert ledger["freeze_date"] == "2026-06-26"
    assert [p["prediction_id"] for p in ledger["predictions"]] == list(LOCKED_PREDICTION_IDS)
    assert validate_prediction_ledger(ledger) == []


def test_each_prediction_has_falsification_and_held_out_classes():
    ledger = load_locked_ledger(ROOT)
    for prediction in ledger["predictions"]:
        assert prediction["falsification_rule"]
        assert prediction["held_out_data_classes"]
        assert prediction["locked_numeric_claim"]


def test_lock_certificate_hashes_match_packaged_artifacts():
    result = verify_lock(ROOT)
    assert result["ledger_hash_matches"]
    assert result["all_locked_files_match"]
    assert result["passed"]


def test_locked_csv_artifacts_are_nonempty():
    result = verify_lock(ROOT)
    rows = {name: meta["rows"] for name, meta in result["locked_files"].items()}
    assert rows["r015_locked_expansion_prediction.csv"] >= 100
    assert rows["r015_locked_matter_template.csv"] >= 100
    assert rows["r015_locked_lowell_template.csv"] >= 30


def test_boundary_statement_is_non_empirical():
    result = verify_lock(ROOT)
    boundary = result["scientific_boundary"].lower()
    assert "does not analyze external data" in boundary
    assert "empirical cosmology" in boundary
