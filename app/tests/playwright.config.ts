import { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
  testDir: '.',
  timeout: 30000,
  retries: 2,
  workers: 1,
  reporter: [['list'], ['html']],
  use: {
    baseURL: process.env.API_URL || 'http://localhost:8000',
    extraHTTPHeaders: {
      'Accept': 'application/json',
    },
  },
  projects: [
    {
      name: 'API Tests',
      testMatch: /.*\.test\.ts/
    }
  ],
  globalTimeout: 600000,
  globalSetup: require.resolve('./global-setup'),
};

export default config;