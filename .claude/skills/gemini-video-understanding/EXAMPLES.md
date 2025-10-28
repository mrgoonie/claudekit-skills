# Gemini Video Understanding - Examples

## Setup

1. **Install dependencies:**
```bash
pip install -r .claude/skills/gemini-video-understanding/requirements.txt
```

2. **Configure API key:**
```bash
# Option 1: Environment variable (recommended)
export GEMINI_API_KEY="your-api-key-here"

# Option 2: Copy and edit .env file
cp .claude/skills/gemini-video-understanding/.env.example \
   .claude/skills/gemini-video-understanding/.env
# Then edit the .env file with your API key
```

3. **Verify configuration:**
```bash
python .claude/skills/gemini-video-understanding/scripts/check_api_key.py
```

## Basic Examples

### Example 1: Simple Video Summary
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/video.mp4" \
  --prompt "Summarize this video in 3 key points"
```

**Output:**
```
1. The video demonstrates how to use the Gemini API for video analysis
2. It covers three main input methods: Files API, inline data, and YouTube URLs
3. Examples show various use cases including transcription and timestamp queries
```

### Example 2: YouTube Video Analysis
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --youtube-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --prompt "What is this video about? List the main topics discussed."
```

### Example 3: Detailed Transcription
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/interview.mp4" \
  --prompt "Transcribe this interview with timestamps and speaker labels" \
  --verbose
```

## Advanced Examples

### Example 4: Video Clipping
Analyze only a specific portion of a video:

```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/long-video.mp4" \
  --prompt "Summarize this segment" \
  --start-offset "2m30s" \
  --end-offset "5m15s"
```

### Example 5: High Frame Rate Analysis
For videos with fast action:

```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/sports.mp4" \
  --prompt "Describe the key movements and techniques shown" \
  --fps 5
```

### Example 6: Comparing Multiple Videos
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-paths "/path/video1.mp4" "/path/video2.mp4" \
  --prompt "Compare these two product demos. Which one is more effective and why?" \
  --model "gemini-2.5-pro"
```

### Example 7: Educational Content Generation
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --prompt "Create a quiz with 5 multiple-choice questions based on this video. Include an answer key with explanations."
```

### Example 8: Timestamp-Specific Questions
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/tutorial.mp4" \
  --prompt "What happens at 01:15 and 02:30? How are these two moments related?"
```

## Prompting Best Practices

### For Summaries
```
"Provide a structured summary with:
1. Main topic or theme
2. Key points discussed (3-5 bullet points)
3. Notable quotes or moments with timestamps
4. Target audience or intended purpose"
```

### For Transcriptions
```
"Transcribe this video including:
- Speaker labels (Speaker 1, Speaker 2, etc.)
- Timestamps for each segment (MM:SS format)
- Visual descriptions in [brackets] when relevant
- Key gestures or on-screen text mentioned"
```

### For Educational Content
```
"Analyze this educational video and create:
1. Learning objectives (3-5 points)
2. Key concepts explained with timestamps
3. 5 quiz questions with multiple choice answers
4. Answer key with brief explanations"
```

### For Comparisons
```
"Compare these videos on the following criteria:
1. Content quality and accuracy
2. Presentation style and clarity
3. Production quality (audio, video, editing)
4. Target audience suitability
5. Overall effectiveness
Provide ratings (1-5) for each criterion with justification."
```

## Use Case Examples

### Use Case 1: Meeting Notes
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "team-meeting.mp4" \
  --prompt "Create meeting notes with: 1) Attendees (if visible), 2) Topics discussed with timestamps, 3) Action items identified, 4) Decisions made" \
  --output-file "meeting-notes.txt"
```

### Use Case 2: Content Moderation
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "user-submitted.mp4" \
  --prompt "Analyze this video for: 1) Overall content type, 2) Any inappropriate content, 3) Compliance with community guidelines, 4) Recommended action (approve/review/reject)"
```

### Use Case 3: Accessibility - Video Descriptions
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "promotional-video.mp4" \
  --prompt "Create an audio description track for visually impaired viewers. Include descriptions of: visual elements, on-screen text, scene changes, and important actions at appropriate timestamps."
```

### Use Case 4: Sports Analysis
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "game-footage.mp4" \
  --prompt "Analyze this game footage: 1) Key plays with timestamps, 2) Player performance highlights, 3) Strategic decisions, 4) Turning points in the game" \
  --fps 2 \
  --verbose
```

### Use Case 5: Tutorial Enhancement
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --youtube-url "https://www.youtube.com/watch?v=TUTORIAL_ID" \
  --prompt "Create an enhanced tutorial outline with: 1) Chapter markers with timestamps, 2) Prerequisites mentioned, 3) Tools/resources needed, 4) Common mistakes to avoid, 5) Practice exercises suggested"
```

## Output Options

### Save to File
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "video.mp4" \
  --prompt "Summarize this video" \
  --output-file "summary.txt"
```

### JSON Output
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "video.mp4" \
  --prompt "Summarize this video" \
  --json \
  --output-file "summary.json"
```

### Verbose Mode (with token usage)
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "video.mp4" \
  --prompt "Analyze this video" \
  --verbose
```

## Error Handling

### Check API Key
```bash
python .claude/skills/gemini-video-understanding/scripts/check_api_key.py
```

### Common Errors

**File Not Found:**
```bash
# Error: Video file not found: /path/to/video.mp4
# Solution: Check file path and ensure file exists
ls -lh /path/to/video.mp4
```

**API Key Invalid:**
```bash
# Error: 403 Forbidden
# Solution: Verify API key is correct
python .claude/skills/gemini-video-understanding/scripts/check_api_key.py
```

**Rate Limit:**
```bash
# Error: 429 Too Many Requests
# Solution: Wait before retrying, or upgrade to paid tier
```

## Model Selection

### Fast Processing
```bash
--model "gemini-2.0-flash-lite"  # Fastest, good for simple tasks
```

### Balanced (Default)
```bash
--model "gemini-2.5-flash"  # Best balance of speed and quality
```

### Highest Quality
```bash
--model "gemini-2.5-pro"  # Most accurate, slower, higher token usage
```

## Performance Tips

1. **Use video clipping** to analyze only relevant portions
2. **Adjust FPS** based on content type (lower for static, higher for action)
3. **Use Files API** for videos >20MB (handled automatically)
4. **Batch process** multiple short videos in one request (Gemini 2.5+)
5. **Cache uploaded files** - reuse file URIs for multiple queries

## Resources

- **API Documentation**: https://ai.google.dev/gemini-api/docs/video-understanding
- **Get API Key**: https://aistudio.google.com/apikey
- **Pricing**: https://ai.google.dev/pricing
- **Rate Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
