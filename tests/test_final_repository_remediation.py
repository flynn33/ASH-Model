import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]


def _load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _load_tool(name: str):
    path = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_proof_certificate_schema_validates_live_certificate():
    schema = _load_json("docs/ash-physics-validation/configs/proof_certificate.schema.json")
    certificate = _load_json("proofs/computational-certificate.json")

    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(certificate, schema)


def test_final_remediation_tools_are_present_and_importable():
    for name in (
        "validate_json_assets",
        "check_generated_outputs",
        "audit_physics_readiness",
        "audit_live_repository_readiness",
        "final_repository_audit",
    ):
        _load_tool(name)


def test_science_manifest_keeps_science_blockers_separate_from_scaffolds():
    manifest = _load_json("docs/ash-physics-validation/tasks/science_manifest.json")

    assert manifest["manifest_type"] == "science_status"
    assert manifest["rules"]["placeholder_files_do_not_count_as_complete"] is True
    assert all(item["completion_type"] != "validation" for item in manifest["items"])
    assert any(item["id"] == "locked_prediction" and item["status"] == "open" for item in manifest["items"])


def test_manuscript_manifest_declares_source_input_equivalence_policy():
    manifest = _load_json("proofs/manuscript-manifest.json")
    input_paths = {item["path"] for item in manifest["source_inputs"]}

    assert manifest["verification_policy"] == "source_input_equivalence"
    assert "latex/main.tex" in input_paths
    assert "docs/ASH-Model-Preprint-v1.pdf" in input_paths
    assert "figures/hypercube-3d-projection.png" in input_paths


def test_manuscript_manifest_uses_only_tracked_figure_inputs():
    manifest = _load_json("proofs/manuscript-manifest.json")
    figure_inputs = {
        item["path"]
        for item in manifest["source_inputs"]
        if item["path"].startswith("figures/")
    }
    tracked_figures = set(
        subprocess.check_output(
            ["git", "ls-files", "figures/*.png"],
            cwd=ROOT,
            text=True,
        ).splitlines()
    )

    assert figure_inputs <= tracked_figures


def test_repository_verifier_accepts_source_input_manuscript_policy():
    verifier = _load_tool("verify_repository")

    assert verifier.verify_manuscript_manifest() == []


def test_generated_remediation_evidence_is_not_normative_source_manifest():
    proof_suite = _load_tool("run_proof_suite")
    source_manifest = proof_suite._source_manifest()

    assert "docs/remediation/physics-readiness.json" not in source_manifest
    assert "docs/remediation/final-remediation-evidence.json" not in source_manifest


def test_physics_readiness_gate_modes_report_open_science_blockers():
    expect_open = subprocess.run(
        [
            sys.executable,
            "tools/audit_physics_readiness.py",
            ".",
            "--expect-open",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    require_ready = subprocess.run(
        [
            sys.executable,
            "tools/audit_physics_readiness.py",
            ".",
            "--require-ready",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert expect_open.returncode == 0
    expect_payload = json.loads(expect_open.stdout)
    manifest = _load_json("docs/ash-physics-validation/tasks/science_manifest.json")
    open_science_items = [item for item in manifest["items"] if item["status"] == "open"]

    assert expect_payload["ready"] is False
    assert expect_payload["blocker_count"] == len(open_science_items)
    assert require_ready.returncode == 1


def test_live_repository_readiness_audit_passes_with_open_science_blockers():
    audit = subprocess.run(
        [
            sys.executable,
            "tools/audit_live_repository_readiness.py",
            ".",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "live repository readiness audit passed" in audit.stdout
