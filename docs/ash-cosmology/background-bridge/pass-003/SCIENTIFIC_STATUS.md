# Scientific Status

## Classification

Pass 003 is a synthetic validation and numerical-diagnostics track. It is
useful for testing whether the implemented bridge can recover its own injected
parameters and reject matched controls under deterministic conditions.

## What Is Supported

- The nested LCDM limit is obtained by setting `beta_branch = 0`.
- The branch template preserves local `H0` because `q_branch(0) = 0`.
- The tested template is bounded for nonnegative redshift and positive
  `gamma_branch`.
- Synthetic ASH data recover the injected bridge parameters within the stated
  tolerances.
- Matched LCDM and random smooth-template controls are present.
- LCDM synthetic data do not force a nonzero branch coupling under the current
  grid and tolerances.

## What Is Not Supported

- No external cosmology dataset is fit in this pass.
- No BAO, SNe, CMB, matter-power, or perturbation likelihood is implemented.
- No branch amplitude law derives `gamma_branch`.
- No full stress-energy tensor or equation of state is derived.
- No continuum-limit geometry theorem is supplied.
- No locked prediction is created.

## Working Interpretation

The branch scalar is a candidate effective background term used for controlled
tests. It should remain labeled as a phenomenological bridge until a reviewed
branch-to-geometry derivation or a stronger replacement is available.
