#!/usr/bin/env python3
"""Validate tracked data-manifest entries against repository files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_ASSET_KEYS = {
    "path",
    "role",
    "format",
    "description",
    "size_bytes",
    "checksum_sha256",
    "sensitivity",
    "provenance",
    "license",
    "usage_restrictions",
    "tracked_with",
    "validation_status",
    "notes",
}

VALID_ROLES = {
    "raw",
    "processed",
    "sample",
    "synthetic",
    "external-reference",
    "generated-output",
    "documentation-asset",
}
VALID_SENSITIVITY = {"public", "internal", "confidential", "regulated", "unknown"}
VALID_TRACKING = {"git", "git-lfs", "ignored", "external", "unknown"}
VALID_STATUS = {"passed", "failed", "not run", "not applicable"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"manifest is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("manifest must be a JSON object")
    return payload


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def validate_manifest(root: Path, manifest_path: Path) -> dict[str, Any]:
    payload = load_manifest(manifest_path)
    failures: list[str] = []
    warnings: list[str] = []

    for key in ("schema_version", "generated_on", "assets"):
        if key not in payload:
            failures.append(f"missing top-level key: {key}")

    assets = payload.get("assets")
    if not isinstance(assets, list) or not assets:
        failures.append("assets must be a non-empty array")
        assets = []

    seen_paths: set[str] = set()
    checked_assets = 0
    external_assets = 0
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            failures.append(f"assets[{index}] must be an object")
            continue
        missing = sorted(REQUIRED_ASSET_KEYS - set(asset))
        if missing:
            failures.append(f"assets[{index}] missing keys: {', '.join(missing)}")
            continue

        relative = asset["path"]
        if not isinstance(relative, str) or not relative:
            failures.append(f"assets[{index}] path must be a non-empty string")
            continue
        if relative in seen_paths:
            failures.append(f"duplicate asset path: {relative}")
        seen_paths.add(relative)

        role = asset["role"]
        if role not in VALID_ROLES:
            failures.append(f"{relative}: invalid role {role!r}")
        sensitivity = asset["sensitivity"]
        if sensitivity not in VALID_SENSITIVITY:
            failures.append(f"{relative}: invalid sensitivity {sensitivity!r}")
        tracked_with = asset["tracked_with"]
        if tracked_with not in VALID_TRACKING:
            failures.append(f"{relative}: invalid tracked_with {tracked_with!r}")
        status = asset["validation_status"]
        if status not in VALID_STATUS:
            failures.append(f"{relative}: invalid validation_status {status!r}")

        if tracked_with == "external":
            external_assets += 1
            continue

        path = root / relative
        if not path.is_file():
            failures.append(f"{relative}: file does not exist")
            continue
        checked_assets += 1

        expected_size = asset["size_bytes"]
        if expected_size is not None and expected_size != path.stat().st_size:
            failures.append(f"{relative}: size_bytes mismatch")

        expected_hash = asset["checksum_sha256"]
        if expected_hash is not None and expected_hash != sha256(path):
            failures.append(f"{relative}: checksum_sha256 mismatch")

        if sensitivity in {"confidential", "regulated"} and tracked_with in {"git", "git-lfs"}:
            warnings.append(f"{relative}: sensitive asset is tracked in repository storage")

    return {
        "manifest": display_path(manifest_path, root),
        "asset_count": len(assets),
        "checked_assets": checked_assets,
        "external_assets": external_assets,
        "failures": failures,
        "warnings": warnings,
        "passed": not failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root.")
    parser.add_argument(
        "--manifest",
        default="data/manifests/data_manifest.json",
        help="Manifest path relative to the repository root.",
    )
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    manifest_path = (root / args.manifest).resolve()
    report = validate_manifest(root, manifest_path)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
