from math import comb

import ash_model
from ash_model.bits import bits_to_int, int_to_bits, is_integrity_valid, make_integrity_state
from ash_model.code import CODEWORDS, orbit
from ash_model.hypercube import (
    coset_partition,
    distance_shell,
    distance_shell_counts,
    even_parity_shell_counts,
    hypercube_adjacency_spectrum,
    hypercube_edge_count,
    hypercube_laplacian_spectrum,
    integrity_states,
    neighbors,
    observed_plane_counts,
    pair_flip_adjacency_spectrum,
    pair_flip_graph_degree,
    pair_flip_graph_edge_count,
    pair_flip_laplacian_spectrum,
    states,
    theoretical_plane_counts,
)


def test_all_512_state_round_trips_and_neighbor_degree():
    all_states = states()
    assert len(all_states) == 512
    for index, state in enumerate(all_states):
        assert bits_to_int(state) == index
        assert int_to_bits(index) == state
        adjacent = neighbors(state)
        assert len(adjacent) == 9
        assert len(set(adjacent)) == 9


def test_hamming_plane_counts_are_binomial():
    expected = tuple(comb(9, weight) for weight in range(10))
    assert theoretical_plane_counts() == expected
    assert observed_plane_counts(states()) == expected
    assert distance_shell_counts() == expected


def test_integrity_hyperplane_has_256_states():
    valid = integrity_states()
    assert len(valid) == 256
    assert all(is_integrity_valid(state) for state in valid)
    for payload_index in range(256):
        payload = int_to_bits(payload_index, length=8)
        assert make_integrity_state(payload) in valid


def test_distance_shells_are_exact_for_any_origin():
    origin = int_to_bits(0b101010101)
    for radius, expected_count in enumerate(distance_shell_counts()):
        shell = distance_shell(origin, radius)
        assert len(shell) == expected_count
        assert len(set(shell)) == expected_count
        assert all(
            sum(left != right for left, right in zip(origin, state, strict=True)) == radius
            for state in shell
        )


def test_hypercube_edge_count_and_spectra_are_exact():
    adjacency = hypercube_adjacency_spectrum()
    laplacian = hypercube_laplacian_spectrum()

    assert hypercube_edge_count() == 9 * 2**8
    assert adjacency == tuple((9 - 2 * weight, comb(9, weight)) for weight in range(10))
    assert laplacian == tuple((2 * weight, comb(9, weight)) for weight in range(10))
    assert sum(multiplicity for _, multiplicity in adjacency) == 512
    assert sum(value * multiplicity for value, multiplicity in adjacency) == 0
    assert (
        sum((value**2) * multiplicity for value, multiplicity in adjacency)
        == 2 * hypercube_edge_count()
    )


def test_even_parity_pair_flip_geometry_is_exact():
    adjacency = pair_flip_adjacency_spectrum()
    laplacian = pair_flip_laplacian_spectrum()

    assert even_parity_shell_counts() == tuple(
        comb(9, weight) for weight in range(0, 10, 2)
    )
    assert pair_flip_graph_degree() == comb(9, 2)
    assert pair_flip_graph_edge_count() == 256 * comb(9, 2) // 2
    assert adjacency == (
        (36, 1),
        (20, 9),
        (8, 36),
        (0, 84),
        (-4, 126),
    )
    assert laplacian == (
        (0, 1),
        (16, 9),
        (28, 36),
        (36, 84),
        (40, 126),
    )
    assert sum(multiplicity for _, multiplicity in adjacency) == 256
    assert sum(value * multiplicity for value, multiplicity in adjacency) == 0
    assert (
        sum((value**2) * multiplicity for value, multiplicity in adjacency)
        == 2 * pair_flip_graph_edge_count()
    )


def test_code_orbits_partition_full_and_integrity_spaces():
    full = coset_partition()
    valid = coset_partition(integrity_only=True)
    assert len(full) == 32
    assert len(valid) == 16
    assert all(len(group) == 16 for group in full)
    assert all(len(group) == 16 for group in valid)
    assert len({state for group in full for state in group}) == 512
    assert len({state for group in valid for state in group}) == 256


def test_coordinate_8_is_invariant_within_every_code_orbit():
    for state in states():
        assert {member[7] for member in orbit(state)} == {state[7]}
        assert all((member[8] == (sum(member[:8]) & 1)) == is_integrity_valid(state) for member in orbit(state))


def test_codewords_are_distinct_hypercube_states():
    assert len(CODEWORDS) == len(set(CODEWORDS)) == 16


def test_public_surface_exports_hypercube_geometry_helpers():
    assert ash_model.hypercube_edge_count is hypercube_edge_count
    assert ash_model.hypercube_adjacency_spectrum is hypercube_adjacency_spectrum
    assert ash_model.pair_flip_adjacency_spectrum is pair_flip_adjacency_spectrum
