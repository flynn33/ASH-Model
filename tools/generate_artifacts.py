#!/usr/bin/env python3
"""Regenerate deterministic data artifacts and bind tracked figure artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.sans-serif": ["DejaVu Sans"],
        "path.simplify": False,
        "text.usetex": False,
    }
)

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ash_model.adinkra import matrix_edges
from ash_model.bits import flip_bit, hamming_weight
from ash_model.branching import generate_branch_tree, leaf_nodes
from ash_model.code import CODEWORDS, MESSAGE_CODEWORD_PAIRS, decode, syndrome
from ash_model.hypercube import projection_coordinates, state_reference_rows, states
from ash_model.simulation import binomial_distribution, run_ablation_suite, run_simulation

PNG_METADATA = {"Software": "ASH Model artifact generator"}
TRACKED_FIGURES = (
    "figures/simulation-histogram.png",
    "figures/single-bit-error.png",
    "figures/hypercube-3d-projection.png",
    "figures/adinkra-graph-colored.png",
    "figures/branch-topology.png",
)


def _write_codewords() -> Path:
    path = REPO_ROOT / "data" / "codewords.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["message", "codeword", "weight", "syndrome"])
        for message, codeword in MESSAGE_CODEWORD_PAIRS:
            writer.writerow(
                [
                    "".join(map(str, message)),
                    "".join(map(str, codeword)),
                    hamming_weight(codeword),
                    "".join(map(str, syndrome(codeword))),
                ]
            )
    return path


def _write_state_reference() -> Path:
    path = REPO_ROOT / "data" / "ash-state-reference.csv"
    rows = state_reference_rows()
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def _write_branch_topology() -> Path:
    source = (0,) * 9
    nodes = generate_branch_tree(source, depth=4)
    payload = {
        "schema_version": "1.0.0",
        "source_state": "000000000",
        "node_count": len(nodes),
        "leaf_count": len(leaf_nodes(nodes)),
        "nodes": [
            {
                "path": node.path,
                "parent_path": node.parent_path,
                "depth": node.depth,
                "action": node.action,
                "message": "".join(map(str, node.message)),
                "codeword": "".join(map(str, node.codeword)),
                "state": "".join(map(str, node.state)),
                "weight": node.weight,
                "start": list(node.start),
                "end": list(node.end),
                "heading_radians": node.heading_radians,
                "segment_length": node.segment_length,
            }
            for node in nodes
        ],
    }
    path = REPO_ROOT / "data" / "branch-topology.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_simulation_data() -> tuple[Path, Path]:
    result = run_simulation(
        agent_count=1000,
        ticks=250,
        initial_mode="uniform",
        transform_mode="ash",
        noise_probability=0.01,
        seed=20260624,
    )
    csv_path = REPO_ROOT / "data" / "simulation-results.csv"
    np.savetxt(
        csv_path,
        result.agents,
        fmt="%d",
        delimiter=",",
        header="dim1,dim2,dim3,dim4,dim5,dim6,dim7,dim8,dim9",
        comments="",
    )
    metadata = {
        "seed": result.seed,
        "agent_count": len(result.agents),
        "ticks": result.ticks,
        "initial_mode": result.initial_mode,
        "transform_mode": result.transform_mode,
        "noise_probability": result.noise_probability,
        "tv_to_binomial": result.tv_to_binomial,
        "interpretation": "Controlled mixing sample; not evidence that ASH transforms uniquely produce the binomial envelope.",
    }
    metadata_path = REPO_ROOT / "data" / "simulation-metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return csv_path, metadata_path


def _write_ablation_data():
    results = run_ablation_suite(agent_count=12_000, ticks=300, noise_probability=0.02, seed=20260624)
    path = REPO_ROOT / "data" / "ablation-results.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "case",
                "initial_mode",
                "transform_mode",
                "noise_probability",
                "ticks",
                "seed",
                "tv_to_binomial",
                *[f"plane_{weight}" for weight in range(10)],
            ]
        )
        for index, result in enumerate(results):
            writer.writerow(
                [
                    index,
                    result.initial_mode,
                    result.transform_mode,
                    result.noise_probability,
                    result.ticks,
                    result.seed,
                    result.tv_to_binomial,
                    *result.occupancy.tolist(),
                ]
            )
    return path, results


def _plot_simulation_histogram(results) -> Path:
    path = REPO_ROOT / "figures" / "simulation-histogram.png"
    expected = binomial_distribution()
    selected = [results[0], results[1], results[4]]
    labels = [
        "Uniform start, no dynamics",
        "Uniform start, ASH + noise",
        "Zero start, ASH + noise",
    ]
    planes = np.arange(10)
    width = 0.20
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(planes - 1.5 * width, expected, width=width, label="Exact Binomial(9, 1/2)")
    for offset, (result, label) in enumerate(zip(selected, labels, strict=True), start=0):
        ax.bar(planes + (-0.5 + offset) * width, result.occupancy, width=width, label=label)
    ax.set_xlabel("Hamming-weight plane")
    ax.set_ylabel("Occupancy probability")
    ax.set_title("Controlled ASH ablations: the binomial envelope is a uniform-state baseline")
    ax.set_xticks(planes)
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180, metadata=PNG_METADATA)
    plt.close(fig)
    return path


def _plot_single_bit_error() -> Path:
    path = REPO_ROOT / "figures" / "single-bit-error.png"
    codeword = CODEWORDS[5]
    corrupted = flip_bit(codeword, 8)
    result = decode(corrupted)
    recovered = result.codeword
    rows = [("Codeword", codeword), ("One-bit error", corrupted), ("Decoded", recovered)]
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.set_xlim(-0.5, 9.8)
    ax.set_ylim(-0.6, 2.8)
    for row_index, (label, bits) in enumerate(rows):
        y = 2 - row_index
        ax.text(-0.35, y, label, ha="right", va="center", fontsize=11)
        for coordinate, bit in enumerate(bits):
            face = "#f0d0d0" if row_index == 1 and coordinate == 8 else "#e8eef7"
            rectangle = plt.Rectangle((coordinate, y - 0.32), 0.82, 0.64, facecolor=face, edgecolor="black")
            ax.add_patch(rectangle)
            ax.text(coordinate + 0.41, y, str(bit), ha="center", va="center", fontsize=12)
            if row_index == 0:
                ax.text(coordinate + 0.41, 2.43, str(coordinate + 1), ha="center", va="center", fontsize=8)
    ax.text(9.15, 1.0, f"status: {result.status}\ndistance: {result.distance}", va="center", fontsize=10)
    ax.set_title("Canonical [9,4,4] bounded-distance recovery")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=180, metadata=PNG_METADATA)
    plt.close(fig)
    return path


def _plot_hypercube_projection() -> Path:
    path = REPO_ROOT / "figures" / "hypercube-3d-projection.png"
    all_states = states()
    coordinates = np.asarray([projection_coordinates(state) for state in all_states])
    weights = np.asarray([hamming_weight(state) for state in all_states])
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")
    # Draw all 2304 undirected Q9 edges once.
    for index, state in enumerate(all_states):
        for bit in range(9):
            neighbor_index = index ^ (1 << bit)
            if neighbor_index > index:
                segment = coordinates[[index, neighbor_index]]
                ax.plot(segment[:, 0], segment[:, 1], segment[:, 2], linewidth=0.25, alpha=0.08, color="black")
    scatter = ax.scatter(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2], c=weights, s=9, cmap="viridis")
    ax.set_title("Deterministic 3D projection of all 512 Q9 vertices")
    ax.set_xlabel("projection axis 1")
    ax.set_ylabel("projection axis 2")
    ax.set_zlabel("projection axis 3")
    fig.colorbar(scatter, ax=ax, shrink=0.65, label="Hamming weight")
    fig.tight_layout()
    fig.savefig(path, dpi=180, metadata=PNG_METADATA)
    plt.close(fig)
    return path


def _plot_adinkra() -> Path:
    path = REPO_ROOT / "figures" / "adinkra-graph-colored.png"
    edges = matrix_edges()
    palette = plt.get_cmap("tab10")
    boson_positions = {index: (0.0, 7 - index) for index in range(8)}
    fermion_positions = {index: (5.0, 7 - index) for index in range(8)}
    fig, ax = plt.subplots(figsize=(10, 7))
    for edge in edges:
        start = boson_positions[edge.boson]
        end = fermion_positions[edge.fermion]
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            color=palette(edge.color),
            linewidth=1.0,
            alpha=0.72,
            linestyle="-" if edge.sign > 0 else "--",
        )
    for index, (x, y) in boson_positions.items():
        ax.scatter([x], [y], s=85, facecolor="white", edgecolor="black", zorder=3)
        ax.text(x - 0.18, y, f"B{index}", ha="right", va="center")
    for index, (x, y) in fermion_positions.items():
        ax.scatter([x], [y], s=85, facecolor="black", edgecolor="black", zorder=3)
        ax.text(x + 0.18, y, f"F{index}", ha="left", va="center")
    ax.set_title("N=8 Garden-algebra Adinkra associated with Q8/C8")
    ax.text(2.5, -0.65, "solid = +1, dashed = -1; edge color = generator", ha="center")
    ax.set_xlim(-1.2, 6.2)
    ax.set_ylim(-1.0, 7.7)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=180, metadata=PNG_METADATA)
    plt.close(fig)
    return path


def _plot_branch_topology() -> Path:
    path = REPO_ROOT / "figures" / "branch-topology.png"
    nodes = generate_branch_tree((0,) * 9, depth=4)
    fig, ax = plt.subplots(figsize=(9, 8))
    for node in nodes:
        if node.depth == 0:
            continue
        ax.plot(
            [node.start[0], node.end[0]],
            [node.start[1], node.end[1]],
            linewidth=max(0.4, 2.2 - 0.35 * node.depth),
            alpha=0.65,
        )
    leaves = leaf_nodes(nodes)
    ax.scatter([node.end[0] for node in leaves], [node.end[1] for node in leaves], s=8)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title("Depth-4 bounded branch topology (81 leaves, 16 operator states)")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=180, metadata=PNG_METADATA)
    plt.close(fig)
    return path


def _write_manifest(paths: list[Path]) -> Path:
    entries = {}
    for path in sorted(paths):
        entries[path.relative_to(REPO_ROOT).as_posix()] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
    manifest_path = REPO_ROOT / "proofs" / "artifact-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path


def _tracked_figure_paths() -> list[Path]:
    paths = [REPO_ROOT / relative for relative in TRACKED_FIGURES]
    missing = [path.relative_to(REPO_ROOT).as_posix() for path in paths if not path.is_file()]
    if missing:
        raise SystemExit(
            "missing tracked figure artifacts: "
            + ", ".join(missing)
            + "; run with --refresh-figures to redraw them"
        )
    return paths


def _refresh_figures(results) -> list[Path]:
    return [
        _plot_simulation_histogram(results),
        _plot_single_bit_error(),
        _plot_hypercube_projection(),
        _plot_adinkra(),
        _plot_branch_topology(),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh-figures",
        action="store_true",
        help=(
            "Redraw tracked PNG figures before recording the artifact manifest. "
            "The default preserves committed figure bytes and verifies them by hash."
        ),
    )
    args = parser.parse_args()

    (REPO_ROOT / "data").mkdir(exist_ok=True)
    (REPO_ROOT / "figures").mkdir(exist_ok=True)
    generated: list[Path] = []
    generated.append(_write_codewords())
    generated.append(_write_state_reference())
    generated.append(_write_branch_topology())
    generated.extend(_write_simulation_data())
    ablation_path, results = _write_ablation_data()
    generated.append(ablation_path)
    figure_paths = _refresh_figures(results) if args.refresh_figures else _tracked_figure_paths()
    generated.extend(figure_paths)
    manifest = _write_manifest(generated)
    data_count = len(generated) - len(figure_paths)
    figure_action = "refreshed" if args.refresh_figures else "verified"
    print(
        f"Generated {data_count} data artifacts, "
        f"{figure_action} {len(figure_paths)} figure artifacts, "
        f"and wrote {manifest.relative_to(REPO_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
