from __future__ import annotations

from math import isclose

import pytest

from ash_model.branch_measure import (
    BranchChild,
    BranchMeasureConfig,
    allocate_branch_measure,
    demo_branch_frontier,
    effective_action,
    frontier_entropy,
    law_summary,
    shell_demo_children,
    transfer_penalty,
    verify_branch_measure,
)


def test_transfer_penalty_uses_finite_shells() -> None:
    penalties = [transfer_penalty(q, 0.05) for q in range(5)]
    assert penalties[0] == 0.0
    assert all(value >= 0.0 for value in penalties)
    assert penalties[-1] > penalties[0]


def test_allocate_branch_measure_normalizes_sibling_set() -> None:
    children = (
        BranchChild("root.a", "root", 0, action=0.0),
        BranchChild("root.b", "root", 1, action=1.0),
        BranchChild("root.c", "root", 2, action=2.0),
    )
    rows = allocate_branch_measure(1.0, children)
    assert len(rows) == 3
    assert isclose(sum(row.local_probability for row in rows), 1.0, abs_tol=1e-15)
    assert isclose(sum(row.measure for row in rows), 1.0, abs_tol=1e-15)
    assert isclose(sum(row.amplitude_norm_squared for row in rows), 1.0, abs_tol=1e-15)
    assert rows[0].measure > rows[1].measure > rows[2].measure


def test_zero_beta_gives_uniform_local_probabilities() -> None:
    children = shell_demo_children("root", depth=1)
    rows = allocate_branch_measure(0.25, children, BranchMeasureConfig(beta=0.0))
    assert all(isclose(row.local_probability, 1.0 / 5.0, abs_tol=1e-15) for row in rows)
    assert isclose(sum(row.measure for row in rows), 0.25, abs_tol=1e-15)


def test_effective_action_rejects_invalid_shell() -> None:
    with pytest.raises(ValueError, match="shell_q"):
        effective_action(BranchChild("bad", "root", 9))


def test_mixed_parent_allocation_is_rejected() -> None:
    children = (
        BranchChild("a", "root", 0),
        BranchChild("b", "other", 1),
    )
    with pytest.raises(ValueError, match="share a parent_id"):
        allocate_branch_measure(1.0, children)


def test_demo_branch_frontier_preserves_total_measure() -> None:
    rows = demo_branch_frontier(depth=3)
    check = verify_branch_measure(rows)
    assert check["passed"] is True
    assert check["num_rows"] == 125
    assert check["parent_count"] == 25
    assert frontier_entropy(rows) > 0.0


def test_law_summary_preserves_boundary_language() -> None:
    summary = law_summary()
    assert "Roadmap 008" in summary["title"]
    assert "no Born-rule proof" in summary["boundary"]
    assert "no empirical validation" in summary["boundary"]
