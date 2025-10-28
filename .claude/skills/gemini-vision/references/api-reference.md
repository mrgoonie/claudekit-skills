# Gemini Vision API Reference

Complete API reference for Google's Gemini Vision API.

## Base URL

```
https://generativelanguage.googleapis.com/v1beta
```

## Authentication

All requests require an API key passed as a query parameter or header:

**Query Parameter:**
```
?key=YOUR_API_KEY
```

**Header:**
```
Authorization: Bearer YOUR_API_KEY
```

## API Methods

### 1. Generate Content

Generate a response from the model with image input.

**Endpoint:**
```
POST /models/{model}:generateContent
```

**Models:**
- `gemini-2.5-pro` - Most capable, segmentation + detection
- `gemini-2.5-flash` - Fast and efficient, segmentation + detection
- `gemini-2.5-flash-lite` - Lightweight, segmentation + detection
- `gemini-2.0-flash` - Object detection support
- `gemini-1.5-pro` - Previous generation, high quality
- `gemini-1.5-flash` - Previous generation, fast

**Request Body:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "What's in this image?"
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
            "data": "base64_encoded_image_data"
          }
        }
      ]
    }
  ]
}
```

**Response:**
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "The image shows..."
          }
        ]
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 258,
    "candidatesTokenCount": 45,
    "totalTokenCount": 303
  }
}
```

**Python Example:**
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

with open('image.jpg', 'rb') as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg'
        ),
        'What is in this image?'
    ]
)

print(response.text)
```

### 2. Upload File

Upload a file for reuse across multiple requests.

**Endpoint:**
```
POST /upload/files
```

**Request (Multipart):**
```
Content-Type: multipart/form-data

file: <binary file data>
```

**Response:**
```json
{
  "file": {
    "name": "files/abc123xyz",
    "displayName": "image.jpg",
    "mimeType": "image/jpeg",
    "sizeBytes": "524288",
    "createTime": "2025-10-26T10:30:00Z",
    "updateTime": "2025-10-26T10:30:00Z",
    "expirationTime": "2025-10-28T10:30:00Z",
    "sha256Hash": "...",
    "uri": "https://generativelanguage.googleapis.com/v1beta/files/abc123xyz",
    "state": "ACTIVE"
  }
}
```

**Python Example:**
```python
client = genai.Client(api_key="YOUR_API_KEY")

uploaded_file = client.files.upload(file="image.jpg")

print(f"Uploaded: {uploaded_file.name}")
print(f"State: {uploaded_file.state}")
```

### 3. Get File

Retrieve metadata for an uploaded file.

**Endpoint:**
```
GET /files/{file_id}
```

**Response:**
```json
{
  "name": "files/abc123xyz",
  "displayName": "image.jpg",
  "mimeType": "image/jpeg",
  "sizeBytes": "524288",
  "createTime": "2025-10-26T10:30:00Z",
  "updateTime": "2025-10-26T10:30:00Z",
  "expirationTime": "2025-10-28T10:30:00Z",
  "sha256Hash": "...",
  "uri": "https://generativelanguage.googleapis.com/v1beta/files/abc123xyz",
  "state": "ACTIVE"
}
```

**Python Example:**
```python
file_info = client.files.get(name="files/abc123xyz")
print(f"File: {file_info.display_name}")
print(f"Size: {file_info.size_bytes} bytes")
```

### 4. List Files

List all uploaded files.

**Endpoint:**
```
GET /files
```

**Query Parameters:**
- `pageSize` (optional): Maximum number of files to return (default: 10)
- `pageToken` (optional): Token for pagination

**Response:**
```json
{
  "files": [
    {
      "name": "files/abc123xyz",
      "displayName": "image.jpg",
      "mimeType": "image/jpeg",
      ...
    }
  ],
  "nextPageToken": "..."
}
```

**Python Example:**
```python
files = client.files.list()
for file in files:
    print(f"{file.display_name}: {file.name}")
```

### 5. Delete File

Delete an uploaded file.

**Endpoint:**
```
DELETE /files/{file_id}
```

**Response:**
```json
{}
```

**Python Example:**
```python
client.files.delete(name="files/abc123xyz")
print("File deleted")
```

## Request Parameters

### Content Part Types

**Text Part:**
```json
{
  "text": "Your prompt text"
}
```

**Inline Image Data:**
```json
{
  "inline_data": {
    "mime_type": "image/jpeg",
    "data": "base64_encoded_data"
  }
}
```

**File Reference:**
```json
{
  "file_data": {
    "mime_type": "image/jpeg",
    "file_uri": "https://generativelanguage.googleapis.com/v1beta/files/abc123"
  }
}
```

### Supported MIME Types

- `image/png` - PNG images
- `image/jpeg` - JPEG images
- `image/webp` - WebP images
- `image/heic` - HEIC images (Apple)
- `image/heif` - HEIF images
- `application/pdf` - PDF documents

## Rate Limits

Limits vary by billing tier:

| Tier | RPM | TPM | RPD |
|------|-----|-----|-----|
| Free | 15 | 1M | 1,500 |
| Tier 1 ($0+) | 1,000 | 4M | - |
| Tier 2 ($250+) | 1,000 | 4M | - |
| Tier 3 ($1,000+) | 2,000 | 4M | - |

**RPM**: Requests per minute
**TPM**: Tokens per minute
**RPD**: Requests per day

## Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 400 | Invalid request | Check request format, file size, MIME type |
| 401 | Unauthorized | Verify API key is valid |
| 403 | Forbidden | Check API key restrictions |
| 404 | Not found | Verify file ID or model name |
| 429 | Rate limit exceeded | Implement retry with backoff |
| 500 | Server error | Retry request |

## Token Calculation

Images consume tokens based on their dimensions:

**Small Images (≤384px both dimensions):**
- Cost: 258 tokens

**Large Images:**
- Images are tiled into 768×768 pixel chunks
- Each chunk costs 258 tokens

**Formula:**
```
crop_unit = floor(min(width, height) / 1.5)
tiles_x = width / crop_unit
tiles_y = height / crop_unit
total_tiles = tiles_x × tiles_y
total_tokens = total_tiles × 258
```

**Examples:**
- 960×540 image: 6 tiles = 1,548 tokens
- 1920×1080 image: 6 tiles = 1,548 tokens
- 3840×2160 image: 25 tiles = 6,450 tokens

## Size Limits

- **Inline data**: 20MB total request size (including prompts)
- **File API**: For files larger than 20MB
- **Max images per request**: 3,600 files
- **PDF pages**: Up to 1,000 pages
- **File retention**: 48 hours after upload

## Best Practices

### API Key Security
- Use environment variables
- Never commit keys to version control
- Add API key restrictions in Google Cloud Console
- Rotate keys regularly

### File Management
- Use File API for files >20MB
- Use File API for repeated usage (saves tokens)
- Delete files after use to free quota
- Files auto-delete after 48 hours

### Performance Optimization
- Choose appropriate model (Flash vs Pro)
- Resize images to reduce token costs
- Batch requests when possible
- Implement caching for repeated queries

### Error Handling
- Implement exponential backoff for rate limits
- Validate inputs before API calls
- Handle network errors gracefully
- Log errors for debugging

## Additional Resources

- **Official Documentation**: https://ai.google.dev/gemini-api/docs
- **API Reference**: https://ai.google.dev/gemini-api/docs/reference
- **Google AI Studio**: https://aistudio.google.com
- **Community Forum**: https://discuss.ai.google.dev
