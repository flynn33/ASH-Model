"""Reference standard-baseline cosmology utilities.

This module implements dimensionless flat-Lambda-CDM comparison mechanics.
It is a baseline contract for validation work, not a derivation from ASH
finite-observer dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Mapping, Sequence

import numpy as np

from .empirical import LikelihoodResult, chi_square, diagonal_gaussian_log_likelihood


@dataclass(frozen=True)
class FlatLambdaCDMParameters:
    """Dimensionless density parameters for a flat standard baseline."""

    matter_density: float
    dark_energy_density: float
    radiation_density: float = 0.0
    flatness_tolerance: float = 1e-12

    def __post_init__(self) -> None:
        values = (
            self.matter_density,
            self.dark_energy_density,
            self.radiation_density,
            self.flatness_tolerance,
        )
        if not all(isfinite(value) for value in values):
            raise ValueError("density values and tolerance must be finite")
        if self.flatness_tolerance <= 0.0:
            raise ValueError("flatness tolerance must be positive")
        if min(self.matter_density, self.dark_energy_density, self.radiation_density) < 0.0:
            raise ValueError("density values must be non-negative")
        if abs(self.total_density - 1.0) > self.flatness_tolerance:
            raise ValueError("parameters must satisfy a flat density budget")

    @property
    def total_density(self) -> float:
        """Return the total dimensionless density budget."""

        return self.matter_density + self.dark_energy_density + self.radiation_density


def _redshift(value: float) -> float:
    redshift = float(value)
    if not isfinite(redshift):
        raise ValueError("redshift must be finite")
    if redshift < 0.0:
        raise ValueError("redshift must be non-negative")
    return redshift


def dimensionless_hubble_parameter(redshift: float, parameters: FlatLambdaCDMParameters) -> float:
    """Return ``E(z) = H(z) / H0`` for a flat standard baseline."""

    z = _redshift(redshift)
    scale = 1.0 + z
    value = (
        parameters.radiation_density * scale**4
        + parameters.matter_density * scale**3
        + parameters.dark_energy_density
    )
    return sqrt(value)


def normalized_comoving_distance(
    redshift: float,
    parameters: FlatLambdaCDMParameters,
    *,
    steps: int = 2048,
) -> float:
    """Return the dimensionless comoving distance ``H0 D_C / c``."""

    z = _redshift(redshift)
    if steps < 2:
        raise ValueError("steps must be at least 2")
    if z == 0.0:
        return 0.0
    grid = np.linspace(0.0, z, num=steps + 1, dtype=float)
    inverse_e = np.asarray(
        [1.0 / dimensionless_hubble_parameter(point, parameters) for point in grid],
        dtype=float,
    )
    widths = np.diff(grid)
    areas = 0.5 * (inverse_e[:-1] + inverse_e[1:]) * widths
    return float(np.sum(areas))


def flat_lcdm_distance_curve(
    redshifts: Sequence[float],
    parameters: FlatLambdaCDMParameters,
    *,
    steps: int = 2048,
) -> np.ndarray:
    """Return a vector of normalized comoving distances for redshifts."""

    values = np.asarray(redshifts, dtype=float)
    if values.ndim != 1:
        raise ValueError("redshifts must be a one-dimensional sequence")
    if values.size == 0:
        raise ValueError("redshifts must be non-empty")
    return np.asarray(
        [normalized_comoving_distance(redshift, parameters, steps=steps) for redshift in values],
        dtype=float,
    )


def compare_distance_baselines(
    *,
    redshifts: Sequence[float],
    observed_distances: Sequence[float],
    standard_deviation: Sequence[float],
    baselines: Mapping[str, FlatLambdaCDMParameters],
    steps: int = 2048,
) -> tuple[LikelihoodResult, ...]:
    """Rank flat-standard-baseline distance curves against observations."""

    if not baselines:
        raise ValueError("baselines must be non-empty")
    results: list[LikelihoodResult] = []
    for name, parameters in baselines.items():
        if not name:
            raise ValueError("baseline names must be non-empty")
        predicted = flat_lcdm_distance_curve(redshifts, parameters, steps=steps)
        statistic = chi_square(observed_distances, predicted, standard_deviation)
        log_likelihood = diagonal_gaussian_log_likelihood(
            observed_distances,
            predicted,
            standard_deviation,
        )
        results.append(
            LikelihoodResult(
                name=name,
                chi_square=statistic,
                log_likelihood=log_likelihood,
                degrees_of_freedom=len(predicted),
            )
        )
    return tuple(
        sorted(
            results,
            key=lambda result: (-result.log_likelihood, result.chi_square, result.name),
        )
    )
