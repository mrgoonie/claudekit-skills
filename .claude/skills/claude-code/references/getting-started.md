# Getting Started with Claude Code

Installation, authentication, and setup guide for Claude Code.

## What is Claude Code?

Claude Code is Anthropic's agentic coding tool that lives in the terminal and helps turn ideas into code faster. Key features:

- **Agentic Capabilities**: Autonomous planning, execution, and validation
- **Terminal Integration**: Works directly in command line
- **IDE Support**: Extensions for VS Code and JetBrains IDEs
- **Extensibility**: Plugins, skills, slash commands, and MCP servers
- **Enterprise Ready**: SSO, sandboxing, monitoring, and compliance features

## Prerequisites

### System Requirements
- **Operating Systems**: macOS, Linux, or Windows (WSL2)
- **Runtime**: Node.js 18+ or Python 3.10+
- **API Key**: From Anthropic Console (console.anthropic.com)

### Getting API Key
1. Go to console.anthropic.com
2. Sign in or create account
3. Navigate to API Keys section
4. Generate new API key
5. Save key securely (cannot be viewed again)

## Installation

### Install via npm (Recommended)
```bash
npm install -g @anthropic-ai/claude-code
```

### Install via pip
```bash
pip install claude-code
```

### Verify Installation
```bash
claude --version
```

## Authentication

### Method 1: Interactive Login
```bash
claude login
# Follow prompts to enter API key
```

### Method 2: Environment Variable
```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY=your_api_key_here

# Or set for single session
export ANTHROPIC_API_KEY=your_api_key_here
claude
```

### Method 3: Configuration File
Create `~/.claude/config.json`:
```json
{
  "apiKey": "your_api_key_here"
}
```

### Verify Authentication
```bash
claude "hello"
# Should respond without authentication errors
```

## First Run

### Start Interactive Session
```bash
# In any directory
claude

# In specific project
cd /path/to/project
claude
```

### Run with Specific Task
```bash
claude "implement user authentication"
```

### Run with File Context
```bash
claude "explain this code" --file app.js
```

## Basic Usage

### Interactive Mode
```bash
$ claude
Claude Code> help me create a React component
# Claude will plan and execute
```

### One-Shot Mode
```bash
claude "add error handling to main.py"
```

### With Additional Context
```bash
claude "refactor this function" --file utils.js --context "make it async"
```

## Understanding the Interface

### Session Start
```
Claude Code v1.x.x
Working directory: /path/to/project
Model: claude-sonnet-4-5-20250929

Claude Code>
```

### Tool Execution
Claude will show:
- Tool being used (Read, Write, Bash, etc.)
- Tool parameters
- Results or outputs
- Thinking/planning process (if enabled)

### Session End
```bash
# Type Ctrl+C or Ctrl+D
# Or type 'exit' or 'quit'
```

## Common First Commands

### Explore Codebase
```bash
claude "explain the project structure"
```

### Run Tests
```bash
claude "run the test suite"
```

### Fix Issues
```bash
claude "fix all TypeScript errors"
```

### Add Feature
```bash
claude "add input validation to the login form"
```

## Directory Structure

Claude Code creates `.claude/` in your project:

```
project/
├── .claude/
│   ├── settings.json      # Project-specific settings
│   ├── commands/          # Custom slash commands
│   ├── skills/            # Custom skills
│   ├── hooks.json         # Hook configurations
│   └── mcp.json           # MCP server configurations
└── ...
```

## Next Steps

### Learn Slash Commands
```bash
# See available commands
/help

# Try common workflows
/cook implement feature X
/fix:fast bug in Y
/test
```

### Create Custom Skills
See `references/agent-skills.md` for creating project-specific skills.

### Configure MCP Servers
See `references/mcp-integration.md` for connecting external tools.

### Set Up Hooks
See `references/hooks-and-plugins.md` for automation.

### Configure Settings
See `references/configuration.md` for customization options.

## Quick Troubleshooting

### Authentication Issues
```bash
# Re-login
claude logout
claude login

# Verify API key is set
echo $ANTHROPIC_API_KEY
```

### Permission Errors
```bash
# Check file permissions
ls -la ~/.claude

# Fix ownership
sudo chown -R $USER ~/.claude
```

### Installation Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code
```

### WSL2 Issues (Windows)
```bash
# Ensure WSL2 is updated
wsl --update

# Check Node.js version in WSL
node --version  # Should be 18+
```

## Getting Help

- **Documentation**: https://docs.claude.com/claude-code
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Support**: support.claude.com
- **Community**: discord.gg/anthropic

For detailed troubleshooting, see `references/troubleshooting.md`.
