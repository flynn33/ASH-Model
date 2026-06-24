# Falsification Criteria

Status: finite-observer criteria specified; external criteria blocked

## Purpose

This file records the criteria that can reject or weaken future ASH-Physics claims before observational validation begins.

## Required criteria

- A physical bridge map must be frozen before observable comparison.
- Predictions must be registered in `prediction-ledger.json` before evaluation.
- Matched baselines must use the same data cuts and likelihood interface.
- Failed synthetic recovery blocks real-data claims that depend on the failed component.
- Failed numerical convergence blocks claims that depend on the failed solver.
- For the finite-observer layer, failure of stochastic normalization,
  parity closure, uniform stationarity, background-kernel lumping, or bounded
  mode factors rejects the current finite dynamics.

## Current status

No external prediction is locked. No empirical rejection test has been run.
Finite-observer rejection tests are implemented in `tests/test_physics.py`.
