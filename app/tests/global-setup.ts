import { request } from '@playwright/test';

async function globalSetup() {
  const apiUrl = process.env.API_URL || 'http://localhost:8000';
  const maxRetries = 30; // 30 prób
  const retryDelay = 2000; // 2 sekundy między próbami

  console.log(`Waiting for API to be ready at ${apiUrl}/health`);

  for (let i = 0; i < maxRetries; i++) {
    try {
      const context = await request.newContext();
      const response = await context.get(`${apiUrl}/health`);
      
      if (response.ok()) {
        const health = await response.json();
        if (health.status === 'healthy' && health.redis === 'connected') {
          console.log('API is ready!');
          return;
        }
      }
      
      console.log(`Attempt ${i + 1}/${maxRetries}: API not ready yet`);
    } catch (e) {
      console.log(`Attempt ${i + 1}/${maxRetries}: Connection failed`);
    }

    await new Promise(resolve => setTimeout(resolve, retryDelay));
  }

  throw new Error('API failed to become ready in time');
}

export default globalSetup;