---
name: gemini-video-understanding
description: Analyze videos using Google's Gemini API - describe content, answer questions, transcribe audio with visual descriptions, reference timestamps, clip videos, and process YouTube URLs. Supports 9 video formats, multiple models (Gemini 2.5/2.0), and context windows up to 2M tokens (6 hours of video).
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
metadata:
  version: "1.0.0"
  author: ClaudeKit
  api-provider: Google Gemini
  requires-api-key: GEMINI_API_KEY
---

# Gemini Video Understanding Skill

This skill enables comprehensive video analysis using Google's Gemini API, including video summarization, question answering, transcription, timestamp references, and more.

## Capabilities

- **Video Summarization**: Create concise summaries of video content
- **Question Answering**: Answer specific questions about video content
- **Transcription**: Transcribe audio with visual descriptions and timestamps
- **Timestamp References**: Query specific moments in videos (MM:SS format)
- **Video Clipping**: Process specific segments using start/end offsets
- **Multiple Videos**: Compare and analyze up to 10 videos (Gemini 2.5+)
- **YouTube Support**: Analyze YouTube videos directly (preview feature)
- **Custom Frame Rate**: Adjust FPS sampling for different video types

## Supported Formats

- MP4, MPEG, MOV, AVI, FLV, MPG, WebM, WMV, 3GPP

## Models Available

**Gemini 2.5 Series:**
- `gemini-2.5-pro` - Best quality, 1M context
- `gemini-2.5-flash` - Balanced quality/speed, 1M context
- `gemini-2.5-flash-preview-09-2025` - Preview features, 1M context

**Gemini 2.0 Series:**
- `gemini-2.0-flash` - Fast processing
- `gemini-2.0-flash-lite` - Lightweight option

**Context Windows:**
- 2M token models: ~2 hours (default) or ~6 hours (low-res)
- 1M token models: ~1 hour (default) or ~3 hours (low-res)

## API Key Configuration

The skill checks for `GEMINI_API_KEY` in this order:
1. **Process environment**: `process.env.GEMINI_API_KEY` or `$GEMINI_API_KEY`
2. **Skill directory**: `.claude/skills/gemini-video-understanding/.env`
3. **Project root**: `.env` file in project root

To set up:

```bash
# Option 1: Environment variable (recommended)
export GEMINI_API_KEY="your-api-key-here"

# Option 2: Skill directory .env file
echo "GEMINI_API_KEY=your-api-key-here" > .claude/skills/gemini-video-understanding/.env

# Option 3: Project root .env file
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

Get your API key at: https://aistudio.google.com/apikey

## Usage Instructions

### When to Use This Skill

Use this skill when the user asks to:
- Analyze, summarize, or describe video content
- Answer questions about videos
- Transcribe video audio with visual context
- Extract information from specific timestamps
- Compare multiple videos
- Process YouTube video content
- Create quizzes or educational content from videos

### Basic Video Analysis

**For video files:**
```python
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/video.mp4" \
  --prompt "Summarize this video in 3 key points"
```

**For YouTube URLs:**
```python
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --prompt "What are the main topics discussed?"
```

### Advanced Features

**Video Clipping (specific time range):**
```python
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/video.mp4" \
  --prompt "Summarize this segment" \
  --start-offset "40s" \
  --end-offset "80s"
```

**Custom Frame Rate:**
```python
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/video.mp4" \
  --prompt "Analyze the rapid movements" \
  --fps 5
```

**Transcription with Timestamps:**
```python
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/video.mp4" \
  --prompt "Transcribe the audio with timestamps and visual descriptions"
```

**Multiple Videos (Gemini 2.5+ only):**
```python
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-paths "/path/video1.mp4" "/path/video2.mp4" \
  --prompt "Compare these two videos and highlight the differences"
```

**Model Selection:**
```python
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/video.mp4" \
  --prompt "Detailed analysis" \
  --model "gemini-2.5-pro"
```

### Script Parameters

```
Required (one of):
  --video-path PATH           Path to local video file
  --youtube-url URL           YouTube video URL
  --video-paths PATH [PATH..] Multiple video paths (Gemini 2.5+)

Required:
  --prompt TEXT              Analysis prompt/question

Optional:
  --model NAME               Model to use (default: gemini-2.5-flash)
  --start-offset TIME        Video clip start (e.g., "40s", "1m30s")
  --end-offset TIME          Video clip end (e.g., "80s", "2m")
  --fps NUMBER               Frame sampling rate (default: 1)
  --output-file PATH         Save response to file
  --verbose                  Show detailed processing info
```

## Common Use Cases

### 1. Video Summarization
```
Prompt: "Summarize this video in 3 key points with timestamps"
```

### 2. Educational Content
```
Prompt: "Create a quiz with 5 questions and answer key based on this video"
```

### 3. Timestamp-Specific Questions
```
Prompt: "What happens at 01:15 and how does it relate to the topic at 02:30?"
```

### 4. Transcription
```
Prompt: "Transcribe the audio from this video with timestamps for salient events and visual descriptions"
```

### 5. Content Comparison
```
Prompt: "Compare these two product demo videos. Which one explains the features more clearly?"
```

### 6. Action Detection
```
Prompt: "List all the actions performed in this tutorial video with timestamps"
```

## Rate Limits & Quotas

**Free Tier (per model):**
- 10-15 RPM (requests per minute)
- 1M-4M TPM (tokens per minute)
- 1,500 RPD (requests per day)

**YouTube Limitations:**
- Free tier: 8 hours of YouTube video per day
- Paid tier: No length-based limits
- Public videos only (no private/unlisted)

**Storage (Files API):**
- 20GB per project
- 2GB per file
- 48-hour retention period

## Token Calculation

Video tokens depend on resolution:
- **Default resolution**: ~300 tokens per second of video
- **Low resolution**: ~100 tokens per second of video

**Example:** A 10-minute video = 600 seconds × 300 tokens = ~180,000 tokens

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| 400 Bad Request | Invalid video format or corrupt file | Check file format and integrity |
| 403 Forbidden | Invalid/missing API key | Verify GEMINI_API_KEY configuration |
| 404 Not Found | File URI not found | Ensure file is uploaded and active |
| 429 Too Many Requests | Rate limit exceeded | Implement backoff, upgrade to paid tier |
| 500 Internal Error | Server-side issue | Retry with exponential backoff |

## Best Practices

1. **Use Files API for videos >20MB** - More reliable than inline data
2. **Wait for file processing** - Poll until state is ACTIVE before analysis
3. **Optimize FPS** - Use lower FPS for static content to save tokens
4. **Clip long videos** - Process specific segments instead of entire video
5. **Cache context** - Reuse uploaded files for multiple queries
6. **Batch processing** - Process multiple short videos in one request (2.5+)
7. **Specific prompts** - Be precise about what you want to extract

## Implementation Notes

### For Claude Code:

When a user requests video analysis:

1. **Check API key availability** first using the helper script
2. **Determine video source**: local file, YouTube URL, or multiple videos
3. **Select appropriate model** based on requirements (default: gemini-2.5-flash)
4. **Run the analysis script** with proper parameters
5. **Parse and present results** to the user clearly
6. **Handle errors gracefully** with helpful suggestions

### Files API Workflow:

For videos >20MB or reusable content:
1. Upload video using Files API (script handles this automatically)
2. Wait for ACTIVE state (polling included in script)
3. Use file URI for analysis
4. Files auto-delete after 48 hours

### Inline Data Workflow:

For videos <20MB:
1. Read video file as bytes
2. Base64 encode for API
3. Send in generateContent request
4. Single-use, no upload needed

## Example Workflows

### Workflow 1: YouTube Video Summary
```bash
# User: "Analyze this YouTube tutorial video"
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --youtube-url "https://www.youtube.com/watch?v=abc123" \
  --prompt "Create a structured summary with: 1) Main topics, 2) Key takeaways, 3) Recommended audience"
```

### Workflow 2: Interview Transcription
```bash
# User: "Transcribe this interview with timestamps"
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "interview.mp4" \
  --prompt "Transcribe this interview with speaker labels, timestamps, and visual descriptions of gestures or slides shown"
```

### Workflow 3: Product Comparison
```bash
# User: "Compare these two product demo videos"
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-paths "demo1.mp4" "demo2.mp4" \
  --model "gemini-2.5-pro" \
  --prompt "Compare these product demos on: features shown, presentation quality, clarity of explanation, and overall effectiveness"
```

## Troubleshooting

**API Key Not Found:**
```bash
# Check API key detection
python .claude/skills/gemini-video-understanding/scripts/check_api_key.py
```

**Video Too Large:**
```
Error: Request size exceeds 20MB
Solution: Script automatically uses Files API for large videos
```

**Processing Timeout:**
```
Error: File not reaching ACTIVE state
Solution: Check video integrity, try smaller file, or different format
```

**Rate Limit Errors:**
```
Error: 429 Too Many Requests
Solution: Wait before retry, or upgrade to paid tier
```

## Additional Resources

- **API Documentation**: https://ai.google.dev/gemini-api/docs/video-understanding
- **Files API Guide**: https://ai.google.dev/gemini-api/docs/vision#uploading-files
- **Rate Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
- **Pricing**: https://ai.google.dev/pricing
- **Get API Key**: https://aistudio.google.com/apikey

## Version History

- **1.0.0** (2025-10-26): Initial release with full video understanding capabilities
