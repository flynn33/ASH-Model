import numpy as np

from ash_model.bits import is_integrity_valid
from ash_model.code import CODEWORDS
from ash_model.simulation import (
    _random_weight4_masks,
    binomial_distribution,
    initialize_agents,
    noise_kernel,
    occupancy_distribution,
    run_simulation,
    step_agents,
)


def test_random_weight4_masks_are_weight_four():
    rng = np.random.default_rng(12345)
    masks = _random_weight4_masks(1000, rng)
    assert masks.shape == (1000, 9)
    assert set(np.sum(masks, axis=1).tolist()) == {4}


def test_noise_kernel_is_doubly_stochastic_irreducible_and_aperiodic_for_0_p_1():
    kernel = noise_kernel(0.2)
    assert kernel.shape == (512, 512)
    assert np.allclose(kernel.sum(axis=1), 1.0)
    assert np.allclose(kernel.sum(axis=0), 1.0)
    assert np.all(np.diag(kernel) > 0.0)
    uniform = np.full(512, 1.0 / 512.0)
    assert np.allclose(uniform @ kernel, uniform)
    # Every hypercube edge has positive transition probability, so the graph is connected.
    for state in range(512):
        for bit in range(9):
            assert kernel[state, state ^ (1 << bit)] > 0.0


def test_uniform_hamming_marginal_is_exact_binomial():
    all_states = np.asarray(
        [[(index >> shift) & 1 for shift in range(8, -1, -1)] for index in range(512)],
        dtype=np.uint8,
    )
    assert np.array_equal(occupancy_distribution(all_states), binomial_distribution())


def test_ash_transforms_preserve_code_orbit_without_noise():
    rng = np.random.default_rng(7)
    agents = initialize_agents(500, "zero", rng)
    for _ in range(20):
        agents = step_agents(agents, transform_mode="ash", noise_probability=0.0, rng=rng)
    assert all(tuple(row.tolist()) in set(CODEWORDS) for row in agents)


def test_integrity_uniform_initialization_and_transform_preserve_integrity_without_noise():
    rng = np.random.default_rng(11)
    agents = initialize_agents(1000, "integrity_uniform", rng)
    agents = step_agents(agents, transform_mode="ash", noise_probability=0.0, rng=rng)
    assert all(is_integrity_valid(tuple(row.tolist())) for row in agents)


def test_seeded_simulation_is_reproducible_and_uniform_start_is_baseline():
    first = run_simulation(agent_count=2000, ticks=25, initial_mode="uniform", transform_mode="ash", noise_probability=0.01, seed=99)
    second = run_simulation(agent_count=2000, ticks=25, initial_mode="uniform", transform_mode="ash", noise_probability=0.01, seed=99)
    assert np.array_equal(first.agents, second.agents)
    assert np.array_equal(first.occupancy, second.occupancy)
    assert first.tv_to_binomial == second.tv_to_binomial
