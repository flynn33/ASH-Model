# Roadmap R-009 — Finite Observer Commitment, Memory, and Decoherence Rule

## Scope

This directory documents the finite R-009 closure added by `src/ash_model/observer_commitment.py`.

R-009 assumes R-008 supplies a normalized finite branch measure or amplitude-derived probability over a branch frontier. R-009 then defines how observer-relative commitment records are embedded in branch histories and how finite branch separation is scored.

## Commitment rule

For a parent branch \(b\), child branch \(c\), and observer-relative token \(o(c;b)\), memory updates by

\[
M(c)=
\begin{cases}
M(b)\Vert o(c;b), & o(c;b)\neq\varnothing,\\
M(b), & o(c;b)=\varnothing.
\end{cases}
\]

Commitment means a finite observer-relative memory record along a branch. It does not prune the branch tree.

## Memory embedding invariant

For every edge \(b\to c\), \(M(b)\) is a prefix of \(M(c)\). Therefore observer memory is embedded monotonically in branch histories.

## Commitment distribution

For frontier leaves \(L_t\) with normalized weights \(\mu(\ell)\), the observer-location distribution over memory classes is

\[
P_t(m)=\sum_{\ell\in L_t:\,M(\ell)=m}\mu(\ell).
\]

Because memory classes partition the finite frontier,

\[
\sum_m P_t(m)=\sum_{\ell\in L_t}\mu(\ell)=1.
\]

## Branch-separation/decoherence score

For leaves \(i,j\), define

\[
D_{ij}=
\sqrt{\mu_i\mu_j}
\exp[-\gamma_B d_T(i,j)-\gamma_M d_M(i,j)-\gamma_O d_O(i,j)]
\exp[i\theta_{ij}].
\]

The diagonal is \(D_{ii}=\mu_i\), so

\[
\sum_iD_{ii}=1.
\]

This is a finite branch-separation/decoherence score, not a claim of a complete physical decoherence functional.

## Generated artifacts

Run:

```bash
python tools/generate_observer_commitment.py --out-root . --depth 4 --pair-sample-limit 5000
```

Generated files:

```text
data/ash-cosmology/observer-commitment/v0.1/r009_frontier.csv
data/ash-cosmology/observer-commitment/v0.1/r009_commitment_distribution.csv
data/ash-cosmology/observer-commitment/v0.1/r009_decoherence_pair_sample.csv
data/ash-cosmology/observer-commitment/v0.1/r009_decoherence_summary_by_depth.csv
validation/observer-commitment/roadmap-009/outputs/verification.json
```

## Boundary

Finite observer-relative commitment and branch-separation workbench only; no collapse claim, no Born-rule proof, no unitary Hilbert-space dynamics, no unit-bearing spacetime bridge, no CMB/matter-spectrum solver, and no empirical cosmology validation.
