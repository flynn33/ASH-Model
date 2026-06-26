#!/usr/bin/env python
"""Generate R-010 unit-bearing bridge artifacts.

This script is deterministic. It accepts upstream R-009 CSV outputs when present,
while also supporting the R-010 packaged synthetic fixture inputs for standalone
verification.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ash_model.unit_bridge import (  # noqa: E402
    bootstrap_covariance,
    bootstrap_observable_samples,
    finite_features_by_depth,
    load_calibration,
    normalize_frontier_columns,
    physical_bridge,
    read_csv_records,
    validate_unit_bridge_artifacts,
    write_csv_records,
)


def _first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("none of these candidate paths exist: " + ", ".join(str(p) for p in paths))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-root", default=".", help="repository root")
    parser.add_argument("--bootstrap-samples", type=int, default=600)
    parser.add_argument("--seed", type=int, default=10010)
    parser.add_argument("--frontier", default=None, help="optional explicit R-009 frontier CSV")
    parser.add_argument("--decoherence", default=None, help="optional explicit R-009 decoherence summary CSV")
    parser.add_argument("--calibration", default=None, help="optional explicit R-010 calibration contract JSON")
    args = parser.parse_args()

    root = Path(args.out_root).resolve()
    data_dir = root / "data" / "ash-cosmology" / "unit-bridge" / "v0.1"
    validation_dir = root / "validation" / "unit-bridge" / "roadmap-010" / "outputs"
    data_dir.mkdir(parents=True, exist_ok=True)
    validation_dir.mkdir(parents=True, exist_ok=True)

    frontier_path = Path(args.frontier) if args.frontier else _first_existing(
        [
            root / "data" / "ash-cosmology" / "observer-commitment" / "v0.1" / "r009_frontier.csv",
            data_dir / "r009_frontier_assumed_input.csv",
        ]
    )
    decoherence_path = Path(args.decoherence) if args.decoherence else _first_existing(
        [
            root / "data" / "ash-cosmology" / "observer-commitment" / "v0.1" / "r009_decoherence_summary_by_depth.csv",
            data_dir / "r009_decoherence_assumed_input.csv",
        ]
    )
    calibration_path = Path(args.calibration) if args.calibration else root / "config" / "ash_r010_unit_bridge_calibration.json"

    frontier = normalize_frontier_columns(read_csv_records(frontier_path))
    decoherence = read_csv_records(decoherence_path)
    calibration = load_calibration(calibration_path)

    features = finite_features_by_depth(frontier, decoherence)
    observables = physical_bridge(features, calibration)
    bootstrap_samples = bootstrap_observable_samples(
        frontier,
        decoherence,
        calibration,
        samples=args.bootstrap_samples,
        seed=args.seed,
    )
    covariance = bootstrap_covariance(
        frontier,
        decoherence,
        calibration,
        samples=args.bootstrap_samples,
        seed=args.seed,
    )

    features_path = data_dir / "r010_finite_bridge_features.csv"
    observables_path = data_dir / "r010_unit_bearing_observables.csv"
    samples_path = data_dir / "r010_bootstrap_samples_final_depth.csv"
    covariance_path = data_dir / "r010_bootstrap_covariance_final_depth.csv"

    write_csv_records(features_path, features, fieldnames=list(features[0]))
    write_csv_records(observables_path, observables, fieldnames=list(observables[0]))
    write_csv_records(samples_path, bootstrap_samples, fieldnames=list(bootstrap_samples[0]))
    write_csv_records(covariance_path, covariance, fieldnames=list(covariance[0]))

    validation = validate_unit_bridge_artifacts(features, observables, calibration, covariance).as_dict()
    validation["inputs"] = {
        "frontier": str(frontier_path.relative_to(root) if frontier_path.is_relative_to(root) else frontier_path),
        "decoherence": str(decoherence_path.relative_to(root) if decoherence_path.is_relative_to(root) else decoherence_path),
        "calibration": str(calibration_path.relative_to(root) if calibration_path.is_relative_to(root) else calibration_path),
    }
    validation["outputs"] = {
        "features": str(features_path.relative_to(root)),
        "observables": str(observables_path.relative_to(root)),
        "bootstrap_samples": str(samples_path.relative_to(root)),
        "covariance": str(covariance_path.relative_to(root)),
    }
    validation["assumptions"] = [
        "R-008 accepted: normalized branch measure.",
        "R-009 accepted: observer commitment memory and decoherence rule.",
        "Default calibration is synthetic and fiducial; no empirical validation is claimed.",
    ]

    verification_path = validation_dir / "verification.json"
    verification_path.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
