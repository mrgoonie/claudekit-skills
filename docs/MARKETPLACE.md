# ClaudeKit Skills Marketplace

ClaudeKit Skills is now available as a **Claude Code Plugin Marketplace**, enabling seamless installation and automatic updates.

## Quick Start

### 1. Add Marketplace

```bash
/plugin marketplace add mrgoonie/claudekit-skills
```

### 2. Install Plugins

Install specific plugin categories based on your needs:

```bash
# AI & ML Tools
/plugin install ai-ml-tools@claudekit-skills

# Web Development
/plugin install web-dev-tools@claudekit-skills

# DevOps & Infrastructure
/plugin install devops-tools@claudekit-skills

# Backend Development
/plugin install backend-tools@claudekit-skills

# Document Processing
/plugin install document-processing@claudekit-skills

# Debugging Frameworks
/plugin install debugging-tools@claudekit-skills

# Problem Solving Techniques
/plugin install problem-solving-tools@claudekit-skills

# Platform Integrations
/plugin install platform-tools@claudekit-skills

# Meta Development
/plugin install meta-tools@claudekit-skills

# Media Processing
/plugin install media-tools@claudekit-skills

# Research Tools
/plugin install research-tools@claudekit-skills

# Specialized Skills
/plugin install specialized-tools@claudekit-skills
```

### 3. Update Plugins

```bash
# Update specific plugin
/plugin update ai-ml-tools@claudekit-skills

# Update all plugins
/plugin update --all
```

## Available Plugins

### 🤖 ai-ml-tools
**AI and ML capabilities with Google Gemini API integration**

**Includes:**
- `ai-multimodal` - Process images, videos, audio, and documents with Gemini API
- `google-adk-python` - Google's Agent Development Kit for building AI agents

**Dependencies:**
- Python 3.8+
- `google-genai`, `pypdf`, `python-docx`, `Pillow`
- Environment: `GEMINI_API_KEY`

---

### 🌐 web-dev-tools
**Comprehensive web development skills**

**Includes:**
- `frontend-development` - React/TypeScript patterns with Suspense, TanStack Router
- `frontend-design` - Production-grade UI/UX with creative, polished code
- `ui-styling` - shadcn/ui components with Tailwind CSS
- `web-frameworks` - Next.js App Router, Turborepo monorepos
- `aesthetic` - Design principles and visual hierarchy

**Dependencies:**
- Node.js 18+
- npm/pnpm/yarn

---

### ☁️ devops-tools
**DevOps and infrastructure management**

**Includes:**
- `devops` - Cloudflare Workers, Docker, Google Cloud Platform
- `databases` - MongoDB and PostgreSQL administration
- `chrome-devtools` - Browser automation with Puppeteer

**Dependencies:**
- Docker (optional)
- Cloudflare Wrangler (optional)
- Google Cloud CLI (optional)
- PostgreSQL client (optional)
- MongoDB Shell (optional)

---

### 💻 backend-tools
**Backend development frameworks**

**Includes:**
- `backend-development` - Node.js, Python, Go, REST/GraphQL APIs
- `better-auth` - TypeScript authentication framework

**Dependencies:**
- Node.js 18+ (for better-auth)
- Python 3.8+ (for backend patterns)

---

### 📄 document-processing
**Document creation and processing**

**Includes:**
- `document-skills/docx` - Word documents with tracked changes
- `document-skills/pdf` - PDF extraction, creation, merging
- `document-skills/pptx` - PowerPoint presentations
- `document-skills/xlsx` - Excel spreadsheets and financial modeling

**Dependencies:**
- Python 3.8+
- `pypdf`, `python-docx`, `python-pptx`, `openpyxl`

---

### 🐛 debugging-tools
**Systematic debugging frameworks**

**Includes:**
- `debugging/defense-in-depth` - Multi-layer validation
- `debugging/root-cause-tracing` - Backward call stack analysis
- `debugging/systematic-debugging` - Four-phase debugging process
- `debugging/verification-before-completion` - Evidence-based completion

---

### 🧠 problem-solving-tools
**Advanced problem-solving techniques**

**Includes:**
- `problem-solving/collision-zone-thinking` - Force unrelated concepts together
- `problem-solving/inversion-exercise` - Flip core assumptions
- `problem-solving/meta-pattern-recognition` - Spot universal principles
- `problem-solving/scale-game` - Test at extremes
- `problem-solving/simplification-cascades` - Find eliminating insights
- `problem-solving/when-stuck` - Dispatch to right technique

---

### 🛍️ platform-tools
**Platform integrations**

**Includes:**
- `shopify` - Build apps, extensions, and themes
- `mcp-management` - Manage MCP servers
- `mcp-builder` - Build MCP servers in Python/TypeScript

**Agents:**
- `mcp-manager` - MCP server management agent

**Commands:**
- `/use-mcp` - MCP integration command

**Dependencies:**
- Node.js 18+
- Shopify CLI (optional)

---

### 🔧 meta-tools
**Meta development tools**

**Includes:**
- `skill-creator` - Create new Claude Code skills
- `code-review` - Review workflows and quality gates

**Commands:**
- `/git/*` - Git workflow commands
- `/skill/*` - Skill management commands

---

### 🎬 media-tools
**Media processing capabilities**

**Includes:**
- `media-processing` - FFmpeg (video/audio) and ImageMagick (images)

**Dependencies:**
- FFmpeg
- ImageMagick

**Installation:**
```bash
# macOS
brew install ffmpeg imagemagick

# Ubuntu/Debian
sudo apt-get install ffmpeg imagemagick

# Windows
choco install ffmpeg imagemagick
```

---

### 📚 research-tools
**Research and documentation**

**Includes:**
- `docs-seeker` - llms.txt documentation discovery
- `repomix` - Package repositories for AI analysis

**Dependencies:**
- Node.js 18+ (for repomix)
- `repomix` CLI tool

---

### ⚡ specialized-tools
**Specialized capabilities**

**Includes:**
- `sequential-thinking` - Step-by-step reasoning with extended thinking
- `mermaidjs-v11` - Diagram generation (flowcharts, sequence, etc.)

---

## Auto-Enable in Projects

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claudekit-skills": {
      "source": {
        "source": "github",
        "repo": "mrgoonie/claudekit-skills"
      }
    }
  },
  "enabledPlugins": {
    "ai-ml-tools@claudekit-skills": true,
    "web-dev-tools@claudekit-skills": true,
    "devops-tools@claudekit-skills": true
  }
}
```

## Version Pinning

Pin to specific version for stability:

```json
{
  "extraKnownMarketplaces": {
    "claudekit-skills": {
      "source": {
        "source": "github",
        "repo": "mrgoonie/claudekit-skills",
        "ref": "v1.0.0"
      }
    }
  }
}
```

## Enterprise Configuration

Restrict to approved marketplaces in managed settings:

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "mrgoonie/claudekit-skills",
      "ref": "v1.0.0"
    }
  ]
}
```

## Manual Installation (Legacy)

For users who prefer manual installation:

```bash
git clone https://github.com/mrgoonie/claudekit-skills
cp -r claudekit-skills/.claude/* /path/to/your/project/.claude/
```

**Note:** Manual installation is deprecated. Marketplace installation is recommended for automatic updates and version management.

## Troubleshooting

### Plugin Not Found

```bash
# Refresh marketplace
/plugin marketplace remove claudekit-skills
/plugin marketplace add mrgoonie/claudekit-skills
```

### Update Not Working

```bash
# Force update
/plugin uninstall ai-ml-tools@claudekit-skills
/plugin install ai-ml-tools@claudekit-skills
```

### Dependencies Missing

Each plugin documents its dependencies. Install required system tools and Python packages as needed. See [INSTALLATION.md](../INSTALLATION.md) for detailed dependency installation instructions.

## Support

- **GitHub Issues:** https://github.com/mrgoonie/claudekit-skills/issues
- **Documentation:** https://claudekit.cc
- **Substack:** https://faafospecialist.substack.com/

## License

MIT License - see [LICENSE](../LICENSE) for details.
