# Gemini Video Understanding Skill

A comprehensive Claude Code skill for analyzing videos using Google's Gemini API.

## Overview

This skill enables AI-powered video analysis with capabilities including:
- Video summarization and content description
- Question answering about video content
- Audio transcription with visual descriptions
- Timestamp-based queries (MM:SS format)
- Video clipping (specific time ranges)
- Multiple video comparison (Gemini 2.5+)
- YouTube video processing
- Custom frame rate sampling

## Features

✅ **Three Video Input Methods:**
- Local files (Files API for >20MB, inline for <20MB)
- YouTube URLs (preview feature)
- Multiple videos (up to 10 with Gemini 2.5+)

✅ **Advanced Processing:**
- Video clipping with start/end offsets
- Custom FPS sampling (default: 1 FPS)
- Context windows up to 2M tokens (~6 hours of video)

✅ **9 Supported Video Formats:**
MP4, MPEG, MOV, AVI, FLV, MPG, WebM, WMV, 3GPP

✅ **Multiple Models:**
- Gemini 2.5 Series (Pro, Flash, Preview)
- Gemini 2.0 Series (Flash, Flash-Lite)

✅ **Flexible API Key Management:**
Checks in order: Process env → Skill directory → Project root

## Quick Start

1. **Install:** `pip install google-genai`
2. **Configure:** `export GEMINI_API_KEY="your-key"`
3. **Verify:** `python scripts/check_api_key.py`
4. **Analyze:** `python scripts/analyze_video.py --video-path video.mp4 --prompt "Summarize"`

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

## Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide
- **[EXAMPLES.md](EXAMPLES.md)** - Comprehensive examples and use cases

## Directory Structure

```
gemini-video-understanding/
├── SKILL.md              # Main skill documentation
├── README.md             # This file
├── QUICKSTART.md         # Quick start guide
├── EXAMPLES.md           # Detailed examples
├── requirements.txt      # Python dependencies
├── .env.example          # API key template
└── scripts/
    ├── analyze_video.py  # Main video analysis script
    └── check_api_key.py  # API key verification tool
```

## Common Use Cases

| Use Case | Command |
|----------|---------|
| Video Summary | `--prompt "Summarize this video in 3 points"` |
| Transcription | `--prompt "Transcribe with timestamps and visual descriptions"` |
| YouTube Analysis | `--youtube-url "URL" --prompt "What are the main topics?"` |
| Time Range | `--start-offset "1m30s" --end-offset "3m"` |
| Multi-Video | `--video-paths vid1.mp4 vid2.mp4 --prompt "Compare"` |
| High Quality | `--model "gemini-2.5-pro"` |

## API Key Configuration

The skill automatically checks for `GEMINI_API_KEY` in this order:

1. **Process Environment** - `$GEMINI_API_KEY`
2. **Skill Directory** - `.claude/skills/gemini-video-understanding/.env`
3. **Project Root** - `.env` file

Get your API key at: https://aistudio.google.com/apikey

## Rate Limits & Pricing

**Free Tier:**
- 10-15 requests per minute
- 1-4M tokens per minute
- 1,500 requests per day
- YouTube: 8 hours per day

**Token Usage:**
- Default: ~300 tokens/second of video
- Low-res: ~100 tokens/second of video

See full pricing: https://ai.google.dev/pricing

## Support

- **API Documentation:** https://ai.google.dev/gemini-api/docs/video-understanding
- **Files API:** https://ai.google.dev/gemini-api/docs/vision#uploading-files
- **Rate Limits:** https://ai.google.dev/gemini-api/docs/rate-limits
- **Issue Tracker:** [Report issues on GitHub]

## License

MIT License - See skill metadata for details.

## Version

1.0.0 (2025-10-26)
