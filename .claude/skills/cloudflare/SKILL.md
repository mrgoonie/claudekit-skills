---
name: cloudflare
description: Guide for building applications on Cloudflare's edge platform. Use when implementing serverless functions (Workers), edge databases (D1), storage (R2, KV), real-time apps (Durable Objects), AI features (Workers AI, AI Gateway), static sites (Pages), or any edge computing solutions.
license: MIT
version: 1.0.0
---

# Cloudflare Developer Platform Skill

Cloudflare Developer Platform is a comprehensive edge computing ecosystem for building full-stack applications on Cloudflare's global network. It includes serverless functions, databases, storage, AI/ML capabilities, and static site hosting.

## When to Use This Skill

Use this skill when:
- Building serverless applications on the edge
- Implementing edge databases (D1 SQLite)
- Working with object storage (R2) or key-value stores (KV)
- Creating real-time applications with WebSockets (Durable Objects)
- Integrating AI/ML capabilities (Workers AI, AI Gateway, Agents)
- Deploying static sites with serverless functions (Pages)
- Building full-stack applications with frameworks (Next.js, Remix, Astro, etc.)
- Implementing message queues and background jobs (Queues)
- Optimizing for global performance and low latency

## Core Concepts

### Edge Computing Platform

**Cloudflare's Edge Network**: Code runs on servers globally distributed across 300+ cities, executing requests from the nearest location for ultra-low latency.

**Key Components**:
- **Workers**: Serverless functions on the edge
- **D1**: SQLite database with global read replication
- **KV**: Distributed key-value store with eventual consistency
- **R2**: Object storage with zero egress fees
- **Durable Objects**: Stateful compute with WebSocket support
- **Queues**: Message queue system for async processing
- **Pages**: Static site hosting with serverless functions
- **Workers AI**: Run AI models on the edge
- **AI Gateway**: Unified interface for AI providers

### Execution Model

**V8 Isolates**: Lightweight execution environments (faster than containers) with:
- Millisecond cold starts
- Zero infrastructure management
- Automatic scaling
- Pay-per-request pricing

**Handler Types**:
- `fetch`: HTTP requests
- `scheduled`: Cron jobs
- `queue`: Message processing
- `tail`: Log aggregation
- `email`: Email handling
- `alarm`: Durable Object timers

## Getting Started with Workers

### Installation

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create new project
wrangler init my-worker
cd my-worker

# Start local development
wrangler dev

# Deploy to production
wrangler deploy
```

### Basic Worker

```typescript
// src/index.ts
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return new Response('Hello from Cloudflare Workers!');
  }
};
```

### Configuration (wrangler.toml)

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Environment variables
[vars]
ENVIRONMENT = "production"

# Bindings (added per product below)
```

### Language Support

- **JavaScript/TypeScript**: Primary language (full Node.js compatibility)
- **Python**: Beta support via Workers Python
- **Rust**: Compile to WebAssembly

## Storage Products

### D1 (SQLite Database)

**Use Cases**: Relational data, complex queries, ACID transactions

**Setup**:
```bash
# Create database
wrangler d1 create my-database

# Add to wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "YOUR_DATABASE_ID"

# Generate and apply schema
wrangler d1 execute my-database --file=./schema.sql
```

**Usage**:
```typescript
export default {
  async fetch(request: Request, env: Env) {
    // Query
    const result = await env.DB.prepare(
      "SELECT * FROM users WHERE id = ?"
    ).bind(userId).first();

    // Insert
    await env.DB.prepare(
      "INSERT INTO users (name, email) VALUES (?, ?)"
    ).bind("Alice", "alice@example.com").run();

    // Batch (atomic)
    await env.DB.batch([
      env.DB.prepare("UPDATE accounts SET balance = balance - 100 WHERE id = ?").bind(user1),
      env.DB.prepare("UPDATE accounts SET balance = balance + 100 WHERE id = ?").bind(user2)
    ]);

    return new Response(JSON.stringify(result));
  }
};
```

**Key Features**:
- Global read replication (low-latency reads)
- Single-writer consistency
- Standard SQLite syntax
- 25GB database size limit

### KV (Key-Value Store)

**Use Cases**: Cache, sessions, feature flags, rate limiting

**Setup**:
```bash
# Create namespace
wrangler kv:namespace create MY_KV

# Add to wrangler.toml
[[kv_namespaces]]
binding = "KV"
id = "YOUR_NAMESPACE_ID"
```

**Usage**:
```typescript
export default {
  async fetch(request: Request, env: Env) {
    // Put with TTL
    await env.KV.put("session:token", JSON.stringify(data), {
      expirationTtl: 3600 // 1 hour
    });

    // Get
    const data = await env.KV.get("session:token", "json");

    // Delete
    await env.KV.delete("session:token");

    // List with prefix
    const list = await env.KV.list({ prefix: "user:123:" });

    return new Response(JSON.stringify(data));
  }
};
```

**Key Features**:
- Sub-millisecond reads (edge-cached)
- Eventual consistency (~60 seconds globally)
- 25MB value size limit
- Automatic expiration (TTL)

### R2 (Object Storage)

**Use Cases**: File storage, media hosting, backups, static assets

**Setup**:
```bash
# Create bucket
wrangler r2 bucket create my-bucket

# Add to wrangler.toml
[[r2_buckets]]
binding = "R2_BUCKET"
bucket_name = "my-bucket"
```

**Usage**:
```typescript
export default {
  async fetch(request: Request, env: Env) {
    // Put object
    await env.R2_BUCKET.put("path/to/file.jpg", fileBuffer, {
      httpMetadata: {
        contentType: "image/jpeg"
      }
    });

    // Get object
    const object = await env.R2_BUCKET.get("path/to/file.jpg");
    if (!object) {
      return new Response("Not found", { status: 404 });
    }

    // Stream response
    return new Response(object.body, {
      headers: {
        "Content-Type": object.httpMetadata?.contentType || "application/octet-stream"
      }
    });

    // Delete
    await env.R2_BUCKET.delete("path/to/file.jpg");

    // List
    const list = await env.R2_BUCKET.list({ prefix: "uploads/" });
  }
};
```

**Key Features**:
- S3-compatible API
- **Zero egress fees** (huge cost advantage)
- Unlimited storage
- 5TB object size limit
- Multipart upload support

### Durable Objects

**Use Cases**: Real-time apps, WebSockets, coordination, stateful logic

**Setup**:
```toml
# wrangler.toml
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"
script_name = "my-worker"
```

**Usage**:
```typescript
// Define Durable Object class
export class Counter {
  state: DurableObjectState;

  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
  }

  async fetch(request: Request) {
    // Get current count
    let count = (await this.state.storage.get<number>('count')) || 0;

    // Increment
    count++;
    await this.state.storage.put('count', count);

    return new Response(JSON.stringify({ count }));
  }
}

// Use in Worker
export default {
  async fetch(request: Request, env: Env) {
    // Get Durable Object instance
    const id = env.COUNTER.idFromName("global-counter");
    const counter = env.COUNTER.get(id);

    // Forward request
    return counter.fetch(request);
  }
};
```

**WebSocket Example**:
```typescript
export class ChatRoom {
  state: DurableObjectState;
  sessions: Set<WebSocket>;

  constructor(state: DurableObjectState) {
    this.state = state;
    this.sessions = new Set();
  }

  async fetch(request: Request) {
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    this.state.acceptWebSocket(server);
    this.sessions.add(server);

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws: WebSocket, message: string) {
    // Broadcast to all connected clients
    for (const session of this.sessions) {
      session.send(message);
    }
  }

  async webSocketClose(ws: WebSocket) {
    this.sessions.delete(ws);
  }
}
```

**Key Features**:
- Single-instance coordination (strong consistency)
- Persistent storage (1GB limit on paid plans)
- WebSocket support
- Automatic hibernation for inactive objects

### Queues

**Use Cases**: Background jobs, email sending, async processing

**Setup**:
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

**Usage**:
```typescript
// Producer: Send messages
export default {
  async fetch(request: Request, env: Env) {
    await env.MY_QUEUE.send({
      type: 'email',
      to: 'user@example.com',
      subject: 'Welcome!'
    });

    return new Response('Message queued');
  }
};

// Consumer: Process messages
export default {
  async queue(batch: MessageBatch<any>, env: Env) {
    for (const message of batch.messages) {
      try {
        await processMessage(message.body);
        message.ack(); // Acknowledge success
      } catch (error) {
        message.retry(); // Retry on failure
      }
    }
  }
};
```

**Key Features**:
- At-least-once delivery
- Automatic retries (exponential backoff)
- Dead-letter queue support
- Batch processing

## AI Products

### Workers AI

**Use Cases**: Run AI models directly on the edge

**Setup**:
```toml
# wrangler.toml
[ai]
binding = "AI"
```

**Usage**:
```typescript
export default {
  async fetch(request: Request, env: Env) {
    // Text generation
    const response = await env.AI.run('@cf/meta/llama-3-8b-instruct', {
      messages: [
        { role: 'user', content: 'What is edge computing?' }
      ]
    });

    // Image classification
    const imageResponse = await env.AI.run('@cf/microsoft/resnet-50', {
      image: imageBuffer
    });

    // Text embeddings
    const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
      text: 'Hello world'
    });

    return new Response(JSON.stringify(response));
  }
};
```

**Available Models**:
- LLMs: Llama 3, Mistral, Gemma, Qwen
- Image: Stable Diffusion, DALL-E, ResNet
- Embeddings: BGE, GTE
- Translation, summarization, sentiment analysis

### AI Gateway

**Use Cases**: Unified interface for AI providers with caching, rate limiting, analytics

**Setup**:
```typescript
// OpenAI via AI Gateway
const response = await fetch(
  'https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/openai/chat/completions',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [{ role: 'user', content: 'Hello!' }]
    })
  }
);
```

**Features**:
- Request caching (reduce costs)
- Rate limiting
- Analytics and logging
- Supports OpenAI, Anthropic, HuggingFace, etc.

### Agents

**Use Cases**: Build AI agents with tools and workflows

```typescript
import { Agent } from '@cloudflare/agents';

export default {
  async fetch(request: Request, env: Env) {
    const agent = new Agent({
      model: '@cf/meta/llama-3-8b-instruct',
      tools: [
        {
          name: 'get_weather',
          description: 'Get current weather',
          parameters: {
            type: 'object',
            properties: {
              location: { type: 'string' }
            }
          },
          handler: async ({ location }) => {
            // Fetch weather data
            return { temperature: 72, conditions: 'sunny' };
          }
        }
      ]
    });

    const result = await agent.run('What is the weather in San Francisco?');
    return new Response(JSON.stringify(result));
  }
};
```

### AI Search (RAG)

**Use Cases**: Build retrieval-augmented generation applications

```typescript
import { VectorizeIndex } from '@cloudflare/workers-types';

export default {
  async fetch(request: Request, env: Env) {
    // Generate embeddings
    const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
      text: query
    });

    // Search vector database
    const results = await env.VECTORIZE_INDEX.query(embeddings.data[0], {
      topK: 5
    });

    // Generate response with context
    const response = await env.AI.run('@cf/meta/llama-3-8b-instruct', {
      messages: [
        {
          role: 'system',
          content: `Context: ${results.matches.map(m => m.metadata.text).join('\n')}`
        },
        { role: 'user', content: query }
      ]
    });

    return new Response(JSON.stringify(response));
  }
};
```

## Cloudflare Pages

### Static Sites + Serverless Functions

**Deployment**:
```bash
# Deploy via Git (recommended)
# Connect GitHub repo in Cloudflare dashboard

# Or deploy via CLI
wrangler pages deploy ./dist
```

### Pages Functions

Directory-based routing in `functions/`:

```
functions/
├── api/
│   ├── users/
│   │   └── [id].ts       # /api/users/:id
│   └── posts.ts          # /api/posts
└── _middleware.ts        # Global middleware
```

**Example Function**:
```typescript
// functions/api/users/[id].ts
export async function onRequestGet(context) {
  const { params, env } = context;
  const user = await env.DB.prepare(
    "SELECT * FROM users WHERE id = ?"
  ).bind(params.id).first();

  return new Response(JSON.stringify(user), {
    headers: { 'Content-Type': 'application/json' }
  });
}
```

**Middleware**:
```typescript
// functions/_middleware.ts
export async function onRequest(context) {
  const start = Date.now();
  const response = await context.next();
  const duration = Date.now() - start;

  console.log(`${context.request.method} ${context.request.url} - ${duration}ms`);
  return response;
}
```

### Framework Support

**Next.js**:
```bash
npx create-next-app@latest my-app
cd my-app
npm install -D @cloudflare/next-on-pages
npx @cloudflare/next-on-pages
wrangler pages deploy .vercel/output/static
```

**Remix**:
```bash
npx create-remix@latest --template cloudflare/remix
```

**Astro**:
```bash
npm create astro@latest
# Select "Cloudflare" adapter during setup
```

**SvelteKit**:
```bash
npm create svelte@latest
npm install -D @sveltejs/adapter-cloudflare
```

## Wrangler CLI Essentials

### Core Commands

```bash
# Development
wrangler dev                    # Local development server
wrangler dev --remote          # Dev on real Cloudflare infrastructure

# Deployment
wrangler deploy                # Deploy to production
wrangler deploy --dry-run     # Preview changes without deploying

# Logs
wrangler tail                  # Real-time logs
wrangler tail --format pretty # Formatted logs

# Versions
wrangler deployments list      # List deployments
wrangler rollback [version]   # Rollback to previous version

# Secrets
wrangler secret put SECRET_NAME    # Add secret
wrangler secret list               # List secrets
wrangler secret delete SECRET_NAME # Delete secret
```

### Project Management

```bash
# Create projects
wrangler init my-worker        # Create Worker
wrangler pages project create  # Create Pages project

# Database
wrangler d1 create my-db           # Create D1 database
wrangler d1 execute my-db --file=schema.sql
wrangler d1 execute my-db --command="SELECT * FROM users"

# KV
wrangler kv:namespace create MY_KV
wrangler kv:key put --binding=MY_KV "key" "value"
wrangler kv:key get --binding=MY_KV "key"

# R2
wrangler r2 bucket create my-bucket
wrangler r2 object put my-bucket/file.txt --file=./file.txt
```

## Integration Patterns

### Full-Stack Application Architecture

```
┌─────────────────────────────────────────┐
│         Cloudflare Pages (Frontend)      │
│    Next.js / Remix / Astro / SvelteKit  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Workers (API Layer / BFF)          │
│    - Routing                             │
│    - Authentication                      │
│    - Business logic                      │
└─┬──────┬──────┬──────┬──────┬───────────┘
  │      │      │      │      │
  ▼      ▼      ▼      ▼      ▼
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────────────┐
│ D1 │ │ KV │ │ R2 │ │ DO │ │ Workers AI │
└────┘ └────┘ └────┘ └────┘ └────────────┘
```

### Polyglot Storage Pattern

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);

    // KV: Fast cache
    const cached = await env.KV.get(url.pathname);
    if (cached) return new Response(cached);

    // D1: Structured data
    const user = await env.DB.prepare(
      "SELECT * FROM users WHERE id = ?"
    ).bind(userId).first();

    // R2: Media files
    const avatar = await env.R2_BUCKET.get(`avatars/${user.id}.jpg`);

    // Durable Objects: Real-time coordination
    const chat = env.CHAT_ROOM.get(env.CHAT_ROOM.idFromName(roomId));

    // Queue: Async processing
    await env.EMAIL_QUEUE.send({ to: user.email, template: 'welcome' });

    return new Response(JSON.stringify({ user, avatar }));
  }
};
```

### Authentication Pattern

```typescript
import { verifyJWT, createJWT } from './jwt';

export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);

    // Login
    if (url.pathname === '/api/login') {
      const { email, password } = await request.json();

      const user = await env.DB.prepare(
        "SELECT * FROM users WHERE email = ?"
      ).bind(email).first();

      if (!user || !await verifyPassword(password, user.password_hash)) {
        return new Response('Invalid credentials', { status: 401 });
      }

      const token = await createJWT({ userId: user.id }, env.JWT_SECRET);

      return new Response(JSON.stringify({ token }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Protected route
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return new Response('Unauthorized', { status: 401 });
    }

    const token = authHeader.replace('Bearer ', '');
    const payload = await verifyJWT(token, env.JWT_SECRET);

    // Store session in KV
    await env.KV.put(`session:${payload.userId}`, JSON.stringify(payload), {
      expirationTtl: 86400 // 24 hours
    });

    return new Response('Authenticated');
  }
};
```

### Cache Strategy

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const cache = caches.default;
    const cacheKey = new Request(request.url);

    // Check cache
    let response = await cache.match(cacheKey);
    if (response) return response;

    // Check KV (distributed cache)
    const kvCached = await env.KV.get(request.url);
    if (kvCached) {
      response = new Response(kvCached);
      await cache.put(cacheKey, response.clone());
      return response;
    }

    // Fetch from origin (D1, R2, etc.)
    const data = await fetchFromOrigin(request, env);
    response = new Response(data);

    // Store in both caches
    await cache.put(cacheKey, response.clone());
    await env.KV.put(request.url, data, { expirationTtl: 3600 });

    return response;
  }
};
```

## Best Practices

### Performance

1. **Minimize Cold Starts**: Keep Workers lightweight (<1MB bundled)
2. **Use Bindings Over Fetch**: Direct bindings are faster than HTTP calls
3. **Edge Caching**: Leverage KV and Cache API for frequently accessed data
4. **Batch Operations**: Use D1 batch for multiple queries
5. **Stream Large Responses**: Use `Response.body` streams for large files

### Security

1. **Secrets Management**: Use `wrangler secret` for API keys
2. **Environment Isolation**: Separate production/staging/development
3. **Input Validation**: Sanitize user input
4. **Rate Limiting**: Use KV or Durable Objects for rate limiting
5. **CORS**: Configure proper CORS headers

### Cost Optimization

1. **R2 for Large Files**: Zero egress fees vs S3
2. **KV for Caching**: Reduce D1/R2 requests
3. **Request Deduplication**: Cache identical requests
4. **Efficient Queries**: Index D1 tables properly
5. **Monitor Usage**: Use Cloudflare Analytics

### Development Workflow

1. **Local Development**: Use `wrangler dev` for testing
2. **Type Safety**: Use TypeScript with `@cloudflare/workers-types`
3. **Testing**: Use Vitest with `unstable_dev()`
4. **CI/CD**: GitHub Actions with `cloudflare/wrangler-action`
5. **Gradual Deployments**: Use percentage-based rollouts

## Common Patterns

### API Gateway

```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/api/users/:id', async (c) => {
  const user = await c.env.DB.prepare(
    "SELECT * FROM users WHERE id = ?"
  ).bind(c.req.param('id')).first();

  return c.json(user);
});

app.post('/api/users', async (c) => {
  const { name, email } = await c.req.json();

  await c.env.DB.prepare(
    "INSERT INTO users (name, email) VALUES (?, ?)"
  ).bind(name, email).run();

  return c.json({ success: true }, 201);
});

export default app;
```

### Image Transformation

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);
    const imageKey = url.pathname.replace('/images/', '');

    // Get from R2
    const object = await env.R2_BUCKET.get(imageKey);
    if (!object) {
      return new Response('Not found', { status: 404 });
    }

    // Transform with Cloudflare Images
    return new Response(object.body, {
      headers: {
        'Content-Type': object.httpMetadata?.contentType || 'image/jpeg',
        'Cache-Control': 'public, max-age=86400',
        'cf-image-resize': JSON.stringify({
          width: 800,
          height: 600,
          fit: 'cover'
        })
      }
    });
  }
};
```

### Rate Limiting (KV)

```typescript
async function rateLimit(ip: string, env: Env): Promise<boolean> {
  const key = `ratelimit:${ip}`;
  const limit = 100; // requests per minute
  const window = 60; // seconds

  const current = await env.KV.get(key);
  const count = current ? parseInt(current) : 0;

  if (count >= limit) {
    return false; // Rate limit exceeded
  }

  await env.KV.put(key, (count + 1).toString(), {
    expirationTtl: window
  });

  return true;
}

export default {
  async fetch(request: Request, env: Env) {
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';

    if (!await rateLimit(ip, env)) {
      return new Response('Rate limit exceeded', { status: 429 });
    }

    return new Response('OK');
  }
};
```

### Scheduled Jobs

```toml
# wrangler.toml
[triggers]
crons = ["0 0 * * *"] # Daily at midnight
```

```typescript
export default {
  async scheduled(event: ScheduledEvent, env: Env) {
    // Cleanup old sessions
    const sessions = await env.KV.list({ prefix: 'session:' });
    for (const key of sessions.keys) {
      const session = await env.KV.get(key.name, 'json');
      if (session.expiresAt < Date.now()) {
        await env.KV.delete(key.name);
      }
    }
  }
};
```

## Troubleshooting

### Common Issues

**"Module not found" errors**
- Ensure dependencies are in `package.json`
- Run `npm install` before deploying
- Check compatibility_date in wrangler.toml

**Database connection errors (D1)**
- Verify database_id in wrangler.toml
- Check database exists: `wrangler d1 list`
- Run migrations: `wrangler d1 execute DB --file=schema.sql`

**KV not found errors**
- Create namespace: `wrangler kv:namespace create MY_KV`
- Add binding to wrangler.toml
- Deploy after configuration changes

**Cold start timeout**
- Reduce bundle size (<1MB ideal)
- Remove unnecessary dependencies
- Use dynamic imports for large libraries

**CORS errors**
- Add CORS headers to responses:
  ```typescript
  return new Response(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
  ```

**Deployment fails**
- Check wrangler version: `wrangler --version`
- Verify authentication: `wrangler whoami`
- Review build errors in console output

### Debugging

```bash
# Real-time logs
wrangler tail

# Local debugging with breakpoints
wrangler dev --local

# Remote debugging
wrangler dev --remote

# Check deployment status
wrangler deployments list
```

## Decision Matrix

| Need | Choose |
|------|--------|
| Sub-millisecond reads | KV |
| SQL queries | D1 |
| Large files (>25MB) | R2 |
| Real-time WebSockets | Durable Objects |
| Async background jobs | Queues |
| ACID transactions | D1 |
| Strong consistency | Durable Objects |
| Zero egress costs | R2 |
| AI inference | Workers AI |
| Static site hosting | Pages |
| Serverless functions | Workers |
| Multi-provider AI | AI Gateway |

## Framework-Specific Guides

### Next.js
- Use `@cloudflare/next-on-pages` adapter
- Configure `next.config.js` for edge runtime
- Deploy via `wrangler pages deploy`

### Remix
- Use official Cloudflare template
- Configure `server.ts` for Workers
- Access bindings via `context.cloudflare.env`

### Astro
- Use `@astrojs/cloudflare` adapter
- Enable SSR in `astro.config.mjs`
- Access env via `Astro.locals.runtime.env`

### SvelteKit
- Use `@sveltejs/adapter-cloudflare`
- Configure in `svelte.config.js`
- Access platform via `event.platform.env`

## Resources

- **Documentation**: https://developers.cloudflare.com
- **Wrangler CLI**: https://developers.cloudflare.com/workers/wrangler/
- **Discord Community**: https://discord.cloudflare.com
- **Examples**: https://developers.cloudflare.com/workers/examples/
- **GitHub**: https://github.com/cloudflare
- **Status Page**: https://www.cloudflarestatus.com

## Implementation Checklist

### Workers Setup
- [ ] Install Wrangler CLI (`npm install -g wrangler`)
- [ ] Login to Cloudflare (`wrangler login`)
- [ ] Create project (`wrangler init`)
- [ ] Configure wrangler.toml
- [ ] Add environment variables/secrets
- [ ] Test locally (`wrangler dev`)
- [ ] Deploy (`wrangler deploy`)

### Storage Setup (as needed)
- [ ] Create D1 database and apply schema
- [ ] Create KV namespace
- [ ] Create R2 bucket
- [ ] Configure Durable Objects
- [ ] Set up Queues
- [ ] Add bindings to wrangler.toml

### Pages Setup
- [ ] Connect Git repository or use CLI
- [ ] Configure build settings
- [ ] Set environment variables
- [ ] Add Pages Functions (if needed)
- [ ] Deploy and test

### Production Checklist
- [ ] Set up custom domain
- [ ] Configure DNS records
- [ ] Enable SSL/TLS
- [ ] Set up monitoring/analytics
- [ ] Configure rate limiting
- [ ] Implement error handling
- [ ] Set up CI/CD pipeline
- [ ] Test gradual deployments
- [ ] Document rollback procedure
- [ ] Configure logging/observability
