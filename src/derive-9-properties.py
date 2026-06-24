#!/usr/bin/env python3
"""Reproduce limited arithmetic observations about the integer nine.

These observations are contextual and do not constitute evidence that nine is
physically privileged.  The executable ASH definition is given by the
canonical computational specification and code modules.
"""

from __future__ import annotations

from math import isqrt


def divisors(value: int) -> tuple[int, ...]:
    result = set()
    for candidate in range(1, isqrt(value) + 1):
        if value % candidate == 0:
            result.add(candidate)
            result.add(value // candidate)
    return tuple(sorted(result))


def divisor_count(value: int) -> int:
    return len(divisors(value))


def digital_root(value: int) -> int:
    if value == 0:
        return 0
    return 1 + (abs(value) - 1) % 9


def main() -> int:
    value = 9
    observations = {
        "divisors": divisors(value),
        "divisor_count": divisor_count(value),
        "refactorable": value % divisor_count(value) == 0,
        "smallest_odd_composite": all(candidate < value and (candidate < 2 or len(divisors(candidate)) == 2) for candidate in range(3, value, 2)),
        "sample_digital_roots": {multiple: digital_root(multiple) for multiple in (9, 18, 27, 36)},
    }
    for key, result in observations.items():
        print(f"{key}: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
