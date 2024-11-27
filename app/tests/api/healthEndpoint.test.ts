import { test, expect } from '@playwright/test';
import { HealthResponse } from './helpers/types';

const API_URL = 'http://localhost:8000';

test.describe('Health Endpoint', () => {
  test('should return healthy status when all services are up', async ({ request }) => {
    const response = await request.get(`${API_URL}/health`);
    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);

    const data = await response.json() as HealthResponse;
    
    expect(data).toHaveProperty('status');
    expect(data).toHaveProperty('redis');
    
    expect(data.status).toBe('healthy');
    expect(data.redis).toBe('connected');
  });

  test('should respond quickly (under 500ms)', async ({ request }) => {
    const start = Date.now();
    await request.get(`${API_URL}/health`);
    const duration = Date.now() - start;
    
    expect(duration).toBeLessThan(500);
  });

  test('health check response should be consistent', async ({ request }) => {
    // Make multiple requests
    const responses = await Promise.all([
      request.get(`${API_URL}/health`),
      request.get(`${API_URL}/health`),
      request.get(`${API_URL}/health`)
    ]);

    // All should be successful
    responses.forEach(response => {
      expect(response.status()).toBe(200);
    });

    // All should have same status
    const data = await Promise.all(responses.map(r => r.json()));
    const statuses = data.map(d => d.status);
    const redisStatuses = data.map(d => d.redis);

    expect(new Set(statuses).size).toBe(1);  // All statuses should be the same
    expect(new Set(redisStatuses).size).toBe(1);  // All redis statuses should be the same
  });
});