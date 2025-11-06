# Slash Commands Reference

Comprehensive catalog of Claude Code slash commands for development workflows.

## What Are Slash Commands?

Slash commands are user-defined operations that:
- Start with `/` (e.g., `/cook`, `/test`)
- Expand to full prompts when executed
- Accept arguments
- Located in `.claude/commands/`
- Can be project-specific or global

## Development Commands

### /cook [task]
Implement features step by step.

```bash
/cook implement user authentication with JWT
/cook add payment integration with Stripe
```

**When to use**: Feature implementation with iterative development

### /plan [task]
Research, analyze, and create implementation plans.

```bash
/plan implement OAuth2 authentication
/plan migrate from SQLite to PostgreSQL
```

**When to use**: Before starting complex implementations

### /debug [issue]
Debug technical issues and provide solutions.

```bash
/debug the API returns 500 errors intermittently
/debug authentication flow not working
```

**When to use**: Investigating and diagnosing problems

### /test
Run test suite.

```bash
/test
```

**When to use**: Validate implementations, check for regressions

### /refactor [target]
Improve code quality.

```bash
/refactor the authentication module
/refactor for better performance
```

**When to use**: Code quality improvements

## Fix Commands

### /fix:fast [issue]
Quick fixes for small issues.

```bash
/fix:fast the login button is not working
/fix:fast typo in error message
```

**When to use**: Simple, straightforward fixes

### /fix:hard [issue]
Complex issues requiring planning and subagents.

```bash
/fix:hard database connection pooling issues
/fix:hard race condition in payment processing
```

**When to use**: Complex bugs requiring deep investigation

### /fix:types
Fix TypeScript type errors.

```bash
/fix:types
```

**When to use**: TypeScript compilation errors

### /fix:test [issue]
Fix test failures.

```bash
/fix:test the user service tests are failing
/fix:test integration tests timing out
```

**When to use**: Test suite failures

### /fix:ui [issue]
Fix UI issues.

```bash
/fix:ui button alignment on mobile
/fix:ui dark mode colors inconsistent
```

**When to use**: Visual or interaction issues

### /fix:ci [url]
Analyze GitHub Actions logs and fix CI/CD issues.

```bash
/fix:ci https://github.com/owner/repo/actions/runs/123456
```

**When to use**: Build or deployment failures

### /fix:logs [issue]
Analyze logs and fix issues.

```bash
/fix:logs server error logs showing memory leaks
```

**When to use**: Production issues with log evidence

## Documentation Commands

### /docs:init
Create initial documentation structure.

```bash
/docs:init
```

**When to use**: New projects needing documentation

### /docs:update
Update existing documentation based on code changes.

```bash
/docs:update
```

**When to use**: After significant code changes

### /docs:summarize
Summarize codebase and create overview.

```bash
/docs:summarize
```

**When to use**: Generate project summaries

## Git Commands

### /git:cm
Stage all files and create commit.

```bash
/git:cm
```

**When to use**: Commit changes with automatic message

### /git:cp
Stage, commit, and push all code in current branch.

```bash
/git:cp
```

**When to use**: Commit and push in one command

### /git:pr [branch] [from-branch]
Create pull request.

```bash
/git:pr feature-branch main
/git:pr bugfix-auth develop
```

**When to use**: Creating PRs with automatic descriptions

## Planning Commands

### /plan:two [task]
Create implementation plan with 2 alternative approaches.

```bash
/plan:two implement caching layer
```

**When to use**: Need to evaluate multiple approaches

### /plan:ci [url]
Analyze GitHub Actions logs and create fix plan.

```bash
/plan:ci https://github.com/owner/repo/actions/runs/123456
```

**When to use**: CI/CD failure analysis

### /plan:cro [issue]
Create conversion rate optimization plan.

```bash
/plan:cro landing page conversion improvement
```

**When to use**: Marketing/conversion optimization

## Content Commands

### /content:fast [request]
Quick copy writing.

```bash
/content:fast write product description for new feature
```

**When to use**: Fast content generation

### /content:good [request]
High-quality, conversion-focused copy.

```bash
/content:good write landing page hero section
```

**When to use**: Marketing copy requiring polish

### /content:enhance [issue]
Enhance existing content.

```bash
/content:enhance improve clarity of pricing page
```

**When to use**: Improving existing copy

### /content:cro [issue]
Conversion rate optimization for content.

```bash
/content:cro optimize email campaign copy
```

**When to use**: Conversion-focused content improvements

## Design Commands

### /design:fast [task]
Quick design implementation.

```bash
/design:fast create dashboard layout
```

**When to use**: Rapid prototyping

### /design:good [task]
High-quality, polished design.

```bash
/design:good create landing page for SaaS product
```

**When to use**: Production-ready designs

### /design:3d [task]
Create 3D designs with Three.js.

```bash
/design:3d create interactive 3D product viewer
```

**When to use**: 3D visualization needs

### /design:screenshot [path]
Create design based on screenshot.

```bash
/design:screenshot screenshot.png
```

**When to use**: Recreating designs from images

### /design:video [path]
Create design based on video.

```bash
/design:video demo-video.mp4
```

**When to use**: Implementing designs from video demos

## Deployment Commands

### /deploy
Deploy using deployment tool.

```bash
/deploy
```

**When to use**: Production deployments

### /deploy-check
Check deployment readiness.

```bash
/deploy-check
```

**When to use**: Pre-deployment validation

## Integration Commands

### /integrate:polar [tasks]
Implement payment integration with Polar.sh.

```bash
/integrate:polar add subscription payments
```

**When to use**: Polar payment integration

### /integrate:sepay [tasks]
Implement payment integration with SePay.vn.

```bash
/integrate:sepay add Vietnamese payment gateway
```

**When to use**: SePay payment integration

## Other Commands

### /brainstorm [question]
Brainstorm features and ideas.

```bash
/brainstorm how to improve user onboarding
```

**When to use**: Ideation and exploration

### /ask [question]
Answer technical and architectural questions.

```bash
/ask what's the best way to handle websocket connections
```

**When to use**: Technical guidance

### /scout [prompt] [scale]
Scout directories to respond to requests.

```bash
/scout find authentication code
```

**When to use**: Code exploration

### /watzup
Review recent changes and wrap up work.

```bash
/watzup
```

**When to use**: End of session summary

### /bootstrap [requirements]
Bootstrap new project step by step.

```bash
/bootstrap create React app with TypeScript and Tailwind
```

**When to use**: New project setup

### /bootstrap:auto [requirements]
Bootstrap new project automatically.

```bash
/bootstrap:auto create Next.js app
```

**When to use**: Automated project setup

### /journal
Write journal entries for development log.

```bash
/journal
```

**When to use**: Development documentation

### /review:codebase [prompt]
Scan and analyze codebase.

```bash
/review:codebase analyze architecture patterns
```

**When to use**: Codebase analysis

### /skill:create [prompt]
Create new agent skill.

```bash
/skill:create create skill for API testing
```

**When to use**: Extending Claude with custom skills

## Creating Custom Slash Commands

### Command File Structure
```
.claude/commands/
└── my-command.md
```

### Example Command File
```markdown
# File: .claude/commands/my-command.md

Create comprehensive test suite for {{feature}}.

Include:
- Unit tests
- Integration tests
- Edge cases
- Mocking examples
```

### Usage
```bash
/my-command authentication
# Expands to: "Create comprehensive test suite for authentication..."
```

### Best Practices

**Clear prompts**: Write specific, actionable prompts
**Use variables**: `{{variable}}` for dynamic content
**Document usage**: Add comments explaining the command
**Test thoroughly**: Verify commands work as expected

## Command Arguments

### Single Argument
```bash
/cook implement user auth
# Argument: "implement user auth"
```

### Multiple Arguments
```bash
/git:pr feature-branch main
# Arguments: "feature-branch", "main"
```

### Optional Arguments
Some commands work with or without arguments:
```bash
/test              # Run all tests
/test user.test.js # Run specific test
```

## See Also

- Creating custom commands: `references/hooks-and-plugins.md`
- Command automation: `references/configuration.md`
- Best practices: `references/best-practices.md`
