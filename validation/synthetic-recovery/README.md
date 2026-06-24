# Synthetic Recovery Validation

Status: finite-observer smoke gate implemented; external recovery blocked

## Implemented finite gate

The current finite-observer gate verifies that a known Hamming-weight
background law can be lifted to a state law, evolved through the pair-flip
kernel, and lumped back to the same result produced by the background kernel.

Evidence:

- `tests/test_physics.py::test_weight_background_kernel_matches_direct_state_kernel_lumping`

## External recovery blocker

Recovery against generated physical data remains blocked until a unitful
bridge, likelihood, priors, and synthetic data generator are specified.
