from fastapi import APIRouter, HTTPException, Request
from datetime import datetime, timedelta, timezone
import json
import logging

from tasks.stats import CACHE_TTL

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    """Health check endpoint."""
    try:
        if request.app.state.redis.ping():
            return {
                "status": "healthy",
                "redis": "connected",
                "timestamp": datetime.now().isoformat()
            }
    except Exception:
        pass
    return {
        "status": "unhealthy",
        "redis": "disconnected",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/api/stats")
async def get_stats(request: Request):
    cache_key = "product:stats"
    redis = request.app.state.redis

    try:
        cached_data = redis.get(cache_key)
        if not cached_data:
            logger.warning("Cache miss in /api/stats - waiting for background update")
            raise HTTPException(
                status_code=503,
                detail="Statistics are being calculated, please try again in a moment"
            )

        stats = json.loads(cached_data)
        ttl = redis.ttl(cache_key)
        now = datetime.now(timezone.utc)
        next_update = now + timedelta(seconds=ttl - (CACHE_TTL - 30 * 60))

        stats["cache_info"] = {
            "ttl_seconds": ttl,
            "next_update_at": next_update.isoformat(timespec='milliseconds')
        }

        return stats

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing data")

@router.get("/debug/redis")
async def debug_redis(request: Request):
    """Debug endpoint to check Redis connection and cached keys."""
    redis = request.app.state.redis

    try:
        keys = redis.keys("*")
        debug_info = {
            "redis_connected": redis.ping(),
            "cached_keys": keys,
            "timestamp": datetime.now().isoformat()
        }

        key_details = {}
        for key in keys:
            ttl = redis.ttl(key)
            value_type = redis.type(key)
            key_details[key] = {
                "ttl": ttl,
                "type": value_type
            }
        debug_info["key_details"] = key_details

        return debug_info
    except Exception as e:
        logger.error(f"Redis debug error: {str(e)}")
        raise HTTPException(status_code=500, detail="Redis connection error")