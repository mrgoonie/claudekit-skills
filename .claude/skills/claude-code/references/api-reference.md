# API Reference

API endpoints and programmatic access to Claude Code functionality.

## Admin API

### Usage Reports

**Get Claude Code Usage Report:**
```bash
GET /v1/admin/claude-code/usage
```

**Query parameters:**
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `user_id`: Filter by user
- `workspace_id`: Filter by workspace

**Response:**
```json
{
  "usage": [
    {
      "date": "2025-11-06",
      "user_id": "user-123",
      "requests": 150,
      "tokens": 45000,
      "cost": 12.50
    }
  ]
}
```

**Example:**
```bash
curl https://api.anthropic.com/v1/admin/claude-code/usage \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d start_date=2025-11-01 \
  -d end_date=2025-11-06
```

### Cost Reports

**Get Cost Report:**
```bash
GET /v1/admin/usage/cost
```

**Query parameters:**
- `start_date`: Start date
- `end_date`: End date
- `group_by`: `user` | `project` | `model`

**Response:**
```json
{
  "costs": [
    {
      "group": "user-123",
      "input_tokens": 100000,
      "output_tokens": 50000,
      "cost": 25.00
    }
  ],
  "total": 250.00
}
```

### User Management

**List Users:**
```bash
GET /v1/admin/users
```

**Get User:**
```bash
GET /v1/admin/users/{user_id}
```

**Update User:**
```bash
PATCH /v1/admin/users/{user_id}
```

**Remove User:**
```bash
DELETE /v1/admin/users/{user_id}
```

## Messages API

### Create Message

**Endpoint:**
```bash
POST /v1/messages
```

**Request:**
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 4096,
  "messages": [
    {
      "role": "user",
      "content": "Explain this code"
    }
  ]
}
```

**With Skills:**
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 4096,
  "skills": [
    {
      "type": "custom",
      "custom": {
        "name": "code-reviewer",
        "description": "Reviews code quality",
        "instructions": "Check for bugs, security issues..."
      }
    }
  ],
  "messages": [...]
}
```

**Response:**
```json
{
  "id": "msg_123",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "This code implements..."
    }
  ],
  "usage": {
    "input_tokens": 100,
    "output_tokens": 200
  }
}
```

### Stream Messages

**Streaming response:**
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 4096,
  "stream": true,
  "messages": [...]
}
```

**Server-sent events:**
```
event: message_start
data: {"type":"message_start","message":{...}}

event: content_block_delta
data: {"type":"content_block_delta","delta":{"text":"Hello"}}

event: message_stop
data: {"type":"message_stop"}
```

### Count Tokens

**Endpoint:**
```bash
POST /v1/messages/count_tokens
```

**Request:**
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "messages": [
    {
      "role": "user",
      "content": "Count these tokens"
    }
  ]
}
```

**Response:**
```json
{
  "input_tokens": 15
}
```

## Files API

### Upload File

**Endpoint:**
```bash
POST /v1/files
```

**Request (multipart/form-data):**
```bash
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -F file=@document.pdf \
  -F purpose=user_upload
```

**Response:**
```json
{
  "id": "file-123",
  "object": "file",
  "bytes": 12345,
  "created_at": 1699564800,
  "filename": "document.pdf",
  "purpose": "user_upload"
}
```

### List Files

**Endpoint:**
```bash
GET /v1/files
```

**Response:**
```json
{
  "data": [
    {
      "id": "file-123",
      "filename": "document.pdf",
      "bytes": 12345
    }
  ]
}
```

### Download File

**Endpoint:**
```bash
GET /v1/files/{file_id}/content
```

### Delete File

**Endpoint:**
```bash
DELETE /v1/files/{file_id}
```

## Models API

### List Models

**Endpoint:**
```bash
GET /v1/models
```

**Response:**
```json
{
  "data": [
    {
      "id": "claude-sonnet-4-5-20250929",
      "type": "model",
      "display_name": "Claude Sonnet 4.5"
    }
  ]
}
```

### Get Model

**Endpoint:**
```bash
GET /v1/models/{model_id}
```

**Response:**
```json
{
  "id": "claude-sonnet-4-5-20250929",
  "type": "model",
  "display_name": "Claude Sonnet 4.5",
  "created_at": 1699564800
}
```

## Skills API

### Create Skill

**Endpoint:**
```bash
POST /v1/skills
```

**Request:**
```json
{
  "name": "my-skill",
  "description": "Skill description",
  "instructions": "Detailed instructions...",
  "version": "1.0.0"
}
```

### List Skills

**Endpoint:**
```bash
GET /v1/skills
```

**Response:**
```json
{
  "data": [
    {
      "id": "skill-123",
      "name": "my-skill",
      "description": "Skill description"
    }
  ]
}
```

### Update Skill

**Endpoint:**
```bash
PATCH /v1/skills/{skill_id}
```

**Request:**
```json
{
  "description": "Updated description",
  "instructions": "Updated instructions..."
}
```

### Delete Skill

**Endpoint:**
```bash
DELETE /v1/skills/{skill_id}
```

## Client SDKs

### TypeScript/JavaScript

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' }
  ]
});

console.log(message.content);
```

### Python

```python
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content)
```

## Error Handling

### Error Response Format

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Invalid API key"
  }
}
```

### Error Types

**invalid_request_error**: Invalid request parameters
**authentication_error**: Invalid API key
**permission_error**: Insufficient permissions
**not_found_error**: Resource not found
**rate_limit_error**: Rate limit exceeded
**api_error**: Internal API error
**overloaded_error**: Server overloaded

### Retry Logic

```typescript
async function withRetry(fn: () => Promise<any>, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 529 && i < maxRetries - 1) {
        await new Promise(r => setTimeout(r, 1000 * (i + 1)));
        continue;
      }
      throw error;
    }
  }
}
```

## Rate Limits

### Headers

Response headers include rate limit info:
```
anthropic-ratelimit-requests-limit: 1000
anthropic-ratelimit-requests-remaining: 999
anthropic-ratelimit-requests-reset: 2025-11-06T12:00:00Z
anthropic-ratelimit-tokens-limit: 100000
anthropic-ratelimit-tokens-remaining: 99500
anthropic-ratelimit-tokens-reset: 2025-11-06T12:00:00Z
```

### Best Practices

- Monitor rate limit headers
- Implement exponential backoff
- Batch requests when possible
- Use caching to reduce requests

## Authentication

### API Key

Include API key in requests:
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Workspace Keys

For organization workspaces:
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $WORKSPACE_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

## See Also

- API documentation: https://docs.anthropic.com/api
- Client SDKs: https://docs.anthropic.com/api/client-sdks
- Rate limits: https://docs.anthropic.com/api/rate-limits
- Error handling: https://docs.anthropic.com/api/errors
