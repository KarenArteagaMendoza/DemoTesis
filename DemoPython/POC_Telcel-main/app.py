from flask import Flask, jsonify
import redis
import myIndex

# Implementar la función de Flask
app = Flask(__name__)

# Conexión de Redis
redis_client = redis.Redis(
    host="redis-19029.c16.us-east-1-3.ec2.redns.redis-cloud.com",
    port=19029,
    password="POC_Telcel",
    decode_responses=True 
)


# Agregar datos a Redis con tiempo de expiración (aproximación) como una transacción
def setRedis(key, data):
    redis_client.hset(key, mapping={"Nombre": data[1],"Perfil": data[2],"Saldo estimado": data[3],"Saldo facturado": data[4]})

# Endpoint para obtener datos de Redis
@app.route('/get_data/<int:key>', methods=['GET'])
def get_data(key):
    # Checar primero en Redis
    cached_data = redis_client.hgetall(key)
    
    if cached_data:
        return jsonify({"id ": key, "data ": cached_data})
    else:
        return jsonify({"error": "Data not found"}), 404
    
# Endpoint para realizar búsquedas en Redis Search
@app.route('/buscar/<string:query>', methods=['GET'])
def get_query(query):
    if query == "":
        return jsonify({"error": "Query no proporcionado"}), 400
    
    resultados = myIndex.buscar(query)
    return jsonify(resultados)

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)

