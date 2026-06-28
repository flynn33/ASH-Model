#!/usr/bin/env python3
"""Run exhaustive finite checks and write machine-readable proof certificates."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ash_model.adinkra import adinkra_certificate
from ash_model.bits import flip_bit, is_integrity_valid, xor_bits
from ash_model.branch_centered_closure import (
    REQUIRED_COMPONENT_SYMBOLS,
    branch_centered_model_card,
    verify_branch_centered_closure,
)
from ash_model.branching import branch_certificate
from ash_model.code import CODEWORDS, code_certificate, decode, decode_affine
from ash_model.cosmology import (
    FlatLambdaCDMParameters,
    compare_distance_baselines,
    dimensionless_hubble_parameter,
    flat_lcdm_distance_curve,
    normalized_comoving_distance,
)
from ash_model.empirical import (
    ObservableCalibration,
    calibrate_observable,
    chi_square,
    compare_gaussian_models,
    diagonal_gaussian_log_likelihood,
)
from ash_model.finite_observer_limit import (
    ODD_LEVELS,
    adjacency_spectrum as finite_observer_adjacency_spectrum,
    causal_cone_sizes,
    causal_interval_size,
    fiber_sizes,
    laplacian_gap as finite_observer_laplacian_gap,
    shell_counts as finite_observer_shell_counts,
    unit_scale_table,
    validate_lipschitz,
    validate_projective_consistency,
    validation_summary as finite_observer_validation_summary,
)
from ash_model.locked_predictions import LOCKED_PREDICTION_IDS, verify_lock
from ash_model.observer_commitment import verify_r009
from ash_model.hypercube import (
    coset_partition,
    distance_shell_counts,
    even_parity_shell_counts,
    hypercube_adjacency_spectrum,
    hypercube_edge_count,
    hypercube_laplacian_spectrum,
    integrity_states,
    pair_flip_adjacency_spectrum,
    pair_flip_graph_degree,
    pair_flip_graph_edge_count,
    pair_flip_laplacian_spectrum,
    state_reference_rows,
    states,
    theoretical_plane_counts,
)
from ash_model.physics import (
    background_moments,
    bridge_observables,
    evolve_weight_distribution,
    lazy_pair_flip_eigenvalue,
    pair_flip_generator,
    pair_flip_transition,
    physical_state_space,
    uniform_background_distribution,
    uniform_physical_distribution,
    weight_level_degeneracies,
    weight_background_kernel,
)
from ash_model.prediction_ledger import canonical_prediction_hash, ledger_lock_status, validate_prediction_ledger
from ash_model.projection import projection_certificate
from ash_model.simulation import binomial_distribution, noise_kernel
from ash_model.unit_bridge import (
    bootstrap_covariance,
    finite_features_by_depth,
    load_calibration,
    physical_bridge,
    read_csv_records,
    validate_unit_bridge_artifacts,
)


def _reported_residual(value: float) -> float:
    """Return stable proof-certificate residuals across BLAS/platform noise."""

    residual = float(value)
    if abs(residual) < 1e-15:
        return 0.0
    return residual


def _source_manifest() -> dict[str, str]:
    suffixes = {".py", ".json", ".toml", ".md", ".tex", ".yml", ".yaml", ".cff"}
    filenames = {"LICENSE", "VERSION", ".gitignore"}
    excluded_prefixes = ("proofs/",)
    excluded_paths = {
        "docs/remediation/final-remediation-evidence.json",
        "docs/remediation/physics-readiness.json",
    }
    manifest: dict[str, str] = {}
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in suffixes and path.name not in filenames:
            continue
        relative = path.relative_to(REPO_ROOT).as_posix()
        if (
            relative in excluded_paths
            or relative.startswith(excluded_prefixes)
            or "/__pycache__/" in f"/{relative}/"
            or "/.pytest_cache/" in f"/{relative}/"
        ):
            continue
        manifest[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return manifest


def _decoder_certificate() -> dict[str, object]:
    status_counts: Counter[str] = Counter()
    nearest_counts: Counter[tuple[int, int]] = Counter()
    for state in product((0, 1), repeat=9):
        result = decode(state)
        status_counts[result.status] += 1
        nearest_counts[(result.distance, result.nearest_count)] += 1

    single_error_checks = 0
    double_error_checks = 0
    for codeword in CODEWORDS:
        for coordinate in range(9):
            result = decode(flip_bit(codeword, coordinate))
            assert result.status == "corrected" and result.codeword == codeword
            single_error_checks += 1
        for left, right in combinations(range(9), 2):
            corrupted = flip_bit(flip_bit(codeword, left), right)
            result = decode(corrupted)
            assert result.status == "uncorrectable"
            double_error_checks += 1

    affine_exact_checks = 0
    affine_single_error_checks = 0
    for anchor in integrity_states():
        for codeword in CODEWORDS:
            target = xor_bits(anchor, codeword)
            exact = decode_affine(target, anchor)
            assert exact.status == "exact" and exact.recovered_state == target
            affine_exact_checks += 1
            for coordinate in range(9):
                recovered = decode_affine(flip_bit(target, coordinate), anchor)
                assert recovered.status == "corrected" and recovered.recovered_state == target
                affine_single_error_checks += 1

    return {
        "full_state_status_counts": dict(sorted(status_counts.items())),
        "nearest_distance_and_tie_counts": {
            f"distance_{distance}_nearest_{count}": value
            for (distance, count), value in sorted(nearest_counts.items())
        },
        "single_error_checks": single_error_checks,
        "double_error_rejection_checks": double_error_checks,
        "affine_exact_checks": affine_exact_checks,
        "affine_single_error_checks": affine_single_error_checks,
        "silent_correction_beyond_radius_one": False,
    }


def _hypercube_certificate() -> dict[str, object]:
    full = states()
    valid = integrity_states()
    full_orbits = coset_partition()
    valid_orbits = coset_partition(integrity_only=True)
    adjacency_spectrum = hypercube_adjacency_spectrum()
    laplacian_spectrum = hypercube_laplacian_spectrum()
    pair_adjacency_spectrum = pair_flip_adjacency_spectrum()
    pair_laplacian_spectrum = pair_flip_laplacian_spectrum()
    return {
        "state_count": len(full),
        "integrity_state_count": len(valid),
        "each_state_neighbor_count": 9,
        "edge_count": hypercube_edge_count(),
        "distance_shell_counts": list(distance_shell_counts()),
        "plane_counts": list(theoretical_plane_counts()),
        "adjacency_spectrum": [
            {"eigenvalue": eigenvalue, "multiplicity": multiplicity}
            for eigenvalue, multiplicity in adjacency_spectrum
        ],
        "adjacency_trace": sum(
            eigenvalue * multiplicity for eigenvalue, multiplicity in adjacency_spectrum
        ),
        "adjacency_square_trace": sum(
            (eigenvalue**2) * multiplicity for eigenvalue, multiplicity in adjacency_spectrum
        ),
        "laplacian_spectrum": [
            {"eigenvalue": eigenvalue, "multiplicity": multiplicity}
            for eigenvalue, multiplicity in laplacian_spectrum
        ],
        "laplacian_spectral_gap": laplacian_spectrum[1][0],
        "even_parity_shell_counts": list(even_parity_shell_counts()),
        "pair_flip_graph_degree": pair_flip_graph_degree(),
        "pair_flip_graph_edge_count": pair_flip_graph_edge_count(),
        "pair_flip_adjacency_spectrum": [
            {"eigenvalue": eigenvalue, "multiplicity": multiplicity}
            for eigenvalue, multiplicity in pair_adjacency_spectrum
        ],
        "pair_flip_adjacency_trace": sum(
            eigenvalue * multiplicity for eigenvalue, multiplicity in pair_adjacency_spectrum
        ),
        "pair_flip_adjacency_square_trace": sum(
            (eigenvalue**2) * multiplicity for eigenvalue, multiplicity in pair_adjacency_spectrum
        ),
        "pair_flip_laplacian_spectrum": [
            {"eigenvalue": eigenvalue, "multiplicity": multiplicity}
            for eigenvalue, multiplicity in pair_laplacian_spectrum
        ],
        "pair_flip_laplacian_spectral_gap": pair_laplacian_spectrum[1][0],
        "full_orbit_count": len(full_orbits),
        "integrity_orbit_count": len(valid_orbits),
        "orbit_size": len(full_orbits[0]),
        "all_integrity_states_valid": all(is_integrity_valid(state) for state in valid),
        "reference_row_count": len(state_reference_rows()),
    }


def _markov_certificate() -> dict[str, object]:
    probability = 0.2
    kernel = noise_kernel(probability)
    uniform = np.full(512, 1.0 / 512.0)
    stationary_residual = uniform @ kernel - uniform
    return {
        "noise_probability_checked": probability,
        "row_sum_max_abs_error": _reported_residual(np.max(np.abs(kernel.sum(axis=1) - 1.0))),
        "column_sum_max_abs_error": _reported_residual(np.max(np.abs(kernel.sum(axis=0) - 1.0))),
        "uniform_stationary_max_abs_error": _reported_residual(np.max(np.abs(stationary_residual))),
        "minimum_self_loop_probability": _reported_residual(np.min(np.diag(kernel))),
        "positive_hypercube_edges": int(np.count_nonzero(kernel - np.diag(np.diag(kernel)))),
        "uniform_hamming_marginal": [float(value) for value in binomial_distribution()],
        "interpretation": "The binomial Hamming marginal follows from uniform occupancy; it is not ASH-specific evidence.",
    }


def _physics_certificate() -> dict[str, object]:
    probability = 0.35
    rate = 1.25
    states = physical_state_space()
    kernel = pair_flip_transition(probability)
    generator = pair_flip_generator(rate)
    background = weight_background_kernel(probability)
    background_distribution = uniform_background_distribution()
    moments = background_moments(background_distribution)
    initial_weight_distribution = np.zeros(len(weight_level_degeneracies()), dtype=float)
    initial_weight_distribution[0] = 1.0
    evolved_weight_distribution = evolve_weight_distribution(
        initial_weight_distribution,
        probability=probability,
        steps=3,
    )
    uniform = uniform_physical_distribution()
    observables = bridge_observables(uniform)
    mode_factors = [lazy_pair_flip_eigenvalue(weight, probability) for weight in range(10)]
    return {
        "state_count": len(states),
        "all_states_parity_valid": all(state[8] == (sum(state[:8]) & 1) for state in states),
        "pair_flip_probability_checked": probability,
        "pair_flip_rate_checked": rate,
        "kernel_row_sum_max_abs_error": _reported_residual(np.max(np.abs(kernel.sum(axis=1) - 1.0))),
        "kernel_symmetry_max_abs_error": _reported_residual(np.max(np.abs(kernel - kernel.T))),
        "uniform_stationary_max_abs_error": _reported_residual(np.max(np.abs(uniform @ kernel - uniform))),
        "generator_row_sum_max_abs_error": _reported_residual(np.max(np.abs(generator.sum(axis=1)))),
        "generator_symmetry_max_abs_error": _reported_residual(np.max(np.abs(generator - generator.T))),
        "background_row_sum_max_abs_error": _reported_residual(np.max(np.abs(background.sum(axis=1) - 1.0))),
        "weight_level_degeneracies": list(weight_level_degeneracies()),
        "uniform_background_distribution": [float(value) for value in background_distribution],
        "uniform_background_stationary_max_abs_error": _reported_residual(
            np.max(np.abs(background_distribution @ background - background_distribution))
        ),
        "uniform_background_mean_hamming_weight": moments.mean_hamming_weight,
        "uniform_background_variance_hamming_weight": moments.variance_hamming_weight,
        "uniform_background_order_parameter": moments.order_parameter,
        "evolved_weight_distribution_sum": float(np.sum(evolved_weight_distribution)),
        "evolved_weight_distribution_mean": background_moments(evolved_weight_distribution).mean_hamming_weight,
        "uniform_mean_hamming_weight": observables.mean_hamming_weight,
        "uniform_order_parameter": observables.order_parameter,
        "uniform_entropy_bits": observables.shannon_entropy_bits,
        "uniform_parity_valid_probability": observables.parity_valid_probability,
        "lazy_pair_flip_mode_factors": mode_factors,
        "mode_factors_bounded": all(-1.0 <= value <= 1.0 for value in mode_factors),
        "interpretation": "Finite-observer stochastic physics layer; not an observational cosmology claim.",
    }


def _empirical_bridge_certificate() -> dict[str, object]:
    observables = bridge_observables(uniform_physical_distribution())
    calibration = ObservableCalibration(
        source="mean_hamming_weight",
        target="example_length",
        scale=3.0,
        offset=1.0,
        unit="m",
    )
    calibrated = calibrate_observable(observables.mean_hamming_weight, calibration)
    observed = [1.0, 2.0]
    close = [1.0, 2.1]
    far = [2.0, 3.0]
    standard_deviation = [0.25, 0.25]
    comparison = compare_gaussian_models(
        observed=observed,
        standard_deviation=standard_deviation,
        predictions={"close": close, "far": far},
    )
    return {
        "calibration_source": calibrated.source,
        "calibration_target": calibrated.target,
        "calibrated_value": calibrated.value,
        "calibrated_unit": calibrated.unit,
        "example_chi_square": chi_square([1.0, 2.0], [0.5, 2.5], [0.5, 1.0]),
        "example_log_likelihood": diagonal_gaussian_log_likelihood([1.0, 2.0], [0.5, 2.5], [0.5, 1.0]),
        "best_likelihood_model": comparison[0].name,
        "comparison_count": len(comparison),
        "interpretation": "Calibration and likelihood contracts only; no external data fit is claimed.",
    }


def _prediction_ledger_certificate() -> dict[str, object]:
    entry = {
        "id": "PRED-EXAMPLE-001",
        "model_version": "ash-physics-v0.2",
        "commit": "0123456789abcdef",
        "frozen_utc": "2026-06-24T12:00:00Z",
        "observable": "example_length",
        "prediction": {"value": 14.5, "unit": "m"},
        "uncertainty": {"standard_deviation": 0.2, "unit": "m"},
        "data_product": "example-held-out-data-product",
        "statistic": "diagonal_gaussian_log_likelihood",
        "rejection_rule": "reject if chi_square exceeds preregistered threshold",
        "test_status": "frozen",
        "artifact_hashes": {
            "proofs/computational-certificate.json": "a" * 64,
        },
    }
    entry["entry_hash"] = canonical_prediction_hash(entry)
    ledger = {
        "schema_version": "1.0",
        "model_version": "ash-physics-v0.2",
        "status": "has_locked_predictions",
        "entries": [entry],
    }
    return {
        "empty_entry_status": ledger_lock_status([]),
        "locked_entry_status": ledger_lock_status(ledger["entries"]),
        "entry_hash_length": len(entry["entry_hash"]),
        "entry_hash_validates": not validate_prediction_ledger(ledger),
        "interpretation": "Prediction-lock mechanics are implemented; no repository prediction is locked by this example.",
    }


def _standard_baseline_certificate() -> dict[str, object]:
    standard = FlatLambdaCDMParameters(matter_density=0.3, dark_energy_density=0.7)
    shifted = FlatLambdaCDMParameters(matter_density=0.4, dark_energy_density=0.6)
    redshifts = [0.2, 0.5, 1.0]
    observed = flat_lcdm_distance_curve(redshifts, standard, steps=512)
    comparison = compare_distance_baselines(
        redshifts=redshifts,
        observed_distances=observed,
        standard_deviation=[0.01, 0.01, 0.01],
        baselines={"standard": standard, "shifted": shifted},
        steps=512,
    )
    distances = [
        normalized_comoving_distance(redshift, standard, steps=512)
        for redshift in (0.0, 0.5, 1.0)
    ]
    return {
        "matter_density": standard.matter_density,
        "dark_energy_density": standard.dark_energy_density,
        "total_density": standard.total_density,
        "hubble_at_zero": dimensionless_hubble_parameter(0.0, standard),
        "hubble_at_one": dimensionless_hubble_parameter(1.0, standard),
        "distance_curve": [float(value) for value in distances],
        "distance_curve_monotonic": distances[0] == 0.0 and distances[0] < distances[1] < distances[2],
        "best_baseline": comparison[0].name,
        "best_baseline_chi_square": comparison[0].chi_square,
        "interpretation": "Standard-baseline comparison mechanics only; not an ASH-derived cosmology limit.",
    }


def _observer_commitment_certificate() -> dict[str, object]:
    report = verify_r009(max_depth=4)
    summary = report["decoherence_summary"]
    return {
        "law_version": report["law_version"],
        "frontier_size": report["frontier_size"],
        "frontier_measure_total": report["frontier_measure_total"],
        "commitment_memory_classes": report["commitment_memory_classes"],
        "commitment_distribution_total": report["commitment_distribution_total"],
        "memory_prefix_embedding_passed": report["memory_prefix_embedding_passed"],
        "diagonal_trace": summary["diagonal_trace"],
        "passed_trace_invariant": summary["passed_trace_invariant"],
        "suppressed_pair_fraction": summary["suppressed_pair_fraction"],
        "passed": report["passed"],
        "boundary": report["boundary"],
    }


def _unit_bridge_certificate() -> dict[str, object]:
    data_root = REPO_ROOT / "data" / "ash-cosmology"
    frontier = read_csv_records(data_root / "observer-commitment" / "v0.1" / "r009_frontier.csv")
    decoherence = read_csv_records(
        data_root / "observer-commitment" / "v0.1" / "r009_decoherence_summary_by_depth.csv"
    )
    calibration = load_calibration(REPO_ROOT / "config" / "ash_r010_unit_bridge_calibration.json")
    features = finite_features_by_depth(frontier, decoherence)
    observables = physical_bridge(features, calibration)
    covariance = bootstrap_covariance(frontier, decoherence, calibration, samples=80, seed=10010)
    validation = validate_unit_bridge_artifacts(features, observables, calibration, covariance).as_dict()
    tests = validation["tests"]
    return {
        "bridge_version": validation["bridge_version"],
        "feature_depths": [row["depth"] for row in features],
        "unit_columns": [column for column in observables[0] if column.endswith(("_s", "_m", "_K", "_m3", "_m_inv2"))],
        "measure_normalization_by_depth": tests["measure_normalization_by_depth"],
        "unit_columns_present": tests["unit_columns_present"],
        "positive_declared_scales": tests["positive_declared_scales"],
        "finite_physical_values": tests["finite_physical_values"],
        "covariance_symmetric": tests["covariance_symmetric"],
        "covariance_psd_tolerance_1e_minus_12": tests["covariance_psd_tolerance_1e_minus_12"],
        "covariance_min_eigenvalue": (
            None
            if tests["covariance_min_eigenvalue"] is None
            else _reported_residual(tests["covariance_min_eigenvalue"])
        ),
        "boundary": validation["boundary"],
    }


def _finite_observer_limit_certificate() -> dict[str, object]:
    summary = finite_observer_validation_summary()
    n9_shell_counts = finite_observer_shell_counts(9)
    n9_cone_sizes = causal_cone_sizes(9)
    n9_spectrum = finite_observer_adjacency_spectrum(9)
    fiber_uniform = {}
    for source_n in ODD_LEVELS:
        for target_m in ODD_LEVELS:
            if source_n < target_m:
                continue
            values = set(fiber_sizes(source_n, target_m).values())
            fiber_uniform[f"{source_n}_to_{target_m}"] = values == {2 ** (source_n - target_m)}
    scale_rows = unit_scale_table(ell9_m=1.0, tau9_s=1.0)
    return {
        "scope": summary["r011_scope"],
        "levels": summary["levels"],
        "projective_consistency": validate_projective_consistency(),
        "projection_lipschitz_on_events": validate_lipschitz(),
        "n9_shell_counts": n9_shell_counts,
        "n9_cone_sizes": n9_cone_sizes,
        "n9_spectrum": n9_spectrum,
        "n9_laplacian_gap": finite_observer_laplacian_gap(9),
        "uniform_fiber_checks": fiber_uniform,
        "unit_scale_rows": [row.__dict__ for row in scale_rows],
        "sample_interval_nodes_n9_dt4_d2": causal_interval_size(9, delta_t=4, distance=2),
        "boundary": "Finite-observer limit closure only; no differentiable continuum, Lorentzian metric, physical light cone, or empirical cosmology is claimed.",
    }


def _locked_predictions_certificate() -> dict[str, object]:
    verification = verify_lock(REPO_ROOT)
    locked_files = verification["locked_files"]
    return {
        "schema": verification["schema"],
        "freeze_date": verification["freeze_date"],
        "prediction_ids": verification["prediction_ids"],
        "locked_prediction_count": verification["locked_prediction_count"],
        "ledger_hash_matches": verification["ledger_hash_matches"],
        "all_locked_files_match": verification["all_locked_files_match"],
        "locked_file_rows": {
            filename: metadata["rows"]
            for filename, metadata in sorted(locked_files.items())
        },
        "passed": verification["passed"],
        "boundary": verification["scientific_boundary"],
    }


def _branch_centered_closure_certificate() -> dict[str, object]:
    verification = verify_branch_centered_closure(REPO_ROOT)
    model_card = branch_centered_model_card(REPO_ROOT)
    return {
        "roadmap_id": verification["roadmap_id"],
        "component_count": verification["component_count"],
        "required_component_count": verification["required_component_count"],
        "missing_components": verification["missing_components"],
        "falsification_gate_count": verification["falsification_gate_count"],
        "missing_falsification_gates": verification["missing_falsification_gates"],
        "upstream_hashes_recorded": verification["upstream_hashes_recorded"],
        "missing_upstream_hashes": verification["missing_upstream_hashes"],
        "formal_model_tuple": verification["formal_model_tuple"],
        "closure_predicate": verification["closure_predicate"],
        "non_empirical_boundary": verification["non_empirical_boundary"],
        "external_empirical_status": verification["external_empirical_status"],
        "closed_formal_candidate": verification["closed_formal_candidate"],
        "scientific_status": verification["scientific_status"],
        "model_card_name": model_card["model_name"],
    }


def build_certificate() -> dict[str, object]:
    sections = {
        "code": code_certificate(),
        "decoder": _decoder_certificate(),
        "hypercube": _hypercube_certificate(),
        "projection": projection_certificate(),
        "adinkra": adinkra_certificate(),
        "branching": branch_certificate(4),
        "markov_chain": _markov_certificate(),
        "physics": _physics_certificate(),
        "empirical_bridge": _empirical_bridge_certificate(),
        "prediction_ledger": _prediction_ledger_certificate(),
        "standard_baseline": _standard_baseline_certificate(),
        "observer_commitment": _observer_commitment_certificate(),
        "unit_bridge": _unit_bridge_certificate(),
        "finite_observer_limit": _finite_observer_limit_certificate(),
        "locked_predictions": _locked_predictions_certificate(),
        "branch_centered_closure": _branch_centered_closure_certificate(),
    }
    checks = {
        "code_parameters": sections["code"]["rank"] == 4
        and sections["code"]["minimum_distance"] == 4
        and sections["code"]["doubly_even"],
        "nine_dimensional_code_not_self_dual": sections["code"]["self_dual_in_f2_9"] is False,
        "punctured_code_self_dual": sections["code"]["punctured_self_dual"] is True,
        "decoder_radius_one_exhaustive": sections["decoder"]["single_error_checks"] == 144,
        "double_errors_rejected": sections["decoder"]["double_error_rejection_checks"] == 576,
        "hypercube_edges_and_shells_exact": sections["hypercube"]["edge_count"] == 2304
        and sections["hypercube"]["distance_shell_counts"] == sections["hypercube"]["plane_counts"]
        and sum(sections["hypercube"]["even_parity_shell_counts"]) == 256,
        "hypercube_spectrum_exact": sections["hypercube"]["adjacency_trace"] == 0
        and sections["hypercube"]["adjacency_square_trace"] == 2 * sections["hypercube"]["edge_count"]
        and sections["hypercube"]["laplacian_spectral_gap"] == 2,
        "parity_pair_flip_spectrum_exact": sections["hypercube"]["pair_flip_graph_degree"] == 36
        and sections["hypercube"]["pair_flip_graph_edge_count"] == 4608
        and sections["hypercube"]["pair_flip_adjacency_trace"] == 0
        and sections["hypercube"]["pair_flip_adjacency_square_trace"]
        == 2 * sections["hypercube"]["pair_flip_graph_edge_count"]
        and sections["hypercube"]["pair_flip_laplacian_spectral_gap"] == 16,
        "projection_idempotent": sections["projection"]["idempotence_max_abs_error"] == 0.0,
        "garden_algebra_exact": sections["adinkra"]["maximum_integer_residual"] == 0,
        "quotient_isomorphism": sections["adinkra"]["valid"] is True,
        "branch_weights_normalized": abs(sections["branching"]["leaf_weight_sum"] - 1.0) < 1e-12,
        "markov_uniform_stationary": sections["markov_chain"]["uniform_stationary_max_abs_error"] < 1e-15,
        "physics_pair_flip_closed": sections["physics"]["state_count"] == 256
        and sections["physics"]["all_states_parity_valid"] is True,
        "physics_kernel_stochastic": sections["physics"]["kernel_row_sum_max_abs_error"] < 1e-15
        and sections["physics"]["kernel_symmetry_max_abs_error"] < 1e-15
        and sections["physics"]["uniform_stationary_max_abs_error"] < 1e-15,
        "physics_generator_valid": sections["physics"]["generator_row_sum_max_abs_error"] < 1e-15
        and sections["physics"]["generator_symmetry_max_abs_error"] < 1e-15,
        "physics_background_lumped": sections["physics"]["background_row_sum_max_abs_error"] < 1e-15,
        "physics_background_moments_exact": sections["physics"]["weight_level_degeneracies"]
        == [1, 36, 126, 84, 9]
        and sections["physics"]["uniform_background_stationary_max_abs_error"] < 1e-15
        and abs(sections["physics"]["uniform_background_mean_hamming_weight"] - 4.5) < 1e-15
        and abs(sections["physics"]["uniform_background_variance_hamming_weight"] - 2.25)
        < 1e-15
        and abs(sections["physics"]["uniform_background_order_parameter"]) < 1e-15
        and abs(sections["physics"]["evolved_weight_distribution_sum"] - 1.0) < 1e-15
        and sections["physics"]["evolved_weight_distribution_mean"] > 0.0,
        "physics_bridge_observables_normalized": abs(sections["physics"]["uniform_mean_hamming_weight"] - 4.5) < 1e-15
        and abs(sections["physics"]["uniform_order_parameter"]) < 1e-15
        and abs(sections["physics"]["uniform_entropy_bits"] - 8.0) < 1e-15
        and abs(sections["physics"]["uniform_parity_valid_probability"] - 1.0) < 1e-15,
        "physics_perturbation_modes_bounded": sections["physics"]["mode_factors_bounded"] is True,
        "empirical_calibration_contract": sections["empirical_bridge"]["calibration_source"] == "mean_hamming_weight"
        and sections["empirical_bridge"]["calibration_target"] == "example_length"
        and abs(sections["empirical_bridge"]["calibrated_value"] - 14.5) < 1e-15
        and sections["empirical_bridge"]["calibrated_unit"] == "m",
        "empirical_likelihood_contract": abs(sections["empirical_bridge"]["example_chi_square"] - 1.25) < 1e-15
        and sections["empirical_bridge"]["best_likelihood_model"] == "close"
        and sections["empirical_bridge"]["comparison_count"] == 2,
        "prediction_lock_contract": sections["prediction_ledger"]["empty_entry_status"] == "no_locked_predictions"
        and sections["prediction_ledger"]["locked_entry_status"] == "has_locked_predictions"
        and sections["prediction_ledger"]["entry_hash_length"] == 64
        and sections["prediction_ledger"]["entry_hash_validates"] is True,
        "standard_baseline_contract": abs(sections["standard_baseline"]["total_density"] - 1.0) < 1e-15
        and abs(sections["standard_baseline"]["hubble_at_zero"] - 1.0) < 1e-15
        and sections["standard_baseline"]["distance_curve_monotonic"] is True
        and sections["standard_baseline"]["best_baseline"] == "standard"
        and abs(sections["standard_baseline"]["best_baseline_chi_square"]) < 1e-15,
        "observer_commitment_verified": sections["observer_commitment"]["passed"] is True
        and abs(sections["observer_commitment"]["frontier_measure_total"] - 1.0) < 1e-12
        and abs(sections["observer_commitment"]["commitment_distribution_total"] - 1.0) < 1e-12
        and sections["observer_commitment"]["memory_prefix_embedding_passed"] is True
        and sections["observer_commitment"]["passed_trace_invariant"] is True,
        "unit_bridge_verified": sections["unit_bridge"]["measure_normalization_by_depth"] is True
        and sections["unit_bridge"]["unit_columns_present"] is True
        and sections["unit_bridge"]["positive_declared_scales"] is True
        and sections["unit_bridge"]["finite_physical_values"] is True
        and sections["unit_bridge"]["covariance_symmetric"] is True
        and sections["unit_bridge"]["covariance_psd_tolerance_1e_minus_12"] is True,
        "finite_observer_limit_verified": sections["finite_observer_limit"]["scope"]
        == "finite_observer_limit_closure_not_differentiable_continuum"
        and sections["finite_observer_limit"]["projective_consistency"] is True
        and sections["finite_observer_limit"]["projection_lipschitz_on_events"] is True
        and sections["finite_observer_limit"]["n9_shell_counts"] == {0: 1, 1: 36, 2: 126, 3: 84, 4: 9}
        and sections["finite_observer_limit"]["n9_spectrum"]
        == [(0, 36, 1), (1, 20, 9), (2, 8, 36), (3, 0, 84), (4, -4, 126)]
        and sections["finite_observer_limit"]["n9_laplacian_gap"] == 16
        and all(sections["finite_observer_limit"]["uniform_fiber_checks"].values())
        and sections["finite_observer_limit"]["unit_scale_rows"][-1]["ell_m"] == 1.0
        and sections["finite_observer_limit"]["unit_scale_rows"][-1]["tau_s"] == 1.0,
        "locked_predictions_verified": sections["locked_predictions"]["passed"] is True
        and sections["locked_predictions"]["prediction_ids"] == list(LOCKED_PREDICTION_IDS)
        and sections["locked_predictions"]["locked_prediction_count"] == 3
        and sections["locked_predictions"]["ledger_hash_matches"] is True
        and sections["locked_predictions"]["all_locked_files_match"] is True
        and sections["locked_predictions"]["locked_file_rows"]["r015_locked_expansion_prediction.csv"] >= 100
        and sections["locked_predictions"]["locked_file_rows"]["r015_locked_matter_template.csv"] >= 100
        and sections["locked_predictions"]["locked_file_rows"]["r015_locked_lowell_template.csv"] >= 30,
        "branch_centered_closure_verified": sections["branch_centered_closure"]["closed_formal_candidate"] is True
        and sections["branch_centered_closure"]["component_count"] == len(REQUIRED_COMPONENT_SYMBOLS)
        and sections["branch_centered_closure"]["missing_components"] == []
        and sections["branch_centered_closure"]["missing_falsification_gates"] == []
        and sections["branch_centered_closure"]["missing_upstream_hashes"] == []
        and sections["branch_centered_closure"]["non_empirical_boundary"] is True
        and sections["branch_centered_closure"]["external_empirical_status"] == "not empirically validated",
    }
    return {
        "certificate_schema": "1.0.0",
        "project_version": (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "arithmetic": "exact integer/GF(2) except explicitly reported floating residuals",
        "sections": sections,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "source_sha256": _source_manifest(),
    }


def _markdown(certificate: dict[str, object]) -> str:
    code = certificate["sections"]["code"]
    decoder = certificate["sections"]["decoder"]
    hypercube = certificate["sections"]["hypercube"]
    projection = certificate["sections"]["projection"]
    adinkra = certificate["sections"]["adinkra"]
    branching = certificate["sections"]["branching"]
    markov = certificate["sections"]["markov_chain"]
    physics = certificate["sections"]["physics"]
    empirical = certificate["sections"]["empirical_bridge"]
    prediction = certificate["sections"]["prediction_ledger"]
    standard = certificate["sections"]["standard_baseline"]
    observer_commitment = certificate["sections"]["observer_commitment"]
    unit_bridge = certificate["sections"]["unit_bridge"]
    finite_observer_limit = certificate["sections"]["finite_observer_limit"]
    locked_predictions = certificate["sections"]["locked_predictions"]
    branch_centered_closure = certificate["sections"]["branch_centered_closure"]
    lines = [
        "# ASH Computational Proof Certificate",
        "",
        "This certificate is written by `tools/run_proof_suite.py`. Finite code, decoder, hypercube, quotient, and Garden-algebra checks use exhaustive integer or GF(2) arithmetic. Floating-point values are reported only for the averaging and Markov-kernel residuals.",
        "",
        "## Result",
        "",
        f"**All checks pass:** `{str(certificate['all_checks_pass']).lower()}`",
        "",
        "## Canonical code",
        "",
        f"- Parameters: `[9, {code['rank']}, {code['minimum_distance']}]`",
        f"- Size: `{code['size']}`",
        f"- Weight distribution: `{code['weight_distribution']}`",
        f"- Doubly even: `{code['doubly_even']}`",
        f"- Self-dual in `F_2^9`: `{code['self_dual_in_f2_9']}`",
        f"- Punctured `[8,4,4]` code self-dual: `{code['punctured_self_dual']}`",
        f"- Coordinate 9 active parity: `{code['coordinate_9_active'] and code['coordinate_9_parity']}`",
        "",
        "## Exhaustive decoder",
        "",
        f"- Full-state status counts: `{decoder['full_state_status_counts']}`",
        f"- Single-bit corrections checked: `{decoder['single_error_checks']}`",
        f"- Two-bit corruptions rejected: `{decoder['double_error_rejection_checks']}`",
        f"- Affine one-bit recoveries checked: `{decoder['affine_single_error_checks']}`",
        "",
        "## Hypercube and projection",
        "",
        f"- Hypercube states: `{hypercube['state_count']}`",
        f"- Integrity-valid states: `{hypercube['integrity_state_count']}`",
        f"- Hypercube edge count: `{hypercube['edge_count']}`",
        f"- Distance-shell counts: `{hypercube['distance_shell_counts']}`",
        f"- Hypercube Laplacian spectral gap: `{hypercube['laplacian_spectral_gap']}`",
        f"- Parity pair-flip graph degree: `{hypercube['pair_flip_graph_degree']}`",
        f"- Parity pair-flip graph edge count: `{hypercube['pair_flip_graph_edge_count']}`",
        f"- Parity pair-flip Laplacian spectral gap: `{hypercube['pair_flip_laplacian_spectral_gap']}`",
        f"- Full/integrity orbit counts: `{hypercube['full_orbit_count']}` / `{hypercube['integrity_orbit_count']}`",
        f"- Projection idempotence residual: `{projection['idempotence_max_abs_error']}`",
        f"- Projection output code-invariant: `{projection['output_is_code_invariant']}`",
        "",
        "## Adinkra/Garden layer",
        "",
        f"- Garden integer residual: `{adinkra['maximum_integer_residual']}`",
        f"- Quotient vertices/edges: `{adinkra['quotient_vertex_count']}` / `{adinkra['quotient_edge_count']}`",
        f"- Quotient-to-matrix isomorphism: `{adinkra['valid']}`",
        "",
        "## Branching",
        "",
        f"- Depth/leaf count: `{branching['depth']}` / `{branching['leaf_count']}`",
        f"- Unique operator messages: `{branching['unique_messages']}`",
        f"- Leaf-weight sum: `{branching['leaf_weight_sum']}`",
        "",
        "## Markov control",
        "",
        f"- Uniform-stationary residual: `{markov['uniform_stationary_max_abs_error']}`",
        f"- Minimum self-loop probability: `{markov['minimum_self_loop_probability']}`",
        "- Conclusion: the binomial Hamming-weight envelope is the marginal of uniform occupancy and is not evidence unique to the ASH code transforms.",
        "",
        "## Finite-observer physics layer",
        "",
        f"- Admissible physical states: `{physics['state_count']}`",
        f"- Pair-flip kernel row residual: `{physics['kernel_row_sum_max_abs_error']}`",
        f"- Pair-flip kernel symmetry residual: `{physics['kernel_symmetry_max_abs_error']}`",
        f"- Uniform stationary residual: `{physics['uniform_stationary_max_abs_error']}`",
        f"- Generator row residual: `{physics['generator_row_sum_max_abs_error']}`",
        f"- Lumped background row residual: `{physics['background_row_sum_max_abs_error']}`",
        f"- Background shell degeneracies: `{physics['weight_level_degeneracies']}`",
        f"- Uniform background stationary residual: `{physics['uniform_background_stationary_max_abs_error']}`",
        f"- Uniform background variance: `{physics['uniform_background_variance_hamming_weight']}`",
        f"- Uniform mean Hamming weight: `{physics['uniform_mean_hamming_weight']}`",
        f"- Uniform order parameter: `{physics['uniform_order_parameter']}`",
        f"- Uniform entropy, bits: `{physics['uniform_entropy_bits']}`",
        f"- Mode factors bounded: `{physics['mode_factors_bounded']}`",
        "- Boundary: this is a finite-observer stochastic layer, not an observational cosmology result.",
        "",
        "## Empirical interface mechanics",
        "",
        f"- Example calibrated observable: `{empirical['calibration_target']}` = `{empirical['calibrated_value']}` `{empirical['calibrated_unit']}`",
        f"- Example chi-square: `{empirical['example_chi_square']}`",
        f"- Best example likelihood model: `{empirical['best_likelihood_model']}`",
        "- Boundary: these are bridge and likelihood contracts, not an external fit.",
        "",
        "## Prediction ledger mechanics",
        "",
        f"- Empty ledger status: `{prediction['empty_entry_status']}`",
        f"- Locked-entry status: `{prediction['locked_entry_status']}`",
        f"- Entry hash length: `{prediction['entry_hash_length']}`",
        f"- Locked-entry validation: `{prediction['entry_hash_validates']}`",
        "- Boundary: mechanics for future locked predictions are present; no repository prediction is locked here.",
        "",
        "## Standard baseline mechanics",
        "",
        f"- Flat density total: `{standard['total_density']}`",
        f"- `E(0)`: `{standard['hubble_at_zero']}`",
        f"- Distance curve monotonic: `{standard['distance_curve_monotonic']}`",
        f"- Best example baseline: `{standard['best_baseline']}`",
        "- Boundary: this is a reference-baseline comparator, not an ASH-derived standard-cosmology limit.",
        "",
        "## Observer commitment workbench",
        "",
        f"- R-009 law version: `{observer_commitment['law_version']}`",
        f"- Frontier size: `{observer_commitment['frontier_size']}`",
        f"- Frontier measure total: `{observer_commitment['frontier_measure_total']}`",
        f"- Commitment memory classes: `{observer_commitment['commitment_memory_classes']}`",
        f"- Commitment distribution total: `{observer_commitment['commitment_distribution_total']}`",
        f"- Memory prefix embedding: `{observer_commitment['memory_prefix_embedding_passed']}`",
        f"- Diagonal trace: `{observer_commitment['diagonal_trace']}`",
        f"- Diagonal trace invariant: `{observer_commitment['passed_trace_invariant']}`",
        f"- Suppressed pair fraction: `{observer_commitment['suppressed_pair_fraction']}`",
        "- Boundary: finite observer-relative commitment and branch-separation workbench only.",
        "",
        "## Unit-bearing bridge workbench",
        "",
        f"- R-010 bridge version: `{unit_bridge['bridge_version']}`",
        f"- Feature depths: `{unit_bridge['feature_depths']}`",
        f"- Unit columns checked: `{unit_bridge['unit_columns']}`",
        f"- Measure normalization by depth: `{unit_bridge['measure_normalization_by_depth']}`",
        f"- Unit columns present: `{unit_bridge['unit_columns_present']}`",
        f"- Positive declared scales: `{unit_bridge['positive_declared_scales']}`",
        f"- Finite physical-proxy values: `{unit_bridge['finite_physical_values']}`",
        f"- Covariance symmetric: `{unit_bridge['covariance_symmetric']}`",
        f"- Covariance PSD tolerance: `{unit_bridge['covariance_psd_tolerance_1e_minus_12']}`",
        f"- Covariance minimum eigenvalue: `{unit_bridge['covariance_min_eigenvalue']}`",
        "- Boundary: synthetic finite-observer unit-bearing bridge only.",
        "",
        "## Finite-observer limit workbench",
        "",
        f"- Scope: `{finite_observer_limit['scope']}`",
        f"- Levels checked: `{[row['n'] for row in finite_observer_limit['levels']]}`",
        f"- Projective consistency: `{finite_observer_limit['projective_consistency']}`",
        f"- Projection non-expansion: `{finite_observer_limit['projection_lipschitz_on_events']}`",
        f"- `n=9` shell counts: `{finite_observer_limit['n9_shell_counts']}`",
        f"- `n=9` cone sizes: `{finite_observer_limit['n9_cone_sizes']}`",
        f"- `n=9` spectrum: `{finite_observer_limit['n9_spectrum']}`",
        f"- `n=9` Laplacian gap: `{finite_observer_limit['n9_laplacian_gap']}`",
        f"- Uniform fiber checks: `{finite_observer_limit['uniform_fiber_checks']}`",
        f"- Unit scale rows: `{finite_observer_limit['unit_scale_rows']}`",
        f"- Sample interval nodes: `{finite_observer_limit['sample_interval_nodes_n9_dt4_d2']}`",
        "- Boundary: finite-observer limit closure only.",
        "",
        "## R-015 locked predictions",
        "",
        f"- Schema: `{locked_predictions['schema']}`",
        f"- Freeze date: `{locked_predictions['freeze_date']}`",
        f"- Prediction IDs: `{locked_predictions['prediction_ids']}`",
        f"- Locked prediction count: `{locked_predictions['locked_prediction_count']}`",
        f"- Ledger hash matches: `{locked_predictions['ledger_hash_matches']}`",
        f"- Locked CSV hashes match: `{locked_predictions['all_locked_files_match']}`",
        f"- Locked CSV rows: `{locked_predictions['locked_file_rows']}`",
        "- Boundary: immutable prospective synthetic templates and falsification metadata only.",
        "",
        "## R-016 branch-centered closure",
        "",
        f"- Roadmap ID: `{branch_centered_closure['roadmap_id']}`",
        f"- Component count: `{branch_centered_closure['component_count']}` / `{branch_centered_closure['required_component_count']}`",
        f"- Falsification gates: `{branch_centered_closure['falsification_gate_count']}`",
        f"- Upstream hashes recorded: `{branch_centered_closure['upstream_hashes_recorded']}`",
        f"- Formal candidate closed: `{branch_centered_closure['closed_formal_candidate']}`",
        f"- External empirical status: `{branch_centered_closure['external_empirical_status']}`",
        "- Boundary: formal repository-contract closure with synthetic/readiness validation only.",
        "",
        "## Check matrix",
        "",
    ]
    for name, passed in certificate["checks"].items():
        lines.append(f"- `{name}`: `{'PASS' if passed else 'FAIL'}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    certificate = build_certificate()
    output_directory = REPO_ROOT / "proofs"
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / "computational-certificate.json").write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_directory / "computational-certificate.md").write_text(
        _markdown(certificate),
        encoding="utf-8",
    )
    print(json.dumps({"all_checks_pass": certificate["all_checks_pass"], "checks": certificate["checks"]}, indent=2))
    return 0 if certificate["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
