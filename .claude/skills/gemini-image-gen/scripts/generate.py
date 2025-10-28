#!/usr/bin/env python3
"""
Gemini Image Generation Helper Script

This script generates images using Google's Gemini 2.5 Flash Image model
with automatic API key detection and file saving to ./docs/assets/

Usage:
    python generate.py "Your prompt here" [options]

Examples:
    python generate.py "A serene mountain landscape"
    python generate.py "Futuristic city" --aspect-ratio 16:9 --output city.png
    python generate.py "Modern design" --response-modalities image text
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed")
    print("Install with: pip install google-genai")
    sys.exit(1)


def find_api_key() -> Optional[str]:
    """
    Find GEMINI_API_KEY in this order:
    1. Process environment
    2. Skill directory .env file
    3. Project directory .env file

    Returns:
        API key string or None if not found
    """
    # 1. Check process environment
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✓ API key found in process environment")
        return api_key

    # 2. Check skill directory .env
    skill_dir = Path(__file__).parent.parent
    skill_env = skill_dir / '.env'
    if skill_env.exists():
        api_key = load_env_file(skill_env)
        if api_key:
            print(f"✓ API key found in skill directory: {skill_env}")
            return api_key

    # 3. Check project directory .env
    project_dir = skill_dir.parent.parent.parent  # Go up to project root
    project_env = project_dir / '.env'
    if project_env.exists():
        api_key = load_env_file(project_env)
        if api_key:
            print(f"✓ API key found in project directory: {project_env}")
            return api_key

    return None


def load_env_file(env_path: Path) -> Optional[str]:
    """
    Load GEMINI_API_KEY from .env file

    Args:
        env_path: Path to .env file

    Returns:
        API key string or None
    """
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GEMINI_API_KEY='):
                    # Remove quotes if present
                    key = line.split('=', 1)[1].strip()
                    key = key.strip('"').strip("'")
                    return key if key else None
    except Exception as e:
        print(f"Warning: Error reading {env_path}: {e}")

    return None


def generate_image(
    prompt: str,
    api_key: str,
    aspect_ratio: str = '1:1',
    response_modalities: List[str] = None,
    output_path: Optional[str] = None,
    model: str = 'gemini-2.5-flash-image'
) -> bool:
    """
    Generate image using Gemini API

    Args:
        prompt: Text description of image to generate
        api_key: Gemini API key
        aspect_ratio: Image aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4)
        response_modalities: List of modalities (image, text)
        output_path: Optional custom output path
        model: Model name to use

    Returns:
        True if successful, False otherwise
    """
    if response_modalities is None:
        response_modalities = ['image']

    print(f"\n🎨 Generating image with Gemini...")
    print(f"   Model: {model}")
    print(f"   Prompt: {prompt}")
    print(f"   Aspect ratio: {aspect_ratio}")
    print(f"   Response modalities: {', '.join(response_modalities)}")

    try:
        # Initialize client
        client = genai.Client(api_key=api_key)

        # Generate content
        config = types.GenerateContentConfig(
            response_modalities=response_modalities,
            aspect_ratio=aspect_ratio
        )

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config
        )

        # Process response
        if not response.candidates:
            print("✗ No candidates in response")
            return False

        candidate = response.candidates[0]

        # Save images
        image_count = 0
        for i, part in enumerate(candidate.content.parts):
            if hasattr(part, 'inline_data') and part.inline_data:
                image_count += 1

                # Determine output path
                if output_path:
                    save_path = Path(output_path)
                else:
                    # Default: ./docs/assets/gemini-YYYYMMDD-HHMMSS-N.png
                    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                    assets_dir = Path('./docs/assets')
                    assets_dir.mkdir(parents=True, exist_ok=True)
                    save_path = assets_dir / f'gemini-{timestamp}-{i}.png'

                # Save image
                save_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(part.inline_data.data)

                print(f"✓ Image saved: {save_path}")

        # Print text if included
        if 'text' in response_modalities:
            text_parts = [p.text for p in candidate.content.parts if hasattr(p, 'text')]
            if text_parts:
                print(f"\n📝 Generated text:")
                for text in text_parts:
                    print(f"   {text}")

        if image_count == 0:
            print("✗ No images generated")
            return False

        print(f"\n✓ Successfully generated {image_count} image(s)")
        return True

    except Exception as e:
        print(f"\n✗ Error generating image: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Generate images using Gemini 2.5 Flash Image model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "A serene mountain landscape"
  %(prog)s "Futuristic city" --aspect-ratio 16:9
  %(prog)s "Modern design" --response-modalities image text
  %(prog)s "Robot" --output ./my-robot.png
        """
    )

    parser.add_argument(
        'prompt',
        help='Text description of image to generate'
    )

    parser.add_argument(
        '--aspect-ratio',
        default='1:1',
        choices=['1:1', '16:9', '9:16', '4:3', '3:4'],
        help='Image aspect ratio (default: 1:1)'
    )

    parser.add_argument(
        '--response-modalities',
        nargs='+',
        default=['image'],
        choices=['image', 'text'],
        help='Response modalities (default: image)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Custom output path (default: ./docs/assets/gemini-TIMESTAMP.png)'
    )

    parser.add_argument(
        '--model',
        default='gemini-2.5-flash-image',
        help='Model to use (default: gemini-2.5-flash-image)'
    )

    args = parser.parse_args()

    # Find API key
    print("🔍 Searching for GEMINI_API_KEY...")
    api_key = find_api_key()

    if not api_key:
        print("\n✗ GEMINI_API_KEY not found!")
        print("\nPlease set your API key in one of these locations:")
        print("  1. Environment variable: export GEMINI_API_KEY='your-key'")
        print("  2. Skill directory: .claude/skills/gemini-image-gen/.env")
        print("  3. Project root: ./.env")
        print("\nGet your API key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    # Generate image
    success = generate_image(
        prompt=args.prompt,
        api_key=api_key,
        aspect_ratio=args.aspect_ratio,
        response_modalities=args.response_modalities,
        output_path=args.output,
        model=args.model
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
