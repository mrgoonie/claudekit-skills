#!/usr/bin/env node
/**
 * MCP Management CLI - Command-line interface for MCP operations
 */
import { MCPClientManager } from './mcp-client.js';
import { analyzeToolsForTask } from './analyze-tools.js';
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
            case 'analyze':
                await analyzeForTask(manager, args.slice(1).join(' '));
                break;
            case 'call-tool':
                await callTool(manager, args[1], args[2], args[3]);
                break;
            default:
                printUsage();
        }
        await manager.cleanup();
    }
    catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}
async function listTools(manager) {
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
}
async function listPrompts(manager) {
    const prompts = await manager.getAllPrompts();
    console.log(`Found ${prompts.length} prompts:\n`);
    for (const prompt of prompts) {
        console.log(`💬 ${prompt.serverName} / ${prompt.name}`);
        console.log(`   ${prompt.description}`);
        if (prompt.arguments && prompt.arguments.length > 0) {
            console.log(`   Arguments: ${prompt.arguments.map((a) => a.name).join(', ')}`);
        }
        console.log('');
    }
}
async function listResources(manager) {
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
async function analyzeForTask(manager, task) {
    if (!task) {
        console.error('Please provide a task description');
        process.exit(1);
    }
    console.log(`Analyzing tools for task: "${task}"\n`);
    const tools = await manager.getAllTools();
    const analysis = analyzeToolsForTask(tools, task);
    console.log(`Confidence: ${(analysis.confidence * 100).toFixed(1)}%`);
    console.log(`\nRelevant tools (${analysis.relevantTools.length}):\n`);
    for (let i = 0; i < analysis.relevantTools.length; i++) {
        const tool = analysis.relevantTools[i];
        console.log(`${i + 1}. ${tool.serverName} / ${tool.name}`);
        console.log(`   ${analysis.reasoning[i]}`);
        console.log('');
    }
}
async function callTool(manager, serverName, toolName, argsJson) {
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
  list-tools              List all tools from all MCP servers
  list-prompts            List all prompts from all MCP servers
  list-resources          List all resources from all MCP servers
  analyze <task>          Analyze which tools are relevant for a task
  call-tool <server> <tool> <json>  Call a specific tool

Examples:
  cli.ts list-tools
  cli.ts analyze "search the web for documentation"
  cli.ts call-tool memory add '{"key":"name","value":"Alice"}'
  `);
}
main();
