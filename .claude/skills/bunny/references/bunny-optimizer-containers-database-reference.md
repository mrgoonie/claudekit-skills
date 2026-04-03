# Bunny Optimizer, Magic Containers & Database Reference

## Bunny Optimizer

Enable via Pull Zone settings. Provides automatic optimization + dynamic image manipulation.

### Automatic Optimization (Pull Zone Setting)
- Image optimization (WebP/AVIF conversion, lossy/lossless compression)
- CSS/JS minification
- Smart image lazy loading
- HTML prerender for SPAs (SEO)

### Dynamic Image Manipulation (URL Parameters)

Append query params to any image URL served through Bunny CDN:

```
https://cdn.example.com/image.jpg?width=800&height=600&quality=85
```

| Parameter | Description | Example |
|-----------|-------------|---------|
| `width` | Resize width (px) | `?width=800` |
| `height` | Resize height (px) | `?height=600` |
| `quality` | Compression 1-100 | `?quality=85` |
| `sharpen` | Sharpen (true/false) | `?sharpen=true` |
| `blur` | Blur radius (1-100) | `?blur=10` |
| `crop` | Crop dimensions | `?crop=100,100,400,300` |
| `crop_gravity` | Auto-crop position | `?crop_gravity=center` |
| `flip` | Flip vertical | `?flip=true` |
| `flop` | Flip horizontal | `?flop=true` |
| `brightness` | Brightness (-100 to 100) | `?brightness=20` |
| `saturation` | Saturation (-100 to 100) | `?saturation=-50` |
| `hue` | Hue rotation (0-360) | `?hue=180` |
| `contrast` | Contrast (-100 to 100) | `?contrast=10` |
| `sepia` | Sepia tone (0-100) | `?sepia=80` |
| `auto_optimize` | Format auto-select | `?auto_optimize=medium` |
| `aspect_ratio` | Force aspect ratio | `?aspect_ratio=16:9` |
| `output` | Force output format | `?output=webp` |
| `class` | Image class preset | `?class=thumbnail` |

### Face Detection Cropping
```
?crop_gravity=face&width=200&height=200
```

### Image Watermarking
Configure watermark image in Pull Zone settings. Auto-applied to all images.

### Image Classes (Presets)
Define reusable transformation presets in Pull Zone settings:
```
Class name: "thumbnail" → width=200, height=200, crop_gravity=center, quality=80
Usage: ?class=thumbnail
```

### Burrow Smart Routing
Optimizes uncached request paths via intelligent routing. Enable in Pull Zone settings.

---

## Magic Containers

Base URL: `https://api.bunny.net/compute/container` | Auth: `AccessKey: {Account API Key}`

### Application CRUD
```
GET    /compute/container                       — List applications
GET    /compute/container/{id}                  — Get application
POST   /compute/container                       — Create application
PUT    /compute/container/{id}                  — Update application (full replace)
PATCH  /compute/container/{id}                  — Partial update (JSON Merge Patch)
DELETE /compute/container/{id}                  — Delete application
```

### Deployment
```
POST   /compute/container/{id}/deploy           — Deploy application
POST   /compute/container/{id}/undeploy         — Stop without deleting
POST   /compute/container/{id}/restart          — Restart all pods
```

### Create Application Body
```json
{
  "Name": "my-app",
  "Containers": [{
    "Name": "web",
    "Image": "nginx:latest",
    "CpuLimit": 1000,
    "MemoryLimit": 512,
    "EnvironmentVariables": [
      {"Name": "NODE_ENV", "Value": "production"}
    ],
    "Endpoints": [{
      "Type": "CDN",
      "Port": 3000,
      "Hostname": "app.example.com"
    }]
  }],
  "DeploymentType": "Magic",
  "AutoscalingSettings": {
    "MinReplicas": 1,
    "MaxReplicas": 5
  }
}
```
CpuLimit in millicores (1000 = 1 vCPU), MemoryLimit in MB.
Endpoint Type: "CDN" or "Anycast".

### Container Registries
```
GET    /compute/container-registries            — List registries
POST   /compute/container-registries            — Add registry
PUT    /compute/container-registries/{id}       — Update registry
DELETE /compute/container-registries/{id}       — Delete registry
```

### Volumes
```
GET    /compute/container/{id}/volumes          — List volumes
PUT    /compute/container/{id}/volumes/{volId}  — Update volume
DELETE /compute/container/{id}/volumes/{volId}/instances      — Delete all instances
DELETE /compute/container/{id}/volumes/{volId}/instances/{iid} — Delete instance
POST   /compute/container/{id}/volumes/{volId}/detach         — Detach volume
```

### Regions
```
GET    /compute/container/regions               — List available regions
GET    /compute/container/{id}/region-settings  — Get region settings
PUT    /compute/container/{id}/region-settings  — Update region settings
```

### Autoscaling
```
GET    /compute/container/{id}/autoscaling      — Get settings
PUT    /compute/container/{id}/autoscaling      — Update settings
```

### Monitoring & Logs
```
GET    /compute/container/{id}/overview         — Application overview (CPU, RAM, latency)
GET    /compute/container/{id}/statistics       — Historical stats
GET    /compute/container/{id}/usage-summary    — Usage/cost summary
```

### Log Forwarding
```
GET    /compute/container/log-forwarding                — List configs
POST   /compute/container/log-forwarding                — Create config
PUT    /compute/container/log-forwarding/{id}           — Update config
DELETE /compute/container/log-forwarding/{id}           — Delete config
```

### Deploy with GitHub Actions
```yaml
name: Deploy to Bunny
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push image
        run: docker build -t registry/app:latest . && docker push registry/app:latest
      - name: Update container
        run: |
          curl -X PATCH "https://api.bunny.net/compute/container/$APP_ID" \
            -H "AccessKey: ${{ secrets.BUNNY_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"Containers":[{"Name":"web","Image":"registry/app:latest"}]}'
      - name: Deploy
        run: |
          curl -X POST "https://api.bunny.net/compute/container/$APP_ID/deploy" \
            -H "AccessKey: ${{ secrets.BUNNY_API_KEY }}"
```

### Injected Environment Variables
Bunny auto-injects into containers:
- `BUNNY_REGION` — current region code
- `BUNNY_APP_ID` — application ID
- `BUNNY_POD_ID` — pod ID

---

## Bunny Database

Globally distributed SQLite-compatible database (libSQL).

### Connection URLs
```
Primary: libsql://{db-name}-{account}.turso.io
HTTP API: https://{db-name}-{account}.turso.io
```

### Authentication
Use database auth tokens (JWT format) from dashboard.

### SQL API (HTTP)
```bash
curl -X POST "https://{db-name}-{account}.turso.io/v2/pipeline" \
  -H "Authorization: Bearer $DB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"requests":[{"type":"execute","stmt":{"sql":"SELECT * FROM users WHERE id = ?","args":[{"type":"integer","value":"1"}]}}]}'
```

### Client SDKs

**TypeScript:**
```typescript
import { createClient } from "@libsql/client";
const db = createClient({
  url: "libsql://{db-name}-{account}.turso.io",
  authToken: process.env.DB_TOKEN,
});
const result = await db.execute("SELECT * FROM users");
```

**Go:**
```go
import "github.com/tursodatabase/libsql-client-go/libsql"
db, _ := libsql.NewClient("libsql://...", libsql.WithAuthToken("..."))
rows, _ := db.Query("SELECT * FROM users")
```

**Rust:**
```rust
use libsql::Builder;
let db = Builder::new_remote("libsql://...", "token").build().await?;
let conn = db.connect()?;
let rows = conn.query("SELECT * FROM users", ()).await?;
```

### Database Shell
```bash
bunny db shell {db-name}
```

### Limits (Public Preview)
- Max databases: 10
- Max DB size: 1GB
- Max rows per query: 10,000
- Max concurrent connections: 100

### Replication
- Primary region for writes, read replicas distributed globally
- Eventual consistency for reads (typically <100ms)
- Strong consistency available via primary reads
