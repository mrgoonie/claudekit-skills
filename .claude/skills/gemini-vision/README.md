# Gemini Vision Skill

Google Gemini API skill for advanced image understanding tasks.

## Quick Start

1. **Get API Key**: https://aistudio.google.com/apikey
2. **Install SDK**: `pip install google-genai`
3. **Set API Key**:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

## Skill Structure

```
gemini-vision/
├── SKILL.md                 # Main skill file (auto-loaded by Claude)
├── README.md               # This file
├── scripts/                # Helper scripts
│   ├── analyze-image.py   # Main analysis script
│   ├── upload-file.py     # File upload helper
│   └── manage-files.py    # File management (list/get/delete)
└── references/            # Detailed documentation
    ├── api-reference.md   # API methods and endpoints
    ├── examples.md        # Code examples
    └── best-practices.md  # Advanced tips and optimization
```

## Usage

### Invoke the Skill

```bash
# In Claude Code CLI
/gemini-vision
```

Once loaded, Claude will have access to all Gemini Vision capabilities.

### Direct Script Usage

```bash
# Analyze single image
python scripts/analyze-image.py image.jpg "What's in this image?"

# Multiple images
python scripts/analyze-image.py img1.jpg img2.jpg "What's different?"

# Upload file
python scripts/upload-file.py large_image.jpg

# Manage files
python scripts/manage-files.py list
python scripts/manage-files.py get files/abc123
python scripts/manage-files.py delete files/abc123
```

## API Key Configuration

The skill checks for `GEMINI_API_KEY` in this order:

1. **Process environment** (recommended)
   ```bash
   export GEMINI_API_KEY="your-key"
   ```

2. **Skill directory**: `.claude/skills/gemini-vision/.env`
   ```
   GEMINI_API_KEY=your-api-key
   ```

3. **Project root**: `.env` or `.gemini_api_key`

## Capabilities

### Basic Features
- Image captioning and description
- Visual question answering
- Image classification
- Multi-image analysis (up to 3,600 images)

### Advanced Features
- **Object Detection** (Gemini 2.0+): Bounding boxes
- **Segmentation** (Gemini 2.5+): Pixel-level masks
- **Document Understanding**: PDF processing (up to 1,000 pages)

### Supported Formats
- Images: PNG, JPEG, WEBP, HEIC, HEIF
- Documents: PDF

## Models

- **gemini-2.5-pro**: Most capable, segmentation + detection
- **gemini-2.5-flash**: Fast and efficient (recommended)
- **gemini-2.5-flash-lite**: Lightweight, high volume
- **gemini-2.0-flash**: Object detection
- **gemini-1.5-pro/flash**: Previous generation

## Documentation

- **SKILL.md**: Quick reference and common usage patterns
- **references/api-reference.md**: Complete API documentation
- **references/examples.md**: Comprehensive code examples
- **references/best-practices.md**: Production tips and optimization

## Examples

### Python
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

with open('image.jpg', 'rb') as f:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(f.read(), mime_type='image/jpeg'),
            'Describe this image'
        ]
    )

print(response.text)
```

### JavaScript
```javascript
import { GoogleGenAI } from "@google/genai";
import fs from "node:fs";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const image = fs.readFileSync("image.jpg", { encoding: "base64" });

const response = await ai.models.generate({
  model: "gemini-2.5-flash",
  contents: [{
    parts: [
      { inline_data: { mime_type: "image/jpeg", data: image } },
      { text: "What's in this image?" }
    ]
  }]
});

console.log(response.text);
```

## Resources

- **Official Docs**: https://ai.google.dev/gemini-api/docs/image-understanding
- **API Reference**: https://ai.google.dev/gemini-api/docs/reference
- **Google AI Studio**: https://aistudio.google.com
- **Cookbook**: https://github.com/google-gemini/cookbook

## License

MIT
