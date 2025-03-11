import psycopg2
import random
import string

# Conexión a PostreSQL
conn = psycopg2.connect(
    host="rdi-postgres.cbyema2mun4d.us-east-2.rds.amazonaws.com",
    database="redis",
    user="redis_user",
    password="postgreSQL123",
    port = 5432
)

# Función para generar cadenas de texto aleatorias
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Función para generar registros aleatorios de 7KB
def generate_record(record_id):
    name = generate_random_string(1500)  
    value1 = generate_random_string(1500) 
    value2 = generate_random_string(1500) 
    value3 = generate_random_string(1500) 
    value4 = generate_random_string(500) 
    value5 = generate_random_string(500) 
    return (record_id, name, value1, value2, value3, value4, value5)

# Función para insertar datos a PostgreSQL
def insert_data_to_postgres(num_records):
    with conn.cursor() as cur:
        for record_id in range(1, 1 + num_records):
            record = generate_record(record_id)
            print(record_id)
            cur.execute("INSERT INTO test.tesis (id, name, value1, value2, value3, value4, value5) VALUES (%s, %s, %s, %s, %s, %s, %s)", record)
        conn.commit()


def main():
    # Necesito 100,000 registros para generar alrededor de 1.5GB 150,000
    num_records = 10_000 

    insert_data_to_postgres(num_records)

    print(f"{num_records} records added to PostgreSQL.")

if __name__ == "__main__":
    main()
