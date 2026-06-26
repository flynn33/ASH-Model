from ash_model.finite_observer_limit import (
    ODD_LEVELS,
    adjacency_spectrum,
    causal_cone_sizes,
    causal_interval_size,
    causal_related,
    edge_count,
    even_states,
    fiber_sizes,
    graph_degree,
    laplacian_gap,
    pair_distance,
    project_between,
    shell_counts,
    unit_scale_table,
    validate_lipschitz,
    validate_projective_consistency,
    validation_summary,
)


def test_even_state_counts_and_shells():
    for n in ODD_LEVELS:
        states = even_states(n)
        assert len(states) == 2 ** (n - 1)
        assert sum(shell_counts(n).values()) == len(states)
        assert causal_cone_sizes(n)[n // 2] == len(states)


def test_halved_cube_graph_invariants():
    for n in ODD_LEVELS:
        assert edge_count(n) == (2 ** (n - 1) * graph_degree(n)) // 2
        assert sum(m for _, _, m in adjacency_spectrum(n)) == 2 ** (n - 1)
    assert adjacency_spectrum(9) == [(0, 36, 1), (1, 20, 9), (2, 8, 36), (3, 0, 84), (4, -4, 126)]
    assert laplacian_gap(9) == 16


def test_projective_consistency_and_uniform_fibers():
    assert validate_projective_consistency()
    for n in ODD_LEVELS:
        for m in ODD_LEVELS:
            if n >= m:
                assert set(fiber_sizes(n, m).values()) == {2 ** (n - m)}


def test_projection_lipschitz_on_microscopic_events():
    assert validate_lipschitz()


def test_causal_bound_for_projected_endpoints():
    x = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    y = (1, 1, 0, 0, 0, 0, 0, 0, 0)
    assert pair_distance(x, y) == 1
    py = project_between(y, 9, 5)
    px = project_between(x, 9, 5)
    assert pair_distance(px, py) <= pair_distance(x, y)


def test_causal_relation_and_interval_are_finite():
    x = (0, 0, 0)
    y = (1, 1, 0)
    assert causal_related(x, 0, y, 1)
    assert not causal_related(y, 1, x, 0)
    assert causal_interval_size(5, delta_t=2, distance=1) > 0


def test_unit_scale_annotations_are_normalized_placeholders():
    rows = unit_scale_table(ell9_m=1.0, tau9_s=1.0)
    assert rows[-1].n == 9
    assert rows[-1].ell_m == 1.0
    assert rows[-1].tau_s == 1.0
    assert rows[0].ell_m == 16.0
    assert rows[0].tau_s == 16.0


def test_validation_summary_closes_only_finite_observer_scope():
    summary = validation_summary()
    assert summary["r011_scope"] == "finite_observer_limit_closure_not_differentiable_continuum"
    assert summary["projective_consistency"] is True
    assert summary["projection_lipschitz_on_events"] is True
    assert summary["n9_shell_counts"] == {0: 1, 1: 36, 2: 126, 3: 84, 4: 9}
