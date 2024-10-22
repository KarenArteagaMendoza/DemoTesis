from scipy.optimize import bisect
import numpy as np

# Parameters
N = 1_000_000  # Number of objects
C = 76_000    # Cache size 90 %
alpha = 0.8    # Zipf distribution parameter

# Step 1: Generate the Zipf distribution for q(i)
q = np.array([1 / (i ** alpha) for i in range(1, N + 1)])
q /= np.sum(q)  # Normalize q to make it a proper probability distribution

# Step 2: Define the cache equation
def cache_equation(tc):
    return np.sum(1 - np.exp(-q * tc)) - C

# Step 3: Use the bisection method
t_C = bisect(cache_equation, a=1e-6, b=1e5)  # Provide a wider interval

print(f"Converged to t_C = {t_C:.6f}")
