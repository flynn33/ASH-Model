import json
import subprocess
import sys
from pathlib import Path


def test_data_manifest_validator_accepts_tracked_assets():
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [
            sys.executable,
            "tools/validate_data_manifest.py",
            "--manifest",
            "data/manifests/data_manifest.json",
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)
    assert completed.returncode == 0, report
    assert report["asset_count"] > 0
    assert report["failures"] == []
