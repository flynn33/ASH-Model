# Mirmir Integration Contract

## Purpose

This document defines the boundary between ASH's deterministic reference semantics and a future Mirmir Metal upscaler. It avoids embedding under-specified research concepts directly into production shaders.

## Required pipeline order

```text
source patch/frame pair
  -> eight normalized measurements
  -> hysteretic 8-bit payload
  -> coordinate-9 parity
  -> depth-bounded branch messages
  -> [9,4,4] codeword encoding
  -> affine branch states
  -> decoded reconstruction operators
  -> source/edge/temporal score
  -> deterministic top-k pruning
  -> selected reconstruction
```

## Stable ABI concepts

A production implementation should preserve:

- coordinate order and integer serialization;
- the four-row generator matrix;
- the 16 message/codeword pairs;
- coordinate-9 parity relation;
- strict correction radius one;
- branch action-to-message toggle rule;
- deterministic tie-breaking by message integer;
- configuration version in output metadata.

## GPU conformance vectors

Use these tracked artifacts as CPU/GPU comparison sources:

- `data/codewords.csv` - all encodings and syndromes;
- `data/ash-state-reference.csv` - all state conversions and decoder classes;
- `data/branch-topology.json` - full branch path/message/state mapping;
- `config/ash_mapping_v1.json` - thresholds and branch constants;
- `proofs/computational-certificate.json` - expected invariant counts.

A Metal implementation should match these bit-exactly. Floating feature and reconstruction values should be compared with an explicitly chosen tolerance and recorded precision mode.

## Decoder policy

The GPU must not choose a codeword at distance two. A fast syndrome decoder may replace brute-force search only when it reproduces the same three statuses:

```text
exact
corrected
uncorrectable
```

Unknown affine anchors must not be guessed.

## Temporal state

Each patch or tile carries the previous parity-valid state. The temporal-change measurement uses the previous source patch, while hysteresis uses the previous state bits. Coordinate 9 is recomputed rather than carried forward.

A scene cut or invalid previous state resets history and uses non-hysteretic thresholding.

## Candidate budget

Depth four generates 81 semantic leaves but only 16 unique messages. Aggregate priors by message before applying reconstruction operators. This bounds the reference operator budget at 16 candidates per patch. Top-k can be selected after scoring.

## Production substitutions

The current operator basis is a conformance reference, not a quality ceiling. Mirmir may replace it with Metal kernels, learned filters, or content-adaptive operators only under a new versioned operator specification. The ASH code, branch, recovery, and scoring interfaces should remain separable so matched ablations are possible.

## Release gate

Before using ASH in production, require:

1. CPU/GPU bit-exact code and branch conformance;
2. image-feature tolerance tests across pixel formats;
3. source consistency and temporal flicker benchmarks;
4. non-ASH operator-prior ablations;
5. performance and memory profiling;
6. invalid-state and two-bit corruption tests;
7. versioned shader/config artifact hashes.
