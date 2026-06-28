# R-015 locked prospective / held-out scientific predictions

## Classification

- **Layer 1 — finite/auditable mathematics:** hash locking, immutable ledger semantics, and deterministic schema checks.
- **Layer 2 — deterministic computation:** repository-side verification of the locked ledger, CSV artifacts, lock certificate, and validation JSON.
- **Layer 3 — interpretive / empirical-facing research:** three prospective ASH cosmology templates are declared for future held-out comparison. These are not observations and not empirical validation.

## R-015 closure target

The live `ROADMAP.md` R-015 closure evidence is:

> Frozen prediction entries with hashes, falsification criteria, input freeze date, and repository validation.

This integration provides:

1. `predictions/locked/r015_prediction_ledger.locked.json`
2. `predictions/locked/r015_lock_certificate.json`
3. locked data vectors under `data/ash-cosmology/locked-predictions/v0.1/`
4. validation command and JSON output under `validation/locked-predictions/roadmap-015/`
5. targeted tests in `tests/test_locked_predictions.py`
6. explicit boundary and falsification documentation.

## Locked prediction entries

The ledger freezes three prediction IDs:

| ID | Topic | Locked posture |
|---|---|---|
| `ASH-R015-P001` | late-time branch-entropy expansion residual | nonnegative residual template over the declared redshift domain |
| `ASH-R015-P002` | finite-shell matter-spectrum residual | locked shell-template ratio over the declared \(k\)-domain |
| `ASH-R015-P003` | low-\(\ell\) finite-parity proxy sign | positive-sign compressed proxy statistic |

## Mutation policy

After the freeze date, numerical claims, domains, nuisance policies, and falsification rules **must not be edited in place**. Any revision must create a new prediction identifier and leave the original R-015 lock auditable.

## Boundary statement

R-015 closes the repository lock mechanics and prospective/held-out prediction-template gate only. It does **not** bundle external cosmological data, run Planck/BAO/SN/DESI/BOSS/Pantheon+ likelihoods, claim empirical preference for ASH, validate empirical cosmology, or prove that the locked signatures are present in nature.

## Verification

```bash
PYTHONPATH=src python tools/generate_locked_predictions.py --out-root . --require-pass
PYTHONPATH=src python -m pytest -q tests/test_locked_predictions.py
```

After repository integration, also run the repository-wide proof/data/audit commands described in the package-level `VERIFICATION_COMMANDS.md`.
