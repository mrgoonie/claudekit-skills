# Bunny Edge Storage & Stream API Reference

## Edge Storage API

Base URL: `https://{region}.bunnycdn.com`
Auth: `AccessKey: {Storage Zone Password}` (NOT the account API key)

Regions: `storage` (Falkenstein default), `uk`, `ny`, `la`, `sg`, `se`, `br`, `jh`, `syd`

### File Operations

```
PUT    /{zoneName}/{path}   — Upload file (raw binary body, NO encoding)
GET    /{zoneName}/{path}   — Download file
DELETE /{zoneName}/{path}   — Delete file/directory (recursive)
GET    /{zoneName}/{path}/  — List directory (trailing slash required)
```

### Upload — Critical Details
- Send file as raw binary in request body — no multipart, no base64
- Content-Type should match file type
- Directory tree auto-created if missing
- Returns 201 on success
- Optional header `Checksum: {SHA256}` for integrity verification

```bash
curl -X PUT "https://storage.bunnycdn.com/my-zone/images/photo.jpg" \
  -H "AccessKey: $STORAGE_PASSWORD" \
  -H "Content-Type: image/jpeg" \
  -H "Checksum: abc123sha256hash" \
  --upload-file ./photo.jpg
```

### List Directory Response
```json
[
  {
    "Guid": "file-guid",
    "StorageZoneName": "my-zone",
    "Path": "/my-zone/images/",
    "ObjectName": "photo.jpg",
    "Length": 102400,
    "LastChanged": "2024-01-15T10:30:00Z",
    "IsDirectory": false,
    "ServerId": 0,
    "ArrayNumber": 0,
    "DateCreated": "2024-01-15T10:30:00Z",
    "UserId": "user-id",
    "ContentType": "image/jpeg",
    "StorageZoneId": 12345,
    "Checksum": "sha256hash",
    "ReplicatedZones": "NY,LA"
  }
]
```

### Official SDKs

| Language | Package |
|----------|---------|
| TypeScript | `@anthropics/bunny-storage-sdk` |
| .NET | `BunnyCDN.Net.Storage` (NuGet) |
| PHP | `bunnycdn/storage` (Composer) |
| Java | `com.bunnycdn:storage` (Maven) |

### FTP Access
- Host: `storage.bunnycdn.com` (or regional)
- Username: storage zone name
- Password: storage zone password (or read-only password)
- Port: 21 (FTP) / 990 (FTPS)

---

## Stream API

Base URL: `https://video.bunnycdn.com`
Auth: `AccessKey: {Stream Library API Key}`

### Video Libraries (via Core API)
```
GET    https://api.bunny.net/videolibrary           — List libraries
GET    https://api.bunny.net/videolibrary/{id}       — Get library
POST   https://api.bunny.net/videolibrary            — Create library
POST   https://api.bunny.net/videolibrary/{id}       — Update library
DELETE https://api.bunny.net/videolibrary/{id}       — Delete library
```

### Videos
```
GET    /library/{libId}/videos                — List videos (?page=1&itemsPerPage=100&search=&collection=&orderBy=date)
GET    /library/{libId}/videos/{videoId}      — Get video details
POST   /library/{libId}/videos               — Create video entry
POST   /library/{libId}/videos/{videoId}     — Update video metadata
DELETE /library/{libId}/videos/{videoId}      — Delete video
PUT    /library/{libId}/videos/{videoId}      — Upload video (raw binary)
POST   /library/{libId}/videos/{videoId}/reencode   — Re-encode video
POST   /library/{libId}/videos/{videoId}/repackage  — Repackage video
```

### Create Video Body
```json
{
  "title": "My Video",
  "collectionId": "optional-collection-guid",
  "thumbnailTime": 5
}
```

### Upload via URL Fetch
```
POST /library/{libId}/videos/fetch
```
```json
{
  "url": "https://example.com/video.mp4",
  "headers": {"Authorization": "Bearer token"}
}
```

### TUS Resumable Upload
```
POST /tusupload with headers:
  Tus-Resumable: 1.0.0
  Upload-Length: {fileSize}
  Upload-Metadata: filetype {base64mime},title {base64title},collection {base64collectionId}
  AuthorizationSignature: {sha256(libraryId + apiKey + expirationTime + videoId)}
  AuthorizationExpire: {unixTimestamp}
  VideoId: {videoId}
  LibraryId: {libraryId}
```

### Collections
```
GET    /library/{libId}/collections               — List collections
GET    /library/{libId}/collections/{collId}      — Get collection
POST   /library/{libId}/collections               — Create {"name":"Collection Name"}
POST   /library/{libId}/collections/{collId}      — Update
DELETE /library/{libId}/collections/{collId}      — Delete
```

### Captions
```
POST   /library/{libId}/videos/{videoId}/captions/{srclang}  — Add caption (body: {"CaptionsFile":"base64srt"})
DELETE /library/{libId}/videos/{videoId}/captions/{srclang}  — Delete caption
```

### Video Statistics
```
GET /library/{libId}/statistics?dateFrom=2024-01-01&dateTo=2024-01-31&videoGuid={optional}
```

### Embedding
```html
<iframe src="https://iframe.mediadelivery.net/embed/{libraryId}/{videoId}"
  loading="lazy" style="border:none;width:100%;aspect-ratio:16/9"
  allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
  allowfullscreen></iframe>
```

### Direct Play URLs
- HLS: `https://vz-{token}.b-cdn.net/{videoId}/playlist.m3u8`
- Thumbnail: `https://vz-{token}.b-cdn.net/{videoId}/thumbnail.jpg`
- Preview: `https://vz-{token}.b-cdn.net/{videoId}/preview.webp`

### Webhooks
Configure webhook URL in library settings. Events:
- `VideoCreated`, `VideoUploaded`, `VideoProcessingStarted`
- `VideoEncoded`, `VideoFailed`, `VideoDeleted`
- `CaptionsCompleted`, `TranscriptionCompleted`

Payload:
```json
{"VideoLibraryId": 123, "VideoGuid": "guid", "Status": 4}
```
Status: 0=Created, 1=Uploaded, 2=Processing, 3=Transcoding, 4=Finished, 5=Error, 6=UploadFailed

### Token Authentication
```
Token = SHA256(securityKey + videoId + expirationTime)
URL: https://iframe.mediadelivery.net/embed/{libId}/{videoId}?token={token}&expires={expirationTime}
```

Optional params: `&token_countries=US,DE` (allow), `&token_countries_blocked=CN` (block), `&token_path=/`
