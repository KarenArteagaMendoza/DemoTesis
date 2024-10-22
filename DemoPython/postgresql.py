import psycopg2
import random
import string

# PostgreSQL connection setup
conn = psycopg2.connect(
    host="localhost",
    database="redis",
    user="redis_user",
    password="post123",
    port = 5432
)

# Function to generate random string
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to generate random data for each record 1.1 KB
def generate_record(record_id):
    name = generate_random_string(1500)  # Random string of length 500
    value1 = generate_random_string(1500) # Random string of length 500
    value2 = generate_random_string(1500) # Random string of length 500
    value3 = generate_random_string(1500) # Random string of length 500
    value4 = generate_random_string(500) # Random string of length 500
    value5 = generate_random_string(500) # Random string of length 500
    return (record_id, name, value1, value2, value3, value4, value5)

# Function to insert data into PostgreSQL
def insert_data_to_postgres(num_records):
    with conn.cursor() as cur:
        for record_id in range(1, 1 + num_records):
            record = generate_record(record_id)
            print(record_id)
            cur.execute("INSERT INTO test.tesis (id, name, value1, value2, value3, value4, value5) VALUES (%s, %s, %s, %s, %s, %s, %s)", record)
        conn.commit()


def main():
    # Estimate around 1,000,000 records to reach 1 GB 
    # Necesito 1,000,000 para llenar la base
    num_records = 100000 

    # Insert records into PostgreSQL
    insert_data_to_postgres(num_records)

    print(f"{num_records} records added to PostgreSQL.")

if __name__ == "__main__":
    main()
