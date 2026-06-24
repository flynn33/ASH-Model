"""Bounded branch generation, geometry, weighting, and state semantics."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from typing import Sequence

from .bits import BitTuple, is_integrity_valid, normalize_bits, xor_bits
from .code import decode_affine, encode

ACTION_ORDER = ("0", "+", "-")
DEFAULT_ACTION_WEIGHTS = {"0": 0.5, "+": 0.25, "-": 0.25}
GEOMETRY_AXIOM = "F"
GEOMETRY_RULE = "FF[+F]F[-F]"
DEFAULT_BRANCH_DEPTH = 4
DEFAULT_TURN_DEGREES = 25.0
DEFAULT_LENGTH_DECAY = 0.72


@dataclass(frozen=True)
class BranchNode:
    path: str
    parent_path: str | None
    depth: int
    action: str
    message: BitTuple
    codeword: BitTuple
    state: BitTuple
    weight: float
    start: tuple[float, float]
    end: tuple[float, float]
    heading_radians: float
    segment_length: float


@dataclass(frozen=True)
class GeometrySegment:
    start: tuple[float, float]
    end: tuple[float, float]
    heading_radians: float
    stack_depth: int


def _validate_action_weights(action_weights: dict[str, float]) -> dict[str, float]:
    if set(action_weights) != set(ACTION_ORDER):
        raise ValueError(f"action weights must have keys {ACTION_ORDER}")
    normalized = {action: float(action_weights[action]) for action in ACTION_ORDER}
    if any(value < 0.0 for value in normalized.values()):
        raise ValueError("action weights may not be negative")
    total = sum(normalized.values())
    if abs(total - 1.0) > 1e-12:
        raise ValueError("action weights must sum to one")
    return normalized


def _next_message(message: BitTuple, action: str, level: int) -> BitTuple:
    bits = list(normalize_bits(message, length=4))
    if action == "+":
        bits[level % 4] ^= 1
    elif action == "-":
        bits[(level + 1) % 4] ^= 1
    elif action != "0":
        raise ValueError(f"unsupported branch action {action!r}")
    return tuple(bits)


def generate_branch_tree(
    source_state: Sequence[int],
    *,
    depth: int = DEFAULT_BRANCH_DEPTH,
    action_weights: dict[str, float] | None = None,
    turn_degrees: float = DEFAULT_TURN_DEGREES,
    length_decay: float = DEFAULT_LENGTH_DECAY,
) -> tuple[BranchNode, ...]:
    """Generate a complete deterministic ternary candidate tree.

    The action at level ``l`` toggles one of four message generators.  ``+``
    toggles generator ``l mod 4``; ``-`` toggles ``(l+1) mod 4``; ``0`` keeps
    the payload.  The encoded payload is a codeword, and every leaf state is
    ``source_state xor codeword``.  At depth four all 16 codewords are reached.
    """

    if depth < 0:
        raise ValueError("depth must be non-negative")
    if not (0.0 < length_decay <= 1.0):
        raise ValueError("length_decay must lie in (0,1]")
    source = normalize_bits(source_state)
    if not is_integrity_valid(source):
        raise ValueError("source state must satisfy coordinate-9 integrity")
    weights = _validate_action_weights(action_weights or DEFAULT_ACTION_WEIGHTS)
    turn = turn_degrees * pi / 180.0

    root = BranchNode(
        path="",
        parent_path=None,
        depth=0,
        action="root",
        message=(0, 0, 0, 0),
        codeword=encode((0, 0, 0, 0)),
        state=source,
        weight=1.0,
        start=(0.0, 0.0),
        end=(0.0, 0.0),
        heading_radians=pi / 2.0,
        segment_length=1.0,
    )
    nodes = [root]
    frontier = [root]
    for level in range(depth):
        next_frontier = []
        for parent in frontier:
            for action in ACTION_ORDER:
                heading = parent.heading_radians + ({"0": 0.0, "+": turn, "-": -turn}[action])
                segment_length = parent.segment_length * length_decay
                start = parent.end
                end = (
                    start[0] + segment_length * cos(heading),
                    start[1] + segment_length * sin(heading),
                )
                message = _next_message(parent.message, action, level)
                codeword = encode(message)
                node = BranchNode(
                    path=parent.path + action,
                    parent_path=parent.path,
                    depth=level + 1,
                    action=action,
                    message=message,
                    codeword=codeword,
                    state=xor_bits(source, codeword),
                    weight=parent.weight * weights[action],
                    start=start,
                    end=end,
                    heading_radians=heading,
                    segment_length=segment_length,
                )
                nodes.append(node)
                next_frontier.append(node)
        frontier = next_frontier
    return tuple(nodes)


def leaf_nodes(nodes: Sequence[BranchNode]) -> tuple[BranchNode, ...]:
    if not nodes:
        return ()
    maximum_depth = max(node.depth for node in nodes)
    return tuple(node for node in nodes if node.depth == maximum_depth)


def aggregate_leaf_weights(nodes: Sequence[BranchNode]) -> dict[BitTuple, float]:
    """Sum prior mass for leaves that map to the same four-bit operator."""

    totals: dict[BitTuple, float] = {}
    for node in leaf_nodes(nodes):
        totals[node.message] = totals.get(node.message, 0.0) + node.weight
    return dict(sorted(totals.items()))


def recover_branch_state(received: Sequence[int], source_state: Sequence[int]):
    """Strict one-bit recovery in the source state's affine code orbit."""

    return decode_affine(received, source_state)


def expand_geometry_lsystem(iterations: int) -> str:
    """Expand the historical deterministic rendering grammar.

    A hard iteration limit prevents accidental exponential memory use.  The
    semantic candidate tree is generated separately by ``generate_branch_tree``.
    """

    if iterations < 0 or iterations > 5:
        raise ValueError("geometry L-system iterations must be between 0 and 5")
    program = GEOMETRY_AXIOM
    for _ in range(iterations):
        program = "".join(GEOMETRY_RULE if symbol == "F" else symbol for symbol in program)
    return program


def interpret_geometry_lsystem(
    program: str,
    *,
    turn_degrees: float = 25.0,
    step: float = 1.0,
) -> tuple[GeometrySegment, ...]:
    """Interpret F,+,-,[,] as a deterministic two-dimensional turtle."""

    turn = turn_degrees * pi / 180.0
    position = (0.0, 0.0)
    heading = pi / 2.0
    stack: list[tuple[tuple[float, float], float]] = []
    segments: list[GeometrySegment] = []
    for symbol in program:
        if symbol == "F":
            end = (position[0] + step * cos(heading), position[1] + step * sin(heading))
            segments.append(
                GeometrySegment(
                    start=position,
                    end=end,
                    heading_radians=heading,
                    stack_depth=len(stack),
                )
            )
            position = end
        elif symbol == "+":
            heading += turn
        elif symbol == "-":
            heading -= turn
        elif symbol == "[":
            stack.append((position, heading))
        elif symbol == "]":
            if not stack:
                raise ValueError("unbalanced closing bracket")
            position, heading = stack.pop()
        else:
            raise ValueError(f"unsupported L-system symbol {symbol!r}")
    if stack:
        raise ValueError("unbalanced opening bracket")
    return tuple(segments)


def branch_certificate(depth: int = DEFAULT_BRANCH_DEPTH) -> dict[str, object]:
    source = (0,) * 9
    tree = generate_branch_tree(source, depth=depth)
    leaves = leaf_nodes(tree)
    aggregate = aggregate_leaf_weights(tree)
    return {
        "depth": depth,
        "node_count": len(tree),
        "leaf_count": len(leaves),
        "expected_leaf_count": 3**depth,
        "leaf_weight_sum": sum(node.weight for node in leaves),
        "unique_messages": len(aggregate),
        "all_leaf_states_integrity_valid": all(is_integrity_valid(node.state) for node in leaves),
        "coordinate_8_preserved": all(node.state[7] == source[7] for node in leaves),
        "geometry_rule": GEOMETRY_RULE,
        "geometry_segments_iteration_2": len(interpret_geometry_lsystem(expand_geometry_lsystem(2))),
    }
