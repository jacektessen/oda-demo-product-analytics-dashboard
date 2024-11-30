import os
import asyncio
from datetime import datetime
from typing import Optional, List
import logging

import httpx
from config import ODA_API_BASE_URL

logger = logging.getLogger(__name__)

# ODA API constants
ODA_API_SEARCH_BASE_URL = f"{ODA_API_BASE_URL}/search/mixed/"


async def fetch_oda_data(page: int) -> Optional[dict]:
    """Fetch data from ODA API for a specific page."""
    async with httpx.AsyncClient() as client:
        try:
            params = {"q": "", "page": page}
            response = await client.get(ODA_API_SEARCH_BASE_URL, params=params)

            # Log the response status
            logger.info(
                f"HTTP Request: GET {ODA_API_SEARCH_BASE_URL} page={page} Status: {response.status_code}"
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 422:
                logger.info(f"Reached end of pagination at page {page}")
                return None
            else:
                logger.error(
                    f"Failed to fetch data for page {page}: {response.status_code}"
                )
                raise httpx.HTTPError(f"HTTP {response.status_code}")

        except Exception as e:
            logger.error(f"Error fetching page {page}: {str(e)}")
            raise


async def fetch_all_products() -> List[dict]:
    """Fetch all products from ODA API."""
    all_products = []
    page = 1
    max_retries = 3

    while True:
        for attempt in range(max_retries):
            try:
                data = await fetch_oda_data(page)
                # Only None means end of pagination (422)
                if data is None:
                    logger.info(
                        f"Finished fetching products. Total products: {len(all_products)}"
                    )
                    return all_products

                products = [item for item in data["items"] if item["type"] == "product"]
                all_products.extend(products)

                if not data["attributes"]["has_more_items"]:
                    logger.info("No more items flag received")
                    return all_products

                break  # Successful attempt, break retry loop

            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(
                        f"Failed to fetch page {page} after {max_retries} attempts: {str(e)}"
                    )
                    raise
                logger.warning(
                    f"Attempt {attempt + 1} failed for page {page}: {str(e)}"
                )
                await asyncio.sleep(1)  # Wait before retry

        page += 1
        await asyncio.sleep(0.2)  # Be nice to the API
