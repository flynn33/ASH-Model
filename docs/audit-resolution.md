# Repository Audit Validation and Resolution

## Verdict

The full-repository audit was materially valid. Independent reproduction confirmed its central findings:

- the six historical masks span a rank-four `[9,4,4]` doubly-even code of size 16 and minimum distance four;
- the former ninth coordinate was zero in every mask;
- the nine-dimensional code was not self-dual;
- the former simulations did not decode errors or explicitly evaluate the averaging operator;
- the former data script applied an involution an even number of times and therefore returned its initial sample;
- the former branch routine counted strings but did not define topology, geometry, weights, state semantics, reconstruction operators, scoring, or pruning;
- the supplied CSV was statistically consistent with an ordinary sample of independent fair bits;
- the former histogram image was an unrelated spreadsheet example;
- the former documents asserted more than the executable evidence supported.

The independent reproduction matched the audit's quantitative values: 444 unique CSV states, mean Hamming weight 4.492, population standard deviation about 1.4697, and total-variation distance about 0.02928 from `Binomial(9,1/2)`.

## One constructive refinement

The repair does not leave coordinate 9 inactive. The canonical code is a coordinate permutation of the verified scaffold:

```text
111100000
110011000
101010100
100110001
```

Coordinate 9 is now active and equals parity of coordinates 1-8. Coordinate 8 is zero in every codeword, so code actions preserve the temporal-change measurement while all nine state coordinates remain available to application states.

The repaired statement is:

> ASH uses a 9-bit state space and a rank-four doubly-even linear `[9,4,4]` transform code. Coordinate 9 is the parity/integrity coordinate. The nine-dimensional code is not self-dual. Puncturing the code-invariant eighth coordinate produces the self-dual doubly-even `[8,4,4]` code used for the Adinkra quotient.

## Resolution matrix

| Audit finding | Resolution |
|---|---|
| No authoritative code definition | Added `src/ash_model/code.py`, generator/parity-check matrices, all 16 codewords, and JSON specification |
| Ninth coordinate inactive | Moved the parity-explicit active coordinate to position 9; tests prove activity and parity |
| False nine-dimensional self-duality claim | Removed; proof shows dual dimension five |
| No decoder | Added strict nearest-codeword and affine-orbit decoders |
| No proof of correction | Exhaustively verified all 144 one-bit corruptions and rejected all 576 two-bit corruptions |
| Random walk confused with averaging | Added exact `orbit_average` and Monte Carlo approximation as separate operations |
| Gaussian baseline overclaimed | Added analytical Markov proof and seven controlled ablations |
| Identity data script | Replaced with seeded nontrivial codeword/noise dynamics and metadata |
| No application bit definitions | Defined eight measurements plus coordinate-9 parity |
| No continuous-to-binary rule | Added fixed thresholds, tie rule, and temporal hysteresis |
| No branch-to-state mapping | Added a complete ternary tree with codeword payload semantics |
| No branch geometry/topology | Added segment geometry, historical rendering L-system, and tracked JSON topology |
| No branch weights | Added normalized priors with a proof of conservation |
| No reconstruction semantics | Added 16 decoded deterministic operator combinations |
| No consistency scoring/pruning | Added source, edge, temporal losses and deterministic top-k selection |
| No temporal transition | Added previous-state hysteresis and temporal-change coordinate |
| No exhaustive 512-state reference | Added `data/ash-state-reference.csv` and tests |
| No controlled baselines | Added ASH/no-transform/random-weight-four ablations |
| Unlinked Adinkra figure | Added `Q8/C8`, exact Garden matrices, graph isomorphism, and generated figure |
| Bogus histogram/error figures | Replaced with generated repository-derived figures |
| Validation reports overstated maturity | Rewritten to report only established claims |

## Evidence produced

- `docs/canonical-computational-specification.md`
- `docs/mathematical-proof.md`
- `docs/falsification-and-controls.md`
- `docs/mirmir-integration.md`
- `proofs/computational-certificate.json`
- `proofs/computational-certificate.md`
- `proofs/artifact-manifest.json`
- `proofs/manuscript-manifest.json`
- stale-evidence rejection through recomputed source/artifact hashes and cross-file version checks
- `data/ash-state-reference.csv`
- `data/codewords.csv`
- `data/branch-topology.json`
- `data/ablation-results.csv`
- exhaustive tests in `tests/`

## Additional epistemic clarification

The finite-code audit did not invalidate the repository's philosophical axioms, but their former wording could be read as established physical or consciousness laws. `axioms-of-existence.json` now labels every item as an interpretive postulate, records model dependence, and states that the erasure and self-modeling clauses are constrained analogies or research criteria rather than empirical conclusions.

## Scientific boundary after remediation

The repaired repository is a complete deterministic ASH mapping reference and a suitable specification target for a separately engineered Metal implementation. It proves the stated finite mathematics and validates its software semantics.

The newly authored feature thresholds, branch priors, geometry, operators, and score weights are explicitly versioned engineering choices. The original repository did not determine them uniquely, and this remediation does not claim that they are physically necessary or quality-optimal.

It does not convert interpretive procedural cosmology into experimentally confirmed physics. No code-only proof can substitute for a falsifiable physical prediction and external measurement. The repository now states that boundary explicitly rather than treating simulation output as empirical validation.

## Manuscript integrity

`tools/build_manuscript.py` performs a two-pass build with a fixed source date and writes `proofs/manuscript-manifest.json`. Repository verification recomputes both the LaTeX-source and PDF hashes, so a stale or altered manuscript is release-blocking.
