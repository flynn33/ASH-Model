"""Finite-observer limit closure utilities for ASH roadmap R-011.

This module implements a finite observer hierarchy over odd-dimensional
even-parity state spaces

    Omega_n = {x in F_2^n : sum_i x_i = 0 mod 2}, n in {1, 3, 5, 7, 9}.

It is a deterministic finite-computation layer.  It does not assert a
differentiable continuum, Lorentzian metric, Einstein equation, physical speed
of light, or empirical cosmology.  The top level n=9 coincides with the ASH
parity-valid admissible state layer used by the repository; lower odd levels
are projective finite-observer coarse-grainings.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import comb
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

BitState = Tuple[int, ...]
SpectrumRow = Tuple[int, int, int]

ODD_LEVELS: Tuple[int, ...] = (1, 3, 5, 7, 9)


@dataclass(frozen=True)
class LimitLevelSummary:
    """Finite invariants for one observer level."""

    n: int
    states: int
    degree: int
    edges: int
    diameter: int
    shell_sum: int
    cone_final: int
    spectrum_multiplicity_sum: int
    laplacian_gap: int


@dataclass(frozen=True)
class UnitScaleRow:
    """Normalized R-010-compatible scale annotation for one level.

    The default values are normalized placeholders.  They are not reviewed
    physical constants.
    """

    n: int
    states: int
    ell_m: float
    tau_s: float
    max_pair_diameter: int
    max_signal_radius_m: float


def _require_odd_level(n: int) -> None:
    if n not in ODD_LEVELS:
        raise ValueError(f"n must be one of {ODD_LEVELS}, got {n!r}")


def parity(x: Sequence[int]) -> int:
    """Return binary parity of a bit sequence."""

    return sum(int(b) for b in x) % 2


def even_states(n: int) -> List[BitState]:
    """Enumerate the even-parity states of ``F_2^n`` for an odd observer level."""

    _require_odd_level(n)
    return [tuple(bits) for bits in product((0, 1), repeat=n) if parity(bits) == 0]


def project_state(x: Sequence[int], m: int) -> BitState:
    """Project an even-parity source state to an odd target level.

    The first ``m - 1`` coordinates are retained and the final target coordinate
    is recomputed as the parity that makes the target state even.  This gives a
    nested observer hierarchy rather than a physical spacetime projection.
    """

    _require_odd_level(m)
    if m > len(x):
        raise ValueError("target dimension cannot exceed source length")
    if m == 1:
        return (0,)
    prefix = tuple(int(b) for b in x[: m - 1])
    last = sum(prefix) % 2
    return prefix + (last,)


def project_between(x: Sequence[int], n: int, m: int) -> BitState:
    """Project a state from odd level ``n`` to odd level ``m``."""

    _require_odd_level(n)
    _require_odd_level(m)
    if m > n:
        raise ValueError("target level m cannot exceed source level n")
    if len(x) != n:
        raise ValueError("state length does not match n")
    if any(int(b) not in (0, 1) for b in x):
        raise ValueError("states must be binary")
    if parity(x) != 0:
        raise ValueError("source state must have even parity")
    return project_state(x, m)


def hamming_distance(x: Sequence[int], y: Sequence[int]) -> int:
    """Hamming distance between equal-length bit states."""

    if len(x) != len(y):
        raise ValueError("states must have equal length")
    return sum(int(a) != int(b) for a, b in zip(x, y))


def pair_distance(x: Sequence[int], y: Sequence[int]) -> int:
    """Graph distance in the pair-flip event graph on same-parity states."""

    d = hamming_distance(x, y)
    if d % 2 != 0:
        raise ValueError("pair distance is defined on same-parity states")
    return d // 2


def shell_counts(n: int) -> Dict[int, int]:
    """Distance shell counts in the even-parity pair-flip graph."""

    _require_odd_level(n)
    return {r: comb(n, 2 * r) for r in range(n // 2 + 1)}


def causal_cone_sizes(n: int) -> Dict[int, int]:
    """Closed finite causal cone counts by pair-flip radius."""

    counts = shell_counts(n)
    total = 0
    out: Dict[int, int] = {}
    for radius in sorted(counts):
        total += counts[radius]
        out[radius] = total
    return out


def graph_degree(n: int) -> int:
    """Degree of the halved n-cube pair-flip graph."""

    _require_odd_level(n)
    return comb(n, 2)


def edge_count(n: int) -> int:
    """Undirected edge count for the halved n-cube pair-flip graph."""

    _require_odd_level(n)
    return (2 ** (n - 1) * graph_degree(n)) // 2


def adjacency_spectrum(n: int) -> List[SpectrumRow]:
    """Return ``(r, eigenvalue, multiplicity)`` rows for the halved n-cube."""

    _require_odd_level(n)
    rows: List[SpectrumRow] = []
    for r in range(n // 2 + 1):
        eigenvalue = ((n - 2 * r) ** 2 - n) // 2
        rows.append((r, eigenvalue, comb(n, r)))
    return rows


def laplacian_gap(n: int) -> int:
    """Unnormalized Laplacian spectral gap for the finite event graph."""

    spec = adjacency_spectrum(n)
    degree = graph_degree(n)
    if len(spec) < 2:
        return 0
    return degree - spec[1][1]


def causal_related(x: Sequence[int], tx: int, y: Sequence[int], ty: int) -> bool:
    """Finite graph-metric causal relation on event nodes ``(time, state)``."""

    if len(x) != len(y):
        raise ValueError("states must have equal length")
    if ty < tx:
        return False
    return pair_distance(x, y) <= (ty - tx)


def causal_interval_size(n: int, delta_t: int, distance: int) -> int:
    """Count finite event nodes in a canonical causal interval.

    For canonical endpoints at pair distance ``distance`` and time separation
    ``delta_t``, count intermediate event nodes ``(s, z)`` satisfying
    ``d(x,z) <= s`` and ``d(z,y) <= delta_t - s``.  This is a finite
    graph-workbench diagnostic, not a spacetime volume claim.
    """

    _require_odd_level(n)
    if distance < 0 or distance > n // 2 or delta_t < distance:
        return 0
    x = tuple([0] * n)
    y = tuple([1] * (2 * distance) + [0] * (n - 2 * distance))
    states = even_states(n)
    count = 0
    for s in range(delta_t + 1):
        for z in states:
            if pair_distance(x, z) <= s and pair_distance(z, y) <= delta_t - s:
                count += 1
    return count


def fiber_sizes(n: int, m: int) -> Dict[BitState, int]:
    """Return projective fiber sizes from level ``n`` to level ``m``."""

    _require_odd_level(n)
    _require_odd_level(m)
    if m > n:
        raise ValueError("target level m cannot exceed source level n")
    counts: Dict[BitState, int] = {}
    for x in even_states(n):
        y = project_between(x, n, m)
        counts[y] = counts.get(y, 0) + 1
    return counts


def validate_projective_consistency() -> bool:
    """Exhaustively verify ``pi_lm o pi_mn = pi_ln`` over finite levels."""

    for n in ODD_LEVELS:
        for k in ODD_LEVELS:
            for m in ODD_LEVELS:
                if n >= k >= m:
                    for x in even_states(n):
                        direct = project_between(x, n, m)
                        via_k = project_between(project_between(x, n, k), k, m)
                        if direct != via_k:
                            return False
    return True


def validate_lipschitz() -> bool:
    """Verify projections do not expand microscopic pair-flip events."""

    for n in ODD_LEVELS:
        states = even_states(n)
        for m in ODD_LEVELS:
            if m > n:
                continue
            for x in states:
                px = project_between(x, n, m)
                for i, j in combinations(range(n), 2):
                    y_list = list(x)
                    y_list[i] ^= 1
                    y_list[j] ^= 1
                    y = tuple(y_list)
                    py = project_between(y, n, m)
                    if pair_distance(px, py) > 1:
                        return False
    return True


def unit_scale_table(ell9_m: float = 1.0, tau9_s: float = 1.0) -> List[UnitScaleRow]:
    """Return normalized scale annotations inherited from the R-010 contract.

    The scale law is

        ell_n = ell_9 * 2^((9-n)/2), tau_n = tau_9 * 2^((9-n)/2).

    Defaults are normalized placeholders only.
    """

    if ell9_m <= 0 or tau9_s <= 0:
        raise ValueError("ell9_m and tau9_s must be positive")
    rows: List[UnitScaleRow] = []
    for n in ODD_LEVELS:
        factor = 2 ** ((9 - n) / 2)
        rows.append(
            UnitScaleRow(
                n=n,
                states=2 ** (n - 1),
                ell_m=ell9_m * factor,
                tau_s=tau9_s * factor,
                max_pair_diameter=n // 2,
                max_signal_radius_m=(n // 2) * ell9_m * factor,
            )
        )
    return rows


def level_summary(n: int) -> LimitLevelSummary:
    """Return the finite invariant summary for one observer level."""

    shells = shell_counts(n)
    cones = causal_cone_sizes(n)
    spec = adjacency_spectrum(n)
    return LimitLevelSummary(
        n=n,
        states=2 ** (n - 1),
        degree=graph_degree(n),
        edges=edge_count(n),
        diameter=n // 2,
        shell_sum=sum(shells.values()),
        cone_final=cones[n // 2],
        spectrum_multiplicity_sum=sum(mult for _, _, mult in spec),
        laplacian_gap=laplacian_gap(n),
    )


def validation_summary() -> Dict[str, object]:
    """Return deterministic R-011 validation evidence as JSON-serializable data."""

    levels = [level_summary(n).__dict__ for n in ODD_LEVELS]
    return {
        "r011_scope": "finite_observer_limit_closure_not_differentiable_continuum",
        "levels": levels,
        "projective_consistency": validate_projective_consistency(),
        "projection_lipschitz_on_events": validate_lipschitz(),
        "n9_shell_counts": shell_counts(9),
        "n9_cone_sizes": causal_cone_sizes(9),
        "n9_spectrum": adjacency_spectrum(9),
    }
