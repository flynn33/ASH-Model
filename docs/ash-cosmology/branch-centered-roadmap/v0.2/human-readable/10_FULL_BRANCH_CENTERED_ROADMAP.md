# ASH Cosmology Branch-Centered Roadmap — Full Research Specification

## Purpose

This document locks the corrected ASH Cosmology research direction. It is intentionally about science, mathematics, evidence, testing, and falsification. It does not advise on storage, implementation workflow, or project-file organization.

## Central correction

Previous material over-weighted the finite Enneahcube layer. That is incomplete. In ASH Cosmology, the finite layer is the local integrity alphabet, while the leaf-branch field is the cosmological possibility structure.

The corrected model is:

```text
ASH Cosmology = finite local Enneahcube state kernel
              + recursive leaf-branch universe
              + branch measure / amplitude / score law
              + commitment / observation rule
              + physical bridge to spacetime and observables
```

The finite layer tells us what a local admissible state is. The branch layer tells us what a cosmos of possible histories is. The commitment layer tells us how an observer experiences a realized history. The bridge layer tells us whether ASH can become a physical cosmology.

## 1. Primary research object

Define ASH Cosmology as:

\[
\mathfrak A = (\Omega,C,D,\Gamma,\mathcal T,\mu/\psi,\mathcal C,\mathcal M,\mathcal B_\ell).
\]

| Symbol | Meaning | Status |
|---|---|---|
| \(\Omega\) | finite local Enneahcube alphabet \(\mathbb F_2^9\) | finite/local |
| \(C\) | rank-4 doubly-even \([9,4,4]\) code/admissibility structure | finite/local |
| \(D\) | decoder and defect policy | finite/local |
| \(\Gamma\) | causal/event graph or emergent adjacency | physical substrate candidate |
| \(\mathcal T\) | unbounded branch tree or branch forest | cosmologically primary |
| \(\mu/\psi\) | branch measure or complex amplitude law | probability/quantum bridge |
| \(\mathcal C\) | commitment/observation/decoherence rule | observer relation |
| \(\mathcal M\) | committed memory/history graph | experienced history |
| \(\mathcal B_\ell\) | branch-to-physical bridge at scale \(\ell\) | cosmology bridge |

The full universe state is not merely \(X_t=\{x_v(t)\}\). A branch-centered ASH universe should be modeled as:

\[
\mathcal U_t=(\Gamma_t,\mathcal B_t,\mathcal M_t,\mathcal O_t),
\]

where \(\mathcal B_t\) is the branch forest of possible histories, \(\mathcal M_t\) is committed memory/realized observer history, and \(\mathcal O_t\) is the set of observation or commitment events.

## 2. Local finite layer

The local layer is:

\[
\Omega=\mathbb F_2^9.
\]

Each event/site carries:

\[
x_v\in \Omega.
\]

The Enneahcube graph connects states by Hamming distance one:

\[
x\sim y\iff d_H(x,y)=1.
\]

The code layer is:

\[
C\subset\mathbb F_2^9,\qquad [n,k,d]=[9,4,4].
\]

### Local theorem targets

1. \(|\Omega|=512\).
2. Every Enneahcube vertex has degree 9.
3. Hamming plane count is \(|P_k|=\binom{9}{k}\).
4. \(C\) is linear.
5. \(\dim C=4\).
6. \(|C|=16\).
7. Every codeword has weight divisible by 4.
8. \(d_{min}=4\).
9. Single-bit codeword errors are uniquely correctable by an explicit decoder.
10. Two-bit errors are detected/rejected under strict policy.
11. Length-nine self-duality is not claimed.

### Scientific boundary

These facts prove a local symbolic/integrity layer. They do not prove spacetime, many-worlds, quantum mechanics, gravity, dark energy, or empirical cosmology.

## 3. Branch history layer

A branch is a finite history path:

\[
b=(\mathcal U_0,\mathcal U_1,\ldots,\mathcal U_n).
\]

The branch tree rooted at \(\mathcal U_0\) is:

\[
\mathcal T_{\mathcal U_0}=\{b:b\text{ is an admissible ASH history branch}\}.
\]

A leaf is a frontier history:

\[
\ell\in L_n(\mathcal T).
\]

Each leaf should carry:

\[
\ell=(\mathrm{history},\mathrm{state},w_\ell,\psi_\ell,S_\ell,M_\ell).
\]

where \(w_\ell\) is a real weight when using a classical measure, \(\psi_\ell\) is a complex amplitude when using a quantum/Everett structure, \(S_\ell\) is an action/cost/coherence score, and \(M_\ell\) is the observer record along that leaf.

## 4. Branch ontology choices

ASH must choose a branch interpretation before making cosmological claims.

### 4.1 Epistemic branches

Branches are possible reconstructions, hypotheses, or computational candidates. This is useful for inference and applications, but weak as cosmology.

Required math: scoring, pruning, calibration, and error analysis.

### 4.2 Ontic non-quantum branches

Branches are physically real histories with a non-quantum branch measure \(\mu\).

Required math: ontology, conservation, normalized measure, observer-location rule, and empirical signatures.

### 4.3 Quantum/Everett branches

Branches are decohered components of a universal state:

\[
\Psi_t=\sum_{\ell\in L_t}\psi_\ell|\ell\rangle.
\]

Required math: Hilbert space, inner product, norm-preserving evolution, decoherence or orthogonality, and Born rule or replacement frequency theorem.

## 5. Branch expansion laws

### Deterministic branch expansion

\[
\mathcal F_{t+1}=\operatorname{expand}(\mathcal F_t).
\]

All admissible children exist.

### Weighted branch expansion

\[
w(b')\ge0,\qquad\sum_{b'\in children(b)}w(b')=w(b).
\]

### Quantum-like branch expansion

\[
\psi(b')\in\mathbb C,\qquad\sum_{b'}|\psi(b')|^2=|\psi(b)|^2.
\]

The branch law must specify whether expansion is local, stochastic, deterministic, action-weighted, amplitude-preserving, or observer-relative.

## 6. Branch measure or amplitude law

ASH must define one of the following.

### Classical measure

\[
\mu(\ell)\ge0,\qquad\sum_{\ell\in L_n}\mu(\ell)=1.
\]

### Action-weighted measure

\[
\mu(\ell)=\frac{e^{-S(\ell)}}{Z}.
\]

### Complex amplitude

\[
\psi(\ell)=A(\ell)e^{iS(\ell)/\hbar},\qquad P(\ell)=|\psi(\ell)|^2.
\]

If ASH targets many-worlds quantum cosmology, the Born-rule problem is central:

\[
P(\ell)=|\psi_\ell|^2.
\]

ASH may propose an alternative, but the alternative must be explicit, normalized, empirically testable, and not post-hoc.

## 7. Commitment and observer memory

Commitment should mean observer-relative realized memory, not automatic collapse.

Define:

\[
\mathcal C:(\mathcal T,\mu/\psi,\mathcal O)\to\mathcal M.
\]

Observer memory satisfies:

\[
M_O(t)\subset b.
\]

Under many-worlds ASH, \(\mathcal T\) persists and \(M_O\) identifies the observer's path through it. Under collapse-like ASH, commitment prunes physical reality. If leaf branches are crucial to the cosmology, the many-worlds interpretation is the stronger default.

## 8. Decoherence and branch separation

Define branch distance:

\[
d_\mathcal T(b_i,b_j).
\]

Define decoherence functional:

\[
\mathcal D(b_i,b_j).
\]

World-like leaves require:

\[
\mathcal D(b_i,b_j)\approx0
\]

for macroscopically distinct leaves, or inner-product suppression:

\[
\langle\psi_i|\psi_j\rangle\approx0.
\]

Research target: prove that branch depth, defect accumulation, memory divergence, environmental entanglement, or action separation makes macroscopic ASH leaves effectively non-interfering.

## 9. Branch entropy

Define frontier entropy:

\[
S_{branch}(t)=-\sum_{\ell\in L_t}p_\ell\log p_\ell.
\]

Candidate cosmological links:

| Branch quantity | Possible bridge |
|---|---|
| branch entropy | arrow of time / horizon entropy |
| branch depth | cosmic time or scale factor |
| leaf divergence | decoherence/classicality |
| branch density | effective energy density |
| defect-weighted branch density | curvature source |
| branch interference | non-Gaussianity |
| commitment distribution | observer-selection statistics |

## 10. Branch-to-spacetime bridge

The physical bridge must map branch ensembles:

\[
\mathcal B_\ell:(\Gamma,\mathcal T,\mu/\psi,\mathcal M)\to(g_{\mu\nu},T_{\mu\nu},\rho,p,\phi,\ldots)_\ell.
\]

It should not be only:

\[
\mathcal B_\ell(X_t).
\]

The branch ensemble may itself generate effective geometry, entropy, dark-sector behavior, time, decoherence, or statistical observables.

## 11. Empirical route

Empirical testing must proceed in sequence:

1. derive fixed branch-centered equations;
2. test synthetic universes emitted from those equations;
3. recover known parameters;
4. compare to matched non-ASH controls;
5. derive observables;
6. freeze predictions;
7. compare to real data;
8. require independent replication.

No real-data claim is mature until branch dynamics and bridge maps are fixed.

## 12. Candidate empirical signatures

These are targets, not claims:

| Candidate signature | Required derivation |
|---|---|
| parity-conditioned CMB correlations | from parity/integrity dynamics |
| low-\(\ell\) selection rules | from code-coset/branch constraints |
| oscillatory \(P(k)\) residuals | from Enneahcube or branch spectra |
| branch-depth non-Gaussianity | from leaf distribution statistics |
| dark-sector effective fluid | from unresolved branch entropy |
| curvature from defect density | from branch-defect bridge |
| arrow of time | from committed memory growth |
| UV cutoff/smoothing scale | from finite-local coarse-graining |

Each candidate must be derived, simulated, controlled, frozen, and then tested.

## 13. Falsification posture

ASH Cosmology fails or must be demoted if:

- finite algebra is inconsistent;
- branch tree cannot be defined;
- branch measure/amplitude cannot normalize;
- Born-rule or replacement frequency law cannot be supplied for quantum claims;
- no decoherence/separation criterion exists;
- observer memory cannot be embedded in branches;
- no branch-to-geometry bridge exists;
- no stable continuum/causal limit emerges;
- matched controls reproduce the claimed signatures;
- observables cannot be computed from fixed equations;
- predictions are changed after unblinding.

## 14. Immediate milestone

The first serious milestone is not fitting cosmological data. It is:

```text
Define one complete branch-centered ASH universe model,
including local state, branch tree, measure/amplitude law,
commitment rule, decoherence criterion, and one physical bridge candidate.
Then prove closure, branch existence, normalization, and at least one nontrivial invariant.
```

The second milestone is deriving either:

\[
H_{ASH}(z)
\]

or

\[
P_\zeta(k)
\]

from that fixed branch-centered model.

Only then does empirical cosmology begin.
