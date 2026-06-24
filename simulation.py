#!/usr/bin/env python3
"""Generate the controlled ASH ablation dataset and evidence figures.

This entry point does not claim that ASH codeword translations uniquely cause
a Gaussian distribution.  It regenerates the controlled comparisons used to
separate uniform-hypercube mixing from code-specific orbit structure.
"""

from __future__ import annotations

from tools.generate_artifacts import main


if __name__ == "__main__":
    raise SystemExit(main())
