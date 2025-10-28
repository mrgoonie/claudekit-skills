---
name: gemini-vision
description: Guide for implementing Google Gemini API image understanding - analyze images with captioning, classification, visual QA, object detection, segmentation, and multi-image comparison. Use when analyzing images, answering visual questions, detecting objects, or processing documents with vision.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Gemini Vision API Skill

This skill enables Claude to use Google's Gemini API for advanced image understanding tasks including captioning, classification, visual question answering, object detection, segmentation, and multi-image analysis.

## Quick Start

### Prerequisites

1. **Get API Key**: Obtain from [Google AI Studio](https://aistudio.google.com/apikey)
2. **Install SDK**: `pip install google-genai` (Python 3.9+)

### API Key Configuration

The skill checks for `GEMINI_API_KEY` in this order:

1. **Process environment variable** (recommended)
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

2. **Skill directory**: `.claude/skills/gemini-vision/.env`
   ```
   GEMINI_API_KEY=your-api-key
   ```

3. **Project directory**: `.env` or `.gemini_api_key` in project root

**Security**: Never commit API keys to version control. Add `.env` to `.gitignore`.

## Core Capabilities

### Image Analysis
- **Captioning**: Generate descriptive text for images
- **Classification**: Categorize and identify image content
- **Visual QA**: Answer questions about image content
- **Multi-image**: Compare and analyze up to 3,600 images

### Advanced Features (Model-Specific)
- **Object Detection**: Identify and locate objects with bounding boxes (Gemini 2.0+)
- **Segmentation**: Create pixel-level masks for objects (Gemini 2.5+)
- **Document Understanding**: Process PDFs with vision (up to 1,000 pages)

## Supported Formats

- **Images**: PNG, JPEG, WEBP, HEIC, HEIF
- **Documents**: PDF (up to 1,000 pages)
- **Size Limits**:
  - Inline: 20MB max total request size
  - File API: For larger files
  - Max images: 3,600 per request

## Available Models

- **gemini-2.5-pro**: Most capable, segmentation + detection
- **gemini-2.5-flash**: Fast, efficient, segmentation + detection
- **gemini-2.5-flash-lite**: Lightweight, segmentation + detection
- **gemini-2.0-flash**: Object detection support
- **gemini-1.5-pro/flash**: Previous generation

## Usage Examples

### Basic Image Analysis

```bash
# Analyze a local image
python scripts/analyze-image.py path/to/image.jpg "What's in this image?"

# Analyze from URL
python scripts/analyze-image.py https://example.com/image.jpg "Describe this"

# Specify model
python scripts/analyze-image.py image.jpg "Caption this" --model gemini-2.5-pro
```

### Object Detection (2.0+)

```bash
python scripts/analyze-image.py image.jpg "Detect all objects" --model gemini-2.0-flash
```

### Multi-Image Comparison

```bash
python scripts/analyze-image.py img1.jpg img2.jpg "What's different between these?"
```

### File Upload (for large files or reuse)

```bash
# Upload file
python scripts/upload-file.py path/to/large-image.jpg

# Use uploaded file
python scripts/analyze-image.py file://file-id "Caption this"
```

### File Management

```bash
# List uploaded files
python scripts/manage-files.py list

# Get file info
python scripts/manage-files.py get file-id

# Delete file
python scripts/manage-files.py delete file-id
```

## Token Costs

Images consume tokens based on size:

- **Small** (≤384px both dimensions): 258 tokens
- **Large**: Tiled into 768×768 chunks, 258 tokens each

**Token Formula**:
```
crop_unit = floor(min(width, height) / 1.5)
tiles = (width / crop_unit) × (height / crop_unit)
total_tokens = tiles × 258
```

**Example**: 960×540 image = 6 tiles = 1,548 tokens

## Rate Limits

Limits vary by tier (Free, Tier 1, 2, 3):
- Measured in RPM (requests/min), TPM (tokens/min), RPD (requests/day)
- Applied per project, not per API key
- RPD resets at midnight Pacific

## Best Practices

### Image Quality
- Use clear, non-blurry images
- Verify correct image rotation
- Consider token costs when sizing

### Prompting
- Be specific in instructions
- Place text after image for single-image prompts
- Use few-shot examples for better accuracy
- Specify output format (JSON, markdown, etc.)

### File Management
- Use File API for files >20MB
- Use File API for repeated usage (saves tokens)
- Files auto-delete after 48 hours
- Clean up manually when done

### Security
- Never expose API keys in code
- Use environment variables
- Add API key restrictions in Google Cloud Console
- Monitor usage regularly
- Rotate keys periodically

## Error Handling

Common errors:
- **401**: Invalid API key
- **429**: Rate limit exceeded
- **400**: Invalid request (check file size, format)
- **403**: Permission denied (check API key restrictions)

## Additional Resources

See the `references/` directory for:
- **api-reference.md**: Detailed API methods and endpoints
- **examples.md**: Comprehensive code examples
- **best-practices.md**: Advanced tips and optimization strategies

## Implementation Guide

When implementing Gemini vision features:

1. **Check API key availability** using the 3-step lookup
2. **Choose appropriate model** based on requirements:
   - Need segmentation? Use 2.5+ models
   - Need detection? Use 2.0+ models
   - Need speed? Use Flash variants
   - Need quality? Use Pro variants
3. **Validate inputs**:
   - Check file format (PNG, JPEG, WEBP, HEIC, HEIF, PDF)
   - Verify file size (<20MB for inline, >20MB use File API)
   - Count images (max 3,600)
4. **Handle responses** appropriately:
   - Parse structured output if requested
   - Extract bounding boxes for object detection
   - Process segmentation masks if applicable
5. **Manage files** efficiently:
   - Upload large files via File API
   - Reuse uploaded files when possible
   - Clean up after use

## Scripts Overview

All scripts support the 3-step API key lookup:

- **analyze-image.py**: Main script for image analysis, supports inline and File API
- **upload-file.py**: Upload files to Gemini File API
- **manage-files.py**: List, get metadata, and delete uploaded files

Run any script with `--help` for detailed usage instructions.

---

**Official Documentation**: https://ai.google.dev/gemini-api/docs/image-understanding
