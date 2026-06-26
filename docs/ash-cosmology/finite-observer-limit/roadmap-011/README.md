# R-011 Finite-Observer Limit Closure

Status: proposed repository integration for roadmap item **R-011 — Continuum, geometry, causal-structure, or finite-observer limit closure**.

## Classification

- **Layer 1 — proved finite mathematics:** nested even-parity state spaces, projective identities, uniform fibers, finite causal cones, halved-cube shell counts, adjacency spectrum, and spectral gap.
- **Layer 2 — deterministic computation:** executable module, tests, artifact generator, generated CSV/JSON/PNG artifacts, and reproducible verification commands.
- **Layer 3 — interpretive research:** the finite causal hierarchy may be used later as a branch-centered cosmology substrate, but this package does not assert a differentiable continuum, Lorentzian metric, Einstein equations, FRW dynamics, physical perturbation solver, or empirical cosmology.

## Closure choice

R-011 is explicitly closed through the **finite-observer limit** route, not through a continuum-limit proof.

For odd levels

\[
n\in\{1,3,5,7,9\},
\]

define

\[
\Omega_n=\{x\in\mathbb F_2^n:\sum_i x_i=0\pmod 2\}.
\]

The event relation is the pair-flip adjacency

\[
x\sim_n y \iff d_H(x,y)=2,
\]

with graph distance

\[
d_n(x,y)=\frac{1}{2}d_H(x,y).
\]

The finite causal relation on event nodes is

\[
(t,x)\preceq(s,y)\iff t\le s\;\mathrm{and}\; d_n(x,y)\le s-t.
\]

The projective observer map from level \(n\) to level \(m\le n\) is

\[
\pi_{m,n}(x_1,\ldots,x_n)
=
(x_1,\ldots,x_{m-1},\sum_{i=1}^{m-1}x_i \bmod 2).
\]

## Verified finite claims

The package verifies:

1. \(|\Omega_n|=2^{n-1}\).
2. finite shell counts

   \[
   |S_r^{(n)}|=\binom{n}{2r}.
   \]

3. closed cone counts

   \[
   |J^+_r(x)|=\sum_{q=0}^r \binom{n}{2q}.
   \]

4. projective consistency

   \[
   \pi_{\ell,m}\circ\pi_{m,n}=\pi_{\ell,n}.
   \]

5. uniform fibers

   \[
   |\pi_{m,n}^{-1}(y)|=2^{n-m}.
   \]

6. projection non-expansion for microscopic pair-flip events.
7. the \(n=9\) halved-cube spectrum

   \[
   36^1,\;20^9,\;8^{36},\;0^{84},\;(-4)^{126}
   \]

   and unnormalized Laplacian gap \(16\).

## Relationship to existing repository files

The current repository already states a finite-observer substitute rather than a continuum claim in `theory/continuum-limit.md`, gives the pair-flip graph as finite causal adjacency in `theory/causal-structure.md`, and lists remaining physical proof obligations in `proofs/physics-proof-obligations.md`. This R-011 integration turns those finite statements into an explicit nested observer hierarchy with executable tests and generated artifacts.

## Boundary statement

This package does **not** claim:

- a differentiable continuum;
- a Lorentzian metric;
- physical light cones;
- a physical speed of light;
- Einstein equations;
- FRW or \(\Lambda\)CDM background dynamics;
- physical perturbation equations;
- CMB or matter spectra;
- external likelihoods;
- empirical cosmology validation.

The phrase “causal” in this package means causal adjacency and reachability in the finite ASH pair-flip event graph only.

## Evidence paths

Recommended repository evidence after integration:

```text
src/ash_model/finite_observer_limit.py
tests/test_finite_observer_limit.py
tools/generate_finite_observer_limit.py
config/ash_r011_finite_observer_limit_contract.json
docs/ash-cosmology/finite-observer-limit/roadmap-011/README.md
data/ash-cosmology/finite-observer-limit/v0.1/
figures/ash-cosmology/finite-observer-limit/v0.1/
validation/finite-observer-limit/roadmap-011/outputs/verification.json
theory/continuum-limit_R011_addendum.md
theory/causal-structure_R011_addendum.md
proofs/physics-proof-obligations_R011_addendum.md
```

## Verification

```bash
python -m pytest tests/test_finite_observer_limit.py
python tools/generate_finite_observer_limit.py --out-root . --refresh-figures
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
python tools/final_repository_audit.py .
```

## Downstream gates left open

R-011 finite-observer closure does not close R-012, R-013, R-014, or R-015. Those still require ASH-derived background equations, physical perturbation equations/solver, external likelihoods and matched baselines, and locked prospective or held-out predictions.
