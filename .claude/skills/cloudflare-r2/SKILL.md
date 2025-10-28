---
name: cloudflare-r2
description: Guide for implementing Cloudflare R2 - S3-compatible object storage with zero egress fees. Use when implementing file storage, uploads/downloads, data migration to/from R2, configuring buckets, integrating with Workers, or working with R2 APIs and SDKs.
---

# Cloudflare R2

S3-compatible object storage with zero egress bandwidth fees. Built on Cloudflare's global network for high durability (11 nines) and strong consistency.

## When to Use This Skill

- Implementing object storage for applications
- Migrating from AWS S3 or other storage providers
- Setting up file uploads/downloads
- Configuring public or private buckets
- Integrating R2 with Cloudflare Workers
- Using R2 with S3-compatible tools and SDKs
- Configuring CORS, lifecycles, or event notifications
- Optimizing storage costs with zero egress fees

## Prerequisites

**Required:**
- Cloudflare account with R2 purchased
- Account ID from Cloudflare dashboard

**For API access:**
- R2 Access Keys (Access Key ID + Secret Access Key)
- Generate from: Cloudflare Dashboard → R2 → Manage R2 API Tokens

**For Wrangler CLI:**
```bash
npm install -g wrangler
wrangler login
```

## Core Concepts

### Architecture
- **S3-compatible API** - works with AWS SDKs and tools
- **Workers API** - native Cloudflare Workers integration
- **Global network** - strong consistency across all regions
- **Zero egress fees** - no bandwidth charges for data retrieval

### Storage Classes
- **Standard** - default, optimized for frequent access
- **Infrequent Access** - lower storage cost, retrieval fees apply, 30-day minimum

### Access Methods
1. **R2 Workers Binding** - serverless integration (recommended for new apps)
2. **S3 API** - compatibility with existing tools
3. **Public buckets** - direct HTTP access via custom domains or r2.dev
4. **Presigned URLs** - temporary access without credentials

## Quick Start

### 1. Create Bucket

**Wrangler:**
```bash
wrangler r2 bucket create my-bucket
```

**With location hint:**
```bash
wrangler r2 bucket create my-bucket --location=wnam
```

Locations: `wnam` (West NA), `enam` (East NA), `weur` (West EU), `eeur` (East EU), `apac` (Asia Pacific)

### 2. Upload Object

**Wrangler:**
```bash
wrangler r2 object put my-bucket/file.txt --file=./local-file.txt
```

**Workers API:**
```javascript
await env.MY_BUCKET.put('file.txt', fileContents, {
  httpMetadata: {
    contentType: 'text/plain',
  },
});
```

### 3. Download Object

**Wrangler:**
```bash
wrangler r2 object get my-bucket/file.txt --file=./downloaded.txt
```

**Workers API:**
```javascript
const object = await env.MY_BUCKET.get('file.txt');
const contents = await object.text();
```

## Workers Integration

### Binding Configuration

**wrangler.toml:**
```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
preview_bucket_name = "my-bucket-preview"
```

### Common Operations

**Upload with metadata:**
```javascript
await env.MY_BUCKET.put('user-uploads/photo.jpg', imageData, {
  httpMetadata: {
    contentType: 'image/jpeg',
    cacheControl: 'public, max-age=31536000',
  },
  customMetadata: {
    uploadedBy: userId,
    uploadDate: new Date().toISOString(),
  },
});
```

**Download with streaming:**
```javascript
const object = await env.MY_BUCKET.get('large-file.mp4');
if (object === null) {
  return new Response('Not found', { status: 404 });
}

return new Response(object.body, {
  headers: {
    'Content-Type': object.httpMetadata.contentType,
    'ETag': object.etag,
  },
});
```

**List objects:**
```javascript
const listed = await env.MY_BUCKET.list({
  prefix: 'user-uploads/',
  limit: 100,
});

for (const object of listed.objects) {
  console.log(object.key, object.size);
}
```

**Delete object:**
```javascript
await env.MY_BUCKET.delete('old-file.txt');
```

**Check if object exists:**
```javascript
const object = await env.MY_BUCKET.head('file.txt');
if (object) {
  console.log('Exists:', object.size, 'bytes');
}
```

## S3 SDK Integration

### AWS CLI

**Configure:**
```bash
aws configure
# Access Key ID: <your-key-id>
# Secret Access Key: <your-secret>
# Region: auto
```

**Operations:**
```bash
# List buckets
aws s3api list-buckets --endpoint-url https://<accountid>.r2.cloudflarestorage.com

# Upload file
aws s3 cp file.txt s3://my-bucket/ --endpoint-url https://<accountid>.r2.cloudflarestorage.com

# Generate presigned URL (expires in 1 hour)
aws s3 presign s3://my-bucket/file.txt --endpoint-url https://<accountid>.r2.cloudflarestorage.com --expires-in 3600
```

### JavaScript (AWS SDK v3)

```javascript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({
  region: "auto",
  endpoint: `https://${accountId}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: process.env.R2_ACCESS_KEY_ID,
    secretAccessKey: process.env.R2_SECRET_ACCESS_KEY,
  },
});

await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "file.txt",
  Body: fileContents,
}));
```

### Python (Boto3)

```python
import boto3

s3 = boto3.client(
    service_name="s3",
    endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name="auto",
)

# Upload file
s3.upload_fileobj(file_obj, 'my-bucket', 'file.txt')

# Download file
s3.download_file('my-bucket', 'file.txt', './local-file.txt')
```

### Rclone (Large Files)

**Configure:**
```bash
rclone config
# Select: Amazon S3 → Cloudflare R2
# Enter credentials and endpoint
```

**Upload with multipart optimization:**
```bash
# For large files (>100MB)
rclone copy large-video.mp4 r2:my-bucket/ \
  --s3-upload-cutoff=100M \
  --s3-chunk-size=100M
```

## Public Buckets

### Enable Public Access

**Wrangler:**
```bash
wrangler r2 bucket create my-public-bucket
# Then enable in dashboard: R2 → Bucket → Settings → Public Access
```

### Access URLs

**r2.dev (development only, rate-limited):**
```
https://pub-<hash>.r2.dev/file.txt
```

**Custom domain (recommended for production):**
1. Dashboard → R2 → Bucket → Settings → Public Access
2. Add custom domain
3. Cloudflare handles DNS/TLS automatically

## CORS Configuration

**Required for:**
- Browser-based uploads
- Cross-origin API calls
- Presigned URL usage from web apps

**Wrangler:**
```bash
wrangler r2 bucket cors put my-bucket --rules '[
  {
    "AllowedOrigins": ["https://example.com"],
    "AllowedMethods": ["GET", "PUT", "POST"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 3600
  }
]'
```

**Important:** Origins must match exactly (no trailing slash).

## Multipart Uploads

For files >100MB or parallel uploads:

**Workers API:**
```javascript
const multipart = await env.MY_BUCKET.createMultipartUpload('large-file.mp4');

// Upload parts (5MiB - 5GiB each, max 10,000 parts)
const part1 = await multipart.uploadPart(1, chunk1);
const part2 = await multipart.uploadPart(2, chunk2);

// Complete upload
const object = await multipart.complete([part1, part2]);
```

**Constraints:**
- Part size: 5MiB - 5GiB
- Max parts: 10,000
- Max object size: 5TB
- Incomplete uploads auto-abort after 7 days (configurable via lifecycle)

## Data Migration

### Sippy (Incremental, On-Demand)

Best for: Gradual migration, avoiding upfront egress fees

```bash
# Enable for bucket
wrangler r2 bucket sippy enable my-bucket \
  --provider=aws \
  --bucket=source-bucket \
  --region=us-east-1 \
  --access-key-id=$AWS_KEY \
  --secret-access-key=$AWS_SECRET
```

Objects migrate when first requested. Subsequent requests served from R2.

### Super Slurper (Bulk, One-Time)

Best for: Complete migration, known object list

1. Dashboard → R2 → Data Migration → Super Slurper
2. Select source provider (AWS, GCS, Azure)
3. Enter credentials and bucket name
4. Start migration

## Lifecycle Rules

Auto-delete or transition storage classes:

**Wrangler:**
```bash
wrangler r2 bucket lifecycle put my-bucket --rules '[
  {
    "action": {"type": "AbortIncompleteMultipartUpload"},
    "filter": {},
    "abortIncompleteMultipartUploadDays": 7
  },
  {
    "action": {"type": "Transition", "storageClass": "InfrequentAccess"},
    "filter": {"prefix": "archives/"},
    "daysFromCreation": 90
  }
]'
```

## Event Notifications

Trigger Workers on bucket events:

**Wrangler:**
```bash
wrangler r2 bucket notification create my-bucket \
  --queue=my-queue \
  --event-type=object-create
```

**Supported events:**
- `object-create` - new uploads
- `object-delete` - deletions

**Message format:**
```json
{
  "account": "account-id",
  "bucket": "my-bucket",
  "object": {"key": "file.txt", "size": 1024, "etag": "..."},
  "action": "PutObject",
  "eventTime": "2024-01-15T12:00:00Z"
}
```

## Best Practices

### Performance
- Use Cloudflare Cache with custom domains for frequently accessed objects
- Multipart uploads for files >100MB (faster, more reliable)
- Rclone for batch operations (concurrent transfers)
- Location hints match user geography

### Security
- Never commit Access Keys to version control
- Use environment variables for credentials
- Bucket-scoped tokens for least privilege
- Presigned URLs for temporary access
- Enable Cloudflare Access for additional protection

### Cost Optimization
- Infrequent Access storage for archives (30+ day retention)
- Lifecycle rules to auto-transition or delete
- Larger multipart chunks = fewer Class A operations
- Monitor usage via dashboard analytics

### Naming
- Bucket names: lowercase, hyphens, 3-63 chars
- Avoid sequential prefixes for better performance (e.g., use hashed prefixes)
- No dots in bucket names if using custom domains with TLS

## Limits

- **Buckets per account:** 1,000
- **Object size:** 5TB max
- **Bucket name:** 3-63 characters
- **Lifecycle rules:** 1,000 per bucket
- **Event notification rules:** 100 per bucket
- **r2.dev rate limit:** 1,000 req/min (use custom domains for production)

## Troubleshooting

**401 Unauthorized:**
- Verify Access Keys are correct
- Check endpoint URL includes account ID
- Ensure region is "auto" for most operations

**403 Forbidden:**
- Check bucket permissions and token scopes
- Verify CORS configuration for browser requests
- Confirm bucket exists and name is correct

**404 Not Found:**
- Object key case-sensitive
- Check bucket name spelling
- Verify object was uploaded successfully

**Presigned URLs not working:**
- Verify CORS configuration
- Check URL expiry time
- Ensure origin matches CORS rules exactly

**Multipart upload failures:**
- Part size must be 5MiB - 5GiB
- Max 10,000 parts per upload
- Complete upload within 7 days (or configure lifecycle)

## Reference Files

For detailed documentation, see:
- `references/api-reference.md` - Complete API endpoint documentation
- `references/sdk-examples.md` - SDK examples for all languages
- `references/workers-patterns.md` - Advanced Workers integration patterns
- `references/pricing-guide.md` - Detailed pricing and cost optimization

## Additional Resources

- **Documentation:** https://developers.cloudflare.com/r2/
- **Wrangler Commands:** https://developers.cloudflare.com/r2/reference/wrangler-commands/
- **S3 Compatibility:** https://developers.cloudflare.com/r2/api/s3/api/
- **Workers API:** https://developers.cloudflare.com/r2/api/workers/workers-api-reference/
