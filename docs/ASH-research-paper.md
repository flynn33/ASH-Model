# Procedural Cosmology in 9 Dimensions: The Adinkra-Stabilized Hypercube Model (ASH Model)

**Author:** James Daley (Independent Researcher, Author, Full Stack Developer)  
**Date:** December 23, 2025

## Abstract

The Adinkra-Stabilized Hypercube Model (ASH Model) is an exploratory procedural-cosmology and simulation-theory framework over the 9-bit raw state space `F2^9`. The Skir formulation defines the canonical ASH code layer as a parity-explicit rank-4 doubly-even linear `[9,4,4]` code. Coordinate 9 is the parity/integrity coordinate for canonical codewords.

The simulation scripts visualize codeword transforms and noisy hypercube mixing across Hamming-weight planes. Error-correction claims are limited to the explicit nearest-codeword decoder and its tests. The controls added in Skir compare canonical codeword transforms with no-codeword and random-codeword baselines, supporting conservative language about noisy mixing toward a binomial/Haar occupancy envelope.

The recurrence of nine dimensions is mathematically motivated by connections to string theory anomaly cancellation, optimal lattice packing (E8 and Leech lattices), and coding theory. A modal-logic foundation is provided by five axioms of existence formalised in Kripke-frame semantics (detailed in `axioms-of-existence.json`).

While classical and discrete, ASH offers a computationally tractable platform for exploring links among supersymmetry-inspired graph structures, coding theory, high-dimensional geometry, and procedural generation.

**Keywords:** Supersymmetry, Adinkras, String Theory, Many-Worlds Interpretation, L-Systems, Procedural Generation, 9 Dimensions, Error-Correcting Codes, Modal Logic

## 1. Introduction

The search for unified descriptions of physical reality has repeatedly revealed deep links between mathematical structures, computational models, and fundamental principles. ASH proposes a procedural cosmology scaffold that uses supersymmetric algebra, coding theory, and 9-dimensional combinatorics.

The raw state space is the 9-dimensional hypercube `F2^9` whose 512 vertices encode binary states. Skir distinguishes that raw state space from the canonical ASH code `C`, a 16-word decoder target set with coordinate 9 serving as a parity/integrity coordinate.

Simulations in this repository are visualization and control demos. They apply canonical codeword transforms and low-probability bit-flip noise, then report Hamming-weight occupancy. They do not by themselves establish runtime correction; correction is supplied by the decoder in `src/ash_code.py`.

![3D Projection of the Hypercube](figures/hypercube-3d-projection.png)  
*Figure 1: Visualisation of a lower-dimensional projection of the 9D hypercube underlying the ASH Model.*

## 2. Related Work

### Supersymmetry and Adinkras

Adinkras encode one-dimensional supersymmetric theories graphically, with edge colourings corresponding to supersymmetry generators (Faux & Gates, 2005; Doran et al., 2008).

### Error-Correcting Codes in Physics

Links between SUSY representations and classical codes have illuminated holographic principles (Almheiri et al., 2015).

### High-Dimensional Geometry and String Theory

Nine spatial dimensions appear recurrently in compactifications and anomaly cancellation mechanisms (Green & Schwarz, 1984; Polchinski, 1998). Optimal lattices in dimensions related to 9 exhibit unique properties (Cohn & Kumar, 2009; Cohn et al., 2019).

![Coloured Adinkra Graph](figures/adinkra-graph-colored.png)  
*Figure 2: Example adinkra graph with coloured edges, used here as code-theoretic inspiration.*

## 3. Mathematical Framework

The hypercube `H_9 = ({0,1}^9, E)` is stratified by Hamming weight into planes 0 through 9.

The Skir canonical code `C` is generated over GF(2) by:

```text
g1 = 1 1 1 1 0 0 0 0 0
g2 = 1 1 0 0 1 1 0 0 0
g3 = 1 0 1 0 1 0 1 0 0
g4 = 1 0 0 1 1 0 0 0 1
g5 = 1 1 1 1 1 1 1 0 1
g6 = 0 0 0 0 1 1 1 0 1
```

The computed span has rank 4, 16 codewords, minimum distance 4, and weight distribution `{0: 1, 4: 14, 8: 1}`. For each canonical codeword `c`:

```text
c9 = c1 XOR c2 XOR c3 XOR c4 XOR c5 XOR c6 XOR c7 XOR c8
```

Coordinate 9 is active in the canonical code. The first eight coordinates form a restricted admissible pre-parity layer, not an unrestricted payload.

Transformations are translations by codewords: `x -> x XOR c` for `c` in `C`. The averaging operator

```text
T f(x) = (1 / |C|) sum_{c in C} f(x XOR c)
```

projects onto `C`-invariant functions.

![Single Bit-Flip Error](figures/single-bit-error.png)  
*Figure 3: Single bit-flip error in transmission, correctable when the explicit decoder is invoked.*

## 4. Simulation Methodology

Agent dynamics are implemented in `simulation.py` and `src/simulate.py`. Agents undergo XOR with canonical codeword masks and optional low-probability bit-flip noise. Occupancy is tracked across Hamming-weight planes.

`tools/run_simulation_controls.py` compares:

1. canonical ASH codewords + noise,
2. no codewords + noise,
3. random codewords + noise,
4. all-zero start + ASH codewords + no noise,
5. all-zero start + ASH codewords + noise.

## 5. Results

The code-theoretic layer is verified by `tests/test_ash_code.py`. The decoder corrects unique single-bit errors around canonical codewords and refuses silent correction of double-bit errors under the default radius.

The simulation controls support conservative noisy-mixing language. They do not establish that ASH codewords uniquely cause occupancy distributions, nor do they establish empirical physical validation.

![Simulation Occupancy Distribution](figures/simulation-histogram.png)  
*Figure 4: Example Hamming-weight occupancy distribution from simulation runs.*

## 6. Discussion

### Logical Foundations: Axioms of Existence

Five axioms (formalised in `axioms-of-existence.json`) provide a Kripke-frame semantic basis:

1. **Relational Existence (A1)** - Existence requires participation in at least one relation.
2. **Structural Compressibility (A2)** - Real patterns exhibit low Kolmogorov complexity.
3. **Multi-Scale Persistence (A3)** - Robust entities survive coarse-graining across scales.
4. **Energetic Cost of Erasure (A4)** - Structured information incurs non-zero erasure cost (Landauer).
5. **Self-Reference for Consciousness (A5)** - Conscious systems contain updating self-models.

These axioms are philosophical and formal scaffolding. They are not empirical validation of ASH as a physical cosmology.

## Limitations

ASH is currently an exploratory, classical, discrete framework. Skir validates code-theoretic properties of the canonical ASH code and adds controls for simulation behavior. It does not establish an empirically verified physical cosmology, and it does not show that ASH codewords uniquely cause Gaussian occupancy distributions.

Future directions include quantum extensions, richer SUSY multiplets, tensor-network interpretations, comparative 8D/10D studies, and a formal proof appendix for code properties and Markov-chain behavior.

## 7. Conclusion

The Skir formulation makes ASH's canonical code layer explicit and testable: a rank-4 doubly-even linear `[9,4,4]` code over `F2^9`, with coordinate 9 serving as parity/integrity. The repository now separates code-theoretic decoder claims from simulation demos and documents the remaining limits of the framework.

## References

- Almheiri, A., Dong, X., & Harlow, D. (2015). Bulk locality and quantum error correction in AdS/CFT. *Journal of High Energy Physics*, 2015(4), 163.
- Cohn, H., & Kumar, A. (2009). Optimality and uniqueness of the Leech lattice among lattices. *Annals of Mathematics*, 170(3), 1003-1050.
- Cohn, H., Jiao, W.-H., Kumar, A., Miller, S. D., & Viazovska, M. (2019). Universal optimality of the E8 and Leech lattices. arXiv:1902.05438.
- Doran, C. F., Gates Jr, S. J., Hubsch, T., Iga, K. M., & Landweber, G. D. (2008). On graph-theoretic identifications of Adinkras, supersymmetry representations and codes. *International Journal of Modern Physics A*, 22(5).
- Faux, M., & Gates, S. J. (2005). Adinkras: A graphical technology for supersymmetric representation theory. *Physical Review D*, 71(6), 065002.
- Green, M. B., & Schwarz, J. H. (1984). Anomaly cancellations in supersymmetric D=10 gauge theory and superstring theory. *Physics Letters B*, 149(1-3), 117-122.
- Polchinski, J. (1998). *String Theory, Vol. II*. Cambridge University Press.

## Appendix: Selected Proofs

See `latex/main.tex` Appendix for formal proofs of:

- Idempotence of the averaging operator `T`
- Error correction bound (`2t < d`)
- Existence and uniqueness of stationary distribution in finite Markov chains

**Projection Idempotence** - `T^2 = T` follows from coset averaging.

**Error Correction Bound** - A linear code with minimum distance `d` corrects `t < d/2` errors via nearest-neighbour decoding when the decoder is invoked.

This Markdown file (`ASH-research-paper.md`) is current as of December 23, 2025. For the publication-ready PDF with full LaTeX typesetting, compile `latex/main.tex`.
