#!/usr/bin/env python3
"""
Gemini Audio Files Management Tool

Manage audio files uploaded to Gemini API (Files API).

Usage:
    python manage-files.py list
    python manage-files.py get <file-id>
    python manage-files.py delete <file-id>
    python manage-files.py upload audio.mp3
    python manage-files.py cleanup  # Delete all files
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from google import genai
from api_key_helper import get_api_key_or_exit


def list_files(client: genai.Client):
    """List all uploaded files"""
    print("\n📁 Uploaded Files:", file=sys.stderr)
    print("="*80, file=sys.stderr)

    files = list(client.files.list())

    if not files:
        print("No files found.", file=sys.stderr)
        return

    for file in files:
        # Parse creation time
        create_time = file.create_time
        if hasattr(create_time, 'isoformat'):
            create_str = create_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            create_str = str(create_time)

        print(f"\nName: {file.name}", file=sys.stderr)
        print(f"Display Name: {file.display_name}", file=sys.stderr)
        print(f"URI: {file.uri}", file=sys.stderr)
        print(f"MIME Type: {file.mime_type}", file=sys.stderr)
        print(f"Size: {file.size_bytes:,} bytes", file=sys.stderr)
        print(f"Created: {create_str}", file=sys.stderr)
        print(f"State: {file.state}", file=sys.stderr)

    print(f"\nTotal files: {len(files)}", file=sys.stderr)


def get_file_info(client: genai.Client, file_id: str):
    """Get detailed info about a specific file"""
    try:
        file = client.files.get(name=file_id)

        print("\n📄 File Details:", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print(f"Name: {file.name}", file=sys.stderr)
        print(f"Display Name: {file.display_name}", file=sys.stderr)
        print(f"URI: {file.uri}", file=sys.stderr)
        print(f"MIME Type: {file.mime_type}", file=sys.stderr)
        print(f"Size: {file.size_bytes:,} bytes", file=sys.stderr)
        print(f"State: {file.state}", file=sys.stderr)

        if hasattr(file, 'create_time'):
            create_time = file.create_time
            if hasattr(create_time, 'isoformat'):
                print(f"Created: {create_time.strftime('%Y-%m-%d %H:%M:%S')}", file=sys.stderr)

        if hasattr(file, 'expiration_time'):
            exp_time = file.expiration_time
            if hasattr(exp_time, 'isoformat'):
                print(f"Expires: {exp_time.strftime('%Y-%m-%d %H:%M:%S')}", file=sys.stderr)

    except Exception as e:
        print(f"❌ Error getting file info: {e}", file=sys.stderr)
        sys.exit(1)


def delete_file(client: genai.Client, file_id: str):
    """Delete a specific file"""
    try:
        client.files.delete(name=file_id)
        print(f"✓ Deleted file: {file_id}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Error deleting file: {e}", file=sys.stderr)
        sys.exit(1)


def upload_file(client: genai.Client, file_path: str):
    """Upload audio file to Files API"""
    if not Path(file_path).exists():
        print(f"❌ Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    print(f"📤 Uploading {file_path}...", file=sys.stderr)

    try:
        uploaded_file = client.files.upload(file=file_path)

        print("\n✓ Upload successful!", file=sys.stderr)
        print(f"Name: {uploaded_file.name}", file=sys.stderr)
        print(f"URI: {uploaded_file.uri}", file=sys.stderr)
        print(f"MIME Type: {uploaded_file.mime_type}", file=sys.stderr)
        print(f"Size: {uploaded_file.size_bytes:,} bytes", file=sys.stderr)

        return uploaded_file

    except Exception as e:
        print(f"❌ Error uploading file: {e}", file=sys.stderr)
        sys.exit(1)


def cleanup_all_files(client: genai.Client):
    """Delete all uploaded files"""
    files = list(client.files.list())

    if not files:
        print("No files to clean up.", file=sys.stderr)
        return

    print(f"⚠️  Deleting {len(files)} file(s)...", file=sys.stderr)

    for file in files:
        try:
            client.files.delete(name=file.name)
            print(f"✓ Deleted: {file.name}", file=sys.stderr)
        except Exception as e:
            print(f"❌ Error deleting {file.name}: {e}", file=sys.stderr)

    print(f"\n✓ Cleanup complete!", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Manage audio files in Gemini Files API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all uploaded files
  python manage-files.py list

  # Get file details
  python manage-files.py get files/abc123

  # Upload new file
  python manage-files.py upload audio.mp3

  # Delete specific file
  python manage-files.py delete files/abc123

  # Delete all files
  python manage-files.py cleanup
        """
    )

    parser.add_argument(
        'command',
        choices=['list', 'get', 'delete', 'upload', 'cleanup'],
        help='Command to execute'
    )

    parser.add_argument(
        'argument',
        nargs='?',
        help='File ID (for get/delete) or file path (for upload)'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.command in ['get', 'delete', 'upload'] and not args.argument:
        print(f"Error: {args.command} requires an argument", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Get API key and create client
    api_key = get_api_key_or_exit()
    client = genai.Client(api_key=api_key)

    # Execute command
    try:
        if args.command == 'list':
            list_files(client)
        elif args.command == 'get':
            get_file_info(client, args.argument)
        elif args.command == 'delete':
            delete_file(client, args.argument)
        elif args.command == 'upload':
            upload_file(client, args.argument)
        elif args.command == 'cleanup':
            cleanup_all_files(client)

    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
