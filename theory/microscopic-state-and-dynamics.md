# Microscopic State and Dynamics

Status: finite stochastic dynamics specified and verified

## State space

The microscopic state space is

```text
Omega = {x in F_2^9 : x_9 = x_1 xor ... xor x_8}
```

so `|Omega| = 256`.

## Discrete dynamics

For `p in [0,1]`, define the one-step Markov kernel `P_p` on `Omega` by

```text
P_p(x, x) = 1 - p
P_p(x, x xor e_i xor e_j) += p / C(9,2),  1 <= i < j <= 9
```

Every mask `e_i xor e_j` has even parity, so `P_p` is closed on `Omega`.
The non-lazy pair-flip adjacency graph has degree `C(9,2)=36`.

## Continuous-time generator

For rate `lambda >= 0`, define the generator `Q_lambda` by

```text
Q_lambda(x, x xor e_i xor e_j) += lambda / C(9,2)
Q_lambda(x, x) = -lambda
```

Rows of `Q_lambda` sum to zero and off-diagonal entries are non-negative.

## Exact graph spectrum

The pair-flip graph is the distance-two graph of `Q9` restricted to the
even-parity hyperplane.  Its adjacency spectrum is:

```text
eigenvalue  multiplicity
36          1
20          9
8           36
0           84
-4          126
```

The unnormalized Laplacian spectrum is:

```text
eigenvalue  multiplicity
0           1
16          9
28          36
36          84
40          126
```

For the continuous-time generator above, the slowest non-constant relaxation
rate is therefore `lambda * (1 - 20/36) = 4 lambda / 9`.

## Verified properties

The repository verifies:

- all generated states are parity-valid;
- `P_p` is row-stochastic;
- `P_p` is symmetric;
- the uniform law on `Omega` is stationary;
- `Q_lambda` is a valid symmetric continuous-time Markov generator;
- the exact pair-flip graph spectrum and finite spectral gap;
- the finite background equation induced by Hamming-weight lumping is
  row-stochastic.

## Physical interpretation

The dynamics is a finite stochastic substrate.  It should be read as a
candidate microscopic update law for finite-observer ASH research, not as a
derived law of physical spacetime.

## Evidence

- `ash_model.physics.pair_flip_transition`
- `ash_model.physics.pair_flip_generator`
- `ash_model.hypercube.pair_flip_adjacency_spectrum`
- `ash_model.hypercube.pair_flip_laplacian_spectrum`
- `tests/test_physics.py`
- `tests/test_bits_hypercube.py`
- `proofs/computational-certificate.json`

## Verification status

Implemented and computationally verified for finite ASH states.
