#!/usr/bin/env python3
"""Bind the tracked manuscript PDF to deterministic source-input evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "latex" / "main.tex"
OUTPUT = REPO_ROOT / "docs" / "ASH-Model-Preprint-v1.pdf"
MANIFEST = REPO_ROOT / "proofs" / "manuscript-manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_epoch() -> str:
    """Derive a stable build epoch from CITATION.cff's ISO release date."""

    for line in (REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8").splitlines():
        if line.startswith("date-released:"):
            date_text = line.split(":", 1)[1].strip().strip('"\'')
            instant = datetime.strptime(date_text, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return str(int(instant.timestamp()))
    raise RuntimeError("CITATION.cff has no date-released field")


def source_input_paths() -> tuple[Path, ...]:
    """Return source-bound manuscript inputs tracked by the manifest."""

    paths = [
        SOURCE,
        REPO_ROOT / "latex" / "bibtex.bib",
        REPO_ROOT / "latex" / "references.bib",
        OUTPUT,
    ]
    paths.extend(sorted((REPO_ROOT / "figures").glob("*.png")))
    return tuple(path for path in paths if path.is_file())


def input_record(path: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def build_pdf() -> None:
    compiler = shutil.which("pdflatex")
    if compiler is None:
        raise SystemExit("pdflatex is required when --build-pdf is used")
    if not SOURCE.is_file():
        raise SystemExit(f"missing manuscript source: {SOURCE}")

    environment = os.environ.copy()
    environment.update(
        {
            "SOURCE_DATE_EPOCH": release_epoch(),
            "FORCE_SOURCE_DATE": "1",
            "TZ": "UTC",
        }
    )
    with tempfile.TemporaryDirectory(prefix="ash-manuscript-") as temporary:
        output_directory = Path(temporary)
        command = [
            compiler,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-output-directory={output_directory}",
            SOURCE.name,
        ]
        for _ in range(2):
            subprocess.run(
                command,
                cwd=SOURCE.parent,
                env=environment,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
        built = output_directory / "main.pdf"
        if not built.is_file():
            raise SystemExit("pdflatex did not produce main.pdf")
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(built, OUTPUT)


def manifest_payload() -> dict[str, object]:
    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    inputs = [input_record(path) for path in source_input_paths()]
    return {
        "schema_version": "1.1.0",
        "project_version": version,
        "verification_policy": "source_input_equivalence",
        "policy_description": (
            "The committed PDF is bound to deterministic hashes of the LaTeX source, "
            "bibliography files, generated figures, and current PDF bytes. CI fails "
            "when any source-bound input changes without a manifest update."
        ),
        "source_date_epoch": int(release_epoch()),
        "source_inputs": inputs,
        "environment": {
            "policy": "platform-independent source-input hashing",
            "pdflatex_required": False,
        },
    }


def record_manifest() -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(manifest_payload(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--build-pdf",
        action="store_true",
        help="Rebuild the PDF with pdflatex before recording the source-input manifest.",
    )
    args = parser.parse_args()
    if args.build_pdf:
        build_pdf()
    if not OUTPUT.is_file():
        raise SystemExit(f"missing tracked manuscript PDF: {OUTPUT}")
    record_manifest()
    print(
        json.dumps(
            {
                "manifest": MANIFEST.relative_to(REPO_ROOT).as_posix(),
                "verification_policy": "source_input_equivalence",
                "source_inputs": len(source_input_paths()),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
