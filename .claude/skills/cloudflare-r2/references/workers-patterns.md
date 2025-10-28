# Cloudflare R2 Workers Integration Patterns

Advanced patterns for integrating R2 with Cloudflare Workers.

## Table of Contents
- Basic Integration
- File Upload Handlers
- Download & Streaming
- Image Processing
- Authentication & Authorization
- Caching Strategies
- Multipart Upload Workflows
- Event-Driven Patterns
- Error Handling
- Performance Optimization

---

## Basic Integration

### Binding Configuration

**wrangler.toml:**
```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-15"

[[r2_buckets]]
binding = "UPLOADS"
bucket_name = "user-uploads-prod"
preview_bucket_name = "user-uploads-dev"

[[r2_buckets]]
binding = "ASSETS"
bucket_name = "static-assets"
```

**TypeScript types:**
```typescript
interface Env {
  UPLOADS: R2Bucket;
  ASSETS: R2Bucket;
}
```

---

## File Upload Handlers

### Simple Upload Handler

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return new Response('No file uploaded', { status: 400 });
    }

    const key = `uploads/${crypto.randomUUID()}-${file.name}`;

    await env.UPLOADS.put(key, file.stream(), {
      httpMetadata: {
        contentType: file.type,
      },
      customMetadata: {
        originalName: file.name,
        uploadedAt: new Date().toISOString(),
      },
    });

    return new Response(JSON.stringify({ key, size: file.size }), {
      headers: { 'Content-Type': 'application/json' },
    });
  },
};
```

### Authenticated Upload with Validation

```typescript
interface UploadRequest {
  file: File;
  userId: string;
  token: string;
}

async function handleAuthenticatedUpload(
  request: Request,
  env: Env
): Promise<Response> {
  // 1. Verify authentication
  const authHeader = request.headers.get('Authorization');
  if (!authHeader?.startsWith('Bearer ')) {
    return new Response('Unauthorized', { status: 401 });
  }

  const token = authHeader.slice(7);
  const userId = await verifyToken(token); // Your auth logic

  // 2. Parse and validate file
  const formData = await request.formData();
  const file = formData.get('file') as File;

  if (!file) {
    return new Response('No file provided', { status: 400 });
  }

  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!allowedTypes.includes(file.type)) {
    return new Response('Invalid file type', { status: 400 });
  }

  // Validate file size (10MB max)
  if (file.size > 10 * 1024 * 1024) {
    return new Response('File too large', { status: 413 });
  }

  // 3. Upload to R2
  const key = `users/${userId}/${Date.now()}-${file.name}`;

  await env.UPLOADS.put(key, file.stream(), {
    httpMetadata: {
      contentType: file.type,
      cacheControl: 'private, max-age=0',
    },
    customMetadata: {
      userId,
      originalName: file.name,
      uploadedAt: new Date().toISOString(),
      ipAddress: request.headers.get('CF-Connecting-IP') || 'unknown',
    },
  });

  // 4. Return success response
  return new Response(
    JSON.stringify({
      success: true,
      key,
      url: `/files/${key}`,
      size: file.size,
    }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );
}
```

### Direct Upload with Presigned URL Pattern

```typescript
// Generate upload URL (backend)
async function generateUploadUrl(
  request: Request,
  env: Env
): Promise<Response> {
  const { fileName, fileType } = await request.json();

  const key = `uploads/${crypto.randomUUID()}-${fileName}`;

  // Store pending upload metadata
  await env.KV.put(
    `upload:${key}`,
    JSON.stringify({ fileName, fileType, createdAt: Date.now() }),
    { expirationTtl: 3600 }
  );

  return new Response(
    JSON.stringify({
      uploadKey: key,
      uploadUrl: `/api/upload/${key}`,
    }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );
}

// Handle direct upload
async function handleDirectUpload(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  // Verify upload key exists
  const metadata = await env.KV.get(`upload:${key}`);
  if (!metadata) {
    return new Response('Invalid upload key', { status: 400 });
  }

  const { fileType } = JSON.parse(metadata);

  // Upload to R2
  await env.UPLOADS.put(key, request.body, {
    httpMetadata: {
      contentType: fileType,
    },
  });

  // Clean up pending upload
  await env.KV.delete(`upload:${key}`);

  return new Response(JSON.stringify({ success: true, key }), {
    headers: { 'Content-Type': 'application/json' },
  });
}
```

---

## Download & Streaming

### Basic Download Handler

```typescript
async function handleDownload(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const object = await env.UPLOADS.get(key);

  if (object === null) {
    return new Response('File not found', { status: 404 });
  }

  return new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
      'ETag': object.httpEtag,
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
}
```

### Range Request Support (Video Streaming)

```typescript
async function handleRangeRequest(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const rangeHeader = request.headers.get('Range');

  if (!rangeHeader) {
    // No range requested, return full file
    const object = await env.UPLOADS.get(key);
    if (!object) {
      return new Response('Not found', { status: 404 });
    }

    return new Response(object.body, {
      headers: {
        'Content-Type': object.httpMetadata?.contentType || 'video/mp4',
        'Content-Length': object.size.toString(),
        'Accept-Ranges': 'bytes',
      },
    });
  }

  // Parse range header (e.g., "bytes=0-1023")
  const match = rangeHeader.match(/bytes=(\d+)-(\d*)/);
  if (!match) {
    return new Response('Invalid range', { status: 416 });
  }

  const start = parseInt(match[1]);
  const end = match[2] ? parseInt(match[2]) : undefined;

  // Get object with range
  const object = await env.UPLOADS.get(key, {
    range: end !== undefined
      ? { offset: start, length: end - start + 1 }
      : { offset: start },
  });

  if (!object) {
    return new Response('Not found', { status: 404 });
  }

  const actualEnd = end !== undefined ? end : object.size - 1;

  return new Response(object.body, {
    status: 206,
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'video/mp4',
      'Content-Range': `bytes ${start}-${actualEnd}/${object.size}`,
      'Content-Length': object.range.length.toString(),
      'Accept-Ranges': 'bytes',
    },
  });
}
```

### Conditional Requests (If-None-Match)

```typescript
async function handleConditionalRequest(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const ifNoneMatch = request.headers.get('If-None-Match');

  const object = await env.UPLOADS.get(key, {
    onlyIf: ifNoneMatch
      ? { etagDoesNotMatch: ifNoneMatch.replace(/"/g, '') }
      : undefined,
  });

  if (object === null) {
    // ETag matched, return 304
    return new Response(null, {
      status: 304,
      headers: {
        'ETag': ifNoneMatch || '',
        'Cache-Control': 'public, max-age=31536000',
      },
    });
  }

  return new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
      'ETag': object.httpEtag,
      'Cache-Control': 'public, max-age=31536000',
    },
  });
}
```

---

## Image Processing

### On-the-Fly Image Resizing

```typescript
async function handleImageResize(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const url = new URL(request.url);
  const width = parseInt(url.searchParams.get('w') || '0');
  const height = parseInt(url.searchParams.get('h') || '0');
  const quality = parseInt(url.searchParams.get('q') || '85');

  const object = await env.UPLOADS.get(key);
  if (!object) {
    return new Response('Not found', { status: 404 });
  }

  // Use Cloudflare Image Resizing
  const resizedResponse = await fetch(request.url, {
    cf: {
      image: {
        width,
        height,
        quality,
        format: 'auto',
      },
    },
  });

  return new Response(resizedResponse.body, {
    headers: {
      'Content-Type': 'image/webp',
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
}
```

### Cached Thumbnail Generation

```typescript
async function handleThumbnail(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const thumbnailKey = `thumbnails/${key}`;

  // Check if thumbnail exists
  let thumbnail = await env.ASSETS.get(thumbnailKey);

  if (!thumbnail) {
    // Generate thumbnail
    const original = await env.UPLOADS.get(key);
    if (!original) {
      return new Response('Not found', { status: 404 });
    }

    // Resize using Cloudflare Images
    const resized = await fetch(`https://your-domain.com/img/${key}`, {
      cf: {
        image: {
          width: 200,
          height: 200,
          fit: 'cover',
          quality: 80,
        },
      },
    });

    const thumbnailData = await resized.arrayBuffer();

    // Cache thumbnail
    await env.ASSETS.put(thumbnailKey, thumbnailData, {
      httpMetadata: { contentType: 'image/webp' },
    });

    return new Response(thumbnailData, {
      headers: {
        'Content-Type': 'image/webp',
        'Cache-Control': 'public, max-age=31536000',
      },
    });
  }

  return new Response(thumbnail.body, {
    headers: {
      'Content-Type': 'image/webp',
      'Cache-Control': 'public, max-age=31536000',
    },
  });
}
```

---

## Authentication & Authorization

### User-Scoped Access

```typescript
async function handleUserFileAccess(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  // 1. Extract user ID from token
  const token = request.headers.get('Authorization')?.slice(7);
  if (!token) {
    return new Response('Unauthorized', { status: 401 });
  }

  const userId = await verifyToken(token, env);

  // 2. Check if user owns file
  const object = await env.UPLOADS.head(key);
  if (!object) {
    return new Response('Not found', { status: 404 });
  }

  const fileUserId = object.customMetadata?.userId;
  if (fileUserId !== userId) {
    return new Response('Forbidden', { status: 403 });
  }

  // 3. Return file
  const fileObject = await env.UPLOADS.get(key);
  return new Response(fileObject!.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
    },
  });
}
```

### Signed Download URLs

```typescript
async function generateSignedUrl(
  env: Env,
  key: string,
  expiresIn: number
): Promise<string> {
  const expiresAt = Date.now() + expiresIn * 1000;
  const message = `${key}:${expiresAt}`;

  // Sign with HMAC
  const encoder = new TextEncoder();
  const keyData = encoder.encode(env.SECRET_KEY);
  const msgData = encoder.encode(message);

  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const signature = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
  const sigHex = Array.from(new Uint8Array(signature))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');

  return `/files/${key}?expires=${expiresAt}&signature=${sigHex}`;
}

async function verifySignedUrl(
  env: Env,
  key: string,
  expires: string,
  signature: string
): Promise<boolean> {
  const expiresAt = parseInt(expires);
  if (Date.now() > expiresAt) {
    return false;
  }

  const message = `${key}:${expiresAt}`;
  const encoder = new TextEncoder();
  const keyData = encoder.encode(env.SECRET_KEY);
  const msgData = encoder.encode(message);

  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['verify']
  );

  const sigBytes = new Uint8Array(
    signature.match(/.{2}/g)!.map(byte => parseInt(byte, 16))
  );

  return await crypto.subtle.verify('HMAC', cryptoKey, sigBytes, msgData);
}
```

---

## Caching Strategies

### Cache API Integration

```typescript
async function handleCachedDownload(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const cache = caches.default;
  const cacheKey = new Request(request.url, request);

  // Check cache
  let response = await cache.match(cacheKey);
  if (response) {
    return response;
  }

  // Fetch from R2
  const object = await env.UPLOADS.get(key);
  if (!object) {
    return new Response('Not found', { status: 404 });
  }

  response = new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
      'Cache-Control': 'public, max-age=31536000, immutable',
      'ETag': object.httpEtag,
    },
  });

  // Store in cache
  await cache.put(cacheKey, response.clone());

  return response;
}
```

### Smart Cache Invalidation

```typescript
async function invalidateCache(
  env: Env,
  key: string
): Promise<void> {
  const cache = caches.default;

  // Invalidate main file
  await cache.delete(`https://your-domain.com/files/${key}`);

  // Invalidate related files (thumbnails, etc.)
  await cache.delete(`https://your-domain.com/thumbnails/${key}`);
}

async function handleFileUpdate(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  // Upload new version
  await env.UPLOADS.put(key, request.body, {
    httpMetadata: {
      contentType: request.headers.get('Content-Type') || 'application/octet-stream',
    },
  });

  // Invalidate cache
  await invalidateCache(env, key);

  return new Response('Updated', { status: 200 });
}
```

---

## Multipart Upload Workflows

### Complete Multipart Upload Handler

```typescript
interface MultipartSession {
  uploadId: string;
  key: string;
  parts: Map<number, string>;
}

async function initializeMultipartUpload(
  request: Request,
  env: Env
): Promise<Response> {
  const { fileName, fileType } = await request.json();
  const key = `uploads/${crypto.randomUUID()}-${fileName}`;

  const upload = await env.UPLOADS.createMultipartUpload(key, {
    httpMetadata: { contentType: fileType },
  });

  // Store session in KV
  await env.KV.put(
    `multipart:${upload.uploadId}`,
    JSON.stringify({ key, uploadId: upload.uploadId }),
    { expirationTtl: 86400 }  // 24 hours
  );

  return new Response(
    JSON.stringify({
      uploadId: upload.uploadId,
      key,
    }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );
}

async function uploadPart(
  request: Request,
  env: Env
): Promise<Response> {
  const { uploadId, partNumber } = await request.json();

  // Get session
  const sessionData = await env.KV.get(`multipart:${uploadId}`);
  if (!sessionData) {
    return new Response('Invalid upload ID', { status: 400 });
  }

  const { key } = JSON.parse(sessionData);

  // Get multipart upload
  const upload = env.UPLOADS.resumeMultipartUpload(key, uploadId);

  // Upload part
  const part = await upload.uploadPart(partNumber, request.body);

  // Store part info
  await env.KV.put(
    `part:${uploadId}:${partNumber}`,
    JSON.stringify({ partNumber, etag: part.etag }),
    { expirationTtl: 86400 }
  );

  return new Response(
    JSON.stringify({
      partNumber,
      etag: part.etag,
    }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );
}

async function completeMultipartUpload(
  request: Request,
  env: Env
): Promise<Response> {
  const { uploadId, parts } = await request.json();

  // Get session
  const sessionData = await env.KV.get(`multipart:${uploadId}`);
  if (!sessionData) {
    return new Response('Invalid upload ID', { status: 400 });
  }

  const { key } = JSON.parse(sessionData);

  // Complete upload
  const upload = env.UPLOADS.resumeMultipartUpload(key, uploadId);
  const object = await upload.complete(parts);

  // Clean up session
  await env.KV.delete(`multipart:${uploadId}`);

  return new Response(
    JSON.stringify({
      key: object.key,
      size: object.size,
      etag: object.etag,
    }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );
}
```

---

## Event-Driven Patterns

### Event Notification Handler

```typescript
interface R2EventMessage {
  account: string;
  bucket: string;
  object: {
    key: string;
    size: number;
    etag: string;
  };
  action: string;
  eventTime: string;
}

export default {
  async queue(
    batch: MessageBatch<R2EventMessage>,
    env: Env
  ): Promise<void> {
    for (const message of batch.messages) {
      const event = message.body;

      switch (event.action) {
        case 'PutObject':
          await handleNewUpload(event, env);
          break;
        case 'DeleteObject':
          await handleDeletion(event, env);
          break;
      }

      message.ack();
    }
  },
};

async function handleNewUpload(
  event: R2EventMessage,
  env: Env
): Promise<void> {
  const { key } = event.object;

  // Generate thumbnail if image
  if (key.match(/\.(jpg|jpeg|png|webp)$/i)) {
    await generateThumbnail(key, env);
  }

  // Log to analytics
  await env.ANALYTICS.writeDataPoint({
    indexes: [key],
    blobs: [event.action],
    doubles: [event.object.size],
  });
}
```

---

## Error Handling

### Comprehensive Error Handler

```typescript
class R2Error extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code: string
  ) {
    super(message);
  }
}

async function handleR2Operation<T>(
  operation: () => Promise<T>
): Promise<T> {
  try {
    return await operation();
  } catch (error) {
    if (error instanceof R2Error) {
      throw error;
    }

    // Map R2 errors
    if (error.message.includes('Object Not Found')) {
      throw new R2Error('File not found', 404, 'NOT_FOUND');
    }

    if (error.message.includes('Bucket Not Found')) {
      throw new R2Error('Bucket not found', 404, 'BUCKET_NOT_FOUND');
    }

    // Unknown error
    console.error('R2 operation failed:', error);
    throw new R2Error('Internal server error', 500, 'INTERNAL_ERROR');
  }
}

async function handleRequest(
  request: Request,
  env: Env
): Promise<Response> {
  try {
    const result = await handleR2Operation(async () => {
      return await env.UPLOADS.get('file.txt');
    });

    return new Response(result?.body);
  } catch (error) {
    if (error instanceof R2Error) {
      return new Response(
        JSON.stringify({
          error: error.code,
          message: error.message,
        }),
        {
          status: error.statusCode,
          headers: { 'Content-Type': 'application/json' },
        }
      );
    }

    return new Response('Internal error', { status: 500 });
  }
}
```

---

## Performance Optimization

### Parallel Operations

```typescript
async function handleBatchDownload(
  request: Request,
  env: Env
): Promise<Response> {
  const { keys } = await request.json<{ keys: string[] }>();

  // Fetch all objects in parallel
  const objects = await Promise.all(
    keys.map(key => env.UPLOADS.get(key))
  );

  const files = objects
    .filter(obj => obj !== null)
    .map(obj => ({
      key: obj!.key,
      size: obj!.size,
      contentType: obj!.httpMetadata?.contentType,
    }));

  return new Response(JSON.stringify(files), {
    headers: { 'Content-Type': 'application/json' },
  });
}
```

### Streaming Responses

```typescript
async function handleLargeFileStream(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const object = await env.UPLOADS.get(key);
  if (!object) {
    return new Response('Not found', { status: 404 });
  }

  // Return stream directly (don't buffer)
  return new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
      'Content-Length': object.size.toString(),
    },
  });
}
```

## Best Practices Summary

1. **Always stream large files** - never buffer in memory
2. **Use Workers Cache API** for frequently accessed objects
3. **Implement proper error handling** with retries
4. **Validate files before upload** (type, size, content)
5. **Use multipart uploads** for files >100MB
6. **Add comprehensive metadata** for debugging
7. **Implement authentication** for private files
8. **Use range requests** for video streaming
9. **Cache thumbnails** separately from originals
10. **Monitor performance** with analytics
