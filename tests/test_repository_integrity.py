import json
import subprocess
import sys
from pathlib import Path


def test_repository_verifier_accepts_current_tracked_evidence():
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, "tools/verify_repository.py"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)
    assert completed.returncode == 0, report
