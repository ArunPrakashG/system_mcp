"""
Minimal MCP client that connects to the local FastMCP server over stdio and
invokes each tool for a quick smoke test.

This uses the official MCP Python SDK high-level client.
"""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

SERVER_PARAMS = StdioServerParameters(
    command="uv",
    args=["run", "-m", "system_mcp.server"],
)


async def run() -> None:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            async def call(name: str, arguments: dict[str, Any] | None = None) -> None:
                print(f"\n==> Calling {name} {arguments or {}}")
                res = await session.call_tool(name, arguments or {})
                # Prefer structured content if available
                if hasattr(res, "structuredContent") and res.structuredContent:
                    print("Structured:", res.structuredContent)
                # Also print any unstructured text content
                for c in res.content:
                    if isinstance(c, types.TextContent):
                        print("Text:", c.text[:400])

            # Mouse
            await call("mouse_get_position")
            await call("mouse_click", {"button": "left"})

            # Window
            await call("window_list", {"visible_only": True, "title_only": True})

            # UIA
            await call("element_under_cursor")
            await call("text_under_cursor")

            # Screenshot: small region around cursor to avoid huge payloads
            pos_res = await session.call_tool("mouse_get_position", {})
            x = y = 0
            if hasattr(pos_res, "structuredContent") and pos_res.structuredContent:
                x = int(pos_res.structuredContent.get("x", 0))
                y = int(pos_res.structuredContent.get("y", 0))
            await call(
                "take_screenshot",
                {
                    "left": max(0, x - 50),
                    "top": max(0, y - 50),
                    "width": 100,
                    "height": 100,
                    "fmt": "png",
                },
            )


if __name__ == "__main__":
    asyncio.run(run())
