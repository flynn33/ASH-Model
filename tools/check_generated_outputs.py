#!/usr/bin/env python3
"""Check that generated repository artifacts are current.

This script assumes it is run from a git working tree. It runs artifact generation,
then verifies that generated paths do not produce an unintended diff. Manuscript
verification can be included after the repository selects byte-deterministic or
equivalence-checked manuscript policy.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

GENERATED_PATHS = [
    "data",
    "figures",
    "proofs/artifact-manifest.json",
    "proofs/computational-certificate.json",
    "proofs/computational-certificate.md",
]
MANUSCRIPT_PATHS = [
    "docs/ASH-Model-Preprint-v1.pdf",
    "proofs/manuscript-manifest.json",
]


def run(root: Path, cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def diff_check(root: Path, paths: list[str]) -> dict[str, Any]:
    cmd = ["git", "diff", "--exit-code", "--"] + paths
    result = run(root, cmd)
    result["paths"] = paths
    result["passed"] = result["returncode"] == 0
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--include-manuscript", action="store_true")
    parser.add_argument("--write-json", default=None)
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    results: dict[str, Any] = {"root": str(root), "steps": []}

    if not (root / ".git").exists():
        results["passed"] = False
        results["error"] = "repository root must be a git working tree for generated-diff checks"
        print(json.dumps(results, indent=2, sort_keys=True))
        return 1

    gen = run(root, [sys.executable, "tools/generate_artifacts.py"])
    results["steps"].append({"name": "generate_artifacts", **gen})
    if gen["returncode"] != 0:
        results["passed"] = False
        print(json.dumps(results, indent=2, sort_keys=True))
        return 1

    artifact_diff = diff_check(root, GENERATED_PATHS)
    results["steps"].append({"name": "generated_artifact_diff", **artifact_diff})

    manuscript_ok = True
    if args.include_manuscript:
        build = run(root, [sys.executable, "tools/build_manuscript.py"])
        results["steps"].append({"name": "build_manuscript", **build})
        if build["returncode"] != 0:
            manuscript_ok = False
        else:
            manuscript_diff = diff_check(root, MANUSCRIPT_PATHS)
            results["steps"].append({"name": "manuscript_diff", **manuscript_diff})
            manuscript_ok = manuscript_diff["passed"]

    results["passed"] = artifact_diff["passed"] and manuscript_ok
    text = json.dumps(results, indent=2, sort_keys=True)
    print(text)
    if args.write_json:
        out = root / args.write_json
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    return 0 if results["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
