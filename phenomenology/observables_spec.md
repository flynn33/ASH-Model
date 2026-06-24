# Observable Map Specification

Status: finite-observer observables implemented

## Observable vector

The current observable vector is:

```text
mean_hamming_weight
order_parameter
shannon_entropy_bits
parity_valid_probability
```

## Implementation

`ash_model.physics.bridge_observables(distribution)` computes the observable
vector from a probability law over the admissible state space.

## Units

The native finite-observer observables remain dimensionless.
`ash_model.empirical.ObservableCalibration` defines an explicit affine contract
for mapping a dimensionless observable into a named unit-bearing value:

```text
unit_value = offset + scale * finite_observer_value
```

This repository implements the contract and tests finite inputs, units, and
deterministic output.  It does not provide reviewed physical calibration
constants.

## Data products

No external data product is attached to this observable vector.  The repository
now provides a diagonal Gaussian likelihood interface for future comparisons,
but empirical validation must still define:

- data release and access date;
- estimator;
- cuts;
- covariance model;
- nuisance parameters;
- matched baselines.

## Acceptance gates

- Probability law shape and normalization are validated.
- Uniform admissible law has entropy `8` bits.
- The observable vector is reproducible from tracked code.
- Calibration parameters must be finite and named.
- Likelihood comparisons must use finite vectors and positive standard
  deviations.

## Boundary

The observable vector is suitable for internal synthetic and numerical tests.
It can be passed through a declared calibration and likelihood contract, but it
is not an external physical-data result until a reviewed calibration, data
product, covariance source, and matched baseline are committed.
