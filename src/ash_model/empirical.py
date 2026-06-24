"""Empirical bridge mechanics for finite-observer ASH outputs.

The functions here provide contracts for calibrated observables and likelihood
comparisons.  They do not supply a physical calibration, external data set, or
empirical result.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi
from typing import Mapping, Sequence

import numpy as np


@dataclass(frozen=True)
class ObservableCalibration:
    """Affine calibration from an internal observable to a named unit value."""

    source: str
    target: str
    scale: float
    offset: float
    unit: str

    def __post_init__(self) -> None:
        if not self.source:
            raise ValueError("source must be non-empty")
        if not self.target:
            raise ValueError("target must be non-empty")
        if not self.unit:
            raise ValueError("unit must be non-empty")
        if not isfinite(self.scale):
            raise ValueError("scale must be finite")
        if not isfinite(self.offset):
            raise ValueError("offset must be finite")


@dataclass(frozen=True)
class CalibratedObservable:
    """Unit-bearing observable produced by a declared calibration."""

    source: str
    target: str
    value: float
    unit: str


@dataclass(frozen=True)
class LikelihoodResult:
    """Likelihood comparison result for one named prediction vector."""

    name: str
    chi_square: float
    log_likelihood: float
    degrees_of_freedom: int


def calibrate_observable(value: float, calibration: ObservableCalibration) -> CalibratedObservable:
    """Apply an affine calibration to one dimensionless observable."""

    if not isfinite(float(value)):
        raise ValueError("observable value must be finite")
    calibrated_value = calibration.offset + calibration.scale * float(value)
    return CalibratedObservable(
        source=calibration.source,
        target=calibration.target,
        value=calibrated_value,
        unit=calibration.unit,
    )


def _as_vector(values: Sequence[float], label: str) -> np.ndarray:
    vector = np.asarray(values, dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"{label} must be a one-dimensional sequence")
    if vector.size == 0:
        raise ValueError(f"{label} must be non-empty")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{label} must contain finite values")
    return vector


def _likelihood_vectors(
    observed: Sequence[float],
    predicted: Sequence[float],
    standard_deviation: Sequence[float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    observed_vector = _as_vector(observed, "observed values")
    predicted_vector = _as_vector(predicted, "predicted values")
    sigma_vector = _as_vector(standard_deviation, "standard deviations")
    if observed_vector.shape != predicted_vector.shape:
        raise ValueError("observed and predicted values must have the same shape")
    if observed_vector.shape != sigma_vector.shape:
        raise ValueError("standard deviations must match observed values")
    if np.any(sigma_vector <= 0.0):
        raise ValueError("standard deviations must be positive")
    return observed_vector, predicted_vector, sigma_vector


def chi_square(
    observed: Sequence[float],
    predicted: Sequence[float],
    standard_deviation: Sequence[float],
) -> float:
    """Return the diagonal-covariance chi-square statistic."""

    observed_vector, predicted_vector, sigma_vector = _likelihood_vectors(
        observed,
        predicted,
        standard_deviation,
    )
    residual = (observed_vector - predicted_vector) / sigma_vector
    return float(residual @ residual)


def diagonal_gaussian_log_likelihood(
    observed: Sequence[float],
    predicted: Sequence[float],
    standard_deviation: Sequence[float],
) -> float:
    """Return the normalized diagonal Gaussian log-likelihood."""

    observed_vector, predicted_vector, sigma_vector = _likelihood_vectors(
        observed,
        predicted,
        standard_deviation,
    )
    residual = (observed_vector - predicted_vector) / sigma_vector
    normalizer = np.log(2.0 * pi * sigma_vector**2)
    return float(-0.5 * np.sum(residual**2 + normalizer))


def compare_gaussian_models(
    *,
    observed: Sequence[float],
    standard_deviation: Sequence[float],
    predictions: Mapping[str, Sequence[float]],
) -> tuple[LikelihoodResult, ...]:
    """Rank prediction vectors by diagonal Gaussian log-likelihood."""

    if not predictions:
        raise ValueError("predictions must be non-empty")
    results: list[LikelihoodResult] = []
    for name, predicted in predictions.items():
        if not name:
            raise ValueError("prediction names must be non-empty")
        statistic = chi_square(observed, predicted, standard_deviation)
        log_likelihood = diagonal_gaussian_log_likelihood(
            observed,
            predicted,
            standard_deviation,
        )
        degrees = len(_as_vector(observed, "observed values"))
        results.append(
            LikelihoodResult(
                name=name,
                chi_square=statistic,
                log_likelihood=log_likelihood,
                degrees_of_freedom=degrees,
            )
        )
    return tuple(
        sorted(
            results,
            key=lambda result: (-result.log_likelihood, result.chi_square, result.name),
        )
    )
