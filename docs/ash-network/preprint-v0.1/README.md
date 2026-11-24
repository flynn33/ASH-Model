# ASH-Network preprint research package — v0.1

Prepared 24 November 2026 from ASH-Network revision `eef17dc023732c8897193345d1c3e89f56a3a21f` and ASH specification revision `5b2880d32425f2c84c33a52c5b191c38a66fec55`.

## Files

- [ASH-Network preprint (PDF)](ASH-Network_James_Daley.pdf) by James Daley.
- `ASH-Network_Preprint_Draft_v0.1.md`: editable manuscript, equations, result tables, related work, limitations, and declarations.
- `ASH-Network_Evidence_Ledger.json`: source locations and reading depth, claim mappings, coverage, searches, negative evidence, and open gaps.
- `ASH-Network_Paper_Development_Notes.md`: title options, outline, thesis, and remaining author decisions.
- `verify_calculations.py`: standalone Python reference check for the stated finite code and numerical derivations. Requires Python 3.10 or newer and uses only the standard library.
- `independent_calculations.json`: results of that calculation, explicitly distinct from native application reproduction.
- `PACKAGE_SHA256SUMS.txt`: hashes for the deliverable files.

## Recheck the calculations

```sh
python3 verify_calculations.py
```

This does not run ASH-Network's native tests, the geometry benchmark, an agent host, or model inference. Those experiments are reported from inspected repository evidence.

The evidence ledger cites the pinned implementation sources and records the scope of each verification step.
