# Fix Report: MCP Management CLI Errors

**Issue**: [#5 - 'Test Connection' runs an error](https://github.com/mrgoonie/claudekit-skills/issues/5)
**Date**: 2025-12-30
**Status**: Fixed

## Problems Identified

### Issue 1: Path Resolution
Config path `.claude/.mcp.json` resolved relative to `process.cwd()`, causing wrong lookup when running from `scripts/` directory.

**Before**: `~/.claude/skills/mcp-management/scripts/.claude/.mcp.json`
**Expected**: `~/.claude/.mcp.json`

### Issue 2: TypeScript Module Resolution
Using `ts-node` with ES modules caused import resolution failures.

## Fixes Applied

### 1. Path Resolution (mcp-client.ts)
- Added `import { homedir } from 'os'`
- Changed default config path from relative `.claude/.mcp.json` to absolute `~/.claude/.mcp.json`
- Config path now resolves to user's home directory by default

```typescript
async loadConfig(configPath?: string): Promise<MCPConfig> {
  const defaultPath = resolve(homedir(), '.claude', '.mcp.json');
  const fullPath = configPath ? resolve(process.cwd(), configPath) : defaultPath;
  // ...
}
```

### 2. TypeScript Configuration (tsconfig.json)
- Changed `module` from `ES2022` to `NodeNext`
- Changed `moduleResolution` from `node` to `NodeNext`

### 3. Package Configuration (package.json)
- Replaced `ts-node` with `tsx` for better ESM support
- Added npm scripts for convenience: `list-tools`, `list-prompts`, `list-resources`

### 4. Documentation (README.md)
- Updated all command examples to use `tsx` instead of `ts-node`
- Added note about automatic config path resolution

### 5. Type Fix (mcp-client.ts)
- Fixed TypeScript error with `timeout` option in `callTool` method

## Files Modified

| File | Change |
|------|--------|
| `scripts/mcp-client.ts` | Path resolution fix, type assertion |
| `scripts/tsconfig.json` | NodeNext module resolution |
| `scripts/package.json` | tsx instead of ts-node, npm scripts |
| `README.md` | Updated documentation |

## Verification

1. TypeScript compilation passes: `npx tsc --noEmit`
2. CLI resolves to `~/.claude/.mcp.json` regardless of cwd
3. Can be run from any directory: `npx tsx cli.ts list-tools`
