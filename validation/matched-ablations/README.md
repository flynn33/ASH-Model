# Matched Ablation Validation

Status: Blocked

## Purpose

Matched ablations will separate ASH-specific assumptions from generic model flexibility, finite sampling, and reconstruction choices.

## Required inputs

- Frozen ASH observable pipeline.
- Same-complexity baseline alternatives.
- Code, branch, prior, and bridge-map ablations with matched parameter counts where practical.

## Acceptance gates

- Each ablation uses the same data cuts and likelihood as the ASH model.
- Parameter-count differences are documented.
- ASH-specific claims are weakened or removed when matched ablations perform equivalently.

## Current blocker

The observable pipeline and likelihood are not yet defined.
