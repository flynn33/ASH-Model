# ASH Leaf-Branching Research v0.1

Research note and reproducible finite checks for extending the finite ASH local alphabet into infinite history and configuration models.

## Contents

- [Research note](ASH-Leaf-Branching-Research-v0.1.md): definitions, constructions, proofs, limitations, and next research gates.
- [Evidence record](research_evidence.json): source inventory, claim mapping, search record, and unresolved questions.
- [Verification harness](verify_branch_models.py): standalone standard-library tests of the stated candidate models.
- [Finite results](finite_checks.json) and [test output](test_output.txt): recorded execution results.

## Reproduce the finite checks

From the repository root:

```sh
python docs/ash-cosmology/leaf-branching/v0.1/verify_branch_models.py
```

The script writes `finite_checks.json` alongside itself and exits unsuccessfully if a test fails. The recorded run passed all 10 tests. The harness tests the mathematical candidates in this note; it does not import or validate the application implementation or replace the repository test suite.

## Research status

The infinite conclusions rely on the arguments and theorem hypotheses in the note, not on finite enumeration. The constructions establish mathematical compatibility with the finite local code, not empirical cosmological validation, a Born-rule derivation, or spacetime emergence. Project-source identifiers in the evidence record refer to supplied research documents; the candidate generators needed to reproduce the tests are included here.
