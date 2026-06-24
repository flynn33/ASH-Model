# Observable Map Specification

Status: Draft

## Definitions

- Observable: a statistic or data product that can be computed from ASH model outputs and compared to an external dataset.
- Likelihood input: a frozen observable vector, covariance model, and nuisance-parameter treatment.

## Required specification

- Observable names, units, cuts, and estimator definitions.
- Data products and access rules.
- Covariance and systematic-error handling.
- Baseline models and parameter counts.

## Acceptance gates

- All observables link to a preregistration entry.
- The same cuts and estimator run for ASH and baselines.
- No post-test model changes occur under the same validation version.

## Current status

Blocked until the bridge map and phenomenology equations exist.
