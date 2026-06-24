# Python Validation Report

**Version:** 1.1.0
**Validation command:** `python -m pytest`

## Scope

The test suite validates the executable claims made by the canonical specification. It does not label interpretive cosmology as proven.

## Coverage

- all 512 state integer/bit round trips;
- degree-nine adjacency for every state;
- exact binomial plane counts;
- all 256 integrity-valid states;
- 32 full code orbits and 16 integrity orbits;
- code rank, size, distance, weights, parity, and dual properties;
- all 16 message/codeword encodings;
- all 144 one-bit corruptions;
- all 576 two-bit corruptions;
- full 512-state decoder classification;
- all 36,864 parity-anchor affine one-bit recoveries;
- orbit-projection linearity, invariance, and idempotence;
- exact Garden algebra and quotient isomorphism;
- feature bounds, threshold ties, hysteresis, and temporal behavior;
- branch counts, weights, geometry, state mapping, and recovery;
- reconstruction range, source re-projection, score, and pruning;
- Markov-kernel stochasticity and uniform stationary distribution;
- normative JSON/executable-constant conformance;
- repository claim-language guardrails;
- source-hash, artifact-hash, and version freshness checks.

## Required commands

```bash
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/build_manuscript.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
```

## Current result

The current local validation pass reports `83 passed`. Exact proof counts are stored in `proofs/computational-certificate.json` rather than duplicated manually here.
