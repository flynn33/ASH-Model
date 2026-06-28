# R-014 External Likelihoods, Matched Baselines, and Reviewed Data Products

## Classification

- **Layer 1: finite/probabilistic mathematics.** The Gaussian likelihood is a finite vector calculation with an explicitly symmetric-positive-definite covariance requirement.
- **Layer 2: deterministic computation.** The repository overlay provides executable likelihood, covariance, matched-baseline, synthetic-recovery, hash-lock, and artifact-generation code.
- **Layer 3: interpretive/phenomenological bridge.** The probe labels and ASH-vs-baseline comparison semantics are a validation workbench only. They are not an empirical cosmology result.

## R-014 closure route

This closes the R-014 gate by adding:

1. metadata-only reviewed external data-product registry;
2. preregistered Gaussian likelihood contract;
3. covariance policy using Cholesky solves and SPD failure gates;
4. matched baseline definitions: `LCDM_nested_baseline`, `ASH_background_only`, `ASH_perturbation_only`, and `ASH_truth_family`;
5. deterministic synthetic fixtures covering SN, BAO, growth, and low-ell CMB proxy rows;
6. grid-recovery tests for the synthetic truth;
7. reproducible validation artifacts and data hashes.

## Boundary statement

This R-014 package supplies **external-likelihood readiness** and **synthetic validation**. It does not bundle third-party observational data, does not run Planck/Pantheon+/DESI/BOSS likelihoods, does not claim empirical preference for ASH, and does not close R-015 locked prospective predictions.

## Core likelihood

$$
\log \mathcal L(d\mid\theta)
= -\frac12\left[(d-m_\theta)^T C^{-1}(d-m_\theta)+\log |C|+n\log(2\pi)\right].
$$

A run is invalid if the covariance is not symmetric positive definite unless a separately declared regularization policy is added and hash-locked before unblinding.

## Verification

```bash
PYTHONPATH=src python -m pytest -q tests/test_external_likelihoods.py
PYTHONPATH=src python tools/generate_external_likelihoods.py --out-root .
python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
python tools/run_proof_suite.py
python tools/verify_repository.py
python tools/final_repository_audit.py .
```
