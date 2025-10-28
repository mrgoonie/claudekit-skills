# Cloudflare R2 Pricing Guide

Comprehensive guide to R2 pricing, cost optimization, and billing.

## Table of Contents
- Pricing Overview
- Storage Classes
- Operations Pricing
- Cost Calculations
- Cost Optimization Strategies
- Billing Examples
- Migration Cost Analysis
- Comparison with Competitors

---

## Pricing Overview

R2's key differentiator: **zero egress fees**. No charges for bandwidth when retrieving data.

### Standard Storage

| Component | Free Tier | Paid Rate |
|-----------|-----------|-----------|
| Storage | 10 GB-month/month | $0.015/GB-month |
| Class A Operations (write/list) | 1 million/month | $4.50/million |
| Class B Operations (read) | 10 million/month | $0.36/million |
| Egress Bandwidth | Unlimited FREE | FREE |

### Infrequent Access Storage

| Component | Free Tier | Paid Rate |
|-----------|-----------|-----------|
| Storage | None | $0.01/GB-month |
| Class A Operations | None | $9.00/million |
| Class B Operations | None | $0.90/million |
| Data Retrieval | None | $0.01/GB |
| Minimum Storage Duration | N/A | 30 days |
| Egress Bandwidth | Unlimited FREE | FREE |

---

## Storage Classes

### Standard Storage

**Best for:**
- Frequently accessed data
- Active applications
- Dynamic content
- User uploads
- Content delivery

**Characteristics:**
- No retrieval fees
- Lower operation costs
- No minimum storage duration
- Optimized for frequent access

### Infrequent Access (IA)

**Best for:**
- Backups and archives
- Cold data (accessed <1x/month)
- Compliance data retention
- Log archives
- Historical data

**Characteristics:**
- 33% cheaper storage ($0.01 vs $0.015)
- Higher operation costs (2x Class B, 2.5x Class A)
- $0.01/GB retrieval fee
- 30-day minimum billing (billed for 30 days even if deleted earlier)

**Break-even analysis:**
```
Standard: $0.015/GB-month storage + $0.36/million reads
IA: $0.01/GB-month storage + $0.90/million reads + $0.01/GB retrieval

IA saves money when:
Retrieval cost < Storage savings
```

**Example:** 1TB data, accessed 10x/year
- Standard: $15/month + negligible operations = $180/year
- IA: $10/month + $100/year retrieval = $220/year
- **Verdict:** Standard better for 10x/year access

**Example:** 1TB data, accessed 2x/year
- Standard: $180/year
- IA: $120/year + $20 retrieval = $140/year
- **Verdict:** IA better for 2x/year access

---

## Operations Pricing

### Class A Operations ($4.50/million after free tier)

**Write Operations:**
- PutObject
- CopyObject
- CompleteMultipartUpload
- CreateMultipartUpload
- UploadPart
- UploadPartCopy

**List Operations:**
- ListBuckets
- ListObjects
- ListObjectsV2
- ListMultipartUploads
- ListParts

**Management Operations:**
- PutBucketCors
- PutBucketLifecycleConfiguration
- PutBucketEncryption

**Lifecycle Transitions:**
- Storage class transitions (Standard ↔ IA)

### Class B Operations ($0.36/million after free tier)

**Read Operations:**
- GetObject
- HeadObject
- HeadBucket

**Metadata Operations:**
- GetBucketLocation
- GetBucketCors
- GetBucketLifecycleConfiguration
- GetBucketEncryption

### Free Operations

- DeleteObject
- DeleteBucket
- AbortMultipartUpload

---

## Cost Calculations

### Storage Billing Metric

**GB-month:** Average peak storage per day over billing period.

**Calculation:**
```
Daily peak storage (30 days)
Sum of daily peaks / 30 days = Average GB-month
Rounded up to next billing unit
```

**Example:**
```
Day 1-10: 50 GB
Day 11-20: 100 GB
Day 21-30: 75 GB

Average = (10×50 + 10×100 + 10×75) / 30 = 75 GB-month
```

**Rounding:** Usage rounded up (1.1 GB-month billed as 2 GB-month)

### Multipart Upload Costs

**Standard approach (5MB parts):**
```
1GB file = 200 parts
Operations = 1 (create) + 200 (upload parts) + 1 (complete) = 202 Class A ops
Cost = 202 / 1,000,000 × $4.50 = $0.00091
```

**Optimized approach (100MB parts):**
```
1GB file = 10 parts
Operations = 1 + 10 + 1 = 12 Class A ops
Cost = 12 / 1,000,000 × $4.50 = $0.000054
```

**Savings:** 94% fewer operations for large chunks

### Lifecycle Transition Costs

**Scenario:** Transition 1TB to Infrequent Access after 90 days

**Transition cost:**
- 1TB = 1,048,576 objects (1MB each)
- Transitions = 1,048,576 Class A operations
- Cost = 1.05 million / 1 million × $4.50 = $4.73

**Monthly savings:**
- Standard: 1,000 GB × $0.015 = $15
- IA: 1,000 GB × $0.01 = $10
- Savings: $5/month

**Payback period:** 1 month (transition cost recovered)

---

## Cost Optimization Strategies

### 1. Maximize Free Tier Usage

**Free tier includes:**
- 10 GB storage
- 1 million Class A operations/month
- 10 million Class B operations/month

**Strategy:** Use for development, testing, small projects

### 2. Optimize Multipart Upload Chunk Size

**Recommendation:** Use largest practical chunk size

```bash
# Rclone optimization
rclone copy large-files/ r2:bucket/ \
  --s3-chunk-size=100M \
  --s3-upload-cutoff=100M
```

**Savings:** Up to 95% fewer Class A operations

### 3. Batch Operations

**Bad practice:**
```javascript
// 1,000 separate list operations
for (const prefix of prefixes) {
  await env.BUCKET.list({ prefix, limit: 1 });
}
```

**Good practice:**
```javascript
// 1 list operation with post-processing
const all = await env.BUCKET.list({ limit: 1000 });
const filtered = all.objects.filter(obj => prefixes.some(p => obj.key.startsWith(p)));
```

### 4. Lifecycle Rules for Automatic Transitions

**Example:** Move logs to IA after 30 days
```bash
wrangler r2 bucket lifecycle put my-bucket --rules '[
  {
    "action": {"type": "Transition", "storageClass": "InfrequentAccess"},
    "filter": {"prefix": "logs/"},
    "daysFromCreation": 30
  }
]'
```

**Savings:** Automatic 33% storage cost reduction for old data

### 5. Abort Incomplete Multipart Uploads

**Cost impact:** Incomplete uploads still charged for storage

```bash
wrangler r2 bucket lifecycle put my-bucket --rules '[
  {
    "action": {"type": "AbortIncompleteMultipartUpload"},
    "filter": {},
    "abortIncompleteMultipartUploadDays": 7
  }
]'
```

### 6. Delete Unnecessary Objects

**Deletions are free** - regularly clean up unused data

### 7. Use Custom Domains with Cloudflare Cache

**Benefit:** Reduce Class B operations by caching at edge

**Setup:**
1. Add custom domain to bucket
2. Enable Cloudflare Cache
3. Set appropriate Cache-Control headers

**Example:**
```javascript
await env.BUCKET.put(key, data, {
  httpMetadata: {
    cacheControl: 'public, max-age=31536000',  // 1 year
  },
});
```

**Savings:** 95%+ reduction in Class B operations for popular files

### 8. Optimize Object Listing

**Bad practice:**
```javascript
// List all 1M objects
const all = await env.BUCKET.list({ limit: 1000 });
// Requires 1,000 API calls
```

**Good practice:**
```javascript
// Use prefix to narrow search
const specific = await env.BUCKET.list({
  prefix: 'user-123/',
  limit: 100,
});
// Single API call
```

### 9. Choose Right Storage Class at Upload

**Avoid transition costs:**
```javascript
// For known archive data, use IA immediately
await env.BUCKET.put(key, data, {
  storageClass: 'InfrequentAccess',
});
```

**Savings:** Skip transition Class A operation

---

## Billing Examples

### Example 1: Small SaaS Application

**Usage:**
- 50 GB storage
- 5,000 uploads/month (PutObject)
- 500,000 downloads/month (GetObject)
- 10,000 list operations

**Cost calculation:**
```
Storage: (50 - 10) GB × $0.015 = $0.60
Class A: (5,000 + 10,000 - 1,000,000) = 0 (within free tier)
Class B: (500,000 - 10,000,000) = 0 (within free tier)
Egress: FREE

Total: $0.60/month
```

### Example 2: Content Delivery Platform

**Usage:**
- 5 TB storage
- 100,000 uploads/month
- 50 million downloads/month
- No list operations (direct access)

**Cost calculation:**
```
Storage: 5,000 GB × $0.015 = $75.00
Class A: (100,000 - 1,000,000) = 0 (within free tier)
Class B: (50,000,000 - 10,000,000) = 40M × $0.36/M = $14.40
Egress: FREE

Total: $89.40/month
```

**AWS S3 comparison:**
```
Storage: 5,000 GB × $0.023 = $115.00
Data transfer out: 50M downloads × 1MB avg = 50TB
Egress: 50,000 GB × $0.09 = $4,500.00

Total: $4,615.00/month
```

**Savings with R2:** $4,525.60/month (98% reduction)

### Example 3: Backup & Archive Service

**Usage:**
- 100 TB storage (Infrequent Access)
- 10,000 uploads/month
- 1,000 restores/month (100 GB total retrieval)

**Cost calculation:**
```
Storage: 100,000 GB × $0.01 = $1,000.00
Class A: 10,000 × $9.00/M = $0.09
Class B: 1,000 × $0.90/M = $0.00 (negligible)
Retrieval: 100 GB × $0.01 = $1.00
Egress: FREE

Total: $1,001.09/month
```

**Standard storage alternative:**
```
Storage: 100,000 GB × $0.015 = $1,500.00
Operations: negligible
Total: $1,500.00/month
```

**Savings with IA:** $498.91/month (33% reduction)

---

## Migration Cost Analysis

### Scenario: Migrating 10TB from AWS S3

**Super Slurper (bulk migration):**
```
Objects: 10,000 (1GB each)
Class A operations: 10,000 (multipart uploads)
Cost: 10,000 / 1,000,000 × $4.50 = $0.045

AWS egress: 10,000 GB × $0.09 = $900.00
Total migration cost: $900.045 (AWS egress dominates)
```

**Sippy (incremental migration):**
```
Objects migrate on first request
No upfront egress fees
Pay AWS egress as objects accessed

Month 1: 20% accessed = $180 AWS egress
Month 2: 30% accessed = $270 AWS egress
Month 3: 50% accessed = $450 AWS egress
Total: $900 (same, but spread over time)
```

**Cost-benefit timeline:**

**Before migration (AWS S3):**
- Storage: $230/month
- Egress (avg 1TB/month): $90/month
- **Total: $320/month**

**After migration (R2):**
- Storage: $150/month
- Egress: $0/month
- **Total: $150/month**

**Savings:** $170/month
**Migration ROI:** 5.3 months to recover egress costs

---

## Comparison with Competitors

### AWS S3 Standard

| Feature | R2 | S3 |
|---------|----|----|
| Storage | $0.015/GB | $0.023/GB |
| PUT requests | $4.50/M | $5.00/M |
| GET requests | $0.36/M | $0.40/M |
| Egress | **FREE** | $0.09/GB |

**R2 savings:** 100% on egress, 35% on storage

### Google Cloud Storage

| Feature | R2 | GCS |
|---------|----|----|
| Storage | $0.015/GB | $0.020/GB |
| Class A ops | $4.50/M | $5.00/M |
| Class B ops | $0.36/M | $0.40/M |
| Egress | **FREE** | $0.12/GB |

**R2 savings:** 100% on egress, 25% on storage

### Azure Blob Storage

| Feature | R2 | Azure |
|---------|----|----|
| Storage | $0.015/GB | $0.018/GB |
| Write ops | $4.50/M | $5.00/M |
| Read ops | $0.36/M | $0.40/M |
| Egress | **FREE** | $0.087/GB |

**R2 savings:** 100% on egress, 17% on storage

---

## Cost Monitoring

### Dashboard Analytics

Access via: Dashboard → R2 → Bucket → Metrics

**Available metrics:**
- Storage usage (GB-month)
- Class A operation count
- Class B operation count
- Request rates

### GraphQL API Queries

```graphql
query {
  viewer {
    accounts(filter: { accountTag: $accountId }) {
      r2OperationsAdaptiveGroups(
        limit: 100
        filter: {
          datetime_geq: "2024-01-01T00:00:00Z"
          datetime_lt: "2024-02-01T00:00:00Z"
        }
      ) {
        sum {
          requests
        }
        dimensions {
          date
          actionType
        }
      }
    }
  }
}
```

### Cost Alerts

**Set up billing alerts:**
1. Dashboard → Billing → Notifications
2. Configure threshold (e.g., $100/month)
3. Receive email when exceeded

---

## Best Practices Summary

1. **Use free tier** for dev/test environments
2. **Optimize multipart uploads** with large chunks
3. **Enable lifecycle rules** for automatic transitions
4. **Cache frequently accessed files** at Cloudflare edge
5. **Delete incomplete multipart uploads** after 7 days
6. **Use Infrequent Access** for data accessed <1x/month
7. **Batch operations** to reduce API calls
8. **Monitor costs** via dashboard analytics
9. **Choose storage class at upload** to avoid transition costs
10. **Leverage zero egress** for high-bandwidth applications

---

## Key Takeaway

R2's **zero egress fees** make it dramatically cheaper for:
- Content delivery networks
- Data-heavy applications
- Video/media streaming
- Backup/restore services
- Multi-cloud architectures

**Cost savings increase with bandwidth usage** - the more data transferred, the greater the savings over traditional cloud storage.
