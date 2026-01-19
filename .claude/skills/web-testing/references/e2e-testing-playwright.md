# E2E Testing with Playwright

## Setup

```bash
npm init playwright@latest
npx playwright install
```

## Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Login', () => {
  test('should login successfully', async ({ page }) => {
    await page.goto('http://localhost:3000/login');
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button:text("Login")');
    await page.waitForURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
});
```

## Selector Strategies

```typescript
// Preferred (accessibility-first)
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByLabel('Email').fill('user@example.com');

// Fallback
await page.locator('[data-testid="submit-btn"]').click();
```

## Common Patterns

### Wait for API
```typescript
const responsePromise = page.waitForResponse('**/api/users');
await page.click('button:text("Load")');
await responsePromise;
```

### Mock API
```typescript
await page.route('**/api/users', route =>
  route.fulfill({ status: 200, body: JSON.stringify([]) })
);
```

## Configuration

```typescript
export default defineConfig({
  workers: process.env.CI ? 2 : undefined,
  fullyParallel: true,
  use: {
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
  },
});
```

## Commands

```bash
npx playwright test                    # Run all
npx playwright test --ui               # UI mode
npx playwright test login.spec.ts      # Specific file
npx playwright codegen https://example.com  # Generate
npx playwright show-report             # View report
```

## CI/CD

```yaml
- run: npx playwright install --with-deps
- run: npx playwright test
- uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: playwright-report
    path: playwright-report/
```
