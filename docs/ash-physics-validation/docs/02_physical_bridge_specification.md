# Physical Bridge Specification

## Purpose

The bridge map is the central missing object between ASH finite algebra and physics. Without it, ASH remains a formal discrete system rather than a physical theory.

## Required map

Define a scale-dependent bridge:

```text
B_l: {x_v}_{v in Gamma} -> (g_mn, T_mn, rho, p, phi^A, J^m, ...)
```

where `l` is the observation or coarse-graining scale.

The map must explain how ASH configurations generate or approximate:

- spacetime events;
- dimensionality;
- distance;
- time;
- causal order;
- metric geometry;
- stress-energy;
- matter fields;
- curvature;
- probabilities or amplitudes.

## Fixed-before-data requirement

The bridge map must be specified before cosmological data fitting. Any bridge map changed after observing a data residual defines a new model version and requires a new validation cycle.

## Minimal repository deliverables

Create:

```text
theory/coarse-graining-and-bridge-map.md
phenomenology/observables_spec.md
validation/synthetic-recovery/README.md
```

Each must identify:

- input state variables;
- output physical quantities;
- units;
- free parameters;
- derived parameters;
- numerical algorithms;
- validation tests;
- unresolved assumptions.

## Required proof obligations

The bridge must satisfy or explicitly fail:

1. consistency under code-equivalent states;
2. stability under small admissible perturbations;
3. convergence under refinement or coarse-graining;
4. locality or declared nonlocality;
5. compatibility with conservation laws;
6. compatibility with observed macroscopic dimensionality;
7. non-degenerate mapping to measurable quantities.

## Prohibited shortcut

Do not infer physical confirmation from visual resemblance, bell-shaped histograms, symbolic analogies, or successful finite algebra verification. Only derived physical observables can be compared to observation.
