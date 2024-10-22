from flask import Flask, jsonify
import psycopg2
import redis

# Implementar la función de Flask
app = Flask(__name__)

# Setup de Redis
redis_client = redis.Redis(
    host='localhost',
    port=12000,
    decode_responses=True  # Optional, helps with automatic string decoding
)
# Setup de PostgreSQL
post_client = psycopg2.connect(
    host="localhost",
    database="redis",
    user="redis_user",
    password="post123",
    port = 5432
)

# Consultar datos de PostgreSQL
def get_data_from_postgres(query):
    with post_client.cursor() as cur:
        cur.execute(query)
        result = cur.fetchone()
    return result

# Agregar datos a Redis con tiempo de expiración (aproximación)
def setRedis(key, data):
    # cambiar TTL
    # redis_client.setex(key, 300, json.dumps(data))
    redis_client.hset(key, mapping={"data": data[1],"value": data[2]})

# Actualizar el tiempo de expiración 
def updateTTL(key):
    # cambiar TTL
    redis_client.expire(key, 1500) # tiempo caracteristico aproximado para 76% del cache
    # para 90 % poner 1950



# Endpoint para obtener datos del caché o de la base de datos persistente
@app.route('/get_data/<int:key>', methods=['GET'])
def get_data(key):
    # Checar primero en Redis
    cached_data = redis_client.hgetall(key)

    
    if cached_data:
        #updateTTL(key)
        # Si el dato está en Redis regresarlo con la bandera "Redis"
        return jsonify({"source": 0, "id": key, "data": cached_data})
    
    # If not found in Redis, fetch from PostgreSQL
    query = f"SELECT id, name, value FROM test.tesis WHERE id = {key}"
    result = get_data_from_postgres(query)
    
    if result:
        data = {"name": result[1], "value": result[2]}
        # Agregar al cache
        setRedis(key, result)
        #updateTTL(key)
    
        # Return the data with a PostgreSQL flag 1: postgres
        return jsonify({"source": 1, "id": result[0], "data": data})
    else:
        return jsonify({"error": "Data not found"}), 404

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
