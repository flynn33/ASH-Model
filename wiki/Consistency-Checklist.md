# Consistency Checklist

Run from the repository root before publishing repository docs or wiki pages:

```bash
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/build_manuscript.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
python docs/ash-physics-validation/scripts/check_claim_language.py .
python docs/ash-physics-validation/scripts/check_sensitive_language.py .
python docs/ash-physics-validation/scripts/run_repository_gate.py .
python tools/validate_json_assets.py .
python tools/check_generated_outputs.py . --include-manuscript
python tools/audit_live_repository_readiness.py .
python -m compileall -q simulation.py src tools scripts docs/ash-physics-validation/scripts
python -m json.tool config/ash_mapping_v1.json > /dev/null
python -m json.tool axioms-of-existence.json > /dev/null
git diff --check
```

Review that:

- no nine-dimensional self-dual claim appears;
- correction claims name the decoder and radius;
- Gaussian/binomial figures are described as controlled baselines;
- generated data and figure hashes are current;
- manuscript and canonical specification agree with code;
- physical cosmology, external validation, and locked predictions remain marked open unless their gates pass;
- the tracked `wiki/` pages and live GitHub wiki have the same current page set.
