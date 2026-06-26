import json
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ash_model.unit_bridge import (
    COVARIANCE_OBSERVABLE_COLUMNS,
    OBSERVABLE_COLUMNS,
    covariance_matrix,
    entropy_bits,
    finite_features_by_depth,
    load_calibration,
    normalize_frontier_columns,
    physical_bridge,
    read_csv_records,
    validate_unit_bridge_artifacts,
)


DATA = ROOT / "data" / "ash-cosmology" / "unit-bridge" / "v0.1"
CAL = ROOT / "config" / "ash_r010_unit_bridge_calibration.json"


def test_entropy_bits_handles_zero_entries():
    assert entropy_bits([0.5, 0.5, 0.0]) == pytest.approx(1.0)


def test_feature_normalization_and_unit_columns():
    frontier = read_csv_records(DATA / "r009_frontier_assumed_input.csv")
    decoherence = read_csv_records(DATA / "r009_decoherence_assumed_input.csv")
    calibration = load_calibration(CAL)

    features = finite_features_by_depth(frontier, decoherence)
    assert all(row["measure_sum"] == pytest.approx(1.0) for row in features)

    observables = physical_bridge(features, calibration)
    for column in OBSERVABLE_COLUMNS:
        assert column in observables[0]

    finite_columns = [c for c in OBSERVABLE_COLUMNS if c != "H_bridge_s_inv"]
    for row in observables:
        for column in finite_columns:
            assert np.isfinite(float(row[column]))


def test_live_r009_frontier_schema_is_normalized():
    frontier = read_csv_records(ROOT / "data" / "ash-cosmology" / "observer-commitment" / "v0.1" / "r009_frontier.csv")
    normalized = normalize_frontier_columns(frontier)
    assert {"measure", "shell_q", "defect_count"}.issubset(normalized[0])
    assert all(row["defect_count"] == 1 for row in normalized if str(row["branch_id"]).endswith(".4"))

    decoherence = read_csv_records(
        ROOT
        / "data"
        / "ash-cosmology"
        / "observer-commitment"
        / "v0.1"
        / "r009_decoherence_summary_by_depth.csv"
    )
    features = finite_features_by_depth(normalized, decoherence)
    assert all(row["measure_sum"] == pytest.approx(1.0) for row in features)


def test_negative_measure_rejected():
    frontier = read_csv_records(DATA / "r009_frontier_assumed_input.csv")[:2]
    decoherence = read_csv_records(DATA / "r009_decoherence_assumed_input.csv")
    frontier[0]["measure"] = -1.0
    with pytest.raises(ValueError):
        finite_features_by_depth(frontier, decoherence)


def test_positive_scale_contract_rejects_zero(tmp_path):
    calibration = json.loads(CAL.read_text())
    calibration["constants"]["tau_star_s"]["value"] = 0.0
    path = tmp_path / "bad_calibration.json"
    path.write_text(json.dumps(calibration), encoding="utf-8")
    with pytest.raises(ValueError):
        load_calibration(path)


def test_generated_covariance_artifact_is_psd():
    covariance = read_csv_records(DATA / "r010_bootstrap_covariance_final_depth.csv")
    assert [row["observable"] for row in covariance] == COVARIANCE_OBSERVABLE_COLUMNS
    matrix = covariance_matrix(covariance)
    assert np.allclose(matrix, matrix.T)
    assert np.linalg.eigvalsh((matrix + matrix.T) / 2.0).min() >= -1e-12


def test_generated_bootstrap_samples_artifact_is_present():
    samples = read_csv_records(DATA / "r010_bootstrap_samples_final_depth.csv")
    assert list(samples[0]) == COVARIANCE_OBSERVABLE_COLUMNS
    assert len(samples) == 600
    assert all(np.isfinite(float(row[column])) for row in samples for column in COVARIANCE_OBSERVABLE_COLUMNS)


def test_validation_record_passes_packaged_artifacts():
    features = read_csv_records(DATA / "r010_finite_bridge_features.csv")
    observables = read_csv_records(DATA / "r010_unit_bearing_observables.csv")
    covariance = read_csv_records(DATA / "r010_bootstrap_covariance_final_depth.csv")
    calibration = load_calibration(CAL)

    validation = validate_unit_bridge_artifacts(features, observables, calibration, covariance).as_dict()
    tests = validation["tests"]
    assert tests["measure_normalization_by_depth"]
    assert tests["unit_columns_present"]
    assert tests["positive_declared_scales"]
    assert tests["finite_physical_values"]
    assert tests["covariance_symmetric"]
    assert tests["covariance_psd_tolerance_1e_minus_12"]
