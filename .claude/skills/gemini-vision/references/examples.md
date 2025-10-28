# Gemini Vision API - Code Examples

Comprehensive code examples for common use cases.

## Table of Contents

1. [Basic Image Analysis](#basic-image-analysis)
2. [Multi-Image Analysis](#multi-image-analysis)
3. [Object Detection](#object-detection)
4. [Segmentation](#segmentation)
5. [Document Processing](#document-processing)
6. [File Upload & Management](#file-upload--management)
7. [Advanced Techniques](#advanced-techniques)

---

## Basic Image Analysis

### Analyze Local Image (Python)

```python
from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key="YOUR_API_KEY")

# Read image file
with open('path/to/image.jpg', 'rb') as f:
    image_bytes = f.read()

# Generate response
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg'
        ),
        'What is in this image?'
    ]
)

print(response.text)
```

### Analyze Image from URL (Python)

```python
from google import genai
from google.genai import types
import requests

# Initialize client
client = genai.Client(api_key="YOUR_API_KEY")

# Download image
image_url = "https://example.com/image.jpg"
image_bytes = requests.get(image_url).content

# Generate response
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg'
        ),
        'Describe this image in detail.'
    ]
)

print(response.text)
```

### Analyze Image (JavaScript/Node.js)

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

// Initialize client
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

// Read image file as base64
const base64Image = fs.readFileSync("path/to/image.jpg", {
  encoding: "base64",
});

// Generate response
const response = await ai.models.generate({
  model: "gemini-2.5-flash",
  contents: [
    {
      parts: [
        {
          inline_data: {
            mime_type: "image/jpeg",
            data: base64Image,
          },
        },
        {
          text: "What is in this image?",
        },
      ],
    },
  ],
});

console.log(response.text);
```

### Analyze Image (REST/curl)

```bash
# Base64 encode the image
IMAGE_BASE64=$(base64 -w 0 image.jpg)

# Make API request
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "inline_data": {
              "mime_type": "image/jpeg",
              "data": "'"$IMAGE_BASE64"'"
            }
          },
          {
            "text": "What is in this image?"
          }
        ]
      }
    ]
  }'
```

---

## Multi-Image Analysis

### Compare Two Images (Python)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

# Read both images
with open('image1.jpg', 'rb') as f1:
    img1_bytes = f1.read()

with open('image2.jpg', 'rb') as f2:
    img2_bytes = f2.read()

# Generate response
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'What are the differences between these two images?',
        types.Part.from_bytes(data=img1_bytes, mime_type='image/jpeg'),
        types.Part.from_bytes(data=img2_bytes, mime_type='image/jpeg')
    ]
)

print(response.text)
```

### Analyze Multiple Images (JavaScript)

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const images = [
  fs.readFileSync("img1.jpg", { encoding: "base64" }),
  fs.readFileSync("img2.jpg", { encoding: "base64" }),
  fs.readFileSync("img3.jpg", { encoding: "base64" }),
];

const parts = [
  { text: "What is the common theme across these images?" },
  ...images.map(img => ({
    inline_data: { mime_type: "image/jpeg", data: img }
  }))
];

const response = await ai.models.generate({
  model: "gemini-2.5-flash",
  contents: [{ parts }],
});

console.log(response.text);
```

---

## Object Detection

### Detect Objects with Bounding Boxes (Python)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

with open('street_scene.jpg', 'rb') as f:
    image_bytes = f.read()

# Request object detection
response = client.models.generate_content(
    model='gemini-2.0-flash',  # 2.0+ required for detection
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        'Detect all objects in this image and provide bounding boxes.'
    ]
)

print(response.text)
```

### Parse Bounding Boxes (Python)

```python
import re
import json

def parse_bounding_boxes(response_text):
    """Parse bounding box coordinates from response."""
    # Gemini returns boxes in format: [ymin, xmin, ymax, xmax]
    # Coordinates are in range [0, 1000]

    boxes = []

    # Look for patterns like: car [100, 200, 300, 400]
    pattern = r'(\w+)\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]'
    matches = re.findall(pattern, response_text)

    for match in matches:
        label, ymin, xmin, ymax, xmax = match
        boxes.append({
            'label': label,
            'bbox': {
                'ymin': int(ymin) / 1000,  # Normalize to [0, 1]
                'xmin': int(xmin) / 1000,
                'ymax': int(ymax) / 1000,
                'xmax': int(xmax) / 1000
            }
        })

    return boxes

# Use it
boxes = parse_bounding_boxes(response.text)
print(json.dumps(boxes, indent=2))
```

### Draw Bounding Boxes (Python)

```python
from PIL import Image, ImageDraw

def draw_boxes(image_path, boxes, output_path='output.jpg'):
    """Draw bounding boxes on image."""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    width, height = img.size

    for box in boxes:
        bbox = box['bbox']
        label = box['label']

        # Convert normalized coords to pixel coords
        x1 = int(bbox['xmin'] * width)
        y1 = int(bbox['ymin'] * height)
        x2 = int(bbox['xmax'] * width)
        y2 = int(bbox['ymax'] * height)

        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline='red', width=3)
        draw.text((x1, y1 - 10), label, fill='red')

    img.save(output_path)
    print(f"Saved to {output_path}")

# Use it
draw_boxes('street_scene.jpg', boxes)
```

---

## Segmentation

### Generate Segmentation Masks (Python)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

with open('portrait.jpg', 'rb') as f:
    image_bytes = f.read()

# Request segmentation
response = client.models.generate_content(
    model='gemini-2.5-flash',  # 2.5+ required for segmentation
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        'Segment the person in this image and provide a pixel mask.'
    ]
)

print(response.text)
```

---

## Document Processing

### Extract Text from PDF (Python)

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

# Upload PDF
uploaded_file = client.files.upload(file="document.pdf")

# Process document
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        uploaded_file,
        'Extract all text from this PDF document.'
    ]
)

print(response.text)
```

### Analyze Charts in Document (Python)

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

uploaded_file = client.files.upload(file="report.pdf")

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        uploaded_file,
        'Analyze all charts and graphs in this document. Provide the data values.'
    ]
)

print(response.text)
```

---

## File Upload & Management

### Upload and Reuse File (Python)

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

# Upload file once
uploaded_file = client.files.upload(file="large_image.jpg")
print(f"Uploaded: {uploaded_file.name}")

# Use multiple times
response1 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[uploaded_file, 'Describe this image.']
)

response2 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[uploaded_file, 'What colors are prominent?']
)

# Clean up
client.files.delete(name=uploaded_file.name)
```

### List and Clean Up Old Files (Python)

```python
from google import genai
from datetime import datetime, timedelta

client = genai.Client(api_key="YOUR_API_KEY")

# List all files
files = client.files.list()

# Delete files older than 24 hours
cutoff = datetime.now() - timedelta(hours=24)

for file in files:
    # Parse create_time and check age
    # Files auto-delete after 48 hours anyway
    print(f"Found: {file.display_name} ({file.name})")

    # Delete specific file
    # client.files.delete(name=file.name)
```

---

## Advanced Techniques

### Structured JSON Output (Python)

```python
from google import genai
from google.genai import types
import json

client = genai.Client(api_key="YOUR_API_KEY")

with open('product.jpg', 'rb') as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        '''Analyze this product image and return JSON with this structure:
        {
          "product_name": "...",
          "category": "...",
          "colors": ["...", "..."],
          "description": "...",
          "features": ["...", "..."]
        }'''
    ]
)

# Parse JSON from response
data = json.loads(response.text)
print(json.dumps(data, indent=2))
```

### Few-Shot Learning (Python)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

# Provide examples first
with open('example1.jpg', 'rb') as f:
    ex1_bytes = f.read()

with open('example2.jpg', 'rb') as f:
    ex2_bytes = f.read()

with open('query.jpg', 'rb') as f:
    query_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Example 1: Modern style',
        types.Part.from_bytes(data=ex1_bytes, mime_type='image/jpeg'),
        'Example 2: Vintage style',
        types.Part.from_bytes(data=ex2_bytes, mime_type='image/jpeg'),
        'What style is this image?',
        types.Part.from_bytes(data=query_bytes, mime_type='image/jpeg')
    ]
)

print(response.text)
```

### Batch Processing (Python)

```python
from google import genai
from google.genai import types
from pathlib import Path
import concurrent.futures

client = genai.Client(api_key="YOUR_API_KEY")

def process_image(image_path):
    """Process a single image."""
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
            'Caption this image in one sentence.'
        ]
    )

    return {
        'path': str(image_path),
        'caption': response.text
    }

# Process multiple images in parallel
image_dir = Path('images/')
image_files = list(image_dir.glob('*.jpg'))

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(process_image, image_files))

for result in results:
    print(f"{result['path']}: {result['caption']}")
```

### Error Handling with Retry (Python)

```python
from google import genai
from google.genai import types
import time

client = genai.Client(api_key="YOUR_API_KEY")

def analyze_with_retry(image_bytes, prompt, max_retries=3):
    """Analyze image with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                    prompt
                ]
            )
            return response.text

        except Exception as e:
            if '429' in str(e):  # Rate limit
                wait_time = (2 ** attempt) * 1  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

    raise Exception("Max retries exceeded")

# Use it
with open('image.jpg', 'rb') as f:
    result = analyze_with_retry(f.read(), "What is this?")
    print(result)
```

---

## Tips & Best Practices

### Optimizing Token Usage

```python
from PIL import Image

def resize_for_gemini(image_path, max_dimension=768):
    """Resize image to minimize token cost."""
    img = Image.open(image_path)

    # If both dimensions ≤ 384, cost is only 258 tokens
    if max(img.size) <= 384:
        return img

    # Otherwise resize to max_dimension to control tiling
    ratio = max_dimension / max(img.size)
    new_size = tuple(int(dim * ratio) for dim in img.size)

    return img.resize(new_size, Image.LANCZOS)

# Use it
img = resize_for_gemini('large_image.jpg')
img.save('optimized.jpg')
```

### Prompt Engineering

```python
# Good: Specific and clear
prompt = "List all visible objects in this image as a bullet-pointed list."

# Better: Specify format and level of detail
prompt = """Analyze this image and provide:
1. Main subject (1 sentence)
2. Background elements (bullet list)
3. Colors (list of 3-5 dominant colors)
4. Overall mood (1 word)

Format as JSON."""

# Best: Include examples if needed
prompt = """Identify the architectural style of this building.
Examples:
- Gothic: pointed arches, flying buttresses
- Modern: clean lines, glass facades
- Victorian: ornate details, asymmetrical

Your answer:"""
```

---

For more examples and tutorials, visit:
- https://ai.google.dev/gemini-api/docs/image-understanding
- https://github.com/google-gemini/cookbook
