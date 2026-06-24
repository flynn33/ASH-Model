# Falsification, Controls, and Ablation Plan

## Purpose

This document prevents a recurrence of the original validation error: treating a generic hypercube baseline as evidence specific to ASH. Every statistical or reconstruction claim must be compared with controls that preserve relevant confounders.

## Markov controls

The tracked ablation suite uses seeded runs with these cases:

| Case | Initial state | Transform | Noise | Question isolated |
|---|---|---|---|---|
| 0 | uniform | none | none | finite-sample binomial baseline |
| 1 | uniform | ASH code | yes | does ASH visibly change an already uniform ensemble? |
| 2 | uniform | none | yes | noise-only baseline |
| 3 | all zero | ASH code | none | code-orbit confinement and code weight distribution |
| 4 | all zero | ASH code | yes | code plus generic hypercube mixing |
| 5 | all zero | none | yes | noise-driven mixing without ASH |
| 6 | all zero | random weight-four masks | yes | non-ASH transform baseline with matched mask weight |

The output is `data/ablation-results.csv`. The figure `figures/simulation-histogram.png` plots selected cases against the exact binomial distribution.

## Interpretation rules

A result is not ASH-specific when a no-transform or matched-random control produces the same statistic within sampling uncertainty. In particular:

- a uniform random start already has a binomial Hamming marginal;
- symmetric bit-flip noise has a uniform stationary state;
- permutations, including XOR translations, preserve uniformity;
- ASH transforms without noise remain in a 16-state code orbit and do not converge to all 512 states.

## Error-correction controls

Correction claims are accepted only for an explicit decoder invocation. The required matrix is:

| Input class | Required behavior |
|---|---|
| valid codeword | exact decode |
| every one-bit corruption | recover original codeword |
| every two-bit corruption | reject; never silently heal |
| general state with known affine anchor | same radius-one policy after removing anchor |
| unknown anchor | no recovery claim |

The proof suite exhaustively evaluates these classes.

## Projection controls

Randomly translating states is not evidence that the orbit-averaging projection was evaluated. A projection claim requires:

1. explicit summation over all 16 codewords, or a declared Monte Carlo estimator;
2. an idempotence test;
3. a code-invariance test;
4. a constant-preservation test.

These checks are implemented in `ash_model.projection`.

## Reconstruction controls

A future upscaler evaluation should compare at minimum:

- nearest-neighbor baseline;
- bilinear or bicubic baseline;
- the same 16 reference operators without ASH branch priors;
- ASH branch prior plus source-consistency scoring;
- random message priors with identical operator/scoring code;
- temporal hysteresis enabled and disabled.

Metrics should include source re-projection error, edge error, temporal flicker, runtime, and external perceptual/quality measures appropriate to the dataset. A quality gain is attributable to ASH only when it survives these matched ablations.

## Falsifiable software claims

The following failures would falsify the current computational specification:

- a generated codeword not having weight divisible by four;
- code rank other than four or minimum distance other than four;
- coordinate 9 violating parity for a codeword;
- a one-bit corruption not being recovered;
- a two-bit corruption being silently accepted;
- `T(T(f))` differing from `T(f)`;
- a Garden identity having nonzero integer residual;
- a mapped patch state failing coordinate-9 integrity;
- branch leaf weights not summing to one;
- nondeterministic pruning under identical inputs and configuration.

All are covered by automated tests.

## Physical claims

Physical or cosmological interpretations require their own observational predictions, uncertainty model, and comparison with established alternatives. The finite code and simulation results do not by themselves establish those interpretations. Any future physical claim should be placed in a separate hypothesis document with explicit disconfirmation criteria.
