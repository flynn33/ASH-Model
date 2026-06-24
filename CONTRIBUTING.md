# Contributing to the ASH Model

ASH combines finite mathematics, generated evidence, and executable reference code. Contributions must keep those layers aligned and must not promote an interpretive hypothesis to a proved result.

## Workflow

1. Open or link an issue describing the change and its intended evidence.
2. Work on a focused branch.
3. Update the canonical specification when behavior or serialization changes.
4. Add tests for every new mathematical or computational claim.
5. Regenerate tracked evidence and inspect the resulting diff.
6. Record limitations and matched controls.

## Required checks

```bash
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/run_proof_suite.py
pytest
python tools/verify_repository.py
python docs/ash-physics-validation/scripts/check_claim_language.py .
python -m json.tool docs/ash-physics-validation/tasks/task_manifest.json > /dev/null
python -m json.tool docs/ash-physics-validation/configs/prediction_ledger.schema.json > /dev/null
python -m json.tool docs/ash-physics-validation/configs/preregistration.schema.json > /dev/null
python -m json.tool docs/ash-physics-validation/configs/proof_certificate.schema.json > /dev/null
python -m json.tool predictions/prediction-ledger.json > /dev/null
python -m json.tool validation/status.json > /dev/null
python -m compileall -q simulation.py src tools scripts
python -m json.tool config/ash_mapping_v1.json > /dev/null
python -m json.tool axioms-of-existence.json > /dev/null
python scripts/github/discussion_agent.py --validate-config --root .
python scripts/github/discussion_topic_agent.py --validate-config --root .
python scripts/github/discussion_moderation_agent.py --validate-config --root .
```

When `latex/main.tex` changes, run `python tools/build_manuscript.py` before `tools/run_proof_suite.py`. The repository verifier rejects a PDF whose recorded source hash, binary hash, or project version is stale.

## Mathematical changes

A change to the generator matrix, bit ordering, decoder policy, branch rule, or operator mapping is a specification change. The pull request must include:

- a precise definition;
- a proof or explicit finite certificate;
- migration impact on tracked artifacts;
- exhaustive tests where the state space is finite;
- a version update.

No length-nine self-duality statement is permitted for the canonical rank-four code. Correction claims must name the decoder and radius.

## Statistical and reconstruction changes

New performance claims require matched controls. At minimum, preserve the no-transform and random-transform ablations, report seeds and configuration, and distinguish finite-sample variation from causal attribution.

## Pull request contents

- concise summary and linked issue;
- change class and release impact;
- exact commands run;
- proof/test results;
- generated artifact changes;
- assumptions, limitations, and follow-up work.

## Style

- Python 3.10+ with type hints for public functions;
- small composable functions and explicit validation;
- deterministic seeds for tracked simulations;
- no silent error recovery;
- equations and code must use the same coordinate order;
- generated files must identify their generator in documentation.

All contributors must follow `CODE_OF_CONDUCT.md` and the repository license.
