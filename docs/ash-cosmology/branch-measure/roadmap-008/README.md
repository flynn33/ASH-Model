# Roadmap 008 - Finite Branch Measure Law

## Classification

- **Layer 1: proved finite mathematics.** The branch-measure law is a finite
  normalization theorem over non-empty sibling sets. For each parent branch
  `b`, local probabilities satisfy `sum_c pi(c | b) = 1`. Therefore child
  measures satisfy `sum_c mu(c) = mu(b)`.
- **Layer 2: deterministic computation.** `src/ash_model/branch_measure.py`
  implements the law and `tools/generate_branch_measure.py` emits
  deterministic CSV and JSON verification artifacts.
- **Layer 3: interpretive research boundary.** The law is a branch-cosmology
  workbench component. It is not empirical cosmology, not a Born-rule
  derivation, not physical amplitude dynamics, and not a decoherence or
  observer-commitment rule.

## Law

For finite child candidates `c in Ch(b)`, define the dimensionless effective
action

```text
A(c) = a_c
     + w_q q_c
     + w_d d_c
     + w_m r_c
     + w_h h_c
     + w_T[-log(max(|mu_q(p)|, epsilon))]
```

where `mu_q(p)` is the Roadmap 007 finite quotient-shell transfer factor.

The local branch probability is

```text
pi(c | b) = exp[-beta A(c)] / sum_u exp[-beta A(u)].
```

The child measure is

```text
mu(c) = mu(b) pi(c | b).
```

The optional complex number

```text
psi(c) = sqrt(mu(c)) exp(i lambda a_c)
```

is a norm-preserving phase decoration only. It is included so downstream work
can explicitly distinguish a classical measure from an amplitude-like
representation. It does not prove a Born rule and does not define quantum
dynamics.

## Closure of R-008

This pass closes R-008 only in the finite-observer sense:

1. The branch law is explicit.
2. The branch law is normalized over every finite sibling set.
3. The implementation rejects invalid shells, invalid probabilities, and
   missing child sets.
4. Deterministic artifacts record normalization, entropy, shell penalties, and
   example frontier rows.
5. Boundary language remains explicit.

## Non-closure

This pass does not close:

- R-009 commitment, observer memory, or decoherence;
- R-010 unit-bearing physical bridge;
- R-013 physical perturbation equations or CMB/matter solvers;
- R-014 external likelihoods or empirical baselines;
- R-015 locked predictions;
- the Born-rule or replacement-frequency problem for quantum/Everett claims.

## Evidence Paths

- `src/ash_model/branch_measure.py`
- `tests/test_branch_measure.py`
- `tools/generate_branch_measure.py`
- `data/ash-cosmology/branch-measure/v0.1/`
- `validation/branch-measure/roadmap-008/outputs/verification.json`
- `docs/ash-cosmology/branch-measure/roadmap-008/README.md`

## Verification

```bash
python tools/generate_branch_measure.py --out-root .
python tools/generate_artifacts.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
python docs/ash-physics-validation/scripts/run_repository_gate.py .
python tools/validate_json_assets.py .
python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
python tools/final_repository_audit.py .
```
