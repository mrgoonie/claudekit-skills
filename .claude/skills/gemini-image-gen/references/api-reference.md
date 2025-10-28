# Gemini Image Generation API Reference

Complete technical reference for the Gemini 2.5 Flash Image model API.

## Model Information

**Model Name**: `gemini-2.5-flash-image`

**Version**: Latest update October 2025
**Knowledge Cutoff**: June 2025

### Capabilities

| Feature | Support |
|---------|---------|
| Image generation | ✓ |
| Structured outputs | ✓ |
| Batch API | ✓ |
| Caching | ✓ |
| Audio generation | ✗ |
| Code execution | ✗ |
| Function calling | ✗ |
| Thinking mode | ✗ |
| Live API | ✗ |
| Search grounding | ✗ |

### Token Limits

- **Input tokens**: 65,536
- **Output tokens**: 32,768
- **Approximate conversion**: ~4 characters per token, 100 tokens ≈ 60-80 words

## API Endpoint

**POST** `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent`

### Authentication

Include API key as header:
```bash
-H "x-goog-api-key: $GEMINI_API_KEY"
```

Or as query parameter:
```bash
?key=$GEMINI_API_KEY
```

## Request Structure

### Python SDK

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="your-api-key")

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='Your prompt here',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='16:9',
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            )
        ]
    )
)
```

### REST API

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Your prompt here"
      }]
    }],
    "generationConfig": {
      "response_modalities": ["IMAGE"],
      "aspect_ratio": "16:9"
    }
  }'
```

## Configuration Parameters

### GenerateContentConfig

**response_modalities** (List[str])
- `['image']` - Generate only images
- `['text']` - Generate only text
- `['image', 'text']` - Generate both images and text descriptions

**aspect_ratio** (str)
- `'1:1'` - Square (1024×1024) - Default
- `'16:9'` - Landscape (1344×768)
- `'9:16'` - Portrait (768×1344)
- `'4:3'` - Traditional landscape (1152×896)
- `'3:4'` - Traditional portrait (896×1152)

**safety_settings** (List[SafetySetting])
- Configure content filtering (see safety-settings.md)

**system_instruction** (str, optional)
- Developer-defined system instructions
- Currently text-only

**cached_content** (str, optional)
- Reference to previously cached content

### Token Costs by Aspect Ratio

All aspect ratios cost the same:

| Aspect Ratio | Resolution | Input Tokens |
|--------------|-----------|--------------|
| 1:1 | 1024×1024 | 1290 |
| 16:9 | 1344×768 | 1290 |
| 9:16 | 768×1344 | 1290 |
| 4:3 | 1152×896 | 1290 |
| 3:4 | 896×1152 | 1290 |

## Content Input Formats

### Text-Only Prompts

```python
contents='A serene mountain landscape at sunset'
```

### Text with Images

```python
import PIL.Image

img = PIL.Image.open('input.png')
contents=[
    'Add a red balloon to this image',
    img
]
```

### Multiple Images

```python
img1 = PIL.Image.open('image1.png')
img2 = PIL.Image.open('image2.png')

contents=[
    'Combine these images into a cohesive scene',
    img1,
    img2
]
```

**Note**: Maximum 3 input images recommended for optimal results.

### Image Input Formats

**Supported formats**:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

**Input methods**:
1. **PIL.Image objects** (Python SDK)
2. **Base64-encoded data** with MIME type
3. **File URI** after uploading via Files API

## Response Structure

### GenerateContentResponse

```python
response = client.models.generate_content(...)

# Access response
for candidate in response.candidates:
    for part in candidate.content.parts:
        # Image data
        if hasattr(part, 'inline_data') and part.inline_data:
            image_bytes = part.inline_data.data
            mime_type = part.inline_data.mime_type

        # Text data
        if hasattr(part, 'text'):
            text = part.text

# Check finish reason
finish_reason = response.candidates[0].finish_reason
# Values: FINISH_REASON_UNSPECIFIED, STOP, MAX_TOKENS, SAFETY, RECITATION, OTHER

# Safety feedback
if response.prompt_feedback:
    block_reason = response.prompt_feedback.block_reason
    safety_ratings = response.prompt_feedback.safety_ratings

# Usage metadata
usage = response.usage_metadata
print(f"Input tokens: {usage.prompt_token_count}")
print(f"Output tokens: {usage.candidates_token_count}")
print(f"Total tokens: {usage.total_token_count}")
```

### Finish Reasons

| Reason | Description |
|--------|-------------|
| STOP | Natural completion |
| MAX_TOKENS | Reached token limit |
| SAFETY | Safety filter triggered |
| RECITATION | Content repetition detected |
| OTHER | Other reason |
| FINISH_REASON_UNSPECIFIED | Unknown reason |

## Error Handling

### Common Errors

**API Key Not Found**
```
Error: API key not valid
```
Solution: Verify API key is set correctly

**Invalid Aspect Ratio**
```
Error: Invalid aspect_ratio value
```
Solution: Use one of: 1:1, 16:9, 9:16, 4:3, 3:4

**Token Limit Exceeded**
```
Error: Request exceeds maximum token limit
```
Solution: Reduce prompt length or simplify request

**Safety Filter Blocking**
```
finish_reason: SAFETY
```
Solution: Check `safety_ratings` and adjust prompt or safety settings

### Error Response Example

```python
try:
    response = client.models.generate_content(...)
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

## Rate Limits

Refer to [Google AI pricing documentation](https://ai.google.dev/pricing) for current rate limits and quotas.

**Best practices**:
- Implement exponential backoff for retries
- Cache responses when appropriate
- Use batch API for multiple requests

## Streaming Alternative

Use streaming for real-time response generation:

```python
response_stream = client.models.generate_content_stream(
    model='gemini-2.5-flash-image',
    contents='Your prompt',
    config=config
)

for chunk in response_stream:
    # Process each chunk as it arrives
    for part in chunk.candidates[0].content.parts:
        if hasattr(part, 'text'):
            print(part.text, end='')
```

**Note**: Streaming is more useful for text generation; images are typically received complete.

## Additional Features

### Caching

Cache frequently used content to reduce costs:

```python
# Create cached content
cached = client.caches.create(
    model='gemini-2.5-flash-image',
    contents='Reusable context or instructions'
)

# Use cached content
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='New prompt',
    config=types.GenerateContentConfig(
        cached_content=cached.name
    )
)
```

### Batch API

Process multiple requests efficiently:

```python
# Submit batch job
batch_job = client.batches.create(
    model='gemini-2.5-flash-image',
    requests=[
        {'contents': 'Prompt 1'},
        {'contents': 'Prompt 2'},
        {'contents': 'Prompt 3'}
    ]
)

# Check status
status = client.batches.get(batch_job.name)

# Get results when complete
if status.state == 'SUCCEEDED':
    results = client.batches.get_results(batch_job.name)
```

## SynthID Watermarking

All generated images include SynthID watermarking automatically. This is:
- **Invisible** to human perception
- **Robust** to common modifications
- **Detectable** via SynthID verification tools

No configuration required - watermarking is always applied.

## Language Support

Optimal performance in:
- English (primary)
- Spanish (Mexico)
- Japanese
- Mandarin (Simplified)
- Hindi

Other languages may work but with reduced quality.

## Regional Restrictions

**Child image uploads** are restricted in:
- European Economic Area (EEA)
- Switzerland (CH)
- United Kingdom (UK)

The API will reject requests containing images of children from these regions.

## Resources

- [Official API Documentation](https://ai.google.dev/api/generate-content)
- [Python SDK Reference](https://ai.google.dev/gemini-api/docs/sdks)
- [Pricing Information](https://ai.google.dev/pricing)
- [Get API Key](https://aistudio.google.com/apikey)
