# Best Practices

Guidelines for project organization, security, performance, collaboration, and cost management.

## Project Organization

### Directory Structure

Keep `.claude/` directory in version control:

```
project/
├── .claude/
│   ├── settings.json       # Project settings
│   ├── commands/           # Custom slash commands
│   │   ├── test-all.md
│   │   └── deploy.md
│   ├── skills/            # Project-specific skills
│   │   └── api-testing/
│   ├── hooks.json         # Hooks configuration
│   ├── mcp.json           # MCP servers (no secrets!)
│   └── .env.example       # Environment template
├── .gitignore             # Ignore .claude/.env
└── README.md
```

### Documentation

Document custom extensions:

**README.md:**
```markdown
## Claude Code Setup

### Custom Commands
- `/test-all`: Run full test suite
- `/deploy`: Deploy to staging

### Skills
- `api-testing`: REST API testing utilities

### MCP Servers
- `postgres`: Database access
- `github`: Repository integration

### Environment Variables
Copy `.claude/.env.example` to `.claude/.env` and fill in:
- GITHUB_TOKEN
- DATABASE_URL
```

### Team Sharing

**What to commit:**
- `.claude/settings.json`
- `.claude/commands/`
- `.claude/skills/`
- `.claude/hooks.json`
- `.claude/mcp.json` (without secrets)
- `.claude/.env.example`

**What NOT to commit:**
- `.claude/.env` (contains secrets)
- `.claude/memory/` (optional)
- `.claude/cache/`
- API keys or tokens

**.gitignore:**
```
.claude/.env
.claude/memory/
.claude/cache/
.claude/logs/
```

## Security

### API Key Management

**Never commit API keys:**
```bash
# Use environment variables
export ANTHROPIC_API_KEY=sk-ant-xxxxx

# Or .env file (gitignored)
echo 'ANTHROPIC_API_KEY=sk-ant-xxxxx' > .claude/.env
```

**Rotate keys regularly:**
```bash
# Generate new key
# Update in all environments
# Revoke old key
```

**Use workspace keys:**
```bash
# For team projects, use workspace API keys
# Easier to manage and rotate
# Better access control
```

### Sandboxing

Enable sandboxing in production:

```json
{
  "sandboxing": {
    "enabled": true,
    "allowedPaths": ["/workspace"],
    "networkAccess": "restricted",
    "allowedDomains": ["api.company.com"]
  }
}
```

### Hook Security

Review hook scripts before execution:

```bash
# Check hooks.json
cat .claude/hooks.json | jq .

# Review scripts
cat .claude/scripts/hook.sh

# Validate inputs in hooks
#!/bin/bash
if [[ ! "$TOOL_ARGS" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "Invalid input"
  exit 1
fi
```

### Plugin Security

Audit plugins before installation:

```bash
# Review plugin source
gh repo view username/plugin

# Check plugin.json
tar -xzf plugin.tar.gz
cat plugin.json

# Install from trusted sources only
claude plugin install gh:anthropics/official-plugin
```

## Performance Optimization

### Model Selection

Choose appropriate model for task:

**Haiku** - Fast, cost-effective:
```bash
claude --model haiku "fix typo in README"
claude --model haiku "format code"
```

**Sonnet** - Balanced (default):
```bash
claude "implement user authentication"
claude "review this PR"
```

**Opus** - Complex tasks:
```bash
claude --model opus "architect microservices system"
claude --model opus "optimize algorithm performance"
```

### Prompt Caching

Cache repeated context:

```typescript
// Cache large codebase
const response = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  system: [
    {
      type: 'text',
      text: largeCodebase,
      cache_control: { type: 'ephemeral' }
    }
  ],
  messages: [...]
});
```

**Benefits:**
- 90% cost reduction on cached tokens
- Faster responses
- Better for iterative development

### Rate Limiting

Implement rate limiting in hooks:

```bash
#!/bin/bash
# .claude/scripts/rate-limit.sh

REQUESTS_FILE=".claude/requests.log"
MAX_REQUESTS=100
WINDOW=3600  # 1 hour

# Count recent requests
RECENT=$(find $REQUESTS_FILE -mmin -60 | wc -l)

if [ $RECENT -ge $MAX_REQUESTS ]; then
  echo "Rate limit exceeded"
  exit 1
fi

echo $(date) >> $REQUESTS_FILE
```

### Token Management

Monitor token usage:

```bash
# Check usage
claude usage show

# Set limits
claude config set maxTokens 8192

# Track costs
claude analytics cost --group-by project
```

## Team Collaboration

### Standardize Commands

Create consistent slash commands:

```markdown
# .claude/commands/test.md
Run test suite with coverage report.

Options:
- {{suite}}: Specific test suite (optional)
```

**Usage:**
```bash
/test
/test unit
/test integration
```

### Share Skills

Create team skills via plugins:

```bash
# Create team plugin
cd .claude/plugins/team-plugin
cat > plugin.json <<EOF
{
  "name": "team-plugin",
  "skills": ["skills/*/"],
  "commands": ["commands/*.md"]
}
EOF

# Package and share
tar -czf team-plugin.tar.gz .
```

### Consistent Settings

Use project settings for consistency:

**.claude/settings.json:**
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "maxTokens": 8192,
  "outputStyle": "technical-writer",
  "thinking": {
    "enabled": true,
    "budget": 10000
  }
}
```

### Memory Settings

Use project memory for shared context:

```json
{
  "memory": {
    "enabled": true,
    "location": "project"
  }
}
```

**Benefits:**
- Shared project knowledge
- Consistent behavior across team
- Reduced onboarding time

## Cost Management

### Budget Limits

Set budget limits in hooks:

```bash
#!/bin/bash
# .claude/scripts/budget-check.sh

MONTHLY_BUDGET=1000
CURRENT_SPEND=$(claude analytics cost --format json | jq '.total')

if (( $(echo "$CURRENT_SPEND > $MONTHLY_BUDGET" | bc -l) )); then
  echo "⚠️  Monthly budget exceeded: \$$CURRENT_SPEND / \$$MONTHLY_BUDGET"
  exit 1
fi
```

### Usage Monitoring

Monitor via analytics API:

```bash
# Daily usage report
claude analytics usage --start $(date -d '1 day ago' +%Y-%m-%d)

# Cost by user
claude analytics cost --group-by user

# Export to CSV
claude analytics export --format csv > usage.csv
```

### Cost Optimization

**Use Haiku for simple tasks:**
```bash
# Expensive (Sonnet)
claude "fix typo in README"

# Cheap (Haiku)
claude --model haiku "fix typo in README"
```

**Enable caching:**
```json
{
  "caching": {
    "enabled": true,
    "ttl": 300
  }
}
```

**Batch operations:**
```bash
# Instead of multiple requests
claude "fix file1.js"
claude "fix file2.js"
claude "fix file3.js"

# Batch them
claude "fix all files: file1.js file2.js file3.js"
```

**Track per-project costs:**
```bash
# Tag projects
claude --project my-project "implement feature"

# View project costs
claude analytics cost --project my-project
```

## Development Workflows

### Feature Development

```bash
# 1. Plan feature
claude /plan "implement user authentication"

# 2. Create checkpoint
claude checkpoint create "before auth implementation"

# 3. Implement
claude /cook "implement user authentication"

# 4. Test
claude /test

# 5. Review
claude "review authentication implementation"

# 6. Commit
claude /git:cm
```

### Bug Fixing

```bash
# 1. Debug
claude /debug "login button not working"

# 2. Fix
claude /fix:fast "fix login button issue"

# 3. Test
claude /test

# 4. Commit
claude /git:cm
```

### Code Review

```bash
# Review PR
claude "review PR #123"

# Check security
claude "review for security vulnerabilities"

# Verify tests
claude "check test coverage"
```

## See Also

- Security guide: https://docs.claude.com/claude-code/security
- Cost tracking: https://docs.claude.com/claude-code/costs
- Team setup: https://docs.claude.com/claude-code/overview
- API usage: `references/api-reference.md`
