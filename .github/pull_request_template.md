## Summary

Closes #

## Classification

- **Change Class:** feature | bugfix | refactor | docs | governance | release | metadata | breaking-change
- **Release Impact:** none | patch | minor | major
- **Breaking Change:** yes | no

## Mathematical/computational effect

Describe any change to bit ordering, code parameters, decoder policy, feature mapping, branching, operators, scores, or artifacts.

## Evidence

- [ ] Tests added or updated
- [ ] `pytest` passes
- [ ] Artifacts regenerated
- [ ] Proof suite passes
- [ ] Repository verifier passes
- [ ] Matched controls added for statistical or quality claims
- [ ] Documentation and manuscript aligned

## Commands and results

```bash
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/run_proof_suite.py
pytest
python tools/verify_repository.py
```

## Assumptions and limitations

State what the change does not establish.
