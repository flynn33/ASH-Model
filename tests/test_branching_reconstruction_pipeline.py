import numpy as np

from ash_model.bits import flip_bit, is_integrity_valid
from ash_model.branching import (
    aggregate_leaf_weights,
    branch_certificate,
    expand_geometry_lsystem,
    generate_branch_tree,
    interpret_geometry_lsystem,
    leaf_nodes,
    recover_branch_state,
)
from ash_model.pipeline import map_patch
from ash_model.reconstruction import (
    apply_operator,
    block_mean_downsample,
    generate_candidates,
    nearest_upsample,
    prune_candidates,
    source_consistency_score,
)


def test_branch_tree_counts_weights_geometry_and_state_semantics():
    source = (1, 0, 1, 0, 1, 0, 1, 0, 0)
    assert is_integrity_valid(source)
    tree = generate_branch_tree(source, depth=4)
    leaves = leaf_nodes(tree)
    assert len(tree) == 1 + 3 + 9 + 27 + 81
    assert len(leaves) == 81
    assert abs(sum(node.weight for node in leaves) - 1.0) < 1e-12
    assert len(aggregate_leaf_weights(tree)) == 16
    assert all(is_integrity_valid(node.state) for node in leaves)
    assert all(node.state[7] == source[7] for node in leaves)
    certificate = branch_certificate(4)
    assert certificate["leaf_count"] == certificate["expected_leaf_count"] == 81
    assert certificate["unique_messages"] == 16


def test_branch_affine_recovery_corrects_one_bit_and_rejects_two():
    source = (0,) * 9
    target = leaf_nodes(generate_branch_tree(source, depth=2))[4].state
    one_error = recover_branch_state(flip_bit(target, 3), source)
    assert one_error.status == "corrected"
    assert one_error.recovered_state == target
    two_error = recover_branch_state(flip_bit(flip_bit(target, 2), 7), source)
    assert two_error.status == "uncorrectable"
    assert two_error.recovered_state is None


def test_historical_geometry_lsystem_produces_balanced_segments():
    program = expand_geometry_lsystem(2)
    segments = interpret_geometry_lsystem(program)
    assert program.count("[") == program.count("]")
    assert len(segments) == program.count("F")
    assert len(segments) > 0


def test_reconstruction_operator_shapes_ranges_and_baseline_consistency():
    source = np.asarray([[0.0, 0.25], [0.75, 1.0]], dtype=float)
    baseline = nearest_upsample(source, 2)
    assert baseline.shape == (4, 4)
    assert np.array_equal(block_mean_downsample(baseline, 2), source)
    assert source_consistency_score(source, baseline, scale=2) == 1.0
    for message_value in range(16):
        message = tuple((message_value >> shift) & 1 for shift in range(3, -1, -1))
        candidate = apply_operator(source, message, scale=2)
        assert candidate.shape == (4, 4)
        assert np.min(candidate) >= 0.0
        assert np.max(candidate) <= 1.0


def test_candidate_generation_scoring_and_pruning_are_deterministic():
    source = np.indices((4, 4)).sum(axis=0).astype(float) % 2
    tree = generate_branch_tree((0,) * 9, depth=4)
    candidates = generate_candidates(source, leaf_nodes(tree), scale=2)
    assert len(candidates) == 16
    assert all(0.0 < candidate.source_score <= 1.0 for candidate in candidates)
    selected = prune_candidates(candidates, top_k=4)
    assert len(selected) == 4
    assert selected == tuple(candidates[:4])


def test_end_to_end_patch_mapping_pipeline():
    current = np.dstack(
        [
            np.linspace(0.0, 1.0, 16).reshape(4, 4),
            np.zeros((4, 4)),
            np.ones((4, 4)) * 0.25,
        ]
    )
    previous = current * 0.9
    result = map_patch(current, previous, branch_depth=4, scale=2, top_k=3)
    assert is_integrity_valid(result.source_state)
    assert len(result.branch_nodes) == 121
    assert len(result.candidates) == 16
    assert len(result.selected) == 3
    assert all(candidate.reconstruction.shape == (8, 8, 3) for candidate in result.selected)
