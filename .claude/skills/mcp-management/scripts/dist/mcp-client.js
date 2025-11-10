#!/usr/bin/env node
/**
 * MCP Client - Core client for interacting with MCP servers
 */
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { readFile } from 'fs/promises';
import { resolve } from 'path';
export class MCPClientManager {
    config = null;
    clients = new Map();
    async loadConfig(configPath = '.claude/.mcp.json') {
        const fullPath = resolve(process.cwd(), configPath);
        const content = await readFile(fullPath, 'utf-8');
        const config = JSON.parse(content);
        this.config = config;
        return config;
    }
    async connectToServer(serverName) {
        if (!this.config?.mcpServers[serverName]) {
            throw new Error(`Server ${serverName} not found in config`);
        }
        const serverConfig = this.config.mcpServers[serverName];
        const transport = new StdioClientTransport({
            command: serverConfig.command,
            args: serverConfig.args,
            env: serverConfig.env
        });
        const client = new Client({
            name: `mcp-manager-${serverName}`,
            version: '1.0.0'
        }, { capabilities: {} });
        await client.connect(transport);
        this.clients.set(serverName, client);
        return client;
    }
    async connectAll() {
        if (!this.config) {
            throw new Error('Config not loaded. Call loadConfig() first.');
        }
        const connections = Object.keys(this.config.mcpServers).map(name => this.connectToServer(name));
        await Promise.all(connections);
    }
    async getAllTools() {
        const allTools = [];
        for (const [serverName, client] of this.clients.entries()) {
            const response = await client.listTools();
            for (const tool of response.tools) {
                allTools.push({
                    serverName,
                    name: tool.name,
                    description: tool.description || '',
                    inputSchema: tool.inputSchema,
                    outputSchema: tool.outputSchema
                });
            }
        }
        return allTools;
    }
    async getAllPrompts() {
        const allPrompts = [];
        for (const [serverName, client] of this.clients.entries()) {
            const response = await client.listPrompts();
            for (const prompt of response.prompts) {
                allPrompts.push({
                    serverName,
                    name: prompt.name,
                    description: prompt.description || '',
                    arguments: prompt.arguments
                });
            }
        }
        return allPrompts;
    }
    async getAllResources() {
        const allResources = [];
        for (const [serverName, client] of this.clients.entries()) {
            const response = await client.listResources();
            for (const resource of response.resources) {
                allResources.push({
                    serverName,
                    uri: resource.uri,
                    name: resource.name,
                    description: resource.description,
                    mimeType: resource.mimeType
                });
            }
        }
        return allResources;
    }
    async callTool(serverName, toolName, args) {
        const client = this.clients.get(serverName);
        if (!client)
            throw new Error(`Not connected to server: ${serverName}`);
        return await client.callTool({ name: toolName, arguments: args });
    }
    async getPrompt(serverName, promptName, args) {
        const client = this.clients.get(serverName);
        if (!client)
            throw new Error(`Not connected to server: ${serverName}`);
        return await client.getPrompt({ name: promptName, arguments: args });
    }
    async readResource(serverName, uri) {
        const client = this.clients.get(serverName);
        if (!client)
            throw new Error(`Not connected to server: ${serverName}`);
        return await client.readResource({ uri });
    }
    async cleanup() {
        for (const client of this.clients.values()) {
            await client.close();
        }
        this.clients.clear();
    }
}
