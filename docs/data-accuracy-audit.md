# Generated Data Accuracy Audit

## Provenance

Tracked data artifacts are refreshed with:

```bash
python tools/generate_artifacts.py
```

Tracked figure artifacts are bound by the same manifest hashes and byte sizes.
When intentionally updating figure PNGs, redraw them with:

```bash
python tools/generate_artifacts.py --refresh-figures
```

The resulting hashes and byte sizes are stored in `proofs/artifact-manifest.json`.

## `simulation-results.csv`

The file contains 1,000 seeded 9-bit terminal states produced by 250 ticks of independently sampled codeword translations plus 1% single-bit noise. Metadata records the seed, parameters, and total-variation distance. It is a controlled sample, not evidence that ASH uniquely produces its Hamming histogram.

## `ash-state-reference.csv`

Contains exactly 512 rows. Each row records the bit string, Hamming plane, integrity relation, code-orbit identifier, canonical representative, nearest-code distance/tie count, and strict decoder status.

## `codewords.csv`

Contains exactly 16 message/codeword rows. Every syndrome is zero and weights have distribution `{0:1,4:14,8:1}`.

## `branch-topology.json`

Contains 121 nodes and 81 depth-four leaves. Every node records path, parent, message, codeword, state, prior weight, segment geometry, and heading.

## `ablation-results.csv`

Contains seven named controls. Interpretation must follow `docs/falsification-and-controls.md`.
