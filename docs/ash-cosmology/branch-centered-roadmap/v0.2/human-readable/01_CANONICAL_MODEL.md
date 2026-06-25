# ASH / Enneahcube Canonical Research Model

## Local finite alphabet

\[
\Omega = \mathbb F_2^9
\]

Each local event/site has a 9-bit state:

\[
x_v=(x_1,\ldots,x_9), \quad x_i\in\{0,1\}.
\]

The Enneahcube graph connects states by one-bit Hamming flips:

\[
x\sim y \iff d_H(x,y)=1.
\]

## Local admissibility code

ASH uses a rank-4 doubly-even linear code:

\[
C\subset \mathbb F_2^9, \quad [n,k,d]=[9,4,4].
\]

The code contributes finite integrity, defect detection, single-bit codeword correction, and algebraic constraints. It does **not** by itself define the whole cosmology.

## Branch history

A branch is a history path:

\[
b=(\mathcal U_0,\mathcal U_1,\ldots,\mathcal U_n).
\]

The branch tree rooted at \(\mathcal U_0\) is:

\[
\mathcal T_{\mathcal U_0}=\{b: b 	ext{ is an admissible ASH history branch}\}.
\]

A leaf is a frontier branch at depth/time \(n\):

\[
\ell\in L_n(\mathcal T).
\]

## Leaf data

A leaf should carry at least:

\[
\ell=(\mathrm{history},\mathrm{state},\mathrm{weight},\mathrm{phase},\mathrm{score},\mathrm{observer\_record}).
\]

For many-worlds ASH, the leaf is the central object. It is not a mere visualization artifact.
