import numpy as np
from scipy.optimize import newton

# Parameters
N = 12_400  # Number of objects
C = 12_400    # Cache size 90%
alpha = 0.8    # Zipf distribution parameter

# Step 1: Generate the Zipf distribution for q(i)
q = np.array([1 / (i ** alpha) for i in range(1, N + 1)])
q /= np.sum(q)  # Normalize q to make it a proper probability distribution

# Step 2: Define the cache equation and its derivative
def cache_equation(tc):
    # Cache size equation
    return np.sum(1 - np.exp(-q * tc)) - C

def cache_equation_derivative(tc):
    # Derivative of the cache equation with respect to tc
    return np.sum(q * np.exp(-q * tc))

# Step 3: Solve using Newton's method
# Initial guess for t_C
initial_guess = 1.0

# Use scipy's newton method
t_C = newton(cache_equation, x0=initial_guess, fprime=cache_equation_derivative)

print(f"Converged to t_C = {t_C:.6f}")
