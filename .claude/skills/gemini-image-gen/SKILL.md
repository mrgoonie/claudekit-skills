---
name: gemini-image-gen
description: Guide for implementing Google Gemini API image generation - create high-quality images from text prompts using gemini-2.5-flash-image model. Use when generating images, creating visual content, or implementing text-to-image features. Supports text-to-image, image editing, multi-image composition, and iterative refinement.
license: MIT
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
---

# Gemini Image Generation Skill

Generate high-quality images using Google's Gemini 2.5 Flash Image model with text prompts, image editing, and multi-image composition capabilities.

## When to Use This Skill

Use this skill when you need to:
- Generate images from text descriptions
- Edit existing images by adding/removing elements or changing styles
- Combine multiple source images into new compositions
- Iteratively refine images through conversational editing
- Create visual content for documentation, design, or creative projects

## Prerequisites

### API Key Setup

The skill automatically detects your `GEMINI_API_KEY` in this order:

1. **Process environment**: `export GEMINI_API_KEY="your-key"`
2. **Skill directory**: `.claude/skills/gemini-image-gen/.env`
3. **Project directory**: `./.env` (project root)

**Get your API key**: Visit [Google AI Studio](https://aistudio.google.com/apikey)

Create `.env` file with:
```bash
GEMINI_API_KEY=your_api_key_here
```

### Python Setup

Install required package:
```bash
pip install google-genai
```

## Quick Start

### Basic Text-to-Image Generation

```python
from google import genai
from google.genai import types
import os

# API key detection handled automatically by helper script
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A serene mountain landscape at sunset with snow-capped peaks',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='16:9'
    )
)

# Save to ./docs/assets/
for i, part in enumerate(response.candidates[0].content.parts):
    if part.inline_data:
        with open(f'./docs/assets/generated-{i}.png', 'wb') as f:
            f.write(part.inline_data.data)
```

### Using the Helper Script

For convenience, use the provided helper script that handles API key detection and file saving:

```bash
# Generate single image
python .claude/skills/gemini-image-gen/scripts/generate.py \
  "A futuristic city with flying cars" \
  --aspect-ratio 16:9 \
  --output ./docs/assets/city.png

# Generate with specific modalities
python .claude/skills/gemini-image-gen/scripts/generate.py \
  "Modern architecture design" \
  --response-modalities image text \
  --aspect-ratio 1:1
```

## Key Features

### Aspect Ratios

| Ratio | Resolution | Use Case | Token Cost |
|-------|-----------|----------|------------|
| 1:1 | 1024×1024 | Social media, avatars | 1290 |
| 16:9 | 1344×768 | Landscapes, banners | 1290 |
| 9:16 | 768×1344 | Mobile, portraits | 1290 |
| 4:3 | 1152×896 | Traditional media | 1290 |
| 3:4 | 896×1152 | Vertical posters | 1290 |

### Response Modalities

- **`['image']`**: Generate only images
- **`['text']`**: Generate only text descriptions
- **`['image', 'text']`**: Generate both images and descriptions

### Image Editing

Provide existing image + text instructions to modify:

```python
import PIL.Image

img = PIL.Image.open('original.png')
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Add a red balloon floating in the sky',
        img
    ]
)
```

### Multi-Image Composition

Combine up to 3 source images (recommended):

```python
img1 = PIL.Image.open('background.png')
img2 = PIL.Image.open('foreground.png')

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Combine these images into a cohesive scene',
        img1,
        img2
    ]
)
```

## Prompt Engineering Tips

**Structure effective prompts** with three elements:
1. **Subject**: What to generate ("a robot")
2. **Context**: Environmental setting ("in a futuristic city")
3. **Style**: Artistic treatment ("cyberpunk style, neon lighting")

**Example**: "A robot in a futuristic city, cyberpunk style with neon lighting and rain-slicked streets"

**Quality modifiers**:
- Add terms like "4K", "HDR", "high-quality", "professional photography"
- Specify camera settings: "35mm lens", "shallow depth of field", "golden hour lighting"

**Text in images**:
- Limit to 25 characters maximum
- Use up to 3 distinct phrases
- Specify font styles: "bold sans-serif title" or "handwritten script"

See `references/prompting-guide.md` for comprehensive prompt engineering strategies.

## Safety Settings

The model includes adjustable safety filters. Configure per-request:

```python
config = types.GenerateContentConfig(
    response_modalities=['image'],
    safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )
    ]
)
```

See `references/safety-settings.md` for detailed configuration options.

## Output Management

All generated images should be saved to `./docs/assets/` directory:

```bash
# Create directory if needed
mkdir -p ./docs/assets
```

The helper script automatically saves to this location with timestamped filenames.

## Model Specifications

**Model**: `gemini-2.5-flash-image`
- **Input tokens**: Up to 65,536
- **Output tokens**: Up to 32,768
- **Supported inputs**: Text and images
- **Supported outputs**: Text and images
- **Knowledge cutoff**: June 2025
- **Features**: Image generation, structured outputs, batch API, caching

## Limitations

- Maximum 3 input images recommended for best results
- Text rendering works best when generated separately first
- Does not support audio/video inputs
- Regional restrictions on child image uploads (EEA, CH, UK)
- Optimal language support: English, Spanish (Mexico), Japanese, Mandarin, Hindi

## Error Handling

Common issues and solutions:

**API key not found**:
```bash
# Check environment variables
echo $GEMINI_API_KEY

# Verify .env file exists
cat .claude/skills/gemini-image-gen/.env
# or
cat .env
```

**Safety filter blocking**:
- Review `response.prompt_feedback.block_reason`
- Adjust safety settings if appropriate for your use case
- Modify prompt to avoid triggering filters

**Token limit exceeded**:
- Reduce prompt length
- Use fewer input images
- Simplify image editing instructions

## Reference Documentation

For detailed information, see:
- `references/api-reference.md` - Complete API specifications
- `references/prompting-guide.md` - Advanced prompt engineering
- `references/safety-settings.md` - Safety configuration details
- `references/code-examples.md` - Additional implementation examples

## Resources

- [Official Documentation](https://ai.google.dev/gemini-api/docs/image-generation)
- [API Reference](https://ai.google.dev/api/generate-content)
- [Get API Key](https://aistudio.google.com/apikey)
- [Google AI Studio](https://aistudio.google.com) - Interactive testing
