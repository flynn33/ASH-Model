import math

import numpy as np
import pytest

import ash_model
from ash_model.empirical import (
    ObservableCalibration,
    calibrate_observable,
    chi_square,
    compare_gaussian_models,
    diagonal_gaussian_log_likelihood,
)
from ash_model.physics import bridge_observables, uniform_physical_distribution


def test_observable_calibration_maps_dimensionless_value_to_unit_value():
    calibration = ObservableCalibration(
        source="order_parameter",
        target="example_temperature_offset",
        scale=2.5,
        offset=273.15,
        unit="K",
    )
    calibrated = calibrate_observable(0.4, calibration)

    assert calibrated.source == "order_parameter"
    assert calibrated.target == "example_temperature_offset"
    assert calibrated.value == 274.15
    assert calibrated.unit == "K"


def test_observable_calibration_rejects_nonfinite_parameters():
    with pytest.raises(ValueError, match="scale must be finite"):
        ObservableCalibration(
            source="order_parameter",
            target="bad",
            scale=math.inf,
            offset=0.0,
            unit="arb",
        )


def test_observable_calibration_can_use_physics_observable_output():
    observables = bridge_observables(uniform_physical_distribution())
    calibration = ObservableCalibration(
        source="mean_hamming_weight",
        target="example_length",
        scale=3.0,
        offset=1.0,
        unit="m",
    )
    calibrated = calibrate_observable(observables.mean_hamming_weight, calibration)

    assert calibrated.value == 14.5
    assert calibrated.unit == "m"


def test_diagonal_gaussian_likelihood_matches_closed_form_value():
    observed = np.asarray([1.0, 2.0])
    predicted = np.asarray([0.5, 2.5])
    sigma = np.asarray([0.5, 1.0])

    expected_chi_square = 1.25
    expected_log_likelihood = -0.5 * (
        expected_chi_square
        + math.log(2.0 * math.pi * 0.5**2)
        + math.log(2.0 * math.pi * 1.0**2)
    )

    assert chi_square(observed, predicted, sigma) == expected_chi_square
    assert diagonal_gaussian_log_likelihood(observed, predicted, sigma) == expected_log_likelihood


def test_gaussian_model_comparison_orders_best_likelihood_first():
    observed = [1.0, 2.0]
    sigma = [0.25, 0.25]
    results = compare_gaussian_models(
        observed=observed,
        standard_deviation=sigma,
        predictions={
            "close": [1.0, 2.1],
            "far": [2.0, 3.0],
        },
    )

    assert [result.name for result in results] == ["close", "far"]
    assert results[0].chi_square < results[1].chi_square
    assert results[0].log_likelihood > results[1].log_likelihood


def test_gaussian_likelihood_rejects_invalid_standard_deviation():
    with pytest.raises(ValueError, match="standard deviations must be positive"):
        diagonal_gaussian_log_likelihood([1.0], [1.0], [0.0])


def test_public_surface_exports_empirical_and_ledger_helpers():
    assert ash_model.ObservableCalibration is ObservableCalibration
    assert ash_model.calibrate_observable is calibrate_observable
    assert ash_model.diagonal_gaussian_log_likelihood is diagonal_gaussian_log_likelihood
    assert callable(ash_model.canonical_prediction_hash)
