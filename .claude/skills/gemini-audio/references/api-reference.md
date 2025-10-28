# Gemini Audio API Reference

Complete API reference for audio understanding and speech generation with Google Gemini API.

## Table of Contents

- [Audio Understanding API](#audio-understanding-api)
- [Speech Generation API](#speech-generation-api)
- [Files API](#files-api)
- [Common Parameters](#common-parameters)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)

## Audio Understanding API

### Generate Content with Audio

**Endpoint**: `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`

**Authentication**: `x-goog-api-key: YOUR_API_KEY`

#### Request Format (File API)

```json
{
  "contents": [{
    "parts": [
      {"text": "Transcribe this audio"},
      {
        "file_data": {
          "mime_type": "audio/mp3",
          "file_uri": "https://generativelanguage.googleapis.com/v1beta/files/abc123"
        }
      }
    ]
  }],
  "generationConfig": {
    "temperature": 0.4,
    "topP": 0.95,
    "maxOutputTokens": 8192
  }
}
```

#### Request Format (Inline Data)

```json
{
  "contents": [{
    "parts": [
      {"text": "Describe this audio"},
      {
        "inline_data": {
          "mime_type": "audio/mp3",
          "data": "base64_encoded_audio_data"
        }
      }
    ]
  }]
}
```

#### Python SDK

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

# Method 1: Upload file
audio_file = client.files.upload(file="audio.mp3")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Transcribe this audio', audio_file]
)

# Method 2: Inline data
with open('audio.mp3', 'rb') as f:
    audio_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Describe this audio',
        types.Part.from_bytes(data=audio_bytes, mime_type='audio/mp3')
    ]
)
```

#### JavaScript SDK

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({ apiKey: "YOUR_API_KEY" });

// Method 1: Upload file
const myfile = await ai.files.upload({
  file: "audio.mp3",
  config: { mimeType: "audio/mp3" }
});

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: [
    { text: "Transcribe this audio" },
    { fileData: { fileUri: myfile.uri, mimeType: myfile.mimeType } }
  ]
});

// Method 2: Inline data
const base64Audio = fs.readFileSync("audio.mp3", { encoding: "base64" });

const response2 = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: [
    { text: "Describe this audio" },
    { inlineData: { mimeType: "audio/mp3", data: base64Audio } }
  ]
});
```

### Supported MIME Types

| Format | MIME Type | Extension |
|--------|-----------|-----------|
| WAV | `audio/wav` | `.wav` |
| MP3 | `audio/mp3` | `.mp3` |
| AAC | `audio/aac` | `.aac`, `.m4a` |
| FLAC | `audio/flac` | `.flac` |
| OGG Vorbis | `audio/ogg` | `.ogg` |
| AIFF | `audio/aiff` | `.aiff`, `.aif` |

### Audio Constraints

- **Maximum duration**: 9.5 hours (34,200 seconds) per request
- **Token rate**: 32 tokens per second
- **Multiple files**: Combined duration must not exceed 9.5 hours
- **File size**: 2 GB max per file (Files API), 20 MB max total (inline)
- **Processing**: Auto-downsampled to 16 Kbps mono

## Speech Generation API

### Text-to-Speech with Native Audio Model

**Model**: `gemini-2.5-flash-native-audio-preview-09-2025`

#### Python SDK

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents='Generate audio: Welcome to our podcast, in a warm, friendly tone.',
    config=types.GenerateContentConfig(
        response_modalities=['audio']
    )
)

# Extract audio data
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('output.wav', 'wb') as f:
            f.write(part.inline_data.data)
```

#### JavaScript SDK

```javascript
const ai = new GoogleGenAI({ apiKey: "YOUR_API_KEY" });

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-native-audio-preview-09-2025",
  contents: [
    { text: "Generate audio: Welcome to our podcast, in a warm, friendly tone." }
  ],
  generationConfig: {
    responseModalities: ['audio']
  }
});

// Extract and save audio
const audioPart = response.candidates[0].content.parts[0];
if (audioPart.inlineData) {
  const buffer = Buffer.from(audioPart.inlineData.data, 'base64');
  fs.writeFileSync('output.wav', buffer);
}
```

### Voice Control Parameters

Control voice characteristics through natural language in the prompt:

```python
# Style examples
"Generate audio: [text], in a professional style"
"Generate audio: [text], casually and conversationally"
"Generate audio: [text], as a narrative storytelling"

# Pace examples
"Generate audio: [text], speaking slowly and clearly"
"Generate audio: [text], at a normal conversational pace"
"Generate audio: [text], quickly and energetically"

# Tone examples
"Generate audio: [text], with a friendly and warm tone"
"Generate audio: [text], seriously and authoritatively"
"Generate audio: [text], enthusiastically and upbeat"

# Combined
"Generate audio: [text], in a professional style, at a normal pace, with a friendly tone"
```

## Files API

### Upload File

**Endpoint**: `POST https://generativelanguage.googleapis.com/upload/v1beta/files`

**Method**: Resumable upload protocol

#### Python SDK

```python
client = genai.Client(api_key="YOUR_API_KEY")

uploaded_file = client.files.upload(
    file="audio.mp3",
    display_name="My Audio File"  # Optional
)

print(f"URI: {uploaded_file.uri}")
print(f"Name: {uploaded_file.name}")
print(f"Size: {uploaded_file.size_bytes}")
print(f"MIME: {uploaded_file.mime_type}")
```

#### JavaScript SDK

```javascript
const ai = new GoogleGenAI({ apiKey: "YOUR_API_KEY" });

const uploadedFile = await ai.files.upload({
  file: "audio.mp3",
  config: {
    displayName: "My Audio File"  // Optional
  }
});

console.log("URI:", uploadedFile.uri);
console.log("Name:", uploadedFile.name);
```

### List Files

```python
# Python
files = list(client.files.list())
for file in files:
    print(f"{file.name}: {file.display_name}")
```

```javascript
// JavaScript
const files = await ai.files.list();
for await (const file of files) {
  console.log(`${file.name}: ${file.displayName}`);
}
```

### Get File Metadata

```python
# Python
file = client.files.get(name="files/abc123")
print(f"State: {file.state}")
print(f"Created: {file.create_time}")
```

```javascript
// JavaScript
const file = await ai.files.get("files/abc123");
console.log("State:", file.state);
```

### Delete File

```python
# Python
client.files.delete(name="files/abc123")
```

```javascript
// JavaScript
await ai.files.delete("files/abc123");
```

## Common Parameters

### Generation Config

```python
from google.genai import types

config = types.GenerateContentConfig(
    temperature=0.4,          # Creativity (0.0-2.0)
    top_p=0.95,              # Nucleus sampling
    top_k=40,                # Top-k sampling
    max_output_tokens=8192,  # Max response length
    response_modalities=['text'],  # Or ['audio'] for TTS
    stop_sequences=["END"]   # Stop generation at these
)
```

### Safety Settings

```python
config = types.GenerateContentConfig(
    safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )
    ]
)
```

## Response Formats

### Audio Understanding Response

```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "text": "This is a transcript of the audio..."
      }],
      "role": "model"
    },
    "finishReason": "STOP",
    "safetyRatings": [...]
  }],
  "usageMetadata": {
    "promptTokenCount": 1920,
    "candidatesTokenCount": 150,
    "totalTokenCount": 2070
  }
}
```

### Speech Generation Response

```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inlineData": {
          "mimeType": "audio/wav",
          "data": "base64_encoded_audio..."
        }
      }],
      "role": "model"
    }
  }]
}
```

## Error Handling

### Common HTTP Status Codes

| Code | Error | Meaning |
|------|-------|---------|
| 400 | INVALID_ARGUMENT | Invalid request format or parameters |
| 401 | UNAUTHENTICATED | Invalid or missing API key |
| 403 | PERMISSION_DENIED | API key doesn't have permission |
| 404 | NOT_FOUND | File or resource not found |
| 429 | RESOURCE_EXHAUSTED | Rate limit exceeded |
| 500 | INTERNAL | Internal server error |
| 503 | UNAVAILABLE | Service temporarily unavailable |

### Error Response Format

```json
{
  "error": {
    "code": 400,
    "message": "Invalid file format",
    "status": "INVALID_ARGUMENT",
    "details": [...]
  }
}
```

### Python Error Handling

```python
from google.api_core import exceptions

try:
    response = client.models.generate_content(...)
except exceptions.InvalidArgument as e:
    print(f"Invalid request: {e}")
except exceptions.ResourceExhausted as e:
    print(f"Rate limit exceeded: {e}")
except exceptions.NotFound as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### JavaScript Error Handling

```javascript
try {
  const response = await ai.models.generateContent(...);
} catch (error) {
  if (error.status === 429) {
    console.error("Rate limit exceeded");
  } else if (error.status === 400) {
    console.error("Invalid request:", error.message);
  } else {
    console.error("Error:", error);
  }
}
```

## Rate Limits

Rate limits vary by tier and model. Check current limits:

**Python**:
```python
# Implement exponential backoff
import time

max_retries = 5
for attempt in range(max_retries):
    try:
        response = client.models.generate_content(...)
        break
    except exceptions.ResourceExhausted:
        if attempt < max_retries - 1:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
        else:
            raise
```

## Token Counting

```python
# Python
response = client.models.count_tokens(
    model='gemini-2.5-flash',
    contents=[audio_file]
)
print(f"Total tokens: {response.total_tokens}")
```

```javascript
// JavaScript
const countResponse = await ai.models.countTokens({
  model: "gemini-2.5-flash",
  contents: [{ fileData: { fileUri: myfile.uri } }]
});
console.log("Total tokens:", countResponse.totalTokens);
```

## Additional Resources

- [Official API Reference](https://ai.google.dev/api/generate-content)
- [Audio Understanding Docs](https://ai.google.dev/gemini-api/docs/audio)
- [Speech Generation Docs](https://ai.google.dev/gemini-api/docs/speech-generation)
- [Files API Docs](https://ai.google.dev/gemini-api/docs/files)
