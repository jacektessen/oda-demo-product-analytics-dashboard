import asyncio
import os
import logging
import redis
from fastapi import HTTPException

logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = None


async def init_redis_client():
    logger.info("Starting Redis initialization...")
    try:
        client = await wait_for_redis()
        if client is None:
            logger.error("wait_for_redis() returned None!")
            raise Exception("Failed to initialize Redis client")

        global redis_client
        redis_client = client
        logger.info("Redis client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Redis initialization failed: {e}")
        raise


async def wait_for_redis(retries=5, delay=2):
    for attempt in range(retries):
        try:
            logger.info(
                f"Attempt {attempt + 1} to connect to Redis at {REDIS_HOST}:{REDIS_PORT}"
            )
            client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30,
            )
            await asyncio.to_thread(client.ping)
            logger.info("Redis connection successful!")
            return client
        except redis.ConnectionError as e:
            logger.warning(f"Redis connection attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                logger.error("All Redis connection attempts failed")
                raise
            await asyncio.sleep(delay)


def get_redis_client(app):
    if not hasattr(app.state, "redis"):
        raise HTTPException(status_code=503, detail="Redis connection not available")
    return app.state.redis
