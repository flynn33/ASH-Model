from math import comb

import numpy as np
import pytest

import ash_model
from ash_model.bits import bits_to_int, hamming_weight, is_integrity_valid
from ash_model.physics import (
    mixed_sector_eigenvalue,
    mixed_sector_transition,
    payload_pair_flip_eigenvalue,
    payload_pair_flip_transition,
    payload_state_space,
    payload_to_physical_state,
    sector_refresh_eigenvalue,
    sector_refresh_transition,
)


def reachable_count(kernel, start):
    seen = {start}
    frontier = [start]
    while frontier:
        row = frontier.pop()
        for column in np.flatnonzero(kernel[row] > 0.0):
            if column not in seen:
                seen.add(int(column))
                frontier.append(int(column))
    return seen


def test_payload_pair_flip_has_two_parity_sectors():
    payloads = payload_state_space()
    kernel = payload_pair_flip_transition(probability=0.5)
    even_sector = reachable_count(kernel, 0)

    assert len(payloads) == 256
    assert kernel.shape == (256, 256)
    assert np.allclose(kernel.sum(axis=1), 1.0)
    assert np.allclose(kernel, kernel.T)
    assert len(even_sector) == 128
    assert {hamming_weight(payloads[index]) % 2 for index in even_sector} == {0}


def test_non_lazy_payload_pair_flip_is_pure_pair_walk():
    kernel = payload_pair_flip_transition(lazy=False)

    assert np.allclose(kernel.sum(axis=1), 1.0)
    assert np.allclose(np.diag(kernel), 0.0)
    assert np.count_nonzero(kernel[0]) == comb(8, 2)
    with pytest.raises(ValueError):
        payload_pair_flip_transition(probability=0.5, lazy=False)


def test_sector_refresh_flips_payload_sector_and_preserves_ash_integrity():
    payloads = payload_state_space()
    kernel = sector_refresh_transition()

    assert kernel.shape == (256, 256)
    assert np.allclose(kernel.sum(axis=1), 1.0)
    assert np.allclose(kernel, kernel.T)

    for row, payload in enumerate(payloads):
        source_sector = hamming_weight(payload) % 2
        for column in np.flatnonzero(kernel[row] > 0.0):
            target_payload = payloads[int(column)]
            physical_state = payload_to_physical_state(target_payload)
            assert hamming_weight(target_payload) % 2 == 1 - source_sector
            assert is_integrity_valid(physical_state)
            assert bits_to_int(target_payload) == int(column)


def test_mixed_sector_transition_is_stochastic_symmetric_and_uniform_stationary():
    kernel = mixed_sector_transition(epsilon=0.01, pair_probability=0.5)
    uniform = np.full(256, 1.0 / 256.0)

    assert kernel.shape == (256, 256)
    assert np.all(kernel >= 0.0)
    assert np.allclose(kernel.sum(axis=1), 1.0)
    assert np.allclose(kernel, kernel.T)
    assert np.allclose(uniform @ kernel, uniform)
    assert len(reachable_count(kernel, 0)) == 256


def test_mixed_sector_transition_spectrum_matches_formula():
    epsilon = 0.05
    kernel = mixed_sector_transition(epsilon=epsilon, pair_probability=0.5)
    exact = np.linalg.eigvalsh(kernel)
    formula = []
    for mode_weight in range(9):
        formula.extend(
            [mixed_sector_eigenvalue(mode_weight, epsilon, pair_probability=0.5)]
            * comb(8, mode_weight)
        )

    assert np.allclose(np.sort(exact), np.sort(formula))


def test_former_sector_mode_is_shifted_by_epsilon():
    epsilon = 0.1

    assert payload_pair_flip_eigenvalue(8, probability=0.5) == 1.0
    assert sector_refresh_eigenvalue(8) == -1.0
    assert mixed_sector_eigenvalue(8, epsilon, pair_probability=0.5) == pytest.approx(
        1.0 - 2.0 * epsilon
    )


def test_invalid_sector_mixing_parameters_raise():
    with pytest.raises(ValueError):
        payload_to_physical_state((0, 1))
    with pytest.raises(ValueError):
        payload_pair_flip_transition(probability=-0.1)
    with pytest.raises(ValueError):
        mixed_sector_transition(epsilon=1.1)
    with pytest.raises(ValueError):
        payload_pair_flip_eigenvalue(9)
    with pytest.raises(ValueError):
        sector_refresh_eigenvalue(-1)


def test_public_surface_exports_sector_mixing_helpers():
    assert ash_model.payload_state_space is payload_state_space
    assert ash_model.payload_to_physical_state is payload_to_physical_state
    assert ash_model.mixed_sector_transition is mixed_sector_transition
