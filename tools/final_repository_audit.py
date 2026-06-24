#!/usr/bin/env python3
"""Final repository-remediation audit runner.

This script runs the repository checks that must pass before the project moves
from repository remediation into science work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

COMMANDS = [
    [sys.executable, "-m", "pytest", "-q"],
    [sys.executable, "tools/run_proof_suite.py"],
    [sys.executable, "tools/verify_repository.py"],
    [sys.executable, "docs/ash-physics-validation/scripts/run_repository_gate.py", "."],
    [sys.executable, "tools/validate_json_assets.py", "."],
    [sys.executable, "tools/check_generated_outputs.py", ".", "--include-manuscript"],
    [sys.executable, "tools/audit_physics_readiness.py", ".", "--expect-open", "--write-json", "docs/remediation/physics-readiness.json"],
    [sys.executable, "tools/audit_live_repository_readiness.py", "."],
]

REQUIRED_PATHS = [
    "tools/validate_json_assets.py",
    "tools/check_generated_outputs.py",
    "tools/audit_physics_readiness.py",
    "tools/audit_live_repository_readiness.py",
    "tools/final_repository_audit.py",
    "tools/generate_artifacts.py",
    "tools/build_manuscript.py",
    "tools/run_proof_suite.py",
    "tools/verify_repository.py",
    "proofs/computational-certificate.json",
    "proofs/artifact-manifest.json",
    "proofs/manuscript-manifest.json",
    "validation/status.json",
    "predictions/prediction-ledger.json",
    "docs/remediation/final-repository-remediation.md",
    "docs/final-live-repository-audit.md",
    "docs/ash-physics-validation/tasks/science_manifest.json",
]


def run(root: Path, cmd: list[str]) -> dict[str, Any]:
    started = time.time()
    proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True)
    ended = time.time()
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "duration_seconds": round(ended - started, 3),
        "stdout_tail": proc.stdout[-6000:],
        "stderr_tail": proc.stderr[-6000:],
        "passed": proc.returncode == 0,
    }


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "dist", "build"} for part in rel.parts):
            continue
        if rel.as_posix() == "docs/remediation/final-remediation-evidence.json":
            continue
        digest.update(str(rel).encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def git_commit(root: Path) -> str | None:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True)
    if proc.returncode == 0:
        return proc.stdout.strip()
    return None


def physics_readiness_summary(root: Path) -> dict[str, Any]:
    path = root / "docs/remediation/physics-readiness.json"
    if not path.exists():
        return {"available": False}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "error": str(exc)}
    return {
        "available": True,
        "ready": payload.get("ready"),
        "blocker_count": payload.get("blocker_count"),
        "blockers": payload.get("blockers", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--write-json", default=None)
    parser.add_argument("--continue-on-failure", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    results: dict[str, Any] = {
        "schema_version": "1.0",
        "root": str(root),
        "timestamp_unix": int(time.time()),
        "commit": git_commit(root),
        "required_paths": [],
        "commands": [],
    }

    missing = []
    for rel in REQUIRED_PATHS:
        exists = (root / rel).exists()
        results["required_paths"].append({"path": rel, "exists": exists})
        if not exists:
            missing.append(rel)

    for cmd in COMMANDS:
        result = run(root, cmd)
        results["commands"].append(result)
        if result["returncode"] != 0 and not args.continue_on_failure:
            break

    readiness = physics_readiness_summary(root)
    passed = not missing and all(item.get("passed") for item in results["commands"])
    results["tree_hash"] = tree_hash(root)
    results["missing_required_paths"] = missing
    results["physics_readiness"] = readiness
    results["remaining_blockers_are_scientific"] = bool(
        passed and readiness.get("available") and readiness.get("ready") is False
    )
    results["passed"] = passed
    results["final_status"] = (
        "repository_remediation_complete" if passed else "repository_remediation_incomplete"
    )

    text = json.dumps(results, indent=2, sort_keys=True)
    print(text)
    if args.write_json:
        out = root / args.write_json
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
