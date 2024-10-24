import numpy as np
from scipy.stats import zipfian

# Parameters
N = 12400  # Number of unique values
calls_per_second = 100  # Number of calls per second
alpha = 0.8  # Zipf distribution parameter (adjustable based on the data)


# Normalize the probabilities to ensure they sum to 1
probabilities = np.array([1 / (i ** alpha) for i in range(1, N + 1)])
probabilities /= np.sum(probabilities)  # Normalize

# Step 2: Simulate the requests
def simulate_requests(probabilities, calls_per_second, N):
    requested_values = set()  # Track unique values requested
    total_calls = 0           # Count total calls made
    while len(requested_values) < N:
        # Simulate a second of calls
        calls = np.random.choice(np.arange(1, N+1), p=probabilities, size=calls_per_second)
        requested_values.update(calls)  # Add the new requests to the set
        total_calls += calls_per_second
    return total_calls

# Run the simulation
total_calls_needed = simulate_requests(probabilities, calls_per_second, N)

# Step 3: Output the results
time_needed = total_calls_needed / calls_per_second  # In seconds
print(f"Total calls needed to request all {N} values: {total_calls_needed}")
print(f"Time needed (in seconds): {time_needed:.2f}")
print(f"Time needed (in minutes): {time_needed / 60:.2f}")
