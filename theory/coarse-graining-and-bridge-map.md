# Coarse-Graining and Bridge Map

Status: Draft

## Definitions

- Coarse-graining: a map from microscopic ASH configurations to effective continuum or finite-observer variables.
- Bridge observable: a measurable quantity derived from a coarse-grained ASH state.
- Scale parameter: the resolution, block size, sampling rule, or observer limit used in the map.

## Assumptions

- The existing feature mapper is a deterministic reference design for image/video state mapping.
- A physical bridge map must be specified independently of visualization or reconstruction convenience.
- Observables must be defined before empirical data are used.

## Theorem or model obligations

- Define the map domain, codomain, parameters, and invariance properties.
- Prove that mapped quantities are well-defined under allowed state equivalences.
- State which physical units and observational coordinates are produced.
- Define error propagation from microscopic state uncertainty to observable uncertainty.

## Required tests

- Schema validation for bridge-map definitions.
- Numerical reproducibility tests for deterministic maps.
- Sensitivity tests for scale choices and admissible perturbations.

## Known gaps

- No physical bridge map is frozen.
- No observable units or likelihood inputs are defined.
- No coarse-graining limit is proven.

## Verification status

Blocked until physical postulates and dynamics identify the mapped state variables.
