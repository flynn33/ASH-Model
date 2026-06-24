# Examples and Tutorials

## Tutorial 1: Verify the repository

```bash
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/build_manuscript.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
```

## Tutorial 2: Map an array patch

```python
import numpy as np
from ash_model.pipeline import map_patch

current = np.linspace(0.0, 1.0, 64).reshape(8, 8)
result = map_patch(current, branch_depth=4, scale=2, top_k=4)

print(result.source_state)
print([candidate.message for candidate in result.selected])
```

## Tutorial 3: Inspect finite physics observables

```python
from ash_model.physics import bridge_observables

state = (0, 0, 0, 0, 0, 0, 0, 0, 0)
print(bridge_observables(state))
```

The values are dimensionless internal observables. They are not unit-bearing physical measurements.

## Tutorial 4: Check science blockers

```bash
python tools/audit_physics_readiness.py . --expect-open
```

The expected current result is not ready, with open science blockers.
