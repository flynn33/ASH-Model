"""
R-010 unit-bearing bridge workbench for ASH Cosmology.

This module implements a deterministic finite branch-ensemble bridge from
R-008/R-009 branch outputs to named unit-bearing proxy observables.

Layer classification:
- Layer 1: finite expectations, entropies, normalization, and covariance checks.
- Layer 2: deterministic computation from finite CSV/table inputs.
- Layer 3: interpretive physical-observable naming; fiducial only.

Boundary:
The bridge has SI units and a versioned calibration contract, but the default
constants are synthetic fiducials. This module does not derive a continuum
metric, FRW limit, Einstein equations, external likelihood, or empirical
cosmology.
"""
from __future__ import annotations

from dataclasses import dataclass
import csv
import json
import math
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy as np


BRIDGE_VERSION = "ash-r010-unit-bridge-v0.1"

FEATURE_COLUMNS = [
    "depth",
    "measure_sum",
    "mean_shell_q",
    "var_shell_q",
    "defect_rate",
    "mean_memory_length",
    "branch_entropy_bits",
    "memory_entropy_bits",
    "suppressed_pair_fraction",
    "max_offdiag_magnitude",
]

OBSERVABLE_COLUMNS = [
    "depth",
    "measure_sum",
    "mean_shell_q",
    "var_shell_q",
    "defect_rate",
    "mean_memory_length",
    "branch_entropy_bits",
    "memory_entropy_bits",
    "suppressed_pair_fraction",
    "max_offdiag_magnitude",
    "time_s",
    "coarse_length_m",
    "scale_factor_dimensionless",
    "H_bridge_s_inv",
    "energy_density_J_m3",
    "mass_density_kg_m3",
    "einstein_curvature_proxy_m_inv2",
    "memory_length_m",
    "temperature_proxy_K",
]

COVARIANCE_OBSERVABLE_COLUMNS = [
    "coarse_length_m",
    "energy_density_J_m3",
    "mass_density_kg_m3",
    "memory_length_m",
    "temperature_proxy_K",
]

REQUIRED_FRONTIER_COLUMNS = {
    "depth",
    "measure",
    "shell_q",
    "defect_count",
    "memory_length",
    "memory_hash",
}

LIVE_R009_FRONTIER_COLUMNS = {
    "branch_id",
    "depth",
    "weight",
    "memory_length",
    "memory_hash",
}

REQUIRED_CALIBRATION_CONSTANTS = [
    "tau_star_s",
    "ell_star_m",
    "epsilon_star_J",
    "alpha_entropy",
    "theta_shell_K",
    "theta0_K",
    "G_m3_kg_s2",
    "c_m_s",
]

CSV_NULL_TOKENS = {"", "nan", "NaN", "None", "null"}


@dataclass(frozen=True)
class UnitBridgeValidation:
    """Small validation record for generated R-010 artifacts."""

    measure_normalization_by_depth: bool
    unit_columns_present: bool
    positive_declared_scales: bool
    finite_physical_values: bool
    covariance_symmetric: bool
    covariance_psd_tolerance_1e_minus_12: bool
    covariance_min_eigenvalue: float | None

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": "ash-r010-validation-v0.1",
            "bridge_version": BRIDGE_VERSION,
            "tests": {
                "measure_normalization_by_depth": self.measure_normalization_by_depth,
                "unit_columns_present": self.unit_columns_present,
                "positive_declared_scales": self.positive_declared_scales,
                "finite_physical_values": self.finite_physical_values,
                "covariance_symmetric": self.covariance_symmetric,
                "covariance_psd_tolerance_1e_minus_12": self.covariance_psd_tolerance_1e_minus_12,
                "covariance_min_eigenvalue": self.covariance_min_eigenvalue,
            },
            "boundary": (
                "Synthetic finite-observer unit bridge only; no empirical "
                "cosmology, continuum metric, FRW limit, or external likelihood."
            ),
        }


def read_csv_records(path: str | Path) -> list[dict[str, object]]:
    """Read a CSV table as dictionaries with numeric values parsed when possible."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [_parse_csv_row(row) for row in csv.DictReader(handle)]


def write_csv_records(
    path: str | Path,
    rows: Sequence[Mapping[str, object]],
    fieldnames: Sequence[str],
) -> None:
    """Write dictionaries as a deterministic CSV table."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(row.get(key)) for key in fieldnames})


def entropy_bits(probabilities: Sequence[float]) -> float:
    """Return Shannon entropy in bits for a finite nonnegative law."""

    p = np.asarray(probabilities, dtype=float)
    if np.any(~np.isfinite(p)) or np.any(p < 0):
        raise ValueError("probabilities must be finite and nonnegative")
    p = p[p > 0]
    if p.size == 0:
        return 0.0
    return float(-(p * np.log2(p)).sum())


def normalize_frontier_columns(frontier: object) -> list[dict[str, object]]:
    """Return an R-010 frontier table with canonical measure and feature columns.

    Standalone R-010 fixture files already contain the canonical columns. The
    live R-009 repository CSV stores the branch measure as ``weight`` and omits
    the deterministic demo shell/defect columns; those are reconstructed from
    the R-009 branch path convention and demo child rule.
    """

    rows = _records(frontier)
    normalized: list[dict[str, object]] = []
    for row in rows:
        out = dict(row)
        if "measure" not in out and "weight" in out:
            out["measure"] = out["weight"]
        if "shell_q" not in out and LIVE_R009_FRONTIER_COLUMNS <= set(out):
            out["shell_q"] = _shell_from_branch_id(out["branch_id"])
        if "defect_count" not in out and {"depth", "shell_q"} <= set(out):
            out["defect_count"] = _demo_defect_from_depth_shell(out["depth"], out["shell_q"])
        normalized.append(out)
    return normalized


def finite_features_by_depth(
    frontier: object,
    decoherence: object | None = None,
) -> list[dict[str, object]]:
    """Compute the finite R-010 feature vector by branch depth."""

    normalized = normalize_frontier_columns(frontier)
    _require_columns(normalized, REQUIRED_FRONTIER_COLUMNS, "frontier")
    if not normalized:
        raise ValueError("frontier must contain at least one branch row")

    decoherence_rows = [] if decoherence is None else _records(decoherence)
    rows: list[dict[str, object]] = []
    for depth, group in sorted(_group_by(normalized, "depth").items()):
        mu = np.asarray([_finite_float(row["measure"], "measure") for row in group], dtype=float)
        if np.any(mu < 0) or float(mu.sum()) <= 0.0:
            raise ValueError(f"depth {depth} has invalid branch measure")
        mu = mu / float(mu.sum())

        q = np.asarray([_finite_float(row["shell_q"], "shell_q") for row in group], dtype=float)
        defect = np.asarray([_finite_float(row["defect_count"], "defect_count") for row in group], dtype=float)
        memory_length = np.asarray(
            [_finite_float(row["memory_length"], "memory_length") for row in group],
            dtype=float,
        )

        memory_totals: dict[str, float] = {}
        for row, probability in zip(group, mu, strict=True):
            key = str(row["memory_hash"])
            memory_totals[key] = memory_totals.get(key, 0.0) + float(probability)

        decrow = _decoherence_row_for_depth(decoherence_rows, int(depth))
        mean_q = float(np.dot(mu, q))
        rows.append(
            {
                "depth": int(depth),
                "measure_sum": float(mu.sum()),
                "mean_shell_q": mean_q,
                "var_shell_q": float(np.dot(mu, (q - mean_q) ** 2)),
                "defect_rate": float(np.dot(mu, defect)),
                "mean_memory_length": float(np.dot(mu, memory_length)),
                "branch_entropy_bits": entropy_bits(mu),
                "memory_entropy_bits": entropy_bits(list(memory_totals.values())),
                "suppressed_pair_fraction": _optional_float(decrow.get("suppressed_pair_fraction")),
                "max_offdiag_magnitude": _optional_float(decrow.get("max_offdiag_magnitude")),
            }
        )

    return rows


def load_calibration(path: str | Path) -> dict[str, object]:
    """Load and validate the R-010 calibration contract."""

    calibration = json.loads(Path(path).read_text(encoding="utf-8"))
    constants = calibration.get("constants", {})
    if not isinstance(constants, dict):
        raise ValueError("calibration constants must be an object")
    missing = [key for key in REQUIRED_CALIBRATION_CONSTANTS if key not in constants]
    if missing:
        raise ValueError(f"missing calibration constants: {missing}")

    for key in ["tau_star_s", "ell_star_m", "epsilon_star_J", "G_m3_kg_s2", "c_m_s"]:
        entry = constants[key]
        if not isinstance(entry, dict):
            raise ValueError(f"{key} must be an object")
        value = entry.get("value")
        if not isinstance(value, (int, float)) or not math.isfinite(float(value)) or float(value) <= 0.0:
            raise ValueError(f"{key} must be finite and positive")
    return calibration


def declared_constants(calibration: Mapping[str, object]) -> dict[str, float]:
    constants = calibration["constants"]
    if not isinstance(constants, Mapping):
        raise ValueError("calibration constants must be a mapping")
    declared: dict[str, float] = {}
    for key, entry in constants.items():
        if not isinstance(entry, Mapping):
            raise ValueError(f"calibration entry {key!r} must be a mapping")
        declared[str(key)] = float(entry["value"])
    return declared


def physical_bridge(
    features: object,
    calibration: Mapping[str, object],
) -> list[dict[str, object]]:
    """Map finite features to named unit-bearing proxy observables."""

    feature_rows = _records(features)
    _require_columns(
        feature_rows,
        {"depth", "mean_shell_q", "defect_rate", "mean_memory_length", "branch_entropy_bits"},
        "features",
    )
    if not feature_rows:
        raise ValueError("features must contain at least one row")

    constants = declared_constants(calibration)
    rows = sorted((dict(row) for row in feature_rows), key=lambda row: int(row["depth"]))

    tau = constants["tau_star_s"]
    ell = constants["ell_star_m"]
    epsilon = constants["epsilon_star_J"]
    alpha = constants["alpha_entropy"]
    theta_shell = constants["theta_shell_K"]
    theta0 = constants["theta0_K"]
    gravitational_constant = constants["G_m3_kg_s2"]
    lightspeed = constants["c_m_s"]

    reference_entropy = _finite_float(rows[0]["branch_entropy_bits"], "branch_entropy_bits")
    times = [_finite_float(row["depth"], "depth") * tau for row in rows]
    log_scale_factors: list[float] = []

    for row, time_s in zip(rows, times, strict=True):
        mean_shell_q = _finite_float(row["mean_shell_q"], "mean_shell_q")
        defect_rate = _finite_float(row["defect_rate"], "defect_rate")
        memory_length = _finite_float(row["mean_memory_length"], "mean_memory_length")
        entropy = _finite_float(row["branch_entropy_bits"], "branch_entropy_bits")

        scale_factor = math.exp(alpha * (entropy - reference_entropy))
        log_scale_factors.append(math.log(scale_factor))
        energy_density = (epsilon / (ell**3)) * defect_rate
        row.update(
            {
                "time_s": time_s,
                "coarse_length_m": ell * math.sqrt(max(mean_shell_q, 0.0) / 9.0),
                "scale_factor_dimensionless": scale_factor,
                "H_bridge_s_inv": math.nan,
                "energy_density_J_m3": energy_density,
                "mass_density_kg_m3": energy_density / (lightspeed**2),
                "einstein_curvature_proxy_m_inv2": (
                    (8.0 * math.pi * gravitational_constant / (lightspeed**4)) * energy_density
                ),
                "memory_length_m": ell * memory_length,
                "temperature_proxy_K": theta0 + theta_shell * (mean_shell_q / 9.0),
            }
        )

    for index in range(1, len(rows)):
        dt = times[index] - times[index - 1]
        if not math.isfinite(dt) or dt == 0.0:
            raise ValueError("depth/time sequence must have nonzero finite differences")
        rows[index]["H_bridge_s_inv"] = (log_scale_factors[index] - log_scale_factors[index - 1]) / dt

    return rows


def bootstrap_observable_samples(
    frontier: object,
    decoherence: object,
    calibration: Mapping[str, object],
    samples: int = 600,
    seed: int = 10010,
) -> list[dict[str, float]]:
    """Bootstrap final-depth samples for selected unit-bearing observables."""

    if samples < 2:
        raise ValueError("samples must be at least 2")
    frontier_rows = normalize_frontier_columns(frontier)
    decoherence_rows = _records(decoherence)
    depth = max(int(row["depth"]) for row in frontier_rows)
    group = [row for row in frontier_rows if int(row["depth"]) == depth]
    if not group:
        raise ValueError("frontier final depth has no rows")

    p = np.asarray([_finite_float(row["measure"], "measure") for row in group], dtype=float)
    p = p / float(p.sum())
    rng = np.random.default_rng(seed)
    depth_decoherence = [row for row in decoherence_rows if int(row.get("depth", -1)) == depth]

    values: list[dict[str, float]] = []
    for _ in range(samples):
        indices = rng.choice(len(group), size=len(group), replace=True, p=p)
        sample = [dict(group[int(index)]) for index in indices]
        uniform_measure = 1.0 / len(sample)
        for row in sample:
            row["measure"] = uniform_measure
        features = finite_features_by_depth(sample, depth_decoherence)
        physical = physical_bridge(features, calibration)[0]
        values.append({column: float(physical[column]) for column in COVARIANCE_OBSERVABLE_COLUMNS})

    return values


def bootstrap_covariance(
    frontier: object,
    decoherence: object,
    calibration: Mapping[str, object],
    samples: int = 600,
    seed: int = 10010,
) -> list[dict[str, object]]:
    """Bootstrap final-depth covariance for selected unit-bearing observables."""

    sample_rows = bootstrap_observable_samples(frontier, decoherence, calibration, samples=samples, seed=seed)
    matrix = np.cov(
        np.asarray([[row[column] for column in COVARIANCE_OBSERVABLE_COLUMNS] for row in sample_rows], dtype=float),
        rowvar=False,
    )
    return [
        {
            "observable": row_name,
            **{
                column: float(matrix[row_index, column_index])
                for column_index, column in enumerate(COVARIANCE_OBSERVABLE_COLUMNS)
            },
        }
        for row_index, row_name in enumerate(COVARIANCE_OBSERVABLE_COLUMNS)
    ]


def validate_unit_bridge_artifacts(
    features: object,
    observables: object,
    calibration: Mapping[str, object],
    covariance: object | None = None,
) -> UnitBridgeValidation:
    """Validate generated R-010 data products."""

    feature_rows = _records(features)
    observable_rows = _records(observables)
    positive_scales = True
    try:
        constants = declared_constants(calibration)
        for key in ["tau_star_s", "ell_star_m", "epsilon_star_J", "G_m3_kg_s2", "c_m_s"]:
            positive_scales = positive_scales and math.isfinite(constants[key]) and constants[key] > 0
    except Exception:
        positive_scales = False

    unit_columns_present = _has_columns(observable_rows, OBSERVABLE_COLUMNS)
    finite_columns = [column for column in OBSERVABLE_COLUMNS if column != "H_bridge_s_inv"]
    finite_physical = unit_columns_present and all(
        math.isfinite(_finite_float(row[column], column))
        for row in observable_rows
        for column in finite_columns
    )
    if unit_columns_present and len(observable_rows) > 1:
        finite_physical = finite_physical and all(
            math.isfinite(_finite_float(row["H_bridge_s_inv"], "H_bridge_s_inv"))
            for row in observable_rows[1:]
        )

    cov_symmetric = False
    cov_psd = False
    min_eig: float | None = None
    if covariance is not None:
        mat = covariance_matrix(covariance)
        cov_symmetric = bool(np.allclose(mat, mat.T))
        eig = np.linalg.eigvalsh((mat + mat.T) / 2.0)
        min_eig = float(eig.min())
        cov_psd = bool(min_eig >= -1e-12)

    return UnitBridgeValidation(
        measure_normalization_by_depth=bool(
            all(abs(_finite_float(row["measure_sum"], "measure_sum") - 1.0) < 1.0e-12 for row in feature_rows)
        ),
        unit_columns_present=bool(unit_columns_present),
        positive_declared_scales=bool(positive_scales),
        finite_physical_values=bool(finite_physical),
        covariance_symmetric=bool(cov_symmetric),
        covariance_psd_tolerance_1e_minus_12=bool(cov_psd),
        covariance_min_eigenvalue=min_eig,
    )


def covariance_matrix(covariance: object) -> np.ndarray:
    """Return a covariance matrix ordered by COVARIANCE_OBSERVABLE_COLUMNS."""

    rows = _records(covariance)
    if not rows:
        raise ValueError("covariance must contain rows")
    if "observable" in rows[0]:
        by_name = {str(row["observable"]): row for row in rows}
        return np.asarray(
            [
                [_finite_float(by_name[row_name][column], column) for column in COVARIANCE_OBSERVABLE_COLUMNS]
                for row_name in COVARIANCE_OBSERVABLE_COLUMNS
            ],
            dtype=float,
        )
    return np.asarray(
        [[_finite_float(row[column], column) for column in COVARIANCE_OBSERVABLE_COLUMNS] for row in rows],
        dtype=float,
    )


def _parse_csv_row(row: Mapping[str, str]) -> dict[str, object]:
    return {key: _parse_csv_value(value) for key, value in row.items() if key is not None}


def _parse_csv_value(value: str) -> object:
    if value in CSV_NULL_TOKENS:
        return math.nan
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    if math.isfinite(number) and number.is_integer() and "e" not in value.lower() and "." not in value:
        return int(number)
    return number


def _csv_value(value: object) -> object:
    if isinstance(value, float) and math.isnan(value):
        return "nan"
    return value


def _records(table: object) -> list[dict[str, object]]:
    if isinstance(table, Mapping):
        return [dict(table)]
    to_dict = getattr(table, "to_dict", None)
    if callable(to_dict):
        try:
            return [dict(row) for row in to_dict("records")]
        except TypeError:
            pass
    if isinstance(table, Iterable):
        return [dict(row) for row in table]  # type: ignore[arg-type]
    raise TypeError("table must be a mapping sequence")


def _require_columns(rows: Sequence[Mapping[str, object]], required: set[str], label: str) -> None:
    columns = set(rows[0]) if rows else set()
    missing = sorted(required - columns)
    if missing:
        raise ValueError(f"{label} missing required columns: {missing}")


def _has_columns(rows: Sequence[Mapping[str, object]], required: Sequence[str]) -> bool:
    return bool(rows) and all(column in rows[0] for column in required)


def _group_by(rows: Sequence[Mapping[str, object]], key: str) -> dict[int, list[Mapping[str, object]]]:
    groups: dict[int, list[Mapping[str, object]]] = {}
    for row in rows:
        value = int(row[key])
        groups.setdefault(value, []).append(row)
    return groups


def _decoherence_row_for_depth(rows: Sequence[Mapping[str, object]], depth: int) -> Mapping[str, object]:
    for row in rows:
        if int(row.get("depth", -1)) == depth:
            return row
    return {}


def _finite_float(value: object, label: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} contains nonfinite values")
    return result


def _optional_float(value: object) -> float:
    if value is None:
        return math.nan
    result = float(value)
    return result if math.isfinite(result) else math.nan


def _shell_from_branch_id(branch_id: object) -> int:
    try:
        shell = int(str(branch_id).rsplit(".", 1)[1])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"cannot derive shell_q from branch_id {branch_id!r}") from exc
    if shell < 0:
        raise ValueError(f"derived shell_q must be nonnegative for branch_id {branch_id!r}")
    return shell


def _demo_defect_from_depth_shell(depth: object, shell_q: object) -> int:
    depth_int = int(depth)
    shell_int = int(shell_q)
    return int(shell_int in (3, 4) and ((depth_int + shell_int) % 2 == 0))
