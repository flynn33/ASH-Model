# Coarse-Graining and Bridge Map

Status: finite-observer bridge specified

## Domain and codomain

The bridge map takes a probability law `rho` over the admissible ASH state
space and returns dimensionless finite-observer observables.

```text
B: Delta(Omega) -> R^4
```

where `Delta(Omega)` is the probability simplex over the 256 admissible
states.

## Frozen observables

The current bridge map returns:

```text
mean_hamming_weight(rho)
order_parameter(rho) = 1 - 2 mean_hamming_weight(rho) / 9
shannon_entropy_bits(rho)
parity_valid_probability(rho)
```

These quantities are deterministic functions of `rho`.

## Invariance and uncertainty

The bridge is invariant under relabeling of states that preserves Hamming
weight for the background variables.  It does not assign SI units.  Uncertainty
propagates by applying the same deterministic bridge to sampled or estimated
state laws.

## Observable boundary

These observables are internal finite-observer quantities.  They are not yet
mapped to telescope data products, particle observables, gravitational
observables, or laboratory measurements.

## Evidence

- `ash_model.physics.bridge_observables`
- `tests/test_physics.py`
- `proofs/computational-certificate.json`

## Verification status

Implemented and computationally verified for the finite-observer bridge.
