# Roadmap 007 Linear Perturbation Validation

This directory records validation outputs for the finite-observer ASH linear
perturbation sector.

## Validation status

The Roadmap 007 validation target is internal finite consistency only:

- exact enumeration of 256 admissible states;
- exact enumeration of 256 restricted Walsh quotient characters;
- exact shell counts `1, 9, 36, 84, 126`;
- pair-flip eigenmode residual at numerical precision;
- shell-power transfer check for a deterministic random perturbation;
- Green-function impulse-response generation.

## Not validated here

This directory does not validate:

- physical spacetime dynamics;
- metric perturbation equations;
- observed redshift behavior;
- matter power spectra;
- CMB spectra;
- external likelihoods or baselines.

## Generate

From the repository root:

```bash
python tools/generate_linear_perturbations.py --out-root . --refresh-figures
```

The generator writes:

```text
validation/linear-perturbations/roadmap-007/outputs/verification.json
```

## Gate

The validation JSON should report:

```text
num_states = 256
num_characters = 256
shell_counts = {"0":1, "1":9, "2":36, "3":84, "4":126}
max_eigen_residual <= 1e-12
max_relative_error <= 1e-10
```
