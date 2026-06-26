# R-010 Addendum — Unit-Bearing Branch-Ensemble Bridge

This addendum extends the existing finite-observer bridge-map documentation with a Roadmap R-010 unit-bearing synthetic bridge.

The previous bridge remains the dimensionless finite-observer map

```text
B: Delta(Omega) -> R^4
```

for internal state distributions. R-010 adds a separate branch-ensemble bridge over R-008/R-009 outputs:

```text
B_l : (Gamma, T, mu, M; Theta_l) -> Y_l
```

where `mu` is a normalized finite branch measure, `M` is the observer-memory summary, and `Theta_l` is a versioned calibration contract with explicit SI units.

This addendum does not replace the original finite-observer bridge and does not assert that the bridge is physically calibrated. It supplies a deterministic unit-bearing workbench for future validation programs.
