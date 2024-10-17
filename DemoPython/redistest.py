import redis

# Redis Enterprise connection details
redis_host = 'localhost'
redis_port = 12000  # Example port for Redis Enterprise database

# Create the Redis client with password authentication
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    db = 1,
    decode_responses=True  # Optional, helps with automatic string decoding
)

# Test connection and set/get a key
try:
    # Ping Redis to test the connection
    response = redis_client.ping()
    print(f"Connected to Redis Enterprise: {response}")

    # Example of setting and getting a key
    redis_client.hset(0, mapping={"name": 'prueba',"value": 0})
    value = redis_client.hgetall(0)
    print(f"test_key: {value}")

except redis.AuthenticationError:
    print("Authentication failed. Please check your Redis Enterprise credentials.")
except redis.ConnectionError:
    print("Failed to connect to Redis Enterprise. Please check the host and port.")
