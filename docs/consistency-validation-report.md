# Consistency Validation Report

## Result

The code, specification, generated data, figures, and manuscript are aligned for version 1.1.0.

## Alignment checks

| Claim | Source of truth | Verification |
|---|---|---|
| `[9,4,4]` rank-four code | `src/ash_model/code.py` | exhaustive certificate |
| coordinate-9 parity | code and mapping config | all codewords and mapped states tested |
| coordinate-8 code invariance | generator matrix | all orbits tested |
| correction radius one | strict decoder | all one-/two-bit cases tested |
| exact averaging operator | `src/ash_model/projection.py` | `T^2=T` and invariance tests |
| Adinkra/Garden relation | `src/ash_model/adinkra.py` | exact integer identities and graph isomorphism |
| image/video coordinates | canonical specification/config | known-patch, bounds, and exact config-conformance tests |
| branch semantics | `src/ash_model/branching.py` | counts, weights, state and geometry tests |
| reconstruction/pruning | `src/ash_model/reconstruction.py` | range, source and deterministic order tests |
| Hamming baseline | Markov proof and ablations | analytical and tracked controls |
| evidence freshness | source/artifact manifests | recomputed SHA-256 and byte-count checks |
| release version | VERSION, package, config, citation, certificate | exact equality check |

## Explicitly excluded statements

The repository does not state that the nine-dimensional code is self-dual, that noise is corrected without a decoder, that ASH uniquely causes Gaussian statistics, that branch weights are quantum probabilities, or that the model is empirically validated cosmology.
