# Document Extraction Reference

Comprehensive guide for PDF processing, structured data extraction, and document understanding using Gemini API.

## Core Capabilities

- **PDF Vision Processing**: Native understanding up to 1,000 pages
- **Multimodal Analysis**: Text, images, diagrams, charts, tables
- **Structured Extraction**: JSON output with schema validation
- **Document Q&A**: Answer questions about content
- **Summarization**: Generate summaries preserving context
- **Format Conversion**: Transcribe to HTML/JSON while preserving layout
- **Table Extraction**: Extract tabular data
- **Form Processing**: Identify and extract form fields
- **Chart Analysis**: Understand charts and diagrams

## Supported Formats

- **PDF**: Full vision processing (up to 1,000 pages)
- **TXT, HTML, Markdown**: Text-only processing (no vision)

## Specifications

- **Max pages**: 1,000 per document
- **Token cost**: 258 tokens per page (fixed)
- **Size limits**:
  - Inline: <20MB (base64 encoding)
  - File API: <2GB per file
- **Retention**: 48 hours (File API)
- **Processing**: Native vision, no OCR needed

## Basic PDF Processing

### Inline Encoding (<20MB)

```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Read PDF
with open('document.pdf', 'rb') as f:
    pdf_data = f.read()

# Process
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Summarize this document',
        types.Part.from_bytes(data=pdf_data, mime_type='application/pdf')
    ]
)
print(response.text)
```

### File API (>20MB)

```python
# Upload
myfile = client.files.upload(file='large-document.pdf')

# Use
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Extract key information', myfile]
)
```

## Structured Data Extraction

### JSON Schema Output

```python
from pydantic import BaseModel
from typing import List

class InvoiceItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float

class InvoiceData(BaseModel):
    invoice_number: str
    date: str
    vendor: str
    items: List[InvoiceItem]
    subtotal: float
    tax: float
    total: float

# Extract with schema
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Extract invoice details', pdf_part],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=InvoiceData
    )
)

invoice = InvoiceData.model_validate_json(response.text)
```

### Table Extraction

```python
class TableRow(BaseModel):
    columns: List[str]

class TableData(BaseModel):
    headers: List[str]
    rows: List[TableRow]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Extract all tables from this document', pdf_part],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=List[TableData]
    )
)
```

### Form Field Extraction

```python
class FormField(BaseModel):
    field_name: str
    field_type: str
    value: str
    is_filled: bool

class FormData(BaseModel):
    form_title: str
    fields: List[FormField]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Extract all form fields and their values', pdf_part],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=FormData
    )
)
```

## Document Understanding

### Summarization

```python
# Executive summary
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Provide an executive summary highlighting key findings',
        pdf_part
    ]
)

# Section-by-section
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Summarize each section separately with section headers',
        pdf_part
    ]
)
```

### Question Answering

```python
# Specific question
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'What are the key terms and conditions in this contract?',
        pdf_part
    ]
)

# Multiple questions
questions = [
    'What is the effective date?',
    'What are the payment terms?',
    'What are the termination conditions?'
]

for question in questions:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[question, pdf_part]
    )
    print(f"{question}\n{response.text}\n")
```

### Chart and Diagram Analysis

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        '''Analyze all charts and diagrams:
        1. Identify chart type
        2. Extract data points
        3. Explain key insights
        4. Reference page numbers
        ''',
        pdf_part
    ]
)
```

## Format Conversion

### PDF to HTML

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Convert this PDF to clean HTML, preserving structure and formatting',
        pdf_part
    ]
)

with open('output.html', 'w') as f:
    f.write(response.text)
```

### PDF to Markdown

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Convert this PDF to Markdown, preserving headers, lists, and tables',
        pdf_part
    ]
)
```

### PDF to JSON

```python
class DocumentSection(BaseModel):
    title: str
    content: str
    page_numbers: List[int]

class DocumentStructure(BaseModel):
    title: str
    sections: List[DocumentSection]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Convert document structure to JSON', pdf_part],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=DocumentStructure
    )
)
```

## Multi-Page Processing

### Page-Specific Queries

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Extract information only from pages 5-10',
        pdf_part
    ]
)
```

### Page Range Extraction

```python
# Note: For actual page splitting, use document_converter.py script
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Summarize the content on pages 1-5 separately from pages 6-10',
        pdf_part
    ]
)
```

### Cross-Reference Analysis

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Find all cross-references and citations in this document',
        pdf_part
    ]
)
```

## Common Use Cases

### 1. Invoice Processing

```python
class Invoice(BaseModel):
    invoice_number: str
    date: str
    vendor: str
    customer: str
    items: List[dict]
    subtotal: float
    tax: float
    total: float

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Extract complete invoice information', pdf_part],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=Invoice
    )
)
```

### 2. Resume Parsing

```python
class Education(BaseModel):
    degree: str
    institution: str
    year: str

class Experience(BaseModel):
    title: str
    company: str
    duration: str
    responsibilities: List[str]

class Resume(BaseModel):
    name: str
    contact: dict
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[str]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Parse resume into structured format', pdf_part],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=Resume
    )
)
```

### 3. Contract Analysis

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        '''Analyze contract:
        1. Parties involved
        2. Effective dates
        3. Key obligations
        4. Payment terms
        5. Termination clauses
        6. Risk factors
        ''',
        pdf_part
    ]
)
```

### 4. Research Paper Extraction

```python
class Paper(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    key_findings: List[str]
    methodology: str
    conclusions: str
    references: List[str]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Extract research paper structure', pdf_part],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=Paper
    )
)
```

### 5. Financial Report Analysis

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        '''Analyze financial report:
        1. Extract all financial tables
        2. Identify key metrics (revenue, profit, margins)
        3. Note significant trends
        4. Highlight risk factors
        5. Summarize management discussion
        ''',
        pdf_part
    ]
)
```

### 6. Form Processing

```python
class FormSubmission(BaseModel):
    form_type: str
    submission_date: str
    applicant_info: dict
    responses: dict
    signatures: List[str]
    attachments: List[str]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Extract form data including all fields', pdf_part],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=FormSubmission
    )
)
```

## Best Practices

### Input Optimization

1. **File size**: Use inline for <20MB, File API for larger
2. **Quality**: Ensure clear scans (300 DPI minimum)
3. **Orientation**: Verify correct page rotation
4. **Format**: PDF only for vision processing

### Prompt Engineering

**Specific instructions**:
- "Extract table on page 3 as JSON"
- "Identify all dates in MM/DD/YYYY format"
- "Find clauses related to liability"

**Output format**:
- "Return as JSON with schema"
- "Format as markdown table"
- "Provide numbered list"

**Context helps**:
- "This is a medical form - use medical terminology"
- "This is a legal contract - identify binding terms"
- "This is a technical manual - extract step-by-step instructions"

### Cost Optimization

**Token costs**:
- 10-page PDF: 2,580 tokens = $0.00258 (Flash)
- 100-page PDF: 25,800 tokens = $0.0258 (Flash)
- 1,000-page PDF: 258,000 tokens = $0.258 (Flash)

**Strategies**:
- Use File API for repeated queries (enables caching)
- Process only relevant page ranges
- Use Flash model for most tasks
- Upgrade to Pro only for complex analysis
- Batch multiple documents when possible

### Context Caching

```python
# Upload and cache
myfile = client.files.upload(file='large-doc.pdf')

# First query (counts toward context)
response1 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Summarize', myfile],
    config=types.GenerateContentConfig(
        cached_content=True
    )
)

# Subsequent queries (uses cache)
response2 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Extract key dates', myfile],
    config=types.GenerateContentConfig(
        cached_content=True
    )
)
```

## Error Handling

```python
import time

def process_pdf_with_retry(pdf_path, prompt, max_retries=3):
    """Process PDF with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    prompt,
                    types.Part.from_bytes(
                        data=pdf_data,
                        mime_type='application/pdf'
                    )
                ]
            )
            return response.text
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1} after {wait_time}s: {e}")
            time.sleep(wait_time)
```

## Limitations

- PDF only for vision processing (TXT/HTML/Markdown text-only)
- Maximum 1,000 pages per document
- Fixed 258 tokens per page (regardless of content density)
- No image extraction (images analyzed as part of page)
- Files expire after 48 hours (File API)
- No real-time collaboration features
- Handwriting recognition varies with quality
