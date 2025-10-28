# Gemini Image Generation Safety Settings

Comprehensive guide to configuring content safety filters for image generation.

## Overview

The Gemini API includes adjustable safety filters to block potentially harmful content across multiple categories. Safety settings can be configured per-request to balance content filtering with your application's needs.

## Safety Categories

The API filters content across **4 main categories**:

| Category | Constant | Description |
|----------|----------|-------------|
| **Harassment** | `HARM_CATEGORY_HARASSMENT` | Negative or harmful comments targeting identity and/or protected attributes |
| **Hate Speech** | `HARM_CATEGORY_HATE_SPEECH` | Content that is rude, disrespectful, or profane |
| **Sexually Explicit** | `HARM_CATEGORY_SEXUALLY_EXPLICIT` | References to sexual acts or other lewd content |
| **Dangerous Content** | `HARM_CATEGORY_DANGEROUS_CONTENT` | Promotes, facilitates, or encourages harmful acts |

**Note**: Civic integrity and other categories are only available for Legacy PaLM 2 models, not Gemini models.

## Block Thresholds

Configure how aggressively content is filtered:

| Threshold | Constant | Behavior |
|-----------|----------|----------|
| **Off** | `OFF` | Turn off safety filter completely |
| **Block None** | `BLOCK_NONE` | Show content regardless of probability |
| **Block Few** | `BLOCK_ONLY_HIGH` | Block only HIGH probability unsafe content |
| **Block Some** | `BLOCK_MEDIUM_AND_ABOVE` | Block MEDIUM and HIGH probability content |
| **Block Most** | `BLOCK_LOW_AND_ABOVE` | Block LOW, MEDIUM, and HIGH probability content |
| **Unspecified** | `HARM_BLOCK_THRESHOLD_UNSPECIFIED` | Use default threshold |

## Probability Levels

Content is rated by **probability** of being unsafe:

- **NEGLIGIBLE** - Very unlikely to be harmful
- **LOW** - Low probability of harm
- **MEDIUM** - Moderate probability of harm
- **HIGH** - High probability of harm

**Important**: The API blocks based on **probability**, not severity. Low-probability content might still contain high-severity harm.

## Default Behavior

### Default Thresholds

- **Newer stable GA models**: Block none by default
- **Other models**: Block some (MEDIUM_AND_ABOVE) by default
- **Google AI Studio**: Cannot completely disable safety settings

### Built-in Protections

**Always blocked** (cannot be configured):
- Child safety content
- Core harmful content categories

These protections cannot be disabled or adjusted.

## Configuration Examples

### Python SDK

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="your-api-key")

# Configure safety settings
config = types.GenerateContentConfig(
    response_modalities=['image'],
    aspect_ratio='16:9',
    safety_settings=[
        # Block only high-probability harassment
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
        ),
        # Block medium and high hate speech
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        # Block all sexually explicit content
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        ),
        # Block dangerous content
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )
    ]
)

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='Your prompt here',
    config=config
)
```

### REST API

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Your prompt here"
      }]
    }],
    "safetySettings": [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_LOW_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      }
    ]
  }'
```

## Reading Safety Feedback

### Prompt Blocking

When a prompt is blocked:

```python
response = client.models.generate_content(...)

# Check if prompt was blocked
if response.prompt_feedback:
    if response.prompt_feedback.block_reason:
        print(f"Prompt blocked: {response.prompt_feedback.block_reason}")

    # View safety ratings
    for rating in response.prompt_feedback.safety_ratings:
        print(f"Category: {rating.category}")
        print(f"Probability: {rating.probability}")
```

**Block reasons**:
- `BLOCK_REASON_UNSPECIFIED`
- `SAFETY` - Blocked due to safety filters
- `OTHER` - Other blocking reason

### Response Blocking

When a response is blocked:

```python
# Check finish reason
for candidate in response.candidates:
    if candidate.finish_reason == 'SAFETY':
        print("Response blocked due to safety filters")

        # View detailed safety ratings
        for rating in candidate.safety_ratings:
            print(f"Category: {rating.category}")
            print(f"Probability: {rating.probability}")
            print(f"Blocked: {rating.blocked}")
```

### Full Safety Check Example

```python
def check_safety(response):
    """Check if content was blocked and why"""

    # Check prompt feedback
    if response.prompt_feedback:
        if response.prompt_feedback.block_reason:
            print("⚠️ Prompt was blocked")
            print(f"Reason: {response.prompt_feedback.block_reason}")

            for rating in response.prompt_feedback.safety_ratings:
                print(f"  {rating.category}: {rating.probability}")
            return False

    # Check response candidates
    if not response.candidates:
        print("⚠️ No candidates returned")
        return False

    candidate = response.candidates[0]

    if candidate.finish_reason == 'SAFETY':
        print("⚠️ Response was blocked by safety filters")

        for rating in candidate.safety_ratings:
            if rating.blocked:
                print(f"  {rating.category}: {rating.probability} (BLOCKED)")
            else:
                print(f"  {rating.category}: {rating.probability}")
        return False

    return True

# Usage
response = client.models.generate_content(...)
if check_safety(response):
    # Process response
    pass
else:
    # Handle blocked content
    pass
```

## Configuration Strategies

### Permissive (Content Creation)

For creative applications where flexibility is important:

```python
safety_settings=[
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
    )
]
```

### Balanced (General Use)

For general applications:

```python
safety_settings=[
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    )
]
```

### Restrictive (Public/Educational)

For public-facing or educational applications:

```python
safety_settings=[
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    )
]
```

### Category-Specific

Different thresholds for different categories:

```python
safety_settings=[
    # More permissive for harassment (artistic expression)
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    # Stricter for hate speech
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    # Very strict for sexually explicit
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    # Moderate for dangerous content
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    )
]
```

## Best Practices

### Testing and Iteration

1. **Start with defaults**: Use default settings initially
2. **Test edge cases**: Try prompts that might trigger filters
3. **Adjust incrementally**: Make small changes to thresholds
4. **Monitor feedback**: Log safety ratings to understand patterns
5. **Document decisions**: Record why certain thresholds were chosen

### Handling Blocked Content

```python
def generate_with_retry(prompt, max_retries=3):
    """Generate image with automatic retry on safety blocks"""

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=prompt,
                config=config
            )

            # Check if blocked
            if response.candidates[0].finish_reason == 'SAFETY':
                print(f"Attempt {attempt + 1} blocked. Adjusting prompt...")
                # Modify prompt or adjust safety settings
                prompt = modify_prompt(prompt)
                continue

            return response

        except Exception as e:
            print(f"Error: {e}")
            if attempt < max_retries - 1:
                continue
            raise

    return None
```

### User Communication

When content is blocked, provide clear feedback:

```python
if candidate.finish_reason == 'SAFETY':
    blocked_categories = [
        rating.category
        for rating in candidate.safety_ratings
        if rating.blocked
    ]

    message = f"Content generation was blocked due to: {', '.join(blocked_categories)}"
    message += "\nPlease try a different prompt or contact support."

    return {"error": message, "categories": blocked_categories}
```

## Regional Restrictions

### Child Image Restrictions

Uploading images of children is **restricted** in:
- European Economic Area (EEA)
- Switzerland (CH)
- United Kingdom (UK)

Requests from these regions with child images will be rejected regardless of safety settings.

## Compliance Considerations

### Terms of Service

Applications using less restrictive safety settings may be subject to review per [Google's Terms of Service](https://ai.google.dev/terms).

**Required**:
- Review terms before deploying with custom settings
- Implement additional content moderation if needed
- Monitor usage for policy compliance

### Responsible AI

Consider these factors when configuring safety:

1. **User base**: Who will use your application?
2. **Use case**: What is the application's purpose?
3. **Context**: Where will generated content appear?
4. **Risk tolerance**: What level of risk is acceptable?
5. **Mitigation**: What additional safeguards are in place?

## Debugging Safety Issues

### Common Issues

**Issue**: Legitimate content being blocked

**Solution**:
1. Check which category triggered the block
2. Review threshold for that category
3. Consider adjusting to next less restrictive level
4. Test with variations of the prompt

**Issue**: Inconsistent blocking

**Solution**:
1. Review probability levels (content near threshold)
2. Make prompts more specific
3. Add context to clarify intent
4. Use system instructions to set tone

**Issue**: Unable to generate certain content types

**Solution**:
1. Verify content doesn't violate core protections
2. Check regional restrictions
3. Review Terms of Service
4. Consider alternative approaches

### Logging for Analysis

```python
import json
from datetime import datetime

def log_safety_feedback(prompt, response):
    """Log safety feedback for analysis"""

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "blocked": False,
        "block_reason": None,
        "safety_ratings": []
    }

    if response.prompt_feedback:
        log_entry["block_reason"] = response.prompt_feedback.block_reason
        log_entry["blocked"] = bool(response.prompt_feedback.block_reason)

        for rating in response.prompt_feedback.safety_ratings:
            log_entry["safety_ratings"].append({
                "category": str(rating.category),
                "probability": str(rating.probability),
                "blocked": rating.blocked
            })

    if response.candidates:
        candidate = response.candidates[0]
        if candidate.finish_reason == 'SAFETY':
            log_entry["blocked"] = True

    # Write to log file
    with open('safety_log.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

    return log_entry
```

## Resources

- [Official Safety Documentation](https://ai.google.dev/gemini-api/docs/safety-settings)
- [Responsible AI Practices](https://ai.google.dev/responsible)
- [Terms of Service](https://ai.google.dev/terms)
- [Jigsaw Team: Probability vs Severity](https://medium.com/jigsaw/a-framework-for-shaping-our-technology-3088a8d89de2)
