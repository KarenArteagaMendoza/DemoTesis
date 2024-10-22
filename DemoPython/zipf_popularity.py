import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zipfian
import time


def muestra_zipf(N, s, sample_size):
    # Compute PMF and CDF
    ks = np.arange(1, N + 1)
    pmf = ks ** (-s)
    Z = np.sum(pmf)
    pmf /= Z
    cdf = np.cumsum(pmf)
    cdf[-1] = 1.0  # Ensure CDF ends at 1 due to numerical errors

    # Generate samples using inverse transform sampling
    U = np.random.uniform(0, 1, size=sample_size)
    samples = np.searchsorted(cdf, U) + 1  # +1 because ks starts from 1
    return ks, pmf, samples

# Parametros 
def graficar_muestra(N, s, sample_size, ks, pmf, samples):
    
   # Calculate counts
    counts = np.bincount(samples, minlength=N + 1)[1:N + 1]

    # Expected counts
    expected_counts = sample_size * pmf

    # Plot the results
    plt.figure(figsize=(12, 7))
    plt.loglog(ks, counts, label='Sampled Counts')
    plt.loglog(ks, expected_counts, label='Expected Counts', linestyle='--')
    plt.xlabel('Value (k)')
    plt.ylabel('Counts')
    plt.title(f'Zipf Distribution (s={s}): Sampled vs Expected Counts')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig('muestra.png')
    plt.close()

    counts, bins, patches = plt.hist(samples, bins=100, density=True, alpha=0.6, color='skyblue', label='Sampled Data')
    plt.plot(ks, pmf, 'k.-', alpha=0.5, label='expected count')
    plt.figure(figsize=(12, 7))
    plt.savefig('muestraCuentas.png')
    plt.close()



