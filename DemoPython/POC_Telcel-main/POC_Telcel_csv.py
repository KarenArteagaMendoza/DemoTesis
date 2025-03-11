import csv
import random
from faker import Faker

# Inicializar Faker
fake = Faker()

# Tipos de perfil
perfiles = ["Básico", "Premium", "VIP"]

# Nombre del archivo CSV
csv_filename = "Cliente.csv"

# Generar 1,000,000 de registros
total_registros = 1_000

# Escribir en el archivo CSV
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Escribir encabezados
    writer.writerow(["id", "Nombre", "Perfil", "Saldo estimado", "Saldo facturado"])
    
    # Generar datos aleatorios
    for i in range(total_registros):
        id = i
        nombre = fake.name()
        perfil = random.choice(perfiles)
        saldo_estimado = round(random.uniform(100, 50000), 2)
        saldo_facturado = round(random.uniform(50, 40000), 2)
        
        writer.writerow([id, nombre, perfil, saldo_estimado, saldo_facturado])

print(f"Archivo '{csv_filename}' generado con {total_registros} registros.")
