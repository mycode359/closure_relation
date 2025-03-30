import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite
from math import factorial
from scipy.integrate import quad

# Normalized Hermite function
def psi(n, x):
    coeff = 1 / np.sqrt(2**n * factorial(n) * np.pi**0.25)
    return coeff * hermite(n)(x) * np.exp(-x**2 / 2)

# Parameters
x_prime = 1.0  # The point where delta function is centered
x_min, x_max = -3, 3
n_max = 20     # Number of terms in the summation

# Create x array
x = np.linspace(x_min, x_max, 1000)

# Compute the closure relation approximation
def closure_approx(x, x_prime, N_terms):
    """Approximate δ(x-x') using N_terms Hermite functions"""
    sum_val = np.zeros_like(x)
    for n in range(N_terms):
        sum_val += psi(n, x) * psi(n, x_prime)
    return sum_val

# Plot the approximation for different numbers of terms
plt.figure(figsize=(12, 8))

for N in [5, 10, 20, 50]:
    y = closure_approx(x, x_prime, N)
    plt.plot(x, y, label=f'N = {N} terms')

# Formatting
plt.title(f"Dirac Delta Approximation δ(x - {x_prime}) using Hermite Functions", fontsize=14)
plt.xlabel('x', fontsize=12)
plt.ylabel('Approximation', fontsize=12)
plt.axvline(x_prime, color='black', linestyle='--', alpha=0.5, label=f'x = {x_prime}')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# Save and show
plt.savefig('dirac_delta_approximation.png', dpi=300)
plt.show()

# Verification: Integral should be approximately 1
integral, _ = quad(lambda x: closure_approx(x, x_prime, n_max), -np.inf, np.inf)
print(f"Integral of approximation (should be 1): {integral:.6f}")

# Check sampling property for f(x) = x^2
def f(x):
    return x**2

approx_integral = np.trapz(f(x) * closure_approx(x, x_prime, n_max), x)
exact_value = f(x_prime)
print(f"Sampling test (f(x) = x²):")
print(f"Approximate integral: {approx_integral:.6f}")
print(f"Exact f({x_prime}): {exact_value:.6f}")
