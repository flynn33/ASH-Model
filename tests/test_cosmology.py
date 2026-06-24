import math

import numpy as np
import pytest

import ash_model
from ash_model.cosmology import (
    FlatLambdaCDMParameters,
    compare_distance_baselines,
    dimensionless_hubble_parameter,
    flat_lcdm_distance_curve,
    normalized_comoving_distance,
)


def test_flat_lcdm_parameters_require_flat_nonnegative_density_budget():
    parameters = FlatLambdaCDMParameters(matter_density=0.3, dark_energy_density=0.7)

    assert parameters.total_density == 1.0

    with pytest.raises(ValueError, match="density values must be non-negative"):
        FlatLambdaCDMParameters(matter_density=-0.1, dark_energy_density=1.1)
    with pytest.raises(ValueError, match="flat density budget"):
        FlatLambdaCDMParameters(matter_density=0.3, dark_energy_density=0.6)


def test_dimensionless_hubble_parameter_matches_flat_lcdm_equation():
    parameters = FlatLambdaCDMParameters(matter_density=0.3, dark_energy_density=0.7)

    assert dimensionless_hubble_parameter(0.0, parameters) == 1.0
    assert dimensionless_hubble_parameter(1.0, parameters) == math.sqrt(0.3 * 8.0 + 0.7)


def test_normalized_comoving_distance_is_zero_then_monotonic():
    parameters = FlatLambdaCDMParameters(matter_density=0.3, dark_energy_density=0.7)

    distances = [
        normalized_comoving_distance(redshift, parameters, steps=512)
        for redshift in (0.0, 0.5, 1.0)
    ]

    assert distances[0] == 0.0
    assert 0.0 < distances[1] < distances[2]


def test_flat_lcdm_distance_curve_preserves_redshift_shape():
    parameters = FlatLambdaCDMParameters(matter_density=0.3, dark_energy_density=0.7)
    curve = flat_lcdm_distance_curve([0.0, 0.5, 1.0], parameters, steps=512)

    assert curve.shape == (3,)
    assert np.all(np.isfinite(curve))
    assert curve[0] == 0.0
    assert curve[1] < curve[2]


def test_compare_distance_baselines_orders_closest_curve_first():
    standard = FlatLambdaCDMParameters(matter_density=0.3, dark_energy_density=0.7)
    shifted = FlatLambdaCDMParameters(matter_density=0.4, dark_energy_density=0.6)
    redshifts = [0.2, 0.5, 1.0]
    observed = flat_lcdm_distance_curve(redshifts, standard, steps=512)

    results = compare_distance_baselines(
        redshifts=redshifts,
        observed_distances=observed,
        standard_deviation=[0.01, 0.01, 0.01],
        baselines={
            "standard": standard,
            "shifted": shifted,
        },
        steps=512,
    )

    assert [result.name for result in results] == ["standard", "shifted"]
    assert results[0].chi_square == 0.0
    assert results[0].log_likelihood > results[1].log_likelihood


def test_public_surface_exports_standard_baseline_helpers():
    assert ash_model.FlatLambdaCDMParameters is FlatLambdaCDMParameters
    assert ash_model.dimensionless_hubble_parameter is dimensionless_hubble_parameter
    assert ash_model.normalized_comoving_distance is normalized_comoving_distance
