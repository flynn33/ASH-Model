# R-014 Addendum: Matched Empirical Baselines and Data Products

R-014 defines the metadata and comparison policy required before external-data scoring.

## Metadata-only reviewed product registry

The repository registry is intentionally metadata-only. It lists official external product targets and required ingestion fields, but it does not redistribute observational data.

## Matched baselines

The minimal matched suite is:

- `LCDM_nested_baseline`: $\Omega_{ASH}=0$, $\alpha_\mu=0$.
- `ASH_background_only`: background term active, perturbation modifier off.
- `ASH_perturbation_only`: perturbation modifier active, background term off.
- `ASH_truth_family`: synthetic full-family fixture.

A future ASH-specific empirical claim must be demoted if a matched non-ASH or ablated control reproduces the claimed signature with equal or better preregistered score.

## Boundary

The included CSV files are deterministic synthetic fixtures. They are not Planck, Pantheon+, DESI, BOSS, or other third-party observational measurements.
