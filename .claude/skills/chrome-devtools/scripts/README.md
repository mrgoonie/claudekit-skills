# Chrome DevTools Scripts

CLI scripts for browser automation using Puppeteer.

## Installation

### Quick Install

```bash
cd .claude/skills/chrome-devtools/scripts
./install.sh  # Auto-checks dependencies and installs
```

### Manual Installation

**Linux/WSL** - Install system dependencies first:
```bash
./install-deps.sh  # Auto-detects OS (Ubuntu, Debian, Fedora, etc.)
```

Or manually:
```bash
sudo apt-get install -y libnss3 libnspr4 libasound2t64 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1
```

**All platforms** - Install Node dependencies:
```bash
npm install
```

## Scripts

### navigate.js
Navigate to a URL.

```bash
node navigate.js --url https://example.com [--wait-until networkidle2] [--timeout 30000]
```

### screenshot.js
Take a screenshot.

**Important**: Always save screenshots to `./docs/screenshots` directory.

```bash
node screenshot.js --output screenshot.png [--url https://example.com] [--full-page true] [--selector .element]
```

### click.js
Click an element.

```bash
node click.js --selector ".button" [--url https://example.com] [--wait-for ".result"]
```

### fill.js
Fill form fields.

```bash
node fill.js --selector "#input" --value "text" [--url https://example.com] [--clear true]
```

### evaluate.js
Execute JavaScript in page context.

```bash
node evaluate.js --script "document.title" [--url https://example.com]
```

### snapshot.js
Get DOM snapshot with interactive elements.

```bash
node snapshot.js [--url https://example.com] [--output snapshot.json]
```

### console.js
Monitor console messages.

```bash
node console.js --url https://example.com [--types error,warn] [--duration 5000]
```

### network.js
Monitor network requests.

```bash
node network.js --url https://example.com [--types xhr,fetch] [--output requests.json]
```

### performance.js
Measure performance metrics and record trace.

```bash
node performance.js --url https://example.com [--trace trace.json] [--metrics] [--resources true]
```

## Common Options

- `--headless false` - Show browser window
- `--close false` - Keep browser open
- `--timeout 30000` - Set timeout in milliseconds
- `--wait-until networkidle2` - Wait strategy (load, domcontentloaded, networkidle0, networkidle2)

## Output Format

All scripts output JSON to stdout:

```json
{
  "success": true,
  "url": "https://example.com",
  "title": "Example Domain",
  ...
}
```

Errors are output to stderr:

```json
{
  "success": false,
  "error": "Error message",
  "stack": "..."
}
```
