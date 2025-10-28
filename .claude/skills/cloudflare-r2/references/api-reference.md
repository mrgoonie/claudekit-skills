# Cloudflare R2 API Reference

Complete reference for R2 authentication, endpoints, and API operations.

## Table of Contents
- Authentication & Tokens
- S3 API Endpoints
- Workers API Reference
- Presigned URLs
- S3 Extensions
- API Operations

## Authentication & Tokens

### Access Key Types

**R2 Access Keys (S3 API):**
- Access Key ID + Secret Access Key pair
- Used with S3-compatible SDKs and tools
- Generate: Dashboard → R2 → Manage R2 API Tokens

**Cloudflare API Token (Management API):**
- Used for Terraform and Cloudflare API
- Different from R2 Access Keys
- Generate: Dashboard → My Profile → API Tokens

### Token Permissions

**Account-level:**
- Read-only: list all buckets, object metadata
- Read/Write: full CRUD on all buckets
- Admin: includes bucket creation/deletion

**Bucket-scoped:**
- Read-only: specific bucket access
- Read/Write: specific bucket CRUD
- Cannot create/delete buckets

**Object-level:**
- Read: specific object patterns (prefix-based)
- Write: specific object patterns
- Requires `no_check_bucket = true` in some tools (Rclone)

### Temporary Credentials

Generate via REST API for time-limited access:

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/r2/temp-access-credentials" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -d '{
    "ttl": 3600,
    "permissions": ["read"],
    "objects": ["bucket-name/*"]
  }'
```

Response includes temporary credentials valid for specified TTL.

## S3 API Endpoints

### Standard Endpoint
```
https://<account-id>.r2.cloudflarestorage.com
```

### Jurisdictional Endpoints

For EU compliance:
```
https://<account-id>.eu.r2.cloudflarestorage.com
```

For FEDRAMP:
```
https://<account-id>.fedramp.r2.cloudflarestorage.com
```

**Usage:** All S3 API calls use this endpoint. Always specify region as `"auto"`.

## S3 API Compatibility

### Fully Supported Operations

**Bucket Operations:**
- CreateBucket (PUT /)
- ListBuckets (GET /)
- DeleteBucket (DELETE /)
- HeadBucket (HEAD /)
- GetBucketLocation
- GetBucketCors / PutBucketCors
- GetBucketEncryption / PutBucketEncryption
- GetBucketLifecycleConfiguration / PutBucketLifecycleConfiguration

**Object Operations:**
- PutObject (PUT /bucket/key)
- GetObject (GET /bucket/key)
- HeadObject (HEAD /bucket/key)
- DeleteObject (DELETE /bucket/key)
- CopyObject (PUT /bucket/key with x-amz-copy-source)
- ListObjectsV2 (GET /bucket?list-type=2)

**Multipart Upload:**
- CreateMultipartUpload
- UploadPart
- UploadPartCopy
- CompleteMultipartUpload
- AbortMultipartUpload
- ListMultipartUploads
- ListParts

### Checksum Support

R2 supports these checksum algorithms:
- **CRC32** - fastest, good for error detection
- **CRC32C** - faster than MD5, better error detection
- **SHA-1** - cryptographic hash
- **SHA-256** - strong cryptographic hash

**Usage:**
```javascript
await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "file.txt",
  Body: contents,
  ChecksumAlgorithm: "SHA256",
  ChecksumSHA256: computedChecksum,
}));
```

### Storage Classes

- `STANDARD` - default storage class
- `INFREQUENT_ACCESS` - lower storage cost, retrieval fees

Set during upload:
```javascript
await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "archive.zip",
  Body: contents,
  StorageClass: "INFREQUENT_ACCESS",
}));
```

### SSE-C (Server-Side Encryption with Customer Keys)

Encrypt objects with your own keys:

```javascript
const encryptionKey = crypto.randomBytes(32);
const keyMD5 = crypto.createHash('md5').update(encryptionKey).digest('base64');

await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "sensitive.txt",
  Body: contents,
  SSECustomerAlgorithm: "AES256",
  SSECustomerKey: encryptionKey.toString('base64'),
  SSECustomerKeyMD5: keyMD5,
}));
```

**Important:** Must provide same key for GET/HEAD operations. Key not stored by R2.

### Differences from AWS S3

**Not Supported:**
- Bucket versioning
- Object locking (WORM)
- S3 Select
- Bucket policies (use Cloudflare Access instead)
- ACLs (use bucket-scoped tokens)
- Website hosting (use Workers Sites or Pages)
- Requester Pays
- Inventory reports
- S3 Transfer Acceleration

**Different Behavior:**
- ListObjectsV2: max 1,000 keys per request (vs 1,000 in AWS)
- ETag format differs for multipart uploads
- No bucket ownership controls (single account per bucket)

## S3 Extensions

Cloudflare-specific enhancements to S3 API.

### 1. Unicode Metadata (RFC 2047)

Store UTF-8 metadata values:

```javascript
await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "file.txt",
  Body: contents,
  Metadata: {
    'author': '=?UTF-8?B?' + Buffer.from('Renée').toString('base64') + '?=',
  },
}));
```

Decode on retrieval:
```javascript
const decoded = metadata.author.replace(
  /=\?UTF-8\?B\?(.+?)\?=/g,
  (_, encoded) => Buffer.from(encoded, 'base64').toString('utf8')
);
```

### 2. Auto-Bucket Creation

R2 creates non-existent buckets automatically during PutObject (if token has permission).

Opt-out via header:
```
cf-create-bucket-if-missing: false
```

### 3. Conditional PutObject

Prevent overwrites with condition:

```javascript
await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "file.txt",
  Body: contents,
  Metadata: {
    'cf-copy-if-none-match': '*',  // Fail if object exists
  },
}));
```

Returns 412 Precondition Failed if object exists.

### 4. MERGE Metadata Directive

Merge metadata instead of replacing:

```javascript
await s3.send(new CopyObjectCommand({
  Bucket: "my-bucket",
  CopySource: "/my-bucket/file.txt",
  Key: "file.txt",
  Metadata: {
    'new-field': 'value',
  },
  MetadataDirective: "MERGE",  // Cloudflare extension
}));
```

Keeps existing metadata, adds/updates specified fields.

### 5. Enhanced ListBuckets

Pagination support via `start-after`:

```javascript
const response = await s3.send(new ListBucketsCommand({}));
// Response includes ContinuationToken if more results

const nextPage = await s3.send(new ListBucketsCommand({
  ContinuationToken: response.ContinuationToken,
}));
```

### 6. Conditional CopyObject (Beta)

Prevent destination overwrites:

```javascript
await s3.send(new CopyObjectCommand({
  Bucket: "my-bucket",
  CopySource: "/source-bucket/file.txt",
  Key: "destination.txt",
  Metadata: {
    'cf-copy-destination-if-none-match': '*',
  },
}));
```

## Presigned URLs

Temporary URLs for client-side access without credentials.

### Generation (JavaScript)

**Read URL:**
```javascript
import { GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const url = await getSignedUrl(
  s3Client,
  new GetObjectCommand({ Bucket: "my-bucket", Key: "file.txt" }),
  { expiresIn: 3600 }  // 1 hour
);
```

**Write URL:**
```javascript
import { PutObjectCommand } from "@aws-sdk/client-s3";

const uploadUrl = await getSignedUrl(
  s3Client,
  new PutObjectCommand({ Bucket: "my-bucket", Key: "upload.txt" }),
  { expiresIn: 3600 }
);

// Client uploads via PUT request
fetch(uploadUrl, { method: 'PUT', body: fileData });
```

### Expiry Range
- **Minimum:** 1 second
- **Maximum:** 7 days (604,800 seconds)

### Limitations
- Cannot use with custom domains (requires WAF Pro+ plan)
- Use r2.dev endpoint or direct S3 endpoint
- CORS configuration required for browser usage

### Security Considerations
- URLs contain credentials in query parameters
- Treat as sensitive (don't log or embed publicly)
- Shorter expiry = better security
- Consider Workers API for production apps (no URL exposure)

## Workers API Reference

Native R2 integration for Cloudflare Workers.

### Binding Setup

**wrangler.toml:**
```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "production-bucket"
preview_bucket_name = "preview-bucket"
jurisdiction = "eu"  # Optional: 'eu' or 'fedramp'
```

**TypeScript types:**
```typescript
interface Env {
  MY_BUCKET: R2Bucket;
}
```

### R2Bucket Methods

#### head(key: string): Promise<R2Object | null>

Check if object exists, get metadata:

```typescript
const object = await env.MY_BUCKET.head('file.txt');
if (object) {
  console.log(object.size, object.etag, object.uploaded);
}
```

#### get(key: string, options?: R2GetOptions): Promise<R2ObjectBody | null>

Retrieve object:

```typescript
const object = await env.MY_BUCKET.get('file.txt');
if (object === null) {
  return new Response('Not found', { status: 404 });
}

const text = await object.text();
// Also: object.arrayBuffer(), object.blob(), object.json()
```

**Options:**
```typescript
{
  range?: { offset: number, length?: number } | { suffix: number },
  onlyIf?: {
    etagMatches?: string,
    etagDoesNotMatch?: string,
    uploadedBefore?: Date,
    uploadedAfter?: Date,
  }
}
```

#### put(key: string, value: ReadableStream | ArrayBuffer | string | Blob, options?: R2PutOptions): Promise<R2Object>

Upload object:

```typescript
await env.MY_BUCKET.put('file.txt', 'Hello, World!', {
  httpMetadata: {
    contentType: 'text/plain',
    contentLanguage: 'en-US',
    contentDisposition: 'inline',
    contentEncoding: 'identity',
    cacheControl: 'public, max-age=3600',
    cacheExpiry: new Date(Date.now() + 86400000),
  },
  customMetadata: {
    userId: '12345',
    purpose: 'example',
  },
  storageClass: 'Standard',  // or 'InfrequentAccess'
  md5: computedMD5,  // Optional validation
  sha1: computedSHA1,
  sha256: computedSHA256,
  sha384: computedSHA384,
  sha512: computedSHA512,
});
```

#### delete(keys: string | string[]): Promise<void>

Delete object(s):

```typescript
await env.MY_BUCKET.delete('file.txt');
await env.MY_BUCKET.delete(['file1.txt', 'file2.txt', 'file3.txt']);
```

#### list(options?: R2ListOptions): Promise<R2Objects>

List objects:

```typescript
const listed = await env.MY_BUCKET.list({
  prefix: 'uploads/',
  delimiter: '/',
  cursor: '',
  limit: 1000,
  include: ['httpMetadata', 'customMetadata'],
});

for (const obj of listed.objects) {
  console.log(obj.key, obj.size);
}

if (listed.truncated) {
  const next = await env.MY_BUCKET.list({ cursor: listed.cursor });
}
```

### Multipart Upload API

For large files (>100MB) or parallel uploads:

#### createMultipartUpload(key: string, options?: R2PutOptions): Promise<R2MultipartUpload>

```typescript
const upload = await env.MY_BUCKET.createMultipartUpload('large.mp4', {
  httpMetadata: { contentType: 'video/mp4' },
});

console.log(upload.uploadId, upload.key);
```

#### uploadPart(partNumber: number, value: ReadableStream | ArrayBuffer | string): Promise<R2UploadedPart>

```typescript
const part1 = await upload.uploadPart(1, chunk1);
const part2 = await upload.uploadPart(2, chunk2);

console.log(part1.partNumber, part1.etag);
```

**Constraints:**
- Part numbers: 1-10,000
- Part size: 5 MiB - 5 GiB
- Last part can be smaller than 5 MiB

#### complete(uploadedParts: R2UploadedPart[]): Promise<R2Object>

```typescript
const object = await upload.complete([part1, part2, part3]);
console.log('Upload complete:', object.key);
```

#### abort(): Promise<void>

```typescript
await upload.abort();  // Cancel incomplete upload
```

### R2Object Properties

```typescript
{
  key: string;              // Object key
  version: string;          // Version ID
  size: number;            // Bytes
  etag: string;            // Entity tag
  httpEtag: string;        // Quoted ETag for HTTP
  uploaded: Date;          // Upload timestamp
  checksums: {
    md5?: ArrayBuffer;
    sha1?: ArrayBuffer;
    sha256?: ArrayBuffer;
    sha384?: ArrayBuffer;
    sha512?: ArrayBuffer;
  };
  httpMetadata: {
    contentType?: string;
    contentLanguage?: string;
    contentDisposition?: string;
    contentEncoding?: string;
    cacheControl?: string;
    cacheExpiry?: Date;
  };
  customMetadata: Record<string, string>;
  range?: { offset: number; length: number };
  storageClass: 'Standard' | 'InfrequentAccess';
}
```

### R2ObjectBody (extends R2Object)

Additional methods for reading data:

```typescript
body: ReadableStream;
bodyUsed: boolean;

text(): Promise<string>;
json<T>(): Promise<T>;
arrayBuffer(): Promise<ArrayBuffer>;
blob(): Promise<Blob>;
```

### Memory Limits

Workers have memory constraints:
- **128MB per request** - don't buffer large files
- Use streaming for files >10MB
- Multipart uploads bypass memory limits (parts uploaded separately)

**Streaming example:**
```typescript
const object = await env.MY_BUCKET.get('large.mp4');
return new Response(object.body);  // Stream, don't buffer
```

## API Operations Reference

### Bucket Operations

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| List Buckets | GET | `/` | List all buckets in account |
| Create Bucket | PUT | `/{bucket}` | Create new bucket |
| Delete Bucket | DELETE | `/{bucket}` | Delete empty bucket |
| Head Bucket | HEAD | `/{bucket}` | Check bucket exists |
| Get Location | GET | `/{bucket}?location` | Get bucket location |
| Get CORS | GET | `/{bucket}?cors` | Get CORS config |
| Put CORS | PUT | `/{bucket}?cors` | Set CORS config |
| Delete CORS | DELETE | `/{bucket}?cors` | Remove CORS config |
| Get Lifecycle | GET | `/{bucket}?lifecycle` | Get lifecycle rules |
| Put Lifecycle | PUT | `/{bucket}?lifecycle` | Set lifecycle rules |

### Object Operations

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| List Objects | GET | `/{bucket}?list-type=2` | List objects (v2) |
| Get Object | GET | `/{bucket}/{key}` | Download object |
| Head Object | HEAD | `/{bucket}/{key}` | Get object metadata |
| Put Object | PUT | `/{bucket}/{key}` | Upload object |
| Delete Object | DELETE | `/{bucket}/{key}` | Delete object |
| Copy Object | PUT | `/{bucket}/{key}` + header | Copy object |

### Multipart Upload Operations

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| Create | POST | `/{bucket}/{key}?uploads` | Start multipart upload |
| Upload Part | PUT | `/{bucket}/{key}?partNumber=N&uploadId=ID` | Upload part |
| List Parts | GET | `/{bucket}/{key}?uploadId=ID` | List uploaded parts |
| Complete | POST | `/{bucket}/{key}?uploadId=ID` | Finish upload |
| Abort | DELETE | `/{bucket}/{key}?uploadId=ID` | Cancel upload |
| List Uploads | GET | `/{bucket}?uploads` | List incomplete uploads |

### Class A Operations (Write/List)
Higher cost ($4.50/million after free tier):
- ListBuckets, PutBucket, ListObjects
- PutObject, CopyObject
- CreateMultipartUpload, UploadPart, CompleteMultipartUpload
- LifecycleStorageTierTransition
- PutBucketCors, PutBucketLifecycleConfiguration

### Class B Operations (Read)
Lower cost ($0.36/million after free tier):
- HeadBucket, HeadObject, GetObject
- GetBucketLocation, GetBucketCors, GetBucketLifecycleConfiguration

### Free Operations
- DeleteObject, DeleteBucket
- AbortMultipartUpload

## Rate Limiting

**r2.dev domain:**
- 1,000 requests per minute per bucket
- Use custom domains for production (no rate limits)

**S3 API:**
- No documented rate limits on standard endpoint
- Use reasonable request rates (<10,000 req/sec)

**Workers API:**
- Subject to Workers request limits
- Subrequests count toward subrequest limit (50 per request)

## Error Codes

### Common HTTP Status Codes

- **200 OK** - Success
- **204 No Content** - Success (delete operations)
- **400 Bad Request** - Invalid request format
- **401 Unauthorized** - Invalid credentials
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Bucket or object doesn't exist
- **409 Conflict** - Bucket name already taken
- **412 Precondition Failed** - Conditional request failed
- **413 Payload Too Large** - Object exceeds size limit
- **500 Internal Server Error** - R2 service error

### S3 Error Codes

```xml
<Error>
  <Code>NoSuchKey</Code>
  <Message>The specified key does not exist</Message>
  <Key>nonexistent.txt</Key>
  <RequestId>...</RequestId>
</Error>
```

Common codes:
- `NoSuchBucket` - Bucket doesn't exist
- `NoSuchKey` - Object doesn't exist
- `AccessDenied` - Insufficient permissions
- `InvalidAccessKeyId` - Bad Access Key ID
- `SignatureDoesNotMatch` - Bad Secret Access Key
- `BucketAlreadyExists` - Bucket name taken
- `EntityTooLarge` - Object > 5TB

## Best Practices

### Authentication
- Store credentials in environment variables
- Use bucket-scoped tokens when possible
- Rotate tokens periodically
- Never commit credentials to version control

### API Usage
- Use Workers API for new projects (better performance, no exposed credentials)
- Batch operations when possible (e.g., list + process)
- Implement retry logic with exponential backoff
- Handle 429 rate limit responses gracefully

### Error Handling
- Check HTTP status codes
- Parse S3 error responses for details
- Log errors with request IDs for support
- Implement fallback strategies

### Performance
- Use multipart uploads for files >100MB
- Stream large responses (don't buffer)
- Enable Cloudflare Cache for read-heavy workloads
- Use location hints matching user geography

### Security
- Use HTTPS for all API calls
- Validate checksums on critical uploads
- Implement CORS carefully (don't use wildcard in production)
- Audit access patterns via R2 analytics
