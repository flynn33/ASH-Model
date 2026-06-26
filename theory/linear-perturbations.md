# Linear Perturbations

Status: finite-observer Roadmap 007 perturbation sector specified and computationally testable.

## Scope

This document describes a finite perturbation sector on the ASH admissible state
space. It is a finite-state theorem-and-computation layer. It is not a metric
perturbation theory, not a gauge-fixed relativistic perturbation system, not a
cosmic matter power spectrum, and not a CMB angular spectrum.

The current physical layer interprets admissible ASH states as the 256-state
even-parity hyperplane of `F_2^9`. The baseline microscopic dynamics is the lazy
pair-flip Markov kernel already implemented in `ash_model.physics`.

## Perturbation variables

Let

\[
H=\{x\in\mathbb F_2^9:\sum_i x_i=0\pmod 2\},
\qquad |H|=256.
\]

Let `u` be the uniform law on `H`. A finite ASH perturbation is

\[
\rho_t(x)=u(x)+\delta_t(x),
\qquad \sum_{x\in H}\delta_t(x)=0.
\]

For a Walsh label \(a\in\mathbb F_2^9\), define

\[
\chi_a(x)=(-1)^{a\cdot x}
\]

and

\[
\alpha_{[a]}(t)=\sum_{x\in H}\delta_t(x)\chi_a(x).
\]

Because every admissible state has even parity,

\[
\chi_a|_H=\chi_{a+\mathbf 1}|_H.
\]

Therefore finite perturbation modes are characters of the quotient

\[
\mathbb F_2^9/\langle \mathbf 1\rangle.
\]

The canonical shell index is

\[
q([a])=\min(|a|_1,9-|a|_1)\in\{0,1,2,3,4\}.
\]

The shell multiplicities are:

| shell \(q\) | multiplicity |
|---:|---:|
| 0 | 1 |
| 1 | 9 |
| 2 | 36 |
| 3 | 84 |
| 4 | 126 |

The \(q=0\) shell is the constant normalization mode. Physical zero-sum
perturbations have no exact constant component except numerical roundoff.

## Pair-flip kernel

The lazy pair-flip kernel is

\[
P_p(x,y)=
(1-p)\mathbf 1_{y=x}
+
\frac{p}{\binom 92}
\sum_{m:|m|_1=2}\mathbf 1_{y=x+m}.
\]

There are \(\binom 92=36\) weight-two masks. The kernel preserves admissibility,
is symmetric, and keeps the uniform admissible law stationary.

## Exact spectral law

The non-lazy pair-flip eigenvalue for shell \(q\) is

\[
\lambda_q=\frac{K_2(q;9)}{\binom 92},
\]

where

\[
K_2(q;9)=
\binom{9-q}{2}
-
q(9-q)
+
\binom q2.
\]

Thus:

| \(q\) | \(K_2(q;9)\) | \(\lambda_q\) | \(\gamma_q=1-\lambda_q\) |
|---:|---:|---:|---:|
| 0 | 36 | 1 | 0 |
| 1 | 20 | 5/9 | 4/9 |
| 2 | 8 | 2/9 | 7/9 |
| 3 | 0 | 0 | 1 |
| 4 | -4 | -1/9 | 10/9 |

The one-tick finite equation is

\[
\alpha_{[a]}(t+1)=\mu_q(p_t)\alpha_{[a]}(t),
\]

with

\[
\mu_q(p_t)=1-p_t+p_t\lambda_q=1-p_t\gamma_q.
\]

For a finite update schedule,

\[
T_q(t_0,t_1)=\prod_{s=t_0}^{t_1-1}\mu_q(p_s),
\]

and

\[
\alpha_{[a]}(t_1)=T_q(t_0,t_1)\alpha_{[a]}(t_0).
\]

## Shell power

The finite ASH shell power is

\[
\mathcal P_q(t)=
\frac{1}{M_q}
\sum_{[a]:q([a])=q}
|\alpha_{[a]}(t)|^2.
\]

It evolves as

\[
\mathcal P_q(t_1)=|T_q(t_0,t_1)|^2\mathcal P_q(t_0).
\]

This is an internal finite-observer spectrum over ASH quotient shells. It is not
a physical \(P(k,z)\) unless a reviewed, unit-bearing bridge maps finite shell
labels to physical modes and supplies covariance, baselines, and locked
predictions.

## Continuous finite-observer clock limit

If

\[
p_t=r(\tau)\Delta\tau+O(\Delta\tau^2),
\]

then the finite-clock limit is

\[
\frac{d\alpha_{[a]}}{d\tau}
=
-r(\tau)\gamma_{q([a])}\alpha_{[a]}.
\]

For a finite interval,

\[
T_q(\tau_0,\tau_1)=
\exp\left[
-\gamma_q\int_{\tau_0}^{\tau_1}r(s)\,ds
\right].
\]

This is only a dimensionless finite-observer clock limit of the finite Markov
kernel. It is not a spacetime continuum limit.

## Source extension

For a declared finite source \(s_{[a]}(t)\),

\[
\alpha_{[a]}(t+1)=\mu_q(p_t)\alpha_{[a]}(t)+s_{[a]}(t).
\]

The retarded finite Green function is

\[
G_q(t,n)=
\begin{cases}
\prod_{r=n+1}^{t-1}\mu_q(p_r),&t>n,\\
0,&t\le n.
\end{cases}
\]

Therefore,

\[
\alpha_{[a]}(t)=
T_q(0,t)\alpha_{[a]}(0)
+
\sum_{n=0}^{t-1}G_q(t,n)s_{[a]}(n).
\]

## Implementation and evidence

Implementation:

- `ash_model.linear_perturbations`
- `tools/generate_linear_perturbations.py`

Tests:

- `tests/test_linear_perturbations.py`

Generated evidence paths:

- `data/ash-cosmology/linear-perturbations/v0.1/`
- `figures/ash-cosmology/linear-perturbations/v0.1/`
- `validation/linear-perturbations/roadmap-007/outputs/verification.json`

## Boundary

This sector provides exact finite perturbation dynamics on the ASH admissible
state space. It does not derive a metric, a gauge-fixed scalar/vector/tensor
cosmological perturbation theory, a cosmic matter power spectrum, or a CMB
angular spectrum. Those require an additional unit-bearing bridge and external
validation program.
