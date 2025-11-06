# Sequential Thinking Skill

Agent skill for systematic problem-solving through iterative reasoning with revision and branching capabilities.

## What This Skill Does

Enables Claude to break down complex problems into sequential thought steps, revise conclusions when needed, and explore alternative solution paths—all while maintaining context throughout the reasoning process.

## Installation

This skill requires the Sequential Thinking MCP server to be installed and configured in your Claude Desktop or Claude Code environment.

### Step 1: Install MCP Server

Choose one of the following methods:

#### NPX (Recommended)

Add to your `claude_desktop_config.json` or MCP settings:

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

#### Docker

```json
{
  "mcpServers": {
    "sequentialthinking": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "mcp/sequentialthinking"]
    }
  }
}
```

### Step 2: Add Skill to Project

Copy this skill folder to your project's `.claude/skills/` directory:

```bash
cp -r sequential-thinking /path/to/your/project/.claude/skills/
```

### Step 3: Verify Installation

Restart Claude and check that the `mcp__reasoning__sequentialthinking` tool is available.

## Usage

Once installed, Claude will automatically use this skill when:
- Facing complex multi-step problems
- Needing to revise earlier conclusions
- Exploring alternative solution approaches
- Working through uncertain or evolving scopes

You can also explicitly request it:
```
"Let's think through this step-by-step using sequential thinking"
```

## Configuration

### Disable Logging (Optional)

To suppress thought information logging, set environment variable:

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "env": {
        "DISABLE_THOUGHT_LOGGING": "true"
      }
    }
  }
}
```

## Skill Structure

```
sequential-thinking/
├── SKILL.md              # Main skill definition
├── README.md             # This file
└── references/
    ├── advanced.md       # Revision and branching patterns
    └── examples.md       # Real-world use cases
```

## When Claude Uses This Skill

The skill activates for:
- **Complex analysis**: Breaking down multi-faceted problems
- **Design decisions**: Exploring and comparing alternatives
- **Debugging**: Systematic investigation with course correction
- **Planning**: Multi-stage project planning with evolving scope
- **Architecture**: Evaluating trade-offs across approaches

## Learn More

- [MCP Sequential Thinking Server](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview.md)

## License

MIT
