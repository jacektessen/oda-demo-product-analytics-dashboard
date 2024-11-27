export interface BrandInfo {
  name: string;
  count: number;
}

export interface PriceRanges {
  '0-50': number;
  '51-100': number;
  '101-200': number;
  '201-500': number;
  '500+': number;
}

export interface CacheInfo {
  ttl_seconds: number;
  next_update_in: number;
}

export interface Categories {
  [key: string]: number;
}

export interface StatsResponse {
  total_products: number;
  average_price: number;
  price_ranges: PriceRanges;
  top_brands: BrandInfo[];
  categories: Categories;
  last_updated: string;
  cache_info: CacheInfo;
}

export interface HealthResponse {
  status: 'healthy' | 'unhealthy';
  redis: 'connected' | 'disconnected';
}