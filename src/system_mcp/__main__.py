from __future__ import annotations

import argparse

from .server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="system-mcp",
        description=(
            "Standalone MCP server exposing Windows mouse, window, UIA, and screenshot tools."
        ),
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport to run the MCP server with (default: stdio).",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host/interface for SSE or streamable-http transports (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port for SSE or streamable-http transports (default: 3000).",
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        # Default stdio for typical MCP clients
        mcp.run()
    else:
        # Network transports for browsers or remote clients
        mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
