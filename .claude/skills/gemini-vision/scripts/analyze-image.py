#!/usr/bin/env python3
"""
Gemini Vision API - Image Analysis Script

This script analyzes images using Google's Gemini API with support for:
- Single or multiple images
- Inline data or File API uploads
- Object detection and segmentation
- Custom prompts and models

API Key Lookup Order:
1. Process environment variable (GEMINI_API_KEY)
2. Skill directory (.claude/skills/gemini-vision/.env)
3. Project directory (.env or .gemini_api_key)
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

def find_api_key() -> Optional[str]:
    """
    Find GEMINI_API_KEY using 3-step lookup:
    1. Process environment variable
    2. Skill directory (.env)
    3. Project directory (.env or .gemini_api_key)
    """
    # Step 1: Check process environment
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        return api_key

    # Step 2: Check skill directory
    skill_dir = Path(__file__).parent.parent  # .claude/skills/gemini-vision/
    skill_env = skill_dir / '.env'

    if skill_env.exists():
        with open(skill_env, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"\'')

    # Step 3: Check project directory
    # Try to find project root (go up from skill dir)
    project_dir = skill_dir.parent.parent.parent  # Back to project root

    # Check .env in project root
    project_env = project_dir / '.env'
    if project_env.exists():
        with open(project_env, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"\'')

    # Check .gemini_api_key in project root
    api_key_file = project_dir / '.gemini_api_key'
    if api_key_file.exists():
        with open(api_key_file, 'r') as f:
            return f.read().strip()

    return None


def analyze_image(
    image_paths: List[str],
    prompt: str,
    model: str = "gemini-2.5-flash",
    output_format: Optional[str] = None
) -> str:
    """
    Analyze one or more images with Gemini API.

    Args:
        image_paths: List of image file paths or URLs
        prompt: Question or instruction for the model
        model: Gemini model to use
        output_format: Optional output format (json, markdown, etc.)

    Returns:
        Model response text
    """
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("Error: google-genai package not installed.", file=sys.stderr)
        print("Install with: pip install google-genai", file=sys.stderr)
        sys.exit(1)

    # Find API key
    api_key = find_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY not found.", file=sys.stderr)
        print("Set it using one of these methods:", file=sys.stderr)
        print("  1. export GEMINI_API_KEY='your-key'", file=sys.stderr)
        print("  2. Create .claude/skills/gemini-vision/.env", file=sys.stderr)
        print("  3. Create .env or .gemini_api_key in project root", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Prepare content parts
    contents = []

    # Add prompt first if single image (best practice)
    if len(image_paths) == 1:
        contents.append(prompt)

    # Add images
    for path in image_paths:
        if path.startswith('file://'):
            # File API reference
            file_id = path[7:]  # Remove 'file://' prefix
            contents.append(types.File(name=file_id))
        elif path.startswith('http://') or path.startswith('https://'):
            # URL - download and convert to bytes
            import requests
            response = requests.get(path)
            response.raise_for_status()

            # Detect MIME type from content-type header or extension
            content_type = response.headers.get('content-type', '').split(';')[0]
            if not content_type or content_type == 'application/octet-stream':
                # Fallback to extension
                ext = Path(path).suffix.lower()
                mime_types = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.webp': 'image/webp',
                    '.heic': 'image/heic',
                    '.heif': 'image/heif',
                    '.pdf': 'application/pdf'
                }
                content_type = mime_types.get(ext, 'image/jpeg')

            contents.append(types.Part.from_bytes(
                data=response.content,
                mime_type=content_type
            ))
        else:
            # Local file
            path_obj = Path(path)
            if not path_obj.exists():
                print(f"Error: File not found: {path}", file=sys.stderr)
                sys.exit(1)

            # Read file
            with open(path, 'rb') as f:
                image_bytes = f.read()

            # Detect MIME type from extension
            ext = path_obj.suffix.lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.webp': 'image/webp',
                '.heic': 'image/heic',
                '.heif': 'image/heif',
                '.pdf': 'application/pdf'
            }
            mime_type = mime_types.get(ext, 'image/jpeg')

            contents.append(types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            ))

    # Add prompt after images for multi-image (best practice)
    if len(image_paths) > 1:
        contents.append(prompt)

    # Generate response
    try:
        response = client.models.generate_content(
            model=model,
            contents=contents
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze images using Google Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single image
  %(prog)s image.jpg "What's in this image?"

  # Multiple images
  %(prog)s img1.jpg img2.jpg "What's different?"

  # From URL
  %(prog)s https://example.com/img.jpg "Describe this"

  # Use uploaded file
  %(prog)s file://file-id "Caption this"

  # Specify model
  %(prog)s image.jpg "Detect objects" --model gemini-2.0-flash

  # Request JSON output
  %(prog)s image.jpg "List objects as JSON" --format json
        """
    )

    parser.add_argument(
        'images',
        nargs='+',
        help='Image file paths, URLs, or file:// references'
    )

    parser.add_argument(
        'prompt',
        help='Question or instruction for the model'
    )

    parser.add_argument(
        '--model',
        default='gemini-2.5-flash',
        choices=[
            'gemini-2.5-pro',
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-pro',
            'gemini-1.5-flash'
        ],
        help='Gemini model to use (default: gemini-2.5-flash)'
    )

    parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'plain'],
        help='Preferred output format'
    )

    args = parser.parse_args()

    # Enhance prompt with format request if specified
    prompt = args.prompt
    if args.format:
        format_instructions = {
            'json': ' Return the response as valid JSON.',
            'markdown': ' Return the response as markdown.',
            'plain': ' Return the response as plain text.'
        }
        prompt += format_instructions.get(args.format, '')

    # Analyze images
    result = analyze_image(
        image_paths=args.images,
        prompt=prompt,
        model=args.model,
        output_format=args.format
    )

    print(result)


if __name__ == '__main__':
    main()
