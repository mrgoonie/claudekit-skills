# Bunny.net Core API Reference

Base URL: `https://api.bunny.net` | Auth: `AccessKey: {Account API Key}`

## Pull Zones (CDN)

### CRUD Operations
```
GET    /pullzone                    — List all pull zones (paginated)
GET    /pullzone/{id}               — Get pull zone details
POST   /pullzone                    — Create pull zone
POST   /pullzone/{id}               — Update pull zone
DELETE /pullzone/{id}               — Delete pull zone
```

### Create Pull Zone Body
```json
{
  "Name": "my-cdn",
  "OriginUrl": "https://origin.example.com",
  "Type": 0,
  "StorageZoneId": -1,
  "EnableGeoZoneUS": true,
  "EnableGeoZoneEU": true,
  "EnableGeoZoneASIA": true
}
```
Type: 0=Premium, 1=Volume

### Cache & Hostnames
```
POST   /pullzone/{id}/purgeCache              — Purge entire zone cache
POST   /purge?url={encodedUrl}                — Purge single URL
POST   /pullzone/{id}/addHostname             — Add custom hostname {"Hostname":"cdn.example.com"}
DELETE /pullzone/{id}/removeHostname           — Remove hostname {"Hostname":"cdn.example.com"}
POST   /pullzone/{id}/setForceSSL             — Force SSL {"Hostname":"...","ForceSSL":true}
POST   /pullzone/{id}/loadFreeCertificate     — Issue Let's Encrypt cert {"Hostname":"..."}
```

### Edge Rules
```
POST   /pullzone/{id}/edgerules/addOrUpdate   — Add/update edge rule
DELETE /pullzone/{id}/edgerules/{ruleId}      — Delete edge rule
POST   /pullzone/{id}/edgerules/{ruleId}/setEdgeRuleEnabled — Enable/disable
```

Edge Rule body:
```json
{
  "Guid": "rule-guid",
  "ActionType": 1,
  "ActionParameter1": "https://redirect.example.com",
  "Triggers": [{"Type": 0, "PatternMatches": ["*.jpg"], "PatternMatchingType": 0}],
  "TriggerMatchingType": 0,
  "Description": "Redirect JPGs",
  "Enabled": true
}
```
ActionType: 0=ForceSSL, 1=Redirect, 2=OriginUrl, 3=OverrideCacheTime, 4=BlockRequest, 5=SetResponseHeader, 6=SetRequestHeader, 7=ForceDownload, 8=DisableTokenAuth, 9=EnableTokenAuth, 10=OverrideCacheTimePublic, 11=IgnoreQueryString, 14=DisableOptimizer, 15=ForceCompression, 16=SetStatusCode, 17=OriginStorage, 18=SetNetworkRateLimit, 19=SetConnectionLimit, 20=SetRequestsPerSecondLimit

TriggerType: 0=Url, 1=RequestHeader, 2=ResponseHeader, 3=UrlExtension, 4=CountryCode, 5=RemoteIP, 6=UrlQueryString, 7=RandomChance, 8=StatusCode, 9=RequestMethod, 10=CookieValue, 11=CountryStateCode

### Security
```
POST   /pullzone/{id}/addAllowedReferer       — {"Hostname":"allowed.com"}
POST   /pullzone/{id}/removeAllowedReferer
POST   /pullzone/{id}/addBlockedReferer        — {"Hostname":"blocked.com"}
POST   /pullzone/{id}/removeBlockedReferer
POST   /pullzone/{id}/addBlockedIp             — {"BlockedIp":"1.2.3.4"}
POST   /pullzone/{id}/removeBlockedIp
POST   /pullzone/{id}/addCertificate           — Upload custom cert (Base64 PEM)
```

## Storage Zones (Management)

```
GET    /storagezone                  — List storage zones
GET    /storagezone/{id}             — Get storage zone
POST   /storagezone                  — Create storage zone
POST   /storagezone/{id}             — Update storage zone
DELETE /storagezone/{id}             — Delete storage zone
POST   /storagezone/{id}/resetPassword         — Reset password
POST   /storagezone/{id}/resetReadOnlyPassword — Reset read-only password
```

Create body:
```json
{
  "Name": "my-storage",
  "Region": "DE",
  "ReplicationRegions": ["NY","LA","SG"],
  "ZoneTier": 0
}
```
Region: DE (Falkenstein), UK, NY, LA, SG, SYD, BR, JH, SE
ZoneTier: 0=Standard (HDD), 1=Edge (SSD)

## DNS Zones

```
GET    /dnszone                      — List DNS zones (paginated)
GET    /dnszone/{id}                 — Get DNS zone
POST   /dnszone                      — Create zone {"Domain":"example.com"}
POST   /dnszone/{id}                 — Update zone
DELETE /dnszone/{id}                 — Delete zone
GET    /dnszone/{id}/export          — Export BIND zone file
POST   /dnszone/{id}/import          — Import BIND records
```

### DNS Records
```
PUT    /dnszone/{id}/records         — Add record
POST   /dnszone/{id}/records/{recId} — Update record
DELETE /dnszone/{id}/records/{recId} — Delete record
```

Record types: 0=A, 1=AAAA, 2=CNAME, 3=TXT, 4=MX, 5=Redirect, 6=Flatten, 7=PullZone, 8=SRV, 9=CAA, 10=PTR, 11=Script, 12=NS

Record body:
```json
{"Type":0, "Name":"www", "Value":"1.2.3.4", "Ttl":300, "Priority":0, "Weight":0}
```

### DNSSEC
```
POST   /dnszone/{id}/dnssec/enable   — Enable DNSSEC
POST   /dnszone/{id}/dnssec/disable  — Disable DNSSEC
```

## Statistics
```
GET /statistics?dateFrom=2024-01-01&dateTo=2024-01-31&pullZone={id}
```
Returns: BandwidthUsedChart, RequestsServedChart, CacheHitRate, etc.

## Pagination

Response format for list endpoints:
```json
{
  "Items": [...],
  "CurrentPage": 1,
  "TotalItems": 100,
  "HasMoreItems": true
}
```
Query params: `?page=1&perPage=100&search=term`

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Invalid or missing AccessKey |
| 404 | Resource not found |
| 409 | Name conflict / already exists |
| 429 | Rate limited |
| 500 | Server error |
