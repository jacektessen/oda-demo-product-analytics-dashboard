import logging
from typing import List, Dict
from datetime import datetime, timezone

from models.stats import ProductStats, BrandInfo

logger = logging.getLogger(__name__)


def calculate_stats(products: List[dict]) -> ProductStats:
    """Calculate various statistics from products data."""
    if not products:
        logger.warning("No products provided to calculate_stats")
        return None

    logger.info(f"Starting stats calculation for {len(products)} products")

    # Price ranges for grouping
    price_ranges = {"0-50": 0, "51-100": 0, "101-200": 0, "201-500": 0, "500+": 0}

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

    top_brands = sorted(valid_brands, key=lambda x: x.count, reverse=True)[:10]

    stats = ProductStats(
        total_products=len(products),
        average_price=round(total_price / len(products), 2) if products else 0,
        price_ranges=price_ranges,
        top_brands=top_brands,
        categories=categories,
        last_updated=datetime.now(timezone.utc).isoformat(),
    )

    logger.info(
        f"Stats calculation completed. Found {len(brands)} unique brands, {len(categories)} categories"
    )
    logger.info(f"Top brand: {top_brands[0].name if top_brands else 'None'}")

    return stats
