"""Roadmap 008 finite branch measure law for ASH.

This module defines an explicit normalized branch-measure workbench for finite ASH
branch frontiers. It is a finite, dimensionless law over repository branch
candidates. It does not derive a Born rule, a Hilbert-space dynamics, spacetime,
or empirical cosmological probabilities.

Primary law
-----------
For a parent branch with mass ``m_b`` and finite children ``c in Ch(b)``,
define an effective action

    A(c) = a_c
         + w_q q_c
         + w_defect d_c
         + w_memory r_c
         + w_coherence h_c
         + w_transfer[-log(max(|mu_q(p)|, epsilon))],

where ``mu_q(p)`` is the finite Roadmap 007 quotient-shell transfer factor.
The local child probability is

    pi(c|b) = exp(-beta A(c)) / sum_{u in Ch(b)} exp(-beta A(u)),

and the child measure is

    m_c = m_b pi(c|b).

The law is normalized on every finite sibling set and therefore preserves total
frontier mass when all parents are expanded.

Optional complex amplitude decoration
-------------------------------------
The helper functions also expose

    psi_c = sqrt(m_c) exp(i phase_scale * a_c).

This is only a norm-preserving representation of the same finite classical
measure. It is not a Born-rule derivation, not a quantum dynamics, and not an
empirical frequency theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, isfinite, log, sin, sqrt
from typing import Mapping, Sequence

from .linear_perturbations import SHELLS, lazy_shell_transfer_factor


@dataclass(frozen=True)
class BranchMeasureConfig:
    """Dimensionless parameters for the finite branch-measure workbench."""

    beta: float = 1.0
    shell_weight: float = 0.05
    defect_weight: float = 0.35
    memory_weight: float = 0.10
    coherence_weight: float = 0.20
    transfer_weight: float = 0.25
    transfer_probability: float = 0.05
    epsilon: float = 1.0e-15
    phase_scale: float = 1.0
    law_version: str = "ash-branch-measure-v0.1-classical-gibbs"

    def validate(self) -> None:
        """Validate dimensionless law parameters."""

        if not isfinite(self.beta) or self.beta < 0.0:
            raise ValueError("beta must be finite and non-negative")
        for name in (
            "shell_weight",
            "defect_weight",
            "memory_weight",
            "coherence_weight",
            "transfer_weight",
            "phase_scale",
        ):
            value = float(getattr(self, name))
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        if not 0.0 <= self.transfer_probability <= 1.0:
            raise ValueError("transfer_probability must lie in [0, 1]")
        if not isfinite(self.epsilon) or self.epsilon <= 0.0:
            raise ValueError("epsilon must be finite and positive")


@dataclass(frozen=True)
class BranchChild:
    """Finite candidate child branch used by the Roadmap 008 law."""

    branch_id: str
    parent_id: str
    shell_q: int
    action: float = 0.0
    defect_count: int = 0
    memory_delta: int = 0
    coherence_penalty: float = 0.0

    def validate(self) -> None:
        """Validate a finite child candidate."""

        if not self.branch_id:
            raise ValueError("branch_id must be non-empty")
        if not self.parent_id:
            raise ValueError("parent_id must be non-empty")
        if self.shell_q not in SHELLS:
            raise ValueError(f"shell_q must be one of {SHELLS}")
        if not isfinite(self.action):
            raise ValueError("action must be finite")
        if self.defect_count < 0:
            raise ValueError("defect_count must be non-negative")
        if self.memory_delta < 0:
            raise ValueError("memory_delta must be non-negative")
        if not isfinite(self.coherence_penalty):
            raise ValueError("coherence_penalty must be finite")


@dataclass(frozen=True)
class BranchMeasure:
    """Measured branch frontier row produced by the Roadmap 008 law."""

    branch_id: str
    parent_id: str
    shell_q: int
    score: float
    local_probability: float
    measure: float
    amplitude_real: float
    amplitude_imag: float

    @property
    def amplitude_norm_squared(self) -> float:
        """Return ``|psi|^2`` for the optional amplitude decoration."""

        return (self.amplitude_real * self.amplitude_real) + (
            self.amplitude_imag * self.amplitude_imag
        )


def _stable_softmax(scores: Sequence[float], beta: float) -> tuple[float, ...]:
    """Return normalized ``exp(-beta score)`` values."""

    if not scores:
        raise ValueError("at least one score is required")
    logits = [-beta * float(score) for score in scores]
    shift = max(logits)
    weights = [exp(logit - shift) for logit in logits]
    total = sum(weights)
    if total <= 0.0 or not isfinite(total):
        raise ValueError("softmax normalization failed")
    return tuple(weight / total for weight in weights)


def transfer_penalty(shell_q: int, probability: float, epsilon: float = 1.0e-15) -> float:
    """Return a finite non-negative transfer penalty for a shell child.

    The penalty uses the Roadmap 007 finite quotient-shell transfer factor and
    stays dimensionless. It is a scoring term only, not a physical action.
    """

    if shell_q not in SHELLS:
        raise ValueError(f"shell_q must be one of {SHELLS}")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0, 1]")
    if epsilon <= 0.0 or not isfinite(epsilon):
        raise ValueError("epsilon must be finite and positive")
    factor = abs(lazy_shell_transfer_factor(shell_q, probability))
    return float(-log(max(factor, epsilon)))


def effective_action(child: BranchChild, config: BranchMeasureConfig | None = None) -> float:
    """Return the dimensionless effective action used by the branch law."""

    config = config or BranchMeasureConfig()
    config.validate()
    child.validate()
    score = (
        float(child.action)
        + (config.shell_weight * float(child.shell_q))
        + (config.defect_weight * float(child.defect_count))
        + (config.memory_weight * float(child.memory_delta))
        + (config.coherence_weight * float(child.coherence_penalty))
        + (
            config.transfer_weight
            * transfer_penalty(
                child.shell_q,
                config.transfer_probability,
                config.epsilon,
            )
        )
    )
    if not isfinite(score):
        raise ValueError("effective action must be finite")
    return float(score)


def allocate_branch_measure(
    parent_measure: float,
    children: Sequence[BranchChild],
    config: BranchMeasureConfig | None = None,
) -> tuple[BranchMeasure, ...]:
    """Allocate a normalized parent measure over a finite child set."""

    config = config or BranchMeasureConfig()
    config.validate()
    if not isfinite(parent_measure) or parent_measure < 0.0:
        raise ValueError("parent_measure must be finite and non-negative")
    if not children:
        raise ValueError("children must be non-empty")
    parent_ids = {child.parent_id for child in children}
    if len(parent_ids) != 1:
        raise ValueError("all children in one allocation must share a parent_id")
    scores = tuple(effective_action(child, config) for child in children)
    probabilities = _stable_softmax(scores, config.beta)
    rows: list[BranchMeasure] = []
    for child, score, probability in zip(children, scores, probabilities, strict=True):
        measure = float(parent_measure * probability)
        phase = float(config.phase_scale * child.action)
        magnitude = sqrt(max(measure, 0.0))
        rows.append(
            BranchMeasure(
                branch_id=child.branch_id,
                parent_id=child.parent_id,
                shell_q=child.shell_q,
                score=float(score),
                local_probability=float(probability),
                measure=measure,
                amplitude_real=float(magnitude * cos(phase)),
                amplitude_imag=float(magnitude * sin(phase)),
            )
        )
    return tuple(rows)


def expand_frontier(
    parent_measures: Mapping[str, float],
    child_map: Mapping[str, Sequence[BranchChild]],
    config: BranchMeasureConfig | None = None,
) -> tuple[BranchMeasure, ...]:
    """Expand all parents with configured children and preserve total mass."""

    config = config or BranchMeasureConfig()
    rows: list[BranchMeasure] = []
    for parent_id in sorted(parent_measures):
        if parent_id not in child_map:
            raise ValueError(f"missing child candidates for parent {parent_id!r}")
        rows.extend(
            allocate_branch_measure(parent_measures[parent_id], child_map[parent_id], config)
        )
    return tuple(rows)


def frontier_entropy(rows: Sequence[BranchMeasure], *, base: float = 2.0) -> float:
    """Return Shannon entropy of a normalized branch frontier."""

    if base <= 0.0 or base == 1.0:
        raise ValueError("entropy base must be positive and not one")
    total = sum(row.measure for row in rows)
    if not isfinite(total) or total <= 0.0:
        raise ValueError("frontier mass must be positive")
    entropy = 0.0
    for row in rows:
        if row.measure < -1e-15:
            raise ValueError("branch measures must be non-negative")
        probability = max(0.0, float(row.measure) / total)
        if probability > 0.0:
            entropy -= probability * (log(probability) / log(base))
    return float(entropy)


def verify_branch_measure(
    rows: Sequence[BranchMeasure],
    *,
    expected_total: float = 1.0,
    atol: float = 1.0e-12,
) -> dict[str, object]:
    """Return machine-readable normalization diagnostics."""

    total_measure = float(sum(row.measure for row in rows))
    total_amplitude_norm = float(sum(row.amplitude_norm_squared for row in rows))
    local_by_parent: dict[str, float] = {}
    measure_by_parent: dict[str, float] = {}
    for row in rows:
        local_by_parent[row.parent_id] = local_by_parent.get(row.parent_id, 0.0) + row.local_probability
        measure_by_parent[row.parent_id] = measure_by_parent.get(row.parent_id, 0.0) + row.measure
    max_local_residual = max(
        (abs(value - 1.0) for value in local_by_parent.values()),
        default=0.0,
    )
    return {
        "num_rows": len(rows),
        "expected_total": float(expected_total),
        "total_measure": total_measure,
        "total_amplitude_norm_squared": total_amplitude_norm,
        "max_total_measure_residual": abs(total_measure - expected_total),
        "max_total_amplitude_residual": abs(total_amplitude_norm - expected_total),
        "max_local_probability_residual": float(max_local_residual),
        "parent_count": len(local_by_parent),
        "passed": (
            abs(total_measure - expected_total) <= atol
            and abs(total_amplitude_norm - expected_total) <= atol
            and max_local_residual <= atol
        ),
    }


def shell_demo_children(parent_id: str, *, depth: int, probability: float = 0.05) -> tuple[BranchChild, ...]:
    """Return deterministic shell-indexed child candidates for examples/tests."""

    checksum = sum(ord(character) for character in parent_id)
    children: list[BranchChild] = []
    for shell_q in SHELLS:
        child_id = f"{parent_id}.q{shell_q}"
        action = 0.02 * depth + transfer_penalty(shell_q, probability)
        defect_count = (checksum + depth + shell_q) % 3
        memory_delta = (depth + shell_q) % 2
        coherence_penalty = abs(shell_q - 2) / 2.0
        children.append(
            BranchChild(
                branch_id=child_id,
                parent_id=parent_id,
                shell_q=shell_q,
                action=float(action),
                defect_count=int(defect_count),
                memory_delta=int(memory_delta),
                coherence_penalty=float(coherence_penalty),
            )
        )
    return tuple(children)


def demo_branch_frontier(
    *,
    depth: int = 3,
    config: BranchMeasureConfig | None = None,
) -> tuple[BranchMeasure, ...]:
    """Return a deterministic finite branch frontier after ``depth`` expansions."""

    if depth < 0:
        raise ValueError("depth must be non-negative")
    config = config or BranchMeasureConfig()
    parent_measures: dict[str, float] = {"root": 1.0}
    rows: tuple[BranchMeasure, ...] = ()
    for step in range(1, depth + 1):
        child_map = {
            parent_id: shell_demo_children(
                parent_id,
                depth=step,
                probability=config.transfer_probability,
            )
            for parent_id in parent_measures
        }
        rows = expand_frontier(parent_measures, child_map, config)
        parent_measures = {row.branch_id: row.measure for row in rows}
    return rows


def law_summary(config: BranchMeasureConfig | None = None) -> dict[str, object]:
    """Return a machine-readable summary of the Roadmap 008 law."""

    config = config or BranchMeasureConfig()
    config.validate()
    return {
        "title": "ASH Roadmap 008 finite branch measure law",
        "law_version": config.law_version,
        "classification": {
            "layer_1": "finite normalization theorem over finite branch sibling sets",
            "layer_2": "deterministic branch-frontier scoring and generated verification artifacts",
            "layer_3_boundary": "interpretive branch-cosmology workbench only; no empirical probability, Born-rule, or physical amplitude claim",
        },
        "measure_equation": "mu(c)=mu(parent)*exp(-beta*A(c))/sum_sibling exp(-beta*A(u))",
        "effective_action": "A=a+w_q*q+w_defect*d+w_memory*r+w_coherence*h+w_transfer*(-log(max(|mu_q(p)|, epsilon)))",
        "amplitude_decoration": "psi(c)=sqrt(mu(c))*exp(i*phase_scale*a_c); norm-preserving representation only",
        "normalization": "For each finite sibling set with at least one child, sum_c pi(c|parent)=1 and sum_c mu(c)=mu(parent).",
        "config": {
            "beta": config.beta,
            "shell_weight": config.shell_weight,
            "defect_weight": config.defect_weight,
            "memory_weight": config.memory_weight,
            "coherence_weight": config.coherence_weight,
            "transfer_weight": config.transfer_weight,
            "transfer_probability": config.transfer_probability,
            "epsilon": config.epsilon,
            "phase_scale": config.phase_scale,
        },
        "boundary": "Finite ASH branch-frontier measure only; no Born-rule proof, no Hilbert-space dynamics, no collapse/decoherence rule, no physical spacetime bridge, and no empirical validation.",
    }
