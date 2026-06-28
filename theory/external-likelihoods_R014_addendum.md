# R-014 Addendum: External Likelihood Contract

This addendum defines the finite external-likelihood scoring contract used by R-014.

For a data vector $d\in\mathbb{R}^n$, model vector $m_\theta$, and covariance $C$, the score is

$$
\log \mathcal L(d\mid\theta)
= -\frac12\left[(d-m_\theta)^T C^{-1}(d-m_\theta)+\log |C|+n\log(2\pi)\right].
$$

The implementation evaluates the quadratic form and log determinant through a Cholesky factorization. Therefore, $C$ must be symmetric positive definite for the declared default likelihood.

This addendum is a validation contract. It is not an empirical result and does not replace official external likelihood codes for Planck, Pantheon+, DESI, BOSS, or future survey products.
