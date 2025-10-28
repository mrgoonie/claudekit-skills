# Gemini Audio Best Practices

Comprehensive guide for optimizing audio processing with Google Gemini API.

## Table of Contents

- [File Management](#file-management)
- [Cost Optimization](#cost-optimization)
- [Prompt Engineering](#prompt-engineering)
- [Performance Optimization](#performance-optimization)
- [Quality Guidelines](#quality-guidelines)
- [Security Best Practices](#security-best-practices)
- [Error Handling](#error-handling)

## File Management

### Choosing Upload Method

**Use File API when**:
- File size > 20 MB
- Reusing audio across multiple requests
- Processing long-form content (>5 minutes)
- Need to reference same file multiple times

**Use Inline Data when**:
- File size < 20 MB total request
- Single-use audio clips
- Quick one-off analysis
- Prototyping and testing

### File Lifecycle Management

```python
from google import genai
import time

client = genai.Client(api_key="YOUR_API_KEY")

# Upload with tracking
uploaded_files = []

def upload_with_tracking(file_path: str):
    file = client.files.upload(file=file_path)
    uploaded_files.append({
        'name': file.name,
        'uploaded_at': time.time()
    })
    return file

# Cleanup after use
def cleanup_old_files(max_age_hours: int = 24):
    """Delete files older than max_age_hours"""
    current_time = time.time()

    for file_info in uploaded_files[:]:
        age_hours = (current_time - file_info['uploaded_at']) / 3600

        if age_hours > max_age_hours:
            try:
                client.files.delete(name=file_info['name'])
                uploaded_files.remove(file_info)
                print(f"Deleted old file: {file_info['name']}")
            except Exception as e:
                print(f"Error deleting {file_info['name']}: {e}")

# Reuse uploaded files efficiently
def process_multiple_tasks(audio_file):
    """Use same file for multiple analyses"""

    # Upload once
    uploaded = client.files.upload(file=audio_file)

    # Transcribe
    transcript = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=['Transcribe', uploaded]
    )

    # Summarize
    summary = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=['Summarize key points', uploaded]
    )

    # Extract speakers
    speakers = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=['Identify speakers', uploaded]
    )

    # Cleanup
    client.files.delete(name=uploaded.name)

    return {
        'transcript': transcript.text,
        'summary': summary.text,
        'speakers': speakers.text
    }
```

### Managing Project Quota

**Quota limits**:
- 20 GB total per project
- 2 GB per file
- 48-hour retention

**Best practices**:

```python
def check_quota_before_upload(file_size_bytes: int) -> bool:
    """Check if upload fits within quota"""

    # List current files
    files = list(client.files.list())

    # Calculate total used
    total_used = sum(f.size_bytes for f in files)

    # Check if new file fits (leave 1 GB buffer)
    quota_limit = 20 * 1024 * 1024 * 1024  # 20 GB
    buffer = 1 * 1024 * 1024 * 1024  # 1 GB

    available = quota_limit - total_used - buffer

    return file_size_bytes < available

def cleanup_if_needed(new_file_size: int):
    """Cleanup old files if quota is tight"""

    if not check_quota_before_upload(new_file_size):
        # Delete oldest files until space available
        files = sorted(
            client.files.list(),
            key=lambda f: f.create_time
        )

        for file in files:
            client.files.delete(name=file.name)
            if check_quota_before_upload(new_file_size):
                break
```

## Cost Optimization

### Model Selection Strategy

| Use Case | Recommended Model | Cost/1M tokens | Rationale |
|----------|------------------|----------------|-----------|
| Simple transcription | gemini-1.5-flash | $0.70 input | Cheapest, sufficient quality |
| General analysis | gemini-2.5-flash | $1.00 input | Best value for most tasks |
| Complex analysis | gemini-2.5-pro | $3.00 input | Use only when needed |
| Multi-modal | gemini-2.5-pro | $3.00 input | Advanced reasoning |

### Token Optimization

```python
# Calculate cost before processing
def estimate_cost(audio_duration_seconds: int, model: str = 'gemini-2.5-flash'):
    """Estimate processing cost"""

    # 32 tokens per second
    tokens = audio_duration_seconds * 32

    # Pricing per model (per 1M tokens)
    pricing = {
        'gemini-1.5-flash': 0.70,
        'gemini-2.5-flash': 1.00,
        'gemini-2.5-pro': 3.00
    }

    input_cost = (tokens / 1_000_000) * pricing.get(model, 1.00)

    # Assume 10% output tokens (conservative)
    output_pricing = {
        'gemini-1.5-flash': 0.175,
        'gemini-2.5-flash': 0.10,
        'gemini-2.5-pro': 12.00
    }

    output_tokens = tokens * 0.1
    output_cost = (output_tokens / 1_000_000) * output_pricing.get(model, 0.10)

    return {
        'input_tokens': tokens,
        'estimated_input_cost': input_cost,
        'estimated_output_cost': output_cost,
        'total_cost': input_cost + output_cost
    }

# Example
duration_minutes = 60
cost = estimate_cost(duration_minutes * 60, 'gemini-2.5-flash')
print(f"60-minute audio: ${cost['total_cost']:.4f}")
# Output: ~$0.1152 for 1-hour audio
```

### Batch Processing for Cost Efficiency

```python
def batch_process_with_caching(audio_files: list[str]):
    """Process multiple files with shared context caching"""

    # Upload all files first (reuse across tasks)
    uploaded = [client.files.upload(file=f) for f in audio_files]

    # Process all with single model instance
    results = []

    for audio_file in uploaded:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=['Transcribe', audio_file]
        )
        results.append(response.text)

    # Cleanup all at once
    for file in uploaded:
        client.files.delete(name=file.name)

    return results
```

### Reducing Output Tokens

```python
# Inefficient: verbose output
prompt = "Transcribe this audio and provide detailed analysis with examples"

# Efficient: concise output
prompt = "Transcribe this audio. Use concise language."

# Structured output reduces tokens
prompt = """
Provide JSON output:
{
  "transcript": "text here",
  "speakers": ["A", "B"],
  "duration": "MM:SS"
}
"""
```

## Prompt Engineering

### Effective Prompts for Audio

**Structure**: Context + Task + Format + Constraints

```python
# Poor prompt
"Transcribe this"

# Better prompt
"Generate a complete transcript with accurate punctuation and capitalization."

# Best prompt
"""
Generate a complete transcript of this audio with:
- Accurate punctuation and capitalization
- Speaker labels (Speaker A, B, etc.)
- Timestamps in [MM:SS] format at paragraph breaks
- Preserve filler words like "um" and "uh"
"""
```

### Timestamp References

```python
# Specific segment
"Transcribe from 02:30 to 05:15"

# Multiple segments
"""
Analyze these segments:
- 00:00-02:00: Introduction
- 02:00-10:00: Main discussion
- 10:00-end: Conclusion
"""

# Find specific content
"At what timestamp does the speaker mention 'artificial intelligence'?"
```

### Multi-Task Prompts

```python
# Combine tasks to reduce API calls
prompt = """
Perform these tasks:
1. Generate complete transcript
2. Summarize in 5 bullet points
3. Identify speakers
4. Extract action items
5. List key timestamps

Format output with clear sections.
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)
```

### Structured Output Requests

```python
# Request JSON format
prompt = """
Analyze this audio and return JSON:
{
  "transcript": "full transcript text",
  "summary": "brief summary",
  "speakers": ["Speaker 1", "Speaker 2"],
  "key_quotes": [
    {"speaker": "Speaker 1", "quote": "...", "timestamp": "MM:SS"}
  ],
  "topics": ["topic1", "topic2"],
  "sentiment": "positive|neutral|negative"
}
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)

# Parse JSON response
import json
data = json.loads(response.text)
```

## Performance Optimization

### Parallel Processing

```python
import concurrent.futures

def process_audio_file(file_path: str) -> dict:
    """Process single audio file"""
    client = genai.Client(api_key="YOUR_API_KEY")

    uploaded = client.files.upload(file=file_path)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=['Transcribe', uploaded]
    )

    client.files.delete(name=uploaded.name)

    return {
        'file': file_path,
        'transcript': response.text
    }

def batch_process_parallel(file_paths: list[str], max_workers: int = 5):
    """Process multiple files in parallel"""

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_audio_file, path)
            for path in file_paths
        ]

        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error processing file: {e}")

        return results

# Process 10 files in parallel
files = ['audio1.mp3', 'audio2.mp3', ...]
results = batch_process_parallel(files, max_workers=5)
```

### Rate Limit Handling

```python
import time
import random
from google.api_core import exceptions

class RateLimitedClient:
    """Gemini client with automatic rate limiting"""

    def __init__(self, api_key: str, requests_per_minute: int = 60):
        self.client = genai.Client(api_key=api_key)
        self.rpm = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request = 0

    def _wait_if_needed(self):
        """Enforce rate limit"""
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()

    def generate_content_with_retry(self, **kwargs):
        """Generate content with rate limiting and retry"""
        max_retries = 5

        for attempt in range(max_retries):
            try:
                self._wait_if_needed()
                return self.client.models.generate_content(**kwargs)

            except exceptions.ResourceExhausted:
                if attempt < max_retries - 1:
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limited. Waiting {wait:.2f}s...")
                    time.sleep(wait)
                else:
                    raise

# Usage
client = RateLimitedClient(api_key="YOUR_API_KEY", requests_per_minute=60)
response = client.generate_content_with_retry(
    model='gemini-2.5-flash',
    contents=['Transcribe', audio_file]
)
```

### Chunking Long Audio

```python
def process_long_audio(file_path: str, chunk_minutes: int = 30):
    """
    Process audio longer than 9.5 hours by chunking

    Args:
        file_path: Path to audio file
        chunk_minutes: Minutes per chunk (max 570 for 9.5 hours)
    """
    from pydub import AudioSegment

    audio = AudioSegment.from_file(file_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []
    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i:i + chunk_ms]
        chunk_path = f"chunk_{i//chunk_ms}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)

    # Process each chunk
    transcripts = []
    for chunk_path in chunks:
        uploaded = client.files.upload(file=chunk_path)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=['Transcribe', uploaded]
        )
        transcripts.append(response.text)

        # Cleanup
        os.remove(chunk_path)
        client.files.delete(name=uploaded.name)

    # Combine transcripts
    return "\n\n".join(transcripts)
```

## Quality Guidelines

### Audio File Preparation

**Format recommendations**:
- **Lossless**: FLAC for highest quality
- **Compressed**: MP3 at 128+ kbps, AAC at 96+ kbps
- **Uncompressed**: WAV for editing workflow

**Quality checks**:
```python
from pydub import AudioSegment
import librosa

def validate_audio_quality(file_path: str) -> dict:
    """Check audio quality metrics"""

    audio = AudioSegment.from_file(file_path)

    # Load with librosa for analysis
    y, sr = librosa.load(file_path, sr=None)

    # Calculate metrics
    duration = len(audio) / 1000.0  # seconds
    channels = audio.channels
    sample_rate = audio.frame_rate
    bit_depth = audio.sample_width * 8

    # Check for silence
    silence_thresh = -50  # dB
    silence_chunks = librosa.effects.split(y, top_db=abs(silence_thresh))

    return {
        'duration': duration,
        'channels': channels,
        'sample_rate': sample_rate,
        'bit_depth': bit_depth,
        'silent_segments': len(silence_chunks),
        'passed': sample_rate >= 16000 and duration > 0
    }
```

### Handling Poor Quality Audio

```python
# Use higher-quality model for difficult audio
prompt = """
This audio has poor quality (background noise, mumbling).
Please transcribe carefully, marking unclear sections as [inaudible].
"""

response = client.models.generate_content(
    model='gemini-2.5-pro',  # Better for challenging audio
    contents=[prompt, audio_file]
)
```

## Security Best Practices

### API Key Management

```python
import os
from pathlib import Path

def load_api_key_securely() -> str:
    """Load API key using secure 3-step lookup"""

    # 1. Environment variable (most secure)
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        return api_key

    # 2. User config file (chmod 600)
    config_file = Path.home() / '.gemini_config'
    if config_file.exists():
        # Ensure restrictive permissions
        if oct(config_file.stat().st_mode)[-3:] == '600':
            return config_file.read_text().strip()

    # 3. Project .env (add to .gitignore)
    env_file = Path('.env')
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith('GEMINI_API_KEY='):
                return line.split('=', 1)[1].strip()

    raise ValueError("GEMINI_API_KEY not found")
```

### Sanitizing Inputs

```python
def sanitize_prompt(user_input: str) -> str:
    """Sanitize user input for prompts"""

    # Remove potential injection attempts
    sanitized = user_input.replace('"', '\\"')

    # Limit length
    max_length = 5000
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized

def safe_transcribe(audio_path: str, user_prompt: str):
    """Transcribe with sanitized user input"""

    safe_prompt = sanitize_prompt(user_prompt)

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[safe_prompt, audio_file]
    )

    return response.text
```

### Content Safety

```python
from google.genai import types

# Enable safety filters
config = types.GenerateContentConfig(
    safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )
    ]
)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file],
    config=config
)

# Check if blocked
if response.prompt_feedback.block_reason:
    print(f"Content blocked: {response.prompt_feedback.block_reason}")
```

## Error Handling

### Comprehensive Error Handling

```python
from google.api_core import exceptions
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def robust_transcribe(audio_path: str) -> dict:
    """Transcribe with comprehensive error handling"""

    result = {
        'success': False,
        'transcript': None,
        'error': None
    }

    try:
        # Validate file exists
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Upload file
        logger.info(f"Uploading {audio_path}...")
        uploaded = client.files.upload(file=audio_path)

        # Transcribe
        logger.info("Transcribing...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=['Transcribe', uploaded]
        )

        result['success'] = True
        result['transcript'] = response.text

        # Cleanup
        client.files.delete(name=uploaded.name)

    except FileNotFoundError as e:
        result['error'] = f"File error: {e}"
        logger.error(result['error'])

    except exceptions.InvalidArgument as e:
        result['error'] = f"Invalid request: {e}"
        logger.error(result['error'])

    except exceptions.ResourceExhausted as e:
        result['error'] = f"Rate limit exceeded: {e}"
        logger.warning(result['error'])

    except exceptions.PermissionDenied as e:
        result['error'] = f"Permission denied: {e}"
        logger.error(result['error'])

    except Exception as e:
        result['error'] = f"Unexpected error: {e}"
        logger.exception("Unexpected error occurred")

    return result
```

## Additional Resources

- See `api-reference.md` for complete API documentation
- See `code-examples.md` for implementation examples
- See `tts-guide.md` for speech generation best practices
