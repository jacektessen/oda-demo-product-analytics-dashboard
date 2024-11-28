from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import redis
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from typing import Optional, Dict, List
from pydantic import BaseModel
import httpx
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
# Na górze pliku, z innymi stałymi
ODA_API_BASE_URL = os.getenv('ODA_API_BASE_URL', 'https://oda.com/api/v1')
ODA_API_SEARCH_BASE_URL = f"{ODA_API_BASE_URL}/search/mixed/"
CACHE_TTL = 3600  # 1 hour
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
API_PORT = int(os.getenv('FASTAPI_PORT', '8000'))

class BrandInfo(BaseModel):
    name: str
    count: int

class ProductStats(BaseModel):
    total_products: int
    average_price: float
    price_ranges: Dict[str, int]
    top_brands: List[BrandInfo]
    categories: Dict[str, int]
    last_updated: str

def wait_for_redis(retries=5, delay=2):
    """Wait for Redis to become available"""
    for attempt in range(retries):
        try:
            client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'redis'),
                port=int(os.getenv('REDIS_PORT', REDIS_PORT)),
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

import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Set
from contextlib import asynccontextmanager
import signal

# Global variable to store background tasks
background_tasks: Set[asyncio.Task] = set()

async def periodic_stats_update():
    """Periodically update product statistics in Redis."""
    logger.info("Periodic stats update task started - waiting 30 minutes before first update")
    # First sleep for 30 minutes to avoid immediate update after initial
    await asyncio.sleep(30 * 60)  # 30 minutes in seconds
    
    while True:
        try:
            next_update = datetime.now() + timedelta(minutes=30)
            logger.info(f"Starting periodic stats update (next update scheduled for: {next_update.isoformat()})")
            
            # Fetch and process data
            products = await fetch_all_products()
            if products:
                stats = calculate_stats(products)
                if stats:
                    # Cache the results
                    redis_client.setex(
                        "product:stats",
                        CACHE_TTL,
                        json.dumps(stats.dict())
                    )
                    logger.info(f"Successfully updated stats cache at {datetime.now().isoformat()}")
            
            # Wait for next update
            await asyncio.sleep(30 * 60)  # 30 minutes in seconds
            
        except asyncio.CancelledError:
            logger.info("Periodic stats update task cancelled")
            break
        except Exception as e:
            logger.error(f"Error in periodic stats update: {str(e)}")
            # Wait 5 minutes before retrying on error
            await asyncio.sleep(5 * 60)

async def initial_stats_update():
    """Initial update of stats during startup."""
    try:
        logger.info("Performing initial stats update...")
        products = await fetch_all_products()
        if products:
            stats = calculate_stats(products)
            if stats:
                redis_client.setex(
                    "product:stats",
                    CACHE_TTL,
                    json.dumps(stats.dict())
                )
                logger.info("Initial stats cache created successfully")
    except Exception as e:
        logger.error(f"Error in initial stats update: {str(e)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global redis_client
    try:
        redis_client = wait_for_redis()
        
        # Perform initial update
        await initial_stats_update()
        
        # Start periodic update task
        task = asyncio.create_task(periodic_stats_update())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
        
        logger.info("Background tasks started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down background tasks...")
    for task in background_tasks:
        task.cancel()
    
    if background_tasks:
        await asyncio.gather(*background_tasks, return_exceptions=True)
    
    if redis_client:
        redis_client.close()
        
    logger.info("Cleanup completed")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def fetch_oda_data(page: int) -> Optional[dict]:
    """Fetch data from ODA API for a specific page."""
    async with httpx.AsyncClient() as client:
        try:
            params = {"q": "", "page": page}
            response = await client.get(ODA_API_SEARCH_BASE_URL, params=params)
            
            # Log the response status
            logger.info(f"HTTP Request: GET {ODA_API_SEARCH_BASE_URL} page={page} Status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 422:
                logger.info(f"Reached end of pagination at page {page}")
                return None
            else:
                logger.error(f"Failed to fetch data for page {page}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching page {page}: {str(e)}")
            return None

async def fetch_all_products() -> List[dict]:
    """Fetch all products from ODA API."""
    all_products = []
    page = 1
    
    while True:
        data = await fetch_oda_data(page)
        # Break if we got None (end of pagination or error)
        if data is None:
            logger.info(f"Finished fetching products. Total products: {len(all_products)}")
            break
            
        products = [item for item in data["items"] if item["type"] == "product"]
        all_products.extend(products)
        
        if not data["attributes"]["has_more_items"]:
            logger.info("No more items flag received")
            break
            
        page += 1
        await asyncio.sleep(0.5)  # Be nice to the API
    
    if not all_products:
        logger.warning("No products were fetched!")
        return []
        
    logger.info(f"Successfully fetched {len(all_products)} products")
    return all_products

def calculate_stats(products: List[dict]) -> ProductStats:
    """Calculate various statistics from products data."""
    if not products:
        logger.warning("No products provided to calculate_stats")
        return None
        
    logger.info(f"Starting stats calculation for {len(products)} products")
        
    # Price ranges for grouping
    price_ranges = {
        "0-50": 0,
        "51-100": 0,
        "101-200": 0,
        "201-500": 0,
        "500+": 0
    }
    
    total_price = 0
    brands = {}
    categories = {}
    
    for product in products:
        attrs = product["attributes"]
        
        try:
            price = float(attrs["gross_price"])
            
            # Update price ranges
            if price <= 50:
                price_ranges["0-50"] += 1
            elif price <= 100:
                price_ranges["51-100"] += 1
            elif price <= 200:
                price_ranges["101-200"] += 1
            elif price <= 500:
                price_ranges["201-500"] += 1
            else:
                price_ranges["500+"] += 1
                
            # Update total price for average calculation
            total_price += price
            
            # Update brand counts - handle None values
            brand = attrs.get("brand")
            if brand is not None and isinstance(brand, str) and brand.strip():
                brand_name = brand.strip()
                brands[brand_name] = brands.get(brand_name, 0) + 1
            else:
                brands["Unknown"] = brands.get("Unknown", 0) + 1
            
            # Update category counts (using client_classifiers as categories)
            for classifier in attrs.get("client_classifiers", []):
                category = classifier["name"]
                categories[category] = categories.get(category, 0) + 1
                
        except (KeyError, ValueError) as e:
            logger.warning(f"Error processing product {attrs.get('id')}: {str(e)}")
            continue
    
    # Calculate top brands with validation
    valid_brands = [
        BrandInfo(name=k, count=v) 
        for k, v in brands.items() 
        if isinstance(k, str) and isinstance(v, int)
    ]
    
    top_brands = sorted(
        valid_brands,
        key=lambda x: x.count,
        reverse=True
    )[:10]
    
    stats = ProductStats(
        total_products=len(products),
        average_price=round(total_price / len(products), 2) if products else 0,
        price_ranges=price_ranges,
        top_brands=top_brands,
        categories=categories,
        last_updated=datetime.now().isoformat()
    )
    
    logger.info(f"Stats calculation completed. Found {len(brands)} unique brands, {len(categories)} categories")
    logger.info(f"Top brand: {top_brands[0].name if top_brands else 'None'}")
    
    return stats

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global redis_client
    try:
        if redis_client and redis_client.ping():
            return {
                "status": "healthy",
                "redis": "connected",
                "timestamp": datetime.now().isoformat()
            }
    except redis.ConnectionError:
        pass
    return {
        "status": "unhealthy",
        "redis": "disconnected",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/stats")
async def get_stats():
    """Get product statistics from cache."""
    global redis_client
    cache_key = "product:stats"
    
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis connection not available")

    try:
        # Get from cache
        cached_data = redis_client.get(cache_key)
        if not cached_data:
            logger.warning("Cache miss in /api/stats - waiting for background update")
            raise HTTPException(
                status_code=503, 
                detail="Statistics are being calculated, please try again in a moment"
            )
            
        stats = json.loads(cached_data)
        
        # Add cache metadata
        ttl = redis_client.ttl(cache_key)
        stats["cache_info"] = {
            "ttl_seconds": ttl,
            "next_update_in": ttl - (CACHE_TTL - 30 * 60)  # Time until next periodic update
        }
        
        return stats
        
    except redis.RedisError as e:
        logger.error(f"Redis operation failed: {e}")
        raise HTTPException(status_code=500, detail="Redis operation failed")
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing data")

@app.get("/debug/redis")
async def debug_redis():
    """Debug endpoint to check Redis connection and cached keys."""
    global redis_client
    
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis connection not available")

    try:
        keys = redis_client.keys("*")
        debug_info = {
            "redis_connected": redis_client.ping(),
            "cached_keys": keys,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add TTL information for each key
        key_details = {}
        for key in keys:
            ttl = redis_client.ttl(key)
            value_type = redis_client.type(key)
            key_details[key] = {
                "ttl": ttl,
                "type": value_type
            }
        debug_info["key_details"] = key_details
        
        return debug_info
    except redis.RedisError as e:
        logger.error(f"Redis debug error: {str(e)}")
        raise HTTPException(status_code=500, detail="Redis connection error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)