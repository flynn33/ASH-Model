"""Finite checks for the proposed ASH leaf-branching research models.

This is a stand-alone research harness, not an ASH repository test suite.
The four generators are taken from the parity-explicit candidate in Project
file file_00000000b21c71f6b74e3b7da08a90f9, displayed as g1 through g4.
Infinite claims require the arguments in the accompanying research note;
finite enumeration alone does not prove them.

Run: python verify_branch_models.py
"""
from __future__ import annotations

import json
import math
import unittest
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from itertools import combinations, product
from operator import xor
from pathlib import Path


@dataclass(frozen=True)
class ASHCode:
    generators: tuple[int, ...]
    words: tuple[int, ...]

    @classmethod
    def candidate(cls) -> ASHCode:
        generators = tuple(int(s, 2) for s in (
            '111100000', '110011000', '101010100', '100110001'))
        words = tuple(sorted({reduce(xor, subset, 0)
                              for size in range(5)
                              for subset in combinations(generators, size)}))
        return cls(generators, words)

    def decode_radius_one(self, received: int) -> int | None:
        if not 0 <= received < 512:
            raise ValueError('Expected a nine-bit integer.')
        candidates = [word for word in self.words
                      if (word ^ received).bit_count() <= 1]
        if len(candidates) > 1:
            raise AssertionError('Overlapping radius-one decoding balls.')
        return candidates[0] if candidates else None


@dataclass(frozen=True)
class StackState:
    blocks: tuple[int, ...] = ()

    @property
    def local_label(self) -> int:
        return reduce(xor, self.blocks, 0)

    @property
    def can_pop(self) -> bool:
        return bool(self.blocks)

    def push(self, codeword: int, code: ASHCode) -> StackState:
        if codeword not in code.words:
            raise ValueError('Only candidate-code blocks can be pushed.')
        return StackState(self.blocks + (codeword,))

    def pop(self) -> StackState:
        if not self.blocks:
            raise ValueError('Cannot pop an empty stack.')
        return StackState(self.blocks[:-1])


CODE = ASHCode.candidate()
OBSERVATIONS: dict[str, object] = {}


class BranchModelTests(unittest.TestCase):
    def test_01_code_invariants(self) -> None:
        words = CODE.words
        self.assertEqual(len(words), 16)
        self.assertEqual(Counter(w.bit_count() for w in words), {0: 1, 4: 14, 8: 1})
        self.assertTrue(all((a ^ b) in words for a in words for b in words))
        self.assertEqual(min((a ^ b).bit_count() for a, b in combinations(words, 2)), 4)
        self.assertEqual({w & 1 for w in words}, {0, 1})
        self.assertTrue(all((w & 1) == ((w >> 1).bit_count() % 2) for w in words))
        self.assertTrue(all((w & 2) == 0 for w in words))
        OBSERVATIONS['code'] = {
            'basis_left_to_right_coordinates_1_to_9': [f'{g:09b}' for g in CODE.generators],
            'words': [f'{w:09b}' for w in words],
            'rank_inferred_from_linear_span_size': 4,
            'size': 16, 'minimum_distance': 4,
            'weight_enumerator': dict(sorted(Counter(w.bit_count() for w in words).items())),
            'coordinate_9_active_and_even_parity': True,
            'coordinate_8_zero_in_this_presentation': True,
        }

    def test_02_coset_invariance_all_8192_translations(self) -> None:
        cosets = {frozenset(x ^ c for c in CODE.words) for x in range(512)}
        self.assertEqual(len(cosets), 32)
        self.assertTrue(all(len(coset) == 16 for coset in cosets))
        for x in range(512):
            initial = frozenset(x ^ c for c in CODE.words)
            for move in CODE.words:
                self.assertEqual(frozenset((x ^ move) ^ c for c in CODE.words), initial)
        OBSERVATIONS['cosets'] = {'count': 32, 'size': 16, 'translations_checked': 8192}

    def test_03_local_decoder_bounds(self) -> None:
        for word in CODE.words:
            self.assertEqual(CODE.decode_radius_one(word), word)
            for bit in range(9):
                self.assertEqual(CODE.decode_radius_one(word ^ (1 << bit)), word)
            for a, b in combinations(range(9), 2):
                self.assertIsNone(CODE.decode_radius_one(word ^ (1 << a) ^ (1 << b)))
        OBSERVATIONS['local_decoder'] = {'clean': 16, 'single_bit_corrected': 144,
                                         'double_bit_rejected': 576}

    def test_04_history_enumeration_and_endpoint_entropy(self) -> None:
        rows = []
        for depth in range(1, 5):
            endpoints = Counter(reduce(xor, history, 0)
                                for history in product(CODE.words, repeat=depth))
            leaves = 16 ** depth
            self.assertEqual(sum(endpoints.values()), leaves)
            self.assertEqual(set(endpoints), set(CODE.words))
            self.assertEqual(set(endpoints.values()), {16 ** (depth - 1)})
            endpoint_entropy = -sum((count / leaves) * math.log2(count / leaves)
                                    for count in endpoints.values())
            self.assertAlmostEqual(endpoint_entropy, 4.0)
            rows.append({'depth': depth, 'explicitly_enumerated_histories': leaves,
                         'distinct_endpoint_labels': len(endpoints),
                         'histories_per_endpoint': 16 ** (depth - 1),
                         'total_probability_exact': str(Fraction(sum(endpoints.values()), leaves)),
                         'uniform_history_entropy_bits': 4 * depth,
                         'endpoint_entropy_bits': endpoint_entropy})
        OBSERVATIONS['uniform_code_move_tree'] = rows

    def test_05_history_dependent_probability_consistency(self) -> None:
        frontier = {(): Fraction(1)}
        for depth in range(8):
            next_frontier = {}
            for history, parent_mass in frontier.items():
                p_zero = Fraction(1 + sum(history) % 3, 4)
                probabilities = (p_zero, 1 - p_zero)
                for symbol, probability in enumerate(probabilities):
                    next_frontier[history + (symbol,)] = parent_mass * probability
                self.assertEqual(sum(next_frontier[history + (symbol,)] for symbol in (0, 1)),
                                 parent_mass)
            self.assertEqual(sum(next_frontier.values()), Fraction(1))
            frontier = next_frontier
        OBSERVATIONS['history_dependent_binary_measure'] = {
            'maximum_depth_checked': 8, 'leaves_at_maximum_depth': len(frontier),
            'total_probability_exact': str(sum(frontier.values())),
            'all_tested_prefix_marginals_consistent': True}

    def test_06_separate_horizon_normalization_counterexample(self) -> None:
        depth_one = (Fraction(1, 2), Fraction(1, 2))
        depth_two = (Fraction(1, 8), Fraction(1, 8), Fraction(3, 8), Fraction(3, 8))
        self.assertEqual(sum(depth_one), 1)
        self.assertEqual(sum(depth_two), 1)
        self.assertNotEqual(sum(depth_two[:2]), depth_one[0])
        OBSERVATIONS['inconsistent_horizon_counterexample'] = {
            'depth_one': [str(p) for p in depth_one],
            'depth_two': [str(p) for p in depth_two],
            'first_parent_mass_at_depth_one': str(depth_one[0]),
            'first_parent_mass_from_depth_two': str(sum(depth_two[:2]))}

    def test_07_stack_transition_closure(self) -> None:
        states = pushes = pops = 0
        for depth in range(4):
            for blocks in product(CODE.words, repeat=depth):
                state = StackState(blocks)
                states += 1
                self.assertIn(state.local_label, CODE.words)
                for word in CODE.words:
                    child = state.push(word, CODE)
                    self.assertEqual(child.local_label, state.local_label ^ word)
                    self.assertIn(child.local_label, CODE.words)
                    self.assertEqual(child.pop(), state)
                    pushes += 1
                if state.can_pop:
                    child = state.pop()
                    self.assertEqual(child.local_label, state.local_label ^ blocks[-1])
                    self.assertIn(child.local_label, CODE.words)
                    pops += 1
        with self.assertRaises(ValueError):
            StackState().pop()
        with self.assertRaises(ValueError):
            StackState().push(1, CODE)
        OBSERVATIONS['stack_closure'] = {'states_checked': states,
                                         'pushes_checked': pushes, 'pops_checked': pops}

    def test_08_same_local_label_distinct_future_pop_languages(self) -> None:
        g = CODE.generators[0]
        pairs = 0
        for k, ell in combinations(range(1, 13), 2):
            shorter = StackState((g,) * (2 * k))
            longer = StackState((g,) * (2 * ell))
            self.assertEqual(shorter.local_label, 0)
            self.assertEqual(longer.local_label, 0)
            for _ in range(2 * k):
                shorter, longer = shorter.pop(), longer.pop()
            self.assertFalse(shorter.can_pop)
            self.assertTrue(longer.can_pop)
            pairs += 1
        OBSERVATIONS['future_distinguishability'] = {
            'even_stack_lengths_checked': list(range(2, 25, 2)),
            'distinct_length_pairs_checked': pairs,
            'all_pairs_same_initial_local_label': '000000000',
            'all_pairs_distinguished_by_further_pop_legality': True}

    def test_09_recorded_history_isometry(self) -> None:
        columns = [{(parent, child): (1j ** ((parent + child) % 4)) / 4
                    for child in range(16)} for parent in range(16)]
        for i in range(16):
            for j in range(16):
                inner = sum(a.conjugate() * columns[j].get(key, 0j)
                            for key, a in columns[i].items())
                self.assertEqual(inner, complex(i == j))
        OBSERVATIONS['recorded_history_isometry'] = {
            'input_dimension': 16, 'output_dimension': 256,
            'gram_matrix_equals_identity': True,
            'claim_scope': 'One finite embedding with orthogonal history records; not a cosmology or infinite-limit verification.'}

    def test_10_column_normalization_is_not_general_isometry(self) -> None:
        # Both columns (1,0) have norm one, but they are not orthogonal.
        output_norm_squared = (1 / math.sqrt(2) + 1 / math.sqrt(2)) ** 2
        self.assertAlmostEqual(output_norm_squared, 2.0)
        OBSERVATIONS['nonisometry_counterexample'] = {
            'columns': [[1, 0], [1, 0]], 'each_column_norm_squared': 1,
            'normalized_equal_superposition_output_norm_squared': output_norm_squared}


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BranchModelTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {
        'scope': 'Independent finite checks of proposed mathematical models; no repository files edited or repository suite executed.',
        'tests_run': result.testsRun,
        'failures': len(result.failures), 'errors': len(result.errors),
        'successful': result.wasSuccessful(), 'observations': OBSERVATIONS,
        'not_verified': ['Infinite objects by enumeration', 'Physical branch ontology',
                         'Quantum Born-rule derivation', 'Spacetime emergence',
                         'Cosmological data fit', 'Global fault tolerance',
                         'Repository implementation status'],
    }
    output = Path(__file__).with_name('finite_checks.json')
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
