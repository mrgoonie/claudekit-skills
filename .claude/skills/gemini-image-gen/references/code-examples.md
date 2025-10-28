# Gemini Image Generation Code Examples

Practical implementation examples for common use cases.

## Basic Examples

### Simple Text-to-Image

```python
from google import genai
from google.genai import types
import os

# Initialize client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Generate image
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A serene mountain landscape at sunset',
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
        print(f"Saved: output-{i}.png")
```

### Generate with Text Description

```python
# Generate both image and descriptive text
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A futuristic city with flying cars',
    config=types.GenerateContentConfig(
        response_modalities=['image', 'text'],
        aspect_ratio='16:9'
    )
)

# Process response
for part in response.candidates[0].content.parts:
    # Save images
    if hasattr(part, 'inline_data') and part.inline_data:
        with open('city.png', 'wb') as f:
            f.write(part.inline_data.data)

    # Print text
    if hasattr(part, 'text'):
        print(f"Description: {part.text}")
```

## Image Editing

### Add Elements to Existing Image

```python
import PIL.Image

# Load existing image
original = PIL.Image.open('photo.jpg')

# Add element
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Add a red balloon floating in the sky',
        original
    ],
    config=types.GenerateContentConfig(
        response_modalities=['image']
    )
)

# Save edited image
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('photo-with-balloon.png', 'wb') as f:
            f.write(part.inline_data.data)
```

### Remove Elements

```python
original = PIL.Image.open('scene.jpg')

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Remove the car from this image, keep everything else',
        original
    ]
)

# Save result
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('scene-no-car.png', 'wb') as f:
            f.write(part.inline_data.data)
```

### Style Transfer

```python
photo = PIL.Image.open('portrait.jpg')

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Transform this photo into an oil painting style, impressionist aesthetic',
        photo
    ]
)

# Save stylized version
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('portrait-oil-painting.png', 'wb') as f:
            f.write(part.inline_data.data)
```

## Multi-Image Composition

### Combine Two Images

```python
background = PIL.Image.open('landscape.jpg')
foreground = PIL.Image.open('subject.jpg')

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Place the subject from the second image into the landscape from the first image, maintaining consistent lighting',
        background,
        foreground
    ]
)

# Save composition
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('composite.png', 'wb') as f:
            f.write(part.inline_data.data)
```

### Create Collage

```python
img1 = PIL.Image.open('photo1.jpg')
img2 = PIL.Image.open('photo2.jpg')
img3 = PIL.Image.open('photo3.jpg')

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        'Create a horizontal collage layout with these three images arranged side by side with thin white borders',
        img1, img2, img3
    ],
    config=types.GenerateContentConfig(
        aspect_ratio='16:9'
    )
)

# Save collage
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open('collage.png', 'wb') as f:
            f.write(part.inline_data.data)
```

## Batch Processing

### Generate Multiple Variations

```python
def generate_variations(prompt, count=4, aspect_ratio='1:1'):
    """Generate multiple variations of the same prompt"""

    variations = []

    for i in range(count):
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['image'],
                aspect_ratio=aspect_ratio
            )
        )

        # Save each variation
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                filename = f'variation-{i}.png'
                with open(filename, 'wb') as f:
                    f.write(part.inline_data.data)
                variations.append(filename)
                print(f"Generated: {filename}")

    return variations

# Usage
variations = generate_variations(
    "Modern minimalist logo design",
    count=4,
    aspect_ratio='1:1'
)
```

### Batch Processing with Different Prompts

```python
def batch_generate(prompts, output_dir='./output'):
    """Generate images for multiple prompts"""

    import os
    os.makedirs(output_dir, exist_ok=True)

    results = []

    for idx, prompt in enumerate(prompts):
        print(f"Processing {idx + 1}/{len(prompts)}: {prompt}")

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['image']
                )
            )

            # Save image
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    filename = f'{output_dir}/image-{idx:03d}.png'
                    with open(filename, 'wb') as f:
                        f.write(part.inline_data.data)

                    results.append({
                        'prompt': prompt,
                        'filename': filename,
                        'success': True
                    })

        except Exception as e:
            print(f"Error: {e}")
            results.append({
                'prompt': prompt,
                'filename': None,
                'success': False,
                'error': str(e)
            })

    return results

# Usage
prompts = [
    "A serene mountain landscape",
    "Modern architecture design",
    "Abstract geometric art",
    "Vintage car illustration"
]

results = batch_generate(prompts)

# Print summary
for r in results:
    status = "✓" if r['success'] else "✗"
    print(f"{status} {r['prompt']}: {r.get('filename', r.get('error'))}")
```

## Error Handling

### Comprehensive Error Handler

```python
def safe_generate(prompt, max_retries=3, **config_kwargs):
    """Generate image with error handling and retries"""

    for attempt in range(max_retries):
        try:
            config = types.GenerateContentConfig(
                response_modalities=['image'],
                **config_kwargs
            )

            response = client.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=prompt,
                config=config
            )

            # Check if blocked by safety
            if response.candidates[0].finish_reason == 'SAFETY':
                print("Content blocked by safety filters")
                return None

            # Extract image
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    return part.inline_data.data

            print("No image in response")
            return None

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
                continue
            else:
                print("Max retries reached")
                raise

    return None

# Usage
image_data = safe_generate(
    "A peaceful garden scene",
    aspect_ratio='16:9'
)

if image_data:
    with open('garden.png', 'wb') as f:
        f.write(image_data)
```

### Handle Safety Blocks

```python
def generate_with_safety_check(prompt):
    """Generate image with detailed safety feedback"""

    response = client.models.generate_content(
        model='gemini-2.5-flash-image',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['image']
        )
    )

    # Check prompt feedback
    if response.prompt_feedback and response.prompt_feedback.block_reason:
        print("❌ Prompt blocked")
        print(f"Reason: {response.prompt_feedback.block_reason}")

        for rating in response.prompt_feedback.safety_ratings:
            print(f"  {rating.category}: {rating.probability}")

        return None

    # Check response
    candidate = response.candidates[0]

    if candidate.finish_reason == 'SAFETY':
        print("❌ Response blocked")

        for rating in candidate.safety_ratings:
            if rating.blocked:
                print(f"  {rating.category}: {rating.probability} (BLOCKED)")

        return None

    # Extract image
    for part in candidate.content.parts:
        if part.inline_data:
            return part.inline_data.data

    return None

# Usage
image_data = generate_with_safety_check("Your prompt")
if image_data:
    with open('output.png', 'wb') as f:
        f.write(image_data)
else:
    print("Generation failed or was blocked")
```

## Advanced Patterns

### Iterative Refinement

```python
class ImageIterator:
    """Iteratively refine an image through conversation"""

    def __init__(self, client, initial_prompt):
        self.client = client
        self.history = []
        self.current_image = None

        # Generate initial image
        self.refine(initial_prompt)

    def refine(self, instruction):
        """Apply refinement instruction"""

        # Build contents
        if self.current_image:
            contents = [instruction, self.current_image]
        else:
            contents = instruction

        # Generate
        response = self.client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=contents
        )

        # Extract image
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                # Convert bytes to PIL Image for next iteration
                from io import BytesIO
                self.current_image = PIL.Image.open(
                    BytesIO(part.inline_data.data)
                )

        # Track history
        self.history.append(instruction)

        return self.current_image

    def save(self, filename):
        """Save current image"""
        if self.current_image:
            self.current_image.save(filename)

# Usage
iterator = ImageIterator(client, "A cozy coffee shop interior")
iterator.refine("Add warm lighting from Edison bulbs")
iterator.refine("Add a person reading by the window")
iterator.refine("Make the colors more vibrant")
iterator.save("final-coffee-shop.png")
```

### Automated Asset Generation

```python
def generate_asset_set(base_prompt, aspects, output_dir='./assets'):
    """Generate a complete asset set with multiple aspect ratios"""

    import os
    os.makedirs(output_dir, exist_ok=True)

    asset_map = {
        'square': '1:1',       # Social media
        'landscape': '16:9',   # Banners
        'portrait': '9:16',    # Stories
        'classic': '4:3'       # Presentations
    }

    results = {}

    for name, ratio in asset_map.items():
        print(f"Generating {name} ({ratio})...")

        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=base_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['image'],
                aspect_ratio=ratio
            )
        )

        # Save
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                filename = f'{output_dir}/{name}.png'
                with open(filename, 'wb') as f:
                    f.write(part.inline_data.data)

                results[name] = {
                    'filename': filename,
                    'aspect_ratio': ratio
                }
                print(f"  Saved: {filename}")

    return results

# Usage
assets = generate_asset_set(
    "Modern tech startup branding illustration, minimalist style, blue and purple colors"
)

# Results include: square, landscape, portrait, classic variants
```

### A/B Testing Generator

```python
def generate_ab_variants(prompt, variations, aspect_ratio='1:1'):
    """Generate A/B test variants with slight modifications"""

    results = []

    for i, variation in enumerate(variations):
        full_prompt = f"{prompt}, {variation}"

        print(f"Generating variant {i + 1}: {variation}")

        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['image', 'text'],
                aspect_ratio=aspect_ratio
            )
        )

        # Extract results
        variant_data = {
            'variation': variation,
            'image': None,
            'description': None
        }

        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                filename = f'variant-{chr(65 + i)}.png'  # A, B, C, etc.
                with open(filename, 'wb') as f:
                    f.write(part.inline_data.data)
                variant_data['image'] = filename

            if hasattr(part, 'text'):
                variant_data['description'] = part.text

        results.append(variant_data)

    return results

# Usage
base = "Product hero image for modern headphones"
variants = [
    "minimalist white background",
    "dramatic black background with spotlight",
    "lifestyle setting with person wearing headphones"
]

ab_results = generate_ab_variants(base, variants, aspect_ratio='16:9')

# Print summary
for i, result in enumerate(ab_results):
    print(f"\nVariant {chr(65 + i)}: {result['variation']}")
    print(f"  Image: {result['image']}")
    print(f"  Description: {result['description']}")
```

## Integration Examples

### Flask API Endpoint

```python
from flask import Flask, request, send_file, jsonify
from io import BytesIO
import os

app = Flask(__name__)
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/generate', methods=['POST'])
def generate_image():
    """API endpoint for image generation"""

    data = request.json
    prompt = data.get('prompt')
    aspect_ratio = data.get('aspect_ratio', '1:1')

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['image'],
                aspect_ratio=aspect_ratio
            )
        )

        # Extract image
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                return send_file(
                    BytesIO(part.inline_data.data),
                    mimetype='image/png',
                    as_attachment=True,
                    download_name='generated.png'
                )

        return jsonify({'error': 'No image generated'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### CLI Tool

```python
#!/usr/bin/env python3
import click
from google import genai
import os

@click.command()
@click.argument('prompt')
@click.option('--aspect-ratio', '-a', default='1:1', help='Aspect ratio')
@click.option('--output', '-o', default='output.png', help='Output file')
def cli_generate(prompt, aspect_ratio, output):
    """CLI tool for image generation"""

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    click.echo(f"Generating: {prompt}")

    response = client.models.generate_content(
        model='gemini-2.5-flash-image',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['image'],
            aspect_ratio=aspect_ratio
        )
    )

    # Save image
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            with open(output, 'wb') as f:
                f.write(part.inline_data.data)
            click.echo(f"Saved: {output}")
            return

    click.echo("No image generated", err=True)

if __name__ == '__main__':
    cli_generate()
```

## Performance Optimization

### Concurrent Generation

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def generate_single(prompt, index):
    """Generate single image (thread-safe)"""

    response = client.models.generate_content(
        model='gemini-2.5-flash-image',
        contents=prompt
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data:
            filename = f'output-{index}.png'
            with open(filename, 'wb') as f:
                f.write(part.inline_data.data)
            return filename

    return None

def generate_concurrent(prompts, max_workers=4):
    """Generate multiple images concurrently"""

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(generate_single, prompt, i)
            for i, prompt in enumerate(prompts)
        ]

        results = [future.result() for future in futures]

    return results

# Usage
prompts = [
    "Mountain landscape",
    "Ocean sunset",
    "Forest path",
    "Desert dunes"
]

results = generate_concurrent(prompts, max_workers=4)
print(f"Generated {len([r for r in results if r])} images")
```

## Resources

- See `api-reference.md` for complete API documentation
- See `prompting-guide.md` for prompt engineering strategies
- See `safety-settings.md` for content filtering configuration
