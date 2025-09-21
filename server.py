"""
Wrapper entrypoint for MCP installers/clients that expect a single Python file.

This adjusts sys.path to include the local 'src' directory so that
`import system_mcp.server` works when run as a plain script, and exposes a
top-level `mcp` object for the MCP Inspector.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure 'src' is on sys.path for local imports when used by MCP Inspector
_REPO_ROOT = Path(__file__).resolve().parent
_SRC_DIR = str(_REPO_ROOT / "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

# Re-export the FastMCP instance so `mcp dev server.py` can discover it
from system_mcp.server import main as run_server  # noqa: E402
from system_mcp.server import mcp  # noqa: E402,F401


def main() -> None:
    run_server()


if __name__ == "__main__":
    main()
