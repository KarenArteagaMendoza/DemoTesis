import redis
import time
import random
import myIndex


# Conexión a Redis 
def conexionRedis():
    try: 
        node1 = {'host': 'localhost', 'port': 12000}
        return redis.Redis(host=node1['host'], port=node1['port'], decode_responses=True)
    except Exception:
        print("No se pudo establecer conexión con Redis")

# Get a Redis
def getR(conn, query):
    resp = myIndex.search(conn, query)
    return resp
    

def main():
    myIndex.tryIndex()
    clientR = conexionRedis()
    try:
        for i in range(200):
            random_key = random.randint(0, 10000)
            resp = getR(clientR, random_key)
            print(random_key, " - ", resp[0][0],  " - ", resp[0][1], " - ", resp[1])
    
    except Exception:
        print("No se pudo establecer la conexión")