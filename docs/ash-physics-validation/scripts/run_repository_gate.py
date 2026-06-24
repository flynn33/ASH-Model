#!/usr/bin/env python3
"""Repository-level validation gate for ASH planning assets."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ash_model.prediction_ledger import validate_prediction_ledger as validate_prediction_locks


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(schema_path: Path, instance_path: Path) -> list[str]:
    schema_name = schema_path.name
    instance = load_json(instance_path)
    if schema_name == "prediction_ledger.schema.json":
        return validate_prediction_ledger(instance_path, instance)
    if schema_name == "validation_status.schema.json":
        return validate_validation_status(instance_path, instance)
    if schema_name == "task_manifest.schema.json":
        return validate_task_manifest(instance_path, instance)
    if schema_name == "science_manifest.schema.json":
        return validate_science_manifest(instance_path, instance)
    return [f"unsupported schema: {schema_path}"]


def _require_object(path: Path, value, label: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path}: {label}: expected object"]
    return []


def _require_string(path: Path, value, label: str) -> list[str]:
    if not isinstance(value, str):
        return [f"{path}: {label}: expected string"]
    return []


def _require_array(path: Path, value, label: str) -> list[str]:
    if not isinstance(value, list):
        return [f"{path}: {label}: expected array"]
    return []


def validate_prediction_ledger(path: Path, payload) -> list[str]:
    failures = _require_object(path, payload, "<root>")
    if failures:
        return failures
    allowed_keys = {"schema_version", "model_version", "status", "entries"}
    required = allowed_keys
    failures.extend(f"{path}: <root>: missing required property {key}" for key in sorted(required - set(payload)))
    failures.extend(f"{path}: <root>: unexpected property {key}" for key in sorted(set(payload) - allowed_keys))
    for key in ("schema_version", "model_version", "status"):
        if key in payload:
            failures.extend(_require_string(path, payload[key], key))
    statuses = {"no_locked_predictions", "has_locked_predictions", "testing_in_progress", "archived"}
    if isinstance(payload.get("status"), str) and payload["status"] not in statuses:
        failures.append(f"{path}: status: unsupported value {payload['status']!r}")
    if "entries" in payload:
        failures.extend(_require_array(path, payload["entries"], "entries"))
    if payload.get("status") == "no_locked_predictions" and isinstance(payload.get("entries"), list) and payload["entries"]:
        failures.append(f"{path}: entries: must be empty when status is no_locked_predictions")
    entry_required = {
        "id",
        "model_version",
        "commit",
        "frozen_utc",
        "observable",
        "prediction",
        "uncertainty",
        "data_product",
        "statistic",
        "rejection_rule",
        "test_status",
    }
    entry_allowed = entry_required | {"artifact_hashes", "entry_hash", "notes"}
    entry_statuses = {"frozen", "tested_pass", "tested_fail", "withdrawn_before_test"}
    for index, entry in enumerate(payload.get("entries", []) if isinstance(payload.get("entries"), list) else []):
        label = f"entries/{index}"
        failures.extend(_require_object(path, entry, label))
        if not isinstance(entry, dict):
            continue
        failures.extend(f"{path}: {label}: missing required property {key}" for key in sorted(entry_required - set(entry)))
        failures.extend(f"{path}: {label}: unexpected property {key}" for key in sorted(set(entry) - entry_allowed))
        if isinstance(entry.get("test_status"), str) and entry["test_status"] not in entry_statuses:
            failures.append(f"{path}: {label}/test_status: unsupported value {entry['test_status']!r}")
    failures.extend(f"{path}: {failure}" for failure in validate_prediction_locks(payload))
    return failures


def validate_task_manifest(path: Path, payload) -> list[str]:
    failures = _require_object(path, payload, "<root>")
    if failures:
        return failures
    for key in ("schema_version", "tasks"):
        if key not in payload:
            failures.append(f"{path}: <root>: missing required property {key}")
    if "schema_version" in payload:
        failures.extend(_require_string(path, payload["schema_version"], "schema_version"))
    if "tasks" in payload:
        failures.extend(_require_array(path, payload["tasks"], "tasks"))
    statuses = {"complete", "blocked", "deferred", "open"}
    for index, task in enumerate(payload.get("tasks", []) if isinstance(payload.get("tasks"), list) else []):
        label = f"tasks/{index}"
        failures.extend(_require_object(path, task, label))
        if not isinstance(task, dict):
            continue
        for key in ("id", "title", "status"):
            if key not in task:
                failures.append(f"{path}: {label}: missing required property {key}")
        if isinstance(task.get("status"), str) and task["status"] not in statuses:
            failures.append(f"{path}: {label}/status: unsupported value {task['status']!r}")
        for key in ("required_paths", "evidence"):
            if key in task:
                failures.extend(_require_array(path, task[key], f"{label}/{key}"))
    return failures


def validate_science_manifest(path: Path, payload) -> list[str]:
    failures = _require_object(path, payload, "<root>")
    if failures:
        return failures
    for key in ("schema_version", "manifest_type", "rules", "items"):
        if key not in payload:
            failures.append(f"{path}: <root>: missing required property {key}")
    if "schema_version" in payload:
        failures.extend(_require_string(path, payload["schema_version"], "schema_version"))
    if payload.get("manifest_type") != "science_status":
        failures.append(f"{path}: manifest_type: expected science_status")
    failures.extend(_require_object(path, payload.get("rules"), "rules"))
    if isinstance(payload.get("rules"), dict):
        if payload["rules"].get("placeholder_files_do_not_count_as_complete") is not True:
            failures.append(f"{path}: rules/placeholder_files_do_not_count_as_complete: expected true")
        failures.extend(_require_array(path, payload["rules"].get("scientific_complete_requires"), "rules/scientific_complete_requires"))
    failures.extend(_require_array(path, payload.get("items"), "items"))
    completion_types = {"blocked", "scientific_definition", "implementation", "validation"}
    statuses = {"open", "complete"}
    for index, item in enumerate(payload.get("items", []) if isinstance(payload.get("items"), list) else []):
        label = f"items/{index}"
        failures.extend(_require_object(path, item, label))
        if not isinstance(item, dict):
            continue
        for key in ("id", "status", "completion_type", "required_evidence"):
            if key not in item:
                failures.append(f"{path}: {label}: missing required property {key}")
        if isinstance(item.get("status"), str) and item["status"] not in statuses:
            failures.append(f"{path}: {label}/status: unsupported value {item['status']!r}")
        if isinstance(item.get("completion_type"), str) and item["completion_type"] not in completion_types:
            failures.append(f"{path}: {label}/completion_type: unsupported value {item['completion_type']!r}")
        if item.get("status") == "open" and item.get("completion_type") != "blocked":
            failures.append(f"{path}: {label}: open science items must use blocked completion_type")
        if "required_evidence" in item:
            failures.extend(_require_array(path, item["required_evidence"], f"{label}/required_evidence"))
    return failures


def validate_validation_status(path: Path, payload) -> list[str]:
    failures = _require_object(path, payload, "<root>")
    if failures:
        return failures
    allowed_keys = {
        "schema_version",
        "model_version",
        "commit",
        "updated_utc",
        "tasks",
        "verification_commands",
        "open_blockers",
        "claim_downgrades",
    }
    required = {"schema_version", "model_version", "updated_utc", "tasks", "verification_commands", "open_blockers"}
    failures.extend(f"{path}: <root>: missing required property {key}" for key in sorted(required - set(payload)))
    failures.extend(f"{path}: <root>: unexpected property {key}" for key in sorted(set(payload) - allowed_keys))
    for key in ("schema_version", "model_version", "commit", "updated_utc"):
        if key in payload:
            failures.extend(_require_string(path, payload[key], key))
    for key in ("tasks", "verification_commands", "open_blockers", "claim_downgrades"):
        if key in payload:
            failures.extend(_require_array(path, payload[key], key))
    statuses = {"complete", "blocked", "deferred"}
    completion_types = {
        "scaffold_created",
        "theorem_proved",
        "implementation_verified",
        "empirical_gate_passed",
        "blocked_scientific_work",
    }
    for index, task in enumerate(payload.get("tasks", []) if isinstance(payload.get("tasks"), list) else []):
        label = f"tasks/{index}"
        failures.extend(_require_object(path, task, label))
        if not isinstance(task, dict):
            continue
        allowed_task_keys = {"id", "status", "completion_type", "evidence", "notes"}
        failures.extend(f"{path}: {label}: unexpected property {key}" for key in sorted(set(task) - allowed_task_keys))
        for key in ("id", "status", "completion_type", "evidence"):
            if key not in task:
                failures.append(f"{path}: {label}: missing required property {key}")
        if isinstance(task.get("status"), str) and task["status"] not in statuses:
            failures.append(f"{path}: {label}/status: unsupported value {task['status']!r}")
        if isinstance(task.get("completion_type"), str) and task["completion_type"] not in completion_types:
            failures.append(f"{path}: {label}/completion_type: unsupported value {task['completion_type']!r}")
        if "evidence" in task:
            failures.extend(_require_array(path, task["evidence"], f"{label}/evidence"))
    command_results = {"passed", "failed", "blocked", "not_run"}
    for index, command in enumerate(payload.get("verification_commands", []) if isinstance(payload.get("verification_commands"), list) else []):
        label = f"verification_commands/{index}"
        failures.extend(_require_object(path, command, label))
        if not isinstance(command, dict):
            continue
        allowed_command_keys = {"command", "result", "summary"}
        failures.extend(f"{path}: {label}: unexpected property {key}" for key in sorted(set(command) - allowed_command_keys))
        for key in ("command", "result", "summary"):
            if key not in command:
                failures.append(f"{path}: {label}: missing required property {key}")
        if isinstance(command.get("result"), str) and command["result"] not in command_results:
            failures.append(f"{path}: {label}/result: unsupported value {command['result']!r}")
    return failures


def require_path(root: Path, relative: str) -> list[str]:
    path = root / relative
    if not path.exists():
        return [f"missing required path: {relative}"]
    return []


def check_task_status_consistency(root: Path) -> list[str]:
    task_path = root / "docs/ash-physics-validation/tasks/task_manifest.json"
    status_path = root / "validation/status.json"
    if not task_path.exists() or not status_path.exists():
        return []
    task_payload = load_json(task_path)
    status_payload = load_json(status_path)
    task_ids = {task["id"] for task in task_payload.get("tasks", [])}
    status_ids = {task["id"] for task in status_payload.get("tasks", [])}
    messages = []
    missing_status = sorted(task_ids - status_ids)
    extra_status = sorted(status_ids - task_ids)
    if missing_status:
        messages.append(f"validation/status.json missing task ids: {', '.join(missing_status)}")
    if extra_status:
        messages.append(f"validation/status.json has ids not in task manifest: {', '.join(extra_status)}")
    for task in status_payload.get("tasks", []):
        if "completion_type" not in task:
            messages.append(f"validation/status.json task {task.get('id')} lacks completion_type")
        for evidence in task.get("evidence", []):
            if evidence and not (root / evidence).exists():
                messages.append(f"validation/status.json task {task.get('id')} evidence path does not exist: {evidence}")
    return messages


def check_readme_references(root: Path) -> list[str]:
    messages = []
    readme = root / "docs/ash-physics-validation/README.md"
    if readme.exists() and "IMPLEMENTATION_INSTRUCTIONS.md" in readme.read_text(encoding="utf-8"):
        messages.extend(require_path(root, "docs/ash-physics-validation/IMPLEMENTATION_INSTRUCTIONS.md"))
    return messages


def check_live_repository_readiness(root: Path) -> list[str]:
    script = root / "tools/audit_live_repository_readiness.py"
    if not script.exists():
        return ["missing required path: tools/audit_live_repository_readiness.py"]
    result = subprocess.run(
        [sys.executable, str(script), str(root)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    output = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)
    return [f"live repository readiness audit failed: {output or result.returncode}"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    failures: list[str] = []

    required = [
        "docs/ash-physics-validation/README.md",
        "docs/ash-physics-validation/IMPLEMENTATION_INSTRUCTIONS.md",
        "docs/ash-physics-validation/tasks/task_manifest.json",
        "docs/ash-physics-validation/tasks/science_manifest.json",
        "docs/ash-physics-validation/configs/prediction_ledger.schema.json",
        "docs/ash-physics-validation/configs/validation_status.schema.json",
        "docs/ash-physics-validation/configs/task_manifest.schema.json",
        "docs/ash-physics-validation/configs/science_manifest.schema.json",
        "docs/ash-physics-validation/configs/proof_certificate.schema.json",
        "predictions/prediction-ledger.json",
        "validation/status.json",
    ]
    for relative in required:
        failures.extend(require_path(root, relative))

    schema_pairs = [
        ("docs/ash-physics-validation/configs/prediction_ledger.schema.json", "predictions/prediction-ledger.json"),
        ("docs/ash-physics-validation/configs/validation_status.schema.json", "validation/status.json"),
        ("docs/ash-physics-validation/configs/task_manifest.schema.json", "docs/ash-physics-validation/tasks/task_manifest.json"),
        ("docs/ash-physics-validation/configs/science_manifest.schema.json", "docs/ash-physics-validation/tasks/science_manifest.json"),
    ]
    for schema_rel, instance_rel in schema_pairs:
        schema_path = root / schema_rel
        instance_path = root / instance_rel
        if schema_path.exists() and instance_path.exists():
            failures.extend(validate(schema_path, instance_path))

    failures.extend(check_task_status_consistency(root))
    failures.extend(check_readme_references(root))
    failures.extend(check_live_repository_readiness(root))

    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("repository gate passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
