# Repository Structure

This page maps major folders/files to their purpose.

## Top-level

- `README.md` - overview, quick start, and contribution checks
- `CONTRIBUTING.md` - contribution workflow and expectations
- `CODE_OF_CONDUCT.md` - discussion and collaboration standards
- `LICENSE` - custom restrictive license
- `axioms-of-existence.json` - formal modal-logic axiom set
- `simulation.py` - visualization-focused noisy-mixing demo

## Research docs

- `docs/ASH-research-paper.md` - markdown-formatted paper narrative
- `docs/ASH-Model-Preprint-v1.pdf` - compiled preprint PDF
- `docs/canonical-code.md` - Skir canonical code specification
- `docs/skir-code-validation.md` - Skir code-theoretic validation
- `docs/falsification-and-controls.md` - Skir controls and falsification boundaries
- `docs/claim-language-policy.md` - supported and unsupported claim language
- `docs/python-smoke-validation.md` - current Skir validation scope
- `docs/repository-review.md` - consistency review and follow-up notes
- `docs/consistency-validation-report.md` - scoped validation audit results
- `docs/data-accuracy-audit.md` - simulation data verification
- `docs/mathematical-accuracy-review.md` - mathematical correctness audit
- `docs/python-code-validation.md` - historical Python validation note
- `latex/main.tex` - canonical manuscript source
- `latex/references.bib` - active bibliography
- `latex/bibtex.bib` - legacy bibliography file

## Code and data

- `src/ash_code.py` - canonical Skir code layer and decoder
- `src/simulate.py` - data-focused simulation script
- `src/derive-9-properties.py` - symbolic/mathematical derivations
- `tests/test_ash_code.py` - code and decoder tests
- `data/simulation-results.csv` - sample/generated simulation output
- `data/simulation-controls.json` - generated Skir control output
- `figures/` - model and simulation images
- `tools/audit_simulation_data.py` - data integrity validation tool
- `tools/audit_claims.py` - documentation claim audit
- `tools/run_simulation_controls.py` - reproducible control runs
- `tools/verify_branch.py` - Skir branch completeness guard

## CI and automation

- `.github/workflows/ci.yml` - repository checks
- `.github/workflows/skir-validation.yml` - Skir validation checks
- `.github/workflows/discussion-agents.yml` - repo-grounded discussion response automation
- `.github/workflows/discussion-topic-seeder.yml` - scheduled topic creation from wiki and paper headings
- `.github/workflows/discussion-moderation.yml` - discussion moderation and incident logging
- `.github/discussion_agents.json` - discussion responder family routing
- `.github/discussion_topic_generator.json` - topic seeding sources and family rules
- `.github/discussion_moderation_policy.json` - moderation policy and enforcement thresholds
- `.github/pull_request_template.md` - PR template for contributors
