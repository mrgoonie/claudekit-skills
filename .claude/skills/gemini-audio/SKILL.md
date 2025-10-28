---
name: gemini-audio
description: Guide for implementing Google Gemini API audio capabilities - analyze audio with transcription, summarization, and understanding (up to 9.5 hours), plus generate speech with controllable TTS. Use when processing audio files, creating transcripts, analyzing speech/music/sounds, or generating natural speech from text.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Gemini Audio API Skill

Process audio with transcription, analysis, and understanding, plus generate natural speech using Google's Gemini API. Supports up to 9.5 hours of audio per request with multiple formats.

## When to Use This Skill

Use this skill when you need to:
- **Transcribe** audio files to text with timestamps
- **Summarize** audio content and extract key points
- **Analyze** speech, music, or environmental sounds
- **Generate speech** from text with controllable voice and style
- **Process** podcasts, interviews, meetings, or any audio content
- **Understand** non-speech audio (birdsong, sirens, music)

## Prerequisites

### API Key Setup

The skill automatically detects your `GEMINI_API_KEY` in this order:

1. **Process environment**: `export GEMINI_API_KEY="your-key"`
2. **Skill directory**: `.claude/skills/gemini-audio/.env`
3. **Project directory**: `./.env` (project root)

**Get your API key**: Visit [Google AI Studio](https://aistudio.google.com/apikey)

Create `.env` file with:
```bash
GEMINI_API_KEY=your_api_key_here
```

### Python Setup

Install required package:
```bash
pip install google-genai
```

## Quick Start

### Audio Analysis (Transcription, Summarization)

```python
from google import genai
import os

# API key auto-detected from environment
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Upload audio file
myfile = client.files.upload(file='podcast.mp3')

# Transcribe
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Generate a transcript of the speech.', myfile]
)
print(response.text)

# Summarize
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Summarize the key points in 5 bullets.', myfile]
)
print(response.text)
```

### Using Helper Scripts

```bash
# Transcribe audio
python .claude/skills/gemini-audio/scripts/transcribe.py audio.mp3

# Summarize audio
python .claude/skills/gemini-audio/scripts/analyze.py audio.mp3 \
  "Summarize key points"

# Analyze specific segment (timestamps in MM:SS format)
python .claude/skills/gemini-audio/scripts/analyze.py audio.mp3 \
  "What is discussed from 02:30 to 05:15?"

# Generate speech
python .claude/skills/gemini-audio/scripts/generate-speech.py \
  "Welcome to our podcast" \
  --output welcome.wav
```

## Audio Understanding Capabilities

### Supported Formats

| Format | MIME Type | Best Use |
|--------|-----------|----------|
| WAV | `audio/wav` | Uncompressed, highest quality |
| MP3 | `audio/mp3` | Compressed, widely compatible |
| AAC | `audio/aac` | Compressed, good quality |
| FLAC | `audio/flac` | Lossless compression |
| OGG Vorbis | `audio/ogg` | Open format |
| AIFF | `audio/aiff` | Apple format |

### Audio Specifications

- **Maximum length**: 9.5 hours per request
- **Multiple files**: Unlimited count, combined max 9.5 hours
- **Token rate**: 32 tokens/second (1 minute = 1,920 tokens)
- **Processing**: Auto-downsampled to 16 Kbps mono
- **File size limits**:
  - Inline: 20 MB max total request
  - File API: 2 GB per file, 20 GB project quota
  - Retention: 48 hours auto-delete

### Analysis Features

- **Transcription**: Full text with punctuation
- **Timestamps**: Reference segments (MM:SS format)
- **Multi-speaker**: Identify different speakers
- **Non-speech**: Analyze music, sounds, ambient audio
- **Languages**: Support for multiple languages

## Speech Generation (TTS)

### Available TTS Models

| Model | Quality | Speed | Cost/1M tokens |
|-------|---------|-------|----------------|
| `gemini-2.5-flash-native-audio-preview-09-2025` | High | Fast | $10 |
| `gemini-2.5-pro` TTS mode | Premium | Slower | $20 |

### Controllable Voice Options

- **Style**: Professional, casual, narrative, conversational
- **Pace**: Slow, normal, fast
- **Tone**: Friendly, serious, enthusiastic
- **Accent**: Natural language control

### TTS Example

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents='Generate audio: Welcome to today\'s episode, in a warm, friendly tone.'
)

# Save audio output
with open('output.wav', 'wb') as f:
    f.write(response.audio_data)
```

## Input Methods

### Method 1: File Upload (Recommended for >20MB)

```python
# Upload and reuse
myfile = client.files.upload(file='large-audio.mp3')

# Use file multiple times
response1 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Transcribe this', myfile]
)

response2 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Summarize this', myfile]
)
```

### Method 2: Inline Data (<20MB)

```python
from google.genai import types

with open('small-audio.mp3', 'rb') as f:
    audio_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Describe this audio',
        types.Part.from_bytes(data=audio_bytes, mime_type='audio/mp3')
    ]
)
```

## Common Use Cases

### Transcription
```bash
python scripts/transcribe.py meeting.mp3 --include-timestamps
```

### Summary with Key Points
```bash
python scripts/analyze.py interview.wav "Extract main topics and key quotes"
```

### Speaker Identification
```bash
python scripts/analyze.py discussion.mp3 "Identify speakers and extract dialogue"
```

### Segment Analysis
```bash
python scripts/analyze.py podcast.mp3 "Summarize content from 10:30 to 15:45"
```

### Non-Speech Analysis
```bash
python scripts/analyze.py ambient.wav "Identify all sounds: voices, music, ambient"
```

## Best Practices

### File Management
- Use File API for files >20MB or repeated usage
- Files auto-delete after 48 hours
- Manage quota (20 GB project limit)

### Prompt Engineering
- Be specific: "Transcribe from 02:30 to 03:29"
- Use timestamps for segment analysis (MM:SS format)
- Combine tasks: "Transcribe and summarize"
- Provide context: "This is a medical interview"

### Cost Optimization
- Use `gemini-2.5-flash` ($1/1M tokens) for most tasks
- Upgrade to `gemini-2.5-pro` ($3/1M tokens) for complex analysis
- Check token count: 1 min audio = 1,920 tokens

### Error Handling
- Validate file format and size before upload
- Implement exponential backoff for rate limits
- Handle 48-hour file expiration

## Token Costs & Pricing

**Audio Input** (32 tokens/second):
- 1 minute = 1,920 tokens
- 1 hour = 115,200 tokens
- 9.5 hours = 1,094,400 tokens

**Model Pricing**:
- Gemini 2.5 Flash: $1.00/1M input, $0.10/1M output
- Gemini 2.5 Pro: $3.00/1M input, $12.00/1M output
- Gemini 1.5 Flash: $0.70/1M input, $0.175/1M output

**TTS Pricing**:
- Flash TTS: $10/1M tokens
- Pro TTS: $20/1M tokens

## Reference Documentation

For detailed information, see:
- `references/api-reference.md` - Complete API specifications
- `references/code-examples.md` - Comprehensive code examples
- `references/tts-guide.md` - Text-to-speech implementation guide
- `references/best-practices.md` - Advanced optimization strategies

## Scripts Overview

All scripts support 3-step API key detection:

- **transcribe.py**: Generate transcripts with optional timestamps
- **analyze.py**: General audio analysis with custom prompts
- **generate-speech.py**: Text-to-speech generation
- **manage-files.py**: Upload, list, and delete audio files

Run any script with `--help` for detailed usage.

## Resources

- [Audio Understanding Docs](https://ai.google.dev/gemini-api/docs/audio)
- [Speech Generation Docs](https://ai.google.dev/gemini-api/docs/speech-generation)
- [API Reference](https://ai.google.dev/api/generate-content)
- [Get API Key](https://aistudio.google.com/apikey)
