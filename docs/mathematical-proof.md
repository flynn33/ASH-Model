# Mathematical Proofs for the Canonical ASH Model

## 1. State-space cardinality and planes

Let `V=F_2^9`. Each of nine coordinates has two choices, so

\[
|V|=2^9=512.
\]

A vertex has one neighbor for each coordinate flip, hence degree nine. Exactly `k` coordinates are one at Hamming weight `k`, so plane `k` has

\[
\binom9k
\]

vertices. The complete count is

```text
1, 9, 36, 84, 126, 126, 84, 36, 9, 1.
```

These sum to 512 by the binomial theorem.

### Exact graph spectra

The adjacency matrix of `Q9` has eigenvalues

\[
\lambda_r=9-2r
\]

with multiplicity `C(9,r)` for `0<=r<=9`.  Equivalently, the
unnormalized graph Laplacian has eigenvalues

\[
\Delta_r=2r
\]

with the same multiplicities, so the finite graph spectral gap is `2`.
The trace identities

\[
\sum_r \lambda_r C(9,r)=0,\qquad
\sum_r \lambda_r^2 C(9,r)=2\cdot 2304
\]

match zero diagonal trace and twice the undirected edge count.

Restricting to the even-parity integrity subspace and using distance-two
pair-flip edges gives a 256-vertex graph with degree `C(9,2)=36` and 4608
undirected edges.  Its adjacency spectrum is

```text
36^1, 20^9, 8^36, 0^84, (-4)^126
```

and its unnormalized Laplacian spectral gap is `16`.

For the even-parity Hamming shells `w in {0,2,4,6,8}`, the shell
degeneracies are

```text
1, 36, 126, 84, 9
```

so the uniform admissible law has shell probabilities `C(9,w)/256`.  Its
finite background moments are

\[
\mathbb E[W]=9/2,\qquad \operatorname{Var}(W)=9/4,
\]

and the order parameter `1 - 2 E[W]/9` is zero.

## 2. The application integrity subspace

Define the linear functional

\[
q(x)=x_1+\cdots+x_9\pmod2.
\]

The integrity relation `x9=x1+...+x8` is equivalent to `q(x)=0`. Because `q` is a nonzero linear functional, its kernel has codimension one. Therefore

\[
\dim E=8,\qquad |E|=2^8=256.
\]

## 3. Rank and cardinality of the canonical code

The generator matrix is

\[
G=\begin{pmatrix}
1&1&1&1&0&0&0&0&0\\
1&1&0&0&1&1&0&0&0\\
1&0&1&0&1&0&1&0&0\\
1&0&0&1&1&0&0&0&1
\end{pmatrix}.
\]

Row reduction over `F_2` gives

\[
\begin{pmatrix}
1&0&0&1&0&1&1&0&0\\
0&1&0&1&0&1&0&0&1\\
0&0&1&1&0&0&1&0&1\\
0&0&0&0&1&1&1&0&1
\end{pmatrix},
\]

with pivots in columns 1, 2, 3, and 5. Thus `rank(G)=4`. The row-span map from `F_2^4` is injective, so

\[
|C|=2^4=16.
\]

## 4. Complete codeword certificate

There are only 16 messages, and their exact images are:

| Message | Codeword | Weight |
|---|---|---:|
| 0000 | 000000000 | 0 |
| 1111 | 000011101 | 4 |
| 0011 | 001100101 | 4 |
| 1100 | 001111000 | 4 |
| 0101 | 010101001 | 4 |
| 1010 | 010110100 | 4 |
| 0110 | 011001100 | 4 |
| 1001 | 011010001 | 4 |
| 1110 | 100101100 | 4 |
| 0001 | 100110001 | 4 |
| 1101 | 101001001 | 4 |
| 0010 | 101010100 | 4 |
| 1011 | 110000101 | 4 |
| 0100 | 110011000 | 4 |
| 1000 | 111100000 | 4 |
| 0111 | 111111101 | 8 |

This finite table proves the weight distribution `{0:1,4:14,8:1}`. Every weight is divisible by four, so `C` is doubly even. In a linear code, distance between codewords equals the weight of their difference, which is another codeword. The least nonzero weight is four, hence

\[
d_{min}(C)=4.
\]

## 5. Coordinate structure and parity

Column 8 of `G` is zero, so `c8=0` for every linear combination. Each generator row satisfies

\[
c_9=c_1+\cdots+c_8\pmod2.
\]

Both sides are linear functions of `c`, so the relation holds throughout the span. The fourth generator has `c9=1`, hence coordinate 9 is active.

Because every `c in C` satisfies the integrity relation, `C` is a subspace of `E`. If `x in E`, then

\[
q(x+c)=q(x)+q(c)=0,
\]

so every code translation preserves integrity. Since every `c` has `c8=0`, coordinate 8 is constant on each orbit `x+C`.

## 6. Self-orthogonality and non-self-duality in nine dimensions

For `u,v in C`, the identity

\[
\operatorname{wt}(u+v)=\operatorname{wt}(u)+\operatorname{wt}(v)-2|\operatorname{supp}(u)\cap\operatorname{supp}(v)|
\]

has all three weights divisible by four. Therefore the intersection size is even, and

\[
u\cdot v=0\pmod2.
\]

Thus `C` is self-orthogonal. For any binary linear code,

\[
\dim C+\dim C^\perp=9.
\]

Since `dim C=4`, `dim C-perp=5`. Therefore `C` is not self-dual in `F_2^9`. More generally, a self-dual binary code must have even length because its dimension must be half the length.

## 7. Punctured code and Adinkra quotient

Delete the invariant eighth coordinate. Puncturing is injective because that coordinate is zero on every codeword. The punctured code `C8` therefore has dimension four and the same nonzero weights, so it is a doubly-even `[8,4,4]` code.

The punctured code is self-orthogonal by the same argument. Its dimension is `8/2=4`; a self-orthogonal subspace of half dimension equals its orthogonal complement. Hence `C8` is self-dual.

The quotient `F_2^8/C8` has

\[
2^8/2^4=16
\]

cosets. Since all codewords have even weight, parity is constant on each coset. Exactly eight cosets are even and eight are odd. Flipping one of eight coordinates gives a colored edge and exchanges parity, so the quotient is an eight-colored bipartite 8-regular graph with

\[
16\cdot8/2=64
\]

undirected edges.

## 8. Garden algebra

Set

\[
I=\begin{pmatrix}1&0\\0&1\end{pmatrix},\quad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

The eight matrices in the canonical specification are Kronecker products of these factors. Each is a signed permutation matrix. `L1` is the identity. For `I>1`, `L_I` is antisymmetric and squares to `-I8`. Distinct nonidentity matrices anticommute. Therefore, with `R_I=L_I^T`:

- if `I=J`, `L_I R_I+L_I R_I=2I8`;
- if `I!=J`, the anticommutation relations give zero.

Hence

\[
L_I R_J+L_J R_I=2\delta_{IJ}I_8.
\]

The proof suite evaluates every one of the 64 matrix pairs with exact integer arithmetic and reports maximum residual zero. It also derives a color-preserving isomorphism between the matrix graph and `Q8/C8` after color permutation `[1,2,3,5,4,8,6,7]`.

## 9. Unique one-bit correction

Let `c` be sent and let `r` differ from `c` in at most one coordinate. For any other codeword `c'`, the triangle inequality gives

\[
d(r,c')\ge d(c,c')-d(r,c)\ge4-1=3.
\]

But `d(r,c)<=1`, so `c` is the unique nearest codeword. Every radius-one Hamming ball contains

\[
1+9=10
\]

states. The 16 balls are disjoint, accounting for 160 states: 16 exact codewords and 144 one-bit corruptions.

Two-bit correction is not guaranteed because the condition `2t<d` fails at `t=2`. The implementation therefore rejects every state with nearest distance greater than one, even when the nearest codeword happens to be unique. Exhaustive enumeration gives:

```text
exact                         16
corrected at distance 1      144
rejected                     352
```

Every one of the `16*36=576` two-bit corruptions of codewords is rejected.

## 10. Affine-orbit recovery

Suppose a branch anchor `a` is known and the valid branch state is `a+c`. If an error vector `e` of weight at most one is added, the receiver obtains

\[
r=a+c+e.
\]

Subtracting the anchor gives `r+a=c+e`, a radius-one codeword corruption. The previous theorem recovers `c`, then `a+c`. The proof suite checks all 256 integrity-valid anchors, all 16 codewords, and all nine single-bit errors:

\[
256\cdot16\cdot9=36{,}864
\]

successful affine corrections.

## 11. Orbit partition

The additive action of `C` on `V` is free: if `x+c=x`, then `c=0`. Every orbit therefore has 16 states. By orbit counting:

\[
|V/C|=512/16=32,\qquad |E/C|=256/16=16.
\]

## 12. Idempotence of orbit averaging

For any `f:V->R`,

\[
(T^2f)(x)=\frac1{|C|^2}\sum_{a\in C}\sum_{b\in C}f(x+a+b).
\]

For every fixed `d in C`, there are exactly `|C|` ordered pairs `(a,b)` with `a+b=d`—choose `a` freely and set `b=d+a`. Therefore

\[
(T^2f)(x)=\frac1{|C|}\sum_{d\in C}f(x+d)=(Tf)(x).
\]

So `T^2=T`. Translation reindexing also proves self-adjointness under the uniform inner product. Finally,

\[
(Tf)(x+c_0)=\frac1{|C|}\sum_{c\in C}f(x+c_0+c)=(Tf)(x),
\]

so the image consists of orbit-invariant functions. Conversely an orbit-invariant function is fixed by `T`. Thus `T` is exactly the orthogonal projection onto that subspace.

## 13. Markov-chain stationary distribution

For `0<p<1`, define

\[
P=(1-p)I+\frac p9\sum_iF_i.
\]

Each flip matrix `F_i` is a permutation matrix and is symmetric. Therefore `P` is symmetric and doubly stochastic, so the uniform distribution is stationary. Positive single-bit transitions connect all vertices of `Q9`, making the chain irreducible. The self-loop probability `1-p` is positive, making it aperiodic. A finite irreducible aperiodic chain has a unique stationary distribution and converges to it.

Under uniform occupancy, the nine bits are independent fair bits, so Hamming weight is exactly `Binomial(9,1/2)`. Any mixture of codeword translations is also doubly stochastic and preserves uniform occupancy. Therefore the binomial Hamming marginal is a generic uniform-state result. It cannot, by itself, distinguish ASH code translations from no transforms or other permutations.

## 14. Branch counts and normalization

Every semantic node has three children. Induction gives `3^d` leaves at depth `d` and

\[
1+3+\cdots+3^d=\frac{3^{d+1}-1}{2}
\]

total nodes. At depth four this is 81 leaves and 121 nodes.

Because child weights are parent weight multiplied by numbers summing to one, total weight is conserved at each level. Induction therefore gives total leaf weight one at every depth.

The level-dependent toggle rule reaches all 16 four-bit messages at depth four; the proof certificate confirms this by exact enumeration.

## 15. Bounded measurements and reconstruction

All normalized pixel values lie in `[0,1]`. Mean luminance, chroma range, absolute differences, and box-blur residual magnitudes are therefore bounded by one. Standard deviation on `[0,1]` is at most `1/2`, so `2*std` is bounded by one. Gradient magnitude is at most `sqrt(2)`, so the normalized edge feature is bounded by one. Thus every feature satisfies the required range.

Reconstruction output is explicitly clipped to `[0,1]`, so it is bounded. The source score is `exp(-L)` for `L>=0`; hence it lies in `(0,1]`. Message prior weights are nonnegative and sum to one, and deterministic tie-breaking makes pruning a total order.

## 16. Computational certificate

The mathematical arguments above are authoritative. The generated certificate independently checks all finite claims and records source hashes. Current exact counts include:

```text
512 hypercube states
256 integrity-valid states
32 full code orbits
16 integrity code orbits
16 codewords
144 single-bit codeword corrections
576 two-bit codeword-corruption rejections
36,864 affine single-bit corrections
64 Garden matrix identities by matrix-pair index
16 quotient vertices and 64 colored edges
81 depth-4 leaves and 16 operator messages
```

See `proofs/computational-certificate.json` for the complete machine-readable result.
