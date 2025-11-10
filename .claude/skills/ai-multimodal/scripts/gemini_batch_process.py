#!/usr/bin/env python3
"""
Batch process multiple media files using Gemini API.

Supports all Gemini modalities:
- Audio: Transcription, analysis, summarization
- Image: Captioning, detection, OCR, analysis
- Video: Summarization, Q&A, scene detection
- Document: PDF extraction, structured output
- Generation: Image creation from text prompts
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import csv
import shutil

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed")
    print("Install with: pip install google-genai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


def find_api_key() -> Optional[str]:
    """Find Gemini API key using correct priority order.

    Priority order (highest to lowest):
    1. process.env (runtime environment variables)
    2. .claude/skills/ai-multimodal/.env (skill-specific config)
    3. .claude/skills/.env (shared skills config)
    4. .claude/.env (Claude global config)
    """
    # Priority 1: Already in process.env (highest)
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        return api_key

    # Load .env files if dotenv available
    if load_dotenv:
        # Determine base paths
        script_dir = Path(__file__).parent
        skill_dir = script_dir.parent  # .claude/skills/ai-multimodal
        skills_dir = skill_dir.parent   # .claude/skills
        claude_dir = skills_dir.parent  # .claude

        # Priority 2: Skill-specific .env
        env_file = skill_dir / '.env'
        if env_file.exists():
            load_dotenv(env_file)
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                return api_key

        # Priority 3: Shared skills .env
        env_file = skills_dir / '.env'
        if env_file.exists():
            load_dotenv(env_file)
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                return api_key

        # Priority 4: Claude global .env
        env_file = claude_dir / '.env'
        if env_file.exists():
            load_dotenv(env_file)
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                return api_key

    return None


def get_mime_type(file_path: str) -> str:
    """Determine MIME type from file extension."""
    ext = Path(file_path).suffix.lower()

    mime_types = {
        # Audio
        '.mp3': 'audio/mp3',
        '.wav': 'audio/wav',
        '.aac': 'audio/aac',
        '.flac': 'audio/flac',
        '.ogg': 'audio/ogg',
        '.aiff': 'audio/aiff',
        # Image
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.webp': 'image/webp',
        '.heic': 'image/heic',
        '.heif': 'image/heif',
        # Video
        '.mp4': 'video/mp4',
        '.mpeg': 'video/mpeg',
        '.mov': 'video/quicktime',
        '.avi': 'video/x-msvideo',
        '.flv': 'video/x-flv',
        '.mpg': 'video/mpeg',
        '.webm': 'video/webm',
        '.wmv': 'video/x-ms-wmv',
        '.3gpp': 'video/3gpp',
        # Document
        '.pdf': 'application/pdf',
        '.txt': 'text/plain',
        '.html': 'text/html',
        '.md': 'text/markdown',
    }

    return mime_types.get(ext, 'application/octet-stream')


def upload_file(client: genai.Client, file_path: str, verbose: bool = False) -> Any:
    """Upload file to Gemini File API."""
    if verbose:
        print(f"Uploading {file_path}...")

    myfile = client.files.upload(file=file_path)

    # Wait for processing (video/audio files need processing)
    mime_type = get_mime_type(file_path)
    if mime_type.startswith('video/') or mime_type.startswith('audio/'):
        max_wait = 300  # 5 minutes
        elapsed = 0
        while myfile.state.name == 'PROCESSING' and elapsed < max_wait:
            time.sleep(2)
            myfile = client.files.get(name=myfile.name)
            elapsed += 2
            if verbose and elapsed % 10 == 0:
                print(f"  Processing... {elapsed}s")

        if myfile.state.name == 'FAILED':
            raise ValueError(f"File processing failed: {file_path}")

        if myfile.state.name == 'PROCESSING':
            raise TimeoutError(f"Processing timeout after {max_wait}s: {file_path}")

    if verbose:
        print(f"  Uploaded: {myfile.name}")

    return myfile


def process_file(
    client: genai.Client,
    file_path: Optional[str],
    prompt: str,
    model: str,
    task: str,
    format_output: str,
    aspect_ratio: Optional[str] = None,
    verbose: bool = False,
    max_retries: int = 3
) -> Dict[str, Any]:
    """Process a single file with retry logic."""

    for attempt in range(max_retries):
        try:
            # For generation tasks without input files
            if task == 'generate' and not file_path:
                content = [prompt]
            else:
                # Process input file
                file_path = Path(file_path)
                # Determine if we need File API
                file_size = file_path.stat().st_size
                use_file_api = file_size > 20 * 1024 * 1024  # >20MB

                if use_file_api:
                    # Upload to File API
                    myfile = upload_file(client, str(file_path), verbose)
                    content = [prompt, myfile]
                else:
                    # Inline data
                    with open(file_path, 'rb') as f:
                        file_bytes = f.read()

                    mime_type = get_mime_type(str(file_path))
                    content = [
                        prompt,
                        types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
                    ]

            # Configure request
            config_args = {}
            if task == 'generate':
                config_args['response_modalities'] = ['Image']  # Capital I per API spec
                if aspect_ratio:
                    # Nest aspect_ratio in image_config per API spec
                    config_args['image_config'] = types.ImageConfig(
                        aspect_ratio=aspect_ratio
                    )

            if format_output == 'json':
                config_args['response_mime_type'] = 'application/json'

            config = types.GenerateContentConfig(**config_args) if config_args else None

            # Generate content
            response = client.models.generate_content(
                model=model,
                contents=content,
                config=config
            )

            # Extract response
            result = {
                'file': str(file_path) if file_path else 'generated',
                'status': 'success',
                'response': response.text if hasattr(response, 'text') else None
            }

            # Handle image output
            if task == 'generate' and hasattr(response, 'candidates'):
                for i, part in enumerate(response.candidates[0].content.parts):
                    if part.inline_data:
                        # Determine output directory - use project root docs/assets
                        if file_path:
                            output_dir = Path(file_path).parent
                            base_name = Path(file_path).stem
                        else:
                            # Find project root (look for .git or .claude directory)
                            script_dir = Path(__file__).parent
                            project_root = script_dir
                            for parent in [script_dir] + list(script_dir.parents):
                                if (parent / '.git').exists() or (parent / '.claude').exists():
                                    project_root = parent
                                    break

                            output_dir = project_root / 'docs' / 'assets'
                            output_dir.mkdir(parents=True, exist_ok=True)
                            base_name = "generated"

                        output_file = output_dir / f"{base_name}_generated_{i}.png"
                        with open(output_file, 'wb') as f:
                            f.write(part.inline_data.data)
                        result['generated_image'] = str(output_file)
                        if verbose:
                            print(f"  Saved image to: {output_file}")

            return result

        except Exception as e:
            if attempt == max_retries - 1:
                return {
                    'file': str(file_path) if file_path else 'generated',
                    'status': 'error',
                    'error': str(e)
                }

            wait_time = 2 ** attempt
            if verbose:
                print(f"  Retry {attempt + 1} after {wait_time}s: {e}")
            time.sleep(wait_time)


def batch_process(
    files: List[str],
    prompt: str,
    model: str,
    task: str,
    format_output: str,
    aspect_ratio: Optional[str] = None,
    output_file: Optional[str] = None,
    verbose: bool = False,
    dry_run: bool = False
) -> List[Dict[str, Any]]:
    """Batch process multiple files."""
    api_key = find_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY not found")
        print("Set via: export GEMINI_API_KEY='your-key'")
        print("Or create .env file with: GEMINI_API_KEY=your-key")
        sys.exit(1)

    if dry_run:
        print("DRY RUN MODE - No API calls will be made")
        print(f"Files to process: {len(files)}")
        print(f"Model: {model}")
        print(f"Task: {task}")
        print(f"Prompt: {prompt}")
        return []

    client = genai.Client(api_key=api_key)
    results = []

    # For generation tasks without input files, process once
    if task == 'generate' and not files:
        if verbose:
            print(f"\nGenerating image from prompt...")

        result = process_file(
            client=client,
            file_path=None,
            prompt=prompt,
            model=model,
            task=task,
            format_output=format_output,
            aspect_ratio=aspect_ratio,
            verbose=verbose
        )

        results.append(result)

        if verbose:
            status = result.get('status', 'unknown')
            print(f"  Status: {status}")
    else:
        # Process input files
        for i, file_path in enumerate(files, 1):
            if verbose:
                print(f"\n[{i}/{len(files)}] Processing: {file_path}")

            result = process_file(
                client=client,
                file_path=file_path,
                prompt=prompt,
                model=model,
                task=task,
                format_output=format_output,
                aspect_ratio=aspect_ratio,
                verbose=verbose
            )

            results.append(result)

            if verbose:
                status = result.get('status', 'unknown')
                print(f"  Status: {status}")

    # Save results
    if output_file:
        save_results(results, output_file, format_output)

    return results


def save_results(results: List[Dict[str, Any]], output_file: str, format_output: str):
    """Save results to file."""
    output_path = Path(output_file)

    # Special handling for image generation - if output has image extension, copy the generated image
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}
    if output_path.suffix.lower() in image_extensions and len(results) == 1:
        generated_image = results[0].get('generated_image')
        if generated_image:
            # Copy the generated image to the specified output location
            shutil.copy2(generated_image, output_path)
            return
        else:
            # Don't write text reports to image files - save error as .txt instead
            output_path = output_path.with_suffix('.error.txt')
            print(f"Warning: Generation failed, saving error report to: {output_path}")

    if format_output == 'json':
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
    elif format_output == 'csv':
        with open(output_path, 'w', newline='') as f:
            fieldnames = ['file', 'status', 'response', 'error']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow({
                    'file': result.get('file', ''),
                    'status': result.get('status', ''),
                    'response': result.get('response', ''),
                    'error': result.get('error', '')
                })
    else:  # markdown
        with open(output_path, 'w') as f:
            f.write("# Batch Processing Results\n\n")
            for i, result in enumerate(results, 1):
                f.write(f"## {i}. {result.get('file', 'Unknown')}\n\n")
                f.write(f"**Status**: {result.get('status', 'unknown')}\n\n")
                if result.get('response'):
                    f.write(f"**Response**:\n\n{result['response']}\n\n")
                if result.get('error'):
                    f.write(f"**Error**: {result['error']}\n\n")


def main():
    parser = argparse.ArgumentParser(
        description='Batch process media files with Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transcribe multiple audio files
  %(prog)s --files *.mp3 --task transcribe --model gemini-2.5-flash

  # Analyze images
  %(prog)s --files *.jpg --task analyze --prompt "Describe this image" \\
    --model gemini-2.5-flash

  # Process PDFs to JSON
  %(prog)s --files *.pdf --task extract --prompt "Extract data as JSON" \\
    --format json --output results.json

  # Generate images
  %(prog)s --task generate --prompt "A mountain landscape" \\
    --model gemini-2.5-flash-image --aspect-ratio 16:9
        """
    )

    parser.add_argument('--files', nargs='*', help='Input files to process')
    parser.add_argument('--task', required=True,
                       choices=['transcribe', 'analyze', 'extract', 'generate'],
                       help='Task to perform')
    parser.add_argument('--prompt', help='Prompt for analysis/generation')
    parser.add_argument('--model', default='gemini-2.5-flash',
                       help='Gemini model to use (default: gemini-2.5-flash)')
    parser.add_argument('--format', dest='format_output', default='text',
                       choices=['text', 'json', 'csv', 'markdown'],
                       help='Output format (default: text)')
    parser.add_argument('--aspect-ratio', choices=['1:1', '16:9', '9:16', '4:3', '3:4'],
                       help='Aspect ratio for image generation')
    parser.add_argument('--output', help='Output file for results')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making API calls')

    args = parser.parse_args()

    # Validate arguments
    if args.task != 'generate' and not args.files:
        parser.error("--files required for non-generation tasks")

    if args.task == 'generate' and not args.prompt:
        parser.error("--prompt required for generation task")

    if args.task != 'generate' and not args.prompt:
        # Set default prompts
        if args.task == 'transcribe':
            args.prompt = 'Generate a transcript with timestamps'
        elif args.task == 'analyze':
            args.prompt = 'Analyze this content'
        elif args.task == 'extract':
            args.prompt = 'Extract key information'

    # Process files
    files = args.files or []
    results = batch_process(
        files=files,
        prompt=args.prompt,
        model=args.model,
        task=args.task,
        format_output=args.format_output,
        aspect_ratio=args.aspect_ratio,
        output_file=args.output,
        verbose=args.verbose,
        dry_run=args.dry_run
    )

    # Print summary
    if not args.dry_run and results:
        success = sum(1 for r in results if r.get('status') == 'success')
        failed = len(results) - success
        print(f"\n{'='*50}")
        print(f"Processed: {len(results)} files")
        print(f"Success: {success}")
        print(f"Failed: {failed}")
        if args.output:
            print(f"Results saved to: {args.output}")


if __name__ == '__main__':
    main()
