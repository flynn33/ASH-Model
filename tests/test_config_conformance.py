import json
from pathlib import Path

from ash_model.branching import (
    ACTION_ORDER,
    DEFAULT_ACTION_WEIGHTS,
    DEFAULT_BRANCH_DEPTH,
    DEFAULT_LENGTH_DECAY,
    DEFAULT_TURN_DEGREES,
    GEOMETRY_RULE,
)
from ash_model.code import (
    GENERATOR_MATRIX,
    INVARIANT_COORDINATE,
    PARITY_COORDINATE,
    TRANSFORM_MASKS,
    code_certificate,
)
from ash_model.features import DEFAULT_HYSTERESIS, DEFAULT_THRESHOLDS, FEATURE_NAMES
from ash_model.reconstruction import (
    DEFAULT_DATA_WEIGHT,
    DEFAULT_EDGE_WEIGHT,
    DEFAULT_OPERATOR_STRENGTH,
    DEFAULT_SCALE,
    DEFAULT_TEMPORAL_WEIGHT,
    DEFAULT_TOP_K,
)


def _bit_strings(rows):
    return ["".join(str(bit) for bit in row) for row in rows]


def test_normative_mapping_config_matches_executable_constants():
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / "config" / "ash_mapping_v1.json").read_text(encoding="utf-8"))
    assert config["project_version"] == (root / "VERSION").read_text().strip()
    assert config["bit_order"] == "coordinate_1_is_most_significant"
    assert config["state_space"] == "F_2^9"

    measured = config["coordinates"][:8]
    assert [entry["index"] for entry in measured] == list(range(1, 9))
    assert [entry["name"] for entry in measured] == list(FEATURE_NAMES)
    assert tuple(entry["threshold"] for entry in measured) == DEFAULT_THRESHOLDS
    assert tuple(entry["hysteresis"] for entry in measured) == DEFAULT_HYSTERESIS
    assert config["coordinates"][8]["index"] == 9
    assert config["coordinates"][8]["name"] == "parity_integrity"

    certificate = code_certificate()
    code = config["code"]
    assert code["parameters"] == [certificate["length"], certificate["rank"], certificate["minimum_distance"]]
    assert code["doubly_even"] is certificate["doubly_even"]
    assert code["self_dual_in_f2_9"] is certificate["self_dual_in_f2_9"]
    assert code["coordinate_8_invariant_under_code"] is certificate["coordinate_8_invariant"]
    assert code["coordinate_9_active"] is certificate["coordinate_9_active"]
    assert code["generator_matrix"] == _bit_strings(GENERATOR_MATRIX)
    assert code["transform_masks"] == _bit_strings(TRANSFORM_MASKS)
    assert code["invariant_coordinate"] == INVARIANT_COORDINATE + 1
    assert code["parity_coordinate"] == PARITY_COORDINATE + 1
    assert code["decoder_radius"] == 1

    branching = config["branching"]
    assert branching["actions"] == list(ACTION_ORDER)
    assert branching["weights"] == DEFAULT_ACTION_WEIGHTS
    assert branching["default_depth"] == DEFAULT_BRANCH_DEPTH
    assert branching["turn_degrees"] == DEFAULT_TURN_DEGREES
    assert branching["length_decay"] == DEFAULT_LENGTH_DECAY
    assert branching["geometry_rule"] == f"F -> {GEOMETRY_RULE}"

    reconstruction = config["reconstruction"]
    assert reconstruction["default_scale"] == DEFAULT_SCALE
    assert reconstruction["default_top_k"] == DEFAULT_TOP_K
    assert reconstruction["operator_strength"] == DEFAULT_OPERATOR_STRENGTH
    assert reconstruction["scoring_weights"] == {
        "data": DEFAULT_DATA_WEIGHT,
        "edge": DEFAULT_EDGE_WEIGHT,
        "temporal": DEFAULT_TEMPORAL_WEIGHT,
    }
    assert reconstruction["silent_recovery_beyond_one_bit"] is False
