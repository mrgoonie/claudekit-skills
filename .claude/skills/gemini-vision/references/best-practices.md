# Gemini Vision API - Best Practices

Advanced tips and optimization strategies for production use.

## Table of Contents

1. [API Key Management](#api-key-management)
2. [Image Quality & Preparation](#image-quality--preparation)
3. [Prompt Engineering](#prompt-engineering)
4. [Performance Optimization](#performance-optimization)
5. [Cost Optimization](#cost-optimization)
6. [Error Handling](#error-handling)
7. [File Management](#file-management)
8. [Production Deployment](#production-deployment)

---

## API Key Management

### Security Best Practices

**DO:**
- ✅ Store API keys in environment variables
- ✅ Use secret management services (AWS Secrets Manager, Google Secret Manager)
- ✅ Add API key restrictions in Google Cloud Console
- ✅ Rotate keys regularly (every 90 days)
- ✅ Monitor usage for anomalies
- ✅ Use separate keys for dev/staging/prod

**DON'T:**
- ❌ Commit API keys to version control
- ❌ Hardcode keys in source code
- ❌ Share keys via email or Slack
- ❌ Use production keys in development
- ❌ Expose keys in client-side code
- ❌ Log API keys in error messages

### Key Restrictions

Configure in Google Cloud Console:

1. **Application restrictions**:
   - HTTP referrers (websites)
   - IP addresses (servers)
   - Android apps
   - iOS apps

2. **API restrictions**:
   - Limit to specific Google APIs
   - Only enable Generative Language API

3. **Usage quotas**:
   - Set daily request limits
   - Alert on unusual activity

---

## Image Quality & Preparation

### Image Quality Guidelines

**High-quality images produce better results:**

- ✅ Clear, well-lit images
- ✅ Correct orientation
- ✅ Appropriate resolution (not too small)
- ✅ Minimal compression artifacts
- ✅ Focused subject matter

**Avoid:**

- ❌ Blurry or out-of-focus images
- ❌ Heavily compressed images
- ❌ Rotated or upside-down images
- ❌ Very dark or overexposed images
- ❌ Watermarked images (may confuse model)

### Image Preprocessing

```python
from PIL import Image, ImageEnhance

def prepare_image(input_path, output_path):
    """Prepare image for optimal Gemini analysis."""
    img = Image.open(input_path)

    # 1. Auto-rotate based on EXIF data
    try:
        from PIL.ExifTags import TAGS
        exif = img._getexif()
        if exif:
            orientation = exif.get(274)  # Orientation tag
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except:
        pass

    # 2. Enhance contrast if needed
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)

    # 3. Convert to RGB (remove alpha channel)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1])
        img = background

    # 4. Save with good quality
    img.save(output_path, 'JPEG', quality=95)
    return output_path
```

### Resolution Guidelines

**For optimal token usage:**

- Small images (≤384px): 258 tokens
- Keep important images at 768px max dimension
- Large images (>768px) get tiled, increasing cost

```python
def optimize_resolution(image_path, target_size=768):
    """Resize to minimize tokens while keeping quality."""
    img = Image.open(image_path)
    w, h = img.size

    # Already optimal
    if max(w, h) <= target_size:
        return img

    # Calculate new dimensions
    if w > h:
        new_w = target_size
        new_h = int(h * target_size / w)
    else:
        new_h = target_size
        new_w = int(w * target_size / h)

    return img.resize((new_w, new_h), Image.LANCZOS)
```

---

## Prompt Engineering

### Effective Prompts

**Be Specific:**
```python
# Vague ❌
"What's in the image?"

# Specific ✅
"List all vehicles visible in the image with their colors and approximate positions."
```

**Specify Output Format:**
```python
# No format ❌
"Tell me about this product."

# With format ✅
"Analyze this product and return JSON with: name, category, colors, features, and estimated price range."
```

**Use Context:**
```python
# No context ❌
"Is this good quality?"

# With context ✅
"You are a professional photographer. Evaluate this image's composition, lighting, and technical quality. Rate from 1-10 and explain."
```

### Multi-Turn Conversations

For complex analysis, break into steps:

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

# Upload once
uploaded_file = client.files.upload(file="complex_scene.jpg")

# Step 1: Overview
response1 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[uploaded_file, "Describe the overall scene."]
)

# Step 2: Details
response2 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[uploaded_file, f"Based on this scene: {response1.text}\n\nNow identify all people and their activities."]
)

# Step 3: Analysis
response3 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[uploaded_file, f"Given: {response2.text}\n\nWhat social dynamics are present?"]
)
```

### Few-Shot Learning

Provide examples for better accuracy:

```python
prompt = """I'll show you examples of 'high quality' vs 'low quality' product photos, then you'll evaluate a new photo.

HIGH QUALITY examples:
- Clean white background
- Sharp focus on product
- Even lighting, no harsh shadows
- Multiple angles shown

LOW QUALITY examples:
- Cluttered background
- Blurry or poor focus
- Harsh lighting or dark shadows
- Only one angle

Now evaluate this product photo and explain your rating."""
```

---

## Performance Optimization

### Model Selection

Choose the right model for your use case:

| Model | Use Case | Speed | Cost |
|-------|----------|-------|------|
| gemini-2.5-pro | Highest quality, complex analysis | Slower | Higher |
| gemini-2.5-flash | Balanced quality/speed | Fast | Medium |
| gemini-2.5-flash-lite | Simple tasks, high volume | Fastest | Lowest |
| gemini-2.0-flash | Need object detection | Fast | Medium |

**Guidelines:**
- Prototype with Flash, upgrade to Pro if needed
- Use Flash-Lite for simple captioning/classification
- Use 2.0+ only when detection/segmentation needed
- Consider latency requirements

### Parallel Processing

Process multiple images concurrently:

```python
import concurrent.futures
from google import genai

def process_batch(image_paths, max_workers=10):
    """Process images in parallel."""
    client = genai.Client(api_key="YOUR_API_KEY")

    def process_one(path):
        with open(path, 'rb') as f:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(f.read(), mime_type='image/jpeg'),
                    'Caption this image.'
                ]
            )
        return {'path': path, 'result': response.text}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_one, image_paths))

    return results
```

### Caching Strategies

Cache results to avoid redundant API calls:

```python
import hashlib
import json
from pathlib import Path

class GeminiCache:
    def __init__(self, cache_dir='.cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_key(self, image_bytes, prompt, model):
        """Generate cache key from inputs."""
        content = image_bytes + prompt.encode() + model.encode()
        return hashlib.sha256(content).hexdigest()

    def get(self, image_bytes, prompt, model):
        """Get cached result if exists."""
        key = self._get_key(image_bytes, prompt, model)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None

    def set(self, image_bytes, prompt, model, result):
        """Save result to cache."""
        key = self._get_key(image_bytes, prompt, model)
        cache_file = self.cache_dir / f"{key}.json"

        with open(cache_file, 'w') as f:
            json.dump(result, f)

# Usage
cache = GeminiCache()

with open('image.jpg', 'rb') as f:
    image_bytes = f.read()

cached = cache.get(image_bytes, prompt, model)
if cached:
    print("Using cached result")
    result = cached
else:
    print("Calling API")
    result = analyze_image(image_bytes, prompt, model)
    cache.set(image_bytes, prompt, model, result)
```

---

## Cost Optimization

### Token Management

**Minimize token usage:**

1. **Resize images** to optimal dimensions (≤768px)
2. **Use File API** for repeated analysis (upload once, use many times)
3. **Batch related questions** in single request
4. **Choose smaller models** when appropriate

### Calculate Costs Before Processing

```python
def estimate_tokens(width, height):
    """Estimate token cost for image."""
    if width <= 384 and height <= 384:
        return 258

    crop_unit = min(width, height) // 1.5
    tiles_x = width / crop_unit
    tiles_y = height / crop_unit
    total_tiles = tiles_x * tiles_y

    return int(total_tiles * 258)

def estimate_cost(image_path, model='gemini-2.5-flash'):
    """Estimate API cost for image analysis."""
    from PIL import Image

    img = Image.open(image_path)
    tokens = estimate_tokens(img.width, img.height)

    # Add prompt tokens (estimate ~50)
    total_tokens = tokens + 50

    # Pricing (example, check current rates)
    rates = {
        'gemini-2.5-pro': 0.000125,  # per 1K tokens
        'gemini-2.5-flash': 0.0000375,
        'gemini-2.5-flash-lite': 0.00001875,
    }

    cost = (total_tokens / 1000) * rates.get(model, 0.0000375)
    return {
        'tokens': total_tokens,
        'cost_usd': round(cost, 6),
        'model': model
    }

# Use it
info = estimate_cost('large_image.jpg')
print(f"Estimated cost: ${info['cost_usd']} ({info['tokens']} tokens)")
```

### Batch Processing Strategy

```python
def smart_batch_process(image_paths, budget_usd=1.00):
    """Process images within budget."""
    total_cost = 0
    results = []

    for path in image_paths:
        est = estimate_cost(path)

        if total_cost + est['cost_usd'] > budget_usd:
            print(f"Budget exceeded. Processed {len(results)} images.")
            break

        # Process image
        result = process_image(path)
        results.append(result)
        total_cost += est['cost_usd']

    print(f"Total cost: ${total_cost:.4f}")
    return results
```

---

## Error Handling

### Comprehensive Error Handling

```python
from google import genai
import time

class GeminiError(Exception):
    """Base exception for Gemini errors."""
    pass

class RateLimitError(GeminiError):
    """Rate limit exceeded."""
    pass

class InvalidAPIKeyError(GeminiError):
    """Invalid API key."""
    pass

def analyze_with_error_handling(image_bytes, prompt, model='gemini-2.5-flash', max_retries=3):
    """Robust image analysis with error handling."""
    client = genai.Client(api_key="YOUR_API_KEY")

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                    prompt
                ]
            )
            return response.text

        except Exception as e:
            error_str = str(e)

            # Rate limit
            if '429' in error_str:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2
                    print(f"Rate limited. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise RateLimitError("Rate limit exceeded after retries")

            # Invalid API key
            elif '401' in error_str or '403' in error_str:
                raise InvalidAPIKeyError("Invalid or unauthorized API key")

            # Invalid request
            elif '400' in error_str:
                raise GeminiError(f"Invalid request: {error_str}")

            # Server error
            elif '500' in error_str or '503' in error_str:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                raise GeminiError(f"Server error after retries: {error_str}")

            # Unknown error
            else:
                raise GeminiError(f"Unexpected error: {error_str}")

    raise GeminiError("Max retries exceeded")
```

---

## File Management

### Efficient File Upload Strategy

```python
from google import genai
from datetime import datetime, timedelta

class FileManager:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.uploaded_files = {}  # Track uploaded files

    def upload_if_needed(self, file_path, reuse_hours=24):
        """Upload file only if not already uploaded recently."""
        file_id = self.uploaded_files.get(file_path)

        if file_id:
            # Check if file still exists
            try:
                self.client.files.get(name=file_id)
                print(f"Reusing existing file: {file_id}")
                return file_id
            except:
                # File expired, remove from tracking
                del self.uploaded_files[file_path]

        # Upload new file
        uploaded = self.client.files.upload(file=file_path)
        self.uploaded_files[file_path] = uploaded.name
        print(f"Uploaded new file: {uploaded.name}")
        return uploaded.name

    def cleanup(self):
        """Delete all tracked files."""
        for file_path, file_id in self.uploaded_files.items():
            try:
                self.client.files.delete(name=file_id)
                print(f"Deleted: {file_id}")
            except:
                pass
        self.uploaded_files.clear()

# Usage
fm = FileManager(api_key="YOUR_API_KEY")

# Upload once
file_id = fm.upload_if_needed('large_image.jpg')

# Use multiple times
for prompt in ['Caption this', 'What colors?', 'Any text?']:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[types.File(name=file_id), prompt]
    )
    print(response.text)

# Cleanup when done
fm.cleanup()
```

---

## Production Deployment

### Monitoring & Logging

```python
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gemini_api.log'),
        logging.StreamHandler()
    ]
)

def log_api_call(image_path, prompt, model, tokens, duration, success, error=None):
    """Log API call for monitoring."""
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'image': image_path,
        'prompt_length': len(prompt),
        'model': model,
        'tokens': tokens,
        'duration_ms': duration * 1000,
        'success': success,
        'error': str(error) if error else None
    }

    if success:
        logging.info(f"API call succeeded: {log_data}")
    else:
        logging.error(f"API call failed: {log_data}")

    return log_data
```

### Rate Limiting

```python
from collections import deque
from time import time, sleep

class RateLimiter:
    def __init__(self, max_requests_per_minute=15):
        self.max_rpm = max_requests_per_minute
        self.requests = deque()

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time()

        # Remove requests older than 1 minute
        while self.requests and self.requests[0] < now - 60:
            self.requests.popleft()

        # If at limit, wait
        if len(self.requests) >= self.max_rpm:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                print(f"Rate limit approaching. Waiting {sleep_time:.1f}s...")
                sleep(sleep_time)

        self.requests.append(now)

# Usage
limiter = RateLimiter(max_requests_per_minute=15)

for image_path in image_paths:
    limiter.wait_if_needed()
    result = process_image(image_path)
```

### Health Checks

```python
def health_check():
    """Verify API is accessible."""
    try:
        client = genai.Client(api_key="YOUR_API_KEY")

        # Simple test request
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=['Hello, are you there?']
        )

        return {
            'status': 'healthy',
            'latency_ms': None,  # Measure if needed
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
```

---

## Additional Resources

- **Official Docs**: https://ai.google.dev/gemini-api/docs
- **Pricing**: https://ai.google.dev/gemini-api/docs/pricing
- **Rate Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
- **Community Forum**: https://discuss.ai.google.dev
- **Cookbook**: https://github.com/google-gemini/cookbook
