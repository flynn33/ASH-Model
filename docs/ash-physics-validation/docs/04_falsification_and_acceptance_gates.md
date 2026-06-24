# Falsification and Acceptance Gates

## Claim levels

Use these labels consistently:

| Label | Meaning |
|---|---|
| `Proved finite theorem` | Exhaustively verified or mathematically proven for a finite ASH object |
| `Implemented mechanism` | Executable source exists and tests pass |
| `Derived physical consequence` | Follows from stated physical definitions and dynamics |
| `Numerical evidence` | Reproducible computation but not a theorem |
| `Empirical support` | Survives declared observational tests against baselines |
| `Speculative interpretation` | Conceptual motivation not yet derived or observed |

## Stop criteria

Stop or downgrade claims if any of the following occur:

- a finite counterexample violates a theorem statement;
- a decoder silently corrects ambiguous errors;
- a physical variable is used before being defined;
- a bridge map is adjusted after seeing validation residuals;
- a continuum limit is assumed but not derived or bounded;
- a fit succeeds only by adding unconstrained functions;
- ASH fails a held-out or prospective prediction outside declared uncertainty;
- a matched ablation performs equally well;
- results depend on undocumented tuning.

## Acceptance gates

| Gate | Acceptance requirement |
|---|---|
| finite algebra | exact tests and proof certificate pass |
| microscopic dynamics | closure, locality, existence, invariants, and stability addressed |
| bridge map | maps ASH states to physical quantities with units and parameters |
| continuum/observer limit | derived, bounded, or explicitly replaced by finite-observer theory |
| cosmological equations | background and perturbation observables computable |
| synthetic recovery | parameters recovered on ASH-generated mock data |
| ablations | ASH-specific components outperform matched controls |
| baseline limit | standard model or declared alternative reproduced in limit |
| real-data test | preregistered likelihood analysis completed |
| prospective prediction | frozen prediction succeeds on future or held-out data |
| replication | independent reproduction is possible from public artifacts |

## Required failure documentation

Every failed gate must produce:

```text
failed gate
exact command or derivation step
observed result
expected result
root cause if known
claim to downgrade
next repair task
```
