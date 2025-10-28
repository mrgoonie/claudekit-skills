# Gemini Document Processing - Code Examples

Comprehensive code examples for common document processing tasks.

## Table of Contents
1. [Basic Document Processing](#basic-document-processing)
2. [Structured Data Extraction](#structured-data-extraction)
3. [Document Summarization](#document-summarization)
4. [Q&A on Documents](#qa-on-documents)
5. [Batch Processing](#batch-processing)
6. [Advanced Patterns](#advanced-patterns)

---

## Basic Document Processing

### Python - Inline Base64 Encoding

```python
from google import genai
from google.genai import types

# Initialize client (API key from environment)
client = genai.Client()

# Read PDF file
with open('document.pdf', 'rb') as f:
    pdf_data = f.read()

# Process document
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Summarize this document',
        types.Part.from_bytes(
            data=pdf_data,
            mime_type='application/pdf'
        )
    ]
)

print(response.text)
```

### Python - File API (Large Files)

```python
from google import genai
import time

client = genai.Client()

# Upload file
print("Uploading file...")
uploaded_file = client.files.upload(path='large-document.pdf')

# Wait for processing
while uploaded_file.state == 'PROCESSING':
    print("Processing...")
    time.sleep(2)
    uploaded_file = client.files.get(name=uploaded_file.name)

if uploaded_file.state == 'FAILED':
    raise Exception("File processing failed")

# Generate content
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Analyze this document', uploaded_file]
)

print(response.text)
```

### REST API - cURL

```bash
# Encode PDF to base64
BASE64_PDF=$(base64 -i document.pdf)

# Send request
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [{
      "parts": [
        {"text": "Summarize this document"},
        {"inline_data": {"mime_type": "application/pdf", "data": "'"$BASE64_PDF"'"}}
      ]
    }]
  }'
```

---

## Structured Data Extraction

### Extract Invoice Data as JSON

```python
from google import genai
from google.genai import types
from pydantic import BaseModel

# Define schema
class InvoiceData(BaseModel):
    invoice_number: str
    invoice_date: str
    due_date: str
    vendor_name: str
    vendor_address: str
    total_amount: float
    currency: str
    line_items: list[dict]

client = genai.Client()

# Process with schema
with open('invoice.pdf', 'rb') as f:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            'Extract all invoice information',
            types.Part.from_bytes(f.read(), mime_type='application/pdf')
        ],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=InvoiceData
        )
    )

# Parse JSON response
invoice = InvoiceData.model_validate_json(response.text)
print(f"Invoice #{invoice.invoice_number}")
print(f"Total: {invoice.currency} {invoice.total_amount}")
```

### Extract Resume Data

```python
from pydantic import BaseModel
from google import genai
from google.genai import types

class Resume(BaseModel):
    name: str
    email: str
    phone: str
    education: list[dict]
    experience: list[dict]
    skills: list[str]

client = genai.Client()

with open('resume.pdf', 'rb') as f:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            'Extract resume information',
            types.Part.from_bytes(f.read(), mime_type='application/pdf')
        ],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=Resume
        )
    )

resume = Resume.model_validate_json(response.text)
print(resume.model_dump_json(indent=2))
```

---

## Document Summarization

### Executive Summary

```python
from google import genai
from google.genai import types

client = genai.Client()

prompt = """
Create an executive summary of this document including:
1. Main topic and purpose
2. Key findings or arguments (3-5 bullet points)
3. Conclusions and recommendations
4. Important data or statistics mentioned

Keep it concise (300-400 words).
"""

with open('report.pdf', 'rb') as f:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            prompt,
            types.Part.from_bytes(f.read(), mime_type='application/pdf')
        ]
    )

print(response.text)
```

### Page-by-Page Summary

```python
from google import genai

client = genai.Client()

# Upload large document
uploaded_file = client.files.upload(path='long-report.pdf')

# Wait for processing
import time
while uploaded_file.state == 'PROCESSING':
    time.sleep(2)
    uploaded_file = client.files.get(name=uploaded_file.name)

# Get page-by-page summary
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Provide a brief summary for each page in the document. Format: "Page X: [summary]"',
        uploaded_file
    ]
)

print(response.text)
```

---

## Q&A on Documents

### Single Question

```python
from google import genai
from google.genai import types

client = genai.Client()

question = "What are the key terms and conditions in this contract?"

with open('contract.pdf', 'rb') as f:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            question,
            types.Part.from_bytes(f.read(), mime_type='application/pdf')
        ]
    )

print(response.text)
```

### Multiple Questions (Context Caching)

```python
from google import genai
from google.genai import types

client = genai.Client()

# Upload file once
uploaded_file = client.files.upload(path='document.pdf')

# Wait for processing
import time
while uploaded_file.state == 'PROCESSING':
    time.sleep(2)
    uploaded_file = client.files.get(name=uploaded_file.name)

# Ask multiple questions
questions = [
    "What is the main topic of this document?",
    "What are the key findings?",
    "What recommendations are made?",
    "Are there any limitations mentioned?"
]

for i, question in enumerate(questions, 1):
    print(f"\n{'='*60}")
    print(f"Question {i}: {question}")
    print('='*60)

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[question, uploaded_file]
    )

    print(response.text)
```

---

## Batch Processing

### Process Multiple Documents

```python
from google import genai
from google.genai import types
import os
from pathlib import Path

client = genai.Client()

def process_pdf(file_path: str, prompt: str) -> str:
    """Process a single PDF"""
    with open(file_path, 'rb') as f:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt,
                types.Part.from_bytes(f.read(), mime_type='application/pdf')
            ]
        )
    return response.text

# Process all PDFs in a directory
pdf_dir = Path('documents/')
results = {}

for pdf_file in pdf_dir.glob('*.pdf'):
    print(f"Processing: {pdf_file.name}")
    result = process_pdf(str(pdf_file), "Summarize this document in 2-3 sentences")
    results[pdf_file.name] = result

# Output results
for filename, summary in results.items():
    print(f"\n{'='*60}")
    print(f"File: {filename}")
    print('='*60)
    print(summary)
```

### Parallel Processing

```python
from google import genai
from google.genai import types
import concurrent.futures
from pathlib import Path

client = genai.Client()

def process_document(file_path: Path) -> dict:
    """Process a single document"""
    with open(file_path, 'rb') as f:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                'Extract key information',
                types.Part.from_bytes(f.read(), mime_type='application/pdf')
            ]
        )
    return {
        'file': file_path.name,
        'result': response.text
    }

# Process multiple files in parallel
pdf_files = list(Path('documents/').glob('*.pdf'))

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(process_document, pdf_files))

for result in results:
    print(f"\n{result['file']}:")
    print(result['result'])
```

---

## Advanced Patterns

### Compare Two Documents

```python
from google import genai
from google.genai import types

client = genai.Client()

# Read both documents
with open('document_v1.pdf', 'rb') as f:
    doc1 = f.read()

with open('document_v2.pdf', 'rb') as f:
    doc2 = f.read()

# Compare
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Compare these two documents and highlight the key differences',
        types.Part.from_bytes(doc1, mime_type='application/pdf'),
        types.Part.from_bytes(doc2, mime_type='application/pdf')
    ]
)

print(response.text)
```

### Extract Tables to CSV

```python
from google import genai
from google.genai import types
import csv

client = genai.Client()

# Extract tables as structured data
with open('report-with-tables.pdf', 'rb') as f:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            'Extract all tables from this document as JSON arrays',
            types.Part.from_bytes(f.read(), mime_type='application/pdf')
        ],
        config=types.GenerateContentConfig(
            response_mime_type='application/json'
        )
    )

# Parse and save as CSV
import json
tables = json.loads(response.text)

for i, table in enumerate(tables.get('tables', []), 1):
    with open(f'table_{i}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)
    print(f"Saved table_{i}.csv")
```

### Convert PDF to HTML

```python
from google import genai
from google.genai import types

client = genai.Client()

with open('document.pdf', 'rb') as f:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            'Convert this document to clean HTML, preserving layout and formatting',
            types.Part.from_bytes(f.read(), mime_type='application/pdf')
        ]
    )

# Save as HTML
with open('document.html', 'w') as f:
    f.write(response.text)

print("Saved document.html")
```

### Error Handling and Retries

```python
from google import genai
from google.genai import types
import time

client = genai.Client()

def process_with_retry(file_path: str, prompt: str, max_retries: int = 3):
    """Process document with retry logic"""
    for attempt in range(max_retries):
        try:
            with open(file_path, 'rb') as f:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        prompt,
                        types.Part.from_bytes(f.read(), mime_type='application/pdf')
                    ]
                )
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise

# Usage
result = process_with_retry('document.pdf', 'Summarize this document')
print(result)
```

---

## Tips and Best Practices

1. **Use Inline Encoding** for files < 20MB - simpler and faster
2. **Use File API** for large files or multiple queries on same document
3. **Define Clear Prompts** - be specific about what you want extracted
4. **Use JSON Schema** for structured output - ensures consistent format
5. **Handle Errors** - implement retry logic for production use
6. **Parallel Processing** - process independent documents concurrently
7. **Context Caching** - reuse uploaded files for multiple queries
8. **Monitor Costs** - 258 tokens per page, plan accordingly
