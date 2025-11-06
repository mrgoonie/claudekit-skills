# Sequential Thinking Examples

## Example 1: Database Performance Problem

**Context**: API endpoints timing out, need to diagnose and fix.

```typescript
// Thought 1
{
  thought: "API timeout reports indicate database bottleneck. Need to profile queries first.",
  thoughtNumber: 1,
  totalThoughts: 6,
  nextThoughtNeeded: true
}

// Thought 2
{
  thought: "Query logs show user profile endpoint makes 50+ queries per request. Classic N+1 pattern.",
  thoughtNumber: 2,
  totalThoughts: 6,
  nextThoughtNeeded: true
}

// Thought 3
{
  thought: "Need to implement eager loading for relationships. Checking ORM documentation for optimal approach.",
  thoughtNumber: 3,
  totalThoughts: 7, // Adjusted scope
  nextThoughtNeeded: true
}

// Thought 4
{
  thought: "ORM supports `include` for eager loading. Will need to modify 3 endpoints: /profile, /dashboard, /settings.",
  thoughtNumber: 4,
  totalThoughts: 7,
  nextThoughtNeeded: true
}

// Thought 5
{
  thought: "Implementation complete. Testing shows queries reduced from 52 to 4 per request. Response time: 2.1s → 180ms.",
  thoughtNumber: 5,
  totalThoughts: 6, // Fewer steps than expected
  nextThoughtNeeded: true
}

// Thought 6
{
  thought: "Success. Solution: eager loading eliminated N+1 queries. Next: add query monitoring to catch similar issues early.",
  thoughtNumber: 6,
  totalThoughts: 6,
  nextThoughtNeeded: false // Done
}
```

## Example 2: Architecture Decision with Branching

**Context**: Choosing between microservices and monolith for new project.

```typescript
// Thought 1
{
  thought: "Need to decide architecture. Key factors: team size (5 devs), timeline (3 months), expected scale (10k users initially).",
  thoughtNumber: 1,
  totalThoughts: 8,
  nextThoughtNeeded: true
}

// Thought 2
{
  thought: "Two viable approaches: monolith for simplicity or microservices for scalability. Need to evaluate both.",
  thoughtNumber: 2,
  totalThoughts: 10,
  nextThoughtNeeded: true
}

// Branch A: Monolith approach
{
  thought: "Monolith pros: faster development, simpler deployment, easier debugging. Cons: potential future refactor cost.",
  thoughtNumber: 3,
  totalThoughts: 6,
  branchFromThought: 2,
  branchId: "monolith",
  nextThoughtNeeded: true
}

{
  thought: "For 10k users, single server handles load easily. Deployment: single container, straightforward CI/CD.",
  thoughtNumber: 4,
  totalThoughts: 6,
  branchId: "monolith",
  nextThoughtNeeded: true
}

{
  thought: "Dev velocity high—team can ship in 3 months. Future scaling: can extract services later if needed.",
  thoughtNumber: 5,
  totalThoughts: 6,
  branchId: "monolith",
  nextThoughtNeeded: true
}

// Branch B: Microservices approach
{
  thought: "Microservices pros: independent scaling, service isolation. Cons: complexity overhead, distributed systems challenges.",
  thoughtNumber: 3,
  totalThoughts: 7,
  branchFromThought: 2,
  branchId: "microservices",
  nextThoughtNeeded: true
}

{
  thought: "For 5-person team: significant overhead in service coordination, API contracts, infrastructure management.",
  thoughtNumber: 4,
  totalThoughts: 7,
  branchId: "microservices",
  nextThoughtNeeded: true
}

{
  thought: "Timeline risk: 3 months insufficient for robust microservices implementation. Need distributed tracing, service mesh, etc.",
  thoughtNumber: 5,
  totalThoughts: 7,
  branchId: "microservices",
  nextThoughtNeeded: true
}

// Convergence
{
  thought: "Comparing branches: monolith clearly better fit. Small team, tight timeline, modest initial scale. Microservices overhead unjustified.",
  thoughtNumber: 6,
  totalThoughts: 7,
  nextThoughtNeeded: true
}

{
  thought: "Decision: monolith with modular design. Extract services later if specific components need independent scaling.",
  thoughtNumber: 7,
  totalThoughts: 7,
  nextThoughtNeeded: false
}
```

## Example 3: Debugging with Revision

**Context**: Feature works in dev, fails in production.

```typescript
// Thought 1
{
  thought: "Payment processing works locally but fails in prod. Checking error logs.",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true
}

// Thought 2
{
  thought: "Logs show 'Connection refused' to payment API. Likely firewall or network config issue.",
  thoughtNumber: 2,
  totalThoughts: 5,
  nextThoughtNeeded: true
}

// Thought 3
{
  thought: "Checked firewall rules—payment API port (443) is open. Must be something else.",
  thoughtNumber: 3,
  totalThoughts: 6,
  nextThoughtNeeded: true
}

// Thought 4 - Revision
{
  thought: "Wait—reviewing logs more carefully. Error message includes 'certificate verify failed'. Not firewall, it's SSL/TLS issue.",
  thoughtNumber: 4,
  totalThoughts: 6,
  isRevision: true,
  revisesThought: 2,
  nextThoughtNeeded: true
}

// Thought 5
{
  thought: "Prod environment missing intermediate CA certificates. Dev works because it uses self-signed cert with verification disabled.",
  thoughtNumber: 5,
  totalThoughts: 6,
  nextThoughtNeeded: true
}

// Thought 6
{
  thought: "Installed CA bundle on prod server. Payment processing now works. Root cause: incomplete SSL cert chain.",
  thoughtNumber: 6,
  totalThoughts: 6,
  nextThoughtNeeded: false
}
```

## Example 4: Complex Feature Planning

**Context**: Building real-time collaborative editing feature.

```typescript
// Thought 1
{
  thought: "Real-time collab editing requires: WebSocket connections, operational transformation or CRDT, conflict resolution, presence tracking.",
  thoughtNumber: 1,
  totalThoughts: 12,
  nextThoughtNeeded: true
}

// Thought 2
{
  thought: "Core decision: OT vs CRDT. OT requires central server for transform logic, CRDT enables P2P. For our use case, CRDT better.",
  thoughtNumber: 2,
  totalThoughts: 12,
  nextThoughtNeeded: true
}

// Thought 3
{
  thought: "Research CRDT libraries: Yjs (popular, mature), Automerge (good TypeScript support). Yjs has better performance benchmarks.",
  thoughtNumber: 3,
  totalThoughts: 14, // Scope expanding
  nextThoughtNeeded: true
}

// Thought 4
{
  thought: "Architecture: Yjs + WebSocket provider + persistence layer. Client-side: Yjs doc syncs via WebSocket. Server: broadcast updates + store snapshots.",
  thoughtNumber: 4,
  totalThoughts: 14,
  nextThoughtNeeded: true
}

// Thought 5
{
  thought: "Implementation phases: (1) Basic sync, (2) Presence/cursors, (3) Persistence, (4) Conflict UI. Estimate 4 weeks total.",
  thoughtNumber: 5,
  totalThoughts: 14,
  nextThoughtNeeded: true
}

// ... continues through implementation details

// Final thought
{
  thought: "Plan complete. MVP: Yjs + WebSocket + Redis persistence. 4-week timeline. Main risk: scaling WebSocket connections—mitigate with load balancer sticky sessions.",
  thoughtNumber: 14,
  totalThoughts: 14,
  nextThoughtNeeded: false
}
```

## Usage Patterns Summary

| Scenario | Pattern | Key Features |
|----------|---------|--------------|
| Linear problem-solving | Sequential thoughts | Steady progress, scope adjustment |
| Exploring alternatives | Branching | Multiple paths from decision point |
| Correcting mistakes | Revision | Reference earlier thought, update conclusion |
| Complex analysis | Mixed | Combine all features as needed |

## Tips for Effective Use

1. **Start broad, narrow down**: Early thoughts explore problem space, later thoughts dive into specifics
2. **Show your work**: Document reasoning process, not just conclusions
3. **Revise when wrong**: Don't continue down incorrect path—backtrack and correct
4. **Branch at crossroads**: When facing clear alternatives, explore each systematically
5. **Adjust dynamically**: Change `totalThoughts` as understanding evolves
6. **End decisively**: Final thought should summarize conclusion and next actions
