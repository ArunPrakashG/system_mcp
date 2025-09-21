# System MCP (Windows)

An MCP server exposing Windows-native capabilities:

- Cursor control (get/set position, click)
- Window management (list, move/resize, activate)
- UI Automation (element/text under cursor)
- Screenshots (full monitor or region, PNG/JPEG base64)

Built with Python, uv, Ruff, and the official `mcp` Python SDK.

## Requirements

- Windows 10/11
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) installed and on PATH
- Some tools may require running the MCP client or terminal as Administrator (UAC constraints)

## Setup

Install dependencies using uv (creates an isolated environment):

```powershell
uv sync
```

## Run (development, with MCP Inspector)

```powershell
.scripts/dev.ps1
```

This opens the MCP Inspector against the `server.py` wrapper (which runs the module under the hood).

## Run (stdio)

```powershell
.scripts/run.ps1
```

To install into Claude Desktop or another MCP client, you can typically run:

```powershell
# Option A: Using the top-level wrapper for simpler installs
uv run mcp install server.py --name "System MCP (Windows)"

# Option B: Install by module path (clients that support it)
uv run mcp install -m system_mcp.server --name "System MCP (Windows)"
```

## Tools exposed

- Mouse: Get Position
- Mouse: Set Position (x, y)
- Mouse: Click (left|right|middle)
- Window: List (visibleOnly, titleOnly)
- Window: Move/Resize (hwnd, x, y, width?, height?)
- Window: Find By Title (substring)
- Window: Activate (hwnd)
- UIA: Element Under Cursor
- UIA: Text Under Cursor
- Screen: Take Screenshot (monitor?, left?, top?, width?, height?, fmt=png|jpeg, quality?)

Coordinates are screen coordinates. Screenshot returns base64 image data; decode as needed.

## Notes

- On multi-monitor and scaled DPI setups, Windows UIA ElementFromPoint can be sensitive to scaling. If text/element does not match expectations, consider aligning display scaling or running elevated.
- The `uiautomation` library wraps Microsoft UI Automation; for complex traversal, extend `win/uia.py` accordingly.
- `mss` is used for fast screenshots; JPEG quality is adjustable.

## License

MIT
