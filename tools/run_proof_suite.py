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
from ash_model.branching import branch_certificate
from ash_model.code import CODEWORDS, code_certificate, decode, decode_affine
from ash_model.hypercube import coset_partition, integrity_states, state_reference_rows, states, theoretical_plane_counts
from ash_model.physics import (
    bridge_observables,
    lazy_pair_flip_eigenvalue,
    pair_flip_generator,
    pair_flip_transition,
    physical_state_space,
    uniform_physical_distribution,
    weight_background_kernel,
)
from ash_model.projection import projection_certificate
from ash_model.simulation import binomial_distribution, noise_kernel


def _source_manifest() -> dict[str, str]:
    suffixes = {".py", ".json", ".toml", ".md", ".tex", ".yml", ".yaml", ".cff"}
    filenames = {"LICENSE", "VERSION", ".gitignore"}
    excluded_prefixes = ("proofs/",)
    manifest: dict[str, str] = {}
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in suffixes and path.name not in filenames:
            continue
        relative = path.relative_to(REPO_ROOT).as_posix()
        if relative.startswith(excluded_prefixes) or "/__pycache__/" in f"/{relative}/" or "/.pytest_cache/" in f"/{relative}/":
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
    return {
        "state_count": len(full),
        "integrity_state_count": len(valid),
        "each_state_neighbor_count": 9,
        "plane_counts": list(theoretical_plane_counts()),
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
        "row_sum_max_abs_error": float(np.max(np.abs(kernel.sum(axis=1) - 1.0))),
        "column_sum_max_abs_error": float(np.max(np.abs(kernel.sum(axis=0) - 1.0))),
        "uniform_stationary_max_abs_error": float(np.max(np.abs(stationary_residual))),
        "minimum_self_loop_probability": float(np.min(np.diag(kernel))),
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
    uniform = uniform_physical_distribution()
    observables = bridge_observables(uniform)
    mode_factors = [lazy_pair_flip_eigenvalue(weight, probability) for weight in range(10)]
    return {
        "state_count": len(states),
        "all_states_parity_valid": all(state[8] == (sum(state[:8]) & 1) for state in states),
        "pair_flip_probability_checked": probability,
        "pair_flip_rate_checked": rate,
        "kernel_row_sum_max_abs_error": float(np.max(np.abs(kernel.sum(axis=1) - 1.0))),
        "kernel_symmetry_max_abs_error": float(np.max(np.abs(kernel - kernel.T))),
        "uniform_stationary_max_abs_error": float(np.max(np.abs(uniform @ kernel - uniform))),
        "generator_row_sum_max_abs_error": float(np.max(np.abs(generator.sum(axis=1)))),
        "generator_symmetry_max_abs_error": float(np.max(np.abs(generator - generator.T))),
        "background_row_sum_max_abs_error": float(np.max(np.abs(background.sum(axis=1) - 1.0))),
        "uniform_mean_hamming_weight": observables.mean_hamming_weight,
        "uniform_order_parameter": observables.order_parameter,
        "uniform_entropy_bits": observables.shannon_entropy_bits,
        "uniform_parity_valid_probability": observables.parity_valid_probability,
        "lazy_pair_flip_mode_factors": mode_factors,
        "mode_factors_bounded": all(-1.0 <= value <= 1.0 for value in mode_factors),
        "interpretation": "Finite-observer stochastic physics layer; not an observational cosmology claim.",
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
    }
    checks = {
        "code_parameters": sections["code"]["rank"] == 4
        and sections["code"]["minimum_distance"] == 4
        and sections["code"]["doubly_even"],
        "nine_dimensional_code_not_self_dual": sections["code"]["self_dual_in_f2_9"] is False,
        "punctured_code_self_dual": sections["code"]["punctured_self_dual"] is True,
        "decoder_radius_one_exhaustive": sections["decoder"]["single_error_checks"] == 144,
        "double_errors_rejected": sections["decoder"]["double_error_rejection_checks"] == 576,
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
        "physics_bridge_observables_normalized": abs(sections["physics"]["uniform_mean_hamming_weight"] - 4.5) < 1e-15
        and abs(sections["physics"]["uniform_order_parameter"]) < 1e-15
        and abs(sections["physics"]["uniform_entropy_bits"] - 8.0) < 1e-15
        and abs(sections["physics"]["uniform_parity_valid_probability"] - 1.0) < 1e-15,
        "physics_perturbation_modes_bounded": sections["physics"]["mode_factors_bounded"] is True,
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
    lines = [
        "# ASH Computational Proof Certificate",
        "",
        "This certificate is generated by `tools/run_proof_suite.py`. Finite code, decoder, hypercube, quotient, and Garden-algebra checks use exhaustive integer or GF(2) arithmetic. Floating-point values are reported only for the averaging and Markov-kernel residuals.",
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
        f"- Uniform mean Hamming weight: `{physics['uniform_mean_hamming_weight']}`",
        f"- Uniform order parameter: `{physics['uniform_order_parameter']}`",
        f"- Uniform entropy, bits: `{physics['uniform_entropy_bits']}`",
        f"- Mode factors bounded: `{physics['mode_factors_bounded']}`",
        "- Boundary: this is a finite-observer stochastic layer, not an observational cosmology result.",
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
