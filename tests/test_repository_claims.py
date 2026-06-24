from pathlib import Path


def test_repository_has_no_forbidden_attribution_or_unqualified_self_dual_claim():
    root = Path(__file__).resolve().parents[1]
    forbidden = (
        "doubly-even self-dual error-correcting codes within a 9-dimensional",
    )
    suffixes = {".md", ".py", ".tex", ".json", ".yml", ".yaml", ".toml"}
    hits = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in forbidden:
            if phrase in text:
                hits.append((str(path.relative_to(root)), phrase))
    assert not hits
