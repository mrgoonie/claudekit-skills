# Performance & Core Web Vitals Testing

## Core Web Vitals (Google Ranking Factor)

| Metric | Target | Description |
|--------|--------|-------------|
| LCP | < 2.5s | Largest Contentful Paint |
| CLS | < 0.1 | Cumulative Layout Shift |
| INP | < 200ms | Interaction to Next Paint |

## Lighthouse CI Setup

```json
{
  "ci": {
    "collect": { "url": ["https://example.com"], "numberOfRuns": 3 },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "largest-contentful-paint": ["warn", { "maxNumericValue": 2500 }]
      }
    }
  }
}
```

## GitHub Actions

```yaml
- run: npm install -g @lhci/cli@*
- run: lhci autorun
```

## Playwright Performance Test

```javascript
test('measure Core Web Vitals', async ({ page }) => {
  await page.goto('https://example.com');
  const metrics = await page.evaluate(() => ({
    lcp: performance.getEntriesByType('largest-contentful-paint')[0]?.startTime,
  }));
  expect(metrics.lcp).toBeLessThan(2500);
});
```

## Quick Performance Checks

```bash
npx lighthouse https://example.com --output=json
npx bundlesize                    # Bundle size check
npx webpack-bundle-analyzer dist/stats.json
```

## Optimization Checklist

### LCP
- [ ] Lazy load below-fold images
- [ ] Preload critical resources
- [ ] Use CDN

### CLS
- [ ] Reserve space for images (width/height)
- [ ] Font loading strategy (font-display: swap)

### INP
- [ ] Break long JavaScript tasks
- [ ] Code splitting
