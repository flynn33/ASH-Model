# Sector-Mixing Resolution Proof Note

## State Space

The sector-mixing workbench uses payload states `x in F_2^8`.  Each payload is
mapped to a parity-valid ASH state by appending the integrity coordinate

```text
x_9 = x_1 xor ... xor x_8
```

This mapping stays inside the repository's 256-state admissible ASH hyperplane.

## Payload Pair-Flip Obstruction

The payload pair-flip kernel chooses an unordered pair of payload coordinates
and flips both bits.  Every update changes the payload Hamming weight by
`-2`, `0`, or `+2`.  Therefore the parity of the payload Hamming weight is
invariant.

The 256 payload states split into two closed communicating classes:

- 128 even-weight payload states;
- 128 odd-weight payload states.

This obstruction is specific to the eight-payload-coordinate workbench.  It is
not a replacement statement for the repository's existing nine-coordinate
finite-observer pair-flip kernel.

## Sector Refresh

The sector-refresh kernel `S` chooses one payload coordinate uniformly and
flips it.  It then recomputes the ninth integrity coordinate.  A single payload
flip changes payload Hamming-weight parity, so `S` bridges the two payload
sectors while preserving ASH admissibility.

For `0 < epsilon <= 1`, the mixed kernel

```text
K_epsilon = (1 - epsilon) K_pair + epsilon S
```

allows moves between the two payload sectors.  For `0 < epsilon < 1` with
nonzero pair laziness, the workbench has the finite stochastic, symmetric, and
sector-bridging behavior verified by the tests.

## Spectrum

Walsh characters on `F_2^8` are indexed by mode weight `r` in `0..8`.

The non-lazy pair-flip eigenvalue is

```text
(((8 - 2r)^2 - 8) / (8 * 7))
```

With pair-flip probability `p`, the lazy pair eigenvalue is

```text
(1 - p) + p * (((8 - 2r)^2 - 8) / (8 * 7))
```

The sector-refresh eigenvalue is

```text
1 - r / 4
```

The mixed eigenvalue is

```text
(1 - epsilon) * lambda_pair + epsilon * lambda_refresh
```

For the former sector mode `r = 8`, the pair eigenvalue is `1` and the refresh
eigenvalue is `-1`, so the mixed value is

```text
1 - 2 * epsilon
```

That shift removes the unit sector obstruction for positive `epsilon`.

## Boundary

This proof note is a finite workbench statement.  It does not establish a
unit-bearing spacetime law, external observational fit, or empirical
cosmology result.
