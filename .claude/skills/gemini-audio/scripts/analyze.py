#!/usr/bin/env python3
"""
Gemini Audio Analysis Tool

Analyze audio with custom prompts using Google Gemini API.
Supports transcription, summarization, segment analysis, and more.

Usage:
    python analyze.py audio.mp3 "Summarize key points"
    python analyze.py audio.mp3 "What is discussed from 02:30 to 05:15?"
    python analyze.py audio.mp3 "Identify speakers and main topics"
    python analyze.py audio.mp3 "Describe all sounds" --model gemini-2.5-pro
"""

import argparse
import sys
from pathlib import Path
from google import genai
from google.genai import types
from api_key_helper import get_api_key_or_exit


def analyze_audio(
    audio_path: str,
    prompt: str,
    model: str = 'gemini-2.5-flash',
    use_inline: bool = False,
    output_file: str = None
) -> str:
    """
    Analyze audio with custom prompt using Gemini API

    Args:
        audio_path: Path to audio file
        prompt: Analysis prompt
        model: Gemini model to use
        use_inline: Use inline data instead of File API
        output_file: Optional output file path

    Returns:
        Analysis result text
    """
    # Get API key
    api_key = get_api_key_or_exit()
    client = genai.Client(api_key=api_key)

    # Prepare audio input
    if use_inline:
        print(f"📂 Reading {audio_path}...", file=sys.stderr)
        with open(audio_path, 'rb') as f:
            audio_bytes = f.read()

        # Determine MIME type from extension
        ext = Path(audio_path).suffix.lower()
        mime_types = {
            '.wav': 'audio/wav',
            '.mp3': 'audio/mp3',
            '.aac': 'audio/aac',
            '.flac': 'audio/flac',
            '.ogg': 'audio/ogg',
            '.aiff': 'audio/aiff'
        }
        mime_type = mime_types.get(ext, 'audio/mp3')

        audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
        contents = [prompt, audio_part]
        print(f"✓ Using inline data ({len(audio_bytes)} bytes)", file=sys.stderr)
    else:
        print(f"📤 Uploading {audio_path}...", file=sys.stderr)
        audio_file = client.files.upload(file=audio_path)
        contents = [prompt, audio_file]
        print(f"✓ File uploaded: {audio_file.name}", file=sys.stderr)

    # Analyze
    print(f"🔍 Analyzing with {model}...", file=sys.stderr)
    print(f"📝 Prompt: {prompt}", file=sys.stderr)

    response = client.models.generate_content(
        model=model,
        contents=contents
    )

    result = response.text

    # Save to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"✓ Result saved to {output_file}", file=sys.stderr)

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Analyze audio with custom prompts using Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Summarize audio
  python analyze.py podcast.mp3 "Summarize key points in 5 bullets"

  # Segment analysis with timestamps
  python analyze.py meeting.wav "What is discussed from 02:30 to 05:15?"

  # Speaker identification
  python analyze.py interview.mp3 "Identify speakers and extract dialogue"

  # Multi-task analysis
  python analyze.py audio.mp3 "Transcribe, identify speakers, and summarize"

  # Non-speech audio
  python analyze.py ambient.wav "Describe all sounds: voices, music, ambient"

  # Use inline data for small files
  python analyze.py small.mp3 "Summarize this" --inline
        """
    )

    parser.add_argument(
        'audio_file',
        help='Path to audio file (WAV, MP3, AAC, FLAC, OGG, AIFF)'
    )

    parser.add_argument(
        'prompt',
        help='Analysis prompt (e.g., "Summarize key points")'
    )

    parser.add_argument(
        '--model',
        default='gemini-2.5-flash',
        choices=['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.5-flash', 'gemini-1.5-pro'],
        help='Gemini model to use (default: gemini-2.5-flash)'
    )

    parser.add_argument(
        '--inline',
        action='store_true',
        help='Use inline data instead of File API (for files <20MB)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: print to stdout)'
    )

    args = parser.parse_args()

    # Validate audio file exists
    if not Path(args.audio_file).exists():
        print(f"Error: File not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)

    # Analyze
    try:
        result = analyze_audio(
            args.audio_file,
            args.prompt,
            model=args.model,
            use_inline=args.inline,
            output_file=args.output
        )

        # Print to stdout if no output file specified
        if not args.output:
            print("\n" + "="*60)
            print("ANALYSIS RESULT")
            print("="*60 + "\n")
            print(result)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
