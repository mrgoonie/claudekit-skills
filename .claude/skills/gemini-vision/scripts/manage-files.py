#!/usr/bin/env python3
"""
Gemini Vision API - File Management Script

Manage files uploaded to the Gemini File API:
- List all uploaded files
- Get file metadata
- Delete files

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


def get_client():
    """Get authenticated Gemini client."""
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

    return genai.Client(api_key=api_key)


def list_files(json_output: bool = False):
    """List all uploaded files."""
    client = get_client()

    try:
        files = client.files.list()

        if json_output:
            import json
            file_list = []
            for file in files:
                file_list.append({
                    'name': file.name,
                    'display_name': file.display_name,
                    'mime_type': file.mime_type,
                    'size_bytes': file.size_bytes,
                    'state': file.state,
                })
            print(json.dumps(file_list, indent=2))
        else:
            file_count = 0
            for file in files:
                file_count += 1
                print(f"\n{file_count}. {file.display_name or file.name}")
                print(f"   ID: {file.name}")
                print(f"   MIME: {file.mime_type}")
                print(f"   Size: {file.size_bytes} bytes")
                print(f"   State: {file.state}")

            if file_count == 0:
                print("No files found.")
            else:
                print(f"\nTotal files: {file_count}")

    except Exception as e:
        print(f"Error listing files: {e}", file=sys.stderr)
        sys.exit(1)


def get_file(file_id: str, json_output: bool = False):
    """Get file metadata."""
    client = get_client()

    try:
        file = client.files.get(name=file_id)

        if json_output:
            import json
            file_info = {
                'name': file.name,
                'display_name': file.display_name,
                'mime_type': file.mime_type,
                'size_bytes': file.size_bytes,
                'uri': file.uri,
                'state': file.state,
            }
            print(json.dumps(file_info, indent=2))
        else:
            print(f"File: {file.display_name or file.name}")
            print(f"ID: {file.name}")
            print(f"MIME Type: {file.mime_type}")
            print(f"Size: {file.size_bytes} bytes")
            print(f"URI: {file.uri}")
            print(f"State: {file.state}")

    except Exception as e:
        print(f"Error getting file: {e}", file=sys.stderr)
        sys.exit(1)


def delete_file(file_id: str):
    """Delete a file."""
    client = get_client()

    try:
        client.files.delete(name=file_id)
        print(f"File deleted successfully: {file_id}")

    except Exception as e:
        print(f"Error deleting file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Manage files in Gemini File API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all files
  %(prog)s list

  # Get file metadata
  %(prog)s get files/abc123

  # Delete a file
  %(prog)s delete files/abc123

  # Output as JSON
  %(prog)s list --json
  %(prog)s get files/abc123 --json
        """
    )

    parser.add_argument(
        'action',
        choices=['list', 'get', 'delete'],
        help='Action to perform'
    )

    parser.add_argument(
        'file_id',
        nargs='?',
        help='File ID (required for get and delete)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    # Validate file_id for get and delete
    if args.action in ['get', 'delete'] and not args.file_id:
        parser.error(f"file_id is required for {args.action} action")

    # Execute action
    if args.action == 'list':
        list_files(args.json)
    elif args.action == 'get':
        get_file(args.file_id, args.json)
    elif args.action == 'delete':
        delete_file(args.file_id)


if __name__ == '__main__':
    main()
