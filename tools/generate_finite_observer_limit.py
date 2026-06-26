#!/usr/bin/env python
"""Generate R-011 finite-observer limit artifacts.

This generator writes CSV/JSON artifacts for roadmap R-011.  It uses only
stdlib for data generation.  If matplotlib is installed, it also refreshes the
three reference PNG figures; otherwise it writes all non-figure artifacts and
prints a boundary-preserving note.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from ash_model.finite_observer_limit import (
    ODD_LEVELS,
    adjacency_spectrum,
    causal_cone_sizes,
    causal_interval_size,
    edge_count,
    fiber_sizes,
    graph_degree,
    laplacian_gap,
    shell_counts,
    unit_scale_table,
    validation_summary,
)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def generate(out_root: Path, refresh_figures: bool = False) -> dict[str, object]:
    data_dir = out_root / "data" / "ash-cosmology" / "finite-observer-limit" / "v0.1"
    fig_dir = out_root / "figures" / "ash-cosmology" / "finite-observer-limit" / "v0.1"
    val_dir = out_root / "validation" / "finite-observer-limit" / "roadmap-011" / "outputs"
    data_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    shell_rows: list[dict[str, object]] = []
    for n in ODD_LEVELS:
        shells = shell_counts(n)
        cones = causal_cone_sizes(n)
        for radius in sorted(shells):
            shell_rows.append(
                {
                    "n": n,
                    "pair_radius": radius,
                    "shell_count": shells[radius],
                    "causal_cone_count": cones[radius],
                    "states": 2 ** (n - 1),
                    "degree": graph_degree(n),
                    "edges": edge_count(n),
                    "laplacian_gap": laplacian_gap(n),
                }
            )
    write_csv(
        data_dir / "r011_shells_cones_by_level.csv",
        ["n", "pair_radius", "shell_count", "causal_cone_count", "states", "degree", "edges", "laplacian_gap"],
        shell_rows,
    )

    spec_rows: list[dict[str, object]] = []
    for n in ODD_LEVELS:
        for r, eigenvalue, multiplicity in adjacency_spectrum(n):
            spec_rows.append({"n": n, "r": r, "adjacency_eigenvalue": eigenvalue, "multiplicity": multiplicity})
    write_csv(
        data_dir / "r011_halved_cube_spectrum.csv",
        ["n", "r", "adjacency_eigenvalue", "multiplicity"],
        spec_rows,
    )

    fiber_rows: list[dict[str, object]] = []
    for n in ODD_LEVELS:
        for m in ODD_LEVELS:
            if n >= m:
                sizes = list(fiber_sizes(n, m).values())
                expected = 2 ** (n - m)
                fiber_rows.append(
                    {
                        "source_n": n,
                        "target_m": m,
                        "target_states": len(sizes),
                        "min_fiber": min(sizes),
                        "max_fiber": max(sizes),
                        "expected_uniform_fiber": expected,
                        "uniform": min(sizes) == max(sizes) == expected,
                    }
                )
    write_csv(
        data_dir / "r011_projective_fibers.csv",
        ["source_n", "target_m", "target_states", "min_fiber", "max_fiber", "expected_uniform_fiber", "uniform"],
        fiber_rows,
    )

    unit_rows = [row.__dict__ for row in unit_scale_table(ell9_m=1.0, tau9_s=1.0)]
    write_csv(
        data_dir / "r011_normalized_unit_scales.csv",
        ["n", "states", "ell_m", "tau_s", "max_pair_diameter", "max_signal_radius_m"],
        unit_rows,
    )

    interval_rows: list[dict[str, object]] = []
    for n in (3, 5, 7, 9):
        for distance in range(n // 2 + 1):
            for time_gap in range(distance, min(distance + 4, n // 2 + 4)):
                interval_rows.append(
                    {
                        "n": n,
                        "endpoint_pair_distance": distance,
                        "time_gap": time_gap,
                        "causal_interval_nodes": causal_interval_size(n, time_gap, distance),
                    }
                )
    write_csv(
        data_dir / "r011_causal_interval_counts.csv",
        ["n", "endpoint_pair_distance", "time_gap", "causal_interval_nodes"],
        interval_rows,
    )

    summary = validation_summary()
    summary["interval_rows"] = len(interval_rows)
    (val_dir / "verification.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    if refresh_figures:
        try:
            import matplotlib.pyplot as plt
        except Exception as exc:  # pragma: no cover - environment-dependent fallback
            summary["figure_generation"] = f"skipped: matplotlib unavailable: {exc}"
            return summary

        fig_dir.mkdir(parents=True, exist_ok=True)

        n9_rows = [row for row in shell_rows if row["n"] == 9]
        plt.figure(figsize=(7, 4.5))
        plt.plot([row["pair_radius"] for row in n9_rows], [row["shell_count"] for row in n9_rows], marker="o", label="distance shell")
        plt.plot([row["pair_radius"] for row in n9_rows], [row["causal_cone_count"] for row in n9_rows], marker="o", label="closed causal cone")
        plt.xlabel("pair-flip radius r")
        plt.ylabel("state count")
        plt.title("R-011 finite causal shells in the n=9 admissible layer")
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_dir / "r011_n9_shells_and_cones.png", dpi=180)
        plt.close()

        spec9 = [row for row in spec_rows if row["n"] == 9]
        plt.figure(figsize=(7, 4.5))
        plt.bar([str(row["adjacency_eigenvalue"]) for row in spec9], [row["multiplicity"] for row in spec9])
        plt.xlabel("adjacency eigenvalue")
        plt.ylabel("multiplicity")
        plt.title("R-011 n=9 halved-cube adjacency spectrum")
        plt.tight_layout()
        plt.savefig(fig_dir / "r011_n9_spectrum.png", dpi=180)
        plt.close()

        fib9 = [row for row in fiber_rows if row["source_n"] == 9]
        plt.figure(figsize=(7, 4.5))
        plt.plot([row["target_m"] for row in fib9], [row["expected_uniform_fiber"] for row in fib9], marker="o")
        plt.xlabel("observer target dimension m")
        plt.ylabel("uniform fiber size from n=9")
        plt.title("R-011 projective coarse-graining fibers")
        plt.tight_layout()
        plt.savefig(fig_dir / "r011_projective_fibers.png", dpi=180)
        plt.close()

        summary["figure_generation"] = "refreshed"

    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", default=".", help="Repository root where artifacts should be written.")
    parser.add_argument("--refresh-figures", action="store_true", help="Refresh R-011 PNG figures if matplotlib is available.")
    args = parser.parse_args()
    summary = generate(Path(args.out_root), refresh_figures=args.refresh_figures)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
