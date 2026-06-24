# Evidence and Artifacts

This page describes how repository evidence is generated and checked.

## Artifact policy

```mermaid
flowchart TD
    A["tools/generate_artifacts.py"] --> B["Regenerate deterministic data"]
    A --> C["Verify tracked figure files by hash"]
    B --> D["proofs/artifact-manifest.json"]
    C --> D
    E["tools/build_manuscript.py"] --> F["proofs/manuscript-manifest.json"]
```

The default generator does not redraw tracked PNG figures. It verifies their committed bytes and records them in `proofs/artifact-manifest.json`. Use `--refresh-figures` only when intentionally updating the tracked figure files.

## Generated data

| Path | Role |
|---|---|
| `data/codewords.csv` | all messages, codewords, weights, and syndromes |
| `data/ash-state-reference.csv` | all 512 states and decoder/orbit metadata |
| `data/branch-topology.json` | depth-4 bounded branch topology |
| `data/simulation-results.csv` | seeded terminal simulation sample |
| `data/simulation-metadata.json` | simulation parameters and interpretation |
| `data/ablation-results.csv` | matched controls and ablations |

## Figures

| Path | Role |
|---|---|
| `figures/hypercube-3d-projection.png` | deterministic projection of Q9 vertices |
| `figures/adinkra-graph-colored.png` | Garden-algebra Adinkra layer |
| `figures/single-bit-error.png` | strict decoder recovery example |
| `figures/simulation-histogram.png` | controlled ablation plot |
| `figures/branch-topology.png` | bounded branch topology |

## Verification commands

```bash
python tools/generate_artifacts.py
python tools/check_generated_outputs.py . --include-manuscript
python tools/verify_repository.py
```
