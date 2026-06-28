#!/usr/bin/env python3
"""Generate ASH R-013 physical perturbation solver artifacts."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ash_model.physical_perturbations import run_artifacts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", default=".")
    parser.add_argument("--copy-source-figures", default=None)
    args = parser.parse_args()

    out_root = Path(args.out_root)
    tmp_root = out_root / "_tmp_r013_physical_perturbations"
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir(parents=True)

    summary = run_artifacts(tmp_root)

    data_dir = out_root / "data" / "ash-cosmology" / "physical-perturbations" / "v0.1"
    val_dir = out_root / "validation" / "physical-perturbations" / "roadmap-013" / "outputs"
    data_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    for path in (tmp_root / "data").glob("r013_*.csv"):
        shutil.copy2(path, data_dir / path.name)
    shutil.copy2(tmp_root / "validation" / "r013_validation_summary.json", val_dir / "r013_validation_summary.json")

    if args.copy_source_figures:
        fig_src = Path(args.copy_source_figures)
        fig_dst = out_root / "figures" / "ash-cosmology" / "physical-perturbations" / "v0.1"
        fig_dst.mkdir(parents=True, exist_ok=True)
        for path in fig_src.glob("r013_*.png"):
            shutil.copy2(path, fig_dst / path.name)

    shutil.rmtree(tmp_root)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
