# Gemini Image Generation Skill

Agent skill for generating high-quality images using Google's Gemini 2.5 Flash Image model.

## Overview

This skill enables Claude Code agents to generate images from text prompts, edit existing images, combine multiple images, and iteratively refine results through conversational interaction.

## Features

- **Text-to-Image**: Generate images from descriptive text prompts
- **Image Editing**: Modify existing images by adding/removing elements or changing styles
- **Multi-Image Composition**: Combine up to 3 source images into new compositions
- **Iterative Refinement**: Progressively improve images through multi-turn conversations
- **Flexible Aspect Ratios**: Support for 1:1, 16:9, 9:16, 4:3, 3:4
- **Safety Controls**: Configurable content filtering
- **SynthID Watermarking**: Automatic invisible watermarking on all outputs

## Installation

### 1. Install Python SDK

```bash
pip install google-genai
```

### 2. Get API Key

Visit [Google AI Studio](https://aistudio.google.com/apikey) to obtain your `GEMINI_API_KEY`.

### 3. Configure API Key

The skill checks for the API key in this order:

1. **Process environment variable**:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

2. **Skill directory** `.env` file:
   ```bash
   # Create .claude/skills/gemini-image-gen/.env
   GEMINI_API_KEY=your-key-here
   ```

3. **Project root** `.env` file:
   ```bash
   # Create ./.env in project root
   GEMINI_API_KEY=your-key-here
   ```

## Quick Start

### Using the Helper Script

```bash
# Generate a simple image
python .claude/skills/gemini-image-gen/scripts/generate.py \
  "A serene mountain landscape at sunset"

# Specify aspect ratio
python .claude/skills/gemini-image-gen/scripts/generate.py \
  "Modern architecture design" \
  --aspect-ratio 16:9

# Generate both image and text
python .claude/skills/gemini-image-gen/scripts/generate.py \
  "Futuristic city with flying cars" \
  --response-modalities image text

# Custom output path
python .claude/skills/gemini-image-gen/scripts/generate.py \
  "Vintage robot illustration" \
  --output ./my-images/robot.png
```

### Using Python Directly

```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A peaceful zen garden with raked sand and stones',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='16:9'
    )
)

# Save image
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('./docs/assets/zen-garden.png', 'wb') as f:
            f.write(part.inline_data.data)
```

## Directory Structure

```
gemini-image-gen/
├── SKILL.md                      # Main skill entry point
├── README.md                     # This file
├── scripts/
│   └── generate.py               # Helper script with API key detection
└── references/
    ├── api-reference.md          # Complete API documentation
    ├── prompting-guide.md        # Prompt engineering strategies
    ├── safety-settings.md        # Safety configuration guide
    └── code-examples.md          # Implementation examples
```

## Documentation

### Main Documentation

- **[SKILL.md](./SKILL.md)** - Main skill instructions with quick start guide
- **[README.md](./README.md)** - This overview document

### Reference Documentation

- **[api-reference.md](./references/api-reference.md)** - Complete API specifications, parameters, error handling
- **[prompting-guide.md](./references/prompting-guide.md)** - Advanced prompt engineering techniques
- **[safety-settings.md](./references/safety-settings.md)** - Content filtering and safety configuration
- **[code-examples.md](./references/code-examples.md)** - Practical implementation examples

## Model Information

**Model**: `gemini-2.5-flash-image`

- **Latest Update**: October 2025
- **Knowledge Cutoff**: June 2025
- **Input Tokens**: 65,536
- **Output Tokens**: 32,768
- **Supported Inputs**: Text and images
- **Supported Outputs**: Text and images

### Capabilities

✅ Image generation
✅ Structured outputs
✅ Batch API
✅ Caching

❌ Audio generation
❌ Code execution
❌ Function calling
❌ Live API

## Output Management

All generated images are automatically saved to:

```
./docs/assets/
```

The directory is created automatically if it doesn't exist. Images are saved with timestamped filenames unless a custom path is specified.

## Common Use Cases

### Product Photography

```python
generate("Commercial product photo of wireless headphones, studio lighting, white background, professional photography")
```

### Social Media Assets

```python
# Square for Instagram
generate("Modern minimalist quote design", aspect_ratio='1:1')

# Story format
generate("Behind-the-scenes photo", aspect_ratio='9:16')
```

### Marketing Materials

```python
# Banner
generate("Website hero banner for tech startup", aspect_ratio='16:9')

# Poster
generate("Event poster design", aspect_ratio='3:4')
```

### Image Editing

```python
import PIL.Image

original = PIL.Image.open('photo.jpg')
edit_image("Add golden hour lighting effect", original)
```

## Troubleshooting

### API Key Not Found

```bash
# Verify environment variable
echo $GEMINI_API_KEY

# Check .env files
cat .claude/skills/gemini-image-gen/.env
cat .env
```

### Safety Filter Blocking

If content is blocked:
1. Review the safety ratings in the response
2. Adjust your prompt to be more specific
3. Consider adjusting safety settings if appropriate
4. See `references/safety-settings.md` for configuration options

### Image Quality Issues

For better results:
1. Add quality modifiers: "4K", "professional", "high detail"
2. Specify technical details: "35mm lens", "soft lighting"
3. Include style references: "impressionist style", "photorealistic"
4. See `references/prompting-guide.md` for advanced techniques

## Limitations

- Maximum 3 input images recommended for multi-image composition
- Text rendering limited to 25 characters per element
- Optimal language support: English, Spanish, Japanese, Mandarin, Hindi
- Regional restrictions on child images (EEA, CH, UK)
- No audio/video input support

## Resources

- [Official Documentation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Get API Key](https://aistudio.google.com/apikey)
- [Google AI Studio](https://aistudio.google.com) - Interactive testing
- [API Reference](https://ai.google.dev/api/generate-content)
- [Pricing Information](https://ai.google.dev/pricing)

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the reference documentation in `./references/`
2. Review [official documentation](https://ai.google.dev/gemini-api/docs/image-generation)
3. Test in [Google AI Studio](https://aistudio.google.com)
4. Report bugs or request features in the project repository

## Version

**1.0.0** - Initial release with Gemini 2.5 Flash Image support
