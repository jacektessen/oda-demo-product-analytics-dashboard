import { test, expect } from '@playwright/test';
import { StatsResponse } from './helpers/types';

const API_URL = process.env.FASTAPI_EXTERNAL_URL;

test.describe('Stats Endpoint', () => {
  test('should return valid stats structure', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/stats`);
    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);

    const data = await response.json() as StatsResponse;

    // Check data structure
    expect(data).toHaveProperty('total_products');
    expect(data).toHaveProperty('average_price');
    expect(data).toHaveProperty('price_ranges');
    expect(data).toHaveProperty('top_brands');
    expect(data).toHaveProperty('categories');
    expect(data).toHaveProperty('last_updated');
    expect(data).toHaveProperty('cache_info');

    // Validate data types
    expect(typeof data.total_products).toBe('number');
    expect(typeof data.average_price).toBe('number');
    expect(Array.isArray(data.top_brands)).toBeTruthy();
    expect(typeof data.last_updated).toBe('string');
  });

  test('should have valid price ranges', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/stats`);
    const data = await response.json() as StatsResponse;

    // Check price ranges structure
    const priceRanges = data.price_ranges;
    expect(priceRanges).toHaveProperty('0-50');
    expect(priceRanges).toHaveProperty('51-100');
    expect(priceRanges).toHaveProperty('101-200');
    expect(priceRanges).toHaveProperty('201-500');
    expect(priceRanges).toHaveProperty('500+');

    // Validate price ranges sum equals total products
    const totalInRanges = Object.values(priceRanges).reduce((a, b) => a + b, 0);
    expect(totalInRanges).toBe(data.total_products);
  });

  test('should have valid top brands', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/stats`);
    const data = await response.json() as StatsResponse;

    // Check top brands structure
    expect(data.top_brands.length).toBeLessThanOrEqual(10);
    
    data.top_brands.forEach(brand => {
      expect(brand).toHaveProperty('name');
      expect(brand).toHaveProperty('count');
      expect(typeof brand.name).toBe('string');
      expect(typeof brand.count).toBe('number');
      expect(brand.count).toBeGreaterThan(0);
    });

    // Verify brands are sorted by count in descending order
    const counts = data.top_brands.map(b => b.count);
    expect([...counts].sort((a, b) => b - a)).toEqual(counts);
  });

  test('should have valid cache info', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/stats`);
    const data = await response.json() as StatsResponse;

    const cacheInfo = data.cache_info;
    expect(cacheInfo).toHaveProperty('ttl_seconds');
    expect(cacheInfo).toHaveProperty('next_update_in');
    
    expect(typeof cacheInfo.ttl_seconds).toBe('number');
    expect(typeof cacheInfo.next_update_in).toBe('number');
    
    // TTL should be positive and less than or equal to 1 hour (3600 seconds)
    expect(cacheInfo.ttl_seconds).toBeGreaterThan(0);
    expect(cacheInfo.ttl_seconds).toBeLessThanOrEqual(3600);
    
    // next_update_in should be less than ttl_seconds
    expect(cacheInfo.next_update_in).toBeLessThan(cacheInfo.ttl_seconds);
  });

  test('should have consistent data between requests', async ({ request }) => {
    // Make two requests with small delay
    const response1 = await request.get(`${API_URL}/api/stats`);
    await new Promise(resolve => setTimeout(resolve, 1000));
    const response2 = await request.get(`${API_URL}/api/stats`);

    const data1 = await response1.json() as StatsResponse;
    const data2 = await response2.json() as StatsResponse;

    // Compare core metrics
    expect(data1.total_products).toBe(data2.total_products);
    expect(data1.average_price).toBe(data2.average_price);
    expect(data1.top_brands.length).toBe(data2.top_brands.length);

    // Cache TTL should be decreasing
    expect(data2.cache_info.ttl_seconds).toBeLessThan(data1.cache_info.ttl_seconds);
  });
});