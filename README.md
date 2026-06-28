# Adinkra-Stabilized Hypercube Model (ASH Model)

**A deterministic reference framework for a 9-bit hypercube, doubly-even code actions, Adinkra quotients, bounded branching, and image/video state mapping**

**Author:** James Daley
**Reference implementation:** version 1.1.0
**Audit-remediation release:** June 24, 2026

## Status and scope

ASH is an exploratory simulation-theory and computational-ontology framework. The repository now distinguishes three kinds of claims:

1. **Proved finite mathematics:** the 9-bit state space, canonical code, decoder radius, code-orbit projection, and Garden-algebra representation.
2. **Specified deterministic computation:** image/video feature mapping, temporal hysteresis, branch-to-state semantics, reconstruction operators, scoring, pruning, and artifact generation.
3. **Interpretive research:** procedural-cosmology and physical interpretations. These are hypotheses, not empirical conclusions established by the code.

The earlier repository overstated self-duality in nine dimensions, error correction in simulations, ASH-specific Gaussian convergence, and branch/Adinkra implementation maturity. Version 1.1.0 resolves those discrepancies and records the evidence in [`docs/audit-resolution.md`](docs/audit-resolution.md).

## Roadmap tracker

The repository-maintained roadmap status log is [`ROADMAP.md`](ROADMAP.md). It tracks identified roadmap items, completion evidence, verification commands, and remaining blockers.

Current roadmap posture after the Roadmap 016 merge:

| Roadmap band | Repository state | Scientific boundary |
|---|---|---|
| R-001 through R-006 | Complete finite core, finite-observer physics layer, prediction-ledger mechanics, sector-mixing workbench, background-bridge diagnostics, and data governance manifest. | Repository mechanics and finite checks only. |
| R-007 through R-011 | Complete finite perturbation sector, branch-measure law, observer-commitment workbench, synthetic unit-bearing bridge, and finite-observer limit hierarchy. | Does not close reviewed physical calibration, differentiable geometry, observed-data likelihoods, empirical validation, or physical model validation. |
| R-012 through R-016 | Complete within their stated synthetic-workbench, readiness, lock-mechanics, and formal-contract scopes: background-equation workbench, bounded matter-sector perturbation workbench, external-likelihood readiness, locked prospective templates, and branch-centered closure contract. | Does not close reviewed physical calibration, a full photon-baryon Boltzmann hierarchy, observed-data scoring, empirical preference, independent replication, or validation of ASH as observed physical cosmology. |

## Verified mathematical core

| Component | Verified result |
|---|---|
| State space | `F_2^9`, 512 vertices, Q9 degree 9 |
| Application integrity states | 256 states satisfying `x9 = x1 xor ... xor x8` |
| Canonical transform code | rank-4 doubly-even linear `[9,4,4]` code |
| Code size / weights | 16 codewords; `{0:1, 4:14, 8:1}` |
| Coordinate 9 | active parity/integrity coordinate |
| Coordinate 8 under code actions | invariant; it remains available as the temporal-change state bit |
| Nine-dimensional self-duality | false; `dim(C)=4`, `dim(C-perp)=5` |
| Punctured code | removing coordinate 8 gives a self-dual doubly-even `[8,4,4]` code |
| Guaranteed correction | every one-bit corruption of a codeword or known affine-orbit state; all tested two-bit codeword corruptions are rejected by policy |
| Code-orbit averaging | exact idempotent projection `T^2=T` |
| Adinkra layer | 16-vertex `Q8/C8` quotient and exact N=8 Garden matrices |
| Controlled-noise limit | uniform state occupancy, with `Binomial(9,1/2)` Hamming marginal |

The generated proof certificate is in [`proofs/computational-certificate.md`](proofs/computational-certificate.md), with the full machine-readable record in JSON. The manuscript manifest records deterministic hashes for the LaTeX source, bibliography inputs, generated figures, and committed PDF in [`proofs/manuscript-manifest.json`](proofs/manuscript-manifest.json).

## Finite-observer physics layer

ASH-Physics v0.2 adds a conservative finite-observer interpretation over the
verified ASH kernel.  The admissible physical state space is the 256-state
parity-valid hyperplane of `F_2^9`; the baseline microscopic dynamics is a
lazy pair-flip Markov kernel that preserves admissibility, is symmetric, and
has the uniform admissible law as a stationary state.

The implemented bridge observables are dimensionless internal quantities:
mean Hamming weight, order parameter, Shannon entropy, and parity-valid
probability.  The finite background equation is the exact Hamming-weight
lumping of the pair-flip dynamics, and the finite perturbation layer is given
by bounded lazy pair-flip mode factors.

Roadmap 007 refines the finite perturbation layer into quotient Walsh-character
shells on the admissible even-parity state space.  It adds exact shell counts,
finite transfer laws, deterministic generated transfer artifacts, and internal
validation outputs.  This remains a finite-observer result; it does not define
metric perturbations, physical wavenumbers, matter power spectra, CMB spectra,
or empirical redshift calibration.

Roadmap 010 adds a synthetic finite-observer unit-bearing bridge from the
accepted Roadmap 009 branch frontier to named SI-unit proxy observables.  It
includes a versioned fiducial calibration contract, deterministic finite
feature extraction, unit-bearing proxy columns, bootstrap samples, covariance
output, provenance, validation JSON, and tests.  This is a repository-local
bridge workbench only; it does not supply reviewed ASH physical calibration
constants, a continuum metric, FRW/LCDM derivation, external likelihood, CMB or
matter-spectrum solver, empirical validation, or locked scientific prediction.

Roadmap 011 closes the finite-observer limit route by adding a nested
parity-valid observer hierarchy over odd levels `1,3,5,7,9`, projective
consistency checks, uniform-fiber verification, finite causal cones,
non-expansion of microscopic pair-flip events under projection, normalized
R010-compatible scale annotations, generated CSV/JSON/PNG artifacts, and
tests.  This is finite graph and projection mathematics only; it does not
derive a differentiable continuum, Lorentzian metric, physical light cone,
Einstein equations, FRW/LCDM dynamics, physical perturbation equations,
CMB/matter spectra, external likelihoods, or empirical cosmology.

Post-R016 finite-observer and branch-centered evidence is split across:

- [`docs/ash-cosmology/unit-bridge/roadmap-010/`](docs/ash-cosmology/unit-bridge/roadmap-010/) for the synthetic unit-bearing bridge.
- [`docs/ash-cosmology/finite-observer-limit/roadmap-011/`](docs/ash-cosmology/finite-observer-limit/roadmap-011/) for the finite projective hierarchy.
- [`docs/ash-cosmology/background-equations/roadmap-012/`](docs/ash-cosmology/background-equations/roadmap-012/) for the synthetic finite-observer background-equation workbench.
- [`docs/ash-cosmology/physical-perturbations/roadmap-013/`](docs/ash-cosmology/physical-perturbations/roadmap-013/) for the bounded matter-sector perturbation workbench.
- [`docs/ash-cosmology/external-likelihoods/roadmap-014/`](docs/ash-cosmology/external-likelihoods/roadmap-014/) for likelihood-readiness contracts and synthetic fixtures.
- [`docs/ash-cosmology/locked-predictions/roadmap-015/`](docs/ash-cosmology/locked-predictions/roadmap-015/) for immutable prospective prediction templates.
- [`docs/ash-cosmology/branch-centered-closure/roadmap-016/`](docs/ash-cosmology/branch-centered-closure/roadmap-016/) for the formal branch-centered closure contract.
- `validation/*/roadmap-0*/outputs/` for machine-readable validation records.
- [`figures/ash-cosmology/finite-observer-limit/v0.1/`](figures/ash-cosmology/finite-observer-limit/v0.1/) for finite-observer hierarchy visual artifacts.

The repository also includes validation mechanics around this layer: explicit
affine and fiducial calibration contracts, a diagonal Gaussian likelihood
comparator, matched synthetic baselines, deterministic hash-lock validation for
locked prediction templates, and a dimensionless flat standard-baseline
relation for baseline checks.

Sector-mixing resolution pass 002 adds a separate eight-payload-coordinate
workbench with deterministic integrity-bit recomputation.  It documents and
tests a sector-refresh kernel that bridges the two payload Hamming-parity
sectors without redefining the existing nine-coordinate finite-observer kernel.

This layer is implemented in [`src/ash_model/physics.py`](src/ash_model/physics.py)
and verified by [`tests/test_physics.py`](tests/test_physics.py) and
[`tests/test_sector_mixing.py`](tests/test_sector_mixing.py).  It is not a
claim of observed spacetime dynamics or empirical cosmology. Reviewed physical
calibration, observed-data scoring, empirical preference over matched
baselines, and independent replication remain outside the completed repository
scopes.

## Canonical state coordinates

Coordinates 1 through 8 are deterministic measurements in `[0,1]`, thresholded with fixed hysteresis. Coordinate 9 is recomputed as parity.

| Bit | Measurement |
|---:|---|
| 1 | mean luminance |
| 2 | RMS contrast |
| 3 | edge energy |
| 4 | texture residual energy |
| 5 | chroma energy |
| 6 | horizontal-gradient energy |
| 7 | vertical-gradient energy |
| 8 | temporal change |
| 9 | parity/integrity of bits 1-8 |

Exact formulas, thresholds, bit ordering, and transition rules are normative in [`docs/canonical-computational-specification.md`](docs/canonical-computational-specification.md) and [`config/ash_mapping_v1.json`](config/ash_mapping_v1.json).

## Install and verify

```bash
python3 -m pip install -e ".[dev]"
python3 tools/generate_artifacts.py
python3 tools/run_proof_suite.py
python3 -m pytest
python3 tools/verify_repository.py
```

After changing manuscript source, bibliography inputs, generated figures, or the committed PDF, refresh the source-input manifest before regenerating the proof certificate:

```bash
python3 tools/generate_artifacts.py --refresh-figures  # only when figure PNGs intentionally change
python3 tools/build_manuscript.py
```

The proof suite exhaustively checks all 512 states, all 16 codewords, every one-bit neighborhood, every two-bit corruption of every codeword, all parity-valid affine anchors, all code orbits, and the exact Garden identities.

## Reference pipeline

```python
import numpy as np
from ash_model.pipeline import map_patch

current = np.linspace(0.0, 1.0, 64).reshape(8, 8)
result = map_patch(current, branch_depth=4, scale=2, top_k=4)

print(result.source_state)
print([candidate.message for candidate in result.selected])
```

The pipeline performs:

`measure -> threshold/hysteresis -> parity state -> code-orbit branches -> reconstruction operators -> source-consistency scoring -> deterministic top-k pruning`

It is a CPU reference for validating semantics before a production GPU or Metal implementation. It does not claim state-of-the-art reconstruction quality.

## Controlled simulation

```bash
python3 simulation.py
python3 src/simulate.py --agents 1000 --ticks 250 --noise 0.01 --seed 20260624
```

The tracked ablations explicitly compare uniform starts, zero starts, ASH transforms, no transforms, random weight-four transforms, and bit-flip noise. The resulting binomial envelope is documented as a uniform-hypercube baseline, not as evidence uniquely caused by ASH.

## ASH-Physics validation program

`docs/ash-physics-validation/` defines the proof and empirical-validation program. It adds implementation instructions, proof obligations, preregistration templates, claim-language scanning, and task manifests for the ASH-Physics research track.

ASH-Physics v0.2 implements the finite-observer state space, pair-flip dynamics, internal bridge observables, finite background surrogate, finite perturbation factors, finite branch-measure normalization law, finite observer-commitment workbench, synthetic unit-bearing bridge workbench, finite-observer limit hierarchy, synthetic background-equation workbench, bounded matter-sector perturbation workbench, likelihood-readiness layer, locked prediction-template mechanics, and branch-centered formal closure contract.  The current validation program is intentionally not an empirical result. Reviewed physical calibrations, observed-data likelihood scoring, physical model validation, and independent replication remain explicit open gates in `theory/`, `phenomenology/`, `validation/`, `predictions/`, and `proofs/`.

`docs/ash-cosmology/background-bridge/pass-003/` records the Pass 003 synthetic background-bridge audit remediation, including numerical convergence checks, deprecation-warning elimination, grid-posterior uncertainty diagnostics, AIC/BIC diagnostics, matched controls, and blocker tracking. This package is synthetic validation only and does not claim observational validation.

## Repository readiness and wiki

The historical repository-readiness audit is recorded in [`docs/final-live-repository-audit.md`](docs/final-live-repository-audit.md). Current readiness evidence is summarized by [`ROADMAP.md`](ROADMAP.md), [`validation/status.json`](validation/status.json), and [`docs/remediation/final-remediation-evidence.json`](docs/remediation/final-remediation-evidence.json); these verify the finite ASH layer, the ASH-Physics finite-observer and branch-centered layers, generated data and figure manifests, JSON schemas, repository gates, and current proof evidence while preserving the remaining science blockers.

The wiki publication map is documented in [`docs/wiki-publication.md`](docs/wiki-publication.md). The tracked wiki source lives under [`wiki/`](wiki/) and is mirrored to the live GitHub wiki at <https://github.com/flynn33/ASH-Model/wiki>.

## Data governance

The tracked data inventory is documented in [`data/README.md`](data/README.md) and machine-recorded in [`data/manifests/data_manifest.json`](data/manifests/data_manifest.json). The manifest covers repository evidence files under `data/`, Roadmap 007-016 synthetic/readiness/lock/closure outputs, pass 003 synthetic diagnostics under `validation/background_bridge/pass_003/outputs/`, and `validation/status.json`.

Validate the manifest with:

```bash
python3 tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
```

No new raw observational dataset is imported by the R012-R016 integration. Future raw data requires explicit provenance, sensitivity, license, and tracking-policy review before it is committed.

## Repository map

- `src/ash_model/` - canonical implementation
- `tests/` - exhaustive and deterministic tests
- `config/ash_mapping_v1.json` - normative mapping configuration
- `proofs/` - generated proof certificate and artifact hashes
- `data/ash-state-reference.csv` - all 512 states and decoder/orbit metadata
- `data/codewords.csv` - all 16 codewords and syndromes
- `data/branch-topology.json` - complete depth-4 branch topology
- `data/ablation-results.csv` - controlled simulation results
- `data/manifests/data_manifest.json` - consolidated data and synthetic-output inventory
- `ROADMAP.md` - repository-maintained roadmap tracker and completion log
- `docs/ash-cosmology/branch-centered-roadmap/v0.2/` - Branch-centered ASH Cosmology roadmap, correction lock, canonical model notes, proof roadmap, empirical validation plan, falsification criteria, and source-evidence package
- `docs/ash-cosmology/linear-perturbations/roadmap-007/` - Roadmap 007 finite linear perturbation sector notes and boundaries
- `docs/ash-cosmology/branch-measure/roadmap-008/` - Roadmap 008 finite branch-measure law notes and boundaries
- `docs/ash-cosmology/observer-commitment/roadmap-009/` - Roadmap 009 finite observer-commitment and branch-separation notes and boundaries
- `docs/ash-cosmology/unit-bridge/roadmap-010/` - Roadmap 010 synthetic unit-bearing bridge notes and boundaries
- `docs/ash-cosmology/finite-observer-limit/roadmap-011/` - Roadmap 011 finite-observer limit notes, formal expressions, and boundaries
- `docs/ash-cosmology/background-equations/roadmap-012/` - Roadmap 012 synthetic finite-observer background-equation workbench notes and boundaries
- `docs/ash-cosmology/physical-perturbations/roadmap-013/` - Roadmap 013 bounded matter-sector perturbation workbench notes and boundaries
- `docs/ash-cosmology/external-likelihoods/roadmap-014/` - Roadmap 014 likelihood-readiness notes, contracts, and boundaries
- `docs/ash-cosmology/locked-predictions/roadmap-015/` - Roadmap 015 locked prediction-template notes and boundaries
- `docs/ash-cosmology/branch-centered-closure/roadmap-016/` - Roadmap 016 formal branch-centered closure notes and boundaries
- `data/ash-cosmology/branch-centered-roadmap/v0.2/` - Machine-readable JSON/YAML catalogs, JSON schema, prediction-ledger templates, CSV summaries, checksums, and provenance manifest for the branch-centered roadmap
- `data/ash-cosmology/linear-perturbations/v0.1/` - Roadmap 007 finite perturbation transfer CSV artifacts
- `data/ash-cosmology/branch-measure/v0.1/` - Roadmap 008 finite branch-measure normalization CSV artifacts
- `data/ash-cosmology/observer-commitment/v0.1/` - Roadmap 009 finite observer-commitment and branch-separation CSV artifacts
- `data/ash-cosmology/unit-bridge/v0.1/` - Roadmap 010 synthetic unit-bearing bridge CSV artifacts
- `data/ash-cosmology/finite-observer-limit/v0.1/` - Roadmap 011 finite-observer limit CSV artifacts
- `data/ash-cosmology/background-equations/v0.1/` - Roadmap 012 background-equation CSV artifacts
- `data/ash-cosmology/physical-perturbations/v0.1/` - Roadmap 013 physical-perturbation CSV artifacts
- `data/ash-cosmology/external-likelihoods/v0.1/` - Roadmap 014 likelihood-readiness CSV artifacts
- `data/ash-cosmology/locked-predictions/v0.1/` - Roadmap 015 locked prediction-template CSV artifacts
- `data/ash-cosmology/branch-centered-closure/v0.1/` - Roadmap 016 closure-matrix CSV artifacts
- `data/ash-physics-sector-mixing/` - Sector-mixing pass 002 CSV evidence, upstream payload manifest, and reproduction metadata
- `figures/ash-cosmology/linear-perturbations/v0.1/` - Roadmap 007 finite perturbation generated figures
- `figures/ash-cosmology/finite-observer-limit/v0.1/` - Roadmap 011 finite-observer limit generated figures
- `figures/ash-cosmology/background-equations/v0.1/` - Roadmap 012 background-equation generated figures
- `figures/ash-cosmology/physical-perturbations/v0.1/` - Roadmap 013 perturbation-workbench generated figures
- `figures/ash-cosmology/external-likelihoods/v0.1/` - Roadmap 014 likelihood-readiness generated figures
- `figures/ash-cosmology/locked-predictions/v0.1/` - Roadmap 015 locked-template generated figures
- `figures/ash-cosmology/branch-centered-closure/v0.1/` - Roadmap 016 closure generated figures
- `figures/ash-physics-sector-mixing/` - Sector-mixing pass 002 finite workbench figures
- `figures/` - generated, repository-linked evidence figures
- `docs/` - specification, proof, controls, integration, and paper
- `docs/ash-physics-validation/` - ASH-Physics proof and empirical-validation planning package
- `theory/` - finite-observer ASH-Physics postulates, dynamics, bridge, and equation boundaries
- `phenomenology/` - internal observable-interface specifications and external-validation blockers
- `validation/` - finite consistency gates, preregistration surfaces, and external-validation blockers
- `validation/linear-perturbations/roadmap-007/` - Roadmap 007 finite perturbation validation notes and generated verification JSON
- `validation/branch-measure/roadmap-008/` - Roadmap 008 finite branch-measure validation notes and generated verification JSON
- `validation/observer-commitment/roadmap-009/` - Roadmap 009 finite observer-commitment validation notes and generated verification JSON
- `validation/unit-bridge/roadmap-010/` - Roadmap 010 synthetic unit-bearing bridge validation notes and generated verification JSON
- `validation/finite-observer-limit/roadmap-011/` - Roadmap 011 finite-observer limit validation notes and generated verification JSON
- `validation/background-equations/roadmap-012/` - Roadmap 012 background-equation validation notes and generated verification JSON
- `validation/physical-perturbations/roadmap-013/` - Roadmap 013 perturbation-workbench validation notes and generated summary JSON
- `validation/external-likelihoods/roadmap-014/` - Roadmap 014 likelihood-readiness validation notes and generated verification JSON
- `validation/locked-predictions/roadmap-015/` - Roadmap 015 locked prediction-template validation notes and generated verification JSON
- `validation/branch-centered-closure/roadmap-016/` - Roadmap 016 formal closure validation notes and generated certificate JSON
- `predictions/` - prediction ledger, locked R015 templates, and falsification criteria
- `axioms-of-existence.json` - explicitly labeled interpretive postulates and narrative implications
- `latex/main.tex` - aligned manuscript source
- `CITATION.cff` - machine-readable citation metadata

## Scientific boundary

This release proves the finite algebra and validates the executable mapping semantics. The feature thresholds, branch priors, reconstruction operators, and score weights are versioned reference-design choices rather than uniquely derived physical constants. It does **not** establish ASH as an empirical cosmology result, does not establish that its branching realizes quantum measurement, and does not establish that its code translations uniquely generate Gaussian statistics. Those questions require separately stated falsifiable predictions and external evidence.

## License and citation

See [`LICENSE`](LICENSE) and [`CITATION.cff`](CITATION.cff). For permitted academic use, cite:

Daley, J. (2026). *Adinkra-Stabilized Hypercube Model: Canonical Computational Specification and Reference Implementation*, version 1.1.0.
