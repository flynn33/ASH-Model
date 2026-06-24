from math import comb

from ash_model.bits import bits_to_int, int_to_bits, is_integrity_valid, make_integrity_state
from ash_model.code import CODEWORDS, orbit
from ash_model.hypercube import (
    coset_partition,
    integrity_states,
    neighbors,
    observed_plane_counts,
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


def test_integrity_hyperplane_has_256_states():
    valid = integrity_states()
    assert len(valid) == 256
    assert all(is_integrity_valid(state) for state in valid)
    for payload_index in range(256):
        payload = int_to_bits(payload_index, length=8)
        assert make_integrity_state(payload) in valid


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
