---
name: cloudflare-browser-rendering
description: Guide for implementing Cloudflare Browser Rendering - a headless browser automation API for screenshots, PDFs, web scraping, and testing. Use when automating browsers, taking screenshots, generating PDFs, scraping dynamic content, extracting structured data, or testing web applications. Supports REST API, Workers Bindings (Puppeteer/Playwright), MCP servers, and AI-powered automation. (project)
---

# Cloudflare Browser Rendering

Control headless browsers with Cloudflare's Workers Browser Rendering API. Automate tasks, take screenshots, convert pages to PDFs, extract data, and test web apps.

## When to Use This Skill

Use Cloudflare Browser Rendering when you need to:
- Take screenshots of web pages (PNG, JPEG, WebP)
- Generate PDFs from HTML/CSS or web pages
- Scrape dynamic content that requires JavaScript execution
- Extract structured data from websites (JSON-LD, Schema.org, Open Graph)
- Convert web pages to Markdown or extract links
- Automate browser interactions for testing or workflows
- Integrate browser automation with Cloudflare Workers
- Build AI-powered web scrapers with Workers AI
- Deploy MCP servers for LLM agent browser control
- Create web crawlers with Queues integration

## Integration Approaches

### 1. REST API (Simple, No Worker Required)

Quick integration using HTTP endpoints. Ideal for one-off tasks or external service integration.

**Available Endpoints:**
- `/screenshot` - Capture PNG/JPEG/WebP screenshots
- `/pdf` - Generate PDF documents
- `/content` - Extract fully rendered HTML
- `/markdown` - Convert pages to Markdown
- `/scrape` - Extract data via CSS selectors
- `/links` - Extract and analyze page links
- `/json` - Extract JSON-LD, Schema.org metadata
- `/snapshot` - Debug with multi-step browser states

**Authentication:**
```bash
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/screenshot" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Rate Limits:**
- 60 requests/minute
- 10 concurrent requests
- 100 burst per 5 minutes

### 2. Workers Bindings with Puppeteer (Low-Level Control)

Full Puppeteer API access within Cloudflare Workers for maximum control.

**Setup (wrangler.toml):**
```toml
name = "browser-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

browser = { binding = "MYBROWSER" }

[[kv_namespaces]]
binding = "KV"
id = "your-kv-namespace-id"
```

**Basic Screenshot Worker:**
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const browser = await puppeteer.launch(env.MYBROWSER);
    const page = await browser.newPage();

    await page.goto("https://example.com", { waitUntil: "networkidle2" });
    const screenshot = await page.screenshot({ type: "png" });

    await browser.close();

    return new Response(screenshot, {
      headers: { "Content-Type": "image/png" }
    });
  }
};
```

**Key Puppeteer Methods:**
- `puppeteer.launch(binding)` - Start new browser
- `browser.newPage()` - Create new page
- `page.goto(url, options)` - Navigate to URL
- `page.screenshot(options)` - Capture screenshot
- `page.content()` - Get HTML content
- `page.pdf(options)` - Generate PDF
- `page.evaluate(fn)` - Execute JS in page context
- `browser.disconnect()` - Disconnect keeping session alive
- `browser.close()` - Close and end session
- `puppeteer.connect(binding, sessionId)` - Reconnect to session

**Session Reuse (Critical for Cost Optimization):**
```typescript
// Disconnect instead of close to keep session alive
await browser.disconnect();

// Retrieve and reconnect to existing session
const sessions = await puppeteer.sessions(env.MYBROWSER);
const freeSession = sessions.find(s => !s.connectionId);

if (freeSession) {
  const browser = await puppeteer.connect(env.MYBROWSER, freeSession.sessionId);
}
```

### 3. Workers Bindings with Playwright (Testing Focus)

Playwright provides advanced testing features, assertions, and debugging.

**Setup:**
```bash
npm create cloudflare@latest -- browser-worker
cd browser-worker
npm install
wrangler dev  # Local testing
wrangler deploy  # Production
```

**Advanced Playwright Worker:**
```typescript
import { Hono } from "hono";

const app = new Hono<{ Bindings: Env }>();

app.get("/screenshot/:url", async (c) => {
  const browser = await c.env.MYBROWSER.launch();
  const page = await browser.newPage();

  await page.goto(c.req.param("url"));
  await page.waitForLoadState("networkidle");

  const screenshot = await page.screenshot({ fullPage: true });
  await browser.close();

  return c.body(screenshot, 200, {
    "Content-Type": "image/png"
  });
});

export default app;
```

**Playwright-Specific Features:**
- Storage state persistence with KV
- Tracing for debugging
- Advanced assertions (`expect(page).toHaveTitle()`)
- Network interception
- Multiple contexts for tab pooling

**Storage State Caching:**
```typescript
// Save authentication state
const state = await page.context().storageState();
await env.KV.put("auth-state", JSON.stringify(state));

// Restore authentication state
const savedState = await env.KV.get("auth-state", "json");
const context = await browser.newContext({ storageState: savedState });
```

### 4. MCP Server (AI Agent Integration)

Deploy Model Context Protocol server for LLM agent browser control.

**Features:**
- No vision models needed (uses accessibility tree)
- Simple natural language instructions
- Built on Playwright with Browser Rendering
- Pre-configured server templates available

**Use Case:** Enable AI agents to interact with web pages using structured accessibility data instead of screenshots.

### 5. Stagehand (AI-Powered Automation)

Natural language browser automation powered by AI.

**Example:**
```typescript
import { Stagehand } from "@stagehand-ai/stagehand";

const stagehand = new Stagehand(env.MYBROWSER);
await stagehand.init();

// Natural language instructions
await stagehand.act("click the login button");
await stagehand.act("fill in email with user@example.com");
const data = await stagehand.extract("get all product prices");

await stagehand.close();
```

## Configuration Patterns

### Wrangler Configuration (Browser Binding)

**Basic Setup:**
```toml
name = "my-browser-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

browser = { binding = "MYBROWSER" }
```

**Advanced Setup with Durable Objects and R2:**
```toml
browser = { binding = "MYBROWSER" }

[[durable_objects.bindings]]
name = "BROWSER"
class_name = "Browser"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-screenshots"

[[migrations]]
tag = "v1"
new_classes = ["Browser"]
```

### Timeout Configuration

**Default Timeouts:**
- `goToOptions.timeout`: 30s (max 60s)
- `waitForSelector`: up to 60s
- `actionTimeout`: up to 5 minutes
- Workers CPU time: 30s (standard), 15 minutes (unbound)

**Custom Timeout Examples:**
```typescript
// Puppeteer
await page.goto(url, {
  timeout: 60000,  // 60 seconds
  waitUntil: "networkidle2"
});

await page.waitForSelector(".content", { timeout: 45000 });

// Playwright
await page.goto(url, {
  timeout: 60000,
  waitUntil: "networkidle"
});

await page.locator(".element").click({ timeout: 10000 });
```

### Viewport and Screenshot Options

```typescript
// Set viewport size
await page.setViewport({ width: 1920, height: 1080 });

// Screenshot options
const screenshot = await page.screenshot({
  type: "png",           // "png" | "jpeg" | "webp"
  quality: 90,           // JPEG/WebP only, 0-100
  fullPage: true,        // Capture full scrollable page
  clip: {                // Crop to specific area
    x: 0, y: 0,
    width: 800,
    height: 600
  }
});
```

### PDF Generation Options

```typescript
const pdf = await page.pdf({
  format: "A4",
  printBackground: true,
  margin: {
    top: "1cm",
    right: "1cm",
    bottom: "1cm",
    left: "1cm"
  },
  displayHeaderFooter: true,
  headerTemplate: "<div>Header</div>",
  footerTemplate: "<div>Footer</div>"
});
```

## Limits and Pricing

### Free Plan
- **Usage:** 10 minutes/day
- **Concurrent:** 3 browsers max
- **Rate Limits:** 3 new browsers/minute, 6 requests/minute
- **Cost:** Free

### Paid Plan (Workers Paid)
- **Usage:** 10 hours/month included
- **Concurrent:** 30 browsers max
- **Rate Limits:** 30 new browsers/minute, 180 requests/minute
- **Overage Pricing:**
  - Additional usage: $0.09/hour
  - Additional concurrency: $2.00/concurrent browser

### REST API Pricing
- **Free:** 100 requests/day
- **Paid:** 10,000 requests/month included
- **Overage:** $0.09/additional hour of browser time

**Cost Optimization Tips:**
1. Use `disconnect()` instead of `close()` for session reuse
2. Enable Keep-Alive (up to 10 minutes)
3. Pool tabs using browser contexts instead of multiple browsers
4. Cache authentication state with KV storage
5. Implement Durable Objects for persistent sessions

## Common Use Cases

### 1. Screenshot Capture with Caching

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const targetUrl = url.searchParams.get("url");

    // Check cache
    const cached = await env.KV.get(targetUrl, "arrayBuffer");
    if (cached) {
      return new Response(cached, {
        headers: { "Content-Type": "image/png" }
      });
    }

    // Generate screenshot
    const browser = await puppeteer.launch(env.MYBROWSER);
    const page = await browser.newPage();
    await page.goto(targetUrl);
    const screenshot = await page.screenshot();
    await browser.close();

    // Cache for 24 hours
    await env.KV.put(targetUrl, screenshot, {
      expirationTtl: 86400
    });

    return new Response(screenshot, {
      headers: { "Content-Type": "image/png" }
    });
  }
};
```

### 2. PDF Certificate Generator

```typescript
async function generateCertificate(name: string, env: Env) {
  const browser = await puppeteer.launch(env.MYBROWSER);
  const page = await browser.newPage();

  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          body { font-family: Arial; text-align: center; padding: 50px; }
          h1 { color: #2c3e50; font-size: 48px; }
        </style>
      </head>
      <body>
        <h1>Certificate of Achievement</h1>
        <p>Awarded to: <strong>${name}</strong></p>
      </body>
    </html>
  `;

  await page.setContent(html);
  const pdf = await page.pdf({
    format: "A4",
    printBackground: true
  });

  await browser.close();
  return pdf;
}
```

### 3. AI-Powered Web Scraper

```typescript
import { Ai } from "@cloudflare/ai";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Render page with Browser Rendering
    const browser = await puppeteer.launch(env.MYBROWSER);
    const page = await browser.newPage();
    await page.goto("https://news.ycombinator.com");
    const content = await page.content();
    await browser.close();

    // Extract data with Workers AI
    const ai = new Ai(env.AI);
    const response = await ai.run(
      "@hf/thebloke/deepseek-coder-6.7b-instruct-awq",
      {
        messages: [
          {
            role: "system",
            content: "Extract top 5 article titles and URLs as JSON array"
          },
          {
            role: "user",
            content: content
          }
        ]
      }
    );

    return Response.json(response);
  }
};
```

### 4. Web Crawler with Queues

```typescript
export default {
  async queue(batch: MessageBatch<any>, env: Env): Promise<void> {
    const browser = await puppeteer.launch(env.MYBROWSER);

    for (const message of batch.messages) {
      const page = await browser.newPage();
      await page.goto(message.body.url);

      // Extract links
      const links = await page.evaluate(() => {
        return Array.from(document.querySelectorAll("a"))
          .map(a => a.href);
      });

      // Queue new links
      for (const link of links) {
        await env.QUEUE.send({ url: link });
      }

      await page.close();
    }

    await browser.close();
  }
};
```

### 5. Durable Objects for Persistent Sessions

```typescript
export class Browser {
  state: DurableObjectState;
  browser: any;
  lastUsed: number;

  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    this.lastUsed = Date.now();
  }

  async fetch(request: Request, env: Env) {
    // Initialize browser on first request
    if (!this.browser) {
      this.browser = await puppeteer.launch(env.MYBROWSER);
    }

    // Set keep-alive alarm
    this.lastUsed = Date.now();
    await this.state.storage.setAlarm(Date.now() + 10000);

    const page = await this.browser.newPage();
    await page.goto(new URL(request.url).searchParams.get("url"));
    const screenshot = await page.screenshot();
    await page.close();

    return new Response(screenshot, {
      headers: { "Content-Type": "image/png" }
    });
  }

  async alarm() {
    // Close browser if idle for 60 seconds
    if (Date.now() - this.lastUsed > 60000) {
      await this.browser?.close();
      this.browser = null;
    } else {
      await this.state.storage.setAlarm(Date.now() + 10000);
    }
  }
}
```

## Best Practices

### 1. Session Management
- **Always use `disconnect()` instead of `close()`** to keep sessions alive for reuse
- Implement session pooling to reduce concurrency costs
- Set Keep-Alive to maximum (10 minutes) for sustained workflows
- Track session IDs and connection states

### 2. Performance Optimization
- Cache frequently accessed content in KV storage
- Use browser contexts instead of multiple browsers for tab pooling
- Implement Durable Objects for persistent, reusable sessions
- Choose appropriate `waitUntil` strategy (load, networkidle0, networkidle2)
- Set realistic timeouts to avoid unnecessary waiting

### 3. Error Handling
- Implement Retry-After awareness for 429 rate limit errors
- Handle timeout errors gracefully with fallback strategies
- Check session availability before attempting reconnection
- Validate responses before caching or returning data

### 4. Cost Management
- Monitor usage via Cloudflare dashboard
- Use session reuse to dramatically reduce concurrency costs
- Implement intelligent caching strategies
- Consider batch processing for multiple URLs
- Set appropriate alarm intervals for Durable Objects cleanup

### 5. Security
- Validate all user-provided URLs before navigation
- Implement proper authentication for Workers endpoints
- Use Web Bot Auth signatures for additional protection
- Sanitize extracted content before processing
- Set appropriate CORS headers

## Troubleshooting

### Common Issues

**Timeout Errors:**
- Increase timeout: `page.goto(url, { timeout: 60000 })`
- Change waitUntil: `{ waitUntil: "domcontentloaded" }`
- Check network conditions and target site performance

**Rate Limit (429) Errors:**
- Implement exponential backoff with Retry-After header
- Reduce request frequency
- Upgrade to paid plan for higher limits

**Session Connection Failures:**
- Check session availability before connecting
- Handle race conditions with try-catch
- Verify browser hasn't timed out (10-minute Keep-Alive limit)

**Memory Issues:**
- Close pages when done: `await page.close()`
- Disconnect browsers properly: `await browser.disconnect()`
- Implement Durable Objects cleanup alarms

**Font Rendering Issues:**
- Use supported fonts (100+ pre-installed)
- Inject custom fonts via CDN or base64
- Check font-family declarations in CSS

## API Reference Quick Lookup

### REST API Global Parameters
- `url` (required) - Target webpage URL
- `waitDelay` - Wait time in milliseconds (0-30000)
- `goto.timeout` - Navigation timeout (0-60000ms)
- `goto.waitUntil` - Wait strategy (load, domcontentloaded, networkidle)

### Puppeteer Key Methods
- `puppeteer.launch(binding)` - Start browser
- `puppeteer.connect(binding, sessionId)` - Reconnect to session
- `puppeteer.sessions(binding)` - List active sessions
- `browser.newPage()` - Create new page
- `browser.disconnect()` - Disconnect keeping session alive
- `browser.close()` - Close and terminate session
- `page.goto(url, options)` - Navigate
- `page.screenshot(options)` - Capture screenshot
- `page.pdf(options)` - Generate PDF
- `page.content()` - Get HTML
- `page.evaluate(fn)` - Execute JavaScript

### Playwright Key Methods
- `env.MYBROWSER.launch()` - Start browser
- `browser.newPage()` - Create new page
- `browser.newContext(options)` - Create context with state
- `page.goto(url, options)` - Navigate
- `page.screenshot(options)` - Capture screenshot
- `page.pdf(options)` - Generate PDF
- `page.locator(selector)` - Find element
- `page.waitForLoadState(state)` - Wait for load
- `context.storageState()` - Get authentication state

## Supported Fonts

Pre-installed fonts include:
- **System:** Arial, Verdana, Times New Roman, Georgia, Courier New
- **Open Source:** Noto Sans, Noto Serif, Roboto, Open Sans, Lato
- **International:** Noto Sans CJK (Chinese, Japanese, Korean), Noto Sans Arabic, Hebrew, Thai
- **Emoji:** Noto Color Emoji

**Custom Font Injection:**
```html
<link href="https://fonts.googleapis.com/css2?family=Poppins" rel="stylesheet">
```

## Deployment Checklist

1. **Setup:**
   - [ ] Install Wrangler: `npm install -g wrangler`
   - [ ] Login: `wrangler login`
   - [ ] Create project: `npm create cloudflare@latest`

2. **Configuration:**
   - [ ] Add browser binding to `wrangler.toml`
   - [ ] Configure KV namespaces for caching (optional)
   - [ ] Set up R2 buckets for storage (optional)
   - [ ] Define Durable Objects if using persistent sessions

3. **Testing:**
   - [ ] Test locally: `wrangler dev`
   - [ ] Verify session management
   - [ ] Test timeout configurations
   - [ ] Validate error handling

4. **Deployment:**
   - [ ] Deploy to production: `wrangler deploy`
   - [ ] Monitor usage in Cloudflare dashboard
   - [ ] Set up alerts for rate limits
   - [ ] Verify cost optimization strategies

## Resources

- **Official Documentation:** https://developers.cloudflare.com/browser-rendering/
- **Puppeteer Docs:** https://pptr.dev/
- **Playwright Docs:** https://playwright.dev/
- **Workers Documentation:** https://developers.cloudflare.com/workers/
- **Wrangler CLI:** https://developers.cloudflare.com/workers/wrangler/

## Implementation Workflow

When implementing Cloudflare Browser Rendering:

1. **Choose Integration Method:**
   - REST API for simple, external integration
   - Workers + Puppeteer for low-level control
   - Workers + Playwright for testing and advanced features
   - MCP Server for AI agent integration
   - Stagehand for natural language automation

2. **Set Up Configuration:**
   - Create `wrangler.toml` with appropriate bindings
   - Install dependencies (`@cloudflare/puppeteer` or `@cloudflare/workers-playwright`)
   - Configure KV, R2, or Durable Objects as needed

3. **Implement Core Logic:**
   - Browser lifecycle management (launch, disconnect, close)
   - Navigation and waiting strategies
   - Content extraction or screenshot/PDF generation
   - Error handling and retries

4. **Optimize for Cost:**
   - Implement session reuse with `disconnect()`
   - Add Keep-Alive for sustained usage
   - Cache results in KV storage
   - Use Durable Objects for persistent sessions

5. **Deploy and Monitor:**
   - Test locally with `wrangler dev`
   - Deploy with `wrangler deploy`
   - Monitor usage and costs in dashboard
   - Adjust rate limiting and caching strategies

## Version Support

- **Puppeteer:** v22.13.1
- **Playwright:** v1.55.0
- **Node.js Compatibility:** Required for Workers integration
- **Browser Version:** Chromium-based (updated regularly by Cloudflare)
