import aioredis

from fastapi_simple_mutex_server.config import service_config


async def Redis():
    """ Yields a aioRedis instance for use in a FastAPI Dependency Context Manager. """

    redis = await aioredis.create_redis_pool(service_config.redis_dsn)
    try:
        yield redis
    finally:
        redis.close()
        await redis.wait_closed()
