# ASH Computational Proof Certificate

This certificate is written by `tools/run_proof_suite.py`. Finite code, decoder, hypercube, quotient, and Garden-algebra checks use exhaustive integer or GF(2) arithmetic. Floating-point values are reported only for the averaging and Markov-kernel residuals.

## Result

**All checks pass:** `true`

## Canonical code

- Parameters: `[9, 4, 4]`
- Size: `16`
- Weight distribution: `{0: 1, 4: 14, 8: 1}`
- Doubly even: `True`
- Self-dual in `F_2^9`: `False`
- Punctured `[8,4,4]` code self-dual: `True`
- Coordinate 9 active parity: `True`

## Exhaustive decoder

- Full-state status counts: `{'corrected': 144, 'exact': 16, 'uncorrectable': 352}`
- Single-bit corrections checked: `144`
- Two-bit corruptions rejected: `576`
- Affine one-bit recoveries checked: `36864`

## Hypercube and projection

- Hypercube states: `512`
- Integrity-valid states: `256`
- Hypercube edge count: `2304`
- Distance-shell counts: `[1, 9, 36, 84, 126, 126, 84, 36, 9, 1]`
- Hypercube Laplacian spectral gap: `2`
- Parity pair-flip graph degree: `36`
- Parity pair-flip graph edge count: `4608`
- Parity pair-flip Laplacian spectral gap: `16`
- Full/integrity orbit counts: `32` / `16`
- Projection idempotence residual: `0.0`
- Projection output code-invariant: `True`

## Adinkra/Garden layer

- Garden integer residual: `0`
- Quotient vertices/edges: `16` / `64`
- Quotient-to-matrix isomorphism: `True`

## Branching

- Depth/leaf count: `4` / `81`
- Unique operator messages: `16`
- Leaf-weight sum: `1.0`

## Markov control

- Uniform-stationary residual: `0.0`
- Minimum self-loop probability: `0.8`
- Conclusion: the binomial Hamming-weight envelope is the marginal of uniform occupancy and is not evidence unique to the ASH code transforms.

## Finite-observer physics layer

- Admissible physical states: `256`
- Pair-flip kernel row residual: `0.0`
- Pair-flip kernel symmetry residual: `0.0`
- Uniform stationary residual: `0.0`
- Generator row residual: `0.0`
- Lumped background row residual: `0.0`
- Background shell degeneracies: `[1, 36, 126, 84, 9]`
- Uniform background stationary residual: `0.0`
- Uniform background variance: `2.25`
- Uniform mean Hamming weight: `4.5`
- Uniform order parameter: `0.0`
- Uniform entropy, bits: `8.0`
- Mode factors bounded: `True`
- Boundary: this is a finite-observer stochastic layer, not an observational cosmology result.

## Empirical interface mechanics

- Example calibrated observable: `example_length` = `14.5` `m`
- Example chi-square: `1.25`
- Best example likelihood model: `close`
- Boundary: these are bridge and likelihood contracts, not an external fit.

## Prediction ledger mechanics

- Empty ledger status: `no_locked_predictions`
- Locked-entry status: `has_locked_predictions`
- Entry hash length: `64`
- Locked-entry validation: `True`
- Boundary: mechanics for future locked predictions are present; no repository prediction is locked here.

## Standard baseline mechanics

- Flat density total: `1.0`
- `E(0)`: `1.0`
- Distance curve monotonic: `True`
- Best example baseline: `standard`
- Boundary: this is a reference-baseline comparator, not an ASH-derived standard-cosmology limit.

## Observer commitment workbench

- R-009 law version: `ash-r009-commitment-memory-decoherence-v0.1`
- Frontier size: `625`
- Frontier measure total: `0.9999999999999999`
- Commitment memory classes: `144`
- Commitment distribution total: `0.9999999999999999`
- Memory prefix embedding: `True`
- Diagonal trace: `0.9999999999999999`
- Diagonal trace invariant: `True`
- Suppressed pair fraction: `0.9999589743589744`
- Boundary: finite observer-relative commitment and branch-separation workbench only.

## Unit-bearing bridge workbench

- R-010 bridge version: `ash-r010-unit-bridge-v0.1`
- Feature depths: `[4]`
- Unit columns checked: `['time_s', 'coarse_length_m', 'energy_density_J_m3', 'mass_density_kg_m3', 'einstein_curvature_proxy_m_inv2', 'memory_length_m', 'temperature_proxy_K']`
- Measure normalization by depth: `True`
- Unit columns present: `True`
- Positive declared scales: `True`
- Finite physical-proxy values: `True`
- Covariance symmetric: `True`
- Covariance PSD tolerance: `True`
- Covariance minimum eigenvalue: `0.0`
- Boundary: synthetic finite-observer unit-bearing bridge only.

## Finite-observer limit workbench

- Scope: `finite_observer_limit_closure_not_differentiable_continuum`
- Levels checked: `[1, 3, 5, 7, 9]`
- Projective consistency: `True`
- Projection non-expansion: `True`
- `n=9` shell counts: `{0: 1, 1: 36, 2: 126, 3: 84, 4: 9}`
- `n=9` cone sizes: `{0: 1, 1: 37, 2: 163, 3: 247, 4: 256}`
- `n=9` spectrum: `[(0, 36, 1), (1, 20, 9), (2, 8, 36), (3, 0, 84), (4, -4, 126)]`
- `n=9` Laplacian gap: `16`
- Uniform fiber checks: `{'1_to_1': True, '3_to_1': True, '3_to_3': True, '5_to_1': True, '5_to_3': True, '5_to_5': True, '7_to_1': True, '7_to_3': True, '7_to_5': True, '7_to_7': True, '9_to_1': True, '9_to_3': True, '9_to_5': True, '9_to_7': True, '9_to_9': True}`
- Unit scale rows: `[{'n': 1, 'states': 1, 'ell_m': 16.0, 'tau_s': 16.0, 'max_pair_diameter': 0, 'max_signal_radius_m': 0.0}, {'n': 3, 'states': 4, 'ell_m': 8.0, 'tau_s': 8.0, 'max_pair_diameter': 1, 'max_signal_radius_m': 8.0}, {'n': 5, 'states': 16, 'ell_m': 4.0, 'tau_s': 4.0, 'max_pair_diameter': 2, 'max_signal_radius_m': 8.0}, {'n': 7, 'states': 64, 'ell_m': 2.0, 'tau_s': 2.0, 'max_pair_diameter': 3, 'max_signal_radius_m': 6.0}, {'n': 9, 'states': 256, 'ell_m': 1.0, 'tau_s': 1.0, 'max_pair_diameter': 4, 'max_signal_radius_m': 4.0}]`
- Sample interval nodes: `184`
- Boundary: finite-observer limit closure only.

## R-015 locked predictions

- Schema: `ash.r015.locked_prediction_ledger.v1`
- Freeze date: `2026-06-26`
- Prediction IDs: `['ASH-R015-P001', 'ASH-R015-P002', 'ASH-R015-P003']`
- Locked prediction count: `3`
- Ledger hash matches: `True`
- Locked CSV hashes match: `True`
- Locked CSV rows: `{'r015_locked_expansion_prediction.csv': 126, 'r015_locked_lowell_template.csv': 59, 'r015_locked_matter_template.csv': 160}`
- Boundary: immutable prospective synthetic templates and falsification metadata only.

## R-016 branch-centered closure

- Roadmap ID: `R-016`
- Component count: `13` / `13`
- Falsification gates: `5`
- Upstream hashes recorded: `['R009', 'R010', 'R011', 'R012', 'R013', 'R014', 'R015']`
- Formal candidate closed: `True`
- External empirical status: `not empirically validated`
- Boundary: formal repository-contract closure with synthetic/readiness validation only.

## Check matrix

- `code_parameters`: `PASS`
- `nine_dimensional_code_not_self_dual`: `PASS`
- `punctured_code_self_dual`: `PASS`
- `decoder_radius_one_exhaustive`: `PASS`
- `double_errors_rejected`: `PASS`
- `hypercube_edges_and_shells_exact`: `PASS`
- `hypercube_spectrum_exact`: `PASS`
- `parity_pair_flip_spectrum_exact`: `PASS`
- `projection_idempotent`: `PASS`
- `garden_algebra_exact`: `PASS`
- `quotient_isomorphism`: `PASS`
- `branch_weights_normalized`: `PASS`
- `markov_uniform_stationary`: `PASS`
- `physics_pair_flip_closed`: `PASS`
- `physics_kernel_stochastic`: `PASS`
- `physics_generator_valid`: `PASS`
- `physics_background_lumped`: `PASS`
- `physics_background_moments_exact`: `PASS`
- `physics_bridge_observables_normalized`: `PASS`
- `physics_perturbation_modes_bounded`: `PASS`
- `empirical_calibration_contract`: `PASS`
- `empirical_likelihood_contract`: `PASS`
- `prediction_lock_contract`: `PASS`
- `standard_baseline_contract`: `PASS`
- `observer_commitment_verified`: `PASS`
- `unit_bridge_verified`: `PASS`
- `finite_observer_limit_verified`: `PASS`
- `locked_predictions_verified`: `PASS`
- `branch_centered_closure_verified`: `PASS`
