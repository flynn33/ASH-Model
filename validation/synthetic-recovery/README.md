# Synthetic Recovery Validation

Status: Blocked

## Purpose

Synthetic recovery tests will verify whether a frozen ASH-Physics model can recover known parameters from generated data before any real-data validation.

## Required inputs

- Frozen dynamics and bridge map.
- Background and perturbation equations.
- Likelihood function and priors.
- Synthetic data generator with recorded seeds.

## Acceptance gates

- Coverage and bias targets are preregistered.
- Recovery succeeds across representative parameter settings.
- Failure cases are recorded without changing the frozen model version.

## Current blocker

The physical model and likelihood are not yet defined.
