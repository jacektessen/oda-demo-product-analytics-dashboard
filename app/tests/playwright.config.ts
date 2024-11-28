import { PlaywrightTestConfig } from '@playwright/test';
import * as path from 'path';
import * as dotenv from 'dotenv';

dotenv.config({
  path: path.resolve(__dirname, '../docker/.env')
});

const config: PlaywrightTestConfig = {
  testDir: '.',
  timeout: 30000,
  retries: 2,
  workers: 1,
  reporter: [['list'], ['html']],
  use: {
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