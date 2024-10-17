import requests
import random
import csv
import numpy as np

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
            return 2
        else:
            print(f"Error: {response.status_code}")
            return 3

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
    a = 0.8 # a es el parámetro de la distribucion zipfs
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

# Main function to initiate the process
if __name__ == "__main__":
    # make_requests_and_export_to_csv(3000, DATA_ID_RANGE, CSV_FILENAME)
    # make_zipf_requests_csv(3000, DATA_ID_RANGE, ZIPF_CSV_FILENAME)
    for key in range(20000): # necesito 100000 para llenar la base
        data = request_data(key)
        # Append the result (request number, data_id, source) to the list
        # print(f"Source: {data['source']} - ID: {data['id']}")
