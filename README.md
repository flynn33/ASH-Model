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

The repository also includes the first validation mechanics around this layer:
an explicit affine calibration contract for future unit-bearing observables, a
diagonal Gaussian likelihood comparator, and deterministic hash-lock validation
for future prediction-ledger entries.  It also includes a dimensionless flat
standard-baseline comparator for future baseline checks.

This layer is implemented in [`src/ash_model/physics.py`](src/ash_model/physics.py)
and verified by [`tests/test_physics.py`](tests/test_physics.py).  It is not a
claim of observed spacetime dynamics or empirical cosmology; those remain
blocked until reviewed physical calibrations, external data products, matched
baselines, and locked scientific predictions exist.

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
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/run_proof_suite.py
pytest
python tools/verify_repository.py
```

After changing manuscript source, bibliography inputs, generated figures, or the committed PDF, refresh the source-input manifest before regenerating the proof certificate:

```bash
python tools/generate_artifacts.py --refresh-figures  # only when figure PNGs intentionally change
python tools/build_manuscript.py
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
python simulation.py
python src/simulate.py --agents 1000 --ticks 250 --noise 0.01 --seed 20260624
```

The tracked ablations explicitly compare uniform starts, zero starts, ASH transforms, no transforms, random weight-four transforms, and bit-flip noise. The resulting binomial envelope is documented as a uniform-hypercube baseline, not as evidence uniquely caused by ASH.

## ASH-Physics validation program

`docs/ash-physics-validation/` defines the proof and empirical-validation program. It adds implementation instructions, proof obligations, preregistration templates, claim-language scanning, and task manifests for the ASH-Physics research track.

ASH-Physics v0.2 implements the finite-observer state space, pair-flip dynamics, internal bridge observables, finite background surrogate, and finite perturbation factors.  The current validation program is intentionally not an empirical result. External likelihoods, standard cosmology baselines, unitful bridge maps, continuum interpretations, and locked predictions remain explicit open gates in `theory/`, `phenomenology/`, `validation/`, `predictions/`, and `proofs/`.

## Repository readiness and wiki

The final repository-readiness audit is recorded in [`docs/final-live-repository-audit.md`](docs/final-live-repository-audit.md). It verifies the finite ASH layer, the ASH-Physics finite-observer layer, generated data and figure manifests, JSON schemas, repository gates, and current proof evidence while preserving the remaining science blockers.

The wiki publication map is documented in [`docs/wiki-publication.md`](docs/wiki-publication.md). The tracked wiki source lives under [`wiki/`](wiki/) and is mirrored to the live GitHub wiki at <https://github.com/flynn33/ASH-Model/wiki>.

## Repository map

- `src/ash_model/` - canonical implementation
- `tests/` - exhaustive and deterministic tests
- `config/ash_mapping_v1.json` - normative mapping configuration
- `proofs/` - generated proof certificate and artifact hashes
- `data/ash-state-reference.csv` - all 512 states and decoder/orbit metadata
- `data/codewords.csv` - all 16 codewords and syndromes
- `data/branch-topology.json` - complete depth-4 branch topology
- `data/ablation-results.csv` - controlled simulation results
- `docs/ash-cosmology/branch-centered-roadmap/v0.2/` - Branch-centered ASH Cosmology roadmap, correction lock, canonical model notes, proof roadmap, empirical validation plan, falsification criteria, and source-evidence package
- `data/ash-cosmology/branch-centered-roadmap/v0.2/` - Machine-readable JSON/YAML catalogs, JSON schema, prediction-ledger templates, CSV summaries, checksums, and provenance manifest for the branch-centered roadmap
- `figures/` - generated, repository-linked evidence figures
- `docs/` - specification, proof, controls, integration, and paper
- `docs/ash-physics-validation/` - ASH-Physics proof and empirical-validation planning package
- `theory/` - finite-observer ASH-Physics postulates, dynamics, bridge, and equation boundaries
- `phenomenology/` - internal observable-interface specifications and external-validation blockers
- `validation/` - finite consistency gates, preregistration surfaces, and external-validation blockers
- `predictions/` - frozen-prediction ledger and falsification criteria
- `axioms-of-existence.json` - explicitly labeled interpretive postulates and narrative implications
- `latex/main.tex` - aligned manuscript source
- `CITATION.cff` - machine-readable citation metadata

## Scientific boundary

This release proves the finite algebra and validates the executable mapping semantics. The feature thresholds, branch priors, reconstruction operators, and score weights are versioned reference-design choices rather than uniquely derived physical constants. It does **not** establish that ASH is an empirically confirmed cosmology, that its branching realizes quantum measurement, or that its code translations uniquely generate Gaussian statistics. Those questions require separately stated falsifiable predictions and external evidence.

## License and citation

See [`LICENSE`](LICENSE) and [`CITATION.cff`](CITATION.cff). For permitted academic use, cite:

Daley, J. (2026). *Adinkra-Stabilized Hypercube Model: Canonical Computational Specification and Reference Implementation*, version 1.1.0.
