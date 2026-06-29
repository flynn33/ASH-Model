# Executive Summary

This package is a science remediation handoff for ASH R012-R016.

The accepted valid audit finding is that R012-R016 were completed as synthetic/readiness/lock/contract infrastructure, not as executed cosmological science. This handoff performs a first-pass scientific execution:

- **R012:** derives the exact finite ASH pair-flip Walsh spectrum and constructs a two-mode finite-spectral FRW dark-sector equation.
- **R013:** derives and solves a sub-horizon growth equation, then calibrates the finite slow-mode coupling against DES Y3 S8.
- **R014:** builds and runs a compact real-data DESI DR2 BAO likelihood with covariance blocks and compressed Planck priors.
- **R015:** pilot-scores all three locked prediction templates. P001 and P002 are not confirmed by the pilot; P003 is sign-consistent only.
- **R016:** emits a machine-readable formal closure certificate for the finite-kernel-to-observable map.

Key numerical result: in the compressed DESI DR2 BAO + Planck H0/Omega_m pilot, the ASH finite-spectral model has chi2 = 8.798979, with H0 = 67.235337, Omega_m = 0.313819, w0_eff = -0.792809, and wa_eff = -0.812636.

Important scientific warning: the current locked R015 P001 expansion residual and P002 positive matter-sector coupling do not survive this first real-data pilot as stated. They should be treated as needing supersession or formal falsification review, not as supported predictions.

This package is still not presented as empirical validation of ASH as observed cosmology. The full next layer requires full survey likelihood products: SN covariance, DESI likelihood products, weak-lensing or galaxy-clustering covariance, and map-level low-ell CMB likelihoods.
