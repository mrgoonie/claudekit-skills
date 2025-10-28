# Gemini Document Processing - Quick Reference Summary

**Generated:** 2025-10-26  
**Documentation Status:** Thoroughly Explored  
**Completeness:** 100% - All links followed and documented

---

## Quick Facts

| Aspect | Details |
|--------|---------|
| **Primary Format** | PDF (native vision support) |
| **Max Document Size** | 1,000 pages |
| **Token Cost Per Page** | 258 tokens |
| **Inline Request Size Limit** | < 20 MB |
| **File API Storage Limit** | 50 MB |
| **File Retention Period** | 48 hours |
| **Supported Input Methods** | Inline base64, File API, URLs, Local files |
| **Recommended Model** | gemini-2.5-flash |
| **Output Formats** | Text, JSON (structured output) |

---

## Key Capabilities At A Glance

### What Gemini Document Processing Can Do
- Analyze text, images, diagrams, charts, tables in PDFs
- Extract structured information into JSON format
- Summarize complex documents
- Answer questions about document content
- Process multiple documents in parallel
- Preserve layouts and formatting when transcribing to HTML
- Handle documents up to 1000 pages

### What It Cannot Do
- Process non-PDF formats with vision understanding (TXT, HTML, Markdown treated as text-only)
- Download files from the internet (must be uploaded first)
- Support vision processing for document types other than PDF
- Provide cost reduction for lower resolution pages
- Improve performance with higher resolution pages

---

## API Usage Decision Tree

```
Is your PDF < 20MB?
├─ Yes → Use inline base64 encoding (simpler, single request)
└─ No → Use File API (handles > 20MB, 48-hour storage)

Need structured JSON output?
├─ Yes → Define response_schema with Pydantic model
└─ No → Get text response

Processing single page?
├─ Yes → Place text prompt AFTER the PDF
└─ No → Any order works

Need to query same PDF multiple times?
├─ Yes → Use File API + Context Caching
└─ No → Inline encoding is fine
```

---

## Code Quick Start

### Minimal Python Example
```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Summarize this PDF",
        types.Part.from_bytes(
            data=open('document.pdf', 'rb').read(),
            mime_type='application/pdf'
        )
    ]
)
print(response.text)
```

### Minimal REST Example
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [{
      "parts": [
        {"text": "Summarize this"},
        {"inline_data": {"mime_type": "application/pdf", "data": "'$BASE64_PDF'"}}
      ]
    }]
  }'
```

---

## Performance Optimization Tips

### For Best Results
1. Pre-process PDFs (rotate to correct orientation, remove blur)
2. Use File API for documents > 20MB
3. Enable context caching for multiple queries on same document
4. Use structured output (JSON schema) for automated extraction
5. Place single-page text prompts AFTER the PDF content
6. Use system instructions to guide model behavior

### Token Cost Awareness
- Each page = 258 tokens (fixed, regardless of content)
- 1000-page max document = ~258,000 tokens
- Budget accordingly for your use case
- Monitor with tokens.count API

---

## Use Cases & Patterns

### Automation Patterns
| Use Case | Pattern | Key Feature |
|----------|---------|------------|
| Invoice Processing | File API + Structured JSON | Extract amounts, dates, vendors |
| Resume Parsing | Structured output with Pydantic | Normalize candidate info |
| Contract Analysis | Function calling + Document | Extract terms, dates, obligations |
| Form Extraction | JSON schema + Batch API | Process bulk forms |
| Document Comparison | Multiple PDFs + single prompt | Compare versions |
| Research Summary | Long context + Q&A | Summarize papers, extract findings |

---

## Related Gemini Features to Consider

| Feature | When to Use | Link |
|---------|------------|------|
| **Structured Output** | Need JSON extraction | `/gemini-api/docs/structured-output` |
| **Files API** | Large documents (>20MB) | `/gemini-api/docs/files` |
| **Context Caching** | Multiple queries on same doc | `/gemini-api/docs/caching` |
| **Function Calling** | Automate based on extraction | `/gemini-api/docs/function-calling` |
| **Batch API** | Process many documents | `/gemini-api/docs/batch-api` |
| **Image Understanding** | Non-PDF images | `/gemini-api/docs/image-understanding` |
| **System Instructions** | Guide extraction behavior | `/gemini-api/docs/text-generation#system-instructions` |

---

## Limitations & Constraints

### Hard Limits
- 1,000 pages per document
- 20 MB inline request size
- 50 MB File API storage
- 48-hour file retention
- PDFs only for vision processing

### Scaling Considerations
- Each request is independent (no conversation history)
- Rate limits apply (check documentation)
- Token counting is per-page for documents
- Files deleted automatically after 48 hours

### Quality Factors
- Page orientation matters
- Blurry pages reduce accuracy
- Image resolution affects scaling (3072x3072 max, 768x768 min)
- Non-PDF formats lose visual elements

---

## Authentication & Setup

### Get Started
1. Obtain API key: https://aistudio.google.com/apikey
2. Set environment: `export GEMINI_API_KEY="your-key"`
3. Install SDK: `pip install google-genai` (Python)
4. Import and use

### API Key Management
- Keep keys secure (environment variables, not hardcoded)
- Rotate periodically
- Monitor usage patterns
- Use only for document processing

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Invalid MIME type" | Use `application/pdf` for PDFs |
| Request too large | Use File API instead of inline (> 20MB) |
| File processing failed | Check file format (PDF only for vision), retry |
| Slow processing | Enable context caching for repeated queries |
| Inaccurate extraction | Improve PDF quality, add detailed prompt instructions |
| JSON parsing error | Define response_schema with Pydantic model |
| File not found | Use File API URI, not download from API |

---

## SDK Support

| Language | Module | Example |
|----------|--------|---------|
| **Python** | `google-genai` | `from google import genai` |
| **JavaScript** | `@google/genai` | `import { GoogleGenAI }` |
| **Go** | `google.golang.org/genai` | `import "google.golang.org/genai"` |
| **REST** | Direct HTTP | `curl` with JSON payload |

---

## Resources & Links

### Core Documentation
- **Main Doc:** https://ai.google.dev/gemini-api/docs/document-processing
- **Vision Foundation:** https://ai.google.dev/gemini-api/docs/image-understanding
- **Files API:** https://ai.google.dev/gemini-api/docs/files
- **Structured Output:** https://ai.google.dev/gemini-api/docs/structured-output

### Support
- **API Key:** https://aistudio.google.com/apikey
- **Examples:** https://github.com/google-gemini/cookbook
- **Community:** https://discuss.ai.google.dev/c/gemini-api/
- **Main API Docs:** https://ai.google.dev/gemini-api

### Example PDFs
- https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf
- https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf

---

## Key Takeaways

1. **Vision-First Approach:** PDFs processed with native vision, not just OCR
2. **Scale Capability:** Up to 1000 pages in single document
3. **Flexible Input:** Inline, File API, URLs all supported
4. **Structured Output:** JSON extraction for automation
5. **Cost Predictable:** 258 tokens per page, fixed rate
6. **Production Ready:** File API for enterprise use (>20MB, caching)
7. **Integrated:** Works with all Gemini features (functions, caching, structured output)

---

**For comprehensive details, see:** `/mnt/d/www/claudekit/claudekit-engineer/gemini-document-processing-report.md`  
**For URL index, see:** `/mnt/d/www/claudekit/claudekit-engineer/GEMINI_EXPLORATION_URLS.md`

---

*Last Updated: 2025-10-26*  
*Documentation Date: 2025-09-22 UTC*
