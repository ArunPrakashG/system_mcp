# System MCP (Windows) – VS Code Extension

This extension connects VS Code to the System MCP Windows server to control the cursor, manage windows, read UI text, and take screenshots.

## Features
- Connect to the Python MCP server (spawned via `uv run -m system_mcp.server`)
- List available tools from the server
- Take a screenshot and preview it inside VS Code

## Commands
- System MCP: Connect (`systemMcp.connect`)
- System MCP: List Tools (`systemMcp.tools.list`)
- System MCP: Take Screenshot (`systemMcp.tools.screenshot`)

## Requirements
- Windows 10/11
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) available on PATH
- The System MCP Python project (this repo) checked out locally

## Development
- Install deps and build:
  ```powershell
  cd vscode-extension
  npm install
  npm run compile
  ```
- Press F5 to launch an Extension Development Host and run commands from the Command Palette.

## Packaging
- Create a .vsix package:
  ```powershell
  npm run package
  ```
  Upload the .vsix to a GitHub Release or install via "Extensions: Install from VSIX" in VS Code.
