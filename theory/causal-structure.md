# Causal Structure

Status: finite event graph specified

## Event graph

The finite causal adjacency relation is the pair-flip graph on the admissible
state space `Omega`.  States `x` and `y` are adjacent when

```text
y = x xor e_i xor e_j
```

for distinct coordinates `i` and `j`.

This graph is the distance-two graph induced by the nine-dimensional
hypercube on the even-parity hyperplane.  It has:

```text
vertices: 256
degree: 36
undirected edges: 4608
adjacency spectrum: 36^1, 20^9, 8^36, 0^84, (-4)^126
Laplacian spectral gap: 16
```

## Propagation bound

For admissible states, the minimum number of microscopic pair-flip events
needed to connect `x` and `y` is

```text
d_pair(x, y) = HammingDistance(x, y) / 2
```

The implementation entrypoint is `ash_model.physics.graph_distance_bound()`.

## Locality statement

This is locality in finite ASH state space, not locality in physical spacetime.
A single microscopic event changes exactly two ASH coordinates and preserves
parity validity.  No spatial metric or light-cone structure is claimed.
The spectral gap above is a finite graph-mixing invariant, not a relativistic
speed of propagation.

## Coarse-graining behavior

The Hamming-weight background map respects the event graph because a pair
flip changes total Hamming weight by `-2`, `0`, or `+2`.  This produces a
closed five-level background equation over weights `0, 2, 4, 6, 8`.

## Evidence

- `ash_model.physics.graph_distance_bound`
- `ash_model.physics.weight_background_kernel`
- `ash_model.hypercube.pair_flip_adjacency_spectrum`
- `tests/test_physics.py`
- `tests/test_bits_hypercube.py`

## Verification status

Implemented and computationally verified for the finite event graph.
