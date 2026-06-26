#!/usr/bin/env python3
"""Generate Roadmap 007 finite linear perturbation artifacts.

Generated artifacts are deterministic finite-observer ASH outputs. They are not
empirical cosmology products and do not define a unit-bearing bridge.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable, Mapping

from ash_model.linear_perturbations import (
    formal_expression_summary,
    impulse_response_rows,
    random_perturbation_power_check,
    spectral_shell_table,
    synthetic_redshift_transfer_rows,
    transfer_function_rows,
    verify_character_eigenmodes,
)


DATA_RELATIVE = Path("data/ash-cosmology/linear-perturbations/v0.1")
FIGURE_RELATIVE = Path("figures/ash-cosmology/linear-perturbations/v0.1")
VALIDATION_RELATIVE = Path("validation/linear-perturbations/roadmap-007/outputs")


def _write_csv(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _shell_rows() -> list[dict[str, object]]:
    return [
        {
            "q": row.q,
            "representative_weight": row.representative_weight,
            "multiplicity": row.multiplicity,
            "krawtchouk_K2": row.krawtchouk_k2,
            "lambda_nonlazy": row.lambda_nonlazy,
            "gamma_continuous": row.gamma_continuous,
        }
        for row in spectral_shell_table()
    ]


def _write_figures(data_dir: Path, figure_dir: Path, ticks: int) -> None:
    import matplotlib.pyplot as plt

    figure_dir.mkdir(parents=True, exist_ok=True)

    for probability in (0.01, 0.05, 0.1):
        rows = transfer_function_rows(probability, ticks)
        xs = [row["tick"] for row in rows]
        plt.figure()
        for q in (1, 2, 3, 4):
            plt.plot(xs, [row[f"T_q{q}"] for row in rows], label=f"q={q}")
        plt.xlabel("finite ASH tick")
        plt.ylabel("mode transfer T_q")
        plt.title(f"ASH finite perturbation transfer functions, p={probability:g}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(figure_dir / f"transfer_functions_p_{probability:g}.png", dpi=180)
        plt.close()

    redshift_rows = synthetic_redshift_transfer_rows()
    plt.figure()
    for q in (1, 2, 3, 4):
        plt.plot([row["z_synthetic"] for row in redshift_rows], [row[f"T_q{q}"] for row in redshift_rows], label=f"q={q}")
    plt.xlabel("synthetic z")
    plt.ylabel("continuous-clock transfer T_q")
    plt.title("ASH finite perturbation synthetic transfer prototype")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_dir / "synthetic_redshift_transfer.png", dpi=180)
    plt.close()

    impulse_rows = impulse_response_rows(probability=0.05, ticks=ticks)
    plt.figure()
    xs = sorted({row["tick"] for row in impulse_rows})
    for q in (1, 2, 3, 4):
        plt.plot(xs, [row["impulse_response"] for row in impulse_rows if int(row["q"]) == q], label=f"q={q}")
    plt.xlabel("finite ASH tick")
    plt.ylabel("Green response G_q(t)")
    plt.title("ASH shell Green functions for a unit impulse, p=0.05")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_dir / "impulse_response_p_0.05.png", dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", default=".", help="repository root for generated outputs")
    parser.add_argument("--ticks", type=int, default=80)
    parser.add_argument("--refresh-figures", action="store_true")
    args = parser.parse_args()

    root = Path(args.out_root)
    data_dir = root / DATA_RELATIVE
    figure_dir = root / FIGURE_RELATIVE
    validation_dir = root / VALIDATION_RELATIVE

    data_dir.mkdir(parents=True, exist_ok=True)
    validation_dir.mkdir(parents=True, exist_ok=True)

    _write_csv(data_dir / "spectral_shells.csv", _shell_rows())
    for probability in (0.01, 0.05, 0.1, 0.5):
        _write_csv(data_dir / f"transfer_functions_p_{probability:g}.csv", transfer_function_rows(probability, args.ticks))

    power_check = random_perturbation_power_check()
    _write_csv(data_dir / "random_perturbation_power_check.csv", power_check["rows"])
    _write_csv(data_dir / "impulse_response_p_0.05.csv", impulse_response_rows(probability=0.05, ticks=args.ticks))
    _write_csv(data_dir / "synthetic_redshift_transfer.csv", synthetic_redshift_transfer_rows())

    verification = {
        "classification": {
            "layer_1": "finite Walsh quotient shell mathematics and pair-flip spectral law",
            "layer_2": "deterministic generated transfer, power-check, and Green-function artifacts",
            "layer_3_boundary": "synthetic dimensionless solver-test outputs only; no empirical cosmology",
        },
        "boundary": "Finite-observer perturbation sector only; no metric perturbation, physical power spectrum, CMB spectrum, or empirical redshift calibration claimed.",
        "eigenmode_verification": verify_character_eigenmodes(),
        "random_power_check": power_check,
        "formal_expressions": formal_expression_summary(),
    }
    (validation_dir / "verification.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.refresh_figures:
        _write_figures(data_dir, figure_dir, args.ticks)

    print(f"wrote finite perturbation data to {data_dir}")
    print(f"wrote verification JSON to {validation_dir / 'verification.json'}")
    if args.refresh_figures:
        print(f"wrote figures to {figure_dir}")


if __name__ == "__main__":
    main()
