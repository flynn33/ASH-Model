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

All current observables are dimensionless.  No external unit conversion is
defined.

## Data products

No external data product is attached to this observable vector.  Future
empirical validation must define:

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

## Boundary

The observable vector is suitable for internal synthetic and numerical tests.
It is not yet a likelihood input for external physical data.
