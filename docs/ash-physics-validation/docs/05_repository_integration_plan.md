# Repository Integration Plan

## Add validation package

Place this package under:

```text
docs/ash-physics-validation/
```

## Add theory skeleton

Create:

```text
theory/physical-postulates.md
theory/microscopic-state-and-dynamics.md
theory/causal-structure.md
theory/coarse-graining-and-bridge-map.md
theory/continuum-limit.md
theory/cosmological-background.md
theory/linear-perturbations.md
```

Each file must include:

```text
Status
Definitions
Assumptions
Obligations
Known gaps
Verification status
```

## Add phenomenology skeleton

Create:

```text
phenomenology/README.md
phenomenology/ash_background_spec.md
phenomenology/ash_perturbations_spec.md
phenomenology/primordial_spectrum_spec.md
phenomenology/observables_spec.md
```

Do not implement observational fitting until the equations are written and reviewed.

## Add validation skeleton

Create:

```text
validation/synthetic-recovery/README.md
validation/matched-ablations/README.md
validation/numerical-convergence/README.md
validation/lcdm-limit/README.md
validation/preregistration.md
validation/status.json
```

## Add prediction ledger

Create:

```text
predictions/prediction-ledger.json
predictions/falsification-criteria.md
```

All future predictions must be frozen here before validation.

## Add proof catalog

Create:

```text
proofs/theorem-catalog.md
proofs/finite-algebra-status.md
proofs/physics-proof-obligations.md
```

## Add claim-language scan

Add the script:

```text
docs/ash-physics-validation/scripts/check_claim_language.py
```

Run it in CI if practical.

## Suggested commit sequence

```text
1. add validation package
2. add theory skeleton
3. add phenomenology skeleton
4. add validation and prediction ledgers
5. add claim-language scanner
6. wire scanner into CI
7. update README with proof-status boundary
8. run full verification
9. record validation/status.json
```
