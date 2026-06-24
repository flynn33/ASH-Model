# Microscopic State and Dynamics

Status: Draft

## Definitions

- Microscopic ASH state: the proposed physical state object before coarse-graining.
- Admissible state: an ASH state satisfying the selected physical constraints and the finite-kernel parity conventions.
- Dynamics: the deterministic, stochastic, reversible, irreversible, or quantum update rule applied to microscopic states.

## Assumptions

- The finite ASH code actions are already verified as algebraic transforms.
- A physical dynamics must be specified separately from the current reference branch-generation and reconstruction pipeline.
- If stochastic dynamics are introduced, normalization and positivity are required proof obligations.

## Theorem or model obligations

- Define the microscopic state space and admissibility conditions.
- Define the update rule, time parameter, boundary conditions, and allowed randomness.
- Prove or explicitly reject closure of admissible states under the update rule.
- Prove existence and uniqueness where deterministic evolution is claimed.
- Identify conserved quantities, invariants, and gauge redundancy.

## Required tests

- Exhaustive finite-state tests where the state space remains finite.
- Property tests for closure, normalization, positivity, and invariant preservation.
- Regression tests that compare dynamics-independent finite-kernel artifacts against the current certificate.

## Known gaps

- No physical update rule is selected.
- No locality, reversibility, or stochastic law is defined.
- No numerical solver exists for a physical dynamics.

## Verification status

Blocked until a microscopic dynamics is specified.
