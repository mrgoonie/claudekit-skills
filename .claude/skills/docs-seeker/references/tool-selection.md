# Tool Selection Guide

Complete reference for choosing and using the right tools for documentation discovery.

## context7.com (PRIORITY)

**Use FIRST for all llms.txt lookups**

**Patterns:**

GitHub repositories:
```
Pattern: https://context7.com/{org}/{repo}/llms.txt
Examples:
- https://github.com/vercel/next.js → https://context7.com/vercel/next.js/llms.txt
- https://github.com/shadcn-ui/ui → https://context7.com/shadcn-ui/ui/llms.txt
```

Websites:
```
Pattern: https://context7.com/websites/{normalized-path}/llms.txt
Examples:
- https://docs.imgix.com/ → https://context7.com/websites/imgix/llms.txt
- https://ffmpeg.org/doxygen/8.0/ → https://context7.com/websites/ffmpeg_doxygen_8_0/llms.txt
```

Topic-specific searches:
```
Pattern: https://context7.com/{path}/llms.txt?topic={query}
Examples:
- https://context7.com/shadcn-ui/ui/llms.txt?topic=date
- https://context7.com/vercel/next.js/llms.txt?topic=cache
- https://context7.com/websites/ffmpeg_doxygen_8_0/llms.txt?topic=compress
```

**Benefits:**
- Comprehensive aggregator of documentation
- Up-to-date content
- Topic filtering for targeted results
- Consistent format across libraries
- Reduces search time

**When to use:**
- ALWAYS try context7.com first before WebSearch
- Use topic parameter when user asks about specific feature
- Fall back to WebSearch only if context7.com returns 404

## WebSearch

**Use when:**
- context7.com unavailable or returns 404
- Finding GitHub repository URLs
- Locating official documentation sites
- Identifying package registries
- Searching for specific versions

**Best practices:**
- Try context7.com FIRST
- Include domain in query: `site:docs.example.com`
- Specify version when needed: `v2.0 llms.txt`
- Use official terms: "official repository" "documentation"
- Check multiple domains if first fails

**Example queries:**
```
Good: "Next.js llms.txt site:nextjs.org"
Good: "React v18 documentation site:react.dev"
Good: "Vue 3 official github repository"

Avoid: "how to use react" (too vague)
Avoid: "best react tutorial" (not official)
```

## WebFetch

**Use when:**
- Reading llms.txt content
- Accessing single documentation pages
- Retrieving specific URLs
- Checking documentation structure
- Verifying content availability

**Best practices:**
- Use specific prompt: "Extract all documentation URLs"
- Handle redirects properly
- Check for rate limiting
- Verify content is complete
- Note last-modified dates when available

**Limitations:**
- Single URL at a time (use Explorer for multiple)
- May timeout on very large pages
- Cannot handle dynamic content
- No JavaScript execution

## Task Tool with Explore Subagent

**Use when:**
- Multiple URLs to read (3+)
- Need parallel exploration
- Comprehensive documentation coverage
- Time-sensitive requests
- Large documentation sets

**Best practices:**
- Launch all agents in single message
- Distribute workload evenly
- Group related URLs per agent
- Maximum 7 agents per batch
- Provide clear extraction goals

**Example prompt:**
```
"Read the following URLs and extract:
1. Installation instructions
2. Core API methods
3. Configuration options
4. Common usage examples

URLs:
- [url1]
- [url2]
- [url3]"
```

## Task Tool with Researcher Subagent

**Use when:**
- No structured documentation found
- Need diverse information sources
- Community knowledge required
- Scattered documentation
- Comparative analysis needed

**Best practices:**
- Assign specific research areas per agent
- Request source verification
- Ask for date/version information
- Prioritize official sources
- Cross-reference findings

**Example prompt:**
```
"Research [library] focusing on:
1. Official installation methods
2. Common usage patterns
3. Known limitations or issues
4. Community best practices

Prioritize official sources and note version/date for all findings."
```

## Repomix

**Use when:**
- GitHub repository available
- Need complete codebase analysis
- Documentation scattered in repository
- Want to analyze code structure
- API documentation in code comments

**Installation:**
```bash
# Check if installed
which repomix

# Install globally if needed
npm install -g repomix

# Verify installation
repomix --version
```

**Usage:**
```bash
# Basic usage
git clone [repo-url] /tmp/docs-analysis
cd /tmp/docs-analysis
repomix --output repomix-output.xml

# Focus on specific directory
repomix --include "docs/**" --output docs-only.xml

# Exclude large files
repomix --exclude "*.png,*.jpg,*.pdf" --output repomix-output.xml
```

**When Repomix may fail:**
- Repository > 1GB (too large)
- Requires authentication (private repo)
- Slow network connection
- Limited disk space
- Binary-heavy repository

**Alternatives if Repomix fails:**
```bash
# Option 1: Focus on docs directory only
repomix --include "docs/**,README.md" --output docs.xml

# Option 2: Use Explorer agents to read specific files
# Launch agents to read key documentation files directly

# Option 3: Manual repository exploration
# Read README, then explore /docs directory structure
```

## Tool Selection Decision Tree

```
Need documentation?
  ↓
Try context7.com first
  ↓
Know GitHub org/repo?
  YES → https://context7.com/{org}/{repo}/llms.txt
  NO → Continue
  ↓
Know website URL?
  YES → https://context7.com/websites/{normalized-path}/llms.txt
  NO → Continue
  ↓
Specific topic/feature?
  YES → Add ?topic={query} parameter
  NO → Use base llms.txt URL
  ↓
context7.com found?
  YES → Process llms.txt URLs (go to URL count check)
  NO → Continue
  ↓
Fallback: WebSearch for llms.txt
  ↓
Single URL?
  YES → WebFetch
  NO → Continue
  ↓
1-3 URLs?
  YES → Single Explorer agent
  NO → Continue
  ↓
4+ URLs?
  YES → Multiple Explorer agents (3-7)
  NO → Continue
  ↓
Need repository analysis?
  YES → Repomix (if available)
  NO → Continue
  ↓
No structured docs?
  YES → Researcher agents
```

## Quick Reference

| Tool | Best For | Speed | Coverage | Complexity |
|------|----------|-------|----------|------------|
| context7.com | llms.txt lookup | Instant | High | Low |
| context7.com?topic= | Targeted search | Instant | Focused | Low |
| WebSearch | Finding URLs | Fast | Narrow | Low |
| WebFetch | Single page | Fast | Single | Low |
| Explorer | Multiple URLs | Fast | Medium | Medium |
| Researcher | Scattered info | Slow | Wide | High |
| Repomix | Repository | Medium | Complete | Medium |
