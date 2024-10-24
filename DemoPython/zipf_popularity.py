import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zipfian
import time

# Función para generar una muestra de distribución Zipf de tamaño "sample_size"
# Valores tomados de {1, 2, ... N} 
# s es el parámetro de la distribución s>0
def muestra_zipf(N, s, sample_size):
    # Computar funciones de densidad y distribución
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

# Función para graficar la cuenta de valores de la muestra
def graficar_muestra(N, s, sample_size, ks, pmf, samples):
    # Calcular cuentas
    counts = np.bincount(samples, minlength=N + 1)[1:N + 1]

    # Cuentas esperadas
    expected_counts = sample_size * pmf

    # Graficar resultados
    plt.figure(figsize=(12, 7))
    plt.loglog(ks, counts, label='Cuentas de la muestra')
    plt.loglog(ks, expected_counts, label='Cuentas esperadas', linestyle='--')
    plt.xlabel('Dato (k)')
    plt.ylabel('Cuentas')
    plt.title(f'Distribuciión Zipf (s={s}): Cuentas de la muestra vs esperadas')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig('muestra.png')
    plt.close()

    plt.figure(figsize=(12, 7))
    counts, bins, patches = plt.hist(samples, bins=100, density=True, alpha=0.6, color='skyblue', label='Muestra')
    plt.plot(ks, pmf, 'k.-', alpha=0.5, label='Cuentas esperadas')
    plt.savefig('muestraCuentas.png')
    plt.close()



