# Quick Start Guide - Gemini Video Understanding

## 1. Install Dependencies

```bash
pip install google-genai
```

Or use the requirements file:
```bash
pip install -r .claude/skills/gemini-video-understanding/requirements.txt
```

## 2. Configure API Key

Choose one option:

**Option A: Environment Variable (Recommended)**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option B: Skill Directory .env**
```bash
cp .claude/skills/gemini-video-understanding/.env.example \
   .claude/skills/gemini-video-understanding/.env
# Edit the .env file with your API key
```

**Option C: Project Root .env**
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

Get your API key at: https://aistudio.google.com/apikey

## 3. Verify Setup

```bash
python .claude/skills/gemini-video-understanding/scripts/check_api_key.py
```

## 4. Analyze Your First Video

**Local video file:**
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "/path/to/video.mp4" \
  --prompt "Summarize this video in 3 sentences"
```

**YouTube video:**
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --prompt "What are the main topics discussed?"
```

## 5. Common Commands

**Transcribe with timestamps:**
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "video.mp4" \
  --prompt "Transcribe this video with timestamps and visual descriptions"
```

**Analyze specific segment:**
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "video.mp4" \
  --prompt "Summarize this part" \
  --start-offset "1m30s" \
  --end-offset "3m"
```

**Compare videos:**
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-paths "video1.mp4" "video2.mp4" \
  --prompt "Compare these videos"
```

**Save to file:**
```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py \
  --video-path "video.mp4" \
  --prompt "Analyze this video" \
  --output-file "analysis.txt"
```

## Help

```bash
python .claude/skills/gemini-video-understanding/scripts/analyze_video.py --help
```

See [EXAMPLES.md](EXAMPLES.md) for more detailed examples and use cases.
