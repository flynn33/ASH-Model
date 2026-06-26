#!/usr/bin/env python3
"""Validate repository JSON files and active JSON-schema pairs.

Usage:
    python tools/validate_json_assets.py .
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover - reported at runtime
    jsonschema = None


SCHEMA_PAIRS = [
    (
        "data/manifests/data_manifest.json",
        "docs/ash-physics-validation/configs/data_manifest.schema.json",
    ),
    (
        "docs/ash-physics-validation/tasks/task_manifest.json",
        "docs/ash-physics-validation/configs/task_manifest.schema.json",
    ),
    (
        "docs/ash-physics-validation/tasks/science_manifest.json",
        "docs/ash-physics-validation/configs/science_manifest.schema.json",
    ),
    (
        "predictions/prediction-ledger.json",
        "docs/ash-physics-validation/configs/prediction_ledger.schema.json",
    ),
    (
        "validation/status.json",
        "docs/ash-physics-validation/configs/validation_status.schema.json",
    ),
    (
        "proofs/computational-certificate.json",
        "docs/ash-physics-validation/configs/proof_certificate.schema.json",
    ),
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_json_files(root: Path):
    for path in sorted(root.rglob("*.json")):
        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--write-json", default=None)
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    results: dict[str, Any] = {
        "root": str(root),
        "json_parse_errors": [],
        "schema_results": [],
        "schema_library_available": jsonschema is not None,
    }

    for path in iter_json_files(root):
        try:
            load_json(path)
        except Exception as exc:
            results["json_parse_errors"].append({"path": str(path.relative_to(root)), "error": str(exc)})

    if jsonschema is None:
        results["schema_results"].append({
            "result": "fail",
            "error": "jsonschema package is not installed; add it to dev dependencies or vendor a validator.",
        })
    else:
        for instance_rel, schema_rel in SCHEMA_PAIRS:
            instance = root / instance_rel
            schema = root / schema_rel
            if not instance.exists() or not schema.exists():
                results["schema_results"].append({
                    "instance": instance_rel,
                    "schema": schema_rel,
                    "result": "fail",
                    "error": "missing instance or schema",
                })
                continue
            try:
                jsonschema.Draft202012Validator.check_schema(load_json(schema))
                jsonschema.validate(load_json(instance), load_json(schema))
                results["schema_results"].append({
                    "instance": instance_rel,
                    "schema": schema_rel,
                    "result": "pass",
                })
            except Exception as exc:
                results["schema_results"].append({
                    "instance": instance_rel,
                    "schema": schema_rel,
                    "result": "fail",
                    "error": str(exc),
                })

    failed = bool(results["json_parse_errors"]) or any(
        item.get("result") != "pass" for item in results["schema_results"]
    )
    results["passed"] = not failed

    text = json.dumps(results, indent=2, sort_keys=True)
    print(text)
    if args.write_json:
        out = root / args.write_json
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
