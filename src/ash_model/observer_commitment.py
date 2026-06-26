"""Roadmap R-009 finite observer commitment, memory, and decoherence rules.

This module implements the finite-computational closure target for ASH Roadmap
R-009.  It assumes Roadmap R-008 supplies normalized finite branch weights or
amplitudes, then defines:

* observer-relative commitment as memory-record update along branch histories;
* the push-forward distribution over committed memory records;
* a bounded finite branch-separation/decoherence score.

Scientific boundary
-------------------
The objects here are dimensionless finite workbench quantities.  They are not
claims of physical wavefunction collapse, a Born-rule derivation, a complete
Hilbert-space decoherence functional, spacetime dynamics, CMB/matter spectra, or
empirical cosmology validation.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, isfinite, sin, sqrt
import hashlib
import json
from typing import Mapping, Sequence

from .branch_measure import BranchChild, BranchMeasureConfig, allocate_branch_measure


LAW_VERSION = "ash-r009-commitment-memory-decoherence-v0.1"
BOUNDARY_STATEMENT = (
    "Finite observer-relative commitment and branch-separation workbench only; "
    "no collapse claim, no Born-rule proof, no unitary Hilbert-space dynamics, "
    "no unit-bearing spacetime bridge, no CMB/matter-spectrum solver, and no "
    "empirical cosmology validation."
)


@dataclass(frozen=True)
class ObserverCommitmentConfig:
    """Parameters for the finite R-009 branch-separation score.

    All parameters are dimensionless engineering choices for the deterministic
    finite workbench.  They are versioned and must not be described as unique or
    physically necessary.
    """

    gamma_branch: float = 0.65
    gamma_memory: float = 1.25
    gamma_observation: float = 0.50
    phase_scale: float = 0.30
    decoherence_threshold: float = 1.0e-3
    probability_tolerance: float = 1.0e-12
    law_version: str = LAW_VERSION


@dataclass(frozen=True)
class BranchRecord:
    """Finite branch leaf/node record used by R-009.

    The branch_id is dot-separated by convention, e.g. ``b0.1.4.2``.  The
    convention is deliberately simple so the rule remains auditable and
    independent of any particular cosmology bridge.
    """

    branch_id: str
    parent_id: str | None
    depth: int
    weight: float
    memory: tuple[str, ...] = ()
    phase: float = 0.0
    observation_token: str | None = None

    @property
    def observation_count(self) -> int:
        return len(self.memory)

    @property
    def memory_record(self) -> str:
        return "|".join(self.memory) if self.memory else "EMPTY"

    @property
    def memory_hash(self) -> str:
        return stable_hash(self.memory_record)[:16]


def stable_hash(text: str) -> str:
    """Return a stable SHA-256 hash for manifests and memory-class keys."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_probability_weights(
    records: Sequence[BranchRecord],
    *,
    tolerance: float = 1.0e-12,
) -> None:
    """Validate that branch weights form a finite normalized frontier."""

    if not records:
        raise ValueError("records must be non-empty")
    total = 0.0
    for record in records:
        if not isfinite(record.weight):
            raise ValueError(f"non-finite branch weight for {record.branch_id!r}")
        if record.weight < 0.0:
            raise ValueError(f"negative branch weight for {record.branch_id!r}")
        total += record.weight
    if abs(total - 1.0) > tolerance:
        raise ValueError(f"branch weights must sum to 1.0 within tolerance; got {total!r}")


def commit_memory(parent_memory: Sequence[str], observation_token: str | None) -> tuple[str, ...]:
    """Append one observer-relative token, or preserve memory if token is absent."""

    memory = tuple(parent_memory)
    if observation_token is None or observation_token == "":
        return memory
    return memory + (str(observation_token),)


def parent_memory_is_prefix(parent: BranchRecord, child: BranchRecord) -> bool:
    """Return true when the parent memory is embedded as a child-memory prefix."""

    return tuple(child.memory[: len(parent.memory)]) == tuple(parent.memory)


def verify_memory_prefix_embedding(records: Sequence[BranchRecord]) -> bool:
    """Check the R-009 memory-embedding invariant on a finite branch set."""

    by_id = {record.branch_id: record for record in records}
    for record in records:
        if record.parent_id is None:
            continue
        parent = by_id.get(record.parent_id)
        if parent is None:
            return False
        if not parent_memory_is_prefix(parent, record):
            return False
    return True


def commitment_distribution(leaves: Sequence[BranchRecord]) -> list[dict[str, object]]:
    """Push forward leaf weights to committed observer-memory classes."""

    totals: dict[str, dict[str, object]] = {}
    for leaf in leaves:
        key = leaf.memory_record
        if key not in totals:
            totals[key] = {
                "memory_hash": leaf.memory_hash,
                "memory_length": len(leaf.memory),
                "memory_record": leaf.memory_record,
                "measure": 0.0,
                "leaf_count": 0,
            }
        totals[key]["measure"] = float(totals[key]["measure"]) + leaf.weight
        totals[key]["leaf_count"] = int(totals[key]["leaf_count"]) + 1
    return sorted(totals.values(), key=lambda row: (-float(row["measure"]), str(row["memory_hash"])))


def normalize_commitment_distribution(
    distribution: Sequence[Mapping[str, object]],
    *,
    tolerance: float = 1.0e-12,
) -> None:
    """Validate that the memory-class push-forward sums to one."""

    total = sum(float(row["measure"]) for row in distribution)
    if abs(total - 1.0) > tolerance:
        raise ValueError(f"commitment distribution must sum to 1.0; got {total!r}")


def _branch_parts(branch_id: str) -> list[str]:
    parts = branch_id.split(".")
    if not parts or parts[0] != "b0":
        raise ValueError("branch_id must use dot-separated paths rooted at 'b0'")
    return parts


def lca_depth(branch_id_a: str, branch_id_b: str) -> int:
    """Depth of the lowest common ancestor for two dot-separated branch paths."""

    parts_a = _branch_parts(branch_id_a)
    parts_b = _branch_parts(branch_id_b)
    depth = 0
    for aa, bb in zip(parts_a, parts_b):
        if aa != bb:
            break
        if aa == "b0":
            depth = 0
        else:
            depth += 1
    return depth


def tree_distance(a: BranchRecord, b: BranchRecord) -> int:
    """Finite branch-tree path distance through the lowest common ancestor."""

    ancestor_depth = lca_depth(a.branch_id, b.branch_id)
    return (a.depth - ancestor_depth) + (b.depth - ancestor_depth)


def memory_divergence(a: BranchRecord, b: BranchRecord) -> int:
    """Length of the non-common suffixes after the longest common memory prefix."""

    common = 0
    for aa, bb in zip(a.memory, b.memory):
        if aa != bb:
            break
        common += 1
    return (len(a.memory) - common) + (len(b.memory) - common)


def decoherence_entry(
    a: BranchRecord,
    b: BranchRecord,
    config: ObserverCommitmentConfig | None = None,
) -> dict[str, float | int | bool | str]:
    """Return the finite R-009 branch-separation/decoherence score.

    The score is

    ``D_ij = sqrt(mu_i mu_j) exp[-gamma_B d_T - gamma_M d_M - gamma_O d_O]
             exp[i phase_scale(phi_i - phi_j)]``.

    It is a bounded finite overlap score.  It is not asserted to be a complete
    quantum decoherence functional or physical density matrix.
    """

    cfg = config or ObserverCommitmentConfig()
    if a.weight < 0.0 or b.weight < 0.0:
        raise ValueError("weights must be non-negative")
    d_t = tree_distance(a, b)
    d_m = memory_divergence(a, b)
    d_o = abs(a.observation_count - b.observation_count)
    magnitude = sqrt(a.weight * b.weight) * exp(
        -cfg.gamma_branch * d_t
        - cfg.gamma_memory * d_m
        - cfg.gamma_observation * d_o
    )
    phase = cfg.phase_scale * (a.phase - b.phase)
    return {
        "branch_i": a.branch_id,
        "branch_j": b.branch_id,
        "tree_distance": d_t,
        "memory_divergence": d_m,
        "observation_count_distance": d_o,
        "magnitude": magnitude,
        "real": magnitude * cos(phase),
        "imag": magnitude * sin(phase),
        "phase": phase,
        "suppressed": magnitude <= cfg.decoherence_threshold,
    }


def decoherence_summary(
    leaves: Sequence[BranchRecord],
    config: ObserverCommitmentConfig | None = None,
) -> dict[str, object]:
    """Summarize finite diagonal trace and off-diagonal suppression."""

    cfg = config or ObserverCommitmentConfig()
    validate_probability_weights(leaves, tolerance=cfg.probability_tolerance)
    offdiag: list[float] = []
    suppressed = 0
    pair_count = 0
    for i, a in enumerate(leaves):
        for b in leaves[i + 1 :]:
            entry = decoherence_entry(a, b, cfg)
            magnitude = float(entry["magnitude"])
            offdiag.append(magnitude)
            pair_count += 1
            if bool(entry["suppressed"]):
                suppressed += 1
    diagonal_trace = sum(leaf.weight for leaf in leaves)
    return {
        "leaf_count": len(leaves),
        "pair_count": pair_count,
        "diagonal_trace": diagonal_trace,
        "max_offdiag_magnitude": max(offdiag) if offdiag else 0.0,
        "mean_offdiag_magnitude": sum(offdiag) / len(offdiag) if offdiag else 0.0,
        "suppressed_pair_fraction": suppressed / pair_count if pair_count else 1.0,
        "threshold": cfg.decoherence_threshold,
        "passed_trace_invariant": abs(diagonal_trace - 1.0) <= cfg.probability_tolerance,
    }


# Deterministic demonstration frontier --------------------------------------


@dataclass(frozen=True)
class DemoBranchMeasureConfig:
    """R-008-compatible deterministic branch allocation for R-009 artifacts."""

    beta: float = 1.0
    shell_weight: float = 0.05
    defect_weight: float = 0.35
    memory_weight: float = 0.0
    coherence_weight: float = 0.20
    transfer_weight: float = 0.25
    transfer_probability: float = 0.05
    epsilon: float = 1.0e-15
    phase_scale: float = 1.0

    def to_branch_measure_config(self) -> BranchMeasureConfig:
        """Return the canonical R-008 configuration used by the demo tree."""

        return BranchMeasureConfig(
            beta=self.beta,
            shell_weight=self.shell_weight,
            defect_weight=self.defect_weight,
            memory_weight=self.memory_weight,
            coherence_weight=self.coherence_weight,
            transfer_weight=self.transfer_weight,
            transfer_probability=self.transfer_probability,
            epsilon=self.epsilon,
            phase_scale=self.phase_scale,
        )


def _demo_observation_token(parent: BranchRecord, shell_q: int, depth: int, child_index: int) -> str | None:
    if shell_q in (2, 4) or ((depth + child_index + shell_q) % 5 == 0):
        return f"t{depth}:q{shell_q}:r{(child_index + parent.observation_count) % 3}"
    return None


def _demo_children(parent: BranchRecord) -> tuple[BranchChild, ...]:
    depth = parent.depth + 1
    children: list[BranchChild] = []
    for idx, shell_q in enumerate(range(5)):
        coherence_loss = ((shell_q * shell_q + depth + idx) % 7) / 6.0
        defect_count = 1 if shell_q in (3, 4) and (depth + idx) % 2 == 0 else 0
        children.append(
            BranchChild(
                branch_id=f"{parent.branch_id}.{shell_q}",
                parent_id=parent.branch_id,
                shell_q=shell_q,
                action=0.07 * depth + 0.11 * idx,
                defect_count=defect_count,
                memory_delta=0,
                coherence_penalty=coherence_loss,
            )
        )
    return tuple(children)


def demo_expand_tree(
    *,
    max_depth: int = 4,
    measure_config: DemoBranchMeasureConfig | None = None,
) -> list[BranchRecord]:
    """Build the deterministic finite R-009 demonstration branch tree."""

    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")
    cfg = measure_config or DemoBranchMeasureConfig()
    root = BranchRecord(
        branch_id="b0",
        parent_id=None,
        depth=0,
        weight=1.0,
        memory=(),
        phase=0.0,
        observation_token=None,
    )
    nodes = [root]
    frontier = [root]
    for depth in range(1, max_depth + 1):
        next_frontier: list[BranchRecord] = []
        for parent in frontier:
            branch_rows = allocate_branch_measure(
                parent.weight,
                _demo_children(parent),
                cfg.to_branch_measure_config(),
            )
            for idx, branch_row in enumerate(branch_rows):
                shell_q = int(branch_row.branch_id.rsplit(".", 1)[1])
                token = _demo_observation_token(parent, shell_q, depth, idx)
                child = BranchRecord(
                    branch_id=branch_row.branch_id,
                    parent_id=parent.branch_id,
                    depth=depth,
                    weight=branch_row.measure,
                    memory=commit_memory(parent.memory, token),
                    phase=parent.phase + cfg.phase_scale * branch_row.score,
                    observation_token=token,
                )
                nodes.append(child)
                next_frontier.append(child)
        frontier = next_frontier
    return nodes


def frontier(records: Sequence[BranchRecord], depth: int | None = None) -> list[BranchRecord]:
    """Return all records at a depth, defaulting to the deepest frontier."""

    if not records:
        raise ValueError("records must be non-empty")
    if depth is None:
        depth = max(record.depth for record in records)
    return [record for record in records if record.depth == depth]


def record_to_row(record: BranchRecord) -> dict[str, object]:
    """Convert a branch record to a CSV/JSON-friendly row."""

    return {
        "branch_id": record.branch_id,
        "parent_id": record.parent_id or "",
        "depth": record.depth,
        "weight": record.weight,
        "phase": record.phase,
        "observation_token": record.observation_token or "",
        "memory_length": len(record.memory),
        "memory_record": record.memory_record,
        "memory_hash": record.memory_hash,
    }


def verify_r009(
    *,
    max_depth: int = 4,
    config: ObserverCommitmentConfig | None = None,
) -> dict[str, object]:
    """Run deterministic finite R-009 invariants on the demonstration tree."""

    cfg = config or ObserverCommitmentConfig()
    records = demo_expand_tree(max_depth=max_depth)
    leaves = frontier(records, max_depth)
    validate_probability_weights(leaves, tolerance=cfg.probability_tolerance)
    distribution = commitment_distribution(leaves)
    normalize_commitment_distribution(distribution, tolerance=cfg.probability_tolerance)
    memory_prefix_ok = verify_memory_prefix_embedding(records)
    summary = decoherence_summary(leaves, cfg)
    total_leaf_weight = sum(leaf.weight for leaf in leaves)
    total_distribution_weight = sum(float(row["measure"]) for row in distribution)
    passed = (
        abs(total_leaf_weight - 1.0) <= cfg.probability_tolerance
        and abs(total_distribution_weight - 1.0) <= cfg.probability_tolerance
        and memory_prefix_ok
        and bool(summary["passed_trace_invariant"])
    )
    return {
        "law_version": cfg.law_version,
        "max_depth": max_depth,
        "node_count": len(records),
        "frontier_size": len(leaves),
        "frontier_measure_total": total_leaf_weight,
        "commitment_memory_classes": len(distribution),
        "commitment_distribution_total": total_distribution_weight,
        "memory_prefix_embedding_passed": memory_prefix_ok,
        "decoherence_summary": summary,
        "passed": passed,
        "boundary": BOUNDARY_STATEMENT,
    }


def verification_json(*, max_depth: int = 4) -> str:
    """Return sorted JSON for deterministic R-009 verification."""

    return json.dumps(verify_r009(max_depth=max_depth), indent=2, sort_keys=True)
