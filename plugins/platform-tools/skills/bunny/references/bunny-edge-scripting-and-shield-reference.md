# Bunny Edge Scripting & Shield Reference

## Edge Scripting

Base URL: `https://api.bunny.net/compute` | Auth: `AccessKey: {Account API Key}`

### Script Management
```
GET    /compute/script                    — List all edge scripts
GET    /compute/script/{id}               — Get script details
POST   /compute/script                    — Create script
POST   /compute/script/{id}               — Update script
DELETE /compute/script/{id}               — Delete script
```

Create body:
```json
{"Name": "my-script", "ScriptType": 0}
```
ScriptType: 0=Standalone, 1=Middleware

### Code & Deployment
```
GET    /compute/script/{id}/code          — Get current code
POST   /compute/script/{id}/code          — Upload code {"Code":"..."}
POST   /compute/script/{id}/publish       — Publish new release
GET    /compute/script/{id}/releases      — List releases
```

### Secrets & Variables
```
GET    /compute/script/{id}/secrets       — List secrets
POST   /compute/script/{id}/secrets       — Add secret {"Name":"key","Value":"val"}
PUT    /compute/script/{id}/secrets       — Upsert secret
DELETE /compute/script/{id}/secrets/{name} — Delete secret

GET    /compute/script/{id}/variables/{name}  — Get variable
POST   /compute/script/{id}/variables         — Add variable
PUT    /compute/script/{id}/variables         — Upsert variable
DELETE /compute/script/{id}/variables/{name}  — Delete variable
```

### Standalone Script Template
```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    if (url.pathname === "/api/data") {
      return new Response(JSON.stringify({ status: "ok" }), {
        headers: { "Content-Type": "application/json" }
      });
    }
    
    return new Response("Hello from the edge!", {
      headers: { "Content-Type": "text/plain" }
    });
  }
};
```

### Middleware Script Template
```javascript
export default {
  async fetch(request, env) {
    // Modify request before origin
    const modifiedRequest = new Request(request.url, {
      method: request.method,
      headers: new Headers(request.headers),
      body: request.body
    });
    modifiedRequest.headers.set("X-Custom-Header", "value");
    
    // Fetch from origin
    const response = await fetch(modifiedRequest);
    
    // Modify response
    const newResponse = new Response(response.body, response);
    newResponse.headers.set("X-Processed-By", "bunny-edge");
    return newResponse;
  }
};
```

### HTMLRewriter (Middleware)
```javascript
const rewriter = new HTMLRewriter()
  .on("title", { element(el) { el.setInnerContent("New Title"); } })
  .on("a[href]", { element(el) { el.setAttribute("target", "_blank"); } })
  .on("body", { element(el) { el.append('<script src="/analytics.js"></script>', { html: true }); } });

return rewriter.transform(response);
```

### Node:FS (Edge Storage Access)
```javascript
import * as fs from "node:fs";
const data = fs.readFileSync("/path/to/file.txt", "utf-8");
fs.writeFileSync("/path/to/output.txt", "content");
```

### Limits
- Max execution time: 50ms (can be extended)
- Max memory: 128MB
- Max script size: 10MB
- Max subrequests: 50 per invocation

### GitHub Integration
Deploy via GitHub Actions:
```yaml
- uses: BunnyWay/actions/deploy@main
  with:
    script_id: ${{ secrets.BUNNY_SCRIPT_ID }}
    deploy_key: ${{ secrets.BUNNY_DEPLOY_KEY }}
    file: ./dist/worker.js
```

---

## Bunny Shield (WAF, DDoS, Security)

### Shield Zones
```
POST   /shield/zone                            — Create shield zone for pull zone
GET    /shield/zone                            — List all shield zones
GET    /shield/zone/{id}                       — Get shield zone config
POST   /shield/zone/{id}                       — Update shield zone
GET    /shield/zone/pullzone/{pullZoneId}      — Get shield for pull zone
```

### WAF Rules
```
GET    /shield/zone/{id}/waf/rules             — List WAF rules
GET    /shield/zone/{id}/waf/rules/custom      — List custom WAF rules
POST   /shield/zone/{id}/waf/rules/custom      — Create custom rule
PUT    /shield/zone/{id}/waf/rules/custom/{ruleId} — Update custom rule
DELETE /shield/zone/{id}/waf/rules/custom/{ruleId} — Delete custom rule
GET    /shield/zone/{id}/waf/profiles          — List WAF profiles
POST   /shield/zone/{id}/waf/review/{ruleId}   — Review triggered rule
```

Custom WAF rule body:
```json
{
  "ruleName": "Block SQL Injection",
  "ruleDescription": "Blocks common SQL injection patterns",
  "ruleConfiguration": {
    "variableTypes": [{"variableType": "QUERY_STRING"}],
    "operatorType": "REGEX",
    "transformationTypes": ["NONE"],
    "matchValue": "(union|select|insert|drop|delete|update).*",
    "actionType": "BLOCK"
  }
}
```

### Rate Limiting
```
GET    /shield/zone/{id}/ratelimits            — List rate limits
POST   /shield/zone/{id}/ratelimits            — Create rate limit
PUT    /shield/zone/{id}/ratelimits/{rlId}     — Update rate limit
DELETE /shield/zone/{id}/ratelimits/{rlId}     — Delete rate limit
```

Rate limit body:
```json
{
  "name": "API Rate Limit",
  "requestsPerSecond": 100,
  "blockTime": 60,
  "actionType": "BLOCK",
  "matchExpression": "/api/*"
}
```

### Access Lists
```
GET    /shield/zone/{id}/accesslists           — List access lists
POST   /shield/zone/{id}/accesslists           — Create access list
PUT    /shield/zone/{id}/accesslists/{alId}    — Update access list
DELETE /shield/zone/{id}/accesslists/{alId}    — Delete access list
```

### Bot Detection
```
GET    /shield/zone/{id}/botdetection          — Get bot detection config
POST   /shield/zone/{id}/botdetection          — Update bot detection config
```

### DDoS Mitigation
```
GET    /shield/zone/{id}/ddos                  — Get DDoS config
POST   /shield/zone/{id}/ddos                  — Update DDoS settings
```

### Metrics & Logs
```
GET    /shield/zone/{id}/metrics               — Overview metrics
GET    /shield/zone/{id}/metrics/waf/{ruleId}  — WAF rule metrics
GET    /shield/zone/{id}/metrics/ratelimits     — Rate limit metrics
GET    /shield/zone/{id}/metrics/botdetection   — Bot detection metrics
GET    /shield/zone/{id}/eventlogs             — Event logs
```

### Upload Scanning
```
GET    /shield/zone/{id}/uploadscanning        — Get scan config
POST   /shield/zone/{id}/uploadscanning        — Update scan config
```
Scans uploads for viruses, malware, and CSAM.
