# Empirical Validation Roadmap

Empirical work starts only after ASH defines a branch-centered dynamics and bridge map.

## Synthetic-first rule

Before using real cosmological data, ASH must generate synthetic branch universes and recover its own parameters.

Required tests:

1. generate synthetic ASH branch universes;
2. recover known branch/dynamics/bridge parameters;
3. add realistic noise and masking;
4. test confidence/credible interval coverage;
5. fit non-ASH controls to ASH-generated data;
6. fit ASH to non-ASH generated data;
7. verify ASH is distinguishable only when it should be.

## Matched controls

For every ASH claim, compare against a matched alternative:

| ASH element | Control |
|---|---|
| Enneahcube graph | matched 512-state graph |
| [9,4,4] code | random rank-4 code |
| doubly-even code | non-doubly-even matched code |
| parity coordinate | shuffled parity rule |
| branch grammar | random/generic branch process |
| branch measure | generic measure with same entropy |
| commitment rule | greedy/random/Bayesian baseline |
| branch decoherence | generic separation process |

## Real-data readiness

ASH should touch real cosmology only after it derives observables from fixed branch equations:

- \(H(z)\)
- \(D_L(z)\)
- \(D_M(z)\)
- \(P_\zeta(k)\)
- \(P_m(k,z)\)
- \(C_\ell\)
- non-Gaussianity shapes
- gravitational-wave propagation corrections

## Prospective prediction rule

A valid prediction must be frozen before the data are inspected. It must specify the observable, scale range, statistic, covariance, model parameters, prediction interval, and rejection rule.
