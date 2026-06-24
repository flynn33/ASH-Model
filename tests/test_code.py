from itertools import combinations, product

from ash_model.bits import flip_bit, hamming_distance, hamming_weight, integrity_bit, is_integrity_valid, xor_bits
from ash_model.code import (
    ACTIVE_CODE_COORDINATES,
    CODEWORDS,
    GENERATOR_MATRIX,
    INVARIANT_COORDINATE,
    PARITY_COORDINATE,
    code_certificate,
    decode,
    decode_affine,
    dual_codewords,
    encode,
    gf2_rank,
    message_for,
    minimum_distance,
    punctured_codewords,
    syndrome,
    translate,
    weight_distribution,
)


def test_exact_code_invariants():
    certificate = code_certificate()
    assert certificate == {
        "length": 9,
        "rank": 4,
        "size": 16,
        "minimum_distance": 4,
        "weight_distribution": {0: 1, 4: 14, 8: 1},
        "doubly_even": True,
        "self_orthogonal": True,
        "self_dual_in_f2_9": False,
        "dual_size": 32,
        "coordinate_8_invariant": True,
        "coordinate_9_active": True,
        "coordinate_9_parity": True,
        "punctured_length": 8,
        "punctured_rank": 4,
        "punctured_minimum_distance": 4,
        "punctured_self_dual": True,
    }
    assert gf2_rank(GENERATOR_MATRIX) == 4
    assert minimum_distance() == 4
    assert weight_distribution() == {0: 1, 4: 14, 8: 1}


def test_coordinate_9_is_active_parity_and_coordinate_8_is_code_invariant():
    assert {word[PARITY_COORDINATE] for word in CODEWORDS} == {0, 1}
    for word in CODEWORDS:
        assert word[INVARIANT_COORDINATE] == 0
        assert word[PARITY_COORDINATE] == integrity_bit(word[:8])
        assert hamming_weight(word) % 4 == 0
        assert is_integrity_valid(word)


def test_encode_and_exact_decode_are_bijections():
    encoded = set()
    for message in product((0, 1), repeat=4):
        codeword = encode(message)
        encoded.add(codeword)
        assert message_for(codeword) == message
        result = decode(codeword)
        assert result.status == "exact"
        assert result.codeword == codeword
        assert result.message == message
        assert result.distance == 0
    assert encoded == set(CODEWORDS)


def test_every_single_bit_error_is_corrected():
    received = set()
    for codeword in CODEWORDS:
        for coordinate in range(9):
            corrupted = flip_bit(codeword, coordinate)
            received.add(corrupted)
            result = decode(corrupted)
            assert result.status == "corrected"
            assert result.codeword == codeword
            assert result.distance == 1
    assert len(received) == 16 * 9


def test_every_two_bit_error_is_rejected_without_silent_healing():
    for codeword in CODEWORDS:
        for left, right in combinations(range(9), 2):
            corrupted = flip_bit(flip_bit(codeword, left), right)
            result = decode(corrupted)
            assert result.status == "uncorrectable"
            assert result.codeword is None
            assert result.distance == 2


def test_full_512_state_decoder_partition():
    counts = {"exact": 0, "corrected": 0, "uncorrectable": 0}
    nearest = {}
    for state in product((0, 1), repeat=9):
        result = decode(state)
        counts[result.status] += 1
        nearest[(result.distance, result.nearest_count)] = nearest.get((result.distance, result.nearest_count), 0) + 1
    assert counts == {"exact": 16, "corrected": 144, "uncorrectable": 352}
    assert nearest == {(0, 1): 16, (1, 1): 144, (2, 1): 128, (2, 4): 112, (3, 4): 112}


def test_affine_recovery_for_all_integrity_anchors_codewords_and_single_errors():
    anchors = [state for state in product((0, 1), repeat=9) if is_integrity_valid(state)]
    for anchor in anchors:
        for codeword in CODEWORDS:
            target = xor_bits(anchor, codeword)
            exact = decode_affine(target, anchor)
            assert exact.status == "exact"
            assert exact.recovered_state == target
            for coordinate in range(9):
                corrupted = flip_bit(target, coordinate)
                result = decode_affine(corrupted, anchor)
                assert result.status == "corrected"
                assert result.recovered_state == target


def test_code_translation_preserves_integrity_and_rejects_noncode_mask():
    anchor = (1, 0, 1, 1, 0, 1, 0, 1, 1)
    assert is_integrity_valid(anchor)
    for codeword in CODEWORDS:
        assert is_integrity_valid(translate(anchor, codeword))
    noncode = (1, 0, 0, 0, 0, 0, 0, 0, 0)
    try:
        translate(anchor, noncode)
    except ValueError:
        pass
    else:
        raise AssertionError("noncode translation mask was accepted")


def test_parity_check_and_dual_dimensions():
    assert len(dual_codewords()) == 32
    assert all(syndrome(word) == (0, 0, 0, 0, 0) for word in CODEWORDS)
    assert len(punctured_codewords()) == 16
    assert set(ACTIVE_CODE_COORDINATES) == {0, 1, 2, 3, 4, 5, 6, 8}
