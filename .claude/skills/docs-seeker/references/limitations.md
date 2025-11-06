# Limitations & Success Criteria

Understanding boundaries and measuring effectiveness of documentation discovery.

## context7.com Limitations

### Not All Libraries Indexed

**Limitation:**
- context7.com doesn't index every repository/website
- Very new libraries may not be available yet
- Private repositories not accessible
- Some niche libraries missing

**Impact:**
- Need fallback to official llms.txt or repository analysis
- May add 10-20 seconds to discovery time
- Requires manual search for obscure libraries

**Workarounds:**
```
1. Try context7.com first (always)
2. If 404, fall back to official llms.txt search
3. If still not found, use repository analysis
4. Note in report which method was used
```

**Example:**
```
Tried: https://context7.com/org/new-lib/llms.txt → 404
Fallback: WebSearch for "new-lib llms.txt" → Found
Used: Official llms.txt from website
```

### Topic Filtering Accuracy

**Limitation:**
- ?topic= parameter relies on keyword matching
- May miss relevant content with different terminology
- May include tangentially related content
- Quality depends on context7 indexing

**Impact:**
- Occasionally need to review base llms.txt without topic filter
- May miss some relevant documentation

**Workarounds:**
```
- Try multiple topic keywords
- Fall back to full llms.txt if topic search insufficient
- Use broader terms for better coverage
```

## Cannot Handle

### Password-Protected Documentation

**Limitation:**
- No access to authentication-required content
- Cannot log in to platforms
- No credential management
- Cannot access organization-internal docs

**Impact:**
- Enterprise documentation inaccessible
- Premium content unavailable
- Private beta docs unreachable
- Internal wikis not readable

**Workarounds:**
```
- Ask user for public alternatives
- Search for public subset of docs
- Use publicly available README/marketing
- Check if trial/demo access available
- Note limitation in report
```

**Report template:**
```markdown
⚠️ **Access Limitation**

Documentation requires authentication.

**What we can access**:
- Public README: [url]
- Package registry info: [url]
- Marketing site: [url]

**Cannot access**:
- Full documentation (requires login)
- Internal guides
- Premium content

**Recommendation**: Contact vendor for access or check if public docs available.
```

### Rate-Limited APIs

**Limitation:**
- No API credentials for authenticated access
- Subject to anonymous rate limits
- Cannot request increased limits
- No retry with authentication

**Impact:**
- Limited requests per hour (e.g., GitHub: 60/hour anonymous)
- May hit limits during comprehensive search
- Slower fallback required
- Incomplete coverage possible

**Workarounds:**
```
- Add delays between requests
- Use alternative sources (cached, mirrors)
- Prioritize critical pages
- Use Researcher agents instead of API
- Switch to repository analysis
```

**Detection:**
```
Symptoms:
- 429 Too Many Requests
- X-RateLimit-Remaining: 0
- Slow or refused connections

Response:
- Immediately switch to alternative method
- Don't retry same endpoint
- Note in report which method used
```

### Real-Time Documentation

**Limitation:**
- Uses snapshot at time of access
- Cannot monitor for updates
- No real-time synchronization
- May miss very recent changes

**Impact:**
- Documentation updated minutes ago may not be reflected
- Breaking changes announced today might be missed
- Latest release notes may not be current
- Version just released may not be documented

**Workarounds:**
```
- Note access date in report
- Recommend user verify if critical
- Check last-modified headers
- Compare with release dates
- Suggest official site for latest
```

**Report template:**
```markdown
ℹ️ **Snapshot Information**

Documentation retrieved: 2025-10-26 14:30 UTC

**Last-Modified** (if available):
- Main docs: 2025-10-24
- API reference: 2025-10-22

**Note**: For real-time updates, check official site: [url]
```

### Interactive Documentation

**Limitation:**
- Cannot run interactive examples
- Cannot execute code playgrounds
- No ability to test API calls
- Cannot verify functionality

**Impact:**
- Cannot confirm examples work
- Cannot test edge cases
- Cannot validate API responses
- Cannot verify performance claims

**Workarounds:**
```
- Provide code examples as-is
- Note: "Example provided, not tested"
- Recommend user run examples
- Link to interactive playground if available
- Include caveats about untested code
```

**Report template:**
```markdown
## Example Usage

```python
# Example from official docs (not tested)
import library
result = library.do_thing()
```

⚠️ **Note**: Example provided from documentation but not executed.
Please test in your environment.

**Interactive playground**: [url if available]
```

### Video-Only Documentation

**Limitation:**
- Cannot process video content directly
- Limited transcript access
- Cannot extract code from video
- Cannot parse visual diagrams

**Impact:**
- Video tutorials not usable
- YouTube courses inaccessible
- Screencasts not processable
- Visual walkthroughs unavailable

**Workarounds:**
```
- Search for transcript if available
- Look for accompanying blog post
- Find text-based alternative
- Check for community notes
- Use automated captions if available (low quality)
```

**Report template:**
```markdown
ℹ️ **Video Content Detected**

Primary documentation is video-based: [url]

**Alternatives found**:
- Blog post summary: [url]
- Community notes: [url]

**Cannot extract**:
- Detailed walkthrough from video
- Visual examples
- Demonstration steps

**Recommendation**: Watch video directly for visual content.
```

## May Struggle With

### Very Large Repositories (>1GB)

**Challenge:**
- Repomix may fail or hang
- Clone takes very long time
- Processing exceeds memory limits
- Output file too large to read

**Success rate:** ~30% for >1GB repos

**Mitigation:**
```
1. Try shallow clone: git clone --depth 1
2. Focus on docs only: repomix --include "docs/**"
3. Exclude binaries: --exclude "*.png,*.jpg,dist/**"
4. If fails: Use Explorer agents on specific files
5. Note limitation in report
```

**When to skip:**
```
Repository size indicators:
- Git clone shows >1GB download
- Contains large binaries (ml models, datasets)
- Has extensive history (>10k commits)
- Many multimedia files

→ Skip Repomix, use targeted exploration
```

### Documentation in Images/PDFs

**Challenge:**
- Cannot reliably extract text from images
- PDF parsing limited
- Formatting often lost
- Code snippets may be corrupted

**Success rate:** ~50% quality for PDFs, ~10% for images

**Mitigation:**
```
1. Search for text alternative
2. Try OCR if critical (low quality)
3. Provide image URL instead
4. Note content not extractable
5. Recommend manual review
```

**Report template:**
```markdown
⚠️ **Image-Based Documentation**

Primary documentation in PDF/images: [url]

**Extraction quality**: Limited
**Recommendation**: Download and review manually

**Text alternatives found**:
- [any alternatives]
```

### Non-English Documentation

**Challenge:**
- No automatic translation
- May miss context/nuance
- Technical terms may not translate well
- Examples may be language-specific

**Success rate:** Variable (depends on user needs)

**Mitigation:**
```
1. Note language in report
2. Offer key section translation if user requests
3. Search for English version
4. Check if bilingual docs exist
5. Provide original with language note
```

**Report template:**
```markdown
ℹ️ **Language Notice**

Primary documentation in: Japanese

**English availability**:
- Partial translation: [url]
- Community translation: [url]
- No official English version found

**Recommendation**: Use translation tool or request community help.
```

### Scattered Documentation

**Challenge:**
- Multiple sites/repositories
- Inconsistent structure
- Conflicting information
- No central source

**Success rate:** ~60% coverage

**Mitigation:**
```
1. Use Researcher agents
2. Prioritize official sources
3. Cross-reference findings
4. Note conflicts clearly
5. Take longer but be thorough
```

**Report template:**
```markdown
ℹ️ **Fragmented Documentation**

Information found across multiple sources:

**Official** (incomplete):
- Website: [url]
- Package registry: [url]

**Community** (supplementary):
- Stack Overflow: [url]
- Tutorial: [url]

**Note**: No centralized documentation. Information aggregated from
multiple sources. Conflicts resolved by prioritizing official sources.
```

### Deprecated/Legacy Libraries

**Challenge:**
- Documentation removed or archived
- Only old versions available
- Outdated information
- No current maintenance

**Success rate:** ~40% for fully deprecated libraries

**Mitigation:**
```
1. Use Internet Archive (Wayback Machine)
2. Search GitHub repository history
3. Check package registry for old README
4. Look for fork with docs
5. Note legacy status clearly
```

**Report template:**
```markdown
⚠️ **Legacy Library**

**Status**: Deprecated as of [date]
**Last update**: [date]

**Documentation sources**:
- Archived docs (via Wayback): [url]
- Repository (last commit [date]): [url]

**Recommendation**: Consider modern alternative: [suggestion]

**Migration path**: [if available]
```

## Success Criteria

### 1. Finds Relevant Information

**Measured by:**
- [ ] Answers user's specific question
- [ ] Covers requested topics
- [ ] Appropriate depth/detail
- [ ] Includes practical examples
- [ ] Links to additional resources

**Quality levels:**

**Excellent (100%):**
```
- All requested topics covered
- Examples for each major concept
- Clear, comprehensive information
- Official source, current version
- No gaps or limitations
```

**Good (80-99%):**
```
- Most requested topics covered
- Examples for core concepts
- Information mostly complete
- Official source, some gaps noted
- Minor limitations
```

**Acceptable (60-79%):**
```
- Core topics covered
- Some examples present
- Information somewhat complete
- Mix of official/community sources
- Some gaps noted
```

**Poor (<60%):**
```
- Only partial coverage
- Few or no examples
- Significant gaps
- Mostly unofficial sources
- Many limitations
```

### 2. Uses Most Efficient Method

**Measured by:**
- [ ] Started with llms.txt
- [ ] Used parallel agents appropriately
- [ ] Avoided unnecessary operations
- [ ] Completed in reasonable time
- [ ] Fell back efficiently when needed

**Efficiency score:**

**Optimal:**
```
- Found llms.txt immediately
- Parallel agents for all URLs
- Single batch processing
- Completed in <2 minutes
- No wasted operations
```

**Good:**
```
- Found llms.txt after 1-2 tries
- Mostly parallel processing
- Minimal sequential operations
- Completed in <5 minutes
- One minor inefficiency
```

**Acceptable:**
```
- Fell back to repository after llms.txt search
- Mix of parallel and sequential
- Some redundant operations
- Completed in <10 minutes
- A few inefficiencies
```

**Poor:**
```
- Didn't try llms.txt first
- Mostly sequential processing
- Many redundant operations
- Took >10 minutes
- Multiple inefficiencies
```

### 3. Completes in Reasonable Time

**Target times:**

| Scenario | Excellent | Good | Acceptable | Poor |
|----------|-----------|------|------------|------|
| Simple (1-5 URLs) | <1 min | 1-2 min | 2-5 min | >5 min |
| Medium (6-15 URLs) | <2 min | 2-4 min | 4-7 min | >7 min |
| Complex (16+ URLs) | <3 min | 3-6 min | 6-10 min | >10 min |
| Repository | <3 min | 3-6 min | 6-10 min | >10 min |
| Research | <5 min | 5-8 min | 8-12 min | >12 min |

**Factors affecting time:**
- Documentation structure (well-organized vs scattered)
- Source availability (llms.txt vs research)
- Content volume (few pages vs many)
- Network conditions (fast vs slow)
- Complexity (simple vs comprehensive)

### 4. Provides Clear Source Attribution

**Measured by:**
- [ ] Lists all sources used
- [ ] Notes method employed
- [ ] Includes URLs/references
- [ ] Identifies official vs community
- [ ] Credits authors when relevant

**Quality template:**

**Excellent:**
```markdown
## Sources

**Primary method**: llms.txt
**URL**: https://docs.library.com/llms.txt

**Documentation retrieved**:
1. Getting Started (official): [url]
2. API Reference (official): [url]
3. Examples (official): [url]

**Additional sources**:
- Repository: https://github.com/org/library
- Package registry: https://npmjs.com/package/library

**Method**: Parallel exploration with 3 agents
**Date**: 2025-10-26 14:30 UTC
```

### 5. Identifies Version/Date

**Measured by:**
- [ ] Documentation version noted
- [ ] Last-updated date included
- [ ] Matches user's version requirement
- [ ] Flags if version mismatch
- [ ] Notes if version unclear

**Best practice:**
```markdown
## Version Information

**Documentation version**: v3.2.1
**Last updated**: 2025-10-20
**Retrieved**: 2025-10-26

**User requested**: v3.x ✓ Match

**Note**: This is the latest stable version as of retrieval date.
```

### 6. Notes Limitations/Gaps

**Measured by:**
- [ ] Missing information identified
- [ ] Incomplete sections noted
- [ ] Known issues mentioned
- [ ] Alternatives suggested
- [ ] Workarounds provided

**Good practice:**
```markdown
## ⚠️ Limitations

**Incomplete documentation**:
- Advanced features section (stub page)
- Migration guide (404 error)

**Not available**:
- Video tutorials mentioned but not accessible
- Interactive examples require login

**Workarounds**:
- Advanced features: See examples in repository
- Migration: Check CHANGELOG.md for breaking changes

**Alternatives**:
- Community tutorial: [url]
- Stack Overflow: [url]
```

### 7. Well-Organized Output

**Measured by:**
- [ ] Clear structure
- [ ] Logical flow
- [ ] Easy to scan
- [ ] Actionable information
- [ ] Proper formatting

**Structure template:**
```markdown
# Documentation for [Library] [Version]

## Overview
[Brief description]

## Source
[Attribution]

## Installation
[Step-by-step]

## Quick Start
[Minimal example]

## Core Concepts
[Main ideas]

## API Reference
[Key methods]

## Examples
[Practical usage]

## Additional Resources
[Links]

## Limitations
[Any gaps]
```

## Quality Checklist

### Before Presenting Report

**Content quality:**
- [ ] Information is accurate
- [ ] Sources are official (or noted as unofficial)
- [ ] Version matches request
- [ ] Examples are clear
- [ ] No obvious errors

**Completeness:**
- [ ] All key topics covered
- [ ] Installation instructions present
- [ ] Usage examples included
- [ ] Configuration documented
- [ ] Troubleshooting information available

**Organization:**
- [ ] Logical flow
- [ ] Clear headings
- [ ] Proper code formatting
- [ ] Links working (spot check)
- [ ] Easy to scan

**Attribution:**
- [ ] Sources listed
- [ ] Method documented
- [ ] Version identified
- [ ] Date noted
- [ ] Limitations disclosed

**Usability:**
- [ ] Actionable information
- [ ] Copy-paste ready examples
- [ ] Next steps clear
- [ ] Resources for deep dive
- [ ] Known issues noted

## Performance Metrics

### Time-to-Value

**Measures:** How quickly user gets useful information

**Targets:**
```
First useful info: <30 seconds
Core coverage: <2 minutes
Complete report: <5 minutes
```

**Tracking:**
```
Start → llms.txt found → First URL fetched → Critical info extracted
  15s        30s               45s                  60s

User can act on info at 60s mark
(even if full report takes 5 minutes)
```

### Coverage Completeness

**Measures:** Percentage of user needs met

**Calculation:**
```
User needs 5 topics:
- Installation ✓
- Basic usage ✓
- API reference ✓
- Configuration ✓
- Examples ✗ (not found)

Coverage: 4/5 = 80%
```

**Targets:**
```
Excellent: 90-100%
Good: 75-89%
Acceptable: 60-74%
Poor: <60%
```

### Source Quality

**Measures:** Reliability of sources used

**Scoring:**
```
Official docs: 100 points
Official repository: 80 points
Package registry: 60 points
Recent community (verified): 40 points
Old community (unverified): 20 points
```

**Target:** Average >70 points

### User Satisfaction Indicators

**Positive signals:**
```
- User proceeds immediately with info
- No follow-up questions needed
- User says "perfect" or "thanks"
- User marks conversation complete
```

**Negative signals:**
```
- User asks same question differently
- User requests more details
- User says "incomplete" or "not what I needed"
- User abandons task
```

## Continuous Improvement

### Learn from Failures

**When documentation discovery struggles:**

1. **Document the issue**
   ```
   - What was attempted
   - What failed
   - Why it failed
   - How it was resolved (if at all)
   ```

2. **Identify patterns**
   ```
   - Is this library-specific?
   - Is this ecosystem-specific?
   - Is this a general limitation?
   ```

3. **Update strategies**
   ```
   - Add workaround to playbook
   - Update fallback sequence
   - Note limitation in documentation
   ```

### Measure and Optimize

**Track these metrics:**
```
- Average time to complete
- Coverage percentage
- Source quality score
- User satisfaction
- Failure rate by method
```

**Optimize based on data:**
```
- Which method succeeds most often?
- Which ecosystems need special handling?
- Where are time bottlenecks?
- What causes most failures?
```
