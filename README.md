# System MCP (Windows)

An MCP server exposing Windows-native capabilities:

- Cursor control (get/set position, click)
- Window management (list, move/resize, activate)
- UI Automation (element/text under cursor)
- Screenshots (full monitor or region, PNG/JPEG base64)

Built with Python, uv, Ruff, and the official `mcp` Python SDK.

## Using in VS Code

Follow these steps to install and use this MCP server entirely from VS Code on Windows:

1. Open the folder

- File > Open Folder… and pick this repository.

2. Install dependencies (once)

- Open the integrated Terminal (PowerShell) and run:
  ```powershell
  uv sync
  ```

3. Run the server via a VS Code Task

- From the Command Palette: "Tasks: Run Task" → choose "Run MCP server (uv)".
- This starts the MCP server over stdio using `uv run -m system_mcp.server`.

4. Inspect and debug tools with MCP Inspector (interactive)

- In the VS Code Terminal, run:
  ```powershell
  .scripts/dev.ps1
  ```
- Your browser opens the Inspector; choose the stdio session and try tools like:
  - "Mouse: Get Position"
  - "Window: List"
  - "UIA: Text Under Cursor"
  - "Screen: Take Screenshot"

5. Programmatic smoke test (optional)

- Run the sample client from the Terminal to exercise all tools:
  ```powershell
  uv run examples/call_tools.py
  ```

6. Debugging tips

- You can set breakpoints in files under `src/system_mcp/**` and run the server via the task; logs and tracebacks will appear in the Terminal.
- For step-through debugging, you can also create a `launch.json` that runs the module `system_mcp.server`. (Optional; not required for normal use.)

Troubleshooting

- PowerShell policies: If scripts don’t run, execute the dev script like this to bypass policy for the current invocation:
  ```powershell
  powershell -NoProfile -ExecutionPolicy Bypass -File .scripts/dev.ps1
  ```
- UAC/Admin: Some UI Automation or window operations may require running VS Code or your MCP client as Administrator.
- uv on PATH: Ensure `uv` is installed and available (`uv --version`).

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

## Standalone CLI (Context7-style)

This package can run as a standalone MCP server with a console script:

```powershell
# Using the module entry point
uv run -m system_mcp --transport stdio

# Using the console script (provided by project.scripts)
uv run system-mcp --transport stdio

# Network transports (for browsers/remote)
uv run system-mcp --transport sse --port 3000
uv run system-mcp --transport streamable-http --port 3001
```

To install the CLI into your active virtual environment (or a global tools env):

```powershell
# Local editable install (puts the 'system-mcp' script on PATH for this venv)
uv pip install -e .

# Or install as a uv tool (isolated)
uv tool install --with . system-mcp
```

### Releases and cross-project installs

1. Tag and publish a GitHub release (from this repo):

- Bump version in `pyproject.toml` if needed.
- Create an annotated tag, e.g. `v0.1.0`, and push it.
- Create a GitHub Release for that tag (optional but recommended).

2. Install the tagged CLI globally with pipx or uv:

- pipx (recommended for global tools):
  ```powershell
  pipx install --force "git+https://github.com/ArunPrakashG/system_mcp.git@v0.1.0"
  ```
- uv tool (isolated tool install):
  ```powershell
  uv tool install --with "git+https://github.com/ArunPrakashG/system_mcp.git@v0.1.0" system-mcp
  ```

3. Use in any project (VS Code task snippet):

- Copy `templates/tasks.system-mcp.json` into your project’s `.vscode/tasks.json` (or merge it), then run the task "Run MCP server (system-mcp)".

4. Optional PyPI wrapper

- A tiny wrapper package scaffold is included under `wrappers/pypi/`.
- If you publish it to PyPI (e.g., name `system-mcp-wrapper`), others can simply:
  ```powershell
  pip install system-mcp-wrapper
  system-mcp --transport stdio
  ```
- The wrapper depends on this GitHub repo at a tag. Update that tag in `wrappers/pypi/pyproject.toml` before publishing a new release.

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

This project is licensed under the MIT License — see the `LICENSE` file for details.
