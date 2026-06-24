"""Reference reconstruction operators, consistency scoring, and pruning.

This module is a deterministic CPU reference for validating ASH branch
semantics.  It is intentionally small and auditable; it is not a claim of
state-of-the-art image quality or a production GPU implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from typing import Sequence

import numpy as np

from .bits import BitTuple, bits_to_int, normalize_bits
from .branching import BranchNode, aggregate_leaf_weights
from .features import normalize_image

DEFAULT_SCALE = 2
DEFAULT_TOP_K = 4
DEFAULT_OPERATOR_STRENGTH = 0.125
DEFAULT_DATA_WEIGHT = 4.0
DEFAULT_EDGE_WEIGHT = 1.0
DEFAULT_TEMPORAL_WEIGHT = 0.5


@dataclass(frozen=True)
class ReconstructionCandidate:
    message: BitTuple
    prior_weight: float
    source_score: float
    total_score: float
    reconstruction: np.ndarray


def nearest_upsample(source: np.ndarray | Sequence[object], scale: int = DEFAULT_SCALE) -> np.ndarray:
    if scale < 1 or not isinstance(scale, int):
        raise ValueError("scale must be a positive integer")
    image = normalize_image(source)
    return np.repeat(np.repeat(image, scale, axis=0), scale, axis=1)


def block_mean_downsample(candidate: np.ndarray | Sequence[object], scale: int = DEFAULT_SCALE) -> np.ndarray:
    if scale < 1 or not isinstance(scale, int):
        raise ValueError("scale must be a positive integer")
    image = normalize_image(candidate)
    height, width = image.shape[:2]
    if height % scale or width % scale:
        raise ValueError("candidate dimensions must be divisible by scale")
    if image.ndim == 2:
        reshaped = image.reshape(height // scale, scale, width // scale, scale)
        return reshaped.mean(axis=(1, 3))
    channels = image.shape[2]
    reshaped = image.reshape(height // scale, scale, width // scale, scale, channels)
    return reshaped.mean(axis=(1, 3))


def _blur_axis(image: np.ndarray, axis: int) -> np.ndarray:
    pad_width = [(0, 0)] * image.ndim
    pad_width[axis] = (1, 1)
    padded = np.pad(image, pad_width, mode="edge")
    left_slice = [slice(None)] * image.ndim
    center_slice = [slice(None)] * image.ndim
    right_slice = [slice(None)] * image.ndim
    left_slice[axis] = slice(0, image.shape[axis])
    center_slice[axis] = slice(1, image.shape[axis] + 1)
    right_slice[axis] = slice(2, image.shape[axis] + 2)
    return (
        padded[tuple(left_slice)]
        + 2.0 * padded[tuple(center_slice)]
        + padded[tuple(right_slice)]
    ) / 4.0


def _box_blur(image: np.ndarray) -> np.ndarray:
    return _blur_axis(_blur_axis(image, 0), 1)


def apply_operator(
    source: np.ndarray | Sequence[object],
    message: Sequence[int],
    *,
    scale: int = DEFAULT_SCALE,
    strength: float = DEFAULT_OPERATOR_STRENGTH,
) -> np.ndarray:
    """Apply the operator selected by a four-bit decoded payload.

    m1: horizontal-detail injection
    m2: vertical-detail injection
    m3: isotropic-detail injection
    m4: isotropic-detail suppression (regularization)
    """

    selector = normalize_bits(message, length=4)
    if strength < 0.0 or strength > 0.5:
        raise ValueError("strength must lie in [0,0.5]")
    baseline = nearest_upsample(source, scale)
    horizontal_detail = baseline - _blur_axis(baseline, 1)
    vertical_detail = baseline - _blur_axis(baseline, 0)
    isotropic_detail = baseline - _box_blur(baseline)
    result = baseline.copy()
    if selector[0]:
        result += strength * horizontal_detail
    if selector[1]:
        result += strength * vertical_detail
    if selector[2]:
        result += strength * isotropic_detail
    if selector[3]:
        result -= strength * isotropic_detail
    return np.clip(result, 0.0, 1.0)


def _gradient_energy(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    dx = np.zeros_like(values, dtype=np.float64)
    dy = np.zeros_like(values, dtype=np.float64)
    if values.shape[1] > 1:
        dx[:, :-1, ...] = values[:, 1:, ...] - values[:, :-1, ...]
    if values.shape[0] > 1:
        dy[:-1, :, ...] = values[1:, :, ...] - values[:-1, :, ...]
    return dx, dy


def source_consistency_score(
    source: np.ndarray | Sequence[object],
    candidate: np.ndarray | Sequence[object],
    *,
    scale: int = DEFAULT_SCALE,
    previous_candidate: np.ndarray | Sequence[object] | None = None,
    data_weight: float = DEFAULT_DATA_WEIGHT,
    edge_weight: float = DEFAULT_EDGE_WEIGHT,
    temporal_weight: float = DEFAULT_TEMPORAL_WEIGHT,
) -> float:
    """Score a candidate by deterministic source, edge, and temporal losses."""

    source_image = normalize_image(source)
    candidate_image = normalize_image(candidate)
    reduced = block_mean_downsample(candidate_image, scale)
    if reduced.shape != source_image.shape:
        raise ValueError("downsampled candidate shape does not match source")
    data_loss = float(np.mean((reduced - source_image) ** 2))
    source_dx, source_dy = _gradient_energy(source_image)
    reduced_dx, reduced_dy = _gradient_energy(reduced)
    edge_loss = float(np.mean((source_dx - reduced_dx) ** 2 + (source_dy - reduced_dy) ** 2) / 2.0)
    temporal_loss = 0.0
    if previous_candidate is not None:
        previous = normalize_image(previous_candidate)
        if previous.shape != candidate_image.shape:
            raise ValueError("previous candidate shape mismatch")
        temporal_loss = float(np.mean((candidate_image - previous) ** 2))
    loss = data_weight * data_loss + edge_weight * edge_loss + temporal_weight * temporal_loss
    return float(exp(-loss))


def generate_candidates(
    source: np.ndarray | Sequence[object],
    leaves: Sequence[BranchNode],
    *,
    scale: int = DEFAULT_SCALE,
    previous_candidate: np.ndarray | Sequence[object] | None = None,
) -> tuple[ReconstructionCandidate, ...]:
    """Aggregate duplicate leaves, apply all reached operators, and score them."""

    if not leaves:
        raise ValueError("at least one branch node is required")
    priors = aggregate_leaf_weights(leaves)
    candidates = []
    for message, prior in priors.items():
        reconstruction = apply_operator(source, message, scale=scale)
        consistency = source_consistency_score(
            source,
            reconstruction,
            scale=scale,
            previous_candidate=previous_candidate,
        )
        total = log(max(prior, 1e-300)) + log(max(consistency, 1e-300))
        candidates.append(
            ReconstructionCandidate(
                message=message,
                prior_weight=prior,
                source_score=consistency,
                total_score=total,
                reconstruction=reconstruction,
            )
        )
    return tuple(
        sorted(
            candidates,
            key=lambda candidate: (-candidate.total_score, bits_to_int(candidate.message)),
        )
    )


def prune_candidates(
    candidates: Sequence[ReconstructionCandidate],
    *,
    top_k: int = DEFAULT_TOP_K,
) -> tuple[ReconstructionCandidate, ...]:
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    ordered = sorted(
        candidates,
        key=lambda candidate: (-candidate.total_score, bits_to_int(candidate.message)),
    )
    return tuple(ordered[:top_k])
