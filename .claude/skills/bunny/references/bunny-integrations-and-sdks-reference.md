# Bunny Integrations, SDKs & Advanced Features Reference

## Official SDKs

### Storage SDKs
| Language | Package | Install |
|----------|---------|---------|
| TypeScript | `@anthropics/bunny-storage-sdk` | `npm i @anthropics/bunny-storage-sdk` |
| .NET | `BunnyCDN.Net.Storage` | `dotnet add package BunnyCDN.Net.Storage` |
| PHP | `bunnycdn/storage` | `composer require bunnycdn/storage` |
| Java | `com.bunnycdn:storage` | Maven/Gradle |

### TypeScript Storage SDK
```typescript
import { BunnyStorage } from "@anthropics/bunny-storage-sdk";
const storage = new BunnyStorage({
  apiKey: process.env.BUNNY_STORAGE_PASSWORD,
  storageZone: "my-zone",
  region: "ny", // optional, default: storage (Falkenstein)
});
await storage.upload("path/file.jpg", fileBuffer);
const files = await storage.list("path/");
const file = await storage.download("path/file.jpg");
await storage.delete("path/file.jpg");
```

## CMS Integrations

### WordPress Plugin
Install via WordPress plugin repository: "bunny.net" or "Bunny CDN"
- Auto-rewrite static asset URLs to CDN
- Storage offloading for media files
- Cache purge from WP admin
- Configuration: WP Admin → Settings → Bunny CDN

### Other CMS
Pre-built guides for: Drupal, Magento, PrestaShop, Shopware, TYPO3, ExpressionEngine, Discourse

## Cloud Storage Origins

Bunny CDN as caching layer in front of:
- **Amazon S3**: Origin URL `https://{bucket}.s3.{region}.amazonaws.com`
- **Azure Blob**: Origin URL `https://{account}.blob.core.windows.net/{container}`
- **Backblaze B2**: Origin URL `https://f00X.backblazeb2.com/file/{bucket}`
- **DigitalOcean Spaces**: Origin URL `https://{space}.{region}.digitaloceanspaces.com`
- **Wasabi**: Origin URL `https://s3.{region}.wasabisys.com/{bucket}`
- **OVH**: Origin URL per OVH configuration

## Token Authentication

### Basic (MD5)
```javascript
const crypto = require("crypto");
function signUrl(securityKey, url, expirationTime) {
  const hashableBase = securityKey + url + expirationTime;
  const token = crypto.createHash("md5").update(hashableBase).digest("base64")
    .replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
  return `${url}?token=${token}&expires=${expirationTime}`;
}
```

### Advanced (SHA256 HMAC)
```javascript
function signUrlAdvanced(securityKey, url, expirationTime, options = {}) {
  const { userIp, pathAllowed, countriesAllowed, countriesBlocked, refererAllowed, speedLimit } = options;
  let hashableBase = securityKey;
  if (pathAllowed) hashableBase += `token_path=${pathAllowed}&`;
  hashableBase += `expires=${expirationTime}`;
  if (userIp) hashableBase += `&token_ip=${userIp}`;
  if (countriesAllowed) hashableBase += `&token_countries=${countriesAllowed}`;
  if (countriesBlocked) hashableBase += `&token_countries_blocked=${countriesBlocked}`;
  if (refererAllowed) hashableBase += `&token_referer=${refererAllowed}`;
  if (speedLimit) hashableBase += `&token_speed_limit=${speedLimit}`;
  
  const token = crypto.createHmac("sha256", securityKey).update(hashableBase).digest("base64")
    .replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
  return `${url}?token=${token}&token_path=${pathAllowed || "/"}&expires=${expirationTime}`;
}
```

## Terraform Provider

```hcl
terraform {
  required_providers {
    bunny = {
      source  = "BunnyWay/bunny"
      version = "~> 0.4"
    }
  }
}

provider "bunny" {
  api_key = var.bunny_api_key
}

# Pull Zone
resource "bunny_pullzone" "cdn" {
  name       = "my-cdn"
  origin_url = "https://origin.example.com"
  
  enable_geo_zone_us   = true
  enable_geo_zone_eu   = true
  enable_geo_zone_asia = true
}

# DNS Zone
resource "bunny_dns_zone" "main" {
  domain = "example.com"
}

resource "bunny_dns_record" "www" {
  zone_id = bunny_dns_zone.main.id
  type    = "CNAME"
  name    = "www"
  value   = bunny_pullzone.cdn.hostname
  ttl     = 300
}

# Storage Zone
resource "bunny_storage_zone" "files" {
  name   = "my-storage"
  region = "DE"
  replication_regions = ["NY", "SG"]
}

# Edge Script
resource "bunny_compute_script" "worker" {
  name        = "my-worker"
  script_type = "standalone"
  code        = file("./worker.js")
}

# Stream Library
resource "bunny_stream_library" "videos" {
  name = "my-videos"
}
```

Available resources: `bunny_pullzone`, `bunny_dns_zone`, `bunny_dns_record`, `bunny_storage_zone`, `bunny_compute_script`, `bunny_stream_library`, `bunny_shield_zone`

## Scriptable DNS

JavaScript-based dynamic DNS responses:

```javascript
function handleQuery(query) {
  // Geo-based routing
  if (query.country === "US") {
    return { type: "A", value: "1.2.3.4", ttl: 300 };
  }
  return { type: "A", value: "5.6.7.8", ttl: 300 };
}
```

Response types:
```javascript
// A record
return { type: "A", value: "1.2.3.4", ttl: 300 };
// AAAA
return { type: "AAAA", value: "::1", ttl: 300 };
// CNAME
return { type: "CNAME", value: "other.example.com", ttl: 300 };
// TXT
return { type: "TXT", value: "v=spf1 ...", ttl: 300 };
// Multiple answers
return [
  { type: "A", value: "1.2.3.4", ttl: 300 },
  { type: "A", value: "5.6.7.8", ttl: 300 }
];
```

Helper objects: `query.country`, `query.continent`, `query.asn`, `query.ip`, `query.name`, `query.type`

## AI Image Generation

```bash
# Generate image via CDN URL parameters
https://cdn.example.com/ai/generate?prompt=a+sunset+over+mountains&engine=flux&width=1024&height=768
```

Engines: `flux`, `sdxl` — configured per Pull Zone.

## Static Site Hosting

Deploy static sites (React, Vue, Vite) to Edge Storage + Pull Zone:
1. Create Storage Zone
2. Create Pull Zone with Storage Zone origin
3. Upload build output to storage zone
4. Set custom 404 → `index.html` for SPA routing
5. Add custom hostname + SSL

## CDN Logging

### Log Forwarding (Syslog)
Configure in Pull Zone settings — streams access logs in real-time.

### Permanent Log Storage
Logs stored in Edge Storage zone. Parts uploaded when closed (by size, time, or midnight UTC).

### Log Format
Raw access logs via API:
```
GET https://logging.bunnycdn.com/{pullZoneId}/{date}.log
```
Headers: `AccessKey: {Account API Key}`

## OpenAPI Specifications

Available at `https://docs.bunny.net/openapi.md`:
- Core API: `https://core-api-public-docs.b-cdn.net/docs/v3/public.json`
- Stream: `https://video.bunnycdn.com/openapi/bunnynet-video-api.public.json`
- Storage: `https://docs.bunny.net/openapi/bunnynet-edge-storage-api.json`
- Shield: `https://docs.bunny.net/openapi/bunny-shield-api.json`
- Scripting: `https://docs.bunny.net/openapi/edge-scripting-api.json`
- Magic Containers: `https://api-mc.opsbunny.net/docs/public/swagger.json`
- Database: `https://api.bunny.net/database/docs/private/api.json`

## Full Documentation Index
Fetch latest: `https://docs.bunny.net/llms.txt` (578 pages)
