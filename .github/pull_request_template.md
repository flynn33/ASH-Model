## Summary

- Describe the change and why it is needed.
- Link to the related issue (required): Closes #

## Change Classification

- **Change Class**: <!-- feature | bugfix | refactor | docs | governance | release | metadata | breaking-change -->
- **Release Impact**: <!-- none | patch | minor | major -->
- **Breaking Change**: <!-- yes | no -->

## Type of change

- [ ] Bug fix
- [ ] Feature
- [ ] Documentation update
- [ ] Refactor/maintenance

## Skir claim-alignment checklist

- [ ] Branch is ahead of `main`.
- [ ] `git diff --stat main...Skir` is non-empty when this PR targets Skir work.
- [ ] `src/ash_code.py` exists when canonical code behavior changes.
- [ ] Tests prove rank 4, span size 16, doubly-even closure, and minimum distance 4 when the canonical code changes.
- [ ] Coordinate 9 is active and parity-valid when the canonical code changes.
- [ ] Decoder behavior is tested when correction claims are changed.
- [ ] Positive self-dual claims are absent.
- [ ] Unsupported Hamming-bound simulation claims are absent.
- [ ] Unsupported code-specific occupancy claims are absent.
- [ ] Narrative interpretation language was not added to ASH base docs.
- [ ] Simulation controls were updated when simulation claims changed.
- [ ] Claim audit passes.

## Contribution requirements checklist

- [ ] I opened or linked an issue for this change before implementation.
- [ ] I kept the change scoped and documented any follow-up work.
- [ ] I updated documentation (`README.md`, `CONTRIBUTING.md`, docs, or comments) where needed.
- [ ] I ran the repository checks locally and they pass.
- [ ] I confirmed the change does not break existing scripts or data files.

## Validation

List the exact commands you ran and their outputs/results.

```bash
python -m compileall .
python -m pytest -q
python tools/audit_claims.py
python tools/run_simulation_controls.py --quick
python tools/audit_simulation_data.py
```

## Notes for reviewers

- Any assumptions, trade-offs, or risks to pay attention to.
