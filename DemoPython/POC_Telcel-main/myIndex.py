import redis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search import Client

# Conexión a Redis
redis_client = redis.Redis(
    host="redis-19029.c16.us-east-1-3.ec2.redns.redis-cloud.com",
    port=19029,
    password="POC_Telcel",
    decode_responses=True 
)

# Nombre del índice
INDEX_NAME = "idx_clientes"

# Crear una instancia del cliente de búsqueda
search_client = Client(INDEX_NAME, redis_client)

def crear_indice():
    """Crea el índice en Redis Search."""
    try:
        search_client.drop_index()
    except Exception:
        pass  # Si el índice no existe, no hacer nada
    
    schema = (
        TextField("Nombre", weight=5.0),
        TextField("Perfil"),
        NumericField("Saldo estimado"),
        NumericField("Saldo facturado")
    )
    
    search_client.create_index(
        schema,
        definition=IndexDefinition(prefix=["cliente:"], index_type=IndexType.HASH)
    )
    
    print("Índice creado exitosamente.")

def buscar(query):
    try:
        result = search_client.search(query)
        return result.docs
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return []
    
if __name__ == "__main__":
    crear_indice()