import numpy as np

from ash_model.adinkra import (
    adinkra_certificate,
    garden_matrices,
    matrix_edges,
    quotient_edges,
    quotient_matrix_isomorphism,
    quotient_vertices,
    verify_garden_algebra,
)
from ash_model.projection import is_code_invariant, orbit_average, projection_certificate


def test_orbit_average_is_idempotent_and_code_invariant():
    values = np.arange(512, dtype=float) ** 2 - 7.0 * np.arange(512) + 3.0
    once = orbit_average(values)
    twice = orbit_average(once)
    assert np.array_equal(once, twice)
    assert is_code_invariant(once)
    certificate = projection_certificate()
    assert certificate["idempotence_max_abs_error"] == 0.0
    assert certificate["output_is_code_invariant"] is True
    assert certificate["constant_preserved"] is True


def test_projection_is_linear():
    left = np.sin(np.arange(512, dtype=float))
    right = np.cos(np.arange(512, dtype=float))
    assert np.allclose(orbit_average(2.0 * left - 3.0 * right), 2.0 * orbit_average(left) - 3.0 * orbit_average(right))


def test_garden_algebra_holds_exactly():
    report = verify_garden_algebra()
    assert report["garden_algebra_holds"] is True
    assert report["maximum_integer_residual"] == 0
    matrices = garden_matrices()
    assert len(matrices) == 8
    assert all(matrix.shape == (8, 8) for matrix in matrices)


def test_adinkra_quotient_graph_and_matrix_graph_are_isomorphic():
    vertices = quotient_vertices()
    edges = quotient_edges()
    matrix_graph = matrix_edges()
    report = quotient_matrix_isomorphism()
    assert len(vertices) == 16
    assert sum(vertex.parity == 0 for vertex in vertices) == 8
    assert sum(vertex.parity == 1 for vertex in vertices) == 8
    assert len(edges) == 64
    assert len(matrix_graph) == 64
    assert report["valid"] is True
    assert report["color_permutation_one_based"] == [1, 2, 3, 5, 4, 8, 6, 7]
    certificate = adinkra_certificate()
    assert certificate["garden_algebra_holds"] is True
    assert certificate["valid"] is True
