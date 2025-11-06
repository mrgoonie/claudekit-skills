# Best Practices

Essential principles and proven strategies for effective documentation discovery.

## 1. Prioritize context7.com for llms.txt

### Why

- **Comprehensive aggregator**: Single source for most documentation
- **Most efficient**: Instant access without searching
- **Authoritative**: Aggregates official sources
- **Up-to-date**: Continuously maintained
- **Fast**: Direct URL construction vs searching
- **Topic filtering**: Targeted results with ?topic= parameter

### Implementation

```
Step 1: Try context7.com (ALWAYS FIRST)
  ↓
Know GitHub repo?
  YES → https://context7.com/{org}/{repo}/llms.txt
  NO → Continue
  ↓
Know website?
  YES → https://context7.com/websites/{normalized-path}/llms.txt
  NO → Continue
  ↓
Specific topic needed?
  YES → Add ?topic={query} parameter
  NO → Use base URL
  ↓
Found?
  YES → Use as primary source
  NO → Fall back to WebSearch for llms.txt
  ↓
Still not found?
  YES → Fall back to repository analysis
```

### Examples

```
Best approach (context7.com):
1. Direct URL: https://context7.com/vercel/next.js/llms.txt
2. WebFetch llms.txt
3. Launch Explorer agents for URLs
Total time: ~15 seconds

Topic-specific approach:
1. Direct URL: https://context7.com/shadcn-ui/ui/llms.txt?topic=date
2. WebFetch filtered content
3. Present focused results
Total time: ~10 seconds

Good fallback approach:
1. context7.com returns 404
2. WebSearch: "Astro llms.txt site:docs.astro.build"
3. Found → WebFetch llms.txt
4. Launch Explorer agents for URLs
Total time: ~60 seconds

Poor approach:
1. Skip context7.com entirely
2. Search for various documentation pages
3. Manually collect URLs
4. Process one by one
Total time: ~5 minutes
```

### When Not Available

Fallback strategy when context7.com unavailable:
- If context7.com returns 404 → try WebSearch for llms.txt
- If WebSearch finds nothing in 30 seconds → move to repository
- If domain is incorrect → try 2-3 alternatives, then move on
- If documentation is very old → likely doesn't have llms.txt

## 2. Use Parallel Agents Aggressively

### Why

- **Speed**: N tasks in time of 1 (vs N × time)
- **Efficiency**: Better resource utilization
- **Coverage**: Comprehensive results faster
- **Scalability**: Handles large documentation sets

### Guidelines

**Always use parallel for 3+ URLs:**
```
3 URLs → 1 Explorer agent (acceptable)
4-10 URLs → 3-5 Explorer agents (optimal)
11+ URLs → 5-7 agents in phases (best)
```

**Launch all agents in single message:**
```
Good:
[Send one message with 5 Task tool calls]

Bad:
[Send message with Task call]
[Wait for result]
[Send another message with Task call]
[Wait for result]
...
```

### Distribution Strategy

**Even distribution:**
```
10 URLs, 5 agents:
Agent 1: URLs 1-2
Agent 2: URLs 3-4
Agent 3: URLs 5-6
Agent 4: URLs 7-8
Agent 5: URLs 9-10
```

**Topic-based distribution:**
```
10 URLs, 3 agents:
Agent 1: Installation & Setup (URLs 1-3)
Agent 2: Core Concepts & API (URLs 4-7)
Agent 3: Examples & Guides (URLs 8-10)
```

### When Not to Parallelize

- Single URL (use WebFetch)
- 2 URLs (single agent is fine)
- Dependencies between tasks (sequential required)
- Limited documentation (1-2 pages)

## 3. Verify Official Sources

### Why

- **Accuracy**: Avoid outdated information
- **Security**: Prevent malicious content
- **Credibility**: Maintain trust
- **Relevance**: Match user's version/needs

### Verification Checklist

**For llms.txt:**
```
[ ] Domain matches official site
[ ] HTTPS connection
[ ] Content format is valid
[ ] URLs point to official docs
[ ] Last-Modified header is recent (if available)
```

**For repositories:**
```
[ ] Organization matches official entity
[ ] Star count appropriate for library
[ ] Recent commits (last 6 months)
[ ] README mentions official status
[ ] Links back to official website
[ ] License matches expectations
```

**For documentation:**
```
[ ] Domain is official
[ ] Version matches user request
[ ] Last updated date visible
[ ] Content is complete (not stubs)
[ ] Links work (not 404s)
```

### Red Flags

⚠️ **Unofficial sources:**
- Personal GitHub forks
- Outdated tutorials (>2 years old)
- Unmaintained repositories
- Suspicious domains
- No version information
- Conflicting with official docs

### When to Use Unofficial Sources

Acceptable when:
- No official documentation exists
- Clearly labeled as community resource
- Recent and well-maintained
- Cross-referenced with official info
- User is aware of unofficial status

## 4. Report Methodology

### Why

- **Transparency**: User knows how you found info
- **Reproducibility**: User can verify
- **Troubleshooting**: Helps debug issues
- **Trust**: Builds confidence in results

### What to Include

**Always report:**
```markdown
## Source

**Method**: llms.txt / Repository / Research / Mixed
**Primary source**: [main URL or repository]
**Additional sources**: [list]
**Date accessed**: [current date]
**Version**: [documentation version]
```

**For llms.txt:**
```markdown
**Method**: llms.txt
**URL**: https://docs.astro.build/llms.txt
**URLs processed**: 8
**Date accessed**: 2025-10-26
**Version**: Latest (as of Oct 2025)
```

**For repository:**
```markdown
**Method**: Repository analysis (Repomix)
**Repository**: https://github.com/org/library
**Commit**: abc123f (2025-10-20)
**Stars**: 15.2k
**Analysis date**: 2025-10-26
```

**For research:**
```markdown
**Method**: Multi-source research
**Sources**:
- Official website: [url]
- Package registry: [url]
- Stack Overflow: [url]
- Community tutorials: [urls]
**Date accessed**: 2025-10-26
**Note**: No official llms.txt or repository available
```

### Limitations Disclosure

Always note:
```markdown
## ⚠️ Limitations

- Documentation for v2.x (user may need v3.x)
- API reference section incomplete
- Examples based on TypeScript (Python examples unavailable)
- Last updated 6 months ago
```

## 5. Handle Versions Explicitly

### Why

- **Compatibility**: Avoid version mismatch errors
- **Accuracy**: Features vary by version
- **Migration**: Support upgrade paths
- **Clarity**: No ambiguity about what's covered

### Version Detection

**Check these sources:**
```
1. URL path: /docs/v2/
2. Page header/title
3. Version selector on page
4. Git tag/branch name
5. Package.json or equivalent
6. Release date correlation
```

### Version Handling Rules

**User specifies version:**
```
Request: "Documentation for React 18"
→ Search: "React v18 documentation"
→ Verify: Check version in content
→ Report: "Documentation for React v18.2.0"
```

**User doesn't specify:**
```
Request: "Documentation for Next.js"
→ Default: Assume latest
→ Confirm: "I'll find the latest Next.js documentation"
→ Report: "Documentation for Next.js 14.0 (latest as of [date])"
```

**Version mismatch found:**
```
Request: "Docs for v2"
Found: Only v3 documentation
→ Report: "⚠️ Requested v2, but only v3 docs available. Here's v3 with migration guide."
```

### Multi-Version Scenarios

**Comparison request:**
```
Request: "Compare v1 and v2"
→ Find both versions
→ Launch parallel agents (set A for v1, set B for v2)
→ Present side-by-side analysis
```

**Migration request:**
```
Request: "How to migrate from v1 to v2"
→ Find v2 migration guide
→ Also fetch v1 and v2 docs
→ Highlight breaking changes
→ Provide code examples (before/after)
```

## 6. Aggregate Intelligently

### Why

- **Clarity**: Easier to understand
- **Efficiency**: Less cognitive load
- **Completeness**: Unified view
- **Actionability**: Clear next steps

### Bad Aggregation (Don't Do This)

```markdown
## Results

Agent 1 found:
[dump of agent 1 output]

Agent 2 found:
[dump of agent 2 output]

Agent 3 found:
[dump of agent 3 output]
```

Problems:
- Redundant information repeated
- No synthesis
- Hard to scan
- Lacks narrative

### Good Aggregation (Do This)

```markdown
## Installation

[Synthesized from agents 1 & 2]
Three installation methods available:

1. **npm (recommended)**:
   ```bash
   npm install library-name
   ```

2. **CDN**: [from agent 1]
   ```html
   <script src="..."></script>
   ```

3. **Manual**: [from agent 3]
   Download and include in project

## Core Concepts

[Synthesized from agents 2 & 4]
The library is built around three main concepts:

1. **Components**: [definition from agent 2]
2. **State**: [definition from agent 4]
3. **Effects**: [definition from agent 2]

## Examples

[From agents 3 & 5, deduplicated]
...
```

Benefits:
- Organized by topic
- Deduplicated
- Clear narrative
- Easy to scan

### Synthesis Techniques

**Deduplication:**
```
Agent 1: "Install with npm install foo"
Agent 2: "You can install using npm: npm install foo"
→ Synthesized: "Install: `npm install foo`"
```

**Prioritization:**
```
Agent 1: Basic usage example
Agent 2: Basic usage example (same)
Agent 3: Advanced usage example
→ Keep: Basic (from agent 1) + Advanced (from agent 3)
```

**Organization:**
```
Agents returned mixed information:
- Installation steps
- Configuration
- Usage example
- Installation requirements
- More usage examples

→ Reorganize:
1. Installation (requirements + steps)
2. Configuration
3. Usage (all examples together)
```

## 7. Time Management

### Why

- **User experience**: Fast results
- **Resource efficiency**: Don't waste compute
- **Fail fast**: Quickly try alternatives
- **Practical limits**: Avoid hanging

### Timeouts

**Set explicit timeouts:**
```
WebSearch: 30 seconds
WebFetch: 60 seconds
Repository clone: 5 minutes
Repomix processing: 10 minutes
Explorer agent: 5 minutes per URL
Researcher agent: 10 minutes
```

### Time Budgets

**Simple query (single library, latest version):**
```
Target: <2 minutes total

Phase 1 (Discovery): 30 seconds
- llms.txt search: 15 seconds
- Fetch llms.txt: 15 seconds

Phase 2 (Exploration): 60 seconds
- Launch agents: 5 seconds
- Agents fetch URLs: 60 seconds (parallel)

Phase 3 (Aggregation): 30 seconds
- Synthesize results
- Format output

Total: ~2 minutes
```

**Complex query (multiple versions, comparison):**
```
Target: <5 minutes total

Phase 1 (Discovery): 60 seconds
- Search both versions
- Fetch both llms.txt files

Phase 2 (Exploration): 180 seconds
- Launch 6 agents (2 sets of 3)
- Parallel exploration

Phase 3 (Comparison): 60 seconds
- Analyze differences
- Format side-by-side

Total: ~5 minutes
```

### When to Extend Timeouts

Acceptable to go longer when:
- User explicitly requests comprehensive analysis
- Repository is large but necessary
- Multiple fallbacks attempted
- User is informed of delay

### When to Give Up

Move to next method after:
- 3 failed attempts on same approach
- Timeout exceeded by 2x
- No progress for 30 seconds
- Error indicates permanent failure (404, auth required)

## 8. Cache Findings

### Why

- **Speed**: Instant results for repeated requests
- **Efficiency**: Reduce network requests
- **Consistency**: Same results within session
- **Reliability**: Less dependent on network

### What to Cache

**High value (always cache):**
```
- Repomix output (large, expensive to generate)
- llms.txt content (static, frequently referenced)
- Repository README (relatively static)
- Package registry metadata (changes rarely)
```

**Medium value (cache within session):**
```
- Documentation page content
- Search results
- Repository structure
- Version lists
```

**Low value (don't cache):**
```
- Real-time data (latest releases)
- User-specific content
- Time-sensitive information
```

### Cache Duration

```
Within conversation:
- All fetched content (reuse freely)

Within session:
- Repomix output (until conversation ends)
- llms.txt content (until new version requested)

Across sessions:
- Don't cache (start fresh each time)
```

### Cache Invalidation

Refresh cache when:
```
- User requests specific different version
- User says "get latest" or "refresh"
- Explicit time reference ("docs from today")
- Previous cache is from different library
```

### Implementation

```
# First request for library X
1. Fetch llms.txt
2. Store content in session variable
3. Use for processing

# Second request for library X (same session)
1. Check if llms.txt cached
2. Reuse cached content
3. Skip redundant fetch

# Request for library Y
1. Don't reuse library X cache
2. Fetch fresh for library Y
```

### Cache Hit Messages

```markdown
ℹ️ Using cached llms.txt from 5 minutes ago.
To fetch fresh, say "refresh" or "get latest".
```

## Quick Reference Checklist

### Before Starting

- [ ] Identify library name clearly
- [ ] Confirm version (default: latest)
- [ ] Check if cached data available
- [ ] Plan method (llms.txt → repo → research)

### During Discovery

- [ ] Start with llms.txt search
- [ ] Verify source is official
- [ ] Check version matches requirement
- [ ] Set timeout for each operation
- [ ] Fall back quickly if method fails

### During Exploration

- [ ] Use parallel agents for 3+ URLs
- [ ] Launch all agents in single message
- [ ] Distribute workload evenly
- [ ] Monitor for errors/timeouts
- [ ] Be ready to retry or fallback

### Before Presenting

- [ ] Synthesize by topic (not by agent)
- [ ] Deduplicate repeated information
- [ ] Verify version is correct
- [ ] Include source attribution
- [ ] Note any limitations
- [ ] Format clearly
- [ ] Check completeness

### Quality Gates

Ask before presenting:
- [ ] Is information accurate?
- [ ] Are sources official?
- [ ] Does version match request?
- [ ] Are all key topics covered?
- [ ] Are limitations noted?
- [ ] Is methodology documented?
- [ ] Is output well-organized?
