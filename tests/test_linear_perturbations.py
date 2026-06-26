from __future__ import annotations

from math import comb, isclose

import numpy as np

from ash_model.linear_perturbations import (
    SHELLS,
    canonical_character_labels,
    character_value,
    impulse_response_rows,
    krawtchouk_k2,
    lazy_shell_transfer_factor,
    pair_flip_shell_eigenvalue,
    random_perturbation_power_check,
    shell_index,
    spectral_shell_table,
    transfer_factor,
    verify_character_eigenmodes,
)
from ash_model.physics import physical_state_space


def test_canonical_character_quotient_has_256_labels_and_shell_counts() -> None:
    labels = canonical_character_labels()
    assert len(labels) == 256
    counts = {q: 0 for q in SHELLS}
    for label in labels:
        counts[shell_index(label)] += 1
    assert counts == {0: 1, 1: 9, 2: 36, 3: 84, 4: 126}


def test_all_ones_quotient_gives_same_restricted_character() -> None:
    states = physical_state_space()
    label = (1, 0, 1, 0, 0, 1, 0, 0, 0)
    complement = tuple(1 - bit for bit in label)
    assert all(character_value(label, state) == character_value(complement, state) for state in states)


def test_exact_shell_eigenvalues() -> None:
    expected_k2 = {0: 36, 1: 20, 2: 8, 3: 0, 4: -4}
    expected_lambda = {0: 1.0, 1: 5.0 / 9.0, 2: 2.0 / 9.0, 3: 0.0, 4: -1.0 / 9.0}
    for q in SHELLS:
        assert krawtchouk_k2(q) == expected_k2[q]
        assert isclose(pair_flip_shell_eigenvalue(q), expected_lambda[q], rel_tol=0.0, abs_tol=1e-15)


def test_spectral_shell_table() -> None:
    rows = spectral_shell_table()
    assert [row.q for row in rows] == [0, 1, 2, 3, 4]
    assert [row.multiplicity for row in rows] == [comb(9, q) for q in range(5)]
    assert [row.krawtchouk_k2 for row in rows] == [36, 20, 8, 0, -4]


def test_eigenmode_verification_residual_is_small() -> None:
    verification = verify_character_eigenmodes(probabilities=(0.01, 0.05, 0.1, 0.5, 1.0))
    assert verification["num_states"] == 256
    assert verification["num_characters"] == 256
    assert verification["shell_counts"] == {"0": 1, "1": 9, "2": 36, "3": 84, "4": 126}
    assert verification["max_eigen_residual"] <= 1e-12


def test_transfer_factor_matches_constant_schedule_power() -> None:
    p = 0.05
    ticks = 20
    schedule = tuple(p for _ in range(ticks))
    for q in SHELLS:
        assert isclose(
            transfer_factor(q, schedule),
            lazy_shell_transfer_factor(q, p) ** ticks,
            rel_tol=0.0,
            abs_tol=1e-15,
        )


def test_random_perturbation_power_check() -> None:
    check = random_perturbation_power_check(seed=20260626, probability=0.05, ticks=20)
    assert check["max_relative_error"] <= 1e-10
    rows = check["rows"]
    assert len(rows) == 5
    assert [int(row["q"]) for row in rows] == [0, 1, 2, 3, 4]


def test_impulse_response_first_values() -> None:
    rows = impulse_response_rows(probability=0.05, ticks=3)
    q1 = [row for row in rows if int(row["q"]) == 1]
    factor = lazy_shell_transfer_factor(1, 0.05)
    assert q1[0]["impulse_response"] == 0.0
    assert q1[1]["impulse_response"] == 1.0
    assert np.isclose(q1[2]["impulse_response"], factor)
