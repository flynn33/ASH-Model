from itertools import combinations
from pathlib import Path

import pytest

from tools import run_simulation_controls

from src.ash_code import (
    CANONICAL_CODEWORDS,
    CANONICAL_GENERATORS,
    CODE_DIMENSION,
    DIM,
    MIN_DISTANCE,
    PARITY_INDEX,
    coordinate_9_matches_parity,
    decode,
    gf2_rank,
    hamming_distance,
    is_doubly_even,
    minimum_distance,
    normalize_vector,
    validate_canonical_code,
    weight_distribution,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def flip_bit(vector, index):
    out = list(vector)
    out[index] ^= 1
    return tuple(out)


def test_code_has_dimension_and_rank():
    assert DIM == 9
    assert CODE_DIMENSION == 4
    assert gf2_rank(CANONICAL_GENERATORS) == 4


def test_code_span_size_is_16():
    assert len(CANONICAL_CODEWORDS) == 16


def test_code_is_doubly_even():
    assert all(is_doubly_even(word) for word in CANONICAL_CODEWORDS)


def test_weight_distribution():
    assert weight_distribution() == {0: 1, 4: 14, 8: 1}


def test_minimum_distance_is_4():
    assert minimum_distance() == MIN_DISTANCE == 4


def test_coordinate_9_is_parity_bit():
    assert all(coordinate_9_matches_parity(word) for word in CANONICAL_CODEWORDS)


def test_coordinate_9_is_active():
    values = {word[PARITY_INDEX] for word in CANONICAL_CODEWORDS}
    assert values == {0, 1}


def test_coordinate_8_reserved_in_canonical_presentation():
    assert all(word[7] == 0 for word in CANONICAL_CODEWORDS)


def test_decode_valid_codewords():
    for word in CANONICAL_CODEWORDS:
        result = decode(word)
        assert result.status == "valid"
        assert result.corrected == word
        assert result.distance == 0


def test_decoder_corrects_all_single_bit_errors():
    for word in CANONICAL_CODEWORDS:
        for index in range(DIM):
            received = flip_bit(word, index)
            result = decode(received)
            assert result.status == "corrected"
            assert result.corrected == word
            assert result.distance == 1


def test_decoder_refuses_double_bit_errors_by_default():
    for word in CANONICAL_CODEWORDS:
        for i, j in combinations(range(DIM), 2):
            received = flip_bit(flip_bit(word, i), j)
            result = decode(received)
            assert result.status in {"uncorrectable", "ambiguous"}
            assert result.corrected is None
            assert result.distance is None or result.distance >= 2


def test_decoder_rejects_invalid_vectors():
    with pytest.raises(ValueError):
        normalize_vector((0, 1))
    with pytest.raises(ValueError):
        normalize_vector((0, 1, 0, 1, 0, 1, 0, 1, 2))


def test_code_is_not_self_dual():
    props = validate_canonical_code()
    assert props["self_dual"] is False
    assert props["rank"] * 2 != props["length"]


def test_pairwise_distances_are_at_least_min_distance():
    for a, b in combinations(CANONICAL_CODEWORDS, 2):
        assert hamming_distance(a, b) >= MIN_DISTANCE


def test_validate_canonical_code_summary():
    props = validate_canonical_code()
    assert props["length"] == 9
    assert props["rank"] == 4
    assert props["span_size"] == 16
    assert props["minimum_distance"] == 4
    assert props["weight_distribution"] == {0: 1, 4: 14, 8: 1}
    assert props["doubly_even"] is True
    assert props["coordinate_9_active"] is True
    assert props["coordinate_9_parity_valid"] is True


def test_simulation_controls_use_package_artifact_path():
    rel_path = run_simulation_controls.OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()
    assert rel_path == "data/simulation-controls.json"


def test_required_skir_package_artifacts_exist():
    required = [
        "tools/verify_branch.py",
        "docs/skir-code-validation.md",
        "reports/skir-completion-report.md",
        "scripts/local_precheck.sh",
        "scripts/final_gate.sh",
    ]
    missing = [path for path in required if not (REPO_ROOT / path).exists()]
    assert missing == []


def test_base_docs_exclude_narrative_coordinate_terms():
    terms = [
        "".join(["W", "R", "W"]),
        " ".join(["Divine", "Core"]),
        " ".join(["Void", "Realm"]),
    ]
    allowed = {
        "docs/claim-language-policy.md",
    }
    paths = [REPO_ROOT / "README.md"]
    for root in [REPO_ROOT / "docs", REPO_ROOT / "wiki"]:
        paths.extend(path for path in root.rglob("*.md") if path.is_file())
    paths.extend(path for path in (REPO_ROOT / "latex").rglob("*.tex"))

    violations = []
    for path in paths:
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel in allowed:
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            if term in text:
                violations.append(f"{rel}: contains {term}")

    assert violations == []
