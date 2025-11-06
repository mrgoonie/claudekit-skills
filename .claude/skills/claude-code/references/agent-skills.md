# Agent Skills

Create, manage, and share Skills to extend Claude's capabilities in Claude Code.

## What Are Agent Skills?

Agent Skills are modular capabilities that extend Claude's functionality. Each Skill packages:
- Instructions and procedural knowledge
- Metadata (name, description)
- Optional resources (scripts, templates, references)

Skills are automatically discovered and used by Claude when relevant to the task.

## Skill Structure

### Basic Structure
```
.claude/skills/
└── my-skill/
    ├── skill.md       # Instructions (required)
    └── skill.json     # Metadata (required)
```

### With Resources
```
.claude/skills/
└── my-skill/
    ├── skill.md
    ├── skill.json
    ├── scripts/       # Executable code
    ├── references/    # Documentation
    └── assets/        # Templates, images
```

## Creating Skills

### skill.json
Metadata and configuration:

```json
{
  "name": "my-skill",
  "description": "Brief description of when to use this skill",
  "version": "1.0.0",
  "author": "Your Name"
}
```

**Key fields:**
- `name`: Unique identifier (kebab-case)
- `description`: When Claude should activate this skill
- `version`: Semantic version
- `author`: Creator name or org

### skill.md
Main instructions for Claude:

```markdown
# Skill Name

Description of what this skill does.

## When to Use This Skill

Specific scenarios when Claude should activate this skill.

## Instructions

Step-by-step instructions for Claude to follow.

## Examples

Concrete examples of skill usage.
```

## Best Practices

### Clear Activation Criteria
Define exactly when the skill should be used:

**Good:**
```
Use when creating React components with TypeScript and Tailwind CSS.
```

**Bad:**
```
Use for frontend development.
```

### Concise Instructions
Focus on essential information, avoid duplication:

**Good:**
```
1. Create component file in src/components/
2. Use TypeScript interfaces for props
3. Apply Tailwind classes for styling
```

**Bad:**
```
First you need to think about creating a component,
then maybe you should consider...
```

### Actionable Guidance
Provide clear steps Claude can follow:

**Good:**
```
Run `npm test` to validate implementation.
```

**Bad:**
```
You might want to test things.
```

### Include Examples
Show concrete input/output examples:

```markdown
## Examples

Input: "Create button component"
Output: Creates src/components/Button.tsx with props interface
```

### Scope Limitation
Keep skills focused on specific domains:

**Good:**
- `api-testing` - Testing REST APIs
- `db-migrations` - Database schema changes

**Bad:**
- `general-development` - Everything

## Resource Types

### Scripts (`scripts/`)
Executable code for deterministic tasks:

```
scripts/
├── format-code.py
├── generate-types.js
└── run-tests.sh
```

**When to use:**
- Repeated code generation
- Deterministic transformations
- External tool integrations

### References (`references/`)
Documentation loaded into context as needed:

```
references/
├── api-docs.md
├── schemas.md
└── workflows.md
```

**When to use:**
- API documentation
- Database schemas
- Domain knowledge
- Detailed workflows

### Assets (`assets/`)
Files used in output:

```
assets/
├── templates/
│   └── component-template.tsx
├── icons/
└── configs/
```

**When to use:**
- Templates
- Boilerplate code
- Images, icons
- Configuration files

## Using Skills via API

### TypeScript Example
```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 4096,
  skills: [
    {
      type: 'custom',
      custom: {
        name: 'document-creator',
        description: 'Creates professional documents',
        instructions: 'Follow corporate style guide...'
      }
    }
  ],
  messages: [{
    role: 'user',
    content: 'Create a project proposal'
  }]
});
```

### Python Example
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    skills=[
        {
            "type": "custom",
            "custom": {
                "name": "code-reviewer",
                "description": "Reviews code for quality and security",
                "instructions": "Check for common issues..."
            }
        }
    ],
    messages=[{
        "role": "user",
        "content": "Review this code"
    }]
)
```

## Skill Discovery

Claude automatically discovers skills:

1. **Global skills**: `~/.claude/skills/`
2. **Project skills**: `.claude/skills/`
3. **Plugin skills**: From installed plugins

Skills are activated when:
- Task matches skill description
- User explicitly invokes skill
- Context suggests skill is relevant

## Managing Skills

### List Skills
```bash
claude skills list
```

### Test Skill
```bash
claude --skill my-skill "test task"
```

### Share Skill
```bash
# Package skill
cd .claude/skills/my-skill
tar -czf my-skill.tar.gz .

# Or create plugin
# See references/hooks-and-plugins.md
```

### Install Skill
```bash
# Manual installation
cd .claude/skills/
tar -xzf my-skill.tar.gz
```

## Example Skills

### API Testing Skill

**skill.json:**
```json
{
  "name": "api-testing",
  "description": "Test REST APIs with automated requests",
  "version": "1.0.0",
  "author": "Team"
}
```

**skill.md:**
```markdown
# API Testing

Test REST APIs with comprehensive validation.

## When to Use

Use when testing API endpoints, validating responses, or
creating API test suites.

## Instructions

1. Read API documentation from references/api-docs.md
2. Use scripts/test-api.py for making requests
3. Validate response status, headers, body
4. Generate test report

## Examples

Request: "Test the /users endpoint"
Actions:
- Read references/api-docs.md for endpoint spec
- Run scripts/test-api.py --endpoint /users
- Validate response matches schema
- Report results
```

### Database Migration Skill

**skill.json:**
```json
{
  "name": "db-migrations",
  "description": "Create and manage database migrations",
  "version": "1.0.0"
}
```

**skill.md:**
```markdown
# Database Migrations

Create safe, reversible database schema changes.

## When to Use

Use when modifying database schema, adding tables,
or changing column definitions.

## Instructions

1. Review current schema in references/schema.md
2. Create migration file in migrations/
3. Include both up and down migrations
4. Test migration on development database
5. Update references/schema.md

## Migration Template

See assets/migration-template.sql for standard format.
```

## Progressive Disclosure

Keep skill.md concise (<200 lines) by:

1. **Core instructions** in skill.md
2. **Detailed docs** in references/
3. **Executable code** in scripts/
4. **Templates** in assets/

Example structure:
```markdown
# My Skill

Brief overview.

## When to Use

Clear activation criteria.

## Instructions

High-level steps that reference:
- references/detailed-workflow.md
- scripts/automation.py
- assets/template.tsx
```

## Troubleshooting

### Skill Not Activating
- Check description specificity
- Verify skill.json format
- Ensure skill.md has clear activation criteria

### Resource Not Found
- Verify file paths in skill.md
- Check directory structure
- Use relative paths from skill root

### Conflicting Skills
- Make descriptions more specific
- Use unique names
- Scope skills narrowly

## See Also

- Skill creation guide: https://docs.claude.com/claude-code/skills
- Best practices: https://docs.claude.com/agents-and-tools/agent-skills/best-practices
- API usage: `references/api-reference.md`
- Plugin system: `references/hooks-and-plugins.md`
