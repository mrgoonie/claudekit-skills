# Testing Pyramid Strategy

## Classic 70-20-10 Ratio

```
       E2E (10%)        Slow, expensive, critical paths
      /----------\
     / Integration\     20% - APIs, database
    /--------------\
   /   Unit Tests    \  70% - Fast, cheap, logic
  /____________________\
```

## Ratios by Context

| Context | Unit | Integration | E2E |
|---------|------|-------------|-----|
| Classic | 70% | 20% | 10% |
| Heavy frontend | 60% | 25% | 15% |
| API-heavy | 75% | 15% | 10% |
| Critical transactions | 60% | 20% | 20% |

## Cost-Benefit

| Type | Cost | Speed | Bug Coverage |
|------|------|-------|--------------|
| Unit | Low | <50ms | 70% |
| Integration | Medium | 100-500ms | 20% |
| E2E | High | 5-30s | 10% |

## Test Organization

```
tests/
├── unit/           # 70%
├── integration/    # 20%
├── e2e/            # 10%
└── fixtures/
```

## Priority Matrix

| Priority | Category | Examples |
|----------|----------|----------|
| P0 | Core flows | Signup, login, checkout |
| P1 | Major features | Search, CRUD, nav |
| P2 | Secondary | Filters, sorting |
| P3 | Edge cases | Empty states, limits |

## When to Use Each

- **Unit**: Pure functions, utilities, state logic
- **Integration**: API endpoints, database ops, modules
- **E2E**: Critical journeys, checkout, payments

## CI/CD Order

```yaml
- run: npm run test:unit        # Gate 1: Fast fail
- run: npm run test:integration # Gate 2
- run: npm run test:e2e         # Gate 3: Pre-merge
```

## Coverage Targets

| Area | Target |
|------|--------|
| Critical paths | 100% |
| Core features | 80-90% |
| Overall | 75-85% |
