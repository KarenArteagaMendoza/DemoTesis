from scipy.optimize import minimize
import numpy as np

# Parameters
N = 76_000  # Number of objects
C = 76_000    # Cache size 90 %
alpha = 0.8    # Zipf distribution parameter

# Step 1: Generate the Zipf distribution for q(i)
q = np.array([1 / (i ** alpha) for i in range(1, N + 1)])
q /= np.sum(q)  # Normalize q to make it a proper probability distribution

# Step 2: Define an objective function to minimize the absolute difference
def objective(tc):
    return abs(np.sum(1 - np.exp(-q * tc)) - C)

# Step 3: Use a minimization function
result = minimize(objective, x0=[1.0], bounds=[(1e-6, 1e5)])

t_C = result.x[0]

print(f"Converged to t_C = {t_C:.6f}")
