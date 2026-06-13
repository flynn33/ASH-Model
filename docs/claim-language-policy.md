# ASH Claim-Language Policy - Skir

This policy prevents recurrence of unsupported claims.

## Required canonical phrase

Use:

```text
rank-4 doubly-even linear [9,4,4] code over F2^9, with coordinate 9 as the parity/integrity coordinate
```

## Avoid positive self-dual language

Do not claim that the Skir canonical code is self-dual. If necessary, say:

```text
The Skir canonical code is not self-dual.
```

## Error-correction language

Allowed:

```text
The decoder corrects unique single-bit errors around canonical codewords.
```

Not allowed:

```text
The simulation demonstrates robust error correction under random bit-flip noise.
```

## Gaussian / occupancy language

Allowed:

```text
Noisy hypercube mixing approaches the expected binomial/Haar occupancy envelope.
```

Not allowed:

```text
ASH codewords uniquely produce Gaussian convergence.
```

## Interpretation separation

ASH base docs must not add narrative interpretation language. Separate interpretations may build on ASH, but ASH base must use neutral terms such as coordinate 9 parity/integrity coordinate.
