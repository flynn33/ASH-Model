"""Finite ASH Roadmap 007 linear perturbation sector.

This module refines the existing finite-observer pair-flip perturbation layer.
It works only on the 256-state admissible even-parity ASH state space and does
not define metric perturbations, physical wavenumbers, or empirical spectra.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb, exp, log1p
from typing import Sequence

import numpy as np

from .bits import BIT_COUNT, BitTuple, hamming_weight, int_to_bits, xor_bits
from .physics import PAIR_FLIP_COUNT, pair_flip_transition, physical_state_space

ALL_ONES: BitTuple = (1,) * BIT_COUNT
SHELLS: tuple[int, ...] = (0, 1, 2, 3, 4)


@dataclass(frozen=True)
class PerturbationShell:
    """Exact quotient-shell data for restricted Walsh characters."""

    q: int
    representative_weight: int
    multiplicity: int
    krawtchouk_k2: int
    lambda_nonlazy: float
    gamma_continuous: float


def dot_mod2(left: Sequence[int], right: Sequence[int]) -> int:
    """Return the mod-two dot product of two ASH bit vectors."""

    if len(left) != BIT_COUNT or len(right) != BIT_COUNT:
        raise ValueError(f"expected {BIT_COUNT}-bit vectors")
    return sum(int(a) & int(b) for a, b in zip(left, right, strict=True)) % 2


def character_value(label: Sequence[int], state: Sequence[int]) -> int:
    """Return the restricted Walsh character value ``(-1)^(label.state)``."""

    return 1 if dot_mod2(label, state) == 0 else -1


def canonical_character_labels() -> tuple[BitTuple, ...]:
    """Return one representative for each restricted Walsh character.

    On the even-parity ASH state space, labels ``a`` and ``a+111111111``
    define the same restricted Walsh character. The canonical representative
    is the member of that coset with Hamming weight at most four; ties cannot
    occur because ``BIT_COUNT`` is odd.
    """

    labels: list[BitTuple] = []
    seen: set[BitTuple] = set()
    for index in range(1 << BIT_COUNT):
        label = int_to_bits(index, length=BIT_COUNT)
        complement = xor_bits(label, ALL_ONES)
        representative = label if hamming_weight(label) <= hamming_weight(complement) else complement
        if representative in seen:
            continue
        seen.add(representative)
        labels.append(representative)
    return tuple(sorted(labels, key=lambda item: (hamming_weight(item), item)))


def shell_index(label: Sequence[int]) -> int:
    """Return ``q=min(|a|, 9-|a|)`` for a Walsh label."""

    if len(label) != BIT_COUNT:
        raise ValueError(f"expected {BIT_COUNT}-bit label")
    weight = hamming_weight(tuple(int(bit) for bit in label))
    return min(weight, BIT_COUNT - weight)


def krawtchouk_k2(weight: int) -> int:
    """Return the weight-two Krawtchouk value ``K_2(weight;9)``."""

    if not 0 <= weight <= BIT_COUNT:
        raise ValueError("weight outside ASH bit count")
    return comb(BIT_COUNT - weight, 2) - weight * (BIT_COUNT - weight) + comb(weight, 2)


def pair_flip_shell_eigenvalue(q: int) -> float:
    """Return the non-lazy pair-flip eigenvalue for quotient shell ``q``."""

    if q not in SHELLS:
        raise ValueError("q must be one of 0, 1, 2, 3, 4")
    return float(krawtchouk_k2(q) / PAIR_FLIP_COUNT)


def lazy_shell_transfer_factor(q: int, probability: float) -> float:
    """Return one-tick lazy transfer factor ``mu_q(p)``."""

    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    return float((1.0 - probability) + probability * pair_flip_shell_eigenvalue(q))


def shell_decay_rate(q: int) -> float:
    """Return ``gamma_q = 1 - lambda_q`` for the finite clock limit."""

    return float(1.0 - pair_flip_shell_eigenvalue(q))


def spectral_shell_table() -> tuple[PerturbationShell, ...]:
    """Return the exact five-shell quotient table."""

    return tuple(
        PerturbationShell(
            q=q,
            representative_weight=q,
            multiplicity=comb(BIT_COUNT, q),
            krawtchouk_k2=krawtchouk_k2(q),
            lambda_nonlazy=pair_flip_shell_eigenvalue(q),
            gamma_continuous=shell_decay_rate(q),
        )
        for q in SHELLS
    )


def verify_character_eigenmodes(
    probabilities: Sequence[float] = (0.01, 0.05, 0.1, 0.5, 1.0),
) -> dict[str, object]:
    """Exhaustively verify restricted Walsh eigenmodes on all 256 states."""

    states = physical_state_space()
    labels = canonical_character_labels()
    max_residual = 0.0
    shell_counts = {q: 0 for q in SHELLS}

    for probability in probabilities:
        kernel = pair_flip_transition(probability)
        for label in labels:
            q = shell_index(label)
            shell_counts[q] += 1
            character = np.asarray([character_value(label, state) for state in states], dtype=float)
            residual = kernel @ character - lazy_shell_transfer_factor(q, probability) * character
            max_residual = max(max_residual, float(np.max(np.abs(residual))))

    repetitions = len(tuple(probabilities))
    normalized_counts = {str(q): shell_counts[q] // repetitions for q in SHELLS}
    return {
        "num_states": len(states),
        "num_characters": len(labels),
        "shell_counts": normalized_counts,
        "p_values": [float(value) for value in probabilities],
        "max_eigen_residual": max_residual,
    }


def transfer_factor(q: int, probabilities: Sequence[float]) -> float:
    """Return ``prod_t mu_q(p_t)`` for a finite schedule."""

    value = 1.0
    for probability in probabilities:
        value *= lazy_shell_transfer_factor(q, float(probability))
    return float(value)


def constant_probability_schedule(probability: float, ticks: int) -> tuple[float, ...]:
    """Return a constant finite update-probability schedule."""

    if ticks < 0:
        raise ValueError("ticks must be non-negative")
    return tuple(float(probability) for _ in range(ticks))


def transfer_function_rows(probability: float, ticks: int) -> list[dict[str, float]]:
    """Return transfer-function rows for all shells under constant ``p``."""

    rows: list[dict[str, float]] = []
    for tick in range(ticks + 1):
        row: dict[str, float] = {"tick": float(tick), "p": float(probability)}
        for q in SHELLS:
            transfer = lazy_shell_transfer_factor(q, probability) ** tick
            row[f"T_q{q}"] = float(transfer)
            row[f"power_T2_q{q}"] = float(transfer * transfer)
        rows.append(row)
    return rows


def shell_power(delta: Sequence[float], labels: Sequence[BitTuple] | None = None) -> dict[int, float]:
    """Return mean squared restricted-Walsh coefficient by quotient shell."""

    states = physical_state_space()
    values = np.asarray(delta, dtype=float)
    if values.shape != (len(states),):
        raise ValueError(f"expected {len(states)} perturbation entries")
    labels = tuple(labels or canonical_character_labels())

    grouped: dict[int, list[float]] = {q: [] for q in SHELLS}
    for label in labels:
        q = shell_index(label)
        character = np.asarray([character_value(label, state) for state in states], dtype=float)
        coefficient = float(values @ character)
        grouped[q].append(coefficient * coefficient)
    return {q: float(np.mean(grouped[q])) for q in SHELLS}


def random_perturbation_power_check(
    *,
    seed: int = 20260626,
    probability: float = 0.05,
    ticks: int = 20,
) -> dict[str, object]:
    """Compare direct finite evolution with the quotient shell-power law."""

    rng = np.random.default_rng(seed)
    states = physical_state_space()
    count = len(states)

    delta = rng.normal(size=count)
    delta -= delta.mean()
    delta *= 1e-4 / max(abs(float(delta.min())), abs(float(delta.max())))

    rho = np.full(count, 1.0 / count, dtype=float) + delta
    if np.min(rho) <= 0.0:
        raise RuntimeError("internal random perturbation scale produced a nonpositive law")

    kernel = pair_flip_transition(probability)
    evolved = rho @ np.linalg.matrix_power(kernel, ticks)
    delta_evolved = evolved - np.full(count, 1.0 / count, dtype=float)

    labels = canonical_character_labels()
    initial_power = shell_power(delta, labels)
    evolved_power = shell_power(delta_evolved, labels)

    rows: list[dict[str, float]] = []
    max_relative_error = 0.0
    for q in SHELLS:
        predicted = (lazy_shell_transfer_factor(q, probability) ** (2 * ticks)) * initial_power[q]
        if q == 0 and initial_power[q] < 1e-24:
            relative_error = 0.0
        else:
            denominator = max(1e-30, abs(predicted), abs(evolved_power[q]))
            relative_error = abs(evolved_power[q] - predicted) / denominator
        max_relative_error = max(max_relative_error, relative_error)
        rows.append(
            {
                "q": float(q),
                "initial_shell_power": float(initial_power[q]),
                "evolved_shell_power": float(evolved_power[q]),
                "predicted_shell_power": float(predicted),
                "relative_error": float(relative_error),
            }
        )

    return {
        "rows": rows,
        "max_relative_error": float(max_relative_error),
        "seed": int(seed),
        "p": float(probability),
        "ticks": int(ticks),
    }


def impulse_response_rows(probability: float = 0.05, ticks: int = 80) -> list[dict[str, float]]:
    """Return Green-function impulse responses for nonconstant shells."""

    rows: list[dict[str, float]] = []
    for q in (1, 2, 3, 4):
        factor = lazy_shell_transfer_factor(q, probability)
        for tick in range(ticks + 1):
            response = 0.0 if tick == 0 else factor ** (tick - 1)
            rows.append({"q": float(q), "tick": float(tick), "impulse_response": float(response)})
    return rows


def synthetic_redshift_transfer_rows(
    *,
    p0: float = 0.05,
    zmax: float = 2.2,
    points: int = 160,
    tau_scale: float = 20.0,
) -> list[dict[str, float]]:
    """Return a dimensionless synthetic redshift-transfer test object.

    This is not empirical calibration. The variable ``z`` is a synthetic
    downstream-solver coordinate and does not supply a physical redshift bridge.
    """

    rows: list[dict[str, float]] = []
    for z in np.linspace(0.0, zmax, points):
        tau = tau_scale * log1p(float(z))
        integrated_activity = p0 * tau_scale * log1p(tau / tau_scale)
        row: dict[str, float] = {
            "z_synthetic": float(z),
            "tau_dimensionless": float(tau),
            "p0": float(p0),
            "tau_scale": float(tau_scale),
            "integrated_flip_activity": float(integrated_activity),
        }
        for q in SHELLS:
            transfer = exp(-shell_decay_rate(q) * integrated_activity)
            row[f"T_q{q}"] = float(transfer)
            row[f"power_T2_q{q}"] = float(transfer * transfer)
        rows.append(row)
    return rows


def formal_expression_summary() -> dict[str, object]:
    """Return a machine-readable summary of the finite perturbation sector."""

    return {
        "title": "ASH Roadmap 007 finite linear perturbation sector",
        "status": "finite-observer perturbation refinement; no metric or empirical spectrum claim",
        "state_space": "H={x in F_2^9 : sum_i x_i = 0 mod 2}, |H|=256",
        "character_quotient": "F_2^9/<111111111>; q=min(|a|,9-|a|)",
        "shells": [
            {
                "q": shell.q,
                "multiplicity": shell.multiplicity,
                "K2": shell.krawtchouk_k2,
                "lambda": shell.lambda_nonlazy,
                "gamma": shell.gamma_continuous,
            }
            for shell in spectral_shell_table()
        ],
        "discrete_equation": "alpha_a(t+1)=mu_q(p_t) alpha_a(t)+s_a(t), mu_q=1-p_t gamma_q",
        "power_equation": "P_q(t1)=|prod_t mu_q(p_t)|^2 P_q(t0)",
        "continuous_clock_limit": "d alpha_a/d tau = - r(tau) gamma_q alpha_a + s_a(tau)",
        "boundary": "finite-observer perturbations only; no metric perturbation or empirical spectrum claimed",
    }
