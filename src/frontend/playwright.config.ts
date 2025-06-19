import { defineConfig, devices } from '@playwright/test';

/**
 * 🐎 Hoof Hearted - Playwright Configuration
 * External testing architecture: app in Docker, tests on host
 * Based on src-brain advanced Docker testing methodology
 */

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  
  // Reporting
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
  ],
  
  // Global test settings for external testing
  use: {
    // Target the Docker container (frontend-dev)
    baseURL: 'http://localhost:5174',
    
    // Visual settings
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // Timeouts optimized for Docker container testing
    actionTimeout: 15000,     // Slightly higher for container latency
    navigationTimeout: 45000,  // Higher for initial container startup
  },

  // Browser configurations for comprehensive testing
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    
    // Mobile testing for responsive monitoring dashboard
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  // External testing configuration - Docker handles the server
  webServer: {
    command: null,                          // No command - Docker handles it
    url: 'http://localhost:5174',           // Check Docker frontend container
    reuseExistingServer: true,              // Always use existing Docker
    timeout: 30 * 1000,                    // Wait up to 30s for container
  },

  // Test output directories
  outputDir: 'test-results/',
  
  // Test timeout settings
  timeout: 60 * 1000, // 1 minute per test
  expect: {
    timeout: 10 * 1000, // 10 seconds for assertions
  },
});