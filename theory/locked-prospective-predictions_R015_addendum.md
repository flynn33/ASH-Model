# R-015 locked prospective predictions addendum

R-015 is a locking layer above the R-012 background, R-013 perturbation, and R-014 likelihood-readiness workbenches. It freezes finite synthetic templates and falsification metadata before future external-data unblinding.

The lock has the abstract form

\[
\operatorname{Lock}(\Pi)=\operatorname{SHA256}(\Pi,\mathcal{D}_{\rm locked},t_{\rm freeze}),
\]

where \(\Pi\) is the prediction-ledger content, \(\mathcal{D}_{\rm locked}\) is the set of locked CSV data vectors, and \(t_{\rm freeze}\) is the declared freeze date.

This is an audit and preregistration mechanism, not an empirical result.
