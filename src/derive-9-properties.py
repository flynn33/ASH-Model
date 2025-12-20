import sympy as sp

# 1. Refactorability of 9
def tau(n):
    """Compute the number of positive divisors of n."""
    return len(list(sp.divisors(n)))

n = 9
tau_9 = tau(n)
refactorable_9 = (n % tau_9 == 0)
divisors_9 = sp.divisors(n)
print(f"tau(9): {tau_9}")
print(f"9 % {tau_9} == 0: {refactorable_9}")
print(f"Divisors of 9: {divisors_9}")

# 2. Minimality as Smallest Odd Refactorable >1
odd_numbers = [3, 5, 7, 9]
tau_values = [tau(m) for m in odd_numbers]
refactorable_checks = [(m % tau_values[i] == 0) for i, m in enumerate(odd_numbers)]
print(f"Odd numbers <10: {odd_numbers}")
print(f"tau values: {tau_values}")
print(f"Refactorable checks: {refactorable_checks}")

# 3. Minimality as Smallest Odd Composite
composites = [m for m in odd_numbers if not sp.isprime(m)]
smallest_odd_composite = min(composites) if composites else None
print(f"Smallest odd composite: {smallest_odd_composite}")

# 4. Digital Root Invariance for Multiples of 9
def digital_root(m):
    """Compute digital root: iterative sum of digits mod 9, adjusted to 9 if 0 (non-zero m)."""
    dr = sum(int(d) for d in str(m)) % 9
    return 9 if dr == 0 else dr

multiples_9 = [9 * k for k in range(1, 5)]  # 9,18,27,36
digital_roots_adjusted = [digital_root(m) for m in multiples_9]
print(f"Multiples of 9: {multiples_9}")
print(f"Adjusted digital roots: {digital_roots_adjusted}")

# 5. 9's Role in Superstring Spatial Dimensions
D = sp.symbols('D')
eq = sp.Eq((sp.Rational(3, 2)) * D - 15, 0)
solution_D = sp.solve(eq, D)
spatial_dims = solution_D[0] - 1  # Subtract 1 temporal
print(f"Critical D: {solution_D[0]}")
print(f"Spatial dimensions: {spatial_dims}")
