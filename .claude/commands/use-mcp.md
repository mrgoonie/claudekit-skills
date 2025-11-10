---
description: Utilize tools of Model Context Protocol (MCP) servers
argument-hint: [task]
---
**ONLY** use `mcp-manager` subagent to discover and execute tools.
If the subagent got issues with the scripts of `mcp-management` skill, use `mcp-builder` skill to fix them.
**DO NOT** create ANY new scripts.
the subagent can only use MCP tools if any to achieve this task.
If the subagent can't find any suitable tools, just report it back to the main agent to move on to the next step.