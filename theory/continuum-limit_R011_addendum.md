# R-011 Addendum — Finite-Observer Limit Closure

This addendum accompanies roadmap item R-011 and should be integrated with `theory/continuum-limit.md`.

## Decision

R-011 is closed through a finite-observer limit construction, not through a differentiable continuum limit.

For odd observer levels \(n\in\{1,3,5,7,9\}\),

\[
\Omega_n=\{x\in\mathbb F_2^n:\sum_i x_i=0\pmod 2\}.
\]

The \(n=9\) level is the canonical ASH parity-valid admissible layer. Lower odd levels are finite projective observer resolutions.

## Projective hierarchy

For \(m\le n\), define

\[
\pi_{m,n}(x_1,\ldots,x_n)
=
(x_1,\ldots,x_{m-1},\sum_{i=1}^{m-1}x_i \bmod 2).
\]

This gives exact projective consistency:

\[
\pi_{\ell,m}\circ \pi_{m,n}=\pi_{\ell,n}.
\]

The fibers are uniform:

\[
|\pi_{m,n}^{-1}(y)|=2^{n-m}.
\]

## Finite limit interpretation

The “limit” here means a nested family of finite observers with exact parity-preserving projections and non-expanding event adjacency. It is a finite substitute for continuum reasoning, not a claim that a differentiable manifold exists.

## Boundary

No differentiable spacetime continuum, metric tensor, Lorentzian signature, Einstein equation, FRW background, physical perturbation equation, or empirical likelihood is derived by this addendum.
