---
name: gemini-document-processing
description: Guide for implementing Google Gemini API document processing - analyze PDFs with native vision to extract text, images, diagrams, charts, and tables. Use when processing documents, extracting structured data, summarizing PDFs, answering questions about document content, or converting documents to structured formats. (project)
---

# Gemini Document Processing

Process and analyze PDF documents using Google Gemini's native vision capabilities. Extract structured information, summarize content, answer questions, and understand complex documents with text, images, diagrams, charts, and tables.

## Core Capabilities

- **PDF Vision Processing**: Native understanding of PDFs up to 1,000 pages (258 tokens/page)
- **Multimodal Analysis**: Process text, images, diagrams, charts, and tables
- **Structured Extraction**: Output to JSON with schema validation
- **Document Q&A**: Answer questions based on document content
- **Summarization**: Generate summaries preserving context
- **Format Conversion**: Transcribe to HTML while preserving layout

## When to Use This Skill

Use this skill when you need to:
- Extract structured data from PDF documents (invoices, resumes, forms)
- Summarize long documents or reports
- Answer questions about PDF content
- Analyze documents with complex layouts, charts, or diagrams
- Convert PDFs to structured formats (JSON, HTML)
- Process multiple documents in batch
- Build document processing pipelines

## Quick Setup

### 1. API Key Configuration

The skill checks for `GEMINI_API_KEY` in this priority order:
1. Process environment variable
2. `.env` file in skill directory (`.claude/skills/gemini-document-processing/.env`)
3. `.env` file in project root

**Get your API key:** https://aistudio.google.com/apikey

**Option A: Environment Variable (Recommended)**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option B: Skill Directory**
```bash
cd .claude/skills/gemini-document-processing
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

**Option C: Project Root**
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

### 2. Install Dependencies

```bash
pip install google-genai python-dotenv
```

## Common Use Cases

### 1. Extract Structured Data from PDF

```python
# Use the provided script
python .claude/skills/gemini-document-processing/scripts/process-document.py \
  --file invoice.pdf \
  --prompt "Extract invoice details as JSON" \
  --format json
```

### 2. Summarize Long Document

```python
# Process and summarize
python .claude/skills/gemini-document-processing/scripts/process-document.py \
  --file report.pdf \
  --prompt "Provide a concise executive summary"
```

### 3. Answer Questions About Document

```python
# Q&A on document content
python .claude/skills/gemini-document-processing/scripts/process-document.py \
  --file contract.pdf \
  --prompt "What are the key terms and conditions?"
```

### 4. Process with Python SDK

```python
from google import genai

client = genai.Client()

# Read PDF
with open('document.pdf', 'rb') as f:
    pdf_data = f.read()

# Process document
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Extract key information from this document',
        genai.types.Part.from_bytes(
            data=pdf_data,
            mime_type='application/pdf'
        )
    ]
)

print(response.text)
```

### 5. Structured Output with JSON Schema

```python
from google import genai
from pydantic import BaseModel

class InvoiceData(BaseModel):
    invoice_number: str
    date: str
    total: float
    vendor: str

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Extract invoice details',
        genai.types.Part.from_bytes(
            data=open('invoice.pdf', 'rb').read(),
            mime_type='application/pdf'
        )
    ],
    config=genai.types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=InvoiceData
    )
)

invoice_data = InvoiceData.model_validate_json(response.text)
```

## Key Constraints

- **Format**: Only PDFs get vision processing (TXT, HTML, Markdown are text-only)
- **Size**: < 20MB use inline encoding, > 20MB use File API
- **Pages**: Max 1,000 pages per document
- **Storage**: File API stores for 48 hours only
- **Cost**: 258 tokens per page (fixed, regardless of content density)

## Performance Tips

1. **Use Inline Encoding** for PDFs < 20MB (simpler, single request)
2. **Use File API** for larger files or repeated queries (enables context caching)
3. **Place Prompt After PDF** for single-page documents
4. **Use Context Caching** when querying same PDF multiple times
5. **Process in Parallel** for multiple independent documents
6. **Use gemini-2.5-flash** for best price/performance ratio

## Decision Guide

```
PDF < 20MB?
├─ Yes → Use inline base64 encoding
└─ No  → Use File API

Need structured JSON output?
├─ Yes → Define response_schema with Pydantic
└─ No  → Get text response

Multiple queries on same PDF?
├─ Yes → Use File API + Context Caching
└─ No  → Inline encoding is sufficient
```

## Script Reference

The skill includes a ready-to-use processing script:

```bash
# Basic usage
python scripts/process-document.py --file document.pdf --prompt "Your prompt"

# With JSON output
python scripts/process-document.py --file document.pdf --prompt "Extract data" --format json

# With File API (for large files)
python scripts/process-document.py --file large-document.pdf --prompt "Summarize" --use-file-api

# Multiple prompts
python scripts/process-document.py --file document.pdf --prompt "Question 1" --prompt "Question 2"
```

## References

For comprehensive documentation, see:
- `references/gemini-document-processing-report.md` - Complete API reference
- `references/quick-reference.md` - Quick lookup guide
- `references/code-examples.md` - Additional code patterns

## Troubleshooting

**API Key Not Found:**
```bash
# Check API key is set
./scripts/check-api-key.sh
```

**File Too Large:**
- Use File API for files > 20MB
- Add `--use-file-api` flag to the script

**Vision Not Working:**
- Ensure file is PDF format
- Other formats (TXT, HTML) don't support vision processing

## Support

- **API Documentation**: https://ai.google.dev/gemini-api/docs/document-processing
- **Get API Key**: https://aistudio.google.com/apikey
- **Model Info**: https://ai.google.dev/gemini-api/docs/models/gemini
