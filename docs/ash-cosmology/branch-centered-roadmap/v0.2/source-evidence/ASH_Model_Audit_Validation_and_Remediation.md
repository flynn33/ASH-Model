# ASH Model Audit Validation and Remediation Report

**Repository release:** 1.1.0
**Validation date:** 2026-06-24
**Author of project:** James Daley
**Authoritative input snapshot:** `ASH-Model-main.zip`
**Audit reviewed:** `ASH_Model_Full_Repository_Audit.md`

## Executive determination

The audit was **materially valid**. Independent reproduction confirmed every central technical finding that affected the repository's claims:

- the six historical masks span a rank-four doubly-even binary `[9,4,4]` code of size 16 and minimum distance four;
- the historical ninth coordinate is zero throughout that span;
- the length-nine code is self-orthogonal but not self-dual;
- the historical simulations did not invoke a decoder or compute the orbit-averaging operator;
- the historical data script applied the same XOR involution 1,000 times, so its net code transform was the identity;
- historical branch strings did not alter states, produce a saved topology, define weights, or select reconstruction operators;
- the historical CSV is statistically consistent with an ordinary fair-bit sample;
- the supplied histogram was a student-score spreadsheet example, and the single-bit figure contained eight bits rather than a nine-bit ASH state;
- the historical repository did not contain the complete application mapping, Garden matrices, branch-to-state semantics, reconstruction operators, scoring, pruning, or exhaustive state reference that its mature claims required.

The audit did not show that the finite scaffold was invalid. It showed that the documentation and validation claims exceeded the implementation. The remediation therefore retained the verified code structure, corrected its mathematical description, and built the missing executable layer.

## Independent reproduction of the original snapshot

| Quantity | Reproduced result |
|---|---:|
| Historical sample masks | 6 |
| GF(2) rank | 4 |
| Span size | 16 |
| Minimum distance | 4 |
| Weight distribution | `{0:1, 4:14, 8:1}` |
| Historical coordinate-9 values | `{0}` |
| Self-orthogonal | yes |
| Dual size in `F_2^9` | 32 |
| Self-dual in `F_2^9` | no |
| CSV shape | `1000 x 9` |
| Unique CSV states | 444 |
| Mean Hamming weight | 4.492 |
| Population standard deviation | 1.4696720723 |
| TV distance to `Binomial(9,1/2)` | 0.02928125 |
| Historical fixed-transform ticks | 1,000 |
| Historical net fixed transform | identity |

The machine-readable reproduction record is `ASH_Model_Original_Audit_Reproduction.json`.

## Canonical repair

The repaired transform code is the row span of

```text
111100000
110011000
101010100
100110001
```

This is a coordinate permutation of the verified historical scaffold. It preserves the valid `[9,4,4]` algebra while making coordinate 9 an active parity/integrity coordinate:

```text
c9 = c1 xor c2 xor c3 xor c4 xor c5 xor c6 xor c7 xor c8
```

Coordinate 8 is zero in every transform codeword, so code translations preserve that application coordinate. Puncturing coordinate 8 gives the doubly-even self-dual `[8,4,4]` code used for the Adinkra quotient. The repaired repository never calls the length-nine code self-dual.

## Missing components built

The release adds a canonical Python package and versioned specification covering:

1. exact bit ordering, serialization, `F_2^9`, all 512 states, Q9 adjacency, planes, parity-valid states, and affine code orbits;
2. the generator and parity-check matrices, all 16 codewords, syndromes, rank, distance, dual, puncturing, encoding, and strict bounded-distance decoding;
3. exhaustive codeword and known-affine-orbit single-bit recovery with explicit rejection beyond radius one;
4. the exact orbit-averaging operator and a separately labeled Monte Carlo approximation;
5. eight deterministic image/video measurements, fixed thresholding, hysteresis, coordinate-9 parity, and temporal transition rules;
6. a complete bounded ternary branch tree with normalized priors, codeword/state semantics, saved topology, geometric segments, and the historical rendering grammar;
7. sixteen deterministic reconstruction-operator combinations, source/edge/temporal scoring, duplicate-leaf aggregation, and deterministic top-k pruning;
8. the punctured-code quotient `Q8/C8`, eight exact signed-permutation Garden matrices, and a color-preserving graph isomorphism;
9. controlled simulations and matched no-transform/random-transform baselines;
10. regenerated repository-linked figures, data tables, manuscript, machine-readable proof certificate, artifact manifest, and manuscript source-to-PDF manifest.

The measurement thresholds, branch priors, geometry constants, reconstruction operators, and score weights are deliberately identified as **versioned reference-design choices**. They make the scaffold executable but are not presented as uniquely derived physical constants or empirically optimal parameters.

## Exact proof results

The generated certificate reports `all_checks_pass: true` and establishes:

| Proof item | Exact result |
|---|---:|
| Hypercube states | 512 |
| Integrity-valid states | 256 |
| Full/integrity code orbits | 32 / 16 |
| Code rank / size / distance | 4 / 16 / 4 |
| Codeword weights | `{0:1, 4:14, 8:1}` |
| Length-nine self-duality | false |
| Punctured `[8,4,4]` self-duality | true |
| Exact codewords decoded | 16 |
| Single-bit codeword corruptions corrected | 144 |
| Two-bit codeword corruptions rejected | 576 |
| Exact affine states checked | 4,096 |
| Affine single-bit recoveries checked | 36,864 |
| Projection idempotence residual | 0.0 |
| Projection output code-invariant | true |
| Garden matrices | 8 signed permutations |
| Maximum Garden integer residual | 0 |
| Quotient vertices / edges | 16 / 64 |
| Quotient-to-matrix isomorphism | true |
| Depth-4 branch nodes / leaves | 121 / 81 |
| Unique branch operator messages | 16 |
| Leaf-weight sum | 1.0 |
| Uniform-stationary residual | `4.336808689942018e-19` |

The certificate records SHA-256 hashes for 76 normative source and documentation files. Eleven generated data/figure artifacts are separately hashed with byte counts. The manuscript manifest binds the seven-page PDF to the exact LaTeX source, project version, and fixed release epoch.

## Validation results

The final packaged repository was extracted into a clean directory and validated again.

```text
pytest -q                                      38 passed
proof-suite checks                             10/10 passed
repository claim violations                   0
missing required artifacts                    0
artifact hash/size mismatches                  0
manuscript source/PDF mismatches               0
source-certificate mismatches                  0
cross-file version mismatches                  0
JSON files parsed                              11
YAML/CFF files parsed                           9
discussion/configuration validators             3 passed
wheel build and isolated core import             passed
PDF render inspection                           7 pages passed
```

The controlled tracked simulation contains 1,000 binary nine-bit rows, 439 unique terminal states, mean Hamming weight 4.536, and TV distance 0.03165625 from the exact binomial marginal. It is labeled as a controlled mixing sample, not evidence of ASH-specific Gaussian causation.

## Deliberate tamper tests

Repository verification was also tested negatively on disposable copies:

| Deliberate alteration | Expected result | Observed result |
|---|---|---|
| none | pass | pass |
| append data to `README.md` | reject stale source certificate | rejected |
| append data to a generated figure | reject artifact hash/size | rejected |
| append data to the manuscript PDF | reject PDF hash/size | rejected |
| change only `VERSION` | reject source, manuscript version, and cross-file version | rejected |

The machine-readable results are in `ASH_Model_Verifier_Negative_Tests.json`.

## Scientific boundary

This release rigorously proves the stated finite code, graph, projection, decoder, branch-count, and Garden-algebra results and verifies the deterministic software semantics. It does not establish empirical cosmology, observed physical supersymmetry, quantum measurement probabilities, superior reconstruction quality, or a unique physical derivation of the newly authored mapping constants. Those require independent falsifiable predictions, external data, and matched empirical evaluation.

The philosophical axioms remain part of the project, but each is now labeled as an interpretive postulate. The repository no longer presents relational existence, compressibility, erasure, persistence, or self-modeling criteria as consequences proved by the finite implementation.

## Reproduction commands

```bash
python -m pip install -e ".[dev]"
python tools/build_manuscript.py        # required after LaTeX changes
python tools/generate_artifacts.py
python tools/run_proof_suite.py
pytest -q
python tools/verify_repository.py
python tools/audit_simulation_data.py
```

## Deliverable hashes

```text
a0dc5eaa483ed4042708eee09d84c1bc0e5a8a63495e9b99357eed1eb9a8455c  ASH-Model-v1.1.0-audit-remediated.zip
a25e0df4b9567e82e03b29620726d141590770b6eacd138542742b3c893a0629  ASH-Model-Preprint-v1.1.0.pdf
e37e4fce9c3e66e20bc70ca864489b37052ef1fd28ad66d9bf02fcf668c0c496  ASH-Model-v1.1.0-computational-certificate.json
1263bae02fac8436be4a78400844b1b4adf183fc890c8c9d9a5821b7078d4d79  ASH-Model-v1.1.0-manuscript-manifest.json
5d5ab2abebaf2bc749a296032c222d52dc2d17e6be80673ac8bb68673f20a85f  ash_model-1.1.0-py3-none-any.whl
```

## Conclusion

The audit's substantive criticism was correct, and the identified implementation/evidence gaps have been repaired. The resulting release is a complete deterministic ASH mapping reference with exhaustive finite proof, controlled statistical claims, reproducible artifacts, explicit epistemic boundaries, and release-blocking consistency checks.
