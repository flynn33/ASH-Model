# ASH-Physics Implementation Instructions

## Objective

Use this package to keep the ASH-Physics layer self-contained, internally consistent, and explicit about its research boundary. The finite ASH kernel remains the verified foundation. Physical interpretation, dynamics, bridge maps, observable pipelines, empirical validation, and locked predictions remain future work until their own gates pass.

## Closed Implementation Loop

Repeat this loop until every applicable gate passes or a blocker is recorded with exact evidence:

1. Read the package instructions and task files.
2. Audit the current repository state.
3. Select one missing or weak item.
4. Implement or repair that item.
5. Add the matching test, proof, schema check, or evidence.
6. Run the narrow verification command for the item.
7. Run the full acceptance gate after narrow checks pass.
8. Update manifests, validation status, and documentation.
9. Record any blocked work without marking it complete.
10. Repeat until the audit has no remaining local remediation item.

## Canonical Task Path

The repository uses the neutral canonical task manifest path:

```text
docs/ash-physics-validation/tasks/task_manifest.json
```

Earlier package material used a package-specific task-manifest filename. That name is not a repository path. All repository instructions, manifests, CI commands, and validation gates must use `tasks/task_manifest.json`.

## Task Status Semantics

Use these status values in repository validation files:

| Status | Meaning |
|---|---|
| `complete` | The stated repository task is implemented and has evidence. |
| `blocked` | The task cannot advance until a named scientific, mathematical, data, or implementation dependency exists. |
| `deferred` | The task is intentionally postponed after recording the dependency and evidence. |

Use these completion types:

| Completion type | Meaning |
|---|---|
| `scaffold_created` | A planning or placeholder surface exists, but it is not a completed scientific result. |
| `theorem_proved` | A theorem has a proof and the proof is recorded. |
| `implementation_verified` | Executable implementation exists and verification passed. |
| `empirical_gate_passed` | A preregistered empirical gate has passed with recorded evidence. |
| `blocked_scientific_work` | The item remains blocked by missing theory, solver, data, or preregistration work. |

Scaffold creation must not be described as completed physics, completed cosmology, completed observation, or completed empirical validation.

## Blocked-Work Policy

Record unresolved scientific obligations in `validation/status.json` under `open_blockers`. At minimum, blockers must cover:

- physical state interpretation;
- microscopic or stochastic dynamics;
- bridge maps to observables;
- empirical validation blocked until theory, solver, and preregistration gates exist.

If a task has only a skeleton file, record `completion_type: scaffold_created` and state the scientific boundary in `notes`.

## Schema Validation

The repository gate must validate instances against schemas, not only JSON syntax:

```text
predictions/prediction-ledger.json
validation/status.json
docs/ash-physics-validation/tasks/task_manifest.json
```

The gate entrypoint is:

```bash
python docs/ash-physics-validation/scripts/run_repository_gate.py .
```

## Artifact Regeneration

After source, schema, validation, or proof changes, run:

```bash
python tools/generate_artifacts.py
python tools/run_proof_suite.py
python tools/verify_repository.py
```

Regenerated manifests must be committed when they are affected by repository source changes.

## Attribution Policy

Repository-facing files must not add external tool-authorship notices, vendor/model signatures, transcript references, prompt references, or contribution-credit statements for tooling. The existing contributor-attribution guard is a required repository policy gate and must remain present.

Run the strict scanner before completion:

```bash
python docs/ash-physics-validation/scripts/check_sensitive_language.py .
```

## Scientific Boundary

The current repository verifies finite algebra and deterministic reference computation. It does not establish empirical cosmology, physical supersymmetry, quantum-measurement derivations, or observational confirmation. Any future claim must be backed by a theorem, implementation gate, preregistration, synthetic recovery, baseline comparison, convergence evidence, and locked prediction where applicable.

## Acceptance Commands

Run these commands from the repository root:

```bash
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
python docs/ash-physics-validation/scripts/check_sensitive_language.py .
python docs/ash-physics-validation/scripts/run_repository_gate.py .
python -m compileall -q simulation.py src tools scripts docs/ash-physics-validation/scripts
```

Then verify that tracked generated and validation surfaces have no unintended diff.
