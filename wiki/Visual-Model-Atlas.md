# Visual Model Atlas

The repository tracks figures as evidence artifacts. They are not decorative outputs; they are hash-bound in `proofs/artifact-manifest.json`.

## Figure roles

| Figure | Role |
|---|---|
| `figures/hypercube-3d-projection.png` | finite Q9 projection |
| `figures/adinkra-graph-colored.png` | quotient and Garden-algebra visual |
| `figures/single-bit-error.png` | strict decoder example |
| `figures/simulation-histogram.png` | controlled ablation comparison |
| `figures/branch-topology.png` | bounded branch topology |

## Refresh rule

Default generation verifies committed figure bytes:

```bash
python tools/generate_artifacts.py
```

Only redraw tracked figures intentionally:

```bash
python tools/generate_artifacts.py --refresh-figures
```

Then rerun:

```bash
python tools/build_manuscript.py
python tools/run_proof_suite.py
python tools/verify_repository.py
```

## Claim boundary

A visual can illustrate a verified finite object or controlled experiment. A visual does not establish external physical validation by itself.
