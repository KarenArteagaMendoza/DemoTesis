import requests
import random
import csv
import time


BASE_URL = "http://127.0.0.1:5000"

# Función para mandar una consulta a la aplicación e imprimir el resultado
def request_data(key):
    try:
        # Enviar un GET a la app
        response = requests.get(f'{BASE_URL}/get_data/{key}')
        if response.status_code == 200:
            data = response.json()
            return data # Regresar el dato solicitado
        else:
            print(f"Error: {response.status_code}")
            return { "id": -1, "data": 0}

    except Exception as e:
        print(f"Failed to retrieve data: {e}")
        return { "id":-1, "data": 0}
    


def request_query(query):
    response = requests.get(f'{BASE_URL}/get_query/{query}')

    if response.status_code == 200:
        resultados = response.json()
        print("Resultados de la búsqueda:")
        for r in resultados:
            print(r)
    else:
        print(f"Error en la solicitud: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    for cliente in range(100):
        print(request_data(cliente))
    
    request_query("John")


