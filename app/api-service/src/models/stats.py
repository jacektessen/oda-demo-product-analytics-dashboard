from typing import Dict, List
from pydantic import BaseModel


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
