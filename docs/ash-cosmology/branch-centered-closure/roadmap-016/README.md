# R-016 Branch-centered cosmology model closure

## Classification

- **Layer 1 — proved finite mathematics:** inherited finite ASH alphabet/admissibility/decoder structures from the verified local layer. This package does not add a new algebraic proof.
- **Layer 2 — deterministic computation:** repository-local closure verifier, model-card generator, component matrix, falsification-gate matrix, validation certificate, and tests.
- **Layer 3 — interpretive research:** branch-centered cosmology model as a closed formal candidate. This is a model/workbench closure, not an empirical physics claim.

## Formal model tuple

\[
\mathfrak A_{\mathrm{BC}} =
(\Omega,C,D,\Gamma,\mathcal T,\mu,\mathcal C,\mathcal M,\mathcal B_\ell,
E_{\mathrm{ASH}},\mathcal P_{\mathrm{ASH}},\mathcal L,\Pi).
\]

Here \(\Omega=\mathbb F_2^9\) is the local finite alphabet; \(C,D\) are the admissibility and decoder structures; \(\Gamma\) is the finite event graph; \(\mathcal T\) is the branch forest; \(\mu\) is the normalized branch measure; \(\mathcal C\) is observer commitment; \(\mathcal M\) is committed memory; \(\mathcal B_\ell\) is the unit-bearing bridge; \(E_{\mathrm{ASH}}\) is the background expansion map; \(\mathcal P_{\mathrm{ASH}}\) is the perturbation map; \(\mathcal L\) is the external-likelihood contract; and \(\Pi\) is the immutable prediction ledger.

## Closure predicate

\[
\mathrm{Closed}_{\mathrm{R016}}(\mathfrak A_{\mathrm{BC}})
\equiv
\bigwedge_{q\in Q_{\mathrm{roadmap}}}\mathrm{ContractPresent}(q)
\land
\mathrm{HashLocked}(\Pi)
\land
\mathrm{BoundaryDeclared}.
\]

The repository verifier operationalizes this as:

1. every required component appears in the component matrix;
2. every required falsification gate appears in the falsification matrix;
3. upstream R-009 through R-015 dependency hashes are recorded;
4. the closure certificate retains the phrase `not empirically validated`;
5. the formal expression file is present and parseable.

## Boundary

This package closes **R-016 formal branch-centered model closure** only. It does not prove a differentiable continuum metric, derive Einstein equations, prove a Born rule, replace a full Boltzmann hierarchy, analyze external data, validate empirical cosmology, or show preference over matched baselines.

## Verification

```bash
python -m compileall -q src tools
PYTHONPATH=src python tools/generate_branch_centered_closure.py --out-root . --require-pass
PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/test_branch_centered_closure.py
```

## Completion evidence

- `src/ash_model/branch_centered_closure.py`
- `tests/test_branch_centered_closure.py`
- `tools/generate_branch_centered_closure.py`
- `config/ash_r016_branch_centered_closure_contract.json`
- `data/ash-cosmology/branch-centered-closure/v0.1/`
- `validation/branch-centered-closure/roadmap-016/outputs/`
- `figures/ash-cosmology/branch-centered-closure/v0.1/`
