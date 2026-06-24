#!/usr/bin/env python3
"""Fail-fast verification for claims, generated artifacts, versions, and proofs."""

from __future__ import annotations

import hashlib
import json
import re
import tomllib
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PHRASES = (
    "doubly-even self-dual error-correcting codes " + "within a 9-dimensional",
    "all mathematical and computational claims are verified",
    "regardless of initial conditions, occupancy converges",
    "quantum measurement statistics",
)

MANIFEST_ARTIFACTS = (
    "data/ash-state-reference.csv",
    "data/codewords.csv",
    "data/ablation-results.csv",
    "data/branch-topology.json",
    "data/simulation-results.csv",
    "data/simulation-metadata.json",
    "figures/simulation-histogram.png",
    "figures/single-bit-error.png",
    "figures/hypercube-3d-projection.png",
    "figures/adinkra-graph-colored.png",
    "figures/branch-topology.png",
)

REQUIRED_ARTIFACTS = MANIFEST_ARTIFACTS + (
    "proofs/computational-certificate.json",
    "proofs/computational-certificate.md",
    "proofs/artifact-manifest.json",
    "proofs/manuscript-manifest.json",
    "docs/ASH-Model-Preprint-v1.pdf",
)

SOURCE_SUFFIXES = {".py", ".json", ".toml", ".md", ".tex", ".yml", ".yaml", ".cff"}
SOURCE_FILENAMES = {"LICENSE", "VERSION", ".gitignore"}
SOURCE_EXCLUDED_PREFIXES = ("proofs/",)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_source_manifest() -> dict[str, str]:
    """Hash every normative text/source file covered by the proof certificate."""

    manifest: dict[str, str] = {}
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(REPO_ROOT).as_posix()
        if relative.startswith(SOURCE_EXCLUDED_PREFIXES):
            continue
        if "__pycache__" in path.parts or ".pytest_cache" in path.parts:
            continue
        if path.suffix.lower() not in SOURCE_SUFFIXES and path.name not in SOURCE_FILENAMES:
            continue
        manifest[relative] = sha256(path)
    return manifest


def scan_claims() -> list[str]:
    """Find exact legacy overclaims in human- and machine-readable source."""

    suffixes = {".md", ".py", ".tex", ".json", ".yml", ".yaml", ".toml"}
    exclusions = {
        Path(__file__).resolve(),
        (REPO_ROOT / "tests" / "test_repository_claims.py").resolve(),
    }
    violations = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if path.resolve() in exclusions or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                violations.append(f"{path.relative_to(REPO_ROOT)}: {phrase}")
    return violations


def compare_manifests(expected: dict[str, str], actual: dict[str, str]) -> list[str]:
    """Return deterministic key/hash mismatches between two SHA-256 maps."""

    mismatches: list[str] = []
    for relative in sorted(set(expected) | set(actual)):
        if relative not in expected:
            mismatches.append(f"unexpected source: {relative}")
        elif relative not in actual:
            mismatches.append(f"missing source: {relative}")
        elif expected[relative] != actual[relative]:
            mismatches.append(f"changed source: {relative}")
    return mismatches


def verify_artifact_manifest() -> list[str]:
    """Recompute every tracked generated-artifact hash and byte count."""

    manifest_path = REPO_ROOT / "proofs" / "artifact-manifest.json"
    if not manifest_path.is_file():
        return ["missing proofs/artifact-manifest.json"]
    payload: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    mismatches: list[str] = []
    expected_keys = set(MANIFEST_ARTIFACTS)
    actual_keys = set(payload)
    for relative in sorted(expected_keys - actual_keys):
        mismatches.append(f"manifest omits artifact: {relative}")
    for relative in sorted(actual_keys - expected_keys):
        mismatches.append(f"manifest contains unexpected artifact: {relative}")
    for relative in sorted(expected_keys & actual_keys):
        path = REPO_ROOT / relative
        if not path.is_file():
            mismatches.append(f"missing artifact: {relative}")
            continue
        entry = payload[relative]
        if not isinstance(entry, dict):
            mismatches.append(f"invalid manifest entry: {relative}")
            continue
        if entry.get("sha256") != sha256(path):
            mismatches.append(f"artifact hash mismatch: {relative}")
        if entry.get("bytes") != path.stat().st_size:
            mismatches.append(f"artifact byte-count mismatch: {relative}")
    return mismatches



def verify_manuscript_manifest() -> list[str]:
    """Bind the tracked PDF to the exact LaTeX source and release version."""

    manifest_path = REPO_ROOT / "proofs" / "manuscript-manifest.json"
    if not manifest_path.is_file():
        return ["missing proofs/manuscript-manifest.json"]
    try:
        payload: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"invalid manuscript manifest: {exc}"]

    mismatches: list[str] = []
    expected_version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if payload.get("project_version") != expected_version:
        mismatches.append("manuscript manifest project version mismatch")

    expected_entries = {
        "source": "latex/main.tex",
        "pdf": "docs/ASH-Model-Preprint-v1.pdf",
    }
    for section, expected_path in expected_entries.items():
        entry = payload.get(section)
        if not isinstance(entry, dict):
            mismatches.append(f"manuscript manifest has invalid {section} entry")
            continue
        if entry.get("path") != expected_path:
            mismatches.append(f"manuscript manifest {section} path mismatch")
            continue
        path = REPO_ROOT / expected_path
        if not path.is_file():
            mismatches.append(f"missing manuscript {section}: {expected_path}")
            continue
        if entry.get("sha256") != sha256(path):
            mismatches.append(f"manuscript {section} hash mismatch: {expected_path}")
        if entry.get("bytes") != path.stat().st_size:
            mismatches.append(f"manuscript {section} byte-count mismatch: {expected_path}")
    return mismatches

def version_mismatches(certificate: dict[str, Any]) -> list[str]:
    """Require VERSION, pyproject, and proof certificate to agree exactly."""

    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_version = str(pyproject["project"]["version"])
    certificate_version = str(certificate.get("project_version", ""))
    config = json.loads((REPO_ROOT / "config" / "ash_mapping_v1.json").read_text(encoding="utf-8"))
    config_version = str(config.get("project_version", ""))
    init_text = (REPO_ROOT / "src" / "ash_model" / "__init__.py").read_text(encoding="utf-8")
    init_match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', init_text, re.MULTILINE)
    init_version = init_match.group(1) if init_match else ""
    citation_text = (REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8")
    citation_match = re.search(r'^version:\s*["\']?([^"\'\n]+)', citation_text, re.MULTILINE)
    citation_version = citation_match.group(1).strip() if citation_match else ""
    values = {
        "VERSION": version,
        "pyproject": package_version,
        "package": init_version,
        "config": config_version,
        "CITATION.cff": citation_version,
        "certificate": certificate_version,
    }
    if len(set(values.values())) == 1:
        return []
    return ["version mismatch: " + ", ".join(f"{key}={value!r}" for key, value in values.items())]


def verification_report() -> dict[str, Any]:
    violations = scan_claims()
    missing = [name for name in REQUIRED_ARTIFACTS if not (REPO_ROOT / name).is_file()]
    artifact_mismatches = verify_artifact_manifest()
    manuscript_mismatches = verify_manuscript_manifest()

    certificate_path = REPO_ROOT / "proofs" / "computational-certificate.json"
    certificate: dict[str, Any] = {}
    certificate_valid = False
    source_mismatches = ["missing proofs/computational-certificate.json"]
    versions = ["proof certificate unavailable for version comparison"]
    if certificate_path.is_file():
        certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
        certificate_valid = certificate.get("all_checks_pass") is True
        expected_sources = certificate.get("source_sha256")
        if isinstance(expected_sources, dict) and all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in expected_sources.items()
        ):
            source_mismatches = compare_manifests(expected_sources, current_source_manifest())
        else:
            source_mismatches = ["proof certificate has no valid source_sha256 manifest"]
        versions = version_mismatches(certificate)

    return {
        "claim_violations": violations,
        "missing_artifacts": missing,
        "artifact_manifest_mismatches": artifact_mismatches,
        "manuscript_manifest_mismatches": manuscript_mismatches,
        "source_manifest_mismatches": source_mismatches,
        "version_mismatches": versions,
        "proof_certificate_passes": certificate_valid,
    }


def main() -> int:
    report = verification_report()
    print(json.dumps(report, indent=2))
    passes = (
        not report["claim_violations"]
        and not report["missing_artifacts"]
        and not report["artifact_manifest_mismatches"]
        and not report["manuscript_manifest_mismatches"]
        and not report["source_manifest_mismatches"]
        and not report["version_mismatches"]
        and report["proof_certificate_passes"] is True
    )
    return 0 if passes else 1


if __name__ == "__main__":
    raise SystemExit(main())
