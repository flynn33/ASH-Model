# Mathematical Framework

## State space

The base state space is the binary hypercube:

```text
F_2^9 = {0,1}^9
```

It has 512 states and degree 9 at every vertex. The application-valid hyperplane is defined by the parity relation:

```text
x9 = x1 xor x2 xor x3 xor x4 xor x5 xor x6 xor x7 xor x8
```

This hyperplane has 256 states.

## Code layer

The canonical transform code is a rank-four doubly-even binary linear code with parameters `[9,4,4]`.

| Property | Result |
|---|---|
| Codewords | 16 |
| Minimum distance | 4 |
| Weight distribution | `{0:1, 4:14, 8:1}` |
| Nine-dimensional self-duality | false |
| Punctured code | self-dual doubly-even `[8,4,4]` |

## Decoder policy

Single-bit correction is guaranteed only through the strict decoder over codewords or known affine-orbit anchors. Two-bit codeword corruptions are rejected by policy.

## Projection and quotient

The code-orbit averaging operator is idempotent:

```text
T^2 = T
```

The punctured quotient gives the 16-vertex `Q8/C8` Adinkra layer with exact integer Garden matrices.

## Evidence

The authoritative proof record is:

- `proofs/computational-certificate.json`
- `proofs/computational-certificate.md`
- `tests/test_bits_hypercube.py`
- `tests/test_code.py`
- `tests/test_projection_adinkra.py`
