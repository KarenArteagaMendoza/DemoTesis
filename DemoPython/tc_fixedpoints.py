import numpy as np

# Parameters
N = 76_000  # Number of objects
C = 76_000    # Cache size 90 %
alpha = 0.8    # Zipf distribution parameter

# Step 1: Generate the Zipf distribution for q(i)
q = np.array([1 / (i ** alpha) for i in range(1, N + 1)])
q /= np.sum(q)  # Normalize q to make it a proper probability distribution

# Step 2: Define the cache equation (fixed-point iteration)
def fixed_point_iteration(tc):
    # Calculate the new tc based on the previous tc
    return C / np.sum(q * np.exp(-q * tc))

# Step 3: Iterate to find t_C
t_C = 1.0  # Initial guess
tolerance = 1e-6
max_iterations = 100

for i in range(max_iterations):
    new_t_C = fixed_point_iteration(t_C)
    if abs(new_t_C - t_C) < tolerance:
        print(f"Converged to t_C = {new_t_C:.6f} after {i+1} iterations")
        t_C = new_t_C
        break
    t_C = new_t_C
else:
    print("Did not converge after maximum iterations.")
