#!/usr/bin/env node
/**
 * MCP Management CLI - Command-line interface for MCP operations
 */

import { MCPClientManager } from './mcp-client.js';
import { writeFileSync, mkdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  const manager = new MCPClientManager();

  try {
    // Load config
    await manager.loadConfig();
    console.log('✓ Config loaded');

    // Connect to all servers
    await manager.connectAll();
    console.log('✓ Connected to all MCP servers\n');

    switch (command) {
      case 'list-tools':
        await listTools(manager);
        break;

      case 'list-prompts':
        await listPrompts(manager);
        break;

      case 'list-resources':
        await listResources(manager);
        break;

      case 'call-tool':
        await callTool(manager, args[1], args[2], args[3]);
        break;

      default:
        printUsage();
    }

    await manager.cleanup();
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

async function listTools(manager: MCPClientManager) {
  const tools = await manager.getAllTools();
  console.log(`Found ${tools.length} tools:\n`);

  for (const tool of tools) {
    console.log(`📦 ${tool.serverName} / ${tool.name}`);
    console.log(`   ${tool.description}`);
    if (tool.inputSchema?.properties) {
      console.log(`   Parameters: ${Object.keys(tool.inputSchema.properties).join(', ')}`);
    }
    console.log('');
  }

  // Save tools to JSON file
  const assetsDir = join(__dirname, '..', 'assets');
  const toolsPath = join(assetsDir, 'tools.json');

  try {
    mkdirSync(assetsDir, { recursive: true });
    writeFileSync(toolsPath, JSON.stringify(tools, null, 2));
    console.log(`\n✓ Tools saved to ${toolsPath}`);
  } catch (error) {
    console.error(`\n✗ Failed to save tools: ${error}`);
  }
}

async function listPrompts(manager: MCPClientManager) {
  const prompts = await manager.getAllPrompts();
  console.log(`Found ${prompts.length} prompts:\n`);

  for (const prompt of prompts) {
    console.log(`💬 ${prompt.serverName} / ${prompt.name}`);
    console.log(`   ${prompt.description}`);
    if (prompt.arguments && prompt.arguments.length > 0) {
      console.log(`   Arguments: ${prompt.arguments.map((a: any) => a.name).join(', ')}`);
    }
    console.log('');
  }
}

async function listResources(manager: MCPClientManager) {
  const resources = await manager.getAllResources();
  console.log(`Found ${resources.length} resources:\n`);

  for (const resource of resources) {
    console.log(`📄 ${resource.serverName} / ${resource.name}`);
    console.log(`   URI: ${resource.uri}`);
    if (resource.description) {
      console.log(`   ${resource.description}`);
    }
    if (resource.mimeType) {
      console.log(`   Type: ${resource.mimeType}`);
    }
    console.log('');
  }
}

async function callTool(
  manager: MCPClientManager,
  serverName: string,
  toolName: string,
  argsJson: string
) {
  if (!serverName || !toolName || !argsJson) {
    console.error('Usage: cli.ts call-tool <server> <tool> <json-args>');
    process.exit(1);
  }

  const args = JSON.parse(argsJson);
  console.log(`Calling ${serverName}/${toolName}...`);

  const result = await manager.callTool(serverName, toolName, args);
  console.log('\nResult:');
  console.log(JSON.stringify(result, null, 2));
}

function printUsage() {
  console.log(`
MCP Management CLI

Usage:
  cli.ts <command> [options]

Commands:
  list-tools                        List all tools and save to assets/tools.json
  list-prompts                      List all prompts from all MCP servers
  list-resources                    List all resources from all MCP servers
  call-tool <server> <tool> <json>  Call a specific tool

Examples:
  cli.ts list-tools
  cli.ts call-tool memory create_entities '{"entities":[{"name":"Alice","entityType":"person"}]}'
  cli.ts call-tool human-mcp playwright_screenshot_fullpage '{"url":"https://example.com"}'

Note: Tool analysis is done by the LLM reading assets/tools.json directly.
  `);
}

main();
