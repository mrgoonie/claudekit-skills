# Gemini Audio Code Examples

Comprehensive code examples for audio understanding and speech generation.

## Table of Contents

- [Audio Understanding Examples](#audio-understanding-examples)
- [Speech Generation Examples](#speech-generation-examples)
- [Advanced Use Cases](#advanced-use-cases)
- [Integration Patterns](#integration-patterns)

## Audio Understanding Examples

### Basic Transcription

**Python**:
```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

# Upload audio
audio_file = client.files.upload(file="meeting.mp3")

# Transcribe
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Generate a complete transcript with accurate punctuation.',
        audio_file
    ]
)

print(response.text)
```

**JavaScript**:
```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: "YOUR_API_KEY" });

const audioFile = await ai.files.upload({
  file: "meeting.mp3",
  config: { mimeType: "audio/mp3" }
});

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: [
    { text: "Generate a complete transcript with accurate punctuation." },
    { fileData: { fileUri: audioFile.uri, mimeType: audioFile.mimeType } }
  ]
});

console.log(response.text);
```

### Transcription with Timestamps

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")
audio_file = client.files.upload(file="podcast.mp3")

prompt = """
Generate a detailed transcript with timestamps in [MM:SS] format.
Format each paragraph with its timestamp at the beginning.
Example:
[00:15] First speaker introduces the topic...
[02:30] Discussion of key points begins...
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)

print(response.text)
```

### Audio Summarization

```python
# Simple summary
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Summarize the key points from this audio in 5 bullet points.',
        audio_file
    ]
)

# Structured summary
prompt = """
Analyze this audio and provide:
1. Main topic (1 sentence)
2. Key points (3-5 bullets)
3. Action items mentioned (if any)
4. Speakers/participants identified
5. Overall tone and context
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)
```

### Segment Analysis with Timestamps

```python
# Analyze specific time range
prompt = "What topics are discussed between 05:30 and 10:15? Provide quotes."

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)

# Multiple segments
prompt = """
Analyze these time segments:
- 00:00-02:30: Introduction
- 02:30-10:00: Main discussion
- 10:00-12:00: Q&A

For each segment, provide:
- Key topics covered
- Important quotes
- Speaker identification
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)
```

### Multi-Speaker Dialogue Extraction

```python
prompt = """
Extract dialogue from this audio:
1. Identify each speaker (Speaker A, B, etc.)
2. Format as:
   Speaker A: "Dialogue text"
   Speaker B: "Response"
3. Include timestamps for speaker changes
4. Note tone and emotion when relevant
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)
```

### Non-Speech Audio Analysis

```python
# Identify all sounds
prompt = """
Analyze all sounds in this audio:
- Speech (what is being said)
- Music (type, instruments, mood)
- Ambient sounds (traffic, nature, etc.)
- Sound effects
Provide timestamps for each sound type.
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)

# Music analysis
prompt = """
Analyze the music in this audio:
- Genre and style
- Tempo and mood
- Instruments used
- Vocal characteristics (if any)
- Similar artists or songs
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)
```

### Inline Audio for Small Files

```python
from google.genai import types

# For files under 20MB
with open('short_clip.mp3', 'rb') as f:
    audio_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Transcribe this audio',
        types.Part.from_bytes(data=audio_bytes, mime_type='audio/mp3')
    ]
)
```

### Multiple Audio Files

```python
# Upload multiple files
file1 = client.files.upload(file="part1.mp3")
file2 = client.files.upload(file="part2.mp3")

# Analyze together (ensure combined duration < 9.5 hours)
prompt = "Compare these two audio clips. What are the differences?"

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, file1, file2]
)
```

## Speech Generation Examples

### Basic Text-to-Speech

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents='Generate audio: Welcome to our podcast.',
    config=types.GenerateContentConfig(
        response_modalities=['audio']
    )
)

# Save audio
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('welcome.wav', 'wb') as f:
            f.write(part.inline_data.data)
```

### Controlled Voice Style

```python
# Professional narration
response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents='Generate audio: In today\'s episode, we explore the future of AI, in a professional, authoritative tone.',
    config=types.GenerateContentConfig(response_modalities=['audio'])
)

# Casual conversation
response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents='Generate audio: Hey everyone, welcome back! in a casual, friendly style.',
    config=types.GenerateContentConfig(response_modalities=['audio'])
)

# Slow and clear
response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents='Generate audio: Follow these steps carefully, speaking slowly and clearly.',
    config=types.GenerateContentConfig(response_modalities=['audio'])
)
```

### Multi-Paragraph Speech

```python
script = """
Generate audio:
Welcome to the Daily Tech Update. I'm your host, and today we have some exciting news.

First up, recent developments in artificial intelligence have shown remarkable progress.
Researchers have achieved new breakthroughs in natural language processing.

Stay tuned for more updates throughout the week.

This has been your Daily Tech Update.

Narrate this in a professional news anchor style, with appropriate pacing and emphasis.
"""

response = client.models.generate_content(
    model='gemini-2.5-flash-native-audio-preview-09-2025',
    contents=script,
    config=types.GenerateContentConfig(response_modalities=['audio'])
)
```

### Batch Speech Generation

```python
# Generate multiple audio segments
segments = [
    "Welcome to chapter one: Introduction",
    "In this chapter, we will explore the basics.",
    "Chapter two begins our deep dive into advanced topics."
]

for i, text in enumerate(segments):
    response = client.models.generate_content(
        model='gemini-2.5-flash-native-audio-preview-09-2025',
        contents=f'Generate audio: {text}, in a narrative storytelling style.',
        config=types.GenerateContentConfig(response_modalities=['audio'])
    )

    # Save each segment
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            with open(f'segment_{i+1}.wav', 'wb') as f:
                f.write(part.inline_data.data)
```

## Advanced Use Cases

### Meeting Transcription with Action Items

```python
prompt = """
Analyze this meeting recording:

1. Provide complete transcript with timestamps
2. Identify all speakers
3. Extract action items in format:
   - Action: [description]
   - Owner: [speaker]
   - Deadline: [if mentioned]
4. Summarize key decisions made
5. Note any follow-up items
"""

response = client.models.generate_content(
    model='gemini-2.5-pro',  # Use Pro for complex analysis
    contents=[prompt, audio_file]
)
```

### Podcast Editing Assistant

```python
prompt = """
Analyze this podcast episode:

1. Identify intro (0:00-?), main content, and outro
2. Flag any long pauses or "um/uh" sections with timestamps
3. Suggest cuts or edits for better flow
4. Identify best quotable moments
5. Suggest chapter markers with titles
6. Rate audio quality and note any issues
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)
```

### Interview Analysis

```python
prompt = """
Analyze this interview:

1. Interview structure:
   - Introduction
   - Main questions and answers
   - Conclusion

2. For each question:
   - Question text with timestamp
   - Answer summary
   - Key insights or quotes

3. Interviewee insights:
   - Main themes discussed
   - Notable quotes
   - Expertise areas demonstrated

4. Overall assessment:
   - Interview quality
   - Best moments
   - Suggested highlights for promotional clips
"""

response = client.models.generate_content(
    model='gemini-2.5-pro',
    contents=[prompt, audio_file]
)
```

### Accessibility: Audio Description Generation

```python
# Analyze video audio, generate descriptions
prompt = """
From this audio track:
1. Transcribe all dialogue
2. Identify sound effects and their timing
3. Generate audio description script for visual scenes based on audio cues
4. Format for screen reader compatibility
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)
```

### Language Learning: Pronunciation Analysis

```python
# Student recording analysis
prompt = """
Analyze this language learning recording:

1. Transcribe what was said
2. Identify pronunciation issues
3. Compare to target pronunciation
4. Suggest specific improvements
5. Rate overall clarity (1-10)
6. Highlight words to practice
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[prompt, audio_file]
)
```

## Integration Patterns

### Flask Web API

```python
from flask import Flask, request, jsonify
from google import genai
import tempfile

app = Flask(__name__)
client = genai.Client(api_key="YOUR_API_KEY")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400

    audio = request.files['audio']

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        audio.save(tmp.name)

        # Upload to Gemini
        uploaded = client.files.upload(file=tmp.name)

        # Transcribe
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=['Transcribe this audio', uploaded]
        )

        return jsonify({
            'transcript': response.text,
            'file_id': uploaded.name
        })

if __name__ == '__main__':
    app.run(debug=True)
```

### Batch Processing with Progress Tracking

```python
import os
from pathlib import Path
from tqdm import tqdm

def batch_transcribe(audio_dir: str, output_dir: str):
    """Transcribe all audio files in directory"""

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    audio_files = list(Path(audio_dir).glob('*.mp3'))

    for audio_path in tqdm(audio_files, desc="Transcribing"):
        # Upload
        uploaded = client.files.upload(file=str(audio_path))

        # Transcribe
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=['Generate complete transcript', uploaded]
        )

        # Save transcript
        output_path = Path(output_dir) / f"{audio_path.stem}.txt"
        with open(output_path, 'w') as f:
            f.write(response.text)

        # Cleanup
        client.files.delete(name=uploaded.name)

# Usage
batch_transcribe('audio_files/', 'transcripts/')
```

### Streaming Response Handler

```python
def process_audio_stream(audio_path: str, chunk_duration: int = 300):
    """
    Process long audio in chunks (for audio > 9.5 hours)

    Args:
        audio_path: Path to audio file
        chunk_duration: Duration per chunk in seconds
    """
    from pydub import AudioSegment

    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)
    chunk_ms = chunk_duration * 1000

    transcripts = []

    for i in range(0, duration_ms, chunk_ms):
        chunk = audio[i:i+chunk_ms]

        # Export chunk
        chunk_path = f"temp_chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")

        # Transcribe chunk
        uploaded = client.files.upload(file=chunk_path)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[f'Transcribe from {i//1000}s:', uploaded]
        )

        transcripts.append({
            'start_time': i // 1000,
            'transcript': response.text
        })

        # Cleanup
        os.remove(chunk_path)
        client.files.delete(name=uploaded.name)

    return transcripts
```

### Error Handling and Retry Logic

```python
import time
import random
from google.api_core import exceptions

def transcribe_with_retry(audio_path: str, max_retries: int = 5):
    """Transcribe with exponential backoff retry"""

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    for attempt in range(max_retries):
        try:
            uploaded = client.files.upload(file=audio_path)

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=['Transcribe this audio', uploaded]
            )

            return response.text

        except exceptions.ResourceExhausted:
            if attempt < max_retries - 1:
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limited. Waiting {wait:.2f}s...")
                time.sleep(wait)
            else:
                raise

        except exceptions.InvalidArgument as e:
            print(f"Invalid request: {e}")
            raise

        except Exception as e:
            print(f"Unexpected error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise
```

## Additional Resources

- See `api-reference.md` for complete API documentation
- See `best-practices.md` for optimization strategies
- See `tts-guide.md` for advanced speech generation techniques
