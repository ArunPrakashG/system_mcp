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

## CI Release

This repo includes two GitHub Actions:

- Build on PR/Push: `.github/workflows/build-extension.yml` builds and packages the VSIX on pushes/PRs that touch `vscode-extension/**`.
- Release on Tag: `.github/workflows/release-extension.yml` runs when you push a tag matching `vscode-v*`.

Release workflow steps:
1) Build and package `system-mcp-vscode.vsix`.
2) Create a GitHub Release for the tag and attach the VSIX file.
3) Optionally publish to the Marketplace if `VSCE_PAT` is configured.

### Tagging format

Push a tag like:

```powershell
git tag vscode-v0.1.0
git push origin vscode-v0.1.0
```

### Marketplace publish (optional)

Provide a Personal Access Token in a repo secret named `VSCE_PAT` with access to your VS Code publisher (e.g., `arunprakashg`). The release workflow will publish automatically when the secret is set.

If you need to create a publisher or PAT, see: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
