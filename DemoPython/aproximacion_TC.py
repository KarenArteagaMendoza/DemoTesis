import numpy as np
from scipy.optimize import newton, bisect, minimize

'''
Valores de N (tamaño de base de datos principal)
    13_800 - caché 100%
    17_250 - caché 80%
    27_600 - caché 50%
    69_000 - caché 20%
    138_000 - caché 10%
'''
# Parámetros
N = 69_000  # Tamaño de la base principal 
C = 13_800    # Tamaño del caché
ALPHA = 0.8    # Parámetro de la distribución de Zipf s > 0
CALLS = 74  # llamadas por segundo 84

# Generar la distribución de Zipf para q(i)
q = np.array([1 / (i ** ALPHA) for i in range(1, N + 1)])
q /= np.sum(q)  # Normalizar el arreglo

# ------------------------------ Método de Newton --------------------------------
# Definir las ecuaciones del caché y derivada 
def cache_equation(tc):
    # Cache size equation
    return np.sum(1 - np.exp(-q * tc)) - C

def cache_equation_derivative(tc):
    # Derivative of the cache equation with respect to tc
    return np.sum(q * np.exp(-q * tc))

def metodo_newton():
    inicio = 1.0
    t_c = newton(cache_equation, x0=inicio, fprime=cache_equation_derivative)
    return t_c

newt = metodo_newton()
segs = newt/CALLS
print(f"Newton - t_C = {newt:.6f}", f"|   Segundos: {segs}", f"|   Minutos: {segs/60}")

# ------------------------------ Método de bisección --------------------------------
def metodo_gradiente():
    t_c = bisect(cache_equation, a=1e-6, b=1e10) 
    return t_c

gradient = metodo_gradiente()
segs = gradient/CALLS
print(f"Gradiente - t_C = {gradient:.6f}", f"|   Segundos: {segs}", f"|   Minutos: {segs/60}")

# ------------------------------ Optimización numérica --------------------------------
# Problema de programación: minimizar la diferencia absoluta de C = sum(1-e^-q(i)tc)
def objective(tc):
    return abs(np.sum(1 - np.exp(-q * tc)) - C)

# Minimizar la función objetivo con el punto inicial x0 = 1
# Restrición 1e-6< tc <1e7
def optnum():
    result = minimize(objective, x0=[1.0], bounds=[(1e-6, 1e7)])
    return result.x[0]


optim = optnum()
segs = optim/CALLS
print(f"OptNum - t_C = {optim:.6f}", f"|   Segundos: {segs}", f"|   Minutos: {segs/60}")


'''
Aproximaciones:
con 78 consultas por segundo
80% - 861 segundos
50% - 497 segundos
20% - 327 segundos
10% - 277 segundos
'''
