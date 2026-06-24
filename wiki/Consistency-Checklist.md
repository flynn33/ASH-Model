# Consistency Checklist

Before release:

```bash
python -m pip install -e ".[dev]"
pytest
python tools/generate_artifacts.py
python tools/run_proof_suite.py
python tools/verify_repository.py
python -m compileall -q simulation.py src tools scripts
python -m json.tool config/ash_mapping_v1.json > /dev/null
python -m json.tool axioms-of-existence.json > /dev/null
```

Review that:

- no nine-dimensional self-dual claim appears;
- correction claims name the decoder and radius;
- Gaussian/binomial figures are described as controlled baselines;
- generated artifact hashes are current;
- manuscript and canonical specification agree with code.
