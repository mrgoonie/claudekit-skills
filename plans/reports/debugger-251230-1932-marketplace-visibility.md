# Marketplace Visibility Investigation: mermaidjs-v11 & context-engineering

**Date:** 2025-12-30
**Investigator:** debugger subagent
**ID:** a3b2656

## Executive Summary

**Issue:** User reports "mermaidjs-v11" and "context-engineering" skills not visible when installing from plugins marketplace.

**Root Cause:**
1. **mermaidjs-v11**: Skill EXISTS and IS properly registered in specialized-tools plugin. NO configuration issue found.
2. **context-engineering**: Skill does NOT EXIST in repository - never created/added.

**Impact:**
- mermaidjs-v11: Should be installable via `specialized-tools@claudekit-skills` - may be UI discovery issue
- context-engineering: Cannot be installed - skill doesn't exist

## Technical Analysis

### Repository Structure

```
claudekit-skills/
├── .claude-plugin/
│   └── marketplace.json          # Root marketplace config
├── .claude/skills/               # 28 actual skill directories
│   ├── mermaidjs-v11/           ✓ EXISTS
│   ├── sequential-thinking/     ✓ EXISTS
│   └── ... (26 others)
└── plugins/                      # Plugin categories
    ├── specialized-tools/
    │   ├── .claude-plugin/
    │   │   └── plugin.json       # Plugin metadata
    │   └── skills/
    │       ├── mermaidjs-v11 -> ../../../.claude/skills/mermaidjs-v11 ✓
    │       └── sequential-thinking -> ../../../.claude/skills/sequential-thinking ✓
    └── ... (11 other plugins)
```

### Marketplace Configuration Analysis

**Root marketplace.json** (`.claude-plugin/marketplace.json`):
```json
{
  "plugins": [
    {
      "name": "specialized-tools",
      "source": "./plugins/specialized-tools",
      "description": "Specialized skills: sequential-thinking (step-by-step reasoning), mermaidjs-v11 (diagram generation)",
      "version": "1.0.0",
      "keywords": ["diagrams", "reasoning", "visualization"],
      "category": "productivity"
    }
  ]
}
```
✓ mermaidjs-v11 IS listed in description
✓ Plugin registered correctly

**Plugin metadata** (`plugins/specialized-tools/.claude-plugin/plugin.json`):
```json
{
  "name": "specialized-tools",
  "description": "Specialized skills for sequential reasoning and Mermaid diagram generation",
  "version": "1.0.0",
  "author": {"name": "ClaudeKit", "email": "[email protected]"},
  "repository": "https://github.com/mrgoonie/claudekit-skills"
}
```
✓ Mentions Mermaid diagram generation
✓ Properly configured

### Skill File Structure

**mermaidjs-v11** (`/.claude/skills/mermaidjs-v11/`):
```
mermaidjs-v11/
├── SKILL.md          ✓ Main skill definition with frontmatter
└── references/       ✓ Supporting docs
```

Frontmatter metadata:
```yaml
---
name: mermaidjs-v11
description: Create diagrams and visualizations using Mermaid.js v11 syntax...
---
```
✓ Properly formatted skill definition

**Symlink verification:**
```bash
plugins/specialized-tools/skills/mermaidjs-v11
  -> ../../../.claude/skills/mermaidjs-v11 ✓
```

### Evidence: context-engineering Does NOT Exist

**Search results:**
```bash
# grep -r "context-engineering" /Users/duynguyen/www/claudekit/claudekit-skills/
# (no output)

# find ... -name "context-engineering*" -type f -o -name "context-engineering*" -type d
# (no output)
```

✗ No skill directory
✗ No references in any config files
✗ No mentions in documentation
✗ Never existed in repository

### Comparison: Working vs Reported Skills

**Working skills** (e.g., frontend-design, ai-multimodal):
- Directory: `.claude/skills/{skill-name}/`
- File: `SKILL.md` with frontmatter
- Symlink: `plugins/{category}/skills/{skill-name}` -> `.claude/skills/{skill-name}`
- Registered: Listed in plugin description

**mermaidjs-v11** (reported as missing):
✓ Has directory
✓ Has SKILL.md with frontmatter
✓ Has symlink
✓ Listed in plugin description
→ Structure IDENTICAL to working skills

**context-engineering** (reported as missing):
✗ No directory
✗ No files
✗ No registration
→ Never existed

## Installation Command Analysis

**Expected installation:**
```bash
/plugin marketplace add mrgoonie/claudekit-skills
/plugin install specialized-tools@claudekit-skills
```

This SHOULD install:
- sequential-thinking ✓
- mermaidjs-v11 ✓ (properly configured)

## Skill Discovery Count

```bash
# Total skill directories in .claude/skills/
29 directories (includes subdirectories like debugging/*, problem-solving/*)

# Total skill definition files
38 SKILL.md files (includes nested skills)

# Plugin categories
12 plugins in marketplace.json
```

## Root Cause Summary

### mermaidjs-v11
**Configuration:** ✓ CORRECT
**Structure:** ✓ VALID
**Registration:** ✓ PRESENT
**Symlink:** ✓ WORKING

**Hypothesis:** Issue likely in:
1. Claude Code UI not discovering skills correctly from plugin structure
2. Cache/refresh issue in marketplace UI
3. Skill file format expectation mismatch (SKILL.md vs skill.md)

**Evidence against configuration issue:**
- Identical structure to working skills (frontend-design, ai-multimodal)
- Properly registered in marketplace.json
- Valid SKILL.md frontmatter format
- Working symlink chain

### context-engineering
**Status:** ✗ DOES NOT EXIST
**Cause:** Skill was never created/added to repository

**Evidence:**
- No directory in `.claude/skills/`
- No references in any JSON configs
- No documentation mentions
- grep/find returned zero results

## Supporting Evidence

**File paths verified:**
- Root config: `/Users/duynguyen/www/claudekit/claudekit-skills/.claude-plugin/marketplace.json`
- Plugin config: `/Users/duynguyen/www/claudekit/claudekit-skills/plugins/specialized-tools/.claude-plugin/plugin.json`
- Skill location: `/Users/duynguyen/www/claudekit/claudekit-skills/.claude/skills/mermaidjs-v11/`
- Symlink: `/Users/duynguyen/www/claudekit/claudekit-skills/plugins/specialized-tools/skills/mermaidjs-v11`

**Symlink resolution:**
```bash
$ readlink plugins/specialized-tools/skills/mermaidjs-v11
../../../.claude/skills/mermaidjs-v11 ✓ VALID
```

## Recommended Investigation Steps

1. Test marketplace installation in clean environment
2. Check Claude Code logs for skill discovery errors
3. Verify marketplace cache/refresh behavior
4. Compare skill.md vs SKILL.md naming expectations
5. Test if skills appear after manual plugin installation

## Unresolved Questions

1. Why does mermaidjs-v11 not appear in UI if config is correct?
2. Is there a skill discovery cache that needs clearing?
3. Does Claude Code expect lowercase `skill.md` instead of `SKILL.md`?
4. Was context-engineering mentioned in error or planned but not implemented?
