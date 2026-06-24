# Adinkra-Stabilized Hypercube Model

ASH 1.1.0 is a deterministic reference framework built on `F_2^9`, a rank-four doubly-even `[9,4,4]` code, a punctured N=8 Adinkra quotient, and a complete image/video state-mapping pipeline.

## Verified core

- 512 hypercube states and 256 parity-valid application states;
- coordinate 9 as active parity/integrity;
- strict single-bit correction when the decoder is invoked;
- exact code-orbit averaging projection;
- exact Garden matrices and quotient graph;
- bounded branch generation, reconstruction scoring, and pruning;
- controlled statistical baselines.

The nine-dimensional code is not self-dual. The punctured `[8,4,4]` code is self-dual.

## Verify

```bash
python -m pip install -e ".[dev]"
pytest
python tools/generate_artifacts.py
python tools/run_proof_suite.py
python tools/verify_repository.py
```

See `docs/canonical-computational-specification.md`, `docs/mathematical-proof.md`, and `docs/audit-resolution.md` for the authoritative details.
