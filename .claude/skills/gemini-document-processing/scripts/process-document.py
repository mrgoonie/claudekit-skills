#!/usr/bin/env python3
"""
Gemini Document Processing Script

Process PDF documents using Google Gemini API with multi-source API key checking.
API key priority: process env -> skill directory -> project directory
"""

import os
import sys
import argparse
import base64
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed")
    print("Install with: pip install google-genai")
    sys.exit(1)


def find_api_key() -> Optional[str]:
    """
    Find GEMINI_API_KEY from multiple sources in priority order:
    1. Process environment variable
    2. .env file in skill directory
    3. .env file in project root

    Returns:
        API key string or None if not found
    """
    # Priority 1: Check process environment
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✓ API key found in environment variable", file=sys.stderr)
        return api_key

    # Priority 2: Check skill directory .env
    skill_dir = Path(__file__).parent.parent
    skill_env = skill_dir / '.env'
    if skill_env.exists():
        load_dotenv(skill_env)
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print(f"✓ API key found in skill directory: {skill_env}", file=sys.stderr)
            return api_key

    # Priority 3: Check project root .env
    project_root = skill_dir.parent.parent.parent  # Go up from .claude/skills/gemini-document-processing
    project_env = project_root / '.env'
    if project_env.exists():
        load_dotenv(project_env)
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print(f"✓ API key found in project root: {project_env}", file=sys.stderr)
            return api_key

    return None


def process_document(
    file_path: str,
    prompt: str,
    model: str = 'gemini-2.5-flash',
    use_file_api: bool = False,
    output_format: str = 'text'
) -> str:
    """
    Process a PDF document with Gemini API

    Args:
        file_path: Path to PDF file
        prompt: Text prompt for processing
        model: Gemini model to use
        use_file_api: Whether to use File API (for large files)
        output_format: Output format ('text' or 'json')

    Returns:
        Response text from Gemini
    """
    # Check API key
    api_key = find_api_key()
    if not api_key:
        print("\nError: GEMINI_API_KEY not found", file=sys.stderr)
        print("\nPlease set API key using one of these methods:", file=sys.stderr)
        print("1. Environment variable: export GEMINI_API_KEY='your-key'", file=sys.stderr)
        print("2. Skill directory: echo 'GEMINI_API_KEY=your-key' > .claude/skills/gemini-document-processing/.env", file=sys.stderr)
        print("3. Project root: echo 'GEMINI_API_KEY=your-key' > .env", file=sys.stderr)
        print("\nGet API key at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Check file exists and is PDF
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    if file_path_obj.suffix.lower() != '.pdf':
        print(f"Warning: File is not a PDF. Vision processing only works with PDFs.", file=sys.stderr)

    # Read file
    with open(file_path, 'rb') as f:
        file_data = f.read()

    file_size_mb = len(file_data) / (1024 * 1024)
    print(f"Processing: {file_path} ({file_size_mb:.2f} MB)", file=sys.stderr)

    # Use File API for large files or if explicitly requested
    if use_file_api or file_size_mb > 20:
        if file_size_mb > 20:
            print(f"File > 20MB, using File API", file=sys.stderr)

        print("Uploading file...", file=sys.stderr)
        uploaded_file = client.files.upload(path=file_path)
        print(f"File uploaded: {uploaded_file.name}", file=sys.stderr)

        # Wait for processing
        import time
        while uploaded_file.state == 'PROCESSING':
            print("Processing file...", file=sys.stderr)
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state == 'FAILED':
            print(f"Error: File processing failed", file=sys.stderr)
            sys.exit(1)

        print(f"File ready: {uploaded_file.state}", file=sys.stderr)

        # Generate content with uploaded file
        contents = [prompt, uploaded_file]
    else:
        # Use inline encoding
        print("Using inline encoding", file=sys.stderr)
        contents = [
            prompt,
            types.Part.from_bytes(
                data=file_data,
                mime_type='application/pdf'
            )
        ]

    # Configure output format
    config = None
    if output_format == 'json':
        config = types.GenerateContentConfig(
            response_mime_type='application/json'
        )

    # Generate content
    print(f"Generating content with {model}...", file=sys.stderr)
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config
    )

    return response.text


def main():
    parser = argparse.ArgumentParser(
        description='Process PDF documents with Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python process-document.py --file invoice.pdf --prompt "Extract invoice details"

  # JSON output
  python process-document.py --file invoice.pdf --prompt "Extract data" --format json

  # Large file with File API
  python process-document.py --file large-doc.pdf --prompt "Summarize" --use-file-api

  # Multiple prompts
  python process-document.py --file doc.pdf --prompt "Q1" --prompt "Q2"
        """
    )

    parser.add_argument('--file', '-f', required=True, help='Path to PDF file')
    parser.add_argument('--prompt', '-p', action='append', required=True,
                       help='Text prompt (can specify multiple times)')
    parser.add_argument('--model', '-m', default='gemini-2.5-flash',
                       help='Gemini model to use (default: gemini-2.5-flash)')
    parser.add_argument('--use-file-api', action='store_true',
                       help='Use File API (for files > 20MB or repeated queries)')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')

    args = parser.parse_args()

    # Process each prompt
    for i, prompt in enumerate(args.prompt, 1):
        if len(args.prompt) > 1:
            print(f"\n{'='*60}", file=sys.stderr)
            print(f"Prompt {i}/{len(args.prompt)}: {prompt}", file=sys.stderr)
            print(f"{'='*60}\n", file=sys.stderr)

        result = process_document(
            file_path=args.file,
            prompt=prompt,
            model=args.model,
            use_file_api=args.use_file_api,
            output_format=args.format
        )

        if len(args.prompt) > 1:
            print(f"\n--- Result {i} ---")
        print(result)
        print()


if __name__ == '__main__':
    main()
