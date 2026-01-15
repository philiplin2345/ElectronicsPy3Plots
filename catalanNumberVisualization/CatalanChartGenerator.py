import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom
import math

def catalan_exact(n):
    """Exact Catalan number: C_n = binom(2n,n) / (n+1)"""
    return binom(2*n, n) / (n + 1)

def catalan_stirling(n):
    """Full Stirling: 4^n / (√(π n^3))"""
    return (4**n) / math.sqrt(math.pi * n**3)

def catalan_sqrt(n):
    """Simplified: 4^n / √n"""
    return (4**n) / math.sqrt(n)

def catalan_linear(n):
    """Linear denom: 4^n / n"""
    return (4**n) / n

# Generate data for n=1 to 20
n_values = np.arange(1, 21)
exact = [catalan_exact(n) for n in n_values]
stirling = [catalan_stirling(n) for n in n_values]
sqrt_approx = [catalan_sqrt(n) for n in n_values]
linear_approx = [catalan_linear(n) for n in n_values]

# Create log-scale plot
plt.figure(figsize=(12, 8))
plt.plot(n_values, np.log10(exact), 'o-', label='Exact C_n', linewidth=3, markersize=6)
plt.plot(n_values, np.log10(stirling), '--', label='Stirling: 4^n/(n^(3/2)√π)', linewidth=2)
plt.plot(n_values, np.log10(sqrt_approx), '-.', label='Simplified: 4^n/√n', linewidth=2)
plt.plot(n_values, np.log10(linear_approx), ':', label='Linear: 4^n/n', linewidth=2)

plt.yscale('log')
plt.xlabel('n')
plt.ylabel('log₁₀(C_n)')
plt.title('Catalan Numbers: Exact vs Asymptotic Approximations')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Print sample values
print("Sample values:")
for n in [5, 10, 15, 20]:
    print(f"n={n:2d}: exact={catalan_exact(n):8.0f}, "
          f"stirling={catalan_stirling(n):8.0f}, "
          f"√n={catalan_sqrt(n):8.0f}, "
          f"n={catalan_linear(n):8.0f}")
