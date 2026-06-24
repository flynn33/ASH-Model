# Empirical Validation Program

## Principle

Empirical support requires predictions derived from a frozen ASH physical model and tested against data not used to construct the model.

## Stage 1: synthetic-universe validation

Before real data, generate synthetic observations from ASH and verify:

- parameter recovery;
- confidence or credible interval coverage;
- robustness to realistic noise;
- parameter degeneracy detection;
- distinguishability from baseline models;
- false-positive resistance when data are sampled from baseline models.

## Stage 2: matched ablations

Compare full ASH against controls that preserve most complexity while removing one ASH-specific component:

| Full component | Ablation |
|---|---|
| canonical code | matched random rank-distance code |
| Adinkra signs | unsigned or shuffled signs |
| branch weights | uniform or shuffled weights |
| integrity enforcement | no parity/integrity enforcement |
| ASH dynamics | matched generic cellular automaton |
| ASH physical equations | same-parameter phenomenological fit |

A result is ASH-specific only if matched controls do not reproduce it.

## Stage 3: prediction-code integration

Implement ASH observables in a cosmological prediction pipeline only after the equations are fixed.

Required acceptance tests:

- standard baseline limit matches the baseline solver within tolerance;
- ASH corrections are isolated and documented;
- numerical derivatives are stable;
- convergence holds under resolution changes;
- unit tests cover each observable component.

## Stage 4: observational probes

Use multiple independent probe classes:

- cosmic microwave background spectra and lensing;
- baryon acoustic oscillation distances;
- supernova luminosity distances;
- structure growth;
- weak lensing;
- big-bang nucleosynthesis;
- gravitational waves, if propagation is modified;
- local gravity tests, if gravity is modified.

## Stage 5: holdout and prospective tests

The strongest test is a frozen prediction made before the relevant data product is released.

Each prediction must record:

- model version;
- source hash;
- exact data product;
- observable;
- estimator;
- covariance treatment;
- scale and redshift cuts;
- nuisance parameters;
- prediction interval;
- rejection rule;
- publication or freeze date.

## Model comparison

Compare using more than fit quality:

- held-out predictive log likelihood;
- posterior predictive checks;
- Bayesian evidence or appropriate approximations;
- goodness of fit;
- parameter-count sensitivity;
- prior-volume sensitivity;
- residual structure;
- cross-probe consistency;
- robustness to nuisance/systematic choices.

A lower chi-square alone is not sufficient if ASH has more adjustable freedom.
