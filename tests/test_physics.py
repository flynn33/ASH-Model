import numpy as np

import ash_model
from ash_model.bits import hamming_weight, is_integrity_valid
from ash_model.physics import (
    BIT_COUNT,
    background_moments,
    bridge_observables,
    compatible_payload_state,
    even_weight_levels,
    evolve_weight_distribution,
    graph_distance_bound,
    lazy_pair_flip_eigenvalue,
    maximum_entropy_bits,
    pair_flip_eigenvalue,
    pair_flip_generator,
    pair_flip_masks,
    pair_flip_transition,
    physical_state_space,
    state_distribution_from_weights,
    uniform_background_distribution,
    uniform_physical_distribution,
    weight_level_degeneracies,
    weight_background_kernel,
)


def test_physical_state_space_is_even_parity_hyperplane():
    states = physical_state_space()
    assert len(states) == 256
    assert len(set(states)) == 256
    assert all(is_integrity_valid(state) for state in states)
    assert {hamming_weight(state) % 2 for state in states} == {0}


def test_pair_flip_masks_are_all_weight_two_masks():
    masks = pair_flip_masks()
    assert len(masks) == 36
    assert len(set(masks)) == 36
    assert {hamming_weight(mask) for mask in masks} == {2}


def test_pair_flip_transition_is_stochastic_symmetric_and_stationary():
    kernel = pair_flip_transition(0.35)
    assert kernel.shape == (256, 256)
    assert np.all(kernel >= 0.0)
    assert np.allclose(kernel.sum(axis=1), 1.0)
    assert np.allclose(kernel, kernel.T)
    uniform = uniform_physical_distribution()
    assert np.allclose(uniform @ kernel, uniform)


def test_pair_flip_generator_has_markov_generator_properties():
    generator = pair_flip_generator(1.7)
    assert generator.shape == (256, 256)
    assert np.allclose(generator.sum(axis=1), 0.0)
    off_diagonal = generator.copy()
    np.fill_diagonal(off_diagonal, 0.0)
    assert np.all(off_diagonal >= 0.0)
    assert np.all(np.diag(generator) <= 0.0)
    assert np.allclose(generator, generator.T)


def test_weight_background_kernel_matches_direct_state_kernel_lumping():
    probability = 0.42
    state_kernel = pair_flip_transition(probability)
    background = weight_background_kernel(probability)
    levels = even_weight_levels()

    # Start uniformly on all states with Hamming weight four.
    weight_law = np.zeros(len(levels), dtype=float)
    weight_law[levels.index(4)] = 1.0
    state_law = state_distribution_from_weights(weight_law)
    next_state_law = state_law @ state_kernel

    direct_next = np.zeros(len(levels), dtype=float)
    for probability_value, state in zip(next_state_law, physical_state_space(), strict=True):
        direct_next[levels.index(hamming_weight(state))] += probability_value

    assert np.allclose(weight_law @ background, direct_next)
    assert np.allclose(background.sum(axis=1), 1.0)


def test_even_weight_degeneracies_and_uniform_background_law():
    degeneracies = weight_level_degeneracies()
    distribution = uniform_background_distribution()

    assert degeneracies == (1, 36, 126, 84, 9)
    assert np.allclose(distribution, np.asarray(degeneracies, dtype=float) / 256.0)
    assert np.isclose(distribution.sum(), 1.0)
    assert np.allclose(distribution @ weight_background_kernel(0.6), distribution)


def test_background_moments_match_uniform_even_parity_shells():
    moments = background_moments(uniform_background_distribution())

    assert moments.mean_hamming_weight == BIT_COUNT / 2
    assert moments.variance_hamming_weight == BIT_COUNT / 4
    assert moments.order_parameter == 0.0


def test_evolve_weight_distribution_matches_repeated_background_kernel():
    levels = even_weight_levels()
    initial = np.zeros(len(levels), dtype=float)
    initial[levels.index(0)] = 1.0
    probability = 0.25

    evolved = evolve_weight_distribution(initial, probability=probability, steps=3)
    expected = initial @ np.linalg.matrix_power(weight_background_kernel(probability), 3)

    assert np.allclose(evolved, expected)
    assert np.isclose(evolved.sum(), 1.0)
    assert background_moments(evolved).mean_hamming_weight > 0.0


def test_bridge_observables_for_uniform_physical_distribution():
    observables = bridge_observables(uniform_physical_distribution())
    assert observables.mean_hamming_weight == BIT_COUNT / 2
    assert observables.order_parameter == 0.0
    assert observables.shannon_entropy_bits == maximum_entropy_bits()
    assert observables.parity_valid_probability == 1.0


def test_pair_flip_perturbation_eigenvalues_are_bounded_and_normalized():
    eigenvalues = [pair_flip_eigenvalue(weight) for weight in range(BIT_COUNT + 1)]
    assert eigenvalues[0] == 1.0
    assert all(-1.0 <= value <= 1.0 for value in eigenvalues)
    assert lazy_pair_flip_eigenvalue(0, 0.25) == 1.0
    assert all(
        -1.0 <= lazy_pair_flip_eigenvalue(weight, 0.25) <= 1.0
        for weight in range(BIT_COUNT + 1)
    )


def test_public_surface_exports_background_moment_helpers():
    assert ash_model.background_moments is background_moments
    assert ash_model.uniform_background_distribution is uniform_background_distribution
    assert ash_model.evolve_weight_distribution is evolve_weight_distribution


def test_compatible_payload_state_and_graph_distance_bound():
    first = compatible_payload_state((0, 0, 0, 0, 0, 0, 0, 0))
    second = compatible_payload_state((1, 1, 0, 0, 0, 0, 0, 0))
    third = compatible_payload_state((1, 1, 1, 1, 0, 0, 0, 0))
    assert is_integrity_valid(first)
    assert is_integrity_valid(second)
    assert is_integrity_valid(third)
    assert graph_distance_bound(first, second) == 1
    assert graph_distance_bound(first, third) == 2
