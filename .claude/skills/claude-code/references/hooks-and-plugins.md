# Hooks and Plugins

Customize and extend Claude Code behavior with hooks and plugins.

## Hooks System

Hooks are shell commands that execute in response to events.

### Hook Types

**Pre-tool hooks**: Execute before tool calls
**Post-tool hooks**: Execute after tool calls
**User prompt submit hooks**: Execute when user submits prompts

### Configuration

Hooks are configured in `.claude/hooks.json`:

```json
{
  "hooks": {
    "pre-tool": {
      "bash": "echo 'Running: $TOOL_ARGS'",
      "write": "./scripts/validate-write.sh"
    },
    "post-tool": {
      "write": "./scripts/format-code.sh",
      "edit": "prettier --write $FILE_PATH"
    },
    "user-prompt-submit": "./scripts/validate-request.sh"
  }
}
```

### Environment Variables

Available in hook scripts:

**All hooks:**
- `$TOOL_NAME`: Name of the tool being called
- `$TOOL_ARGS`: JSON string of tool arguments

**Post-tool only:**
- `$TOOL_RESULT`: Tool execution result

**User-prompt-submit only:**
- `$USER_PROMPT`: User's prompt text

### Hook Examples

#### Pre-tool: Security Validation
```bash
#!/bin/bash
# .claude/scripts/validate-bash.sh

# Block dangerous commands
if echo "$TOOL_ARGS" | grep -E "rm -rf /|format|mkfs"; then
  echo "❌ Dangerous command blocked"
  exit 1
fi

echo "✓ Command validated"
```

**Configuration:**
```json
{
  "hooks": {
    "pre-tool": {
      "bash": "./.claude/scripts/validate-bash.sh"
    }
  }
}
```

#### Post-tool: Auto-format
```bash
#!/bin/bash
# .claude/scripts/format-code.sh

# Extract file path from tool args
FILE_PATH=$(echo "$TOOL_ARGS" | jq -r '.file_path')

# Format based on file type
case "$FILE_PATH" in
  *.js|*.ts|*.jsx|*.tsx)
    prettier --write "$FILE_PATH"
    ;;
  *.py)
    black "$FILE_PATH"
    ;;
  *.go)
    gofmt -w "$FILE_PATH"
    ;;
esac
```

**Configuration:**
```json
{
  "hooks": {
    "post-tool": {
      "write": "./.claude/scripts/format-code.sh",
      "edit": "./.claude/scripts/format-code.sh"
    }
  }
}
```

#### User-prompt-submit: Cost Tracking
```bash
#!/bin/bash
# .claude/scripts/track-usage.sh

# Log prompt
echo "$(date): $USER_PROMPT" >> .claude/usage.log

# Estimate tokens (rough)
TOKEN_COUNT=$(echo "$USER_PROMPT" | wc -w)
echo "Estimated tokens: $TOKEN_COUNT"
```

**Configuration:**
```json
{
  "hooks": {
    "user-prompt-submit": "./.claude/scripts/track-usage.sh"
  }
}
```

### Hook Best Practices

**Performance**: Keep hooks fast (<100ms)
**Reliability**: Handle errors gracefully
**Security**: Validate all inputs
**Logging**: Log important actions
**Testing**: Test hooks thoroughly

### Hook Errors

When a hook fails:
- Pre-tool hook failure blocks tool execution
- Post-tool hook failure is logged but doesn't block
- User can configure strict mode to block on all failures

## Plugins System

Plugins are packaged collections of extensions.

### Plugin Structure

```
my-plugin/
├── plugin.json          # Plugin metadata
├── commands/            # Slash commands
│   ├── my-command.md
│   └── another-command.md
├── skills/             # Agent skills
│   └── my-skill/
│       ├── skill.md
│       └── skill.json
├── hooks/              # Hook scripts
│   ├── hooks.json
│   └── scripts/
├── mcp/                # MCP server configurations
│   └── mcp.json
└── README.md           # Documentation
```

### plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": "Your Name",
  "homepage": "https://github.com/user/plugin",
  "license": "MIT",
  "commands": ["commands/*.md"],
  "skills": ["skills/*/"],
  "hooks": "hooks/hooks.json",
  "mcpServers": "mcp/mcp.json",
  "dependencies": {
    "node": ">=18.0.0"
  }
}
```

### Installing Plugins

#### From GitHub
```bash
claude plugin install gh:username/repo
claude plugin install gh:username/repo@v1.0.0
```

#### From npm
```bash
claude plugin install npm:package-name
claude plugin install npm:@scope/package-name
```

#### From Local Path
```bash
claude plugin install ./path/to/plugin
claude plugin install ~/plugins/my-plugin
```

#### From URL
```bash
claude plugin install https://example.com/plugin.zip
```

### Managing Plugins

#### List Installed Plugins
```bash
claude plugin list
```

#### Update Plugin
```bash
claude plugin update my-plugin
claude plugin update --all
```

#### Uninstall Plugin
```bash
claude plugin uninstall my-plugin
```

#### Enable/Disable Plugin
```bash
claude plugin disable my-plugin
claude plugin enable my-plugin
```

### Creating Plugins

#### Initialize Plugin
```bash
mkdir my-plugin
cd my-plugin
```

#### Create plugin.json
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My awesome plugin",
  "author": "Your Name",
  "commands": ["commands/*.md"],
  "skills": ["skills/*/"]
}
```

#### Add Components
```bash
# Add slash command
mkdir -p commands
cat > commands/my-command.md <<EOF
# My Command
Do something awesome with {{input}}.
EOF

# Add skill
mkdir -p skills/my-skill
cat > skills/my-skill/skill.json <<EOF
{
  "name": "my-skill",
  "description": "Does something",
  "version": "1.0.0"
}
EOF
```

#### Package Plugin
```bash
# Create archive
tar -czf my-plugin.tar.gz .

# Or zip
zip -r my-plugin.zip .
```

### Publishing Plugins

#### To GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git tag v1.0.0
git push origin main --tags
```

#### To npm
```bash
npm init
npm publish
```

### Plugin Marketplaces

Organizations can create private plugin marketplaces.

#### Configure Marketplace
```json
{
  "marketplaces": [
    {
      "name": "company-internal",
      "url": "https://plugins.company.com/catalog.json",
      "auth": {
        "type": "bearer",
        "token": "${COMPANY_PLUGIN_TOKEN}"
      }
    }
  ]
}
```

#### Marketplace Catalog Format
```json
{
  "plugins": [
    {
      "name": "company-plugin",
      "version": "1.0.0",
      "description": "Internal plugin",
      "downloadUrl": "https://plugins.company.com/company-plugin-1.0.0.zip",
      "checksum": "sha256:abc123..."
    }
  ]
}
```

#### Install from Marketplace
```bash
claude plugin install company-internal:company-plugin
```

## Example Plugin: Code Quality

### Structure
```
code-quality-plugin/
├── plugin.json
├── commands/
│   ├── lint.md
│   └── format.md
├── skills/
│   └── code-review/
│       ├── skill.md
│       └── skill.json
└── hooks/
    ├── hooks.json
    └── scripts/
        └── auto-lint.sh
```

### plugin.json
```json
{
  "name": "code-quality",
  "version": "1.0.0",
  "description": "Code quality tools and automation",
  "commands": ["commands/*.md"],
  "skills": ["skills/*/"],
  "hooks": "hooks/hooks.json"
}
```

### commands/lint.md
```markdown
# Lint

Run linter on {{files}} and fix all issues automatically.
```

### hooks/hooks.json
```json
{
  "hooks": {
    "post-tool": {
      "write": "./scripts/auto-lint.sh"
    }
  }
}
```

## Security Considerations

### Hook Security
- Validate all inputs
- Use whitelists for allowed commands
- Implement timeouts
- Log all executions
- Review hook scripts regularly

### Plugin Security
- Verify plugin sources
- Review code before installation
- Use signed packages when available
- Monitor plugin behavior
- Keep plugins updated

### Best Practices
- Install plugins from trusted sources only
- Review plugin permissions
- Use plugin sandboxing when available
- Monitor resource usage
- Regular security audits

## Troubleshooting

### Hooks Not Running
- Check hooks.json syntax
- Verify script permissions (`chmod +x`)
- Check script paths
- Review logs in `.claude/logs/`

### Plugin Installation Failures
- Verify internet connectivity
- Check plugin URL/path
- Review error messages
- Clear cache: `claude plugin cache clear`

### Plugin Conflicts
- Check for conflicting commands
- Review plugin load order
- Disable conflicting plugins
- Update plugins to compatible versions

## See Also

- Creating slash commands: `references/slash-commands.md`
- Agent skills: `references/agent-skills.md`
- Configuration: `references/configuration.md`
- Best practices: `references/best-practices.md`
