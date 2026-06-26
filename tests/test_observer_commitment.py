from math import isclose

from ash_model.observer_commitment import (
    BranchRecord,
    ObserverCommitmentConfig,
    commit_memory,
    commitment_distribution,
    decoherence_entry,
    decoherence_summary,
    demo_expand_tree,
    frontier,
    memory_divergence,
    parent_memory_is_prefix,
    tree_distance,
    validate_probability_weights,
    verify_memory_prefix_embedding,
    verify_r009,
)


def test_commit_memory_appends_or_preserves():
    assert commit_memory(("a",), "b") == ("a", "b")
    assert commit_memory(("a",), None) == ("a",)
    assert commit_memory(("a",), "") == ("a",)


def test_demo_frontier_measure_is_conserved():
    records = demo_expand_tree(max_depth=4)
    leaves = frontier(records, 4)
    assert len(leaves) == 625
    validate_probability_weights(leaves)
    assert isclose(sum(leaf.weight for leaf in leaves), 1.0, abs_tol=1.0e-12)


def test_memory_prefix_embedding():
    records = demo_expand_tree(max_depth=3)
    by_id = {record.branch_id: record for record in records}
    assert verify_memory_prefix_embedding(records)
    for record in records:
        if record.parent_id is None:
            continue
        assert parent_memory_is_prefix(by_id[record.parent_id], record)


def test_commitment_distribution_is_push_forward_partition():
    leaves = frontier(demo_expand_tree(max_depth=4), 4)
    distribution = commitment_distribution(leaves)
    assert len(distribution) > 1
    assert isclose(sum(float(row["measure"]) for row in distribution), 1.0, abs_tol=1.0e-12)
    assert sum(int(row["leaf_count"]) for row in distribution) == len(leaves)


def test_branch_and_memory_distances():
    a = BranchRecord("b0.1.2", "b0.1", 2, 0.5, ("x", "y"))
    b = BranchRecord("b0.1.3", "b0.1", 2, 0.5, ("x", "z"))
    assert tree_distance(a, b) == 2
    assert memory_divergence(a, b) == 2


def test_decoherence_bound_and_suppression_summary():
    leaves = frontier(demo_expand_tree(max_depth=3), 3)
    cfg = ObserverCommitmentConfig(decoherence_threshold=1.0e-3)
    entry = decoherence_entry(leaves[0], leaves[1], cfg)
    assert entry["magnitude"] <= (leaves[0].weight * leaves[1].weight) ** 0.5
    summary = decoherence_summary(leaves, cfg)
    assert summary["passed_trace_invariant"] is True
    assert summary["max_offdiag_magnitude"] < 0.01
    assert summary["suppressed_pair_fraction"] > 0.5


def test_r009_verification_passes():
    report = verify_r009(max_depth=4)
    assert report["passed"] is True
    assert report["memory_prefix_embedding_passed"] is True
    assert report["decoherence_summary"]["passed_trace_invariant"] is True
    assert report["commitment_distribution_total"] == report["frontier_measure_total"]
