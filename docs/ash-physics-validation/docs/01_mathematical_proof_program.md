# Mathematical Proof Program

## Core separation

Mathematical proof can establish that consequences follow from ASH definitions. It cannot by itself prove that the physical universe instantiates those definitions.

The proof program must therefore be divided into:

1. finite algebra proofs;
2. physical postulate consistency proofs;
3. dynamics proofs;
4. continuum or finite-observer limit proofs;
5. observable-derivation proofs.

## Current finite layer

The finite layer is considered established only for claims covered by exhaustive verification or explicit proof certificates, including:

- binary state space over `F_2^9`;
- canonical rank-4 doubly-even `[9,4,4]` code;
- codeword enumeration;
- minimum distance;
- single-bit decoder behavior where implemented;
- projection idempotence;
- punctured `[8,4,4]` Adinkra/Garden representation where verified;
- finite branch and reconstruction semantics where implemented.

These facts do not automatically imply physical cosmology.

## Required physical definitions

Define an ASH physical state as one of the following, or explicitly choose a different formalism:

```text
x_v(t) in E subset F_2^9
```

where:

- `v` is a site, event, observer cell, causal-set element, or field register;
- `t` is a discrete update index or emergent ordering label;
- `E` is the admissible ASH local state set.

The repository must define:

- what `v` represents physically;
- what adjacency means;
- whether time is fundamental or emergent;
- whether updates are deterministic, stochastic, reversible, or quantum;
- what quantities are conserved;
- how dimensional units enter the theory;
- which parameters are fixed, derived, or fitted.

## Dynamics theorem obligations

For a deterministic update:

```text
x_v(t + 1) = F_theta(x_v(t), {x_u(t): u adjacent to v})
```

prove or mark unresolved:

1. closure of admissible states;
2. existence for all admissible initial configurations;
3. uniqueness where deterministic;
4. finite propagation speed or stated nonlocality;
5. preservation of invariants;
6. stability under perturbations;
7. compatibility with the finite decoder and projection layer.

For stochastic dynamics:

```text
P_theta(X_{t + 1} | X_t)
```

prove or mark unresolved:

1. nonnegativity;
2. normalization;
3. Markov property or reason for memory;
4. stationary distributions where claimed;
5. detailed balance if claimed;
6. ergodicity if claimed;
7. convergence rates if claimed.

## Symmetry and gauge obligations

Distinguish among:

- code automorphisms;
- hypercube symmetries;
- graph symmetries;
- gauge redundancies;
- physical spacetime symmetries;
- supersymmetry-like algebraic identities.

A Garden-algebra identity is not sufficient to claim physical supersymmetry unless the repository also defines physical bosonic fields, fermionic fields, supercharges, an action or Hamiltonian, and closure on physical states.

## Continuum or finite-observer limit

ASH must either derive a controlled continuum limit or explicitly define a finite-observer theory that reproduces continuum observations within declared error bounds.

The limiting program must address:

- effective dimensionality;
- metric or causal structure;
- approximate Lorentz invariance or bounded violation;
- energy and momentum;
- stable propagating modes;
- positive probabilities;
- absence of ghost or gradient instabilities;
- scale dependence and lattice artifacts.

## Cosmological equation obligations

Before empirical fitting, derive:

```text
H^2(a) = H_ASH^2(a; theta)
```

and perturbation equations sufficient to compute:

```text
D_L(z)
D_M(z)
H(z)
r_d
C_l^TT, C_l^TE, C_l^EE, C_l^phiphi
P_m(k, z)
f sigma_8(z)
P_zeta(k)
```

If ASH modifies gravity, matter, dark energy, dark matter, neutrinos, or primordial perturbations, each modification must be stated as an equation, not as interpretive language.

## Distinctive prediction requirement

ASH must derive at least one fixed prediction that is not a flexible post-hoc fit. Strong candidates include:

- a fixed relation among cosmological parameters;
- a parameter-free correction to the primordial spectrum;
- a parity or selection rule in correlation functions;
- a discrete scale or oscillatory feature;
- a modified growth relation;
- a bounded deviation from general relativity;
- a cosmic-topology signature.

No item is an ASH prediction until derived from fixed definitions and frozen before validation.
