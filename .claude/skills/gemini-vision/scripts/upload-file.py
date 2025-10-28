#!/usr/bin/env python3
"""
Gemini Vision API - File Upload Script

Upload files to the Gemini File API for reuse across multiple requests.
Files uploaded via the API are automatically deleted after 48 hours.

API Key Lookup Order:
1. Process environment variable (GEMINI_API_KEY)
2. Skill directory (.claude/skills/gemini-vision/.env)
3. Project directory (.env or .gemini_api_key)
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

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
    skill_dir = Path(__file__).parent.parent
    skill_env = skill_dir / '.env'

    if skill_env.exists():
        with open(skill_env, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"\'')

    # Step 3: Check project directory
    project_dir = skill_dir.parent.parent.parent

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


def upload_file(file_path: str, display_name: Optional[str] = None) -> dict:
    """
    Upload a file to Gemini File API.

    Args:
        file_path: Path to the file to upload
        display_name: Optional display name for the file

    Returns:
        Dictionary with file metadata
    """
    try:
        from google import genai
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

    # Check file exists
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    client = genai.Client(api_key=api_key)

    try:
        # Upload file
        print(f"Uploading {file_path}...", file=sys.stderr)

        uploaded_file = client.files.upload(
            file=file_path,
            name=display_name
        )

        # Return file metadata
        return {
            'name': uploaded_file.name,
            'display_name': uploaded_file.display_name,
            'mime_type': uploaded_file.mime_type,
            'size_bytes': uploaded_file.size_bytes,
            'uri': uploaded_file.uri,
            'state': uploaded_file.state,
        }
    except Exception as e:
        print(f"Error uploading file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Upload files to Gemini File API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload a file
  %(prog)s image.jpg

  # Upload with custom display name
  %(prog)s image.jpg --name "My Image"

  # Upload PDF
  %(prog)s document.pdf --name "Report"

Notes:
  - Files are automatically deleted after 48 hours
  - Use the returned file ID with analyze-image.py: file://file-id
  - Maximum file size depends on your API tier
        """
    )

    parser.add_argument(
        'file',
        help='Path to file to upload'
    )

    parser.add_argument(
        '--name',
        help='Display name for the uploaded file'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON instead of human-readable format'
    )

    args = parser.parse_args()

    # Upload file
    file_info = upload_file(args.file, args.name)

    if args.json:
        import json
        print(json.dumps(file_info, indent=2))
    else:
        print(f"\nFile uploaded successfully!", file=sys.stderr)
        print(f"File ID: {file_info['name']}")
        print(f"Display Name: {file_info['display_name']}")
        print(f"MIME Type: {file_info['mime_type']}")
        print(f"Size: {file_info['size_bytes']} bytes")
        print(f"State: {file_info['state']}")
        print(f"\nUse with analyze-image.py:")
        print(f"  python analyze-image.py file://{file_info['name']} \"Your prompt\"")


if __name__ == '__main__':
    main()
