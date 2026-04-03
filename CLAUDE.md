# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ClaudeKit Skills is a collection of 35+ reusable Agent Skills for Claude Code, organized into 12 plugin categories for marketplace distribution. Skills use a **progressive disclosure** architecture (3-tier loading) achieving 85% context efficiency over flat designs.

## Architecture

### Dual-Directory Pattern (Source + Distribution)

```
.claude/skills/{skill-name}/     ← SOURCE (actual skill files)
plugins/{category}/skills/{name} ← SYMLINK → ../../../.claude/skills/{name}
```

**Every skill lives in `.claude/skills/`**. Plugin directories contain only symlinks. This is the single source of truth pattern.

### Skill Structure

```
.claude/skills/skill-name/
├── SKILL.md              # Entry point (<200 lines, YAML frontmatter required)
├── references/            # Detailed docs loaded on-demand (<300 lines each)
├── scripts/               # Executable code (Python/Node.js, optional)
└── assets/                # Templates, images (optional)
```

### Plugin Structure

```
plugins/category-name/
├── .claude-plugin/plugin.json   # Manifest: name, description, version, skills array
└── skills/
    ├── skill-a → ../../../.claude/skills/skill-a  (symlink)
    └── skill-b → ../../../.claude/skills/skill-b  (symlink)
```

### 12 Plugin Categories

`ai-ml-tools`, `web-dev-tools`, `devops-tools`, `backend-tools`, `document-processing`, `debugging-tools`, `problem-solving-tools`, `platform-tools`, `meta-tools`, `media-tools`, `research-tools`, `specialized-tools`

## Adding a New Skill

1. Create skill in `.claude/skills/{name}/` with SKILL.md + references/
2. Create symlink: `ln -s ../../../.claude/skills/{name} plugins/{category}/skills/{name}`
3. Update `plugins/{category}/.claude-plugin/plugin.json` — add to `skills` array
4. Update README.md catalog entry

## Key Conventions

- **SKILL.md**: Max 200 lines. YAML frontmatter with `name` and `description` required.
- **References**: Max 300 lines each. Split by logical boundaries.
- **File naming**: kebab-case for all files and directories.
- **Shared utilities**: `.claude/skills/common/api_key_helper.py` for Gemini API keys.
- **Python venv**: `~/.claude/skills/.venv/bin/python3` for scripts requiring packages.
- **Env var hierarchy**: process env > skill .env > skills/.env > .claude/.env > root .env

## Testing

```bash
# Validate skill structure
~/.claude/skills/.venv/bin/python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/{name}

# Run skill-specific tests
cd .claude/skills/{name}/scripts && python -m pytest tests/ -v
```

## Marketplace

```bash
# Install from marketplace
/plugin marketplace add mrgoonie/claudekit-skills
/plugin install {category}@claudekit-skills
```

Root marketplace metadata: `.claude-plugin/marketplace.json`
