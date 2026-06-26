# R-011 Addendum — Finite Causal Structure

This addendum accompanies `theory/causal-structure.md`.

## Event graph

At each odd observer level \(n\in\{1,3,5,7,9\}\), the finite event graph is the halved \(n\)-cube on

\[
\Omega_n=\{x\in\mathbb F_2^n:\sum_i x_i=0\pmod 2\}.
\]

The adjacency relation is

\[
x\sim_n y \iff d_H(x,y)=2.
\]

The graph metric is

\[
d_n(x,y)=\frac{1}{2}d_H(x,y).
\]

## Finite causal relation

For event nodes \((t,x)\) and \((s,y)\),

\[
(t,x)\preceq(s,y)\iff t\le s \text{ and } d_n(x,y)\le s-t.
\]

Finite causal cones have shell counts

\[
|S_r^{(n)}|=\binom{n}{2r}
\]

and closed cone counts

\[
|J^+_r(x)|=\sum_{q=0}^r\binom{n}{2q}.
\]

## Projection non-expansion

Projective observer maps do not expand microscopic pair-flip events: projected adjacent states are either adjacent at the target level or collapse to the same target state.

## Boundary

This is finite ASH graph reachability. It is not a physical light cone, a relativistic metric, or a statement about observed spacetime propagation.
