"""Deterministic image/video measurements and 9-bit ASH state encoding."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Sequence

import numpy as np

from .bits import BitTuple, is_integrity_valid, make_integrity_state, normalize_bits

FEATURE_NAMES = (
    "mean_luminance",
    "rms_contrast",
    "edge_energy",
    "texture_energy",
    "chroma_energy",
    "horizontal_gradient_energy",
    "vertical_gradient_energy",
    "temporal_change",
)

DEFAULT_THRESHOLDS = (0.50, 0.20, 0.12, 0.08, 0.10, 0.10, 0.10, 0.08)
DEFAULT_HYSTERESIS = (0.02, 0.02, 0.015, 0.015, 0.015, 0.015, 0.015, 0.02)


@dataclass(frozen=True)
class FeatureVector:
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.values) != 8:
            raise ValueError("ASH feature vectors contain exactly eight measured values")
        if any(not np.isfinite(value) or value < 0.0 or value > 1.0 for value in self.values):
            raise ValueError("feature values must be finite and lie in [0,1]")

    def as_dict(self) -> dict[str, float]:
        return dict(zip(FEATURE_NAMES, self.values, strict=True))


def normalize_image(image: np.ndarray | Sequence[object]) -> np.ndarray:
    """Normalize a grayscale/RGB/RGBA patch to finite float64 values in [0,1].

    Integer arrays use their dtype maximum.  Floating arrays are required to
    be pre-normalized; this strict rule avoids data-dependent hidden scaling.
    """

    array = np.asarray(image)
    if array.ndim not in (2, 3):
        raise ValueError("image must have shape HxW or HxWxC")
    if array.ndim == 3 and array.shape[2] not in (1, 3, 4):
        raise ValueError("channel count must be 1, 3, or 4")
    if array.shape[0] < 1 or array.shape[1] < 1:
        raise ValueError("image dimensions must be nonzero")
    if np.issubdtype(array.dtype, np.integer):
        maximum = np.iinfo(array.dtype).max
        normalized = array.astype(np.float64) / float(maximum)
    else:
        normalized = array.astype(np.float64)
    if not np.all(np.isfinite(normalized)):
        raise ValueError("image contains NaN or infinity")
    if float(np.min(normalized)) < 0.0 or float(np.max(normalized)) > 1.0:
        raise ValueError("floating image values must already lie in [0,1]")
    if normalized.ndim == 3 and normalized.shape[2] == 4:
        normalized = normalized[:, :, :3]
    return normalized


def luminance(image: np.ndarray | Sequence[object]) -> np.ndarray:
    """Return a deterministic luma plane in [0,1]."""

    normalized = normalize_image(image)
    if normalized.ndim == 2:
        return normalized
    if normalized.shape[2] == 1:
        return normalized[:, :, 0]
    coefficients = np.asarray([0.2126, 0.7152, 0.0722], dtype=np.float64)
    return normalized[:, :, :3] @ coefficients


def _forward_gradients(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    dx = np.zeros_like(values, dtype=np.float64)
    dy = np.zeros_like(values, dtype=np.float64)
    if values.shape[1] > 1:
        dx[:, :-1] = values[:, 1:] - values[:, :-1]
    if values.shape[0] > 1:
        dy[:-1, :] = values[1:, :] - values[:-1, :]
    return dx, dy


def _box_blur3(values: np.ndarray) -> np.ndarray:
    padded = np.pad(values, ((1, 1), (1, 1)), mode="edge")
    result = np.zeros_like(values, dtype=np.float64)
    for row_offset in range(3):
        for column_offset in range(3):
            result += padded[
                row_offset : row_offset + values.shape[0],
                column_offset : column_offset + values.shape[1],
            ]
    return result / 9.0


def extract_features(
    current: np.ndarray | Sequence[object],
    previous: np.ndarray | Sequence[object] | None = None,
) -> FeatureVector:
    """Extract the eight canonical measurements, each provably bounded [0,1]."""

    normalized = normalize_image(current)
    y = luminance(normalized)
    dx, dy = _forward_gradients(y)

    mean_luminance = float(np.mean(y))
    rms_contrast = float(min(1.0, 2.0 * np.std(y)))
    edge_energy = float(np.mean(np.sqrt(dx * dx + dy * dy)) / sqrt(2.0))
    texture_energy = float(np.mean(np.abs(y - _box_blur3(y))))

    if normalized.ndim == 3 and normalized.shape[2] >= 3:
        chroma_energy = float(np.mean(np.max(normalized[:, :, :3], axis=2) - np.min(normalized[:, :, :3], axis=2)))
    else:
        chroma_energy = 0.0

    horizontal_gradient = float(np.mean(np.abs(dx)))
    vertical_gradient = float(np.mean(np.abs(dy)))

    if previous is None:
        temporal_change = 0.0
    else:
        previous_y = luminance(previous)
        if previous_y.shape != y.shape:
            raise ValueError("current and previous patches must have identical spatial shape")
        temporal_change = float(np.mean(np.abs(y - previous_y)))

    values = tuple(
        float(np.clip(value, 0.0, 1.0))
        for value in (
            mean_luminance,
            rms_contrast,
            edge_energy,
            texture_energy,
            chroma_energy,
            horizontal_gradient,
            vertical_gradient,
            temporal_change,
        )
    )
    return FeatureVector(values)


def _validate_parameters(values: Sequence[float], name: str) -> tuple[float, ...]:
    parameters = tuple(float(value) for value in values)
    if len(parameters) != 8:
        raise ValueError(f"{name} must contain eight values")
    if any(not np.isfinite(value) or value < 0.0 or value > 1.0 for value in parameters):
        raise ValueError(f"{name} values must lie in [0,1]")
    return parameters


def binarize_features(
    features: FeatureVector | Sequence[float],
    *,
    previous_state: Sequence[int] | None = None,
    thresholds: Sequence[float] = DEFAULT_THRESHOLDS,
    hysteresis: Sequence[float] = DEFAULT_HYSTERESIS,
) -> BitTuple:
    """Map measurements to a parity-valid 9-bit ASH state.

    Without history, ties at a threshold map to one.  With history, a zero bit
    switches on at ``threshold+hysteresis`` and a one bit switches off below
    ``threshold-hysteresis``.  Coordinate 9 is then recomputed exactly.
    """

    feature_values = features.values if isinstance(features, FeatureVector) else tuple(float(value) for value in features)
    FeatureVector(tuple(feature_values))
    threshold_values = _validate_parameters(thresholds, "thresholds")
    hysteresis_values = _validate_parameters(hysteresis, "hysteresis")

    prior_payload: tuple[int, ...] | None = None
    if previous_state is not None:
        prior = normalize_bits(previous_state)
        if not is_integrity_valid(prior):
            raise ValueError("previous_state fails the coordinate-9 integrity relation")
        prior_payload = prior[:8]

    payload: list[int] = []
    for index, (value, threshold, band) in enumerate(
        zip(feature_values, threshold_values, hysteresis_values, strict=True)
    ):
        if prior_payload is None:
            payload.append(int(value >= threshold))
        elif prior_payload[index] == 0:
            payload.append(int(value >= min(1.0, threshold + band)))
        else:
            payload.append(int(not (value < max(0.0, threshold - band))))
    return make_integrity_state(payload)


def map_patch_to_state(
    current: np.ndarray | Sequence[object],
    previous: np.ndarray | Sequence[object] | None = None,
    *,
    previous_state: Sequence[int] | None = None,
    thresholds: Sequence[float] = DEFAULT_THRESHOLDS,
    hysteresis: Sequence[float] = DEFAULT_HYSTERESIS,
) -> tuple[FeatureVector, BitTuple]:
    features = extract_features(current, previous)
    state = binarize_features(
        features,
        previous_state=previous_state,
        thresholds=thresholds,
        hysteresis=hysteresis,
    )
    return features, state
