# CI/CD Integration

Integrate Claude Code into development workflows with GitHub Actions and GitLab CI/CD.

## GitHub Actions

### Basic Workflow

**.github/workflows/claude.yml:**
```yaml
name: Claude Code CI

on: [push, pull_request]

jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: anthropic/claude-code-action@v1
        with:
          command: '/fix:types && /test'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Code Review Workflow

```yaml
name: Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Review with Claude
        uses: anthropic/claude-code-action@v1
        with:
          command: |
            Review the changes in this PR:
            - Check for bugs and edge cases
            - Verify test coverage
            - Assess performance implications
            - Review security concerns
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Post Review Comment
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: process.env.CLAUDE_OUTPUT
            })
```

### Test & Fix Workflow

```yaml
name: Test and Fix

on: [push]

jobs:
  test-fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Tests
        id: test
        continue-on-error: true
        run: npm test

      - name: Fix Failures
        if: steps.test.outcome == 'failure'
        uses: anthropic/claude-code-action@v1
        with:
          command: '/fix:test check test output and fix failures'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Commit Fixes
        if: steps.test.outcome == 'failure'
        run: |
          git config user.name "Claude Bot"
          git config user.email "claude@anthropic.com"
          git add .
          git commit -m "fix: auto-fix test failures"
          git push
```

### Documentation Update

```yaml
name: Update Docs

on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Update Documentation
        uses: anthropic/claude-code-action@v1
        with:
          command: '/docs:update'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Commit Docs
        run: |
          git config user.name "Claude Bot"
          git config user.email "claude@anthropic.com"
          git add docs/
          git commit -m "docs: auto-update documentation" || echo "No changes"
          git push
```

## GitLab CI/CD

### Basic Pipeline

**.gitlab-ci.yml:**
```yaml
stages:
  - review
  - test
  - deploy

claude-review:
  stage: review
  image: node:18
  script:
    - npm install -g @anthropic-ai/claude-code
    - claude login --api-key $ANTHROPIC_API_KEY
    - claude '/fix:types && /test'
  only:
    - merge_requests
```

### Advanced Pipeline

```yaml
variables:
  CLAUDE_MODEL: "claude-sonnet-4-5-20250929"

stages:
  - lint
  - test
  - review
  - deploy

before_script:
  - npm install -g @anthropic-ai/claude-code
  - claude login --api-key $ANTHROPIC_API_KEY

lint:
  stage: lint
  script:
    - claude '/fix:types'
  artifacts:
    paths:
      - src/
    expire_in: 1 hour

test:
  stage: test
  script:
    - npm test || claude '/fix:test analyze failures and fix'
  coverage: '/Coverage: \d+\.\d+%/'

review:
  stage: review
  script:
    - |
      claude "Review this merge request:
      - Check code quality
      - Verify tests
      - Review security
      - Assess performance" > review.md
  artifacts:
    reports:
      codequality: review.md
  only:
    - merge_requests

deploy:
  stage: deploy
  script:
    - claude '/deploy-check'
    - ./deploy.sh
  only:
    - main
```

### Automated Fixes

```yaml
fix-on-failure:
  stage: test
  script:
    - npm test
  retry:
    max: 2
    when:
      - script_failure
  after_script:
    - |
      if [ $CI_JOB_STATUS == 'failed' ]; then
        claude '/fix:test analyze CI logs and fix issues'
        git add .
        git commit -m "fix: auto-fix from CI"
        git push origin HEAD:$CI_COMMIT_REF_NAME
      fi
```

## Common Patterns

### PR Comment Bot

Post Claude reviews as PR comments:

```yaml
# GitHub Actions
- name: Comment PR
  uses: actions/github-script@v6
  with:
    script: |
      const review = process.env.CLAUDE_REVIEW
      github.rest.pulls.createReview({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: context.issue.number,
        body: review,
        event: 'COMMENT'
      })
```

### Conditional Execution

Run Claude only on certain conditions:

```yaml
# Run on large PRs only
- name: Review Large PRs
  if: ${{ github.event.pull_request.changed_files > 10 }}
  uses: anthropic/claude-code-action@v1
  with:
    command: '/review:codebase analyze changes'
```

### Cost Control

Limit CI usage to control costs:

```yaml
# Skip for draft PRs
- name: Claude Review
  if: ${{ !github.event.pull_request.draft }}
  uses: anthropic/claude-code-action@v1

# Run only on specific branches
- name: Claude Check
  if: startsWith(github.ref, 'refs/heads/release/')
  uses: anthropic/claude-code-action@v1
```

## Security Best Practices

### API Key Management

**GitHub:**
```
Settings → Secrets and variables → Actions
Add: ANTHROPIC_API_KEY
```

**GitLab:**
```
Settings → CI/CD → Variables
Add: ANTHROPIC_API_KEY (Protected, Masked)
```

### Restricted Permissions

**GitHub Actions:**
```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

**GitLab CI:**
```yaml
variables:
  GIT_STRATEGY: clone
  GIT_DEPTH: 1
```

### Secrets Scanning

Prevent API key exposure:

```yaml
- name: Scan for Secrets
  run: |
    if git diff | grep -i "ANTHROPIC_API_KEY"; then
      echo "API key detected in diff!"
      exit 1
    fi
```

## Monitoring & Debugging

### Workflow Logs

**GitHub Actions:**
```yaml
- name: Debug Info
  run: |
    echo "Workflow: ${{ github.workflow }}"
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
```

**GitLab CI:**
```yaml
debug:
  script:
    - echo "Pipeline ID: $CI_PIPELINE_ID"
    - echo "Job ID: $CI_JOB_ID"
    - echo "Branch: $CI_COMMIT_BRANCH"
```

### Artifacts

Save Claude outputs:

```yaml
# GitHub
- name: Save Claude Output
  uses: actions/upload-artifact@v3
  with:
    name: claude-results
    path: claude-output.md

# GitLab
artifacts:
  paths:
    - claude-output.md
  expire_in: 1 week
```

### Error Handling

```yaml
- name: Claude Task
  continue-on-error: true
  id: claude
  uses: anthropic/claude-code-action@v1

- name: Handle Failure
  if: steps.claude.outcome == 'failure'
  run: |
    echo "Claude task failed, continuing anyway"
```

## Performance Optimization

### Caching

**GitHub Actions:**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.claude/cache
    key: claude-cache-${{ hashFiles('package-lock.json') }}
```

**GitLab CI:**
```yaml
cache:
  key: claude-cache
  paths:
    - .claude/cache
```

### Parallel Execution

```yaml
# GitHub - Matrix builds
strategy:
  matrix:
    task: [lint, test, review]
steps:
  - run: claude "/${{ matrix.task }}"

# GitLab - Parallel jobs
test:
  parallel: 3
  script:
    - claude "/test --shard $CI_NODE_INDEX/$CI_NODE_TOTAL"
```

## See Also

- GitHub Actions docs: https://docs.github.com/actions
- GitLab CI/CD docs: https://docs.gitlab.com/ee/ci/
- Claude Code Actions: https://github.com/anthropics/claude-code-action
- Best practices: `references/best-practices.md`
