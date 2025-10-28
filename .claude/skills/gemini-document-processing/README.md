# Gemini Document Processing Skill

Agent skill for processing PDF documents using Google Gemini API's native vision capabilities.

## Overview

This skill enables Claude Code to process and analyze PDF documents with Gemini's multimodal vision API. Extract structured data, summarize content, answer questions, and understand complex documents containing text, images, diagrams, charts, and tables.

## Quick Start

### 1. Get API Key

Get your Gemini API key from: https://aistudio.google.com/apikey

### 2. Configure API Key

The skill checks for API key in this priority order:

1. **Environment variable** (recommended):
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

2. **Skill directory**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

3. **Project root**:
   ```bash
   echo "GEMINI_API_KEY=your-api-key-here" > ../../../.env
   ```

### 3. Install Dependencies

```bash
pip install google-genai python-dotenv
```

### 4. Verify Setup

```bash
./scripts/check-api-key.sh
```

## Usage

### Use in Claude Code

Simply invoke the skill when working with documents:

```
/gemini-document-processing
```

Claude will have access to all document processing capabilities.

### Use Script Directly

```bash
# Basic usage
python scripts/process-document.py \
  --file document.pdf \
  --prompt "Summarize this document"

# Extract structured data as JSON
python scripts/process-document.py \
  --file invoice.pdf \
  --prompt "Extract invoice details" \
  --format json

# Process large file with File API
python scripts/process-document.py \
  --file large-report.pdf \
  --prompt "Analyze this report" \
  --use-file-api

# Multiple prompts
python scripts/process-document.py \
  --file contract.pdf \
  --prompt "What are the key terms?" \
  --prompt "What are the obligations?"
```

## Capabilities

- **PDF Vision Processing**: Native understanding of PDFs up to 1,000 pages
- **Multimodal Analysis**: Process text, images, diagrams, charts, tables
- **Structured Extraction**: Output to JSON with schema validation
- **Document Q&A**: Answer questions based on document content
- **Summarization**: Generate summaries preserving context
- **Format Conversion**: Transcribe to HTML while preserving layout
- **Batch Processing**: Process multiple documents in parallel
- **Context Caching**: Reuse uploaded files for multiple queries

## File Structure

```
gemini-document-processing/
├── SKILL.md                        # Skill entrypoint (loaded by Claude)
├── README.md                       # This file
├── .env.example                    # Environment template
├── scripts/
│   ├── process-document.py        # Main processing script
│   └── check-api-key.sh           # API key verification utility
└── references/
    ├── gemini-document-processing-report.md  # Comprehensive API reference
    ├── quick-reference.md         # Quick lookup guide
    └── code-examples.md           # Code patterns and examples
```

## Key Constraints

- **Format**: Only PDFs get vision processing (TXT, HTML, Markdown are text-only)
- **Size**: < 20MB use inline encoding, > 20MB use File API
- **Pages**: Max 1,000 pages per document
- **Storage**: File API stores for 48 hours only
- **Cost**: 258 tokens per page (fixed, regardless of content)

## Documentation

- **SKILL.md**: Main skill documentation for Claude
- **references/gemini-document-processing-report.md**: Comprehensive API reference (24KB, 713 lines)
- **references/quick-reference.md**: Quick lookup guide with decision trees
- **references/code-examples.md**: Code patterns in Python, JavaScript, REST

## Examples

See `references/code-examples.md` for comprehensive examples including:
- Basic document processing
- Structured data extraction
- Document summarization
- Q&A on documents
- Batch processing
- Advanced patterns

## Troubleshooting

**API Key Not Found:**
```bash
./scripts/check-api-key.sh
```

**File Too Large:**
- Use File API for files > 20MB
- Add `--use-file-api` flag

**Vision Not Working:**
- Ensure file is PDF format
- Other formats don't support vision processing

## Support

- **API Documentation**: https://ai.google.dev/gemini-api/docs/document-processing
- **Get API Key**: https://aistudio.google.com/apikey
- **Model Info**: https://ai.google.dev/gemini-api/docs/models/gemini

## License

This skill is part of ClaudeKit Engineer project.
