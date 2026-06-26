# Next Steps

## Pass 004 Candidates

1. Define branch tree states that emit the scalar used by the Pass 003 bridge.
2. Derive `gamma_branch` from branch expansion or decoherence parameters rather
   than fitting it as a free grid coordinate.
3. Define observer-relative commitment while preserving the branch ensemble.
4. Build a branch-to-background adapter that calls the Pass 003 observables.
5. Add coverage tests for synthetic recovery under wider noise and masking
   conditions.

## Later Work

- Add reviewed BAO and SNe likelihood adapters.
- Add perturbation-sector prototypes and matched controls.
- Replace the coarse grid posterior with a production inference path.
- Define and lock prospective prediction-ledger entries before any external
  data test.
- Attempt a continuum or geometry bridge only after the branch measure law and
  background adapter are stable.

## Boundary For Future Passes

Later work should not convert this synthetic recovery pass into an
external-data claim. Any such claim requires separate likelihoods, covariance
handling, preregistration, and locked predictions.
