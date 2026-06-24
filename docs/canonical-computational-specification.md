# ASH Canonical Computational Specification

**Specification version:** 1.0.0  
**Reference implementation:** ASH Model 1.1.0  
**Normative configuration:** `config/ash_mapping_v1.json`

## 1. Scope

This document defines a complete executable ASH mapping layer. It fixes bit ordering, code construction, state integrity, image/video measurements, thresholding, branch semantics, recovery, reconstruction operators, scoring, pruning, temporal transitions, and generated reference artifacts.

Interpretive cosmology is outside the normative computational layer. The word *state* below means a finite binary state, not a claim about a physical ontology.

The measurement formulas, thresholds, hysteresis bands, branch priors, geometry constants, reconstruction operators, and score weights are versioned reference-design choices. They make the verified algebra executable, but they are not uniquely derived from the philosophical axioms or empirically calibrated as optimal.

## 2. Binary notation and ordering

Let

\[
V = \mathbb F_2^9.
\]

A state is written

\[
x=(x_1,x_2,\ldots,x_9),\qquad x_i\in\{0,1\}.
\]

Coordinate 1 is the leftmost displayed bit and the most-significant bit in integer serialization:

\[
\operatorname{index}(x)=\sum_{i=1}^{9}x_i2^{9-i}.
\]

Thus `000000000` has index 0 and `111111111` has index 511. Addition in `V` is coordinate-wise XOR.

The graph `Q9` has vertex set `V`; two states are adjacent exactly when their Hamming distance is one. Each vertex therefore has nine neighbors and the graph has

\[
9\cdot 2^8=2304
\]

undirected edges.  The canonical plane map is Hamming weight:

\[
P(x)=\operatorname{wt}(x)\in\{0,\ldots,9\}.
\]

The distance shell around any vertex has size

\[
|\{y:d_H(x,y)=r\}|=\binom{9}{r}.
\]

The adjacency spectrum of `Q9` is

\[
\lambda_r=9-2r,\qquad m_r=\binom{9}{r},\qquad 0\le r\le 9.
\]

The unnormalized graph-Laplacian spectrum is

\[
\Delta_r=2r,\qquad m_r=\binom{9}{r},\qquad 0\le r\le 9,
\]

so the finite graph spectral gap is `2`.

No historical decimal scaling rule is used by this specification.

## 3. Application integrity hyperplane

Image/video mapping produces states in

\[
E=\{x\in V:x_9=x_1\oplus\cdots\oplus x_8\}.
\]

Equivalently, every state in `E` has even total Hamming weight. `E` is an eight-dimensional linear subspace with 256 states. States outside `E` remain valid vertices of `Q9`, but they fail the application integrity relation and may represent corrupted or unvalidated data.

The pair-flip graph on `E` connects states that differ in exactly two
coordinates.  It has degree

\[
\binom{9}{2}=36
\]

and `4608` undirected edges.  Its adjacency spectrum is

```text
eigenvalue  multiplicity
36          1
20          9
8           36
0           84
-4          126
```

The corresponding unnormalized Laplacian spectral gap is `16`.  These are
finite graph identities, not a physical spacetime metric.

## 4. Canonical transform code

The code `C` is the row span over `F_2` of

```text
G = 111100000
    110011000
    101010100
    100110001
```

The six canonical transform masks exposed by the implementation are

```text
111100000
110011000
101010100
100110001
111111101
000011101
```

The last two masks are dependent members of the same span; the first four form a basis.

Verified parameters are:

```text
length                 9
rank                   4
size                   16
minimum distance       4
weight distribution    0^1 4^14 8^1
doubly even            yes
self-orthogonal        yes
self-dual in F_2^9     no
```

For every `c in C`:

\[
c_8=0,\qquad c_9=c_1\oplus\cdots\oplus c_8.
\]

Consequences:

- coordinate 9 is active in the code;
- coordinate 8 is unchanged by code translations;
- `C` is contained in `E`;
- translation by `C` preserves application integrity;
- translation by `C` preserves the measured temporal-change bit `x8`.

The code is not called self-dual in nine dimensions. Its dual has dimension five. Puncturing coordinate 8 produces the doubly-even self-dual `[8,4,4]` code `C8`, which is the code used for the Adinkra quotient.

## 5. Encoding and strict recovery

A four-bit message `m=(m1,m2,m3,m4)` is encoded by

\[
\operatorname{enc}(m)=mG.
\]

The decoder computes all 16 Hamming distances. It returns:

- `exact` when the distance is zero;
- `corrected` when there is one nearest codeword at distance one;
- `uncorrectable` in every other case.

The decoder does not accept a unique nearest codeword at distance two. Minimum distance four guarantees correction only through radius

\[
t=\left\lfloor\frac{d-1}{2}\right\rfloor=1.
\]

For a known branch anchor `a`, branch states have the form `a xor c`. Recovery computes `received xor a`, decodes the relative codeword, and reconstructs `a xor c`. This affine recovery is exhaustive and safe through one bit.

## 6. Code orbits and the averaging projection

For `x in V`, the code orbit is

\[
[x]_C=x+C=\{x\oplus c:c\in C\}.
\]

Every orbit has 16 states. `V` contains 32 such orbits; the integrity hyperplane `E` contains 16. Coordinate 8 is constant within each orbit.

For a real-valued function `f` on `V`, define

\[
(Tf)(x)=\frac1{16}\sum_{c\in C}f(x\oplus c).
\]

`T` is implemented exactly by `ash_model.projection.orbit_average`. It is a linear, self-adjoint, idempotent projection onto functions constant on code orbits. Random codeword translation is not the same operation as evaluating `T`; the repository provides separate exact and Monte Carlo implementations.

## 7. Image/video measurements

Input patches are grayscale, RGB, or RGBA arrays. Integer arrays are divided by their dtype maximum. Floating arrays must already be finite and in `[0,1]`; no data-dependent rescaling is allowed. RGBA alpha is ignored.

For RGB input, luma is

\[
Y=0.2126R+0.7152G+0.0722B.
\]

Forward differences are zero at the final row/column:

\[
D_x(i,j)=Y(i,j+1)-Y(i,j),\qquad
D_y(i,j)=Y(i+1,j)-Y(i,j).
\]

The eight measured coordinates are:

| Coordinate | Feature | Exact definition | Threshold | Hysteresis |
|---:|---|---|---:|---:|
| 1 | mean luminance | `mean(Y)` | 0.500 | 0.020 |
| 2 | RMS contrast | `min(1, 2*std(Y))` | 0.200 | 0.020 |
| 3 | edge energy | `mean(sqrt(Dx^2+Dy^2))/sqrt(2)` | 0.120 | 0.015 |
| 4 | texture energy | `mean(abs(Y-boxblur3(Y)))` | 0.080 | 0.015 |
| 5 | chroma energy | `mean(max(R,G,B)-min(R,G,B))`; zero for grayscale | 0.100 | 0.015 |
| 6 | horizontal-gradient energy | `mean(abs(Dx))` | 0.100 | 0.015 |
| 7 | vertical-gradient energy | `mean(abs(Dy))` | 0.100 | 0.015 |
| 8 | temporal change | `mean(abs(Y_current - Y_previous))`; zero without history | 0.080 | 0.020 |
| 9 | parity/integrity | XOR of coordinates 1-8 | exact | none |

Every measured value lies in `[0,1]` by construction.

## 8. Threshold and temporal transition rule

Without a previous state, measured bit `i` is one exactly when `feature_i >= threshold_i`; ties map to one.

With previous bit `b_i` and hysteresis `h_i`:

- if `b_i=0`, switch to one only at `feature_i >= threshold_i+h_i`;
- if `b_i=1`, switch to zero only at `feature_i < threshold_i-h_i`;
- otherwise retain the previous bit.

Bounds are clipped to `[0,1]`. Coordinate 9 is always recomputed after the first eight bits. A previous state that fails integrity is rejected.

This is the canonical temporal-state transition. It suppresses threshold flicker without introducing randomness or hidden learned parameters.

## 9. Branch grammar, weights, state mapping, and geometry

The semantic candidate tree has actions

```text
0  +  -
```

with probabilities

```text
P(0)=0.50, P(+)=0.25, P(-)=0.25.
```

At level `l` starting from zero:

- `0` leaves the four-bit message unchanged;
- `+` toggles message bit `l mod 4`;
- `-` toggles message bit `(l+1) mod 4`.

For source state `x`, a node with message `m` has

\[
c=\operatorname{enc}(m),\qquad x_{node}=x\oplus c.
\]

At depth `d` there are `3^d` leaves and total leaf weight one. Depth four reaches all 16 operator messages, although multiple paths can reach the same message. Duplicate leaf prior weights are summed before reconstruction.

Geometric segments use an initial upward heading, a 25-degree turn for `+/-`, and length decay 0.72 per level. The independently testable rendering L-system is

```text
axiom: F
rule:  F -> FF[+F]F[-F]
```

The geometry is a visualization of bounded branching. It is not assigned a quantum probability interpretation.

## 10. Reconstruction operators

For integer scale `s`, the baseline `u` is nearest-neighbor upsampling. Four exact basis actions are selected by decoded message bits:

1. horizontal-detail injection;
2. vertical-detail injection;
3. isotropic-detail injection;
4. isotropic-detail suppression.

With strength `alpha=0.125`, the output is

\[
R_m(u)=\operatorname{clip}_{[0,1]}\bigl(u+\alpha(m_1H_x+m_2H_y+m_3H-m_4H)\bigr),
\]

where `Hx`, `Hy`, and `H` are differences between `u` and fixed `[1,2,1]/4` directional or separable box blurs. Message `0000` is exactly the nearest-neighbor baseline.

The operator family is a deterministic reference semantics. A production upscaler may replace the basis operators only by publishing a new versioned specification and retaining the same input/output tests.

## 11. Source-consistency score and pruning

A candidate is block-mean downsampled to the source resolution. The losses are:

```text
Ldata     = mean((downsample(candidate)-source)^2)
Ledge     = mean((source gradients-candidate gradients)^2)/2
Ltemporal = mean((candidate-previous candidate)^2), or zero
```

The source score is

\[
S=\exp[-(4L_{data}+L_{edge}+0.5L_{temporal})].
\]

The total ranking score is

\[
\log P(message)+\log S.
\]

Candidates are ordered by descending total score and then by the numeric message value. Top-`k` pruning is therefore deterministic. No candidate is silently repaired beyond the decoder's one-bit radius.

## 12. Adinkra/Garden construction

Puncture coordinate 8 from `C` to obtain `C8`. The quotient `Q8/C8` has 16 cosets. Because `C8` is even, parity is well-defined on cosets, producing eight bosonic and eight fermionic vertices. Each quotient vertex has one edge of each of eight coordinate colors, for 64 undirected colored edges.

Define

```text
I = [[1,0],[0,1]]
X = [[0,1],[1,0]]
Z = [[1,0],[0,-1]]
J = [[0,1],[-1,0]]
```

and the eight signed-permutation matrices

```text
L1 = I tensor I tensor I
L2 = I tensor I tensor J
L3 = I tensor J tensor X
L4 = X tensor J tensor Z
L5 = Z tensor J tensor Z
L6 = J tensor Z tensor X
L7 = J tensor I tensor Z
L8 = J tensor X tensor X
```

With `R_I=L_I^T`, they satisfy exactly

\[
L_I R_J+L_J R_I=2\delta_{IJ}I_8.
\]

The quotient graph and matrix graph are color-preserving isomorphic after the one-based color permutation `[1,2,3,5,4,8,6,7]`. The generated Adinkra figure is therefore linked to executable matrices and the punctured code, rather than being an unrelated illustration.

## 13. Controlled Markov dynamics

The canonical noise kernel for `0<p<1` is

\[
P=(1-p)I+\frac p9\sum_{i=1}^{9}F_i,
\]

where `F_i` flips coordinate `i`. It is irreducible, aperiodic, symmetric, and doubly stochastic. Its unique stationary distribution is uniform on all 512 states. The Hamming-weight marginal of uniform occupancy is

\[
\Pr[\operatorname{wt}(X)=k]=\binom9k2^{-9}.
\]

Mixtures of code translations also preserve uniform occupancy. Therefore a bell-shaped Hamming histogram from a uniform start or symmetric bit-flip noise is a control baseline, not an ASH-specific causal result.

## 14. Normative artifacts and tests

The implementation generates:

- `data/ash-state-reference.csv`: every state, plane, integrity, orbit, and decoder result;
- `data/codewords.csv`: every message/codeword pair, weight, and syndrome;
- `data/branch-topology.json`: every node of the depth-4 tree;
- `data/ablation-results.csv`: controlled simulation cases;
- `proofs/computational-certificate.json`: exhaustive finite checks;
- `proofs/artifact-manifest.json`: SHA-256 hashes of generated evidence.

The test suite must pass before a release. The proof suite is an additional generated certificate, not a substitute for the mathematical arguments in `docs/mathematical-proof.md`.
