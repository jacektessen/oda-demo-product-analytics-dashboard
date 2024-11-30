import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.redis import init_redis_client
from tasks.stats import periodic_stats_update, initial_stats_update, background_tasks
from api.endpoints import router as api_router
from config import API_PORT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting services initialization...")

        # Initialize Redis client
        logger.info("Initializing Redis client...")
        app.state.redis = await init_redis_client()
        logger.info(f"Redis client initialization completed: {app.state.redis}")

        logger.info("Starting initial stats update...")
        await initial_stats_update(app.state.redis)
        logger.info("Initial stats update completed")

        # Start periodic update task
        task = asyncio.create_task(periodic_stats_update(app.state.redis))
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        logger.info("Background tasks started successfully")

    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down background tasks...")
    for task in background_tasks:
        task.cancel()

    if background_tasks:
        await asyncio.gather(*background_tasks, return_exceptions=True)

    if app.state.redis:
        app.state.redis.close()

    logger.info("Cleanup completed")

app = FastAPI(lifespan=lifespan)
# Include the API routes
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)