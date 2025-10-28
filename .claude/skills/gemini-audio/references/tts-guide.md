# Gemini Text-to-Speech Guide

Advanced guide for generating natural speech using Google Gemini API.

## Table of Contents

- [Overview](#overview)
- [Voice Control Techniques](#voice-control-techniques)
- [Prompt Engineering for TTS](#prompt-engineering-for-tts)
- [Quality Optimization](#quality-optimization)
- [Common Use Cases](#common-use-cases)
- [Production Best Practices](#production-best-practices)

## Overview

Gemini provides controllable text-to-speech through natural language instructions embedded in the prompt.

### Available Models

| Model | Quality | Speed | Cost | Best For |
|-------|---------|-------|------|----------|
| `gemini-2.5-flash-native-audio-preview-09-2025` | High | Fast | $10/1M tokens | General TTS, podcasts |
| `gemini-2.5-pro` | Premium | Slower | $20/1M tokens | Production audio |

### Basic Usage

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents='Generate audio: Hello, welcome to our podcast.',
    config=types.GenerateContentConfig(
        response_modalities=['audio']
    )
)

# Save audio
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('output.wav', 'wb') as f:
            f.write(part.inline_data.data)
```

## Voice Control Techniques

### Style Control

Control voice characteristics through natural language:

```python
# Professional/Formal
"Generate audio: Welcome to the quarterly earnings call, in a professional, formal tone."

# Casual/Conversational
"Generate audio: Hey everyone, what's up? in a casual, friendly style."

# Narrative/Storytelling
"Generate audio: Once upon a time, in a distant land, in a narrative storytelling style."

# Instructional/Educational
"Generate audio: Today we'll learn how to..., in a clear, instructional tone."

# Enthusiastic/Energetic
"Generate audio: Welcome back to the show! in an enthusiastic, high-energy style."

# Calm/Soothing
"Generate audio: Take a deep breath and relax, in a calm, soothing voice."
```

### Pace Control

```python
# Slow pace
"Generate audio: Follow these steps carefully, speaking slowly and clearly."

# Normal pace
"Generate audio: This is a standard narration, at a normal conversational pace."

# Fast pace
"Generate audio: Breaking news update, speaking quickly with urgency."

# Variable pace
"""Generate audio:
Speak slowly here for emphasis.
Then speed up for this exciting part!
And return to normal pace for conclusion.
"""
```

### Tone Control

```python
# Friendly/Warm
"Generate audio: Thank you for joining us, with a warm, friendly tone."

# Serious/Authoritative
"Generate audio: This is a critical announcement, in a serious, authoritative voice."

# Playful/Lighthearted
"Generate audio: Let's have some fun! in a playful, lighthearted manner."

# Empathetic/Compassionate
"Generate audio: We understand this is difficult, with an empathetic, compassionate tone."

# Confident/Assertive
"Generate audio: We will succeed, speaking confidently and assertively."
```

### Accent and Language

```python
# Specify accent
"Generate audio: Cheerio, old chap! with a British English accent."

"Generate audio: G'day mate! with an Australian accent."

# Different languages (check model support)
"Generate audio: Bonjour, comment allez-vous? in French with native accent."
```

### Emotion Control

```python
# Happy/Joyful
"Generate audio: We did it! speaking happily and joyfully."

# Excited
"Generate audio: This is amazing! with excitement and enthusiasm."

# Sad/Somber
"Generate audio: We'll miss you, in a sad, somber tone."

# Angry/Frustrated
"Generate audio: This is unacceptable, with controlled frustration."

# Surprised
"Generate audio: Wow, I didn't expect that! with genuine surprise."
```

## Prompt Engineering for TTS

### Effective Prompt Structure

**Template**: `Generate audio: [text], [style], [pace], [tone], [additional modifiers]`

```python
# Simple
"Generate audio: Hello world."

# With modifiers
"Generate audio: Hello world, in a professional tone."

# Multiple modifiers
"Generate audio: Hello world, in a professional tone, speaking clearly at normal pace."

# Complex instruction
"""Generate audio:
Welcome to our podcast. Today we have an exciting episode.
Speak professionally with a warm, welcoming tone at a moderate pace.
Emphasize the word 'exciting' with enthusiasm.
"""
```

### Multi-Paragraph Speech

```python
script = """
Generate audio:

[Intro - warm and welcoming]
Welcome to Tech Talks, your weekly dose of technology news.
I'm your host, and today we have an incredible lineup.

[Main content - professional and informative]
First up, let's discuss the latest developments in artificial intelligence.
Recent breakthroughs have shown remarkable progress in natural language processing.

[Conclusion - friendly and upbeat]
That's all for today's episode. Thanks for listening!
Join us next week for more tech insights.

Narrate this as a professional podcast host, varying tone and energy
appropriately for each section. Use natural pacing with brief pauses
between sections.
"""

response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents=script,
    config=types.GenerateContentConfig(response_modalities=['audio'])
)
```

### Emphasis and Pronunciation

```python
# Emphasis
"""Generate audio:
This is VERY important. Please emphasize the word 'VERY'.
"""

# Pronunciation guidance
"""Generate audio:
The company name is Anthropic (an-THROP-ik).
Pronounce it as specified in the phonetic guide.
"""

# Acronyms
"""Generate audio:
We'll discuss AI (spell out as 'A-I'), API (spell as 'A-P-I'),
and NASA (pronounce as 'NASA', not spelled out).
"""
```

### Pauses and Timing

```python
# Natural pauses
"""Generate audio:
First point. [pause] Second point. [pause] Third point.
Include natural pauses between each point.
"""

# Dramatic pauses
"""Generate audio:
The answer is... [dramatic pause] ... yes!
Add a suspenseful pause before revealing the answer.
"""

# Breathing points
"""Generate audio:
This is a long sentence that needs breathing points [breath]
so the listener can follow along comfortably [breath]
without feeling rushed or overwhelmed.
Include natural breathing pauses where indicated.
"""
```

## Quality Optimization

### Audio Post-Processing

```python
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

def enhance_audio(input_path: str, output_path: str):
    """Enhance generated audio quality"""

    # Load audio
    audio = AudioSegment.from_file(input_path)

    # Normalize volume
    audio = normalize(audio)

    # Light compression
    audio = compress_dynamic_range(audio, threshold=-20.0, ratio=2.0)

    # Export with high quality
    audio.export(
        output_path,
        format='wav',
        parameters=['-ar', '44100', '-ac', '2']  # 44.1kHz stereo
    )
```

### Combining Multiple Segments

```python
def generate_segmented_audio(segments: list[dict], output_path: str):
    """
    Generate audio for multiple segments and combine

    Args:
        segments: List of {'text': str, 'style': str}
        output_path: Output file path
    """
    from pydub import AudioSegment

    audio_segments = []

    for i, segment in enumerate(segments):
        prompt = f"Generate audio: {segment['text']}, {segment.get('style', '')}"

        response = client.models.generate_content(
            model='gemini-2.5-flash-native-audio-preview-09-2025',
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=['audio'])
        )

        # Extract audio
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                # Save temporary file
                temp_path = f'temp_segment_{i}.wav'
                with open(temp_path, 'wb') as f:
                    f.write(part.inline_data.data)

                # Load with pydub
                segment_audio = AudioSegment.from_file(temp_path)
                audio_segments.append(segment_audio)

                # Cleanup
                os.remove(temp_path)

    # Combine all segments with silence between
    silence = AudioSegment.silent(duration=500)  # 500ms pause
    combined = audio_segments[0]

    for segment in audio_segments[1:]:
        combined += silence + segment

    # Export
    combined.export(output_path, format='wav')

# Usage
segments = [
    {'text': 'Welcome to our podcast', 'style': 'warm and welcoming'},
    {'text': 'Today we discuss AI', 'style': 'professional and clear'},
    {'text': 'Thanks for listening', 'style': 'friendly and upbeat'}
]

generate_segmented_audio(segments, 'podcast_intro.wav')
```

## Common Use Cases

### Podcast Production

```python
def generate_podcast_intro(
    title: str,
    host_name: str,
    episode_number: int,
    topic: str
) -> bytes:
    """Generate podcast introduction"""

    script = f"""
Generate audio:

Welcome to {title}, episode {episode_number}.
I'm your host, {host_name}.

Today, we're diving into {topic}.
This is going to be an exciting episode, so let's get started!

Narrate this as a professional podcast host with energy and enthusiasm.
Use a warm, welcoming tone with natural pacing.
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash-native-audio-preview-09-2025',
        contents=script,
        config=types.GenerateContentConfig(response_modalities=['audio'])
    )

    # Extract and return audio bytes
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            return part.inline_data.data

# Usage
intro_audio = generate_podcast_intro(
    title="Tech Insights",
    host_name="Alex",
    episode_number=42,
    topic="the future of artificial intelligence"
)

with open('podcast_intro.wav', 'wb') as f:
    f.write(intro_audio)
```

### Audiobook Narration

```python
def generate_audiobook_chapter(chapter_text: str, output_path: str):
    """Generate audiobook narration for chapter"""

    # Split into paragraphs for better control
    paragraphs = chapter_text.split('\n\n')

    audio_parts = []

    for para in paragraphs:
        prompt = f"""
Generate audio:
{para}

Narrate this as an audiobook reader with clear, expressive delivery.
Use appropriate pacing for narrative fiction. Add natural pauses
between sentences. Convey emotion and tone based on the content.
"""

        response = client.models.generate_content(
            model='gemini-2.5-pro',  # Use Pro for higher quality
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=['audio'])
        )

        # Extract audio
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                audio_parts.append(part.inline_data.data)

    # Combine and save
    combine_audio_parts(audio_parts, output_path)
```

### E-Learning Content

```python
def generate_tutorial_audio(
    lesson_title: str,
    steps: list[str],
    output_path: str
):
    """Generate instructional audio for e-learning"""

    script_parts = [
        f"Generate audio: Welcome to this lesson on {lesson_title}. "
        "Let's begin. Speak in a clear, instructional tone."
    ]

    for i, step in enumerate(steps, 1):
        script_parts.append(
            f"Generate audio: Step {i}: {step}. "
            "Speak slowly and clearly, emphasizing key terms."
        )

    script_parts.append(
        "Generate audio: Great work! You've completed this lesson. "
        "Speak encouragingly with a warm tone."
    )

    # Generate each part
    audio_bytes_list = []

    for script in script_parts:
        response = client.models.generate_content(
            model='gemini-2.5-flash-native-audio-preview-09-2025',
            contents=script,
            config=types.GenerateContentConfig(response_modalities=['audio'])
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data:
                audio_bytes_list.append(part.inline_data.data)

    # Combine with pauses
    combine_with_pauses(audio_bytes_list, output_path, pause_ms=1000)
```

### Voice Announcements

```python
def generate_announcement(
    message: str,
    style: str = 'professional',
    urgency: str = 'normal'
) -> bytes:
    """Generate public announcement audio"""

    urgency_styles = {
        'low': 'in a calm, relaxed manner',
        'normal': 'in a clear, professional tone',
        'high': 'with urgency and importance',
        'critical': 'with immediate urgency and seriousness'
    }

    prompt = f"""
Generate audio:
{message}

Speak {urgency_styles.get(urgency, 'clearly')}, {style}.
Ensure the message is clearly understandable.
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash-native-audio-preview-09-2025',
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=['audio'])
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data:
            return part.inline_data.data

# Usage examples
normal_announcement = generate_announcement(
    "The meeting will begin in 5 minutes.",
    style='professional',
    urgency='normal'
)

urgent_announcement = generate_announcement(
    "Please evacuate the building immediately.",
    style='authoritative',
    urgency='critical'
)
```

## Production Best Practices

### Caching for Reusable Content

```python
import hashlib
from pathlib import Path

class AudioCache:
    """Cache generated audio to avoid regeneration"""

    def __init__(self, cache_dir: str = '.audio_cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_path(self, text: str, style: str = '') -> Path:
        """Generate cache file path from text hash"""
        content = f"{text}|{style}"
        hash_key = hashlib.md5(content.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.wav"

    def get_or_generate(self, text: str, style: str = '') -> bytes:
        """Get cached audio or generate new"""
        cache_path = self.get_cache_path(text, style)

        if cache_path.exists():
            print(f"Using cached audio: {cache_path}")
            return cache_path.read_bytes()

        # Generate new
        prompt = f"Generate audio: {text}, {style}" if style else f"Generate audio: {text}"

        response = client.models.generate_content(
            model='gemini-2.5-flash-native-audio-preview-09-2025',
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=['audio'])
        )

        audio_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                audio_bytes = part.inline_data.data
                break

        if audio_bytes:
            cache_path.write_bytes(audio_bytes)
            print(f"Cached audio: {cache_path}")

        return audio_bytes

# Usage
cache = AudioCache()

# First call generates
audio1 = cache.get_or_generate("Welcome to our podcast", "warm and friendly")

# Second call uses cache
audio2 = cache.get_or_generate("Welcome to our podcast", "warm and friendly")
```

### Quality Assurance

```python
def validate_audio_output(audio_bytes: bytes) -> dict:
    """Validate generated audio quality"""

    import tempfile
    from pydub import AudioSegment

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    # Load and analyze
    audio = AudioSegment.from_file(tmp_path)

    # Check duration
    duration_ms = len(audio)

    # Check silence
    silence_thresh = -50  # dB
    non_silent = audio.strip_silence(silence_thresh=silence_thresh)

    # Calculate metrics
    silence_ratio = 1 - (len(non_silent) / duration_ms)

    # Cleanup
    os.remove(tmp_path)

    # Validation
    passed = (
        duration_ms > 100 and  # At least 100ms
        silence_ratio < 0.5 and  # Less than 50% silence
        audio.frame_rate >= 16000  # Min sample rate
    )

    return {
        'passed': passed,
        'duration_ms': duration_ms,
        'silence_ratio': silence_ratio,
        'sample_rate': audio.frame_rate,
        'channels': audio.channels
    }
```

### Error Handling for TTS

```python
def generate_speech_robust(text: str, style: str = '', max_retries: int = 3):
    """Generate speech with robust error handling"""

    for attempt in range(max_retries):
        try:
            prompt = f"Generate audio: {text}, {style}" if style else f"Generate audio: {text}"

            response = client.models.generate_content(
                model='gemini-2.5-flash-native-audio-preview-09-2025',
                contents=prompt,
                config=types.GenerateContentConfig(response_modalities=['audio'])
            )

            # Extract audio
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    audio_bytes = part.inline_data.data

                    # Validate quality
                    validation = validate_audio_output(audio_bytes)

                    if validation['passed']:
                        return audio_bytes
                    else:
                        print(f"Audio quality check failed: {validation}")
                        if attempt < max_retries - 1:
                            continue
                        else:
                            return audio_bytes  # Return anyway on last attempt

            raise ValueError("No audio data in response")

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise

            time.sleep(2 ** attempt)  # Exponential backoff

    raise RuntimeError("Failed to generate speech after all retries")
```

## Additional Resources

- See `api-reference.md` for complete API documentation
- See `code-examples.md` for more implementation examples
- See `best-practices.md` for general optimization strategies
