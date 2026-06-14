# Skir Code Validation

## Purpose

This document records the mathematical validation for the Skir canonical ASH code.

## Canonical code

Skir uses a parity-explicit rank-4 doubly-even linear `[9,4,4]` code over `F2^9`.

Coordinate 9 is the parity/integrity coordinate:

```text
c9 = c1 xor c2 xor c3 xor c4 xor c5 xor c6 xor c7 xor c8
```

Coordinate 8 is fixed to 0 in this canonical presentation. This is a neutral presentation fact and has no narrative interpretation in the ASH base repository.

## Validated properties

The tests in `tests/test_ash_code.py` verify:

- rank = 4;
- closure size = 16;
- all codewords have length 9;
- all codewords are doubly-even;
- minimum pairwise Hamming distance = 4;
- coordinate 9 is active;
- coordinate 9 equals parity of coordinates 1 through 8;
- every valid codeword decodes as valid;
- every single-bit error around every codeword corrects to the original codeword;
- double-bit errors are not silently corrected.

## Error-correction boundary

The code supports deterministic correction of a single bit when the explicit decoder is invoked.

Random bit-flip noise in visualization scripts is not itself a decoder and must not be documented as runtime error correction.

## Disallowed conclusion

This validation does not prove a physical cosmology. It validates the code-theoretic layer used by the Skir branch.
