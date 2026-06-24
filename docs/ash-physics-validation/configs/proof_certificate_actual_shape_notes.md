# Proof Certificate Schema Alignment Notes

The live proof certificate emitted by the finite proof suite uses the repository's current certificate shape. The schema must validate that actual shape, or the proof suite must emit a second standards-shaped certificate.

Do not leave a schema that validates a different object than the one produced by the proof suite.

Minimum fields expected in the current certificate family:

```text
certificate_schema or schema_version
project_version or model_version
all_checks_pass
checks
code
projection/adinkra/branching/markov sections as applicable
source_sha256 or artifact/source hashes
```

The final repository gate must validate the live certificate, not only reference files.
