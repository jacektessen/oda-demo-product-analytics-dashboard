export interface ProductStats {
  total_products: number;
  average_price: number;
  price_ranges: {
    [key: string]: number;
  };
  top_brands: {
    name: string;
    count: number;
  }[];
  categories: {
    [key: string]: number;
  };
  last_updated: string;
  cache_info: {
    ttl_seconds: number;
    next_update_in: number;
  };
}