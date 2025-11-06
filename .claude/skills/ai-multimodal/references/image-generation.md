# Image Generation Reference

Comprehensive guide for image creation, editing, and composition using Gemini API.

## Core Capabilities

- **Text-to-Image**: Generate images from text prompts
- **Image Editing**: Modify existing images with text instructions
- **Multi-Image Composition**: Combine up to 3 images
- **Iterative Refinement**: Refine images conversationally
- **Aspect Ratios**: Multiple formats (1:1, 16:9, 9:16, 4:3, 3:4)
- **Style Control**: Control artistic style and quality
- **Text in Images**: Limited text rendering (max 25 chars)

## Model

**gemini-2.5-flash-image** - Specialized for image generation
- Input tokens: 65,536
- Output tokens: 32,768
- Knowledge cutoff: June 2025
- Supports: Text and image inputs, image outputs

## Quick Start

### Basic Generation

```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A serene mountain landscape at sunset with snow-capped peaks',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='16:9'
    )
)

# Save image
for i, part in enumerate(response.candidates[0].content.parts):
    if part.inline_data:
        with open(f'output-{i}.png', 'wb') as f:
            f.write(part.inline_data.data)
```

## Aspect Ratios

| Ratio | Resolution | Use Case | Token Cost |
|-------|-----------|----------|------------|
| 1:1 | 1024×1024 | Social media, avatars | 1290 |
| 16:9 | 1344×768 | Landscapes, banners | 1290 |
| 9:16 | 768×1344 | Mobile, portraits | 1290 |
| 4:3 | 1152×896 | Traditional media | 1290 |
| 3:4 | 896×1152 | Vertical posters | 1290 |

All ratios cost the same: 1,290 tokens per image.

## Response Modalities

### Image Only

```python
config = types.GenerateContentConfig(
    response_modalities=['image'],
    aspect_ratio='1:1'
)
```

### Text Only (No Image)

```python
config = types.GenerateContentConfig(
    response_modalities=['text']
)
# Returns text description instead of generating image
```

### Both Image and Text

```python
config = types.GenerateContentConfig(
    response_modalities=['image', 'text'],
    aspect_ratio='16:9'
)
# Returns both generated image and description
```

## Image Editing

### Modify Existing Image

```python
import PIL.Image

# Load original
img = PIL.Image.open('original.png')

# Edit with instructions
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Add a red balloon floating in the sky',
        img
    ],
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='16:9'
    )
)
```

### Style Transfer

```python
img = PIL.Image.open('photo.jpg')

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Transform this into an oil painting style',
        img
    ]
)
```

### Object Addition/Removal

```python
# Add object
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Add a vintage car parked on the street',
        img
    ]
)

# Remove object
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Remove the person on the left side',
        img
    ]
)
```

## Multi-Image Composition

### Combine Multiple Images

```python
img1 = PIL.Image.open('background.png')
img2 = PIL.Image.open('foreground.png')
img3 = PIL.Image.open('overlay.png')

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Combine these images into a cohesive scene',
        img1,
        img2,
        img3
    ],
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='16:9'
    )
)
```

**Note**: Recommended maximum 3 input images for best results.

## Prompt Engineering

### Effective Prompt Structure

**Three key elements**:
1. **Subject**: What to generate
2. **Context**: Environmental setting
3. **Style**: Artistic treatment

**Example**: "A robot [subject] in a futuristic city [context], cyberpunk style with neon lighting [style]"

### Quality Modifiers

**Technical terms**:
- "4K", "8K", "high resolution"
- "HDR", "high dynamic range"
- "professional photography"
- "studio lighting"
- "ultra detailed"

**Camera settings**:
- "35mm lens", "50mm lens"
- "shallow depth of field"
- "wide angle shot"
- "macro photography"
- "golden hour lighting"

### Style Keywords

**Art styles**:
- "oil painting", "watercolor", "sketch"
- "digital art", "concept art"
- "photorealistic", "hyperrealistic"
- "minimalist", "abstract"
- "cyberpunk", "steampunk", "fantasy"

**Mood and atmosphere**:
- "dramatic lighting", "soft lighting"
- "moody", "bright and cheerful"
- "mysterious", "whimsical"
- "dark and gritty", "pastel colors"

### Subject Description

**Be specific**:
- ❌ "A cat"
- ✅ "A fluffy orange tabby cat with green eyes"

**Add context**:
- ❌ "A building"
- ✅ "A modern glass skyscraper reflecting sunset clouds"

**Include details**:
- ❌ "A person"
- ✅ "A young woman in a red dress holding an umbrella"

### Composition and Framing

**Camera angles**:
- "bird's eye view", "aerial shot"
- "low angle", "high angle"
- "close-up", "wide shot"
- "centered composition"
- "rule of thirds"

**Perspective**:
- "first person view"
- "third person perspective"
- "isometric view"
- "forced perspective"

### Text in Images

**Limitations**:
- Maximum 25 characters total
- Up to 3 distinct text phrases
- Works best with simple text

**Best practices**:
```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A vintage poster with bold text "EXPLORE" at the top, mountain landscape, retro 1950s style'
)
```

**Font control**:
- "bold sans-serif title"
- "handwritten script"
- "vintage letterpress"
- "modern minimalist font"

## Advanced Techniques

### Iterative Refinement

```python
# Initial generation
response1 = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A futuristic city skyline'
)

# Save first version
with open('v1.png', 'wb') as f:
    f.write(response1.candidates[0].content.parts[0].inline_data.data)

# Refine
img = PIL.Image.open('v1.png')
response2 = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Add flying vehicles and neon signs',
        img
    ]
)
```

### Negative Prompts (Indirect)

```python
# Instead of "no blur", be specific about what you want
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A crystal clear, sharp photograph of a diamond ring with perfect focus and high detail'
)
```

### Consistent Style Across Images

```python
base_prompt = "Digital art, vibrant colors, cel-shaded style, clean lines"

prompts = [
    f"{base_prompt}, a warrior character",
    f"{base_prompt}, a mage character",
    f"{base_prompt}, a rogue character"
]

for i, prompt in enumerate(prompts):
    response = client.models.generate_content(
        model='gemini-2.5-flash-image',
        contents=prompt
    )
    # Save each character
```

## Safety Settings

### Configure Safety Filters

```python
config = types.GenerateContentConfig(
    response_modalities=['image'],
    safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )
    ]
)
```

### Available Categories

- `HARM_CATEGORY_HATE_SPEECH`
- `HARM_CATEGORY_DANGEROUS_CONTENT`
- `HARM_CATEGORY_HARASSMENT`
- `HARM_CATEGORY_SEXUALLY_EXPLICIT`

### Thresholds

- `BLOCK_NONE`: No blocking
- `BLOCK_LOW_AND_ABOVE`: Block low probability and above
- `BLOCK_MEDIUM_AND_ABOVE`: Block medium and above (default)
- `BLOCK_ONLY_HIGH`: Block only high probability

## Common Use Cases

### 1. Marketing Assets

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='''Professional product photography:
    - Sleek smartphone on minimalist white surface
    - Dramatic side lighting creating subtle shadows
    - Shallow depth of field, crisp focus
    - Clean, modern aesthetic
    - 4K quality
    ''',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='4:3'
    )
)
```

### 2. Concept Art

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='''Fantasy concept art:
    - Ancient floating islands connected by chains
    - Waterfalls cascading into clouds below
    - Magical crystals glowing on the islands
    - Epic scale, dramatic lighting
    - Detailed digital painting style
    ''',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='16:9'
    )
)
```

### 3. Social Media Graphics

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='''Instagram post design:
    - Pastel gradient background (pink to blue)
    - Motivational quote layout
    - Modern minimalist style
    - Clean typography
    - Mobile-friendly composition
    ''',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='1:1'
    )
)
```

### 4. Illustration

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='''Children's book illustration:
    - Friendly cartoon dragon reading a book
    - Bright, cheerful colors
    - Soft, rounded shapes
    - Whimsical forest background
    - Warm, inviting atmosphere
    ''',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='4:3'
    )
)
```

### 5. UI/UX Mockups

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='''Modern mobile app interface:
    - Clean dashboard design
    - Card-based layout
    - Soft shadows and gradients
    - Contemporary color scheme (blue and white)
    - Professional fintech aesthetic
    ''',
    config=types.GenerateContentConfig(
        response_modalities=['image'],
        aspect_ratio='9:16'
    )
)
```

## Best Practices

### Prompt Quality

1. **Be specific**: More detail = better results
2. **Order matters**: Most important elements first
3. **Use examples**: Reference known styles or artists
4. **Avoid contradictions**: Don't ask for opposing styles
5. **Test and iterate**: Refine prompts based on results

### File Management

```python
# Save with descriptive names
timestamp = int(time.time())
filename = f'generated_{timestamp}_{aspect_ratio}.png'

with open(filename, 'wb') as f:
    f.write(image_data)
```

### Cost Optimization

**Token costs**:
- 1 image: 1,290 tokens = $0.00129 (Flash Image at $1/1M)
- 10 images: 12,900 tokens = $0.0129
- 100 images: 129,000 tokens = $0.129

**Strategies**:
- Generate fewer iterations
- Use text modality first to validate concept
- Batch similar requests
- Cache prompts for consistent style

## Error Handling

### Safety Filter Blocking

```python
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash-image',
        contents=prompt
    )
except Exception as e:
    # Check block reason
    if hasattr(e, 'prompt_feedback'):
        print(f"Blocked: {e.prompt_feedback.block_reason}")
        # Modify prompt and retry
```

### Token Limit Exceeded

```python
# Keep prompts concise
if len(prompt) > 1000:
    # Truncate or simplify
    prompt = prompt[:1000]
```

## Limitations

- Maximum 3 input images for composition
- Text rendering limited (25 chars max)
- No video or animation generation
- Regional restrictions (child images in EEA, CH, UK)
- Optimal language support: English, Spanish (Mexico), Japanese, Mandarin, Hindi
- No real-time generation
- Cannot perfectly replicate specific people or copyrighted characters

## Troubleshooting

### aspect_ratio Parameter Error

**Error**: `Extra inputs are not permitted [type=extra_forbidden, input_value='1:1', input_type=str]`

**Cause**: The `aspect_ratio` parameter must be nested inside an `image_config` object, not passed directly to `GenerateContentConfig`.

**Incorrect Usage**:
```python
# ❌ This will fail
config = types.GenerateContentConfig(
    response_modalities=['image'],
    aspect_ratio='16:9'  # Wrong - not a direct parameter
)
```

**Correct Usage**:
```python
# ✅ Correct implementation
config = types.GenerateContentConfig(
    response_modalities=['Image'],  # Note: Capital 'I'
    image_config=types.ImageConfig(
        aspect_ratio='16:9'
    )
)
```

### Response Modality Case Sensitivity

The `response_modalities` parameter expects capital case values:
- ✅ Correct: `['Image']`, `['Text']`, `['Image', 'Text']`
- ❌ Wrong: `['image']`, `['text']`
