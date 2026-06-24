# Phenomenology Specifications

Status: finite-observer interface specified

This directory defines the observable interface for the finite-observer
ASH-Physics layer.  The interface is internal and dimensionless.  It does not
claim observational validation.

## Files

- `ash_background_spec.md`: finite Hamming-weight background equation.
- `ash_perturbations_spec.md`: finite perturbation-mode decay factors.
- `primordial_spectrum_spec.md`: conditions for any future spectrum claim.
- `observables_spec.md`: bridge observables implemented in `ash_model.physics`.

## Current boundary

The finite-observer observables are implemented and tested.  Any external
phenomenology remains blocked until a unitful bridge, data product, likelihood,
and preregistration exist.
