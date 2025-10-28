---
name: cloudflare-workers
description: Comprehensive guide for building serverless applications with Cloudflare Workers. Use when developing Workers, configuring bindings, implementing runtime APIs, testing Workers, using Wrangler CLI, deploying to production, or building edge functions with JavaScript/TypeScript/Python/Rust.
license: MIT
version: 1.0.0
---

# Cloudflare Workers Skill

Cloudflare Workers is a serverless execution environment that runs JavaScript, TypeScript, Python, and Rust code on Cloudflare's global edge network across 300+ cities worldwide.

## Reference

- Main Documentation: https://developers.cloudflare.com/workers/
- Runtime APIs: https://developers.cloudflare.com/workers/runtime-apis/
- Examples: https://developers.cloudflare.com/workers/examples/
- Wrangler CLI: https://developers.cloudflare.com/workers/wrangler/

## When to Use This Skill

Use this skill when:
- Creating new Cloudflare Workers applications
- Configuring Worker bindings (D1, KV, R2, Durable Objects, etc.)
- Implementing Worker runtime APIs (fetch, cache, HTMLRewriter, WebSockets)
- Writing and testing Workers locally with Wrangler
- Deploying Workers to production
- Implementing cron triggers and scheduled jobs
- Building API endpoints and middleware
- Working with Workers static assets
- Setting up CI/CD for Workers
- Migrating from service workers to ES modules
- Debugging and monitoring Workers
- Optimizing Worker performance

## Core Concepts

### Execution Model

**V8 Isolates**: Workers run in lightweight V8 isolates (not containers):
- **Millisecond cold starts** (faster than containers)
- **Zero infrastructure management**
- **Automatic global scaling**
- **Pay-per-request pricing**

**Request Lifecycle**:
1. Request arrives at nearest Cloudflare data center
2. Worker executes in V8 isolate
3. Response returned to client
4. Isolate may be reused for subsequent requests

**Key Characteristics**:
- Maximum CPU time: 50ms (Free), 30 seconds (Paid)
- Maximum memory: 128MB
- Executes at the edge (closest to user)
- No state between requests (use Durable Objects for state)

### Worker Formats

**ES Modules (Recommended)**:
```typescript
// Modern syntax with export default
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response('Hello World!');
  }
};
```

**Service Worker (Legacy)**:
```javascript
// Legacy format
addEventListener('fetch', (event) => {
  event.respondWith(new Response('Hello World!'));
});
```

### Handler Types

Workers support multiple event types:

**Fetch Handler** (HTTP requests):
```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response('Hello');
  }
};
```

**Scheduled Handler** (Cron jobs):
```typescript
export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    // Runs on schedule
    await fetch('https://api.example.com/cleanup');
  }
};
```

**Queue Handler** (Message processing):
```typescript
export default {
  async queue(batch: MessageBatch, env: Env, ctx: ExecutionContext): Promise<void> {
    for (const message of batch.messages) {
      await processMessage(message.body);
    }
  }
};
```

**Email Handler** (Email routing):
```typescript
export default {
  async email(message: ForwardableEmailMessage, env: Env, ctx: ExecutionContext): Promise<void> {
    await message.forward('destination@example.com');
  }
};
```

**Tail Handler** (Log aggregation):
```typescript
export default {
  async tail(events: TraceItem[], env: Env, ctx: ExecutionContext): Promise<void> {
    // Process logs from other Workers
  }
};
```

## Wrangler CLI

### Installation & Setup

```bash
# Install globally
npm install -g wrangler

# Or use npx
npx wrangler <command>

# Login to Cloudflare
wrangler login

# Check version
wrangler --version
```

### Project Management

```bash
# Create new Worker
wrangler init my-worker
# Options: TypeScript, Git, deploy

# Create with template
wrangler init my-worker --template <template-url>

# Development server
wrangler dev                    # Local mode
wrangler dev --remote          # Remote mode (actual edge)
wrangler dev --port 8080       # Custom port

# Deploy
wrangler deploy                # Production
wrangler deploy --dry-run      # Preview changes
wrangler deploy --env staging  # Specific environment

# Logs
wrangler tail                  # Real-time logs
wrangler tail --format pretty  # Formatted output
wrangler tail --status error   # Filter by status

# Versions & Rollback
wrangler deployments list
wrangler rollback [version-id]
wrangler versions list
```

### Configuration (wrangler.toml)

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"
compatibility_flags = ["nodejs_compat"]

# Routes
routes = [
  { pattern = "example.com/*", zone_name = "example.com" }
]

# Or use custom domains
# [[routes]]
# pattern = "api.example.com/*"
# custom_domain = true

# Environment variables
[vars]
ENVIRONMENT = "production"
API_VERSION = "v1"

# Cron triggers
[triggers]
crons = ["0 0 * * *"]  # Daily at midnight

# Build configuration
[build]
command = "npm run build"
watch_dirs = ["src"]

# Environments
[env.staging]
name = "my-worker-staging"
routes = [
  { pattern = "staging.example.com/*", zone_name = "example.com" }
]

[env.staging.vars]
ENVIRONMENT = "staging"
```

### Secrets Management

```bash
# Add secret
wrangler secret put API_KEY
# Enter value when prompted

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete API_KEY

# Bulk upload
echo "VALUE" | wrangler secret put API_KEY
```

## Runtime APIs

### Fetch API

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // Parse URL
    const url = new URL(request.url);

    // Request properties
    const method = request.method;
    const headers = request.headers;
    const body = await request.text();

    // Subrequest
    const response = await fetch('https://api.example.com/data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key: 'value' })
    });

    const data = await response.json();

    // Response
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600'
      }
    });
  }
};
```

### Headers API

```typescript
// Read headers
const userAgent = request.headers.get('User-Agent');
const allHeaders = Object.fromEntries(request.headers);

// Set headers
const headers = new Headers();
headers.set('Content-Type', 'application/json');
headers.append('X-Custom-Header', 'value');

// Cloudflare-specific headers
const country = request.cf?.country;
const colo = request.cf?.colo;
const clientIP = request.headers.get('CF-Connecting-IP');

// Response with headers
return new Response(body, { headers });
```

### Cache API

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const cache = caches.default;

    // Check cache
    let response = await cache.match(request);

    if (!response) {
      // Cache miss - fetch from origin
      response = await fetch(request);

      // Clone and cache response
      const cacheResponse = response.clone();
      ctx.waitUntil(cache.put(request, cacheResponse));
    }

    return response;
  }
};
```

**Cache with custom key**:
```typescript
const cacheKey = new Request(url.toString(), request);
const response = await cache.match(cacheKey);

if (!response) {
  response = await fetch(request);
  ctx.waitUntil(cache.put(cacheKey, response.clone()));
}
```

**Cache with TTL**:
```typescript
const response = await fetch('https://api.example.com/data', {
  cf: {
    cacheTtl: 3600,
    cacheEverything: true,
    cacheKey: 'custom-key'
  }
});
```

### HTMLRewriter

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const response = await fetch(request);

    return new HTMLRewriter()
      .on('title', {
        element(element) {
          element.setInnerContent('New Title');
        }
      })
      .on('a[href]', {
        element(element) {
          const href = element.getAttribute('href');
          element.setAttribute('href', href.replace('http://', 'https://'));
        }
      })
      .on('script', {
        element(element) {
          element.remove();
        }
      })
      .transform(response);
  }
};
```

**Text manipulation**:
```typescript
new HTMLRewriter()
  .on('p', {
    text(text) {
      if (text.text.includes('replace-me')) {
        text.replace('new-text');
      }
    }
  })
  .transform(response);
```

### WebSockets

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const upgradeHeader = request.headers.get('Upgrade');

    if (upgradeHeader !== 'websocket') {
      return new Response('Expected WebSocket', { status: 426 });
    }

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    // Accept WebSocket connection
    server.accept();

    // Handle messages
    server.addEventListener('message', (event) => {
      server.send(`Echo: ${event.data}`);
    });

    server.addEventListener('close', () => {
      console.log('WebSocket closed');
    });

    return new Response(null, {
      status: 101,
      webSocket: client
    });
  }
};
```

### Streams API

```typescript
// Readable stream
const { readable, writable } = new TransformStream();

const writer = writable.getWriter();
writer.write(new TextEncoder().encode('chunk 1'));
writer.write(new TextEncoder().encode('chunk 2'));
writer.close();

return new Response(readable, {
  headers: { 'Content-Type': 'text/plain' }
});
```

**Stream transformation**:
```typescript
const response = await fetch('https://example.com/large-file');

const { readable, writable } = new TransformStream({
  transform(chunk, controller) {
    // Process chunk
    controller.enqueue(chunk);
  }
});

response.body.pipeTo(writable);

return new Response(readable);
```

### Context API

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // waitUntil: Run tasks after response sent
    ctx.waitUntil(
      fetch('https://analytics.example.com/log', {
        method: 'POST',
        body: JSON.stringify({ url: request.url })
      })
    );

    // passThroughOnException: Continue to origin on error
    ctx.passThroughOnException();

    return new Response('OK');
  }
};
```

### Web Crypto API

```typescript
// Generate hash
const data = new TextEncoder().encode('message');
const hashBuffer = await crypto.subtle.digest('SHA-256', data);
const hashArray = Array.from(new Uint8Array(hashBuffer));
const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

// HMAC signature
const key = await crypto.subtle.importKey(
  'raw',
  new TextEncoder().encode('secret'),
  { name: 'HMAC', hash: 'SHA-256' },
  false,
  ['sign', 'verify']
);

const signature = await crypto.subtle.sign('HMAC', key, data);

// Verify
const valid = await crypto.subtle.verify('HMAC', key, signature, data);

// Random values
const randomBytes = crypto.getRandomValues(new Uint8Array(32));
const uuid = crypto.randomUUID();

// Timing-safe comparison
const equal = crypto.timingSafeEqual(buffer1, buffer2);
```

## Bindings

### Environment Variables

```typescript
// wrangler.toml
[vars]
API_URL = "https://api.example.com"

// Usage
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const apiUrl = env.API_URL;
    return new Response(apiUrl);
  }
};
```

### KV Namespace

```toml
# wrangler.toml
[[kv_namespaces]]
binding = "MY_KV"
id = "your-namespace-id"
```

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Put
    await env.MY_KV.put('key', 'value', {
      expirationTtl: 3600,
      metadata: { userId: '123' }
    });

    // Get
    const value = await env.MY_KV.get('key');
    const json = await env.MY_KV.get('key', 'json');
    const buffer = await env.MY_KV.get('key', 'arrayBuffer');
    const stream = await env.MY_KV.get('key', 'stream');

    // Get with metadata
    const { value, metadata } = await env.MY_KV.getWithMetadata('key');

    // Delete
    await env.MY_KV.delete('key');

    // List
    const list = await env.MY_KV.list({ prefix: 'user:' });

    return new Response(value);
  }
};
```

### R2 Bucket

```toml
# wrangler.toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Put object
    await env.MY_BUCKET.put('file.txt', 'content', {
      httpMetadata: {
        contentType: 'text/plain',
        contentLanguage: 'en-US',
        cacheControl: 'public, max-age=3600'
      },
      customMetadata: {
        uploadedBy: 'user123'
      }
    });

    // Get object
    const object = await env.MY_BUCKET.get('file.txt');

    if (!object) {
      return new Response('Not Found', { status: 404 });
    }

    // Return object
    return new Response(object.body, {
      headers: {
        'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
        'ETag': object.etag
      }
    });

    // Delete object
    await env.MY_BUCKET.delete('file.txt');

    // List objects
    const listed = await env.MY_BUCKET.list({ prefix: 'uploads/' });

    // Multipart upload
    const multipart = await env.MY_BUCKET.createMultipartUpload('large-file.bin');
    const part1 = await multipart.uploadPart(1, chunk1);
    const part2 = await multipart.uploadPart(2, chunk2);
    await multipart.complete([part1, part2]);
  }
};
```

### D1 Database

```toml
# wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-database-id"
```

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Query
    const result = await env.DB.prepare(
      'SELECT * FROM users WHERE id = ?'
    ).bind(userId).first();

    // Insert
    const info = await env.DB.prepare(
      'INSERT INTO users (name, email) VALUES (?, ?)'
    ).bind('Alice', 'alice@example.com').run();

    // Batch (atomic)
    const results = await env.DB.batch([
      env.DB.prepare('UPDATE accounts SET balance = balance - 100 WHERE id = ?').bind(1),
      env.DB.prepare('UPDATE accounts SET balance = balance + 100 WHERE id = ?').bind(2)
    ]);

    // All results
    const { results: rows } = await env.DB.prepare(
      'SELECT * FROM users'
    ).all();

    return new Response(JSON.stringify(result));
  }
};
```

### Durable Objects

```toml
# wrangler.toml
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"
script_name = "my-worker"
```

```typescript
// Define Durable Object
export class Counter {
  state: DurableObjectState;

  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    let count = (await this.state.storage.get<number>('count')) || 0;
    count++;
    await this.state.storage.put('count', count);

    return new Response(JSON.stringify({ count }));
  }

  // Alarm handler
  async alarm(): Promise<void> {
    // Runs at scheduled time
    await this.state.storage.deleteAll();
  }
}

// Use in Worker
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const id = env.COUNTER.idFromName('global');
    const counter = env.COUNTER.get(id);
    return counter.fetch(request);
  }
};
```

### Queues

```toml
# wrangler.toml
[[queues.producers]]
binding = "MY_QUEUE"
queue = "my-queue"

[[queues.consumers]]
queue = "my-queue"
max_batch_size = 10
max_batch_timeout = 30
```

```typescript
// Producer
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    await env.MY_QUEUE.send({
      type: 'email',
      to: 'user@example.com'
    });

    // Batch send
    await env.MY_QUEUE.sendBatch([
      { body: { message: 1 } },
      { body: { message: 2 } }
    ]);

    return new Response('Queued');
  }
};

// Consumer
export default {
  async queue(batch: MessageBatch, env: Env, ctx: ExecutionContext): Promise<void> {
    for (const message of batch.messages) {
      try {
        await processMessage(message.body);
        message.ack();
      } catch (error) {
        message.retry();
      }
    }
  }
};
```

### Workers AI

```toml
# wrangler.toml
[ai]
binding = "AI"
```

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Text generation
    const response = await env.AI.run('@cf/meta/llama-3-8b-instruct', {
      messages: [
        { role: 'user', content: 'What is edge computing?' }
      ]
    });

    // Image generation
    const imageResponse = await env.AI.run('@cf/stabilityai/stable-diffusion-xl-base-1.0', {
      prompt: 'A sunset over mountains'
    });

    // Embeddings
    const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
      text: ['Hello world', 'Cloudflare Workers']
    });

    // Speech recognition
    const audio = await request.arrayBuffer();
    const transcription = await env.AI.run('@cf/openai/whisper', {
      audio: [...new Uint8Array(audio)]
    });

    return new Response(JSON.stringify(response));
  }
};
```

### Vectorize (Vector Database)

```toml
# wrangler.toml
[[vectorize]]
binding = "VECTORIZE_INDEX"
index_name = "my-index"
```

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Insert vectors
    await env.VECTORIZE_INDEX.insert([
      {
        id: '1',
        values: [0.1, 0.2, 0.3],
        metadata: { text: 'Hello world' }
      }
    ]);

    // Query
    const results = await env.VECTORIZE_INDEX.query(
      [0.1, 0.2, 0.3],
      { topK: 5 }
    );

    return new Response(JSON.stringify(results));
  }
};
```

## Development Patterns

### Routing

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    // Route by path
    switch (url.pathname) {
      case '/':
        return new Response('Home');
      case '/about':
        return new Response('About');
      default:
        return new Response('Not Found', { status: 404 });
    }
  }
};
```

**Using Hono framework**:
```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/', (c) => c.text('Home'));
app.get('/api/users/:id', async (c) => {
  const id = c.req.param('id');
  const user = await getUser(id);
  return c.json(user);
});

export default app;
```

### Middleware Pattern

```typescript
async function auth(request: Request, env: Env): Promise<Response | null> {
  const token = request.headers.get('Authorization');

  if (!token) {
    return new Response('Unauthorized', { status: 401 });
  }

  return null; // Continue
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const authResponse = await auth(request, env);
    if (authResponse) return authResponse;

    // Continue with request
    return new Response('Protected content');
  }
};
```

### Error Handling

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    try {
      const response = await processRequest(request, env);
      return response;
    } catch (error) {
      console.error('Error:', error);

      // Log to external service
      ctx.waitUntil(
        fetch('https://logging.example.com/error', {
          method: 'POST',
          body: JSON.stringify({
            error: error.message,
            stack: error.stack,
            url: request.url
          })
        })
      );

      return new Response('Internal Server Error', { status: 500 });
    }
  }
};
```

### CORS

```typescript
function corsHeaders(origin: string) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400'
  };
}

export default {
  async fetch(request: Request): Promise<Response> {
    const origin = request.headers.get('Origin') || '*';

    // Handle preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: corsHeaders(origin)
      });
    }

    // Handle request
    const response = await handleRequest(request);

    // Add CORS headers
    const headers = new Headers(response.headers);
    Object.entries(corsHeaders(origin)).forEach(([key, value]) => {
      headers.set(key, value);
    });

    return new Response(response.body, {
      status: response.status,
      headers
    });
  }
};
```

### Rate Limiting

```typescript
async function rateLimit(ip: string, env: Env): Promise<boolean> {
  const key = `ratelimit:${ip}`;
  const limit = 100;
  const window = 60;

  const current = await env.MY_KV.get(key);
  const count = current ? parseInt(current) : 0;

  if (count >= limit) {
    return false;
  }

  await env.MY_KV.put(key, (count + 1).toString(), {
    expirationTtl: window
  });

  return true;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';

    if (!await rateLimit(ip, env)) {
      return new Response('Rate limit exceeded', { status: 429 });
    }

    return new Response('OK');
  }
};
```

## Testing

### Local Testing with Wrangler

```bash
# Start dev server
wrangler dev

# Test with curl
curl http://localhost:8787

# Remote development (uses actual edge)
wrangler dev --remote
```

### Unit Testing with Vitest

```bash
npm install -D vitest @cloudflare/vitest-pool-workers
```

**vitest.config.ts**:
```typescript
import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config';

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.toml' },
      },
    },
  },
});
```

**Test file**:
```typescript
import { env, createExecutionContext, waitOnExecutionContext } from 'cloudflare:test';
import { describe, it, expect } from 'vitest';
import worker from '../src/index';

describe('Worker', () => {
  it('responds with Hello World', async () => {
    const request = new Request('http://example.com');
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);
    await waitOnExecutionContext(ctx);

    expect(await response.text()).toBe('Hello World!');
  });
});
```

### Integration Testing

```typescript
import { unstable_dev } from 'wrangler';

describe('Worker integration tests', () => {
  let worker;

  beforeAll(async () => {
    worker = await unstable_dev('src/index.ts', {
      experimental: { disableExperimentalWarning: true }
    });
  });

  afterAll(async () => {
    await worker.stop();
  });

  it('should return 200', async () => {
    const resp = await worker.fetch();
    expect(resp.status).toBe(200);
  });
});
```

## Deployment

### Basic Deployment

```bash
# Deploy to production
wrangler deploy

# Deploy to specific environment
wrangler deploy --env staging

# Preview deployment
wrangler deploy --dry-run
```

### Environments

```toml
# wrangler.toml
name = "my-worker"

[env.staging]
name = "my-worker-staging"
routes = [
  { pattern = "staging.example.com/*", zone_name = "example.com" }
]

[env.production]
name = "my-worker-production"
routes = [
  { pattern = "api.example.com/*", zone_name = "example.com" }
]
```

```bash
wrangler deploy --env staging
wrangler deploy --env production
```

### CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy Worker

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm install

      - run: npm test

      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

### Gradual Deployments

```bash
# Deploy to 10% of traffic
wrangler versions deploy --percentage 10

# Promote to 100%
wrangler versions deploy --percentage 100

# Rollback
wrangler rollback
```

## Static Assets

### Configuration

```toml
# wrangler.toml
name = "my-worker"
main = "src/index.ts"

[assets]
directory = "./public"
binding = "ASSETS"
```

### Serving Static Assets

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Serve static asset
    const asset = await env.ASSETS.fetch(request);

    if (asset.status === 200) {
      return asset;
    }

    // Fallback to dynamic response
    return new Response('Not Found', { status: 404 });
  }
};
```

### Single Page Application (SPA)

```toml
[assets]
directory = "./dist"
binding = "ASSETS"
html_handling = "force-https"
not_found_handling = "single-page-application"
```

## Observability

### Logging

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    console.log('Request URL:', request.url);
    console.error('Error occurred');
    console.warn('Warning message');

    // Structured logging
    console.log(JSON.stringify({
      level: 'info',
      message: 'Request processed',
      url: request.url,
      timestamp: new Date().toISOString()
    }));

    return new Response('OK');
  }
};
```

### Real-time Logs

```bash
# Tail logs
wrangler tail

# Filter by status
wrangler tail --status error

# Filter by method
wrangler tail --method POST

# Filter by sampling
wrangler tail --sampling-rate 0.5
```

### Analytics

```typescript
// Use Analytics Engine binding
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    env.ANALYTICS.writeDataPoint({
      blobs: ['example'],
      doubles: [123.45],
      indexes: ['index_value']
    });

    return new Response('Logged');
  }
};
```

### Error Tracking (Sentry)

```typescript
import * as Sentry from '@sentry/cloudflare';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    Sentry.init({
      dsn: env.SENTRY_DSN,
      environment: env.ENVIRONMENT
    });

    try {
      return await handleRequest(request);
    } catch (error) {
      Sentry.captureException(error);
      throw error;
    }
  }
};
```

## Performance Optimization

### Best Practices

1. **Minimize Bundle Size**: Keep Workers under 1MB
2. **Use Bindings**: Direct bindings are faster than fetch
3. **Cache Aggressively**: Use Cache API and KV
4. **Stream Large Responses**: Use streams instead of buffering
5. **Batch Operations**: Combine D1 queries with batch()
6. **waitUntil for Background Tasks**: Don't block response
7. **Avoid Synchronous I/O**: All operations should be async

### Code Splitting

```typescript
// Lazy load large dependencies
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/heavy') {
      const { processHeavy } = await import('./heavy');
      return processHeavy(request);
    }

    return new Response('OK');
  }
};
```

### Caching Strategy

```typescript
const CACHE_TTL = 3600;

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const cache = caches.default;
    const cacheKey = new Request(request.url);

    // 1. Check edge cache
    let response = await cache.match(cacheKey);
    if (response) return response;

    // 2. Check KV cache
    const kvCached = await env.MY_KV.get(request.url);
    if (kvCached) {
      response = new Response(kvCached);
      ctx.waitUntil(cache.put(cacheKey, response.clone()));
      return response;
    }

    // 3. Fetch from origin
    response = await fetch(request);

    // 4. Store in both caches
    ctx.waitUntil(Promise.all([
      cache.put(cacheKey, response.clone()),
      env.MY_KV.put(request.url, await response.clone().text(), {
        expirationTtl: CACHE_TTL
      })
    ]));

    return response;
  }
};
```

## Common Patterns

### API Gateway

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';

const app = new Hono();

app.use('*', cors());
app.use('*', logger());

// Routes
app.get('/api/users', async (c) => {
  const users = await c.env.DB.prepare('SELECT * FROM users').all();
  return c.json(users.results);
});

app.get('/api/users/:id', async (c) => {
  const id = c.req.param('id');
  const user = await c.env.DB.prepare(
    'SELECT * FROM users WHERE id = ?'
  ).bind(id).first();

  if (!user) {
    return c.json({ error: 'Not found' }, 404);
  }

  return c.json(user);
});

app.post('/api/users', async (c) => {
  const body = await c.req.json();

  const result = await c.env.DB.prepare(
    'INSERT INTO users (name, email) VALUES (?, ?)'
  ).bind(body.name, body.email).run();

  return c.json({ id: result.meta.last_row_id }, 201);
});

export default app;
```

### Authentication

```typescript
import { sign, verify } from 'hono/jwt';

async function authenticate(request: Request, env: Env): Promise<any> {
  const authHeader = request.headers.get('Authorization');

  if (!authHeader?.startsWith('Bearer ')) {
    throw new Error('Missing token');
  }

  const token = authHeader.substring(7);
  const payload = await verify(token, env.JWT_SECRET);

  return payload;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    try {
      const user = await authenticate(request, env);
      return new Response(`Hello ${user.name}`);
    } catch (error) {
      return new Response('Unauthorized', { status: 401 });
    }
  }
};
```

### Image Proxy

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const imageUrl = url.searchParams.get('url');

    if (!imageUrl) {
      return new Response('Missing url parameter', { status: 400 });
    }

    const response = await fetch(imageUrl);

    return new Response(response.body, {
      headers: {
        'Content-Type': response.headers.get('Content-Type') || 'image/jpeg',
        'Cache-Control': 'public, max-age=86400',
        'CDN-Cache-Control': 'public, max-age=31536000'
      }
    });
  }
};
```

### Webhook Handler

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    // Verify signature
    const signature = request.headers.get('X-Hub-Signature-256');
    const body = await request.text();

    const valid = await verifySignature(body, signature, env.WEBHOOK_SECRET);

    if (!valid) {
      return new Response('Invalid signature', { status: 401 });
    }

    // Queue for processing
    ctx.waitUntil(
      env.WEBHOOK_QUEUE.send(JSON.parse(body))
    );

    return new Response('OK');
  }
};
```

## Troubleshooting

### Common Issues

**CPU Time Exceeded**:
- Optimize expensive operations
- Use streams for large data
- Move processing to Durable Objects
- Consider splitting work across multiple requests

**Memory Exceeded**:
- Stream large responses instead of buffering
- Clear unused variables
- Use chunked processing

**Script Size Too Large**:
- Remove unused dependencies
- Use code splitting
- Minify production builds
- Check `wrangler deploy --dry-run --outdir=dist` output

**Binding Not Found**:
- Check wrangler.toml configuration
- Ensure binding name matches env property
- Redeploy after configuration changes

**CORS Errors**:
- Add proper CORS headers
- Handle OPTIONS requests
- Check allowed origins

### Debugging

```bash
# Local debugging
wrangler dev --local

# Remote debugging (real edge environment)
wrangler dev --remote

# Inspect bundle
wrangler deploy --dry-run --outdir=dist

# Check logs
wrangler tail --format pretty
```

## Resources

- **Main Docs**: https://developers.cloudflare.com/workers/
- **Examples**: https://developers.cloudflare.com/workers/examples/
- **Discord**: https://discord.cloudflare.com
- **GitHub**: https://github.com/cloudflare/workers-sdk
- **Status**: https://www.cloudflarestatus.com
- **Pricing**: https://developers.cloudflare.com/workers/platform/pricing/

## Implementation Checklist

### Initial Setup
- [ ] Install Wrangler CLI
- [ ] Login to Cloudflare account
- [ ] Create new Worker project
- [ ] Configure wrangler.toml
- [ ] Test locally with `wrangler dev`

### Development
- [ ] Implement fetch handler
- [ ] Add error handling
- [ ] Set up TypeScript types
- [ ] Configure bindings (KV, D1, R2, etc.)
- [ ] Add environment variables
- [ ] Implement caching strategy

### Testing
- [ ] Write unit tests with Vitest
- [ ] Test locally with wrangler dev
- [ ] Test on remote edge
- [ ] Validate bindings work

### Deployment
- [ ] Set up environments (staging, production)
- [ ] Configure routes or custom domains
- [ ] Add secrets
- [ ] Set up CI/CD pipeline
- [ ] Deploy to production
- [ ] Monitor logs and analytics

### Production
- [ ] Set up error tracking
- [ ] Configure analytics
- [ ] Implement rate limiting
- [ ] Add monitoring alerts
- [ ] Document API endpoints
- [ ] Set up rollback procedure
