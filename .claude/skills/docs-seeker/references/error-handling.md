# Error Handling Guide

Comprehensive troubleshooting and error resolution strategies for documentation discovery.

## context7.com Not Accessible

### Symptoms

- 404 error (library not indexed)
- Connection timeout
- Server error (500)
- Empty response

### Troubleshooting Steps

**1. Verify URL pattern:**

For GitHub repos:
```
✓ Correct: https://context7.com/vercel/next.js/llms.txt
✗ Wrong: https://context7.com/nextjs/llms.txt
```

For websites:
```
✓ Correct: https://context7.com/websites/imgix/llms.txt
✗ Wrong: https://context7.com/docs.imgix.com/llms.txt
```

**2. Try official llms.txt as fallback:**
```
https://docs.[library].com/llms.txt
https://[library].dev/llms.txt
https://[library].io/llms.txt
```

**3. Search for llms.txt if still not found:**
```
WebSearch: "[library] llms.txt"
WebSearch: "[library] documentation AI format"
```

**4. Fall back to repository analysis:**
- If no llms.txt available anywhere
- Note in report: "llms.txt not available, used repository analysis"

### Common Causes

- Library not yet indexed by context7.com
- Very new or obscure library
- Private repository
- context7.com temporary outage

### Example Resolution

```
Problem: https://context7.com/org/new-lib/llms.txt returns 404

Steps:
1. Check official site: https://new-lib.dev/llms.txt ✗ Not found
2. WebSearch for llms.txt ✗ Not found
3. Fall back to repository: https://github.com/org/new-lib ✓ Found
4. Use Repomix for documentation extraction
5. Note in report: "No llms.txt available, analyzed repository directly"
```

## llms.txt Not Accessible (Official Sites)

### Symptoms

- 404 error
- Connection timeout
- Access denied (403)
- Empty response

### Troubleshooting Steps

**1. ALWAYS try context7.com first:**
```
https://context7.com/{org}/{repo}/llms.txt
```

**2. Try alternative official domains:**
```
https://[name].dev/llms.txt
https://[name].io/llms.txt
https://[name].com/llms.txt
https://docs.[name].com/llms.txt
https://www.[name].com/llms.txt
```

**3. Check for redirects:**
- Old domain → new domain
- Non-HTTPS → HTTPS
- www → non-www or vice versa
- Root → /docs subdirectory

**4. Search for llms.txt mention:**
```
WebSearch: "[library] llms.txt"
WebSearch: "[library] documentation AI format"
```

**5. Check documentation announcements:**
- Blog posts about llms.txt
- GitHub discussions
- Recent release notes

**6. If all fail:**
- Fall back to repository analysis (Phase 3)
- Note in report: "llms.txt not available"

### Common Causes

- Documentation recently moved/redesigned
- llms.txt not yet implemented
- Domain configuration issues
- Rate limiting or IP blocking
- Firewall/security restrictions

### Example Resolution

```
Problem: https://example.dev/llms.txt returns 404

Steps:
1. Try: https://docs.example.dev/llms.txt ✓ Works!
2. Note: Documentation moved to docs subdomain
3. Proceed with Phase 2 using correct URL
```

## Repository Not Found

### Symptoms

- GitHub 404 error
- No official repository found
- Repository is private/requires auth
- Multiple competing repositories

### Troubleshooting Steps

**1. Search official website:**
```
WebSearch: "[library] official website"
```

**2. Check package registries:**
```
WebSearch: "[library] npm"
WebSearch: "[library] pypi"
WebSearch: "[library] crates.io"
```

**3. Look for organization GitHub:**
```
WebSearch: "[company] github organization"
WebSearch: "[library] github org:[known-org]"
```

**4. Check for mirrors or forks:**
```
WebSearch: "[library] github mirror"
WebSearch: "[library] source code"
```

**5. Verify through package manager:**
```bash
# npm example
npm info [package-name] repository

# pip example
pip show [package-name]
```

**6. If all fail:**
- Use Researcher agents (Phase 4)
- Note: "No public repository available"

### Common Causes

- Proprietary/closed-source software
- Documentation separate from code repository
- Company uses internal hosting (GitLab, Bitbucket, self-hosted)
- Project discontinued or archived
- Repository renamed/moved

### Verification Checklist

When you find a repository, verify:
- [ ] Organization/user matches official entity
- [ ] Star count appropriate for library popularity
- [ ] Recent commits (active maintenance)
- [ ] README mentions official status
- [ ] Links back to official website
- [ ] License matches expectations

## Repomix Failures

### Symptoms

- Out of memory error
- Command hangs indefinitely
- Output file empty or corrupted
- Permission errors
- Network timeout during clone

### Troubleshooting Steps

**1. Check repository size:**
```bash
# Clone and check size
git clone [url] /tmp/test-repo
du -sh /tmp/test-repo

# If >500MB, use focused approach
```

**2. Focus on documentation only:**
```bash
repomix --include "docs/**,README.md,*.md" --output docs.xml
```

**3. Exclude large files:**
```bash
repomix --exclude "*.png,*.jpg,*.pdf,*.zip,dist/**,build/**,node_modules/**" --output repomix-output.xml
```

**4. Use shallow clone:**
```bash
git clone --depth 1 [url] /tmp/docs-analysis
cd /tmp/docs-analysis
repomix --output repomix-output.xml
```

**5. Alternative: Explorer agents**
```
If Repomix fails completely:
1. Read README.md directly
2. List /docs directory structure
3. Launch Explorer agents for key files
4. Read specific documentation files
```

**6. Check system resources:**
```bash
# Check disk space
df -h /tmp

# Check available memory
free -h

# Kill if hung
pkill -9 repomix
```

### Common Causes

- Repository too large (>1GB)
- Many binary files (images, videos)
- Large commit history
- Insufficient disk space
- Memory constraints
- Slow network connection
- Repository has submodules

### Size Guidelines

| Repo Size | Strategy |
|-----------|----------|
| <50MB | Full Repomix |
| 50-200MB | Exclude binaries |
| 200-500MB | Focus on /docs |
| 500MB-1GB | Shallow clone + focus |
| >1GB | Explorer agents only |

## Multiple Conflicting Sources

### Symptoms

- Different installation instructions
- Conflicting API signatures
- Contradictory recommendations
- Version mismatches
- Breaking changes not documented

### Resolution Steps

**1. Check version of each source:**
```
- Note documentation version number
- Check last-updated date
- Check URL for version indicator (v1/, v2/)
- Look for version selector on page
```

**2. Prioritize sources:**
```
Priority order:
1. Official docs (latest version)
2. Official docs (specified version)
3. Package registry (verified)
4. Official repository README
5. Community tutorials (recent)
6. Stack Overflow (recent, high votes)
7. Blog posts (date-verified)
```

**3. Present both with context:**
```markdown
## Installation (v1.x - Legacy)
[old method]
Source: [link] (Last updated: [date])

## Installation (v2.x - Current)
[new method]
Source: [link] (Last updated: [date])

⚠️ Note: v2.x is recommended for new projects.
Migration guide: [link]
```

**4. Cross-reference:**
- Check if conflict is intentional (breaking change)
- Look for migration guides
- Check changelog/release notes
- Verify in GitHub issues/discussions

**5. Document discrepancy:**
```markdown
## ⚠️ Conflicting Information Found

**Source 1** (official docs): Method A
**Source 2** (repository): Method B

**Analysis**: Source 1 reflects v2.x API. Source 2 README
not yet updated. Confirmed via changelog [link].

**Recommendation**: Use Method A (official docs).
```

### Version Identification

**Check these locations:**
```
- URL path: /docs/v2/...
- Page header/footer
- Version selector dropdown
- Git branch/tag
- Package.json or equivalent
- CHANGELOG.md date correlation
```

## Rate Limiting

### Symptoms

- 429 Too Many Requests
- 403 Forbidden (temporary)
- Slow responses
- Connection refused
- "Rate limit exceeded" message

### Solutions

**1. Add delays between requests:**
```bash
# Add 2-second delay
sleep 2
```

**2. Use alternative sources:**
```
Priority fallback chain:
GitHub → Official docs → Package registry → Repository → Archive
```

**3. Batch operations:**
```
Instead of:
- WebFetch URL 1
- WebFetch URL 2
- WebFetch URL 3

Use:
- Launch 3 Explorer agents (single batch)
```

**4. Cache aggressively:**
```
- Reuse fetched content within session
- Don't re-fetch same URLs
- Store repomix output for reuse
- Note fetch time, reuse if <1 hour old
```

**5. Check rate limit headers:**
```
If available:
- X-RateLimit-Remaining
- X-RateLimit-Reset
- Retry-After
```

**6. Respect robots.txt:**
```bash
# Check before aggressive crawling
curl https://example.com/robots.txt
```

### Rate Limit Recovery

**GitHub API (if applicable):**
```
- Anonymous: 60 requests/hour
- Authenticated: 5000 requests/hour
- Wait period: 1 hour from first request
```

**General approach:**
```
1. Detect rate limit (429 or slow responses)
2. Switch to alternative source immediately
3. Don't retry same endpoint repeatedly
4. Note in report: "Rate limit encountered, used [alternative]"
```

## Network Timeouts

### Symptoms

- Request hangs indefinitely
- Connection timeout error
- No response received
- Partial content received

### Solutions

**1. Set explicit timeouts:**
```
WebSearch: 30 seconds max
WebFetch: 60 seconds max
Repository clone: 5 minutes max
Repomix processing: 10 minutes max
```

**2. Retry with timeout:**
```
1st attempt: 60 seconds
2nd attempt: 90 seconds (if needed)
3rd attempt: Switch to alternative method
```

**3. Check network connectivity:**
```bash
# Test basic connectivity
ping -c 3 8.8.8.8

# Test DNS resolution
nslookup docs.example.com

# Test specific host
curl -I https://docs.example.com
```

**4. Use alternative endpoints:**
```
If main site times out:
- Try CDN version
- Try regional mirror
- Try cached version (Google Cache, Archive.org)
```

**5. Fall back gracefully:**
```
Main docs timeout → Repository → Package registry → Research
```

## Incomplete Documentation

### Symptoms

- Documentation stub pages
- "Coming soon" sections
- Broken links (404)
- Missing API reference
- Outdated examples

### Handling Strategy

**1. Identify gaps:**
```markdown
## Documentation Status

✅ Available:
- Installation guide
- Basic usage examples

⚠️ Incomplete:
- Advanced features (stub page)
- API reference (404 links)

❌ Missing:
- Migration guide
- Performance optimization
```

**2. Supplement from repository:**
```
- Check /examples directory
- Read test files for usage
- Analyze TypeScript definitions
- Check CHANGELOG for features
```

**3. Use community sources:**
```
- Recent Stack Overflow answers
- GitHub discussions
- Blog posts from maintainers
- Video tutorials
```

**4. Note limitations clearly:**
```markdown
⚠️ **Documentation Limitations**

Official docs incomplete (as of [date]).
The following information inferred from:
- Repository examples
- TypeScript definitions
- Community discussions

May not reflect official recommendations.
```

## Authentication/Access Issues

### Symptoms

- Private repository
- Login required
- Organization-only access
- Documentation behind paywall

### Solutions

**1. For private repositories:**
```
- Note: "Repository is private"
- Check for public mirror
- Look for public documentation site
- Search package registry for info
```

**2. For paywalled docs:**
```
- Check for free tier/trial
- Look for open-source alternative
- Search for community mirrors
- Use package registry info instead
```

**3. Document access limitation:**
```markdown
## ⚠️ Access Limitation

Official repository is private. This report based on:
- Public documentation site: [url]
- Package registry info: [url]
- Community resources: [urls]

May not include internal implementation details.
```

## Error Handling Best Practices

### General Principles

1. **Fail fast**: Don't retry same method repeatedly
2. **Fall back**: Have alternative strategies ready
3. **Document**: Note what failed and why
4. **Inform user**: Clear about limitations
5. **Partial success**: Deliver what you can find

### Error Reporting Template

```markdown
## ⚠️ Discovery Issues Encountered

**Primary method**: [method] - [reason for failure]
**Fallback used**: [alternative method]
**Information completeness**: [percentage or description]

**What was found**:
- [list available information]

**What is missing**:
- [list gaps]

**Recommended action**:
- [how user can get missing info]
```

### Recovery Decision Tree

```
Error encountered
  ↓
Is there an obvious alternative?
  YES → Try alternative immediately
  NO → Continue below
  ↓
Have we tried all primary methods?
  NO → Try next method in sequence
  YES → Continue below
  ↓
Is partial information useful?
  YES → Deliver partial results with notes
  NO → Inform user, request guidance
```
