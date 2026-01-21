---
name: chrome-devtools
description: Browser automation, debugging, and performance analysis using Puppeteer CLI scripts. Use for automating browsers, taking screenshots, analyzing performance, monitoring network traffic, web scraping, form automation, and JavaScript debugging.
license: Apache-2.0
---

# Chrome DevTools Agent Skill

Browser automation via executable Puppeteer scripts. All scripts output JSON for easy parsing.

## Quick Start

**CRITICAL**: Always check `pwd` before running scripts.

### Installation

#### Step 1: Install System Dependencies (Linux/WSL only)

On Linux/WSL, Chrome requires system libraries. Install them first:

```bash
pwd  # Should show current working directory
cd .claude/skills/chrome-devtools/scripts
./install-deps.sh  # Auto-detects OS and installs required libs
```

Supports: Ubuntu, Debian, Fedora, RHEL, CentOS, Arch, Manjaro

**macOS/Windows**: Skip this step (dependencies bundled with Chrome)

#### Step 2: Install Node Dependencies

```bash
npm install  # Installs puppeteer, debug, yargs
```

#### Step 3: Install ImageMagick (Optional, Recommended)

ImageMagick enables automatic screenshot compression to keep files under 5MB:

**macOS:**

```bash
brew install imagemagick
```

**Ubuntu/Debian/WSL:**

```bash
sudo apt-get install imagemagick
```

**Verify:**

```bash
magick -version  # or: convert -version
```

Without ImageMagick, screenshots >5MB will not be compressed (may fail to load in Gemini/Claude).

### Test

```bash
node navigate.js --url https://example.com
# Output: {"success": true, "url": "https://example.com", "title": "Example Domain"}
```

## Available Scripts

All scripts are in `.claude/skills/chrome-devtools/scripts/`

**CRITICAL**: Always check `pwd` before running scripts.

### Script Usage

- `./scripts/README.md`

### Core Automation

- `navigate.js` - Navigate to URLs
- `click.js` - Click elements
- `fill.js` - Fill form fields
- `evaluate.js` - Execute JavaScript in page context

### Web Scraping & Downloads

- `download-dribbble.js` - Download design images from Dribbble search results
- `snapshot.js` - Extract interactive elements with metadata

### Analysis & Monitoring

- `console.js` - Monitor console messages/errors
- `network.js` - Track HTTP requests/responses
- `performance.js` - Measure Core Web Vitals + record traces
- `screenshot.js` - Capture screenshots (full page or element)

## Usage Patterns

### Download Design Images from Dribbble

```bash
pwd  # Should show current working directory
cd .claude/skills/chrome-devtools/scripts
node download-dribbble.js --query "financial dashboard dark ui" --output ./docs/screenshots --count 12
```

**Features:**

- Automatically visits each shot's page to extract full-resolution images
- Supports queries for any design type (UI, logo, icon, illustration, etc.)
- Auto-compresses images for optimal file size
- Downloads metadata including source URLs
- Retry logic for reliable downloads

**Important**: Always save downloads to `./docs/screenshots` directory.

### Automatic Image Compression

Downloaded images are **automatically compressed** if they exceed 10MB (default) to optimize file size. This uses ImageMagick internally:

```bash
# Default: auto-compress if >10MB
node download-dribbble.js --query "financial dashboard" --output ./docs/screenshots

# Custom size threshold (e.g., 5MB)
node download-dribbble.js --query "financial dashboard" --output ./docs/screenshots --max-size 5

# Disable compression
node download-dribbble.js --query "financial dashboard" --output ./docs/screenshots --no-compress
```

**Compression behavior:**

- JPEG: Quality 75 with progressive encoding (or quality 60 if still too large)
- Requires ImageMagick installed for automatic compression

**Output includes compression info:**

```json
{
  "success": true,
  "downloads": [
    {
      "success": true,
      "filename": "001-design-title.jpg",
      "path": "/path/to/docs/screenshots/001-design-title.jpg",
      "originalSize": 2097152,
      "size": 512000,
      "compressed": true,
      "compressionRatio": "75.61%",
      "url": "https://cdn.dribbble.com/..."
    }
  ]
}
```

### Chain Commands (reuse browser)

```bash
# Keep browser open with --close false
node navigate.js --url https://example.com/login --close false
node fill.js --selector "#email" --value "user@example.com" --close false
node fill.js --selector "#password" --value "secret" --close false
node click.js --selector "button[type=submit]"
```

### Parse JSON Output

```bash
# Extract specific fields with jq
node performance.js --url https://example.com | jq '.vitals.LCP'

# Save to file
node network.js --url https://example.com --output /tmp/requests.json
```

## Execution Protocol

### Working Directory Verification

BEFORE executing any script:

1. Check current working directory with `pwd`
2. Verify in `.claude/skills/chrome-devtools/scripts/` directory
3. If wrong directory, `cd` to correct location
4. Use absolute paths for all output files

Example:

```bash
pwd  # Should show: .../chrome-devtools/scripts
# If wrong:
cd .claude/skills/chrome-devtools/scripts
```

### Output Validation

AFTER screenshot/capture operations:

1. Verify file created with `ls -lh <output-path>`
2. Read screenshot using Read tool to confirm content
3. Check JSON output for success:true
4. Report file size and compression status

Example:

```bash
node screenshot.js --url https://example.com --output ./docs/screenshots/page.png
ls -lh ./docs/screenshots/page.png  # Verify file exists
# Then use Read tool to visually inspect
```

1. Restart working directory to the project root.

### Error Recovery

If script fails:

1. Check error message for selector issues
2. Use snapshot.js to discover correct selectors
3. Try XPath selector if CSS selector fails
4. Verify element is visible and interactive

Example:

```bash
# CSS selector fails
node click.js --url https://example.com --selector ".btn-submit"
# Error: waiting for selector ".btn-submit" failed

# Discover correct selector
node snapshot.js --url https://example.com | jq '.elements[] | select(.tagName=="BUTTON")'

# Try XPath
node click.js --url https://example.com --selector "//button[contains(text(),'Submit')]"
```

### Common Mistakes

❌ Wrong working directory → output files go to wrong location
❌ Skipping output validation → silent failures
❌ Using complex CSS selectors without testing → selector errors
❌ Not checking element visibility → timeout errors

✅ Always verify `pwd` before running scripts
✅ Always validate output after screenshots
✅ Use snapshot.js to discover selectors
✅ Test selectors with simple commands first

## Common Workflows

### Download Design Inspiration from Dribbble

```bash
# Download UI/UX designs
node download-dribbble.js --query "dashboard ui" --output ./docs/screenshots --count 20

# Download with custom compression
node download-dribbble.js --query "mobile app design" --output ./docs/screenshots --max-size 5

# Slow download for rate limiting
node download-dribbble.js --query "landing page" --output ./docs/screenshots --delay 2000
```

### Web Scraping

```bash
node evaluate.js --url https://example.com --script "
  Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('h2')?.textContent,
    link: el.querySelector('a')?.href
  }))
" | jq '.result'
```

### Performance Testing

```bash
PERF=$(node performance.js --url https://example.com)
LCP=$(echo $PERF | jq '.vitals.LCP')
if (( $(echo "$LCP < 2500" | bc -l) )); then
  echo "✓ LCP passed: ${LCP}ms"
else
  echo "✗ LCP failed: ${LCP}ms"
fi
```

### Form Automation

```bash
node fill.js --url https://example.com --selector "#search" --value "query" --close false
node click.js --selector "button[type=submit]"
```

### Error Monitoring

```bash
node console.js --url https://example.com --types error,warn --duration 5000 | jq '.messageCount'
```

## Script Options

All scripts support:

- `--headless false` - Show browser window
- `--close false` - Keep browser open for chaining
- `--timeout 30000` - Set timeout (milliseconds)
- `--wait-until networkidle2` - Wait strategy

See `./scripts/README.md` for complete options.

## Output Format

All scripts output JSON to stdout:

```json
{
  "success": true,
  "url": "https://example.com",
  ... // script-specific data
}
```

Errors go to stderr:

```json
{
  "success": false,
  "error": "Error message"
}
```

## Finding Elements

Use `snapshot.js` to discover selectors:

```bash
node snapshot.js --url https://example.com | jq '.elements[] | {tagName, text, selector}'
```

## Troubleshooting

### Common Errors

**"Cannot find package 'puppeteer'"**

- Run: `npm install` in the scripts directory

**"error while loading shared libraries: libnss3.so"** (Linux/WSL)

- Missing system dependencies
- Fix: Run `./install-deps.sh` in scripts directory
- Manual install: `sudo apt-get install -y libnss3 libnspr4 libasound2t64 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1`

**"Failed to launch the browser process"**

- Check system dependencies installed (Linux/WSL)
- Verify Chrome downloaded: `ls ~/.cache/puppeteer`
- Try: `npm rebuild` then `npm install`

**Chrome not found**

- Puppeteer auto-downloads Chrome during `npm install`
- If failed, manually trigger: `npx puppeteer browsers install chrome`

### Script Issues

**Element not found**

- Get snapshot first to find correct selector: `node snapshot.js --url <url>`

**Script hangs**

- Increase timeout: `--timeout 60000`
- Change wait strategy: `--wait-until load` or `--wait-until domcontentloaded`

**Blank screenshot**

- Wait for page load: `--wait-until networkidle2`
- Increase timeout: `--timeout 30000`

**Permission denied on scripts**

- Make executable: `chmod +x *.sh`

### Download failures

- Images may fail if shot page structure changes: Check error message for details
- Some designs may have restricted downloads: Script will skip them automatically
- Network timeouts: Increase delay between downloads with `--delay 2000`

**Compression not working**

- Verify ImageMagick installed: `magick -version` or `convert -version`
- Check files were actually compressed in output JSON: `"compressed": true`
- Images may stay uncompressed if already below threshold size

## Reference Documentation

Detailed guides available in `./references/`:

- [CDP Domains Reference](./references/cdp-domains.md) - 47 Chrome DevTools Protocol domains
- [Puppeteer Quick Reference](./references/puppeteer-reference.md) - Complete Puppeteer API patterns
- [Performance Analysis Guide](./references/performance-guide.md) - Core Web Vitals optimization

## Advanced Usage

### Custom Scripts

Create custom scripts using shared library:

```javascript
import { getBrowser, getPage, closeBrowser, outputJSON } from './lib/browser.js';
// Your automation logic
```

### Direct CDP Access

```javascript
const client = await page.createCDPSession();
await client.send('Emulation.setCPUThrottlingRate', { rate: 4 });
```

See reference documentation for advanced patterns and complete API coverage.

## External Resources

- [Puppeteer Documentation](https://pptr.dev/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Scripts README](./scripts/README.md)
