import numpy as np

from ash_model.bits import is_integrity_valid
from ash_model.features import (
    DEFAULT_HYSTERESIS,
    DEFAULT_THRESHOLDS,
    FEATURE_NAMES,
    FeatureVector,
    binarize_features,
    extract_features,
    map_patch_to_state,
    normalize_image,
)


def test_feature_names_and_bounds_on_known_patches():
    assert len(FEATURE_NAMES) == 8
    patches = [
        np.zeros((4, 4), dtype=np.uint8),
        np.full((4, 4), 255, dtype=np.uint8),
        np.indices((4, 4)).sum(axis=0).astype(np.uint8) * 255,
        np.dstack(
            [
                np.full((4, 4), 255, dtype=np.uint8),
                np.zeros((4, 4), dtype=np.uint8),
                np.zeros((4, 4), dtype=np.uint8),
            ]
        ),
    ]
    for patch in patches:
        features = extract_features(patch)
        assert len(features.values) == 8
        assert all(0.0 <= value <= 1.0 for value in features.values)
        state = binarize_features(features)
        assert is_integrity_valid(state)


def test_black_and_white_patches_have_expected_luminance_features():
    black = extract_features(np.zeros((3, 3), dtype=np.uint8))
    white = extract_features(np.full((3, 3), 255, dtype=np.uint8))
    assert black.values == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    assert white.values[0] == 1.0
    assert white.values[1:] == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)


def test_temporal_feature_is_exact_and_shape_checked():
    current = np.ones((2, 2), dtype=float)
    previous = np.zeros((2, 2), dtype=float)
    features = extract_features(current, previous)
    assert features.values[7] == 1.0
    try:
        extract_features(current, np.zeros((3, 3), dtype=float))
    except ValueError:
        pass
    else:
        raise AssertionError("shape mismatch was accepted")


def test_binarization_tie_rule_hysteresis_and_parity():
    at_threshold = FeatureVector(tuple(DEFAULT_THRESHOLDS))
    state = binarize_features(at_threshold)
    assert state[:8] == (1,) * 8
    assert state[8] == 0

    zero_previous = (0,) * 9
    inside_band = FeatureVector(tuple(DEFAULT_THRESHOLDS))
    held_zero = binarize_features(inside_band, previous_state=zero_previous)
    assert held_zero[:8] == (0,) * 8

    on_values = tuple(min(1.0, threshold + band) for threshold, band in zip(DEFAULT_THRESHOLDS, DEFAULT_HYSTERESIS, strict=True))
    switched_on = binarize_features(FeatureVector(on_values), previous_state=zero_previous)
    assert switched_on[:8] == (1,) * 8
    assert is_integrity_valid(switched_on)


def test_mapping_is_deterministic_and_normalization_is_strict():
    patch = np.arange(16, dtype=np.uint8).reshape(4, 4) * 16
    first = map_patch_to_state(patch)
    second = map_patch_to_state(patch)
    assert first == second
    assert np.allclose(normalize_image(patch), patch.astype(float) / 255.0)
    try:
        normalize_image(np.asarray([[2.0]], dtype=float))
    except ValueError:
        pass
    else:
        raise AssertionError("out-of-range floating image was accepted")
