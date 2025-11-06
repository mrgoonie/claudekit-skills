#!/usr/bin/env python3
"""
Convert documents to PDF for Gemini API processing.

Features:
- Convert DOCX, XLSX, PPTX, HTML, Markdown to PDF
- Extract page ranges from PDFs
- Optimize PDFs for Gemini API
- Extract images from PDFs
- Batch conversion support
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, List

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


def load_env_files():
    """Load .env files in correct priority order.

    Priority order (highest to lowest):
    1. process.env (runtime environment variables)
    2. .claude/skills/ai-multimodal/.env (skill-specific config)
    3. .claude/skills/.env (shared skills config)
    4. .claude/.env (Claude global config)
    """
    if not load_dotenv:
        return

    # Determine base paths
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent  # .claude/skills/ai-multimodal
    skills_dir = skill_dir.parent   # .claude/skills
    claude_dir = skills_dir.parent  # .claude

    # Priority 2: Skill-specific .env
    env_file = skill_dir / '.env'
    if env_file.exists():
        load_dotenv(env_file)

    # Priority 3: Shared skills .env
    env_file = skills_dir / '.env'
    if env_file.exists():
        load_dotenv(env_file)

    # Priority 4: Claude global .env
    env_file = claude_dir / '.env'
    if env_file.exists():
        load_dotenv(env_file)


# Load environment variables at module level
load_env_files()


def check_dependencies() -> dict:
    """Check which conversion libraries are available."""
    deps = {}

    try:
        import pypdf
        deps['pypdf'] = True
    except ImportError:
        deps['pypdf'] = False

    try:
        import docx2pdf
        deps['docx2pdf'] = True
    except ImportError:
        deps['docx2pdf'] = False

    try:
        import markdown
        deps['markdown'] = True
    except ImportError:
        deps['markdown'] = False

    try:
        from PIL import Image
        deps['pillow'] = True
    except ImportError:
        deps['pillow'] = False

    return deps


def extract_pdf_pages(
    input_path: str,
    output_path: str,
    page_range: str,
    verbose: bool = False
) -> bool:
    """Extract specific pages from PDF."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("Error: pypdf not installed")
        print("Install with: pip install pypdf")
        return False

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Parse page range
        if '-' in page_range:
            start, end = page_range.split('-')
            start = int(start) - 1  # 0-indexed
            end = int(end)
            pages = range(start, end)
        else:
            pages = [int(page_range) - 1]

        if verbose:
            print(f"Total pages in PDF: {len(reader.pages)}")
            print(f"Extracting pages: {page_range}")

        for page_num in pages:
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
            else:
                print(f"Warning: Page {page_num + 1} out of range")

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        if verbose:
            print(f"Extracted {len(writer.pages)} pages to {output_path}")

        return True

    except Exception as e:
        print(f"Error extracting pages: {e}")
        return False


def optimize_pdf(
    input_path: str,
    output_path: str,
    verbose: bool = False
) -> bool:
    """Optimize PDF for smaller file size."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("Error: pypdf not installed")
        return False

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Compress
        for page in writer.pages:
            page.compress_content_streams()

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        if verbose:
            input_size = Path(input_path).stat().st_size
            output_size = Path(output_path).stat().st_size
            compression = (1 - output_size / input_size) * 100
            print(f"Input: {input_size / (1024*1024):.2f} MB")
            print(f"Output: {output_size / (1024*1024):.2f} MB")
            print(f"Compression: {compression:.1f}%")

        return True

    except Exception as e:
        print(f"Error optimizing PDF: {e}")
        return False


def extract_images_from_pdf(
    input_path: str,
    output_dir: str,
    verbose: bool = False
) -> List[str]:
    """Extract images from PDF."""
    try:
        from pypdf import PdfReader
        from PIL import Image
        import io
    except ImportError:
        print("Error: pypdf or Pillow not installed")
        print("Install with: pip install pypdf pillow")
        return []

    try:
        reader = PdfReader(input_path)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        extracted_files = []
        image_count = 0

        for page_num, page in enumerate(reader.pages):
            if '/XObject' in page['/Resources']:
                xobjects = page['/Resources']['/XObject'].get_object()

                for obj_name in xobjects:
                    obj = xobjects[obj_name]

                    if obj['/Subtype'] == '/Image':
                        size = (obj['/Width'], obj['/Height'])
                        data = obj.get_data()

                        # Determine format
                        if '/Filter' in obj:
                            filter_type = obj['/Filter']
                            if filter_type == '/DCTDecode':
                                ext = 'jpg'
                            elif filter_type == '/JPXDecode':
                                ext = 'jp2'
                            elif filter_type == '/FlateDecode':
                                ext = 'png'
                            else:
                                ext = 'png'
                        else:
                            ext = 'png'

                        # Save image
                        output_file = output_path / f"page{page_num+1}_img{image_count+1}.{ext}"

                        try:
                            if ext == 'png':
                                img = Image.frombytes('RGB', size, data)
                                img.save(output_file)
                            else:
                                with open(output_file, 'wb') as f:
                                    f.write(data)

                            extracted_files.append(str(output_file))
                            image_count += 1

                            if verbose:
                                print(f"Extracted: {output_file.name}")

                        except Exception as e:
                            if verbose:
                                print(f"Could not extract image: {e}")

        if verbose:
            print(f"\nExtracted {len(extracted_files)} images to {output_dir}")

        return extracted_files

    except Exception as e:
        print(f"Error extracting images: {e}")
        return []


def convert_markdown_to_pdf(
    input_path: str,
    output_path: str,
    verbose: bool = False
) -> bool:
    """Convert Markdown to PDF (requires wkhtmltopdf or similar)."""
    try:
        import markdown
        import subprocess
    except ImportError:
        print("Error: markdown not installed")
        print("Install with: pip install markdown")
        return False

    try:
        # Read markdown
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert to HTML
        html = markdown.markdown(md_content)

        # Wrap in basic HTML structure
        html_full = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                pre {{ background: #f4f4f4; padding: 10px; }}
                code {{ background: #f4f4f4; padding: 2px 5px; }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """

        # Save HTML temporarily
        html_path = Path(output_path).with_suffix('.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_full)

        # Convert to PDF using wkhtmltopdf
        try:
            cmd = ['wkhtmltopdf', str(html_path), output_path]
            subprocess.run(cmd, check=True, capture_output=True)

            # Clean up HTML
            html_path.unlink()

            if verbose:
                print(f"Converted {input_path} to {output_path}")

            return True

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: wkhtmltopdf not found")
            print("Install: apt-get install wkhtmltopdf (Linux) or brew install wkhtmltopdf (Mac)")
            print(f"HTML version saved to: {html_path}")
            return False

    except Exception as e:
        print(f"Error converting markdown: {e}")
        return False


def convert_html_to_pdf(
    input_path: str,
    output_path: str,
    verbose: bool = False
) -> bool:
    """Convert HTML to PDF."""
    try:
        import subprocess
    except ImportError:
        return False

    try:
        cmd = ['wkhtmltopdf', input_path, output_path]
        subprocess.run(cmd, check=True, capture_output=True)

        if verbose:
            print(f"Converted {input_path} to {output_path}")

        return True

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: wkhtmltopdf not found")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert documents to PDF for Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract pages from PDF
  %(prog)s --input document.pdf --output chapter1.pdf --pages 1-20

  # Optimize PDF
  %(prog)s --input large.pdf --output optimized.pdf --optimize

  # Extract images from PDF
  %(prog)s --input document.pdf --extract-images --output-dir ./images

  # Convert Markdown to PDF
  %(prog)s --input README.md --output README.pdf

  # Convert HTML to PDF
  %(prog)s --input page.html --output page.pdf

Note: Some conversions require additional tools:
  - Markdown/HTML to PDF: wkhtmltopdf
  - DOCX to PDF: Microsoft Office or LibreOffice
        """
    )

    parser.add_argument('--input', required=True, help='Input file')
    parser.add_argument('--output', help='Output file or directory')
    parser.add_argument('--pages', help='Page range (e.g., 1-10 or 5)')
    parser.add_argument('--optimize', action='store_true', help='Optimize PDF')
    parser.add_argument('--extract-images', action='store_true', help='Extract images from PDF')
    parser.add_argument('--output-dir', help='Output directory for extracted images')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Check dependencies
    deps = check_dependencies()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    ext = input_path.suffix.lower()

    # Extract images
    if args.extract_images:
        if not deps['pypdf'] or not deps['pillow']:
            print("Error: pypdf and pillow required for image extraction")
            print("Install with: pip install pypdf pillow")
            sys.exit(1)

        output_dir = args.output_dir or './extracted_images'
        images = extract_images_from_pdf(str(input_path), output_dir, args.verbose)
        sys.exit(0 if images else 1)

    # Require output for other operations
    if not args.output:
        parser.error("--output required")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Extract pages
    if args.pages:
        if ext != '.pdf':
            print("Error: Page extraction only works with PDF files")
            sys.exit(1)

        if not deps['pypdf']:
            print("Error: pypdf required")
            print("Install with: pip install pypdf")
            sys.exit(1)

        success = extract_pdf_pages(str(input_path), str(output_path), args.pages, args.verbose)
        sys.exit(0 if success else 1)

    # Optimize PDF
    if args.optimize:
        if ext != '.pdf':
            print("Error: Optimization only works with PDF files")
            sys.exit(1)

        if not deps['pypdf']:
            print("Error: pypdf required")
            sys.exit(1)

        success = optimize_pdf(str(input_path), str(output_path), args.verbose)
        sys.exit(0 if success else 1)

    # Convert to PDF
    if ext == '.md' or ext == '.markdown':
        if not deps['markdown']:
            print("Error: markdown package required")
            print("Install with: pip install markdown")
            sys.exit(1)

        success = convert_markdown_to_pdf(str(input_path), str(output_path), args.verbose)
        sys.exit(0 if success else 1)

    elif ext == '.html' or ext == '.htm':
        success = convert_html_to_pdf(str(input_path), str(output_path), args.verbose)
        sys.exit(0 if success else 1)

    else:
        print(f"Error: Unsupported file type: {ext}")
        print("Supported: .pdf (extract/optimize), .md, .html")
        sys.exit(1)


if __name__ == '__main__':
    main()
