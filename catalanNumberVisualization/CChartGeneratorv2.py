import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom
import math

def catalan_exact(n):
    """Exact Catalan number: C_n = binom(2n,n) / (n+1)"""
    try:
        return binom(2*n, n) / (n + 1)
    except:
        return 0

def catalan_stirling(n):
    """Full Stirling: 4^n / (√(π n^3))"""
    return (4**n) / math.sqrt(math.pi * n**3)

def catalan_sqrt(n):
    """Simplified: 4^n / √n"""
    return (4**n) / math.sqrt(n)

def catalan_linear(n):
    """Linear denom: 4^n / n"""
    return (4**n) / n

# Generate log-spaced n values from 10^0 to 10^4
n_values = np.arange(1,10000)

print(f"Using n from 1 to {n_values[-1]}")

# Calculate values
exact = np.array([catalan_exact(n) for n in n_values])
stirling = np.array([catalan_stirling(n) for n in n_values])
sqrt_approx = np.array([catalan_sqrt(n) for n in n_values])
linear_approx = np.array([catalan_linear(n) for n in n_values])

# Create plot with SAFE formatter
fig, ax = plt.subplots(figsize=(12, 8))

ax.loglog(n_values, exact, 'o-', label='Exact C_n', linewidth=3, markersize=6)
ax.loglog(n_values, stirling, '--', label='Stirling: 4^n/(n^(3/2)√π)', linewidth=2)
ax.loglog(n_values, sqrt_approx, '-.', label='Simplified: 4^n/√n', linewidth=2)
ax.loglog(n_values, linear_approx, ':', label='Linear: 4^n/n', linewidth=2)

# SAFE formatter - handles inf/nan
def safe_log_formatter(x, pos):
    if x <= 0 or not np.isfinite(x):
        return ''
    try:
        return f'$10^{{{int(np.log10(x)):.0f}}}$'
    except:
        return f'{x:.0e}'

ax.xaxis.set_major_formatter(plt.FuncFormatter(safe_log_formatter))
ax.yaxis.set_major_formatter(plt.FuncFormatter(safe_log_formatter))

ax.set_ylim(1e0, 1e10) 

ax.set_xlabel('n (log scale)')
ax.set_ylabel('C_n (log scale)')
ax.set_title('Catalan Numbers: Exact vs Asymptotic Approximations\n(Log-Log Scale)')
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3, which="both", ls="-", lw=0.5)

plt.tight_layout()
plt.show()

# Print sample values
print("\nSample values:")
for n in [5, 10, 15, 20]:
    print(f"n={n:2d}: exact={catalan_exact(n):10.0f}, "
          f"stirling={catalan_stirling(n):10.0f}, "
          f"√n={catalan_sqrt(n):10.0f}, "
          f"n={catalan_linear(n):10.0f}")
