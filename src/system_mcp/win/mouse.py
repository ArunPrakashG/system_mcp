from __future__ import annotations

import ctypes
from ctypes import wintypes
from dataclasses import dataclass

# Windows API structures and functions via ctypes
user32 = ctypes.WinDLL("user32", use_last_error=True)


@dataclass
class Point:
    x: int
    y: int


POINT = wintypes.POINT


def _raise_last_error(prefix: str) -> None:
    err = ctypes.get_last_error()
    raise ctypes.WinError(err, f"{prefix} failed: {err}")


def get_cursor_pos() -> Point:
    pt = POINT()
    if not user32.GetCursorPos(ctypes.byref(pt)):
        _raise_last_error("GetCursorPos")
    return Point(x=pt.x, y=pt.y)


def set_cursor_pos(x: int, y: int) -> None:
    if not user32.SetCursorPos(int(x), int(y)):
        _raise_last_error("SetCursorPos")


# Mouse event flags
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800


def click(button: str = "left") -> None:
    if button == "left":
        down, up = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
    elif button == "right":
        down, up = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
    elif button == "middle":
        down, up = MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
    else:
        raise ValueError("invalid button")

    user32.mouse_event(down, 0, 0, 0, 0)
    user32.mouse_event(up, 0, 0, 0, 0)
