#!/usr/bin/env python3
"""Build the tracked manuscript PDF and record its source-to-binary linkage."""

from __future__ import annotations

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


def record_manifest() -> None:
    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    payload = {
        "schema_version": "1.0.0",
        "project_version": version,
        "source": {
            "path": SOURCE.relative_to(REPO_ROOT).as_posix(),
            "sha256": sha256(SOURCE),
            "bytes": SOURCE.stat().st_size,
        },
        "pdf": {
            "path": OUTPUT.relative_to(REPO_ROOT).as_posix(),
            "sha256": sha256(OUTPUT),
            "bytes": OUTPUT.stat().st_size,
        },
        "source_date_epoch": int(release_epoch()),
        "passes": 2,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    compiler = shutil.which("pdflatex")
    if compiler is None:
        raise SystemExit("pdflatex is required to build the manuscript")
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

    record_manifest()
    print(
        json.dumps(
            {
                "pdf": OUTPUT.relative_to(REPO_ROOT).as_posix(),
                "pdf_sha256": sha256(OUTPUT),
                "manifest": MANIFEST.relative_to(REPO_ROOT).as_posix(),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
