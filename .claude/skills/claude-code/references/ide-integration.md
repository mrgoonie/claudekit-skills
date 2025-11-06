# IDE Integration

Use Claude Code with Visual Studio Code and JetBrains IDEs.

## Visual Studio Code

### Installation

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Claude Code"
4. Click Install
5. Authenticate with API key

### Features

**Inline Chat**
- Press Ctrl+I (Cmd+I on Mac)
- Ask questions about code
- Get suggestions in context
- Apply changes directly

**Code Actions**
- Right-click on code
- Select "Ask Claude"
- Get refactoring suggestions
- Fix bugs and issues

**Diff View**
- See proposed changes
- Accept/reject modifications
- Review before applying
- Staged diff comparison

**Terminal Integration**
- Built-in Claude terminal
- Run commands via Claude
- Execute tools directly
- View real-time output

### Configuration

**.vscode/settings.json:**
```json
{
  "claude.apiKey": "${ANTHROPIC_API_KEY}",
  "claude.model": "claude-sonnet-4-5-20250929",
  "claude.maxTokens": 8192,
  "claude.autoSave": true,
  "claude.inlineChat.enabled": true,
  "claude.terminalIntegration": true
}
```

### Keyboard Shortcuts

**Default shortcuts:**
- `Ctrl+I`: Inline chat
- `Ctrl+Shift+C`: Open Claude panel
- `Ctrl+Shift+Enter`: Submit to Claude
- `Escape`: Close Claude chat

**Custom shortcuts (.vscode/keybindings.json):**
```json
[
  {
    "key": "ctrl+alt+c",
    "command": "claude.openChat"
  },
  {
    "key": "ctrl+alt+r",
    "command": "claude.refactor"
  }
]
```

### Workspace Integration

**Project-specific Claude settings:**

.vscode/claude.json:
```json
{
  "skills": [".claude/skills/project-skill"],
  "commands": [".claude/commands"],
  "mcpServers": ".claude/mcp.json",
  "outputStyle": "technical-writer"
}
```

### Common Workflows

**Explain Code:**
1. Select code
2. Right-click → "Ask Claude"
3. Type: "Explain this code"

**Refactor:**
1. Select function
2. Press Ctrl+I
3. Type: "Refactor for better performance"

**Fix Bug:**
1. Click on error
2. Press Ctrl+I
3. Type: "Fix this error"

**Generate Tests:**
1. Select function
2. Right-click → "Ask Claude"
3. Type: "Write tests for this"

## JetBrains IDEs

Supported IDEs:
- IntelliJ IDEA
- PyCharm
- WebStorm
- PhpStorm
- GoLand
- RubyMine
- CLion
- Rider

### Installation

1. Open Settings (Ctrl+Alt+S)
2. Go to Plugins
3. Search "Claude Code"
4. Click Install
5. Restart IDE
6. Authenticate with API key

### Features

**AI Assistant Panel**
- Dedicated Claude panel
- Context-aware suggestions
- Multi-file awareness
- Project understanding

**Inline Suggestions**
- As-you-type completions
- Contextual code generation
- Smart refactoring hints
- Error fix suggestions

**Code Reviews**
- Automated code reviews
- Security vulnerability detection
- Best practice recommendations
- Performance optimization tips

**Refactoring Support**
- Smart rename
- Extract method
- Inline variable
- Move class

### Configuration

**Settings → Tools → Claude Code:**
```
API Key: [Your API Key]
Model: claude-sonnet-4-5-20250929
Max Tokens: 8192
Auto-complete: Enabled
Code Review: Enabled
```

**Project Settings (.idea/claude.xml):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ClaudeSettings">
    <option name="model" value="claude-sonnet-4-5-20250929" />
    <option name="skillsPath" value=".claude/skills" />
    <option name="autoReview" value="true" />
  </component>
</project>
```

### Keyboard Shortcuts

**Default shortcuts:**
- `Ctrl+Shift+A`: Ask Claude
- `Alt+Enter`: Quick fixes with Claude
- `Ctrl+Alt+L`: Format with Claude suggestions

**Custom shortcuts (Settings → Keymap → Claude Code):**
```
Ask Claude: Ctrl+Shift+C
Refactor with Claude: Ctrl+Alt+R
Generate Tests: Ctrl+Alt+T
Code Review: Ctrl+Alt+V
```

### Integration with IDE Features

**Version Control:**
- Review commit diffs with Claude
- Generate commit messages
- Suggest PR improvements
- Analyze merge conflicts

**Debugger:**
- Explain stack traces
- Suggest fixes for errors
- Debug complex issues
- Analyze variable states

**Database Tools:**
- Generate SQL queries
- Optimize database schema
- Write migration scripts
- Explain query plans

### Common Workflows

**Generate Boilerplate:**
1. Right-click in editor
2. Select "Generate" → "Claude Code"
3. Choose template type

**Review Changes:**
1. Open Version Control panel
2. Right-click on changeset
3. Select "Review with Claude"

**Debug Error:**
1. Hit breakpoint
2. Right-click in debugger
3. Select "Ask Claude about this"

## CLI Integration

Use Claude Code from IDE terminal:

```bash
# In VS Code terminal
claude "explain this project structure"

# In JetBrains terminal
claude "add error handling to current file"
```

## Best Practices

### VS Code

**Workspace Organization:**
- Use workspace settings for team consistency
- Share .vscode/claude.json in version control
- Document custom shortcuts
- Configure output styles per project

**Performance:**
- Limit inline suggestions in large files
- Disable auto-save for better control
- Use specific prompts
- Close unused editor tabs

### JetBrains

**Project Configuration:**
- Enable Claude for specific file types only
- Configure inspection severity
- Set up custom code review templates
- Use project-specific skills

**Performance:**
- Adjust auto-complete delay
- Limit scope of code analysis
- Disable for binary files
- Configure memory settings

## Troubleshooting

### VS Code

**Extension Not Loading:**
```bash
# Check extension status
code --list-extensions | grep claude

# Reinstall
code --uninstall-extension anthropic.claude-code
code --install-extension anthropic.claude-code
```

**Authentication Issues:**
- Verify API key in settings
- Check environment variable
- Re-authenticate in extension
- Review proxy settings

### JetBrains

**Plugin Not Responding:**
```
File → Invalidate Caches / Restart
Settings → Plugins → Claude Code → Reinstall
```

**Performance Issues:**
- Increase IDE memory (Help → Edit Custom VM Options)
- Disable unused features
- Clear caches
- Update plugin version

## See Also

- VS Code extension: https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code
- JetBrains plugin: https://plugins.jetbrains.com/plugin/claude-code
- Configuration: `references/configuration.md`
- Troubleshooting: `references/troubleshooting.md`
