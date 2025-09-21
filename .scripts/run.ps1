# Runs the MCP server directly (stdio)
param()

$ErrorActionPreference = 'Stop'

uv run -m system_mcp.server
