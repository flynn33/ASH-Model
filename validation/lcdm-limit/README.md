# Baseline Limit Validation

Status: standard baseline comparator implemented; ASH-derived limit not present

## Internal baseline

The finite-observer baseline is the uniform admissible state law.  It gives:

```text
mean_hamming_weight = 4.5
order_parameter = 0
entropy = 8 bits
```

## Standard-model comparison boundary

`ash_model.cosmology` implements a dimensionless flat standard-baseline
comparator:

```text
E(z) = sqrt(Omega_r (1 + z)^4 + Omega_m (1 + z)^3 + Omega_Lambda)
H0 D_C / c = integral_0^z dz' / E(z')
```

The comparator validates a flat non-negative density budget, computes
normalized comoving-distance curves, and ranks baseline curves with the
diagonal Gaussian likelihood contract.

No standard cosmological limit is derived from ASH.  This means the current
ASH finite-observer layer must be treated as a separate candidate mathematical
model rather than a deformation or limit of a standard cosmological model.

## Current blocker

External baseline comparison remains blocked until a reviewed physical
calibration, external data product, covariance source, and matched baseline
package are committed.
