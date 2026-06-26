# Roadmap 007 Linear Perturbation Sector

Status: finite-observer perturbation refinement for ASH-Physics v0.2.

## Classification

| Component | Classification |
|---|---|
| Walsh-character quotient on the even-parity state space | Layer 1: proved finite mathematics |
| Shell counts and pair-flip eigenvalues | Layer 1: finite spectral theorem |
| Transfer functions, random power check, Green response | Layer 2: deterministic computation |
| Synthetic redshift-transfer table | Layer 3: synthetic phenomenology test object only |

## Summary

Roadmap 007 organizes finite ASH perturbations on the admissible 256-state layer
using restricted Walsh characters. On the even-parity hyperplane, labels
differing by the all-ones vector define the same character. This gives five
quotient shells:

\[
q([a])=\min(|a|,9-|a|)\in\{0,1,2,3,4\}.
\]

The shell multiplicities are:

```text
1, 9, 36, 84, 126
```

The non-lazy pair-flip eigenvalues are:

```text
1, 5/9, 2/9, 0, -1/9
```

and the lazy transfer factor is:

\[
\mu_q(p)=1-p+p\lambda_q.
\]

## What this adds

- A quotient-shell refinement of the existing finite perturbation mode basis.
- Exact shell-power transfer laws.
- A finite source/Green-function recurrence.
- Deterministic artifact generation for CSV/JSON/PNG outputs.
- Tests that exhaustively verify all 256 restricted characters over the finite state space.

## What this does not add

This pass does not add:

- a metric perturbation equation;
- gauge-fixed relativistic scalar/vector/tensor perturbations;
- a physical wavenumber map;
- a matter power spectrum;
- a CMB angular spectrum;
- observed redshift calibration;
- external empirical validation.

## Reproduction

From the repository root:

```bash
python -m pytest tests/test_linear_perturbations.py
python tools/generate_linear_perturbations.py --out-root . --refresh-figures
```

Generated outputs:

```text
data/ash-cosmology/linear-perturbations/v0.1/
figures/ash-cosmology/linear-perturbations/v0.1/
validation/linear-perturbations/roadmap-007/outputs/
```

## Next bridge

A future Roadmap 008-style bridge may attempt to map finite shell summaries

\[
(q,\mathcal P_q,T_q)
\]

to calibrated finite-observer observable statistics. Such a bridge must declare
units, covariance, external data provenance, matched baselines, and prediction
locking before any empirical claim is allowed.
