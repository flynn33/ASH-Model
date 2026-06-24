#!/usr/bin/env python3
"""Audit whether ASH-Physics is ready for empirical cosmology.

Repository remediation should usually run this in --expect-open mode. That mode
passes only when open scientific blockers are honestly recorded. The --require-ready
mode is for the later science phase and fails until the theory is actually complete.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_ITEMS = [
    {
        "id": "ontology",
        "label": "physical state ontology",
        "paths": ["theory/physical-postulates.md"],
        "required_terms": ["state", "physical", "unit", "domain", "codomain"],
    },
    {
        "id": "dynamics",
        "label": "microscopic dynamics",
        "paths": ["theory/microscopic-state-and-dynamics.md"],
        "required_terms": ["dynamics", "update", "transition", "equation"],
    },
    {
        "id": "causal_structure",
        "label": "causal structure or explicit nonlocality",
        "paths": ["theory/causal-structure.md"],
        "required_terms": ["causal", "local", "propagation"],
    },
    {
        "id": "bridge_map",
        "label": "bridge map to physical observables",
        "paths": ["theory/coarse-graining-and-bridge-map.md"],
        "required_terms": ["bridge", "observable", "map", "unit"],
    },
    {
        "id": "continuum_or_observer_limit",
        "label": "continuum limit or finite-observer substitute",
        "paths": ["theory/continuum-limit.md"],
        "required_terms": ["limit", "scale", "convergence"],
    },
    {
        "id": "background_equations",
        "label": "cosmological background equations",
        "paths": ["theory/cosmological-background.md", "phenomenology/ash_background_spec.md"],
        "required_terms": ["H", "scale", "equation"],
    },
    {
        "id": "perturbations",
        "label": "perturbation equations or alternate observable evolution",
        "paths": ["theory/linear-perturbations.md", "phenomenology/ash_perturbations_spec.md"],
        "required_terms": ["perturb", "equation", "stability"],
    },
    {
        "id": "solver",
        "label": "executable cosmology solver",
        "paths": ["phenomenology"],
        "required_terms": ["solver"],
    },
    {
        "id": "synthetic_recovery",
        "label": "synthetic recovery",
        "paths": ["validation/synthetic-recovery"],
        "required_terms": ["synthetic", "recovery"],
    },
    {
        "id": "matched_ablations",
        "label": "matched ablations",
        "paths": ["validation/matched-ablations"],
        "required_terms": ["ablation", "matched"],
    },
    {
        "id": "baseline_limit",
        "label": "baseline limit or justified alternative",
        "paths": ["validation/lcdm-limit"],
        "required_terms": ["baseline", "limit"],
    },
    {
        "id": "locked_prediction",
        "label": "locked empirical prediction",
        "paths": ["predictions/prediction-ledger.json"],
        "required_terms": ["entries"],
    },
]

BLOCKER_PATTERNS = [
    re.compile(r"\bblocked\b", re.IGNORECASE),
    re.compile(r"\bnot\s+defined\b", re.IGNORECASE),
    re.compile(r"\bnot\s+derived\b", re.IGNORECASE),
    re.compile(r"\bno\s+locked\s+prediction", re.IGNORECASE),
    re.compile(r"\bplaceholder\b", re.IGNORECASE),
    re.compile(r"\btemplate\b", re.IGNORECASE),
]

COMPLETION_PATTERNS = [
    re.compile(r"\bcomplete\b", re.IGNORECASE),
    re.compile(r"\bvalidated\b", re.IGNORECASE),
    re.compile(r"\bderived\b", re.IGNORECASE),
    re.compile(r"\bimplemented\b", re.IGNORECASE),
]

SCIENCE_MANIFEST = Path("docs/ash-physics-validation/tasks/science_manifest.json")


def read_path(root: Path, rel: str) -> str:
    path = root / rel
    if not path.exists():
        return ""
    if path.is_dir():
        texts = []
        for file in sorted(path.rglob("*")):
            if file.is_file() and file.suffix.lower() in {".md", ".json", ".py", ".txt", ".tex", ".yaml", ".yml"}:
                try:
                    texts.append(file.read_text(encoding="utf-8", errors="replace"))
                except Exception:
                    pass
        return "\n".join(texts)
    return path.read_text(encoding="utf-8", errors="replace")


def load_science_items(root: Path) -> list[dict[str, Any]]:
    """Load the explicit science-readiness manifest when present."""

    manifest_path = root / SCIENCE_MANIFEST
    if not manifest_path.is_file():
        return REQUIRED_ITEMS
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = payload.get("items")
    if not isinstance(items, list):
        return REQUIRED_ITEMS
    return [item for item in items if isinstance(item, dict)]


def item_status(root: Path, item: dict[str, Any]) -> dict[str, Any]:
    paths = item.get("required_evidence", item.get("paths", []))
    required_terms = item.get("required_terms", [])
    if not isinstance(paths, list):
        paths = []
    if not isinstance(required_terms, list):
        required_terms = []

    text = "\n".join(read_path(root, rel) for rel in paths if isinstance(rel, str))
    exists = any((root / rel).exists() for rel in paths if isinstance(rel, str))
    all_evidence_exists = all((root / rel).exists() for rel in paths if isinstance(rel, str))
    has_terms = all(str(term).lower() in text.lower() for term in required_terms)
    has_blocker = any(pattern.search(text) for pattern in BLOCKER_PATTERNS)
    has_completion_language = any(pattern.search(text) for pattern in COMPLETION_PATTERNS)
    status = item.get("status")
    completion_type = item.get("completion_type")
    manifest_ready = status == "complete" and completion_type != "blocked"

    # Locked prediction requires at least one ledger entry, not just an entries field.
    if item.get("id") == "locked_prediction":
        ledger_path = root / "predictions/prediction-ledger.json"
        entry_count = 0
        if ledger_path.exists():
            try:
                ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
                entry_count = len(ledger.get("entries", []))
            except Exception:
                pass
        ready = manifest_ready and all_evidence_exists and entry_count > 0 and not has_blocker
        return {
            **item,
            "paths": paths,
            "exists": exists,
            "all_evidence_exists": all_evidence_exists,
            "has_required_terms": has_terms,
            "has_blocker_language": has_blocker,
            "has_completion_language": has_completion_language,
            "entry_count": entry_count,
            "ready": ready,
        }

    ready = manifest_ready and all_evidence_exists and not has_blocker
    return {
        **item,
        "paths": paths,
        "exists": exists,
        "all_evidence_exists": all_evidence_exists,
        "has_required_terms": has_terms,
        "has_blocker_language": has_blocker,
        "has_completion_language": has_completion_language,
        "ready": ready,
    }


def item_label(item: dict[str, Any]) -> str:
    label = item.get("label")
    if isinstance(label, str):
        return label
    identifier = item.get("id")
    if isinstance(identifier, str):
        return identifier.replace("_", " ")
    return "unnamed science item"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--expect-open", action="store_true", help="Pass if blockers are honestly open.")
    parser.add_argument("--require-ready", action="store_true", help="Fail unless all science-readiness items are ready.")
    parser.add_argument("--write-json", default=None)
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    statuses = [item_status(root, item) for item in load_science_items(root)]
    blockers = [item for item in statuses if not item["ready"]]
    ready = not blockers

    results = {
        "root": str(root),
        "ready": ready,
        "science_manifest": str(SCIENCE_MANIFEST),
        "mode": "require-ready" if args.require_ready else "expect-open" if args.expect_open else "status-only",
        "items": statuses,
        "blocker_count": len(blockers),
        "blockers": [{"id": item.get("id"), "label": item_label(item)} for item in blockers],
    }

    text = json.dumps(results, indent=2, sort_keys=True)
    print(text)
    if args.write_json:
        out = root / args.write_json
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")

    if args.require_ready:
        return 0 if ready else 1
    if args.expect_open:
        # Repository remediation is allowed to pass only when blockers are explicitly reported.
        return 0 if not ready and blockers else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
