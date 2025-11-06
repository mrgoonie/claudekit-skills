# Troubleshooting

Common issues, debugging, and solutions for Claude Code.

## Authentication Issues

### API Key Not Recognized

**Symptoms:**
- "Invalid API key" errors
- Authentication failures
- 401 Unauthorized responses

**Solutions:**

```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Re-login
claude logout
claude login

# Check API key format (should start with sk-ant-)
echo $ANTHROPIC_API_KEY | grep "^sk-ant-"

# Test API key directly
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```

### Environment Variable Issues

```bash
# Add to shell profile
echo 'export ANTHROPIC_API_KEY=sk-ant-xxxxx' >> ~/.bashrc
source ~/.bashrc

# Or use .env file
echo 'ANTHROPIC_API_KEY=sk-ant-xxxxx' > .claude/.env

# Verify it's loaded
claude config get apiKey
```

## Installation Problems

### npm Installation Failures

```bash
# Clear npm cache
npm cache clean --force

# Remove and reinstall
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code

# Use specific version
npm install -g @anthropic-ai/claude-code@1.0.0

# Check installation
which claude
claude --version
```

### Permission Errors

```bash
# Fix permissions on Unix/Mac
sudo chown -R $USER ~/.claude
chmod -R 755 ~/.claude

# Or install without sudo (using nvm)
nvm install 18
npm install -g @anthropic-ai/claude-code
```

### Python Installation Issues

```bash
# Upgrade pip
pip install --upgrade pip

# Install in virtual environment
python -m venv claude-env
source claude-env/bin/activate
pip install claude-code

# Install with --user flag
pip install --user claude-code
```

## Connection & Network Issues

### Proxy Configuration

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1

# Configure in settings
claude config set proxy http://proxy.company.com:8080

# Test connection
curl -x $HTTP_PROXY https://api.anthropic.com
```

### SSL/TLS Errors

```bash
# Trust custom CA certificate
export NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.crt

# Disable SSL verification (not recommended for production)
export NODE_TLS_REJECT_UNAUTHORIZED=0

# Update ca-certificates
sudo update-ca-certificates  # Debian/Ubuntu
sudo update-ca-trust         # RHEL/CentOS
```

### Firewall Issues

```bash
# Check connectivity to Anthropic API
ping api.anthropic.com
telnet api.anthropic.com 443

# Test HTTPS connection
curl -v https://api.anthropic.com

# Check firewall rules
sudo iptables -L  # Linux
netsh advfirewall show allprofiles  # Windows
```

## MCP Server Problems

### Server Not Starting

```bash
# Test MCP server command manually
npx -y @modelcontextprotocol/server-filesystem /tmp

# Check server logs
cat ~/.claude/logs/mcp-*.log

# Verify environment variables
echo $GITHUB_TOKEN  # For GitHub MCP

# Test with MCP Inspector
npx @modelcontextprotocol/inspector
```

### Connection Timeouts

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-example"],
      "timeout": 30000,
      "retries": 3
    }
  }
}
```

### Permission Denied

```bash
# Check file permissions
ls -la /path/to/mcp/server

# Make executable
chmod +x /path/to/mcp/server

# Check directory access
ls -ld /path/to/allowed/directory
```

## Performance Issues

### Slow Responses

**Check network latency:**
```bash
ping api.anthropic.com
```

**Use faster model:**
```bash
claude --model haiku "simple task"
```

**Reduce context:**
```json
{
  "maxTokens": 4096,
  "context": {
    "autoTruncate": true
  }
}
```

**Enable caching:**
```json
{
  "caching": {
    "enabled": true
  }
}
```

### High Memory Usage

```bash
# Clear cache
rm -rf ~/.claude/cache/*

# Limit context window
claude config set maxTokens 8192

# Disable memory
claude config set memory.enabled false

# Close unused sessions
claude session list
claude session close session-123
```

### Rate Limiting

```bash
# Check rate limits
claude usage show

# Wait and retry
sleep 60
claude "retry task"

# Implement exponential backoff in scripts
```

## Tool Execution Errors

### Bash Command Failures

**Check sandboxing settings:**
```json
{
  "sandboxing": {
    "enabled": true,
    "allowedPaths": ["/workspace", "/tmp"]
  }
}
```

**Verify command permissions:**
```bash
# Make script executable
chmod +x script.sh

# Check PATH
echo $PATH
which command-name
```

### File Access Denied

```bash
# Check file permissions
ls -la file.txt

# Change ownership
sudo chown $USER file.txt

# Grant read/write permissions
chmod 644 file.txt
```

### Write Tool Failures

```bash
# Check disk space
df -h

# Verify directory exists
mkdir -p /path/to/directory

# Check write permissions
touch /path/to/directory/test.txt
rm /path/to/directory/test.txt
```

## Hook Errors

### Hooks Not Running

```bash
# Verify hooks.json syntax
cat .claude/hooks.json | jq .

# Check hook script permissions
chmod +x .claude/scripts/hook.sh

# Test hook script manually
.claude/scripts/hook.sh

# Check logs
cat ~/.claude/logs/hooks.log
```

### Hook Script Errors

```bash
# Add error handling to hooks
#!/bin/bash
set -e  # Exit on error
set -u  # Exit on undefined variable

# Debug hook execution
#!/bin/bash
set -x  # Print commands
echo "Hook running: $TOOL_NAME"
```

## Debug Mode

### Enable Debugging

```bash
# Set debug environment variable
export CLAUDE_DEBUG=1
export CLAUDE_LOG_LEVEL=debug

# Run with debug flag
claude --debug "task"

# View debug logs
tail -f ~/.claude/logs/debug.log
```

### Verbose Output

```bash
# Enable verbose mode
claude --verbose "task"

# Show all tool calls
claude --show-tools "task"

# Display thinking process
claude --show-thinking "task"
```

## Common Error Messages

### "Model not found"

```bash
# Use correct model name
claude --model claude-sonnet-4-5-20250929

# Update claude-code
npm update -g @anthropic-ai/claude-code
```

### "Rate limit exceeded"

```bash
# Wait and retry
sleep 60

# Check usage
claude usage show

# Implement rate limiting in code
```

### "Context length exceeded"

```bash
# Reduce context
claude config set maxTokens 100000

# Summarize long content
claude "summarize this codebase"

# Process in chunks
claude "analyze first half of files"
```

### "Timeout waiting for response"

```bash
# Increase timeout
claude config set timeout 300

# Check network connection
ping api.anthropic.com

# Retry with smaller request
```

## Getting Help

### Collect Diagnostic Info

```bash
# System info
claude --version
node --version
npm --version

# Configuration
claude config list --all

# Recent logs
tail -n 100 ~/.claude/logs/session.log

# Environment
env | grep CLAUDE
env | grep ANTHROPIC
```

### Report Issues

1. **Check existing issues**: https://github.com/anthropics/claude-code/issues
2. **Gather diagnostic info**
3. **Create minimal reproduction**
4. **Submit issue** with:
   - Claude Code version
   - Operating system
   - Error messages
   - Steps to reproduce

### Support Channels

- **Documentation**: https://docs.claude.com/claude-code
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Support Portal**: support.claude.com
- **Community Discord**: discord.gg/anthropic

## See Also

- Installation guide: `references/getting-started.md`
- Configuration: `references/configuration.md`
- MCP setup: `references/mcp-integration.md`
- Best practices: `references/best-practices.md`
