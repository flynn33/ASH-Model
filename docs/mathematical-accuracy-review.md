# Mathematical Accuracy Review

## Established

- `F_2^9` has 512 states and Q9 has degree nine.
- The integrity relation defines an eight-dimensional subspace.
- The canonical code is a doubly-even rank-four `[9,4,4]` code.
- Its weight distribution is `{0:1,4:14,8:1}`.
- It is self-orthogonal but not self-dual in length nine.
- Puncturing coordinate 8 yields a self-dual `[8,4,4]` code.
- Radius-one nearest-codeword recovery is guaranteed and exhaustive.
- The orbit average is an idempotent projection.
- The N=8 Garden matrices satisfy the algebra exactly.
- Lazy symmetric bit-flip noise converges to uniform occupancy.
- The uniform Hamming marginal is `Binomial(9,1/2)`.

## Not established by this repository

- empirical cosmological truth;
- a physical derivation of nine dimensions;
- Born-rule or other quantum outcome statistics from branch priors;
- unique Gaussian causation by ASH transforms;
- image-quality superiority over non-ASH methods.

Detailed proofs are in `docs/mathematical-proof.md` and exact finite checks are in `proofs/computational-certificate.json`.
