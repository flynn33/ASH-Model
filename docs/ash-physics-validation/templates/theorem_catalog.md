# ASH Theorem Catalog

## Format

Each theorem entry must use this structure:

```text
ID:
Title:
Status: proposed | proved | computationally verified | falsified | obsolete
Statement:
Definitions used:
Assumptions:
Proof location:
Executable verification:
Artifacts:
Limitations:
Review notes:
```

## Initial required entries

### FIN-001: finite state space

Status: computationally verified

Statement: ASH local finite states are represented in `F_2^9` with 512 possible bit strings before admissibility restrictions.

### FIN-002: canonical code parameters

Status: computationally verified

Statement: The canonical ASH code has length 9, rank 4, size 16, minimum distance 4, and doubly-even codeword weights.

### FIN-003: single-bit correction

Status: implemented where decoder is invoked

Statement: For codewords in the canonical code, all single-bit corruptions decode uniquely to the source codeword.

### PHY-001: physical-state interpretation

Status: proposed

Statement: Pending. Must define what an ASH state represents physically.

### PHY-002: microscopic dynamics

Status: proposed

Statement: Pending. Must define deterministic, stochastic, reversible, or quantum evolution.

### PHY-003: bridge map

Status: proposed

Statement: Pending. Must map ASH configurations to physical observables.
