import requests
import random
import csv
import numpy as np
import zipf_popularity as zp
import matplotlib.pyplot as plt
import time


BASE_URL = "http://127.0.0.1:5000"
CSV_FILENAME = "request_results.csv"
ZIPF_CSV_FILENAME = "zipf_request_results.csv"

# Rango de posibles keys
DATA_ID_RANGE = (1, 100000)


# Función para mandar una consulta a la aplicación e imprimir el resultado
def request_data(key):
    try:
        # Enviar un GET a la app
        response = requests.get(f'{BASE_URL}/get_data/{key}')
        
        # Checar si la consulta fue exitosa
        if response.status_code == 200:
            data = response.json()
            return data 
        elif response.status_code == 404:
            print("Data not found.")
            return {"source": -1, "id": 0, "data": 0}
        else:
            print(f"Error: {response.status_code}")
            return {"source": -1, "id": 0, "data": 0}

    except Exception as e:
        print(f"Failed to retrieve data: {e}")
        return 4

# Function to make 500 random requests and store the results
def make_requests_and_export_to_csv(num_requests, data_id_range, filename):
    results = []

    # Loop to make the requests
    for i in range(num_requests):
        key = random.randint(data_id_range[0], data_id_range[1])
        data = request_data(key)
        # Append the result (request number, data_id, source) to the list
        print(f"Source: {data['source']} - ID: {data['id']}")
        results.append([i + 1, key, data['source']])

    # Write results to a CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Consulta", "ID", "Fuente"]) # 0: caché, 1: base de datos
        writer.writerows(results)
    
    print(f"Results exported to {filename}")


def zipfs_sample(num_requests, data_id_range):
    a = 1.1 # a es el parámetro de la distribucion zipfs
    # Generate a random sample of 1000 values from the Zipf distribution
    sample = np.random.zipf(a, num_requests)
    # Ensure all values are within the range 1 to 10,000
    sample = np.clip(sample, data_id_range[0], data_id_range[1])
    return sample


def make_zipf_requests_csv(num_requests, data_id_range, filename):
    results = []
    sample = zipfs_sample(num_requests, data_id_range)
    # Loop to make the requests
    i = 1
    for key in sample:
        data = request_data(key)
        # Append the result (request number, data_id, source) to the list
        print(f"Source: {data['source']} - ID: {data['id']}")
        results.append([i, key, data['source']])
        i += 1

    # Write results to a CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Consulta", "ID", "Fuente"]) # 0: caché, 1: base de datos
        writer.writerows(results)
    
    print(f"Results exported to {filename}")


def prueba(N, s, sample_size):
    ks, pmf, samples = zp.muestra_zipf(N, s, sample_size)
    zp.graficar_muestra(N, s, sample_size, ks, pmf, samples)
    cache_hits = 0
    hit_rate = 0.0
    i = 1
    rates = []

    # make_requests_and_export_to_csv(3000, DATA_ID_RANGE, CSV_FILENAME)
    # make_zipf_requests_csv(3000, DATA_ID_RANGE, ZIPF_CSV_FILENAME)
    for key in samples: # necesito 100000 para llenar la base
        start_time = time.time()
        data = request_data(key)
        if data['source'] == 0:
            cache_hits += 1
        hit_rate = cache_hits/i
        end_time = time.time()
        print(f'Consulta: {i}   |', f'Hit rate: {hit_rate}    |', f'Tiempo ejecución: {end_time - start_time}')
        rates.append(hit_rate)
        i += 1
    
    return rates

def graficar_hitrates(N, s, sample_size):
    rates = prueba(N, s, sample_size)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, sample_size + 1), rates, label='Hit Rate to First Database')
    plt.xlabel('Request Number')
    plt.ylabel('Hit Rate')
    plt.title('Hit Rate to First Database Over Time')
    plt.grid(True)
    plt.legend()
    plt.savefig('hit_rates.png')
    plt.show()

def llenar_cache():
    for key in range(100000):
        start_time = time.time()
        data = request_data(key)
        end_time = time.time()
        print(f'Tiempo entre consultas: {end_time - start_time}')


# Main function to initiate the process
if __name__ == "__main__":

    N = 76_000       # Maximum value (large N)
    s = 0.8           # Exponent parameter (s < 1)
    sample_size = 200_000  # Very large sample size
    #llenar_cache()
    graficar_hitrates(N, s, sample_size)

