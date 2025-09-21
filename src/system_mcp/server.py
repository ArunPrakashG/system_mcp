from __future__ import annotations

from typing import Literal, TypedDict

from mcp.server.fastmcp import FastMCP

from .win import mouse, screenshot, uia, window

mcp = FastMCP(
    name="System MCP (Windows)",
    instructions=(
        "Tools to read and control cursor, windows, and UI elements on Windows. "
        "Use cautiously; coordinates are in screen space."
    ),
)


# Mouse tools
class PointOut(TypedDict):
    x: int
    y: int


@mcp.tool(title="Mouse: Get Position")
def mouse_get_position() -> PointOut:
    pt = mouse.get_cursor_pos()
    return {"x": pt.x, "y": pt.y}


@mcp.tool(title="Mouse: Set Position")
def mouse_set_position(x: int, y: int) -> str:
    mouse.set_cursor_pos(x, y)
    return f"moved to {x},{y}"


@mcp.tool(title="Mouse: Click")
def mouse_click(button: Literal["left", "right", "middle"] = "left") -> str:
    mouse.click(button)
    return f"clicked {button}"


# Window tools
class WindowOut(TypedDict):
    hwnd: int
    title: str
    left: int
    top: int
    width: int
    height: int


@mcp.tool(title="Window: List")
def window_list(visible_only: bool = True, title_only: bool = True) -> list[WindowOut]:
    items = window.list_windows(visible_only=visible_only, title_only=title_only)
    return [
        {
            "hwnd": it.hwnd,
            "title": it.title,
            "left": it.left,
            "top": it.top,
            "width": it.width,
            "height": it.height,
        }
        for it in items
    ]


@mcp.tool(title="Window: Move/Resize")
def window_move(
    hwnd: int,
    x: int,
    y: int,
    width: int | None = None,
    height: int | None = None,
) -> str:
    window.move_window(hwnd, x, y, width=width, height=height)
    return "ok"


@mcp.tool(title="Window: Find By Title")
def window_find_by_title(substring: str) -> list[WindowOut]:
    items = window.find_windows_by_title(substring)
    return [
        {
            "hwnd": it.hwnd,
            "title": it.title,
            "left": it.left,
            "top": it.top,
            "width": it.width,
            "height": it.height,
        }
        for it in items
    ]


@mcp.tool(title="Window: Activate")
def window_activate(hwnd: int) -> str:
    window.set_foreground_window(hwnd)
    return "ok"


# UI Automation tools
class ElementOut(TypedDict):
    name: str | None
    control_type: str | None
    class_name: str | None
    bounding: tuple[int, int, int, int] | None
    runtime_id: list[int] | None
    hwnd: int | None


@mcp.tool(title="UIA: Element Under Cursor")
def element_under_cursor() -> ElementOut | None:
    pt = mouse.get_cursor_pos()
    info = uia.element_from_point(pt.x, pt.y)
    if not info:
        return None
    return {
        "name": info.name,
        "control_type": info.control_type,
        "class_name": info.class_name,
        "bounding": info.bounding,
        "runtime_id": info.runtime_id,
        "hwnd": info.hwnd,
    }


@mcp.tool(title="UIA: Text Under Cursor")
def text_under_cursor() -> str | None:
    pt = mouse.get_cursor_pos()
    return uia.element_text_from_point(pt.x, pt.y)


# Screenshot tools
class ScreenshotOut(TypedDict):
    width: int
    height: int
    format: Literal["png", "jpeg"]
    data_base64: str


@mcp.tool(title="Screen: Take Screenshot")
def take_screenshot(
    monitor: int | None = None,
    left: int | None = None,
    top: int | None = None,
    width: int | None = None,
    height: int | None = None,
    fmt: Literal["png", "jpeg"] = "png",
    quality: int | None = None,
) -> ScreenshotOut:
    region = None
    if None not in (left, top, width, height):
        region = (int(left or 0), int(top or 0), int(width or 0), int(height or 0))
    res = screenshot.take_screenshot(monitor=monitor, region=region, fmt=fmt, quality=quality)
    return {
        "width": res.width,
        "height": res.height,
        "format": res.format,
        "data_base64": res.data_base64,
    }


def main() -> None:
    # Default to stdio transport when run directly
    mcp.run()


if __name__ == "__main__":
    main()
