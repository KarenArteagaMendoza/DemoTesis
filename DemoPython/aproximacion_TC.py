import numpy as np
from scipy.optimize import newton, bisect, minimize

'''
Valores de N (tamaño de base de datos principal)
    12,400 - caché 100%
    15,500 - caché 80%
    24,800 - caché 50%
    62,000 - caché 20%
    124,000 - caché 10%
'''
# Parámetros
N = 24_800  # Tamaño de la base principal 
C = 12_400    # Tamaño del caché
ALPHA = 0.8    # Parámetro de la distribución de Zipf s > 0
CALLS = 100  # llamadas por segundo

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

# ------------------------------ Punto fijo --------------------------------
def fixed_point_iteration(tc):
    # Calculate the new tc based on the previous tc
    return C / np.sum(q * np.exp(-q * tc))

# Step 3: Iterate to find t_C
t_C = 1.0  # Initial guess
tolerance = 1e-6
max_iterations = 200

for i in range(max_iterations):
    new_t_C = fixed_point_iteration(t_C)
    if abs(new_t_C - t_C) < tolerance:
        mins = new_t_C/CALLS
        print(f"Punto fijo - t_C = {new_t_C:.6f} después de {i+1} iteraciones", f"|   Tiempo en minutos: {mins}")
        t_C = new_t_C
        break
    t_C = new_t_C
else:
    print("No converge despues de 200 iteraciones.")


