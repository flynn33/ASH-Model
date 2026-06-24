"""End-to-end deterministic ASH patch-mapping reference pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .bits import BitTuple
from .branching import DEFAULT_BRANCH_DEPTH, BranchNode, generate_branch_tree, leaf_nodes
from .features import FeatureVector, map_patch_to_state
from .reconstruction import (
    DEFAULT_SCALE,
    DEFAULT_TOP_K,
    ReconstructionCandidate,
    generate_candidates,
    prune_candidates,
)


@dataclass(frozen=True)
class MappingResult:
    features: FeatureVector
    source_state: BitTuple
    branch_nodes: tuple[BranchNode, ...]
    candidates: tuple[ReconstructionCandidate, ...]
    selected: tuple[ReconstructionCandidate, ...]


def map_patch(
    current: np.ndarray | Sequence[object],
    previous: np.ndarray | Sequence[object] | None = None,
    *,
    previous_state: Sequence[int] | None = None,
    previous_reconstruction: np.ndarray | Sequence[object] | None = None,
    branch_depth: int = DEFAULT_BRANCH_DEPTH,
    scale: int = DEFAULT_SCALE,
    top_k: int = DEFAULT_TOP_K,
) -> MappingResult:
    """Map a patch to state, branches, reconstruction candidates, and top-k."""

    features, source_state = map_patch_to_state(
        current,
        previous,
        previous_state=previous_state,
    )
    tree = generate_branch_tree(source_state, depth=branch_depth)
    candidates = generate_candidates(
        current,
        leaf_nodes(tree),
        scale=scale,
        previous_candidate=previous_reconstruction,
    )
    selected = prune_candidates(candidates, top_k=top_k)
    return MappingResult(
        features=features,
        source_state=source_state,
        branch_nodes=tree,
        candidates=candidates,
        selected=selected,
    )
