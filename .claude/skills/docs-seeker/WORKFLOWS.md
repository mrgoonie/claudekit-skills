# Detailed Workflows & Examples

This document provides comprehensive workflow examples for the docs-seeker skill.

## Parallel Exploration Strategy

### When to Use Multiple Agents

Deploy parallel agents when:
- llms.txt contains more than 3 URLs
- Repository has multiple documentation directories
- Need to check multiple versions
- Comprehensive coverage required

### How to Launch Parallel Agents

Use Task tool with `Explore` subagent:

```markdown
Example for 5 URLs:
1. Launch all 5 Explore agents in single message
2. Each agent gets specific URLs to read
3. Each agent extracts relevant information
4. Wait for all agents to complete
5. Aggregate results
```

### Agent Distribution Guidelines

**Small documentation sets (1-3 URLs):**
- Deploy 2 Explore agents to handle all URLs
- Simple, straightforward extraction
- Fastest for small amounts

**Medium documentation sets (4-10 URLs):**
- Deploy 3-6 Explore agents
- Balance workload evenly
- Group related URLs together

**Large documentation sets (11+ URLs):**
- Deploy 7-15 Explore agents (max)
- Prioritize most relevant URLs first
- Group related URLs together
- Balance workload evenly
- Avoid over-parallelization

### Best Distribution Practices

1. **Group related content**: Keep related URLs with same agent
2. **Balance workload**: Distribute URLs evenly by estimated size
3. **Prioritize critical docs**: Assign core docs first
4. **Avoid over-parallelization**: Max 7 agents to avoid overwhelming
5. **Sequential batches**: For 15+ URLs, use two sequential batches

## Workflow Examples

### Example 1: Library with llms.txt (Simple)

**Scenario**: User requests documentation for Astro

```
Step 1: Initial Search (PRIORITIZE context7.com)
→ Try context7.com first: https://context7.com/withastro/astro/llms.txt
→ WebFetch: Read llms.txt content
→ Result: Contains 8+ documentation URLs (success!)

Alternative if context7.com fails:
→ WebSearch: "Astro llms.txt site:docs.astro.build"
→ Result: https://docs.astro.build/llms.txt found

Step 2: Process llms.txt
→ Already fetched in Step 1
→ Result: Contains 8 documentation URLs

Step 3: Parallel Exploration
→ Launch 3 Explorer agents simultaneously:

  Agent 1 (URLs 1-3):
  - https://docs.astro.build/en/getting-started/
  - https://docs.astro.build/en/install/
  - https://docs.astro.build/en/editor-setup/

  Agent 2 (URLs 4-6):
  - https://docs.astro.build/en/core-concepts/project-structure/
  - https://docs.astro.build/en/core-concepts/astro-components/
  - https://docs.astro.build/en/core-concepts/layouts/

  Agent 3 (URLs 7-8):
  - https://docs.astro.build/en/guides/configuring-astro/
  - https://docs.astro.build/en/reference/configuration-reference/

Step 4: Aggregate Findings
→ Collect results from all 3 agents
→ Synthesize into cohesive documentation

Step 5: Present Report
→ Format using standard output structure
→ Include source attribution
→ Note any gaps or limitations
```

### Example 2: Library without llms.txt on context7 (Repository Analysis)

**Scenario**: User requests documentation for obscure library

```
Step 1: Try context7.com first
→ Attempt: https://context7.com/org/library-name/llms.txt
→ Result: Not found (404)

Step 2: Find GitHub Repository
→ WebSearch: "[library-name] github repository"
→ Result: https://github.com/org/library-name

Step 2a: Try context7.com with GitHub info
→ Attempt: https://context7.com/org/library-name/llms.txt
→ Result: Still not found

Step 3: Verify Repository
→ Check if it's official/active
→ Note star count, last update, license

Step 4: Check Repomix Installation
→ Bash: which repomix || npm install -g repomix

Step 5: Clone and Process Repository
→ Bash: git clone https://github.com/org/library-name /tmp/docs-analysis
→ Bash: cd /tmp/docs-analysis && repomix --output repomix-output.xml

Step 6: Analyze Repomix Output
→ Read: /tmp/docs-analysis/repomix-output.xml
→ Extract sections: README, docs/, examples/, CONTRIBUTING.md

Step 7: Present Findings
→ Format extracted documentation
→ Highlight key sections: installation, usage, API, examples
→ Note repository health: stars, activity, issues
```

### Example 3: Topic-Specific Search (context7.com feature)

**Scenario**: User asks "How do I use the date picker in shadcn/ui?"

```
Step 1: Identify library and topic
→ Library: shadcn/ui
→ Topic: date picker

Step 2: Construct context7.com URL with topic parameter
→ URL: https://context7.com/shadcn-ui/ui/llms.txt?topic=date
→ WebFetch: Read filtered content
→ Result: Returns ONLY date-related documentation (highly targeted!)

Step 3: Present Findings
→ Focused documentation on date picker component
→ Installation instructions
→ Usage examples
→ API reference for date components
→ Much faster than reading entire documentation

Benefits of topic search:
- Reduces context usage (only relevant docs loaded)
- Faster results (no need to filter manually)
- More accurate (context7 filters for you)
```

### Example 4: Multiple Versions Comparison

**Scenario**: User wants to compare v1 and v2 documentation

```
Step 1: Identify Version Requirements
→ User needs: v1.x and v2.x comparison
→ Primary focus: migration path and breaking changes

Step 2: Search Both Versions
→ WebSearch: "[library] v1 llms.txt"
→ WebSearch: "[library] v2 llms.txt"

Step 3: Launch Parallel Version Analysis
→ Deploy two sets of Explorer agents:

  Set A - v1 Documentation (3 agents):
  Agent 1: Core concepts v1
  Agent 2: API reference v1
  Agent 3: Examples v1

  Set B - v2 Documentation (3 agents):
  Agent 4: Core concepts v2
  Agent 5: API reference v2
  Agent 6: Examples v2

Step 4: Compare Findings
→ Analyze differences in:
  - Core concepts changes
  - API modifications
  - Breaking changes
  - New features in v2
  - Deprecated features from v1

Step 5: Present Side-by-Side Analysis
→ Migration guide format:
  - What changed
  - What's new
  - What's deprecated
  - Migration steps
  - Code examples (before/after)
```

### Example 4: No Official Documentation (Research Fallback)

**Scenario**: Library with scattered documentation

```
Step 1: Exhaust Structured Sources
→ WebSearch: llms.txt (not found)
→ WebSearch: GitHub repo (not found or no docs)
→ WebSearch: Official website (minimal content)

Step 2: Deploy Researcher Agents
→ Launch 4 Researcher agents in parallel:

  Researcher 1: Official sources
  - Package registry page (npm, PyPI, etc.)
  - Official website
  - Release notes

  Researcher 2: Tutorial content
  - Blog posts
  - Getting started guides
  - Video tutorials

  Researcher 3: Community resources
  - Stack Overflow discussions
  - Reddit threads
  - GitHub issues/discussions

  Researcher 4: API & reference
  - Auto-generated docs
  - Code examples in wild
  - Community examples

Step 3: Aggregate Diverse Sources
→ Collect findings from all researchers
→ Cross-reference information
→ Identify consistent patterns
→ Note conflicting information

Step 4: Present Consolidated Report
→ Structure findings:
  - Overview (from multiple sources)
  - Installation (verified approach)
  - Basic usage (community examples)
  - Common patterns (from discussions)
  - Known issues (from GitHub/SO)
  - Caveats about source quality
```

### Example 5: Large Documentation Set (Two-Phase)

**Scenario**: Framework with 20+ documentation pages

```
Step 1: Analyze Documentation Structure
→ WebFetch: llms.txt
→ Result: Contains 24 URLs across multiple categories

Step 2: Prioritize URLs
→ Categorize by importance:
  - Critical (8): Getting started, core concepts, API
  - Important (10): Guides, integrations, examples
  - Supplementary (6): Advanced topics, internals

Step 3: Phase 1 - Critical Documentation
→ Launch 5 Explorer agents:
  Agent 1: URLs 1-2 (Getting started)
  Agent 2: URLs 3-4 (Installation & setup)
  Agent 3: URLs 5-6 (Core concepts)
  Agent 4: URLs 7-8 (Basic API)
  Agent 5: URL 9 (Configuration)

→ Wait for completion
→ Quick review of coverage

Step 4: Phase 2 - Important Documentation
→ Launch 5 Explorer agents:
  Agent 6: URLs 10-11 (Routing guide)
  Agent 7: URLs 12-13 (Data fetching)
  Agent 8: URLs 14-15 (Authentication)
  Agent 9: URLs 16-17 (Deployment)
  Agent 10: URLs 18-19 (Integrations)

Step 5: Evaluate Need for Phase 3
→ Assess user needs
→ If supplementary topics required:
  - Launch final batch for advanced topics
→ If basics sufficient:
  - Note additional resources in report

Step 6: Comprehensive Report
→ Synthesize all phases
→ Organize by topic
→ Cross-reference related sections
→ Highlight critical workflows
```

## Performance Optimization Strategies

### Minimize Sequential Operations

**Bad approach:**
```
1. Read URL 1 with WebFetch
2. Wait for result
3. Read URL 2 with WebFetch
4. Wait for result
5. Read URL 3 with WebFetch
6. Wait for result
Time: 3x single URL fetch time
```

**Good approach:**
```
1. Launch 3 Explorer agents simultaneously
2. Each reads one URL
3. All complete in parallel
4. Aggregate results
Time: ~1x single URL fetch time
```

### Batch Related Operations

**Group by topic:**
```
Agent 1: Authentication (login.md, oauth.md, sessions.md)
Agent 2: Database (models.md, queries.md, migrations.md)
Agent 3: API (routes.md, middleware.md, validation.md)
```

**Group by content type:**
```
Agent 1: Tutorials (getting-started.md, quickstart.md)
Agent 2: Reference (api-ref.md, config-ref.md)
Agent 3: Guides (best-practices.md, troubleshooting.md)
```

### Use Caching Effectively

**Repository analysis:**
```
1. First request: Clone + Repomix (slow)
2. Save repomix-output.xml
3. Subsequent requests: Reuse saved output (fast)
4. Refresh only if repository updated
```

**llms.txt content:**
```
1. First fetch: WebFetch llms.txt
2. Store URL list in session
3. Reuse for follow-up questions
4. Re-fetch only if user changes version
```

### Fail Fast Strategy

**Set timeouts:**
```
1. WebSearch: 30 seconds max
2. WebFetch: 60 seconds max
3. Repository clone: 5 minutes max
4. Repomix processing: 10 minutes max
```

**Quick fallback:**
```
1. Try llms.txt (30 sec timeout)
2. If fails → immediately try repository
3. If fails → immediately launch researchers
4. Don't retry failed methods
```

## Common Pitfalls & Solutions

### Pitfall 1: Over-Parallelization

**Problem**: Launching 15 agents at once
**Impact**: Slow, overwhelming, hard to track
**Solution**: Max 7 agents per batch, use phases for large sets

### Pitfall 2: Unbalanced Workload

**Problem**: Agent 1 gets 1 URL, Agent 2 gets 10 URLs
**Impact**: Agent 1 finishes fast, Agent 2 bottleneck
**Solution**: Distribute evenly or by estimated size

### Pitfall 3: Ignoring Errors

**Problem**: Agent fails, continue without checking
**Impact**: Incomplete documentation, missing sections
**Solution**: Check all agent outputs, retry or note failures

### Pitfall 4: Poor Aggregation

**Problem**: Concatenating agent outputs without synthesis
**Impact**: Redundant, disorganized information
**Solution**: Synthesize findings, organize by topic, deduplicate

### Pitfall 5: Not Verifying Sources

**Problem**: Using first result without verification
**Impact**: Outdated or unofficial documentation
**Solution**: Check official status, version, date

## Decision Trees

### Choosing Documentation Strategy

```
Start
  ↓
Does llms.txt exist?
  ↓
YES → How many URLs?
  ↓
  1-3 URLs → Single WebFetch/Explorer
  4+ URLs → Parallel Explorers
  ↓
NO → Is there GitHub repo?
  ↓
  YES → Is Repomix feasible?
    ↓
    YES → Use Repomix
    NO → Manual exploration with Explorers
  ↓
  NO → Deploy Researcher agents
```

### Choosing Agent Count

```
URL Count < 3
  ↓
Single Explorer
  ↓
URL Count 4-10
  ↓
3-5 Explorers
  ↓
URL Count 11-20
  ↓
5-7 Explorers (or two phases)
  ↓
URL Count > 20
  ↓
Two-phase approach:
  Phase 1: 5 agents (critical)
  Phase 2: 5 agents (important)
```

## Advanced Scenarios

### Scenario: Multi-Language Documentation

**Challenge**: Documentation in multiple languages

**Approach**:
1. Identify target language from user
2. Search for language-specific llms.txt
3. If not found, search for English version
4. Note language limitations in report
5. Offer to translate key sections if needed

### Scenario: Framework with Plugins

**Challenge**: Core framework + 50 plugin docs

**Approach**:
1. Focus on core framework first
2. Ask user which plugins they need
3. Launch targeted search for specific plugins
4. Avoid trying to document everything
5. Note available plugins in report

### Scenario: Documentation Under Construction

**Challenge**: New release with incomplete docs

**Approach**:
1. Note documentation status upfront
2. Combine available docs with repository analysis
3. Check GitHub issues for documentation requests
4. Provide code examples from tests/examples
5. Clearly mark sections as "inferred from code"

### Scenario: Conflicting Information

**Challenge**: Multiple sources with different approaches

**Approach**:
1. Identify primary official source
2. Note version differences between sources
3. Present both approaches with context
4. Recommend official/latest approach
5. Explain why conflict exists (e.g., version change)
