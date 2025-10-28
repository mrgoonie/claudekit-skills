#!/usr/bin/env python3
"""
Gemini Text-to-Speech Generation Tool

Generate natural speech from text using Google Gemini API.

Usage:
    python generate-speech.py "Hello world" --output hello.wav
    python generate-speech.py "Welcome to our podcast" --style professional
    python generate-speech.py "Read this slowly" --pace slow --tone friendly
    python generate-speech.py --input script.txt --output narration.wav
"""

import argparse
import sys
from pathlib import Path
from google import genai
from google.genai import types
from api_key_helper import get_api_key_or_exit


def generate_speech(
    text: str,
    output_file: str,
    model: str = 'gemini-2.5-flash-native-audio-preview-09-2025',
    style: str = None,
    pace: str = None,
    tone: str = None,
    accent: str = None
) -> None:
    """
    Generate speech from text using Gemini API

    Args:
        text: Text to convert to speech
        output_file: Output audio file path
        model: Gemini TTS model to use
        style: Voice style (professional, casual, narrative, conversational)
        pace: Speech pace (slow, normal, fast)
        tone: Voice tone (friendly, serious, enthusiastic, warm)
        accent: Voice accent (natural language description)
    """
    # Get API key
    api_key = get_api_key_or_exit()
    client = genai.Client(api_key=api_key)

    # Build enhanced prompt with style controls
    prompt_parts = ["Generate audio:"]

    # Add style modifiers
    modifiers = []
    if style:
        modifiers.append(f"in a {style} style")
    if pace and pace != 'normal':
        modifiers.append(f"at a {pace} pace")
    if tone:
        modifiers.append(f"with a {tone} tone")
    if accent:
        modifiers.append(f"with {accent} accent")

    if modifiers:
        prompt_parts.append(", ".join(modifiers) + ".")

    prompt_parts.append(text)

    final_prompt = " ".join(prompt_parts)

    # Generate speech
    print(f"🎙️  Generating speech with {model}...", file=sys.stderr)
    if modifiers:
        print(f"📝 Style: {', '.join(modifiers)}", file=sys.stderr)

    try:
        response = client.models.generate_content(
            model=model,
            contents=final_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['audio']
            )
        )

        # Extract audio data from response
        audio_data = None
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                audio_data = part.inline_data.data
                break

        if not audio_data:
            print("❌ Error: No audio data in response", file=sys.stderr)
            sys.exit(1)

        # Save audio to file
        with open(output_file, 'wb') as f:
            f.write(audio_data)

        print(f"✓ Speech saved to {output_file}", file=sys.stderr)
        print(f"📊 Size: {len(audio_data):,} bytes", file=sys.stderr)

    except Exception as e:
        print(f"❌ Error generating speech: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Generate speech from text using Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic speech generation
  python generate-speech.py "Hello world" --output hello.wav

  # Professional narration
  python generate-speech.py "Welcome to today's episode" \\
    --style professional --tone warm --output intro.wav

  # Casual conversation
  python generate-speech.py "Hey, what's up?" \\
    --style casual --tone friendly --output greeting.wav

  # Slow-paced instruction
  python generate-speech.py "Follow these steps carefully" \\
    --pace slow --tone serious --output instruction.wav

  # From file
  python generate-speech.py --input script.txt --output narration.wav

  # With accent
  python generate-speech.py "Cheerio!" \\
    --accent "British English" --output cheerio.wav
        """
    )

    parser.add_argument(
        'text',
        nargs='?',
        help='Text to convert to speech (or use --input)'
    )

    parser.add_argument(
        '--input', '-i',
        help='Read text from file instead of command line'
    )

    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output audio file path (e.g., output.wav)'
    )

    parser.add_argument(
        '--model',
        default='gemini-2.5-flash-native-audio-preview-09-2025',
        choices=[
            'gemini-2.5-flash-native-audio-preview-09-2025',
            'gemini-2.5-pro'
        ],
        help='Gemini TTS model (default: flash-native-audio)'
    )

    parser.add_argument(
        '--style',
        choices=['professional', 'casual', 'narrative', 'conversational'],
        help='Voice style'
    )

    parser.add_argument(
        '--pace',
        choices=['slow', 'normal', 'fast'],
        help='Speech pace'
    )

    parser.add_argument(
        '--tone',
        choices=['friendly', 'serious', 'enthusiastic', 'warm', 'calm'],
        help='Voice tone'
    )

    parser.add_argument(
        '--accent',
        help='Voice accent (natural language, e.g., "British English", "American Southern")'
    )

    args = parser.parse_args()

    # Get text from argument or file
    if args.input:
        if not Path(args.input).exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read().strip()

        print(f"📖 Reading text from {args.input}", file=sys.stderr)
    elif args.text:
        text = args.text
    else:
        print("Error: Provide text as argument or use --input", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    if not text:
        print("Error: Text is empty", file=sys.stderr)
        sys.exit(1)

    print(f"📝 Text length: {len(text)} characters", file=sys.stderr)

    # Generate speech
    generate_speech(
        text=text,
        output_file=args.output,
        model=args.model,
        style=args.style,
        pace=args.pace,
        tone=args.tone,
        accent=args.accent
    )


if __name__ == '__main__':
    main()
