import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Set

from services.redis import redis_client
from services.oda import fetch_all_products
from utils.stats import calculate_stats

CACHE_TTL = 3600  # 1 hour

logger = logging.getLogger(__name__)

background_tasks: Set[asyncio.Task] = set()

async def periodic_stats_update():
    """Periodically update product statistics in Redis."""
    logger.info("Periodic stats update task started - waiting 30 minutes before first update")
    await asyncio.sleep(30 * 60)

    while True:
        try:
            next_update = datetime.now() + timedelta(minutes=30)
            logger.info(f"Starting periodic stats update (next update scheduled for: {next_update.isoformat()})")

            products = await fetch_all_products()
            if products:
                stats = calculate_stats(products)
                if stats:
                    # Write to temporary key first
                    temp_key = "product:stats:temp"
                    redis_client.setex(temp_key, CACHE_TTL, json.dumps(stats.dict()))

                    # Atomic swap
                    redis_client.rename(temp_key, "product:stats")
                    logger.info(f"Successfully updated stats cache at {datetime.now().isoformat()}")

            await asyncio.sleep(30 * 60)

        except asyncio.CancelledError:
            logger.info("Periodic stats update task cancelled")
            break
        except Exception as e:
            logger.error(f"Error in periodic stats update: {str(e)}")
            await asyncio.sleep(5 * 60)

async def initial_stats_update():
    """Initial update of stats during startup."""
    try:
        logger.info("Performing initial stats update...")
        products = await fetch_all_products()
        if products:
            stats = calculate_stats(products)
            if stats:
                # Same atomic update pattern for initial update
                temp_key = "product:stats:temp"
                redis_client.setex(temp_key, CACHE_TTL, json.dumps(stats.dict()))
                redis_client.rename(temp_key, "product:stats")
                logger.info("Initial stats cache created successfully")
    except Exception as e:
        logger.error(f"Error in initial stats update: {str(e)}")