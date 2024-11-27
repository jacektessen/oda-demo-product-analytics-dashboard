from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import redis
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_redis(retries=5, delay=2):
    """Wait for Redis to become available"""
    for attempt in range(retries):
        try:
            client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'redis'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            client.ping()
            logger.info("Successfully connected to Redis")
            return client
        except redis.ConnectionError as e:
            if attempt == retries - 1:
                logger.error(f"Could not connect to Redis after {retries} attempts")
                raise
            logger.warning(f"Redis connection attempt {attempt + 1} failed, retrying in {delay} seconds...")
            time.sleep(delay)

# Initialize Redis client as None
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global redis_client
    try:
        redis_client = wait_for_redis()
    except Exception as e:
        logger.error(f"Failed to initialize Redis connection: {e}")
    
    yield
    
    # Shutdown
    if redis_client:
        await redis_client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    global redis_client
    try:
        if redis_client and redis_client.ping():
            return {"status": "healthy", "redis": "connected"}
    except redis.ConnectionError:
        pass
    return {"status": "unhealthy", "redis": "disconnected"}

@app.get("/api/dummy-data")
async def get_dummy_data():
    global redis_client
    
    # Generate fresh data if Redis is not available
    if not redis_client:
        logger.warning("Redis client not initialized, returning fresh data")
        return generate_dummy_data(from_cache=False)

    try:
        # Try to get data from Redis
        cached_data = redis_client.get('dummy_key')
        
        if cached_data:
            logger.info("Retrieved data from Redis cache")
            return {"source": "redis", "data": json.loads(cached_data)}
        
        # If no cached data, generate new data
        data = generate_dummy_data(from_cache=False)
        
        # Cache for 15 minutes
        redis_client.setex('dummy_key', 900, json.dumps(data["data"]))
        logger.info("Cached new data in Redis")
        
        return data
    except redis.RedisError as e:
        logger.error(f"Redis operation failed: {e}")
        return generate_dummy_data(from_cache=False)

def generate_dummy_data(from_cache: bool = True):
    dummy_data = {
        "products": [
            {"id": 1, "name": "Test Product 1", "price": 99.99},
            {"id": 2, "name": "Test Product 2", "price": 149.99}
        ],
        "timestamp": "2024-03-27T12:00:00Z"
    }
    return {"source": "redis" if from_cache else "generated", "data": dummy_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)