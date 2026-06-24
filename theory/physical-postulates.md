# Physical Postulates

Status: finite-observer interpretation specified

## Scope

The ASH-Physics layer now has a conservative finite-observer interpretation.
It does not identify ASH states with measured spacetime events, matter fields,
or observed cosmological structure.  It defines a mathematically closed
candidate substrate on top of the verified finite ASH kernel.

## Postulates

### P1: Local finite state

A local ASH physical state is a parity-valid bit string

```text
x = (x_1, ..., x_9) in F_2^9
x_9 = x_1 xor ... xor x_8
```

The admissible state space is therefore the 256-state even-parity hyperplane.
The implementation entrypoint is `ash_model.physics.physical_state_space()`.

### P2: Observer state law

A finite observer does not observe a single hidden state directly.  The
observer state is a probability law `rho` over the 256 admissible states.
All bridge observables are functions of `rho`.

### P3: Microscopic evolution

The baseline microscopic dynamics is the lazy pair-flip Markov kernel
implemented by `ash_model.physics.pair_flip_transition(p)`.  At one step,
the state is unchanged with probability `1 - p`; otherwise one of the 36
coordinate pairs is selected uniformly and both bits are flipped.

This evolution preserves the admissible state space, is symmetric, is
normalized, and has the uniform admissible law as a stationary law.

### P4: Finite causal adjacency

Two admissible states are one microscopic event apart when they differ in
exactly two coordinates.  The event graph is the even-parity subgraph of the
9-cube with pair-flip edges.

The graph distance is

```text
d_pair(x, y) = HammingDistance(x, y) / 2
```

for admissible states `x` and `y`.

### P5: Bridge observables

The first frozen bridge map is dimensionless and finite-observer only:

```text
mean_hamming_weight(rho) = sum_x rho(x) |x|
order_parameter(rho) = 1 - 2 mean_hamming_weight(rho) / 9
entropy_bits(rho) = - sum_x rho(x) log2 rho(x)
parity_valid_probability(rho) = sum_{x admissible} rho(x)
```

The implementation entrypoint is `ash_model.physics.bridge_observables()`.

### P6: Scientific boundary

The postulates above define a closed finite stochastic model.  They do not
derive physical spacetime, SI-unit observables, gravitational dynamics,
quantum probabilities, or empirical cosmological predictions.  Those require
additional postulates and validation gates.

## Evidence

- `src/ash_model/physics.py`
- `tests/test_physics.py`
- `proofs/computational-certificate.json`
- `proofs/computational-certificate.md`

## Verification status

Implemented and computationally verified for the finite-observer scope.
