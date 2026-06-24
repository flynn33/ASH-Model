# Causal Structure

Status: Draft

## Definitions

- Causal relation: an ordering or dependency relation between microscopic ASH events or states.
- Propagation bound: a limit on how state changes influence separated degrees of freedom.
- Nonlocal declaration: an explicit statement that no finite propagation bound is claimed.

## Assumptions

- The current finite reference implementation does not define physical spacetime causality.
- Branch topology in the reference package is computational structure, not a completed physical causal graph.

## Theorem or model obligations

- Define the event set, adjacency relation, and update neighborhood.
- Prove locality under the selected dynamics, or declare and justify nonlocal behavior.
- Define how causal order behaves under coarse-graining.
- Specify whether causal structure is fixed, emergent, or state dependent.

## Required tests

- Finite propagation tests for any bounded-neighborhood dynamics.
- Counterexample search for out-of-bound influence.
- Consistency checks between causal assumptions and observable maps.

## Known gaps

- No causal graph or metric relation is defined.
- No propagation bound is derived.
- No compatibility proof exists between branch topology and physical causality.

## Verification status

Blocked until microscopic dynamics and bridge-map definitions exist.
