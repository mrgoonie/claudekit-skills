# Performance Optimization

Strategies and techniques for maximizing speed and efficiency in documentation discovery.

## Core Principles

### 0. Use context7.com for Instant llms.txt Access

**Fastest Approach:**

Direct URL construction instead of searching:
```
Traditional: WebSearch (15-30s) → WebFetch (5-10s) = 20-40s
context7.com: Direct WebFetch (5-10s) = 5-10s

Speed improvement: 2-4x faster
```

**Benefits:**
- No search required (instant URL construction)
- Consistent URL patterns
- Reliable availability
- Topic filtering for targeted results

**Examples:**
```
GitHub repo:
https://context7.com/vercel/next.js/llms.txt
→ Instant, no search needed

Website:
https://context7.com/websites/imgix/llms.txt
→ Instant, no search needed

Topic-specific:
https://context7.com/shadcn-ui/ui/llms.txt?topic=date
→ Filtered results, even faster
```

**Performance Impact:**
```
Without context7.com:
1. WebSearch for llms.txt: 15s
2. WebFetch llms.txt: 5s
3. Launch agents: 5s
Total: 25s

With context7.com:
1. Direct WebFetch: 5s
2. Launch agents: 5s
Total: 10s (2.5x faster!)

With context7.com + topic:
1. Direct WebFetch (filtered): 3s
2. Process focused results: 2s
Total: 5s (5x faster!)
```

### 1. Minimize Sequential Operations

**The Problem:**

Sequential operations add up linearly:
```
Total Time = Op1 + Op2 + Op3 + ... + OpN
```

Example:
```
Fetch URL 1: 5 seconds
Fetch URL 2: 5 seconds
Fetch URL 3: 5 seconds
Total: 15 seconds
```

**The Solution:**

Parallel operations complete in max time of slowest:
```
Total Time = max(Op1, Op2, Op3, ..., OpN)
```

Example:
```
Launch 3 agents simultaneously
All complete in: ~5 seconds
Total: 5 seconds (3x faster!)
```

### 2. Batch Related Operations

**Benefits:**
- Fewer context switches
- Better resource utilization
- Easier to track
- More efficient aggregation

**Grouping Strategies:**

**By topic:**
```
Agent 1: All authentication-related docs
Agent 2: All database-related docs
Agent 3: All API-related docs
```

**By content type:**
```
Agent 1: All tutorials
Agent 2: All reference docs
Agent 3: All examples
```

**By priority:**
```
Phase 1 (critical): Getting started, installation, core concepts
Phase 2 (important): Guides, API reference, configuration
Phase 3 (optional): Advanced topics, internals, optimization
```

### 3. Smart Caching

**What to cache:**
- Repomix output (expensive to generate)
- llms.txt content (static)
- Repository structure (rarely changes)
- Documentation URLs (reference list)

**When to refresh:**
- User requests specific version
- Documentation updated (check last-modified)
- Cache older than session
- User explicitly requests fresh data

### 4. Early Termination

**When to stop:**
```
✓ User's core needs met
✓ Critical information found
✓ Time limit approaching
✓ Diminishing returns (90% coverage achieved)
```

**How to decide:**
```
After Phase 1 (critical docs):
- Review what was found
- Check against user request
- If 80%+ covered → deliver now
- Offer to fetch more if needed
```

## Performance Patterns

### Pattern 1: Parallel Exploration

**Scenario:** llms.txt contains 10 URLs

**Slow approach (sequential):**
```
Time: 10 URLs × 5 seconds = 50 seconds

Step 1: Fetch URL 1 (5s)
Step 2: Fetch URL 2 (5s)
Step 3: Fetch URL 3 (5s)
...
Step 10: Fetch URL 10 (5s)
```

**Fast approach (parallel):**
```
Time: ~5-10 seconds total

Step 1: Launch 5 Explorer agents (simultaneous)
  Agent 1: URLs 1-2
  Agent 2: URLs 3-4
  Agent 3: URLs 5-6
  Agent 4: URLs 7-8
  Agent 5: URLs 9-10

Step 2: Wait for all (max time: ~5-10s)
Step 3: Aggregate results
```

**Speedup:** 5-10x faster

### Pattern 2: Lazy Loading

**Scenario:** Documentation has 30+ pages

**Slow approach (fetch everything):**
```
Time: 30 URLs × 5 seconds ÷ 5 agents = 30 seconds

Fetch all 30 pages upfront
User only needs 5 of them
Wasted: 25 pages × 5 seconds ÷ 5 = 25 seconds
```

**Fast approach (priority loading):**
```
Time: 10 URLs × 5 seconds ÷ 5 agents = 10 seconds

Phase 1: Fetch critical 10 pages
Review: Does this cover user's needs?
If yes: Stop here (saved 20 seconds)
If no: Fetch additional as needed
```

**Speedup:** Up to 3x faster for typical use cases

### Pattern 3: Smart Fallbacks

**Scenario:** llms.txt not found

**Slow approach (exhaustive search):**
```
Time: ~5 minutes

Try: docs.library.com/llms.txt (30s timeout)
Try: library.dev/llms.txt (30s timeout)
Try: library.io/llms.txt (30s timeout)
Try: library.org/llms.txt (30s timeout)
Try: www.library.com/llms.txt (30s timeout)
Then: Fall back to repository
```

**Fast approach (quick fallback):**
```
Time: ~1 minute

Try: docs.library.com/llms.txt (15s)
Try: library.dev/llms.txt (15s)
Not found → Immediately try repository (30s)
```

**Speedup:** 5x faster

### Pattern 4: Incremental Results

**Scenario:** Large documentation set

**Slow approach (all-or-nothing):**
```
Time: 5 minutes until first result

Fetch all documentation
Aggregate everything
Present complete report
User waits 5 minutes
```

**Fast approach (streaming):**
```
Time: 30 seconds to first result

Phase 1: Fetch critical docs (30s)
Present: Initial findings
Phase 2: Fetch important docs (60s)
Update: Additional findings
Phase 3: Fetch supplementary (90s)
Final: Complete report
```

**Benefit:** User gets value immediately, can stop early if satisfied

## Optimization Techniques

### Technique 1: Workload Balancing

**Problem:** Uneven distribution causes bottlenecks

```
Bad distribution:
Agent 1: 1 URL (small) → finishes in 5s
Agent 2: 10 URLs (large) → finishes in 50s
Total: 50s (bottlenecked by Agent 2)
```

**Solution:** Balance by estimated size

```
Good distribution:
Agent 1: 3 URLs (medium pages) → ~15s
Agent 2: 3 URLs (medium pages) → ~15s
Agent 3: 3 URLs (medium pages) → ~15s
Agent 4: 1 URL (large page) → ~15s
Total: ~15s (balanced)
```

### Technique 2: Request Coalescing

**Problem:** Redundant requests slow things down

```
Bad:
Agent 1: Fetch README.md
Agent 2: Fetch README.md (duplicate!)
Agent 3: Fetch README.md (duplicate!)
Wasted: 2 redundant fetches
```

**Solution:** Deduplicate before fetching

```
Good:
Pre-processing: Identify unique URLs
Agent 1: Fetch README.md (once)
Agent 2: Fetch INSTALL.md
Agent 3: Fetch API.md
Share: README.md content across agents if needed
```

### Technique 3: Timeout Tuning

**Problem:** Default timeouts too conservative

```
Slow:
WebFetch timeout: 120s (too long for fast sites)
If site is down: Wait 120s before failing
```

**Solution:** Adaptive timeouts

```
Fast:
Known fast sites (official docs): 30s timeout
Unknown sites: 60s timeout
Large repos: 120s timeout
If timeout hit: Immediately try alternative
```

### Technique 4: Selective Fetching

**Problem:** Fetching irrelevant content

```
Wasteful:
Fetch: Installation guide ✓ (needed)
Fetch: API reference ✓ (needed)
Fetch: Internal architecture ✗ (not needed for basic usage)
Fetch: Contributing guide ✗ (not needed)
Fetch: Changelog ✗ (not needed)
```

**Solution:** Filter by user needs

```
Efficient:
User need: "How to get started"
Fetch only: Installation, basic usage, examples
Skip: Advanced topics, internals, contribution
Speedup: 50% less fetching
```

## Performance Benchmarks

### Target Times

| Scenario | Target Time | Acceptable | Too Slow |
|----------|-------------|------------|----------|
| Single URL | <10s | 10-20s | >20s |
| llms.txt (5 URLs) | <30s | 30-60s | >60s |
| llms.txt (15 URLs) | <60s | 60-120s | >120s |
| Repository analysis | <2min | 2-5min | >5min |
| Research fallback | <3min | 3-7min | >7min |

### Real-World Examples

**Fast case (Next.js with llms.txt):**
```
00:00 - Start
00:05 - Found llms.txt
00:10 - Fetched content (12 URLs)
00:15 - Launched 4 agents
00:45 - All agents complete
00:55 - Report ready
Total: 55 seconds ✓
```

**Medium case (Repository without llms.txt):**
```
00:00 - Start
00:15 - llms.txt not found
00:20 - Found repository
00:30 - Cloned repository
02:00 - Repomix complete
02:30 - Analyzed output
02:45 - Report ready
Total: 2m 45s ✓
```

**Slow case (Scattered documentation):**
```
00:00 - Start
00:30 - llms.txt not found
00:45 - Repository not found
01:00 - Launched 4 Researcher agents
05:00 - All research complete
06:00 - Aggregated findings
06:30 - Report ready
Total: 6m 30s (acceptable for research)
```

## Common Performance Issues

### Issue 1: Too Many Agents

**Symptom:** Slower than sequential

```
Problem:
Launched 15 agents for 15 URLs
Overhead: Agent initialization, coordination
Result: Slower than 5 agents with 3 URLs each
```

**Solution:**
```
Max 7 agents per batch
Group URLs sensibly
Use phases for large sets
```

### Issue 2: Blocking Operations

**Symptom:** Agents waiting unnecessarily

```
Problem:
Agent 1: Fetch URL, wait for Agent 2
Agent 2: Fetch URL, wait for Agent 3
Agent 3: Fetch URL
Result: Sequential instead of parallel
```

**Solution:**
```
Launch all agents independently
No dependencies between agents
Aggregate after all complete
```

### Issue 3: Redundant Fetching

**Symptom:** Same content fetched multiple times

```
Problem:
Phase 1: Fetch installation guide
Phase 2: Fetch installation guide again
Result: Wasted time
```

**Solution:**
```
Cache fetched content
Check cache before fetching
Reuse within session
```

### Issue 4: Late Bailout

**Symptom:** Continuing when should stop

```
Problem:
Found 90% of needed info after 1 minute
Spent 4 more minutes on remaining 10%
Result: 5x time for marginal gain
```

**Solution:**
```
Check progress after critical phase
If 80%+ covered → offer to stop
Only continue if user wants comprehensive
```

## Performance Monitoring

### Key Metrics

**Track these times:**
```
- llms.txt discovery: Target <30s
- Repository clone: Target <60s
- Repomix processing: Target <2min
- Agent exploration: Target <60s
- Total time: Target <3min for typical case
```

### Performance Report Template

```markdown
## Performance Summary

**Total time**: 1m 25s
**Method**: llms.txt + parallel exploration

**Breakdown**:
- Discovery: 15s (llms.txt search & fetch)
- Exploration: 50s (4 agents, 12 URLs)
- Aggregation: 20s (synthesis & formatting)

**Efficiency**: 8.5x faster than sequential
(12 URLs × 5s = 60s sequential, actual: 50s parallel)
```

### When to Optimize Further

Optimize if:
- [ ] Total time >2x target
- [ ] User explicitly requests "fast"
- [ ] Repeated similar queries (cache benefit)
- [ ] Large documentation set (>20 URLs)

Don't over-optimize if:
- [ ] Already meeting targets
- [ ] One-time query
- [ ] User values completeness over speed
- [ ] Research requires thoroughness

## Quick Optimization Checklist

### Before Starting

- [ ] Check if content already cached
- [ ] Identify fastest method for this case
- [ ] Plan for parallel execution
- [ ] Set appropriate timeouts

### During Execution

- [ ] Launch agents in parallel (not sequential)
- [ ] Use single message for multiple agents
- [ ] Monitor for bottlenecks
- [ ] Be ready to terminate early

### After First Phase

- [ ] Assess coverage achieved
- [ ] Determine if user needs met
- [ ] Decide: continue or deliver now
- [ ] Cache results for potential reuse

### Optimization Decision Tree

```
Need documentation?
  ↓
Check cache
  ↓
HIT → Use cached (0s) ✓
MISS → Continue
  ↓
llms.txt available?
  ↓
YES → Parallel agents (30-60s) ✓
NO → Continue
  ↓
Repository available?
  ↓
YES → Repomix (2-5min)
NO → Research (3-7min)
  ↓
After Phase 1:
80%+ coverage?
  ↓
YES → Deliver now (save time) ✓
NO → Continue to Phase 2
```
