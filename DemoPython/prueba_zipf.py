#import numpy as np

# Parameters for the Zipf distribution
# a = 1.1  # Exponent parameter
# s = 10000  # Maximum number (sample space 1 to 10,000)

# Generate a random sample of 1000 values from the Zipf distribution
# sample = np.random.zipf(a, 1000)

# Ensure all values are within the range 1 to 10,000
# sample = np.clip(sample, 1, s)

# print(sample)


#import matplotlib.pyplot as plt

# Generar una muestra aleatoria de 10,000 valores de la distribución Zipf

'''# Parametros
N = 100  # Número de valores posibles (el 1 es el más popular y el 50 es el menos popular)
a = 0.8   # Parámetro de la distribución

# Compute the normalized probabilities P(k)
k = np.arange(1, N + 1)
pk = 1 / k**a
H_Ns = np.sum(pk)
P = pk / H_Ns  # Normalized probabilities

# Generar 100000 muestras de la distribución Zipf 
sample_size = 100000
samples = np.random.choice(k, size=sample_size, p=P)

# Graficar el histograma de la muestra junto con los valores esperados
plt.figure(figsize=(12, 6))

count = np.bincount(samples)
# plt.bar(k, count[1:], alpha=0.5, label='sample count')
counts, bins, patches = plt.hist(samples, bins=np.arange(1, N + 2) - 0.5, density=True, alpha=0.6, color='skyblue', label='Sampled Data')
plt.plot(k, P, 'k.-', alpha=0.5, label='expected count')   
plt.semilogy()
plt.grid(alpha=0.4)
plt.legend()
plt.title(f'Zipf sample, a={0.8}, size={sample_size}')
plt.show()'''

'''import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 1000000  # Maximum value
s = 0.8      # Exponent parameter for the Zipf distribution
sample_size = 10000000  # Number of samples to generate

# Compute the PMF and CDF
ks = np.arange(1, N + 1)
pmf = 1 / ks ** s
Z = np.sum(pmf)  # Normalization constant
pmf /= Z
cdf = np.cumsum(pmf)

# Ensure the CDF ends at 1 due to numerical errors
cdf[-1] = 1.0

# Generate uniform random numbers
u = np.random.uniform(0, 1, size=sample_size)

# Use inverse transform sampling
# Since the CDF is over a large range, we can use interpolation
samples = np.searchsorted(cdf, u) + 1  # +1 to match ks starting from 1

# Calculate the counts of each value
counts = np.bincount(samples)[1:N+1]  # Skip zero index

# Compute the expected counts
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
plt.show()'''


import numpy as np
from scipy.stats import zipfian
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)

a, n = 0.8, 100
mean, var, skew, kurt = zipfian.stats(a, n, moments='mvsk')

x = np.arange(zipfian.ppf(0.01, a, n),
              zipfian.ppf(0.99, a, n))
samp = zipfian.pmf(x, a, n)
print(samp)
ax.plot(x, 1000*samp, 'bo', ms=8, label='zipfian pmf')
ax.vlines(x, 0, 1000*zipfian.pmf(x, a, n), colors='b', lw=5, alpha=0.5)

rv = zipfian(a, n)
ax.vlines(x, 0, 1000*rv.pmf(x), colors='k', linestyles='-', lw=1,
        label='frozen pmf')
ax.legend(loc='best', frameon=False)
plt.show()