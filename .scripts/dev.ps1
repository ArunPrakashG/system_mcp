# Runs the MCP Inspector (dev) against the server via stdio
param()

$ErrorActionPreference = 'Stop'

# Ensure uv is available on PATH
# Use the top-level server.py wrapper for MCP Inspector
uv run mcp dev server.py
