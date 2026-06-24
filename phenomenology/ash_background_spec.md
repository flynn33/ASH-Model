# ASH Background Specification

Status: Draft

## Definitions

- Background state variables: homogeneous or averaged quantities produced by the bridge map.
- Evolution parameter: the time, scale, or ordering variable used by the background equations.

## Required specification

- Variable names, units, and domains.
- Equations of motion and initial-condition surface.
- Baseline limit and comparison model.
- Numerical solver accuracy requirements.

## Acceptance gates

- Equation derivation reviewed against `theory/cosmological-background.md`.
- Solver reproduces known baseline behavior in the declared limit.
- Validation inputs are frozen before data comparison.

## Current status

Blocked until background equations are derived.
