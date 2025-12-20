## Appendix A: Supersymmetry Matrices and Proofs
We provide an explicit (1|4) valise adinkra representation via signed permutation matrices and verify the Garden algebra.

### Construction
Using Pauli matrices \( \sigma_1 = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \), \( \sigma_3 = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \), define:

\[ L_1 = \sigma_1 \otimes I_2 = \begin{pmatrix} 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}, \]

\[ L_2 = \sigma_3 \otimes \sigma_1 = \begin{pmatrix} 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & -1 \\ 0 & 0 & -1 & 0 \end{pmatrix}, \]

\[ L_3 = \sigma_3 \otimes \sigma_3 = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}, \]

\[ L_4 = \sigma_1 \otimes \sigma_3 = \begin{pmatrix} 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \\ 1 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \end{pmatrix}. \]

### Theorem A.1: Garden Algebra Verification
The matrices satisfy \( L_i L_j^T + L_j L_i^T = 2\delta_{ij} I_4 \).

**Proof**: [Full expanded proof from our discussions, including diagonal and off-diagonal cases with Pauli relations.]

[Include other theorems like A.2 Bijection, A.3 Counting, A.6 Automorphism, with derivations.]

## Appendix B: Coding Theory
### Definitions
Doubly-even code: wt(c) ≡ 0 mod 4 for all c in C.

### E8 Embedding into 9 Bits
Generator matrix for E8 (8-bit):

\[ G = \begin{pmatrix} 1&1&1&1&0&0&0&0 \\ 1&1&0&0&1&1&0&0 \\ 1&0&1&0&1&0&1&0 \\ 1&0&0&1&1&0&0&1 \end{pmatrix}. \]

Zero-padding to 9 bits: \( \tilde{G} = [G | 0] \).

## Appendix C: Mathematical Properties of 9
### Refactorability
τ(9)=3, 9 mod 3=0. See src/derive_9_properties.py for SymPy verification.

[Include full SymPy derivations from our last response, with code snippets and outputs.]

[Add other properties: odd composite, digital root, string dimensions.]
