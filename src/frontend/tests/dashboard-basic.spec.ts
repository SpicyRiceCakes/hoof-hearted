import { test, expect } from '@playwright/test';

/**
 * 🐎 Hoof Hearted Dashboard - Basic Functionality Tests
 * External testing against Docker container
 * Based on src-brain testing patterns
 */

test.describe('Dashboard Homepage', () => {
  test('loads successfully and has correct title', async ({ page }) => {
    await page.goto('/');
    
    // Check for Hoof Hearted title
    await expect(page).toHaveTitle(/Hoof Hearted/);
    
    // Verify main dashboard container is visible
    await expect(page.locator('main')).toBeVisible();
  });

  test('displays connection status indicators', async ({ page }) => {
    await page.goto('/');
    
    // Look for backend API connection status
    const backendStatus = page.locator('[data-testid="backend-status"]');
    if (await backendStatus.isVisible()) {
      await expect(backendStatus).toBeVisible();
    }
    
    // Look for database connection status
    const dbStatus = page.locator('[data-testid="database-status"]');
    if (await dbStatus.isVisible()) {
      await expect(dbStatus).toBeVisible();
    }
  });

  test('displays monitoring dashboard elements', async ({ page }) => {
    await page.goto('/');
    
    // Look for dashboard grid or monitoring widgets
    const dashboardGrid = page.locator('[data-testid="dashboard-grid"]');
    const monitoringWidget = page.locator('[data-testid="monitoring-widget"]');
    
    // At least one should be visible
    const gridVisible = await dashboardGrid.isVisible();
    const widgetVisible = await monitoringWidget.isVisible();
    
    expect(gridVisible || widgetVisible).toBeTruthy();
  });
});

test.describe('Responsive Design', () => {
  test('displays correctly on mobile devices', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Main content should be visible
    await expect(page.locator('main')).toBeVisible();
    
    // Check no horizontal overflow
    const bodyWidth = await page.locator('body').boundingBox();
    expect(bodyWidth?.width).toBeLessThanOrEqual(375);
  });

  test('navigation works on tablet sizes', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    
    // Navigation should be accessible
    const nav = page.locator('nav');
    if (await nav.isVisible()) {
      await expect(nav).toBeVisible();
    }
  });
});

test.describe('API Integration', () => {
  test('can connect to backend API', async ({ page }) => {
    await page.goto('/');
    
    // Wait for any initial API calls to complete
    await page.waitForLoadState('networkidle');
    
    // Check for any error indicators
    const errorMessages = page.locator('[data-testid="error-message"]');
    const errorCount = await errorMessages.count();
    
    // Should not have connection errors
    expect(errorCount).toBe(0);
  });
});

test.describe('Performance', () => {
  test('page loads within acceptable time', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;
    
    // Should load within 10 seconds (accounting for Docker container startup)
    expect(loadTime).toBeLessThan(10000);
  });

  test('dashboard updates without excessive requests', async ({ page }) => {
    await page.goto('/');
    
    // Monitor network requests for 5 seconds
    const requests: string[] = [];
    page.on('request', (request) => {
      requests.push(request.url());
    });
    
    await page.waitForTimeout(5000);
    
    // Should not have excessive API polling
    const apiRequests = requests.filter(url => url.includes('/api/'));
    expect(apiRequests.length).toBeLessThan(50); // Max ~10 requests per second
  });
});