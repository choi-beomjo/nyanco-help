import redis.asyncio as redis
import os


redis_pool = redis.ConnectionPool.from_url(
    f"redis://{os.getenv('REDIS_HOST', 'localhost')}:6379/0",
    max_connections=10,
    decode_responses=True
)

redis_client = redis.Redis(
    connection_pool=redis_pool
)
