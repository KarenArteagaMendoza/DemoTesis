from flask import Flask, jsonify
import psycopg2
import redis

# Implementar la función de Flask
app = Flask(__name__)

# Conexión de Redis
redis_client = redis.Redis(
    host='localhost',
    port=12000,
    decode_responses=True 
)
# Conexión de PostgreSQL
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

# Agregar datos a Redis con tiempo de expiración (aproximación) como una transacción
def setRedis(key, data):
    # cambiar TTL
    with redis_client.pipeline() as pipe:
        pipe.hset(key, mapping={"name": data[1],"value1": data[2],"value2": data[3],"value3": data[4],"value4": data[5],"value5": data[6]})
        pipe.expire(key, 1500) 
        pipe.execute()
    

# Actualizar el tiempo de expiración para datos que ya están en el caché
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
        #updateTTL(key) # descomentar esta línea para pruebas de caché < 100%
        # Source: 0 - está en el caché
        return jsonify({"source": 0, "id": key, "data": cached_data})
    
    # Si la llave no está en Redis buscarla en PostgreSQL
    query = f"SELECT id, name, value1, value2, value3, value4, value5 FROM test.tesis WHERE id = {key}"
    result = get_data_from_postgres(query)
    
    if result:
        data = {"name": result[1], "value1": result[2],"value2": result[3],"value3": result[4],"value4": result[5],"value5": result[6]}
        # Agregar al caché
        setRedis(key, result)
    
        # Source: 1 - está en base de datos principal
        return jsonify({"source": 1, "id": result[0], "data": data})
    else:
        return jsonify({"error": "Data not found"}), 404

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
