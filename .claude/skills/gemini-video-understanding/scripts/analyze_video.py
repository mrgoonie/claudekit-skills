#!/usr/bin/env python3
"""
Gemini Video Understanding Analysis Script

Analyzes videos using Google's Gemini API with support for:
- Local video files (Files API or inline data)
- YouTube URLs
- Multiple videos
- Video clipping (start/end offsets)
- Custom frame rate sampling
- Multiple models

API Key Configuration:
1. Process environment: $GEMINI_API_KEY
2. Skill directory: .claude/skills/gemini-video-understanding/.env
3. Project root: .env
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, List


def find_api_key() -> Optional[str]:
    """
    Search for GEMINI_API_KEY in priority order:
    1. Process environment variable
    2. Skill directory .env file
    3. Project root .env file
    """
    # 1. Check process environment
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        return api_key

    # 2. Check skill directory .env
    skill_dir = Path(__file__).parent.parent
    skill_env = skill_dir / '.env'
    if skill_env.exists():
        api_key = load_env_file(skill_env, 'GEMINI_API_KEY')
        if api_key:
            return api_key

    # 3. Check project root .env
    # Traverse up to find project root (where .git or .claude exists)
    current = Path.cwd()
    while current != current.parent:
        if (current / '.git').exists() or (current / '.claude').exists():
            project_env = current / '.env'
            if project_env.exists():
                api_key = load_env_file(project_env, 'GEMINI_API_KEY')
                if api_key:
                    return api_key
            break
        current = current.parent

    return None


def load_env_file(env_path: Path, key: str) -> Optional[str]:
    """Load a specific key from .env file"""
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith(f'{key}='):
                    value = line.split('=', 1)[1]
                    # Remove quotes if present
                    value = value.strip('"').strip("'")
                    return value if value else None
    except Exception as e:
        print(f"Warning: Error reading {env_path}: {e}", file=sys.stderr)
    return None


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import google.genai
        return True
    except ImportError:
        print("Error: google-genai package not found", file=sys.stderr)
        print("Install it with: pip install google-genai", file=sys.stderr)
        return False


def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    return os.path.getsize(file_path)


def parse_time_offset(offset: str) -> str:
    """
    Parse time offset to seconds format.
    Accepts: "40s", "1m30s", "1h20m30s"
    Returns: "XXs" format
    """
    # If already in correct format, return as-is
    if offset.endswith('s') and offset[:-1].isdigit():
        return offset

    # Parse complex formats
    total_seconds = 0
    current = ""

    for char in offset:
        if char.isdigit():
            current += char
        elif char in ['h', 'm', 's']:
            if current:
                value = int(current)
                if char == 'h':
                    total_seconds += value * 3600
                elif char == 'm':
                    total_seconds += value * 60
                elif char == 's':
                    total_seconds += value
                current = ""

    return f"{total_seconds}s"


def analyze_video(
    prompt: str,
    video_path: Optional[str] = None,
    youtube_url: Optional[str] = None,
    video_paths: Optional[List[str]] = None,
    model: str = "gemini-2.5-flash",
    start_offset: Optional[str] = None,
    end_offset: Optional[str] = None,
    fps: Optional[int] = None,
    verbose: bool = False
) -> dict:
    """
    Analyze video(s) using Gemini API

    Returns:
        dict with 'text' (response) and 'usage' (token usage) keys
    """
    from google import genai
    from google.genai import types

    # Find API key
    api_key = find_api_key()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Set it in:\n"
            "1. Environment: export GEMINI_API_KEY=your-key\n"
            "2. Skill directory: .claude/skills/gemini-video-understanding/.env\n"
            "3. Project root: .env file\n\n"
            "Get your API key at: https://aistudio.google.com/apikey"
        )

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Prepare video metadata if needed
    video_metadata = None
    if start_offset or end_offset or fps:
        metadata_args = {}
        if start_offset:
            metadata_args['start_offset'] = parse_time_offset(start_offset)
        if end_offset:
            metadata_args['end_offset'] = parse_time_offset(end_offset)
        if fps:
            metadata_args['fps'] = fps
        video_metadata = types.VideoMetadata(**metadata_args)

    # Build content parts
    parts = []

    # Handle multiple videos
    if video_paths:
        if verbose:
            print(f"Processing {len(video_paths)} videos...", file=sys.stderr)

        for vpath in video_paths:
            if not os.path.exists(vpath):
                raise FileNotFoundError(f"Video file not found: {vpath}")

            file_size = get_file_size(vpath)
            use_files_api = file_size > 20 * 1024 * 1024  # 20MB threshold

            if use_files_api:
                if verbose:
                    print(f"Uploading {vpath} via Files API ({file_size / 1024 / 1024:.1f}MB)...", file=sys.stderr)

                myfile = client.files.upload(file=vpath)

                # Wait for file to be processed
                while myfile.state == 'PROCESSING':
                    time.sleep(1)
                    myfile = client.files.get(name=myfile.name)

                if myfile.state == 'FAILED':
                    raise RuntimeError(f"File upload failed for {vpath}")

                if verbose:
                    print(f"File uploaded: {myfile.uri}", file=sys.stderr)

                part_args = {'file_data': types.FileData(file_uri=myfile.uri)}
            else:
                if verbose:
                    print(f"Using inline data for {vpath} ({file_size / 1024 / 1024:.1f}MB)...", file=sys.stderr)

                with open(vpath, 'rb') as f:
                    video_bytes = f.read()

                mime_type = get_mime_type(vpath)
                part_args = {
                    'inline_data': types.Blob(
                        data=video_bytes,
                        mime_type=mime_type
                    )
                }

            if video_metadata:
                part_args['video_metadata'] = video_metadata

            parts.append(types.Part(**part_args))

    # Handle single local video file
    elif video_path:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        file_size = get_file_size(video_path)
        use_files_api = file_size > 20 * 1024 * 1024  # 20MB threshold

        if use_files_api:
            if verbose:
                print(f"Uploading via Files API ({file_size / 1024 / 1024:.1f}MB)...", file=sys.stderr)

            myfile = client.files.upload(file=video_path)

            # Wait for file to be processed
            while myfile.state == 'PROCESSING':
                if verbose:
                    print("Processing...", file=sys.stderr)
                time.sleep(1)
                myfile = client.files.get(name=myfile.name)

            if myfile.state == 'FAILED':
                raise RuntimeError("File upload failed")

            if verbose:
                print(f"File uploaded: {myfile.uri}", file=sys.stderr)

            part_args = {'file_data': types.FileData(file_uri=myfile.uri)}
        else:
            if verbose:
                print(f"Using inline data ({file_size / 1024 / 1024:.1f}MB)...", file=sys.stderr)

            with open(video_path, 'rb') as f:
                video_bytes = f.read()

            mime_type = get_mime_type(video_path)
            part_args = {
                'inline_data': types.Blob(
                    data=video_bytes,
                    mime_type=mime_type
                )
            }

        if video_metadata:
            part_args['video_metadata'] = video_metadata

        parts.append(types.Part(**part_args))

    # Handle YouTube URL
    elif youtube_url:
        if verbose:
            print(f"Processing YouTube URL: {youtube_url}", file=sys.stderr)

        part_args = {'file_data': types.FileData(file_uri=youtube_url)}

        if video_metadata:
            part_args['video_metadata'] = video_metadata

        parts.append(types.Part(**part_args))

    else:
        raise ValueError("Must provide video_path, youtube_url, or video_paths")

    # Add prompt
    parts.append(types.Part(text=prompt))

    # Generate content
    if verbose:
        print(f"Analyzing with {model}...", file=sys.stderr)

    response = client.models.generate_content(
        model=f'models/{model}' if not model.startswith('models/') else model,
        contents=types.Content(parts=parts)
    )

    # Extract response
    result = {
        'text': response.text,
        'usage': {
            'prompt_tokens': getattr(response.usage_metadata, 'prompt_token_count', 0),
            'candidates_tokens': getattr(response.usage_metadata, 'candidates_token_count', 0),
            'total_tokens': getattr(response.usage_metadata, 'total_token_count', 0)
        }
    }

    return result


def get_mime_type(file_path: str) -> str:
    """Get MIME type based on file extension"""
    ext = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.mp4': 'video/mp4',
        '.mpeg': 'video/mpeg',
        '.mov': 'video/mov',
        '.avi': 'video/avi',
        '.flv': 'video/x-flv',
        '.mpg': 'video/mpg',
        '.webm': 'video/webm',
        '.wmv': 'video/wmv',
        '.3gp': 'video/3gpp',
    }
    return mime_types.get(ext, 'video/mp4')


def main():
    parser = argparse.ArgumentParser(
        description='Analyze videos using Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze local video
  %(prog)s --video-path video.mp4 --prompt "Summarize this video"

  # Analyze YouTube video
  %(prog)s --youtube-url "https://youtube.com/watch?v=abc" --prompt "What are the main topics?"

  # Video clipping
  %(prog)s --video-path video.mp4 --prompt "Summarize" --start-offset 40s --end-offset 80s

  # Custom FPS
  %(prog)s --video-path video.mp4 --prompt "Analyze" --fps 5

  # Multiple videos
  %(prog)s --video-paths video1.mp4 video2.mp4 --prompt "Compare these videos"

  # Different model
  %(prog)s --video-path video.mp4 --prompt "Detailed analysis" --model gemini-2.5-pro
        """
    )

    # Video source (mutually exclusive)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--video-path', help='Path to local video file')
    source_group.add_argument('--youtube-url', help='YouTube video URL')
    source_group.add_argument('--video-paths', nargs='+', help='Multiple video paths (Gemini 2.5+)')

    # Required
    parser.add_argument('--prompt', required=True, help='Analysis prompt/question')

    # Optional
    parser.add_argument('--model', default='gemini-2.5-flash',
                       help='Model to use (default: gemini-2.5-flash)')
    parser.add_argument('--start-offset', help='Video clip start (e.g., "40s", "1m30s")')
    parser.add_argument('--end-offset', help='Video clip end (e.g., "80s", "2m")')
    parser.add_argument('--fps', type=int, help='Frame sampling rate (default: 1)')
    parser.add_argument('--output-file', help='Save response to file')
    parser.add_argument('--verbose', action='store_true', help='Show detailed processing info')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    try:
        # Analyze video
        result = analyze_video(
            prompt=args.prompt,
            video_path=args.video_path,
            youtube_url=args.youtube_url,
            video_paths=args.video_paths,
            model=args.model,
            start_offset=args.start_offset,
            end_offset=args.end_offset,
            fps=args.fps,
            verbose=args.verbose
        )

        # Output results
        if args.json:
            output = json.dumps(result, indent=2)
        else:
            output = result['text']
            if args.verbose:
                print(f"\n{'='*60}", file=sys.stderr)
                print(f"Token Usage:", file=sys.stderr)
                print(f"  Prompt: {result['usage']['prompt_tokens']}", file=sys.stderr)
                print(f"  Response: {result['usage']['candidates_tokens']}", file=sys.stderr)
                print(f"  Total: {result['usage']['total_tokens']}", file=sys.stderr)
                print(f"{'='*60}\n", file=sys.stderr)

        # Save to file or print
        if args.output_file:
            with open(args.output_file, 'w') as f:
                f.write(output)
            print(f"Response saved to {args.output_file}", file=sys.stderr)
        else:
            print(output)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
