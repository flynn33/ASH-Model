# Wiki Publication Map

The repository has two wiki surfaces:

- tracked source pages in `wiki/`;
- the live GitHub wiki at `https://github.com/flynn33/ASH-Model/wiki`.

The tracked source is the reviewable copy that belongs in pull requests. The live wiki is a separate Git repository and must be published from the tracked source after review or by an explicit documentation update.

## Current publication scope

The current wiki describes:

- the verified finite ASH mathematics;
- the ASH-Physics v0.2 finite-observer layer;
- deterministic data generation and figure hash binding;
- repository-readiness commands and final audit evidence;
- open science blockers for physical cosmology, external validation, and locked predictions.

## Page map

| Tracked source | Live wiki page |
|---|---|
| `wiki/Home.md` | `Home.md` |
| `wiki/Getting-Started.md` | `Getting-Started.md` |
| `wiki/Introduction-to-ASH-Model.md` | `Introduction-to-ASH-Model.md` |
| `wiki/Mathematical-Framework.md` | `Mathematical-Framework.md` |
| `wiki/Finite-Observer-Physics.md` | `Finite-Observer-Physics.md` |
| `wiki/Evidence-and-Artifacts.md` | `Evidence-and-Artifacts.md` |
| `wiki/Hypercube-and-Adinkra-Visual-Guide.md` | `Hypercube-and-Adinkra-Visual-Guide.md` |
| `wiki/Visual-Model-Atlas.md` | `Visual-Model-Atlas.md` |
| `wiki/Validation-and-Data-Audit.md` | `Validation-and-Data-Audit.md` |
| `wiki/Science-Roadmap.md` | `Science-Roadmap.md` |
| `wiki/Simulation-Guide.md` | `Simulation-Guide.md` |
| `wiki/Repository-Structure.md` | `Repository-Structure.md` |
| `wiki/Consistency-Checklist.md` | `Consistency-Checklist.md` |
| `wiki/Research-Paper-Guide.md` | `Research-Paper-Guide.md` |
| `wiki/Axioms-of-Existence.md` | `Axioms-of-Existence.md` |
| `wiki/Codebase-Overview.md` | `Codebase-Overview.md` |
| `wiki/Examples-and-Tutorials.md` | `Examples-and-Tutorials.md` |
| `wiki/Theoretical-Applications.md` | `Theoretical-Applications.md` |
| `wiki/Contributing-Guidelines.md` | `Contributing-Guidelines.md` |
| `wiki/Governance-and-Discussions.md` | `Governance-and-Discussions.md` |
| `wiki/References-and-Further-Reading.md` | `References-and-Further-Reading.md` |
| `wiki/License-and-Use.md` | `License-and-Use.md` |
| `wiki/_Sidebar.md` | `_Sidebar.md` |
| `wiki/_Footer.md` | `_Footer.md` |

## Publication checks

Run these before publishing repository docs or the live wiki:

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
git diff --check
```

## Publication rule

Do not use the wiki to claim empirical cosmology completion. The live wiki may state the finite algebra, executable reference implementation, and finite-observer ASH-Physics layer are verified. It must keep physical cosmology, unit-bearing bridge maps, external likelihoods, and locked predictions marked as open science work until their gates pass.
