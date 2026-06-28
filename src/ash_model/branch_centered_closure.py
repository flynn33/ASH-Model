"""Roadmap R-016 branch-centered ASH model closure workbench.

This module verifies a finite repository-level closure certificate for the
branch-centered ASH cosmology model.  It is a contract/readiness verifier:
it records that the required finite/computational/model-contract components
are present and boundary language is explicit.

It does not validate empirical cosmology, prove a continuum metric, prove a
Born rule, or assert physical preference over matched baselines.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_COMPONENT_SYMBOLS: tuple[str, ...] = (
    "Omega",
    "C,D",
    "Gamma",
    "T",
    "mu",
    "C_commit",
    "M",
    "B_l",
    "limit",
    "background",
    "perturbations",
    "likelihoods",
    "predictions",
)

REQUIRED_FALSIFICATION_GATES: tuple[str, ...] = (
    "internal consistency",
    "LCDM matched baseline",
    "external likelihood",
    "prediction immutability",
    "bridge semantics",
)

NON_EMPIRICAL_STATUS_MARKER = "not empirically validated"


@dataclass(frozen=True)
class ClosurePaths:
    """Resolved repository paths for the R-016 closure artifacts."""

    root: Path
    component_matrix: Path
    falsification_matrix: Path
    closure_certificate: Path
    verification_summary: Path
    formal_expressions: Path

    @classmethod
    def from_root(cls, root: str | Path = ".") -> "ClosurePaths":
        root_path = Path(root)
        base = root_path / "data" / "ash-cosmology" / "branch-centered-closure" / "v0.1"
        validation = (
            root_path
            / "validation"
            / "branch-centered-closure"
            / "roadmap-016"
            / "outputs"
        )
        docs = (
            root_path
            / "docs"
            / "ash-cosmology"
            / "branch-centered-closure"
            / "roadmap-016"
        )
        return cls(
            root=root_path,
            component_matrix=base / "r016_model_component_closure_matrix.csv",
            falsification_matrix=base / "r016_falsification_gate_matrix.csv",
            closure_certificate=validation / "r016_closure_certificate.json",
            verification_summary=validation / "verification.json",
            formal_expressions=docs / "r016_formal_expressions.json",
        )


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 digest for *path*."""

    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_component_matrix(root: str | Path = ".") -> list[dict[str, str]]:
    """Load the R-016 model component closure matrix."""

    return _read_csv_rows(ClosurePaths.from_root(root).component_matrix)


def load_falsification_matrix(root: str | Path = ".") -> list[dict[str, str]]:
    """Load the R-016 falsification gate matrix."""

    return _read_csv_rows(ClosurePaths.from_root(root).falsification_matrix)


def verify_branch_centered_closure(root: str | Path = ".") -> dict[str, Any]:
    """Verify repository-local R-016 formal closure artifacts.

    The result is suitable for deterministic tests and validation reports.
    ``closed_formal_candidate`` is true only when every required component and
    falsification gate is present, the certificate retains the non-empirical
    status marker, and the formal expression file exists.
    """

    paths = ClosurePaths.from_root(root)
    components = load_component_matrix(root)
    gates = load_falsification_matrix(root)
    certificate = _read_json(paths.closure_certificate)
    summary = _read_json(paths.verification_summary)
    formal = _read_json(paths.formal_expressions)

    present_symbols = {row.get("symbol", "") for row in components}
    present_gates = {row.get("gate", "") for row in gates}
    missing_components = [
        symbol for symbol in REQUIRED_COMPONENT_SYMBOLS if symbol not in present_symbols
    ]
    missing_gates = [
        gate for gate in REQUIRED_FALSIFICATION_GATES if gate not in present_gates
    ]
    scientific_status = str(certificate.get("scientific_status", ""))
    non_empirical_boundary = NON_EMPIRICAL_STATUS_MARKER in scientific_status

    upstream_hashes = certificate.get("upstream_assumed_accepted", {})
    expected_upstream = {f"R{index:03d}" for index in range(9, 16)}
    missing_upstream_hashes = sorted(expected_upstream - set(upstream_hashes))

    return {
        "roadmap_id": "R-016",
        "component_count": len(components),
        "required_component_count": len(REQUIRED_COMPONENT_SYMBOLS),
        "missing_components": missing_components,
        "falsification_gate_count": len(gates),
        "missing_falsification_gates": missing_gates,
        "closure_certificate_sha256": sha256_file(paths.closure_certificate),
        "verification_summary_sha256": sha256_file(paths.verification_summary),
        "formal_model_tuple": formal.get("model_tuple"),
        "closure_predicate": formal.get("closure_predicate"),
        "upstream_hashes_recorded": sorted(upstream_hashes),
        "missing_upstream_hashes": missing_upstream_hashes,
        "scientific_status": scientific_status,
        "non_empirical_boundary": non_empirical_boundary,
        "external_empirical_status": summary.get("external_empirical_status"),
        "closed_formal_candidate": (
            not missing_components
            and not missing_gates
            and not missing_upstream_hashes
            and non_empirical_boundary
        ),
    }


def branch_centered_model_card(root: str | Path = ".") -> dict[str, Any]:
    """Return a compact R-016 model-card summary."""

    paths = ClosurePaths.from_root(root)
    certificate = _read_json(paths.closure_certificate)
    return {
        "model_name": certificate.get("model_name"),
        "closure_date": certificate.get("closure_date"),
        "scientific_status": certificate.get("scientific_status"),
        "definition_components": certificate.get("definition_components", []),
        "synthetic_closure_observables": certificate.get(
            "synthetic_closure_observables", {}
        ),
    }
