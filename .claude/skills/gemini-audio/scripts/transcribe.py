#!/usr/bin/env python3
"""
Gemini Audio Transcription Tool

Transcribe audio files using Google Gemini API with optional timestamps.

Usage:
    python transcribe.py audio.mp3
    python transcribe.py audio.mp3 --include-timestamps
    python transcribe.py audio.mp3 --model gemini-2.5-pro
    python transcribe.py audio.mp3 --output transcript.txt
"""

import argparse
import sys
from pathlib import Path
from google import genai
from api_key_helper import get_api_key_or_exit


def transcribe_audio(
    audio_path: str,
    model: str = 'gemini-2.5-flash',
    include_timestamps: bool = False,
    output_file: str = None
) -> str:
    """
    Transcribe audio file using Gemini API

    Args:
        audio_path: Path to audio file
        model: Gemini model to use
        include_timestamps: Include timestamps in transcript
        output_file: Optional output file path

    Returns:
        Transcript text
    """
    # Get API key
    api_key = get_api_key_or_exit()
    client = genai.Client(api_key=api_key)

    # Upload audio file
    print(f"📤 Uploading {audio_path}...", file=sys.stderr)
    audio_file = client.files.upload(file=audio_path)
    print(f"✓ File uploaded: {audio_file.name}", file=sys.stderr)

    # Create prompt
    if include_timestamps:
        prompt = (
            "Generate a detailed transcript of this audio with timestamps. "
            "Format timestamps as [MM:SS] before each sentence or paragraph. "
            "Include speaker labels if multiple speakers are present."
        )
    else:
        prompt = (
            "Generate a complete transcript of this audio with accurate "
            "punctuation, capitalization, and paragraph breaks."
        )

    # Generate transcript
    print(f"🎙️  Transcribing with {model}...", file=sys.stderr)
    response = client.models.generate_content(
        model=model,
        contents=[prompt, audio_file]
    )

    transcript = response.text

    # Save to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"✓ Transcript saved to {output_file}", file=sys.stderr)

    return transcript


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe audio files using Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic transcription
  python transcribe.py podcast.mp3

  # With timestamps
  python transcribe.py meeting.wav --include-timestamps

  # Save to file
  python transcribe.py interview.mp3 --output transcript.txt

  # Use different model
  python transcribe.py audio.aac --model gemini-2.5-pro
        """
    )

    parser.add_argument(
        'audio_file',
        help='Path to audio file (WAV, MP3, AAC, FLAC, OGG, AIFF)'
    )

    parser.add_argument(
        '--model',
        default='gemini-2.5-flash',
        choices=['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.5-flash', 'gemini-1.5-pro'],
        help='Gemini model to use (default: gemini-2.5-flash)'
    )

    parser.add_argument(
        '--include-timestamps',
        action='store_true',
        help='Include timestamps in transcript ([MM:SS] format)'
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

    # Transcribe
    try:
        transcript = transcribe_audio(
            args.audio_file,
            model=args.model,
            include_timestamps=args.include_timestamps,
            output_file=args.output
        )

        # Print to stdout if no output file specified
        if not args.output:
            print("\n" + "="*60)
            print("TRANSCRIPT")
            print("="*60 + "\n")
            print(transcript)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
