# ASH Model Full Repository Audit

## Scope

This audit examines the uploaded `ASH-Model-main.zip` as the authoritative repository snapshot. It covers:

- 18 Markdown documents
- the LaTeX manuscript and compiled five-page PDF
- five JSON configuration/specification files
- seven Python source files
- eleven GitHub workflow files
- the 1,000-row simulation CSV
- four bundled figures
- both bibliography files

macOS `__MACOSX` metadata and AppleDouble resource-fork files were excluded as non-content metadata.

## Repository-defined mathematical surface

The repository explicitly defines or states:

1. A binary state space `F_2^9` with 512 states.
2. Hamming-weight planes 0 through 9.
3. State translation by XOR: `x -> x XOR c`.
4. Six sample doubly-even 9-bit transform masks.
5. The averaging operator

   `T f(x) = (1 / |C|) sum_{c in C} f(x XOR c)`.

6. The generic nearest-codeword error-correction bound `2t < d`.
7. A conditional finite Markov-chain stationary-distribution theorem.
8. A ternary branch-string routine `b -> {b, b+, b-}`.
9. Five philosophical/formal axioms concerning relation, compressibility, persistence, erasure, and self-reference.
10. Several arithmetic observations about the number nine.

## Independently derived properties of the implemented transform masks

The six masks in `simulation.py` span a binary linear code with:

- length: 9
- rank: 4
- size: 16
- minimum distance: 4
- weight distribution: `{0: 1, 4: 14, 8: 1}`
- ninth coordinate: always zero
- self-orthogonal: yes
- self-dual in `F_2^9`: no

The first eight coordinates form the familiar doubly-even `[8,4,4]` code; the implemented nine-bit version is its zero-padded embedding. A binary self-dual code cannot have odd length, so the manuscript's unqualified description of a self-dual nine-dimensional code is not mathematically consistent with the implemented masks.

## Implementation findings

### `simulation.py`

- Initializes every agent uniformly at random in `F_2^9`.
- Applies one nonzero transform mask globally to all agents at each tick.
- Independently gives each agent a 1% chance per tick of one randomly selected bit flip.
- Records only Hamming-weight occupancy.
- Does not implement nearest-codeword decoding.
- Does not explicitly evaluate the averaging operator.
- Does not implement Adinkra matrices, Garden algebra, or per-vertex embedded graphs.

Because the initial states are uniformly random, their Hamming weights already follow `Binomial(9, 1/2)`. XOR translations are permutations of `F_2^9`, and symmetric bit-flip noise preserves the uniform distribution in expectation. Therefore, the resulting bell-shaped occupancy is not evidence of convergence caused by the ASH transform masks.

### `src/simulate.py`

- Initializes 1,000 random 9-bit states.
- Applies the same weight-four mask exactly 1,000 times.
- Since XOR is self-inverse and 1,000 is even, the net transform is the identity.
- The output CSV therefore contains the initial random sample, not a transformed terminal state attributable to ASH dynamics.
- Its branch strings are expanded independently and never modify the agents, their coordinates, or the CSV.

### Branching

The implemented rule is:

`b -> b, b+, b-`

After `n` expansions, it produces `3^n` strings. The implementation does not:

- assign branch strings to Enneahcube vertices;
- alter ASH state by branch;
- produce geometric segments;
- calculate branch weights;
- perform leaf scoring, pruning, or recovery;
- save branch topology to an artifact.

### Error correction

The generic distance theorem in the paper is valid. The implemented code span has minimum distance four and is therefore capable of unique single-bit correction if a nearest-codeword decoder is implemented. No such decoder exists in this repository snapshot, and the simulations do not perform correction.

### Averaging operator

The operator definition and its idempotence proof are mathematically valid for a linear code. Randomly moving states by one mask per tick is not the same operation as explicitly computing `T f(x)`. A Monte Carlo approximation would require evaluating and averaging `f(x XOR c)` over sampled codewords; that is not implemented.

## Dataset findings

The supplied CSV has:

- shape: 1,000 x 9
- binary values only
- 444 unique states in the uploaded snapshot
- mean Hamming weight: 4.492
- standard deviation: approximately 1.470
- total-variation distance from `Binomial(9, 1/2)`: approximately 0.0293

These values are consistent with an ordinary random sample from nine independent fair bits. The repository's own parity audit confirms that the data script's net transform is identity.

## Figure findings

1. `figures/simulation-histogram.png` is a spreadsheet example containing student names and scores. It is not an ASH simulation histogram.
2. `figures/single-bit-error.png` depicts an eight-bit message, not a nine-bit ASH state.
3. `figures/hypercube-3d-projection.png` has no repository generator or documented mapping to the 512-state Enneahcube.
4. `figures/adinkra-graph-colored.png` has no repository generator or formal link to the state-transition code.
5. The PDF embeds these figures, so the paper's visual evidence does not independently validate the simulations.

## Material not present in the uploaded snapshot

An exhaustive search of every text-bearing file found no occurrence of:

- `Enneahcube` or `Enneacube`;
- the historical `2.25` state-to-plane mapping equation;
- a formal leaf-to-state mapping;
- `F -> FF[+F]F[-F]`;
- Garden-algebra matrices or equations;
- a definition of the nine application dimensions;
- a mapping from image/video measurements into ASH coordinates;
- a mapping from ASH leaves into reconstruction operators.

The archive therefore does not contain a complete executable ASH mapping for an upscaler, even though it contains the core hypercube, code, projection, and branching concepts.

## Internal documentation conflicts

- The paper claims a doubly-even self-dual code in nine dimensions; the implementation is not self-dual in nine dimensions.
- The paper claims correction under noise; no decoder is implemented.
- The paper claims convergence independent of initial conditions; the provided simulations do not test multiple controlled initial distributions.
- The paper claims total-variation distance below 0.05 under noise; no tracked script calculates that statistic.
- The paper claims branch-weight distributions and geometric fractal trees; the branch routine only counts strings.
- Validation reports treat the random Hamming-weight baseline as evidence of ASH convergence.
- Validation reports describe all claims as verified despite the above missing implementations.

## Implications for the Mirmir upscaler

The repository supplies useful deterministic building blocks:

- a compact 9-bit state;
- Enneahcube adjacency through bit flips;
- a rank-four stabilizer subgroup;
- Hamming distance and code orbits;
- an idempotent code-invariant projection;
- bounded deterministic branch generation.

Before these can safely become the upscaler foundation, a canonical computational specification must add:

1. exact bit ordering and authoritative code definition;
2. definitions for all nine image/video dimensions;
3. deterministic continuous-to-binary threshold rules;
4. branch grammar and branch-to-operator semantics;
5. decoder and recovery semantics;
6. source-consistency scoring and leaf pruning;
7. temporal-state transition rules;
8. exhaustive 512-state reference tests;
9. controlled ablations against non-ASH deterministic baselines.

## Audit conclusion

The uploaded repository contains a meaningful deterministic mathematical scaffold, but the current implementation and documentation do not yet constitute a complete, validated ASH mapping engine. The correct next step is to consolidate the verified algebra and explicitly restore or author the missing mapping and branch semantics before designing the Metal upscaler around them.
