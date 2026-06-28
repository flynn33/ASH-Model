from pathlib import Path

from ash_model.branch_centered_closure import (
    REQUIRED_COMPONENT_SYMBOLS,
    branch_centered_model_card,
    load_component_matrix,
    load_falsification_matrix,
    verify_branch_centered_closure,
)


ROOT = Path(__file__).resolve().parents[1]


def test_required_components_present():
    result = verify_branch_centered_closure(ROOT)
    assert result["missing_components"] == []
    assert result["component_count"] == len(REQUIRED_COMPONENT_SYMBOLS)


def test_falsification_gates_present():
    result = verify_branch_centered_closure(ROOT)
    assert result["missing_falsification_gates"] == []
    gates = load_falsification_matrix(ROOT)
    assert len(gates) >= 5
    assert all(row["failure_action"] for row in gates)


def test_boundary_is_explicitly_non_empirical():
    result = verify_branch_centered_closure(ROOT)
    assert result["non_empirical_boundary"]
    assert result["external_empirical_status"] == "not empirically validated"
    assert result["closed_formal_candidate"]


def test_upstream_hashes_recorded_for_r009_through_r015():
    result = verify_branch_centered_closure(ROOT)
    assert result["missing_upstream_hashes"] == []
    assert result["upstream_hashes_recorded"] == [
        "R009",
        "R010",
        "R011",
        "R012",
        "R013",
        "R014",
        "R015",
    ]


def test_component_layers_are_populated():
    rows = load_component_matrix(ROOT)
    assert all(row["layer"] for row in rows)
    assert {row["symbol"] for row in rows} >= set(REQUIRED_COMPONENT_SYMBOLS)


def test_model_card_contains_synthetic_observables():
    card = branch_centered_model_card(ROOT)
    obs = card["synthetic_closure_observables"]
    assert obs["max_delta_H_over_H"] > 0
    assert obs["matter_template_dynamic_range"] > 0
    assert obs["lowell_template_dynamic_range"] > 0
    assert "not empirically validated" in card["scientific_status"]
