from __future__ import annotations

import ctypes
from ctypes import wintypes
from dataclasses import dataclass

user32 = ctypes.WinDLL("user32", use_last_error=True)


RECT = wintypes.RECT


HWND = wintypes.HWND
LPARAM = wintypes.LPARAM
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, HWND, LPARAM)


@dataclass
class WindowInfo:
    hwnd: int
    title: str
    left: int
    top: int
    width: int
    height: int


def _raise_last_error(prefix: str) -> None:
    err = ctypes.get_last_error()
    raise ctypes.WinError(err, f"{prefix} failed: {err}")


def _get_window_text(hwnd: int) -> str:
    length = user32.GetWindowTextLengthW(HWND(hwnd))
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(HWND(hwnd), buf, length + 1)
    return buf.value


def _get_window_rect(hwnd: int) -> tuple[int, int, int, int]:
    rect = RECT()
    if not user32.GetWindowRect(HWND(hwnd), ctypes.byref(rect)):
        _raise_last_error("GetWindowRect")
    left, top = rect.left, rect.top
    width, height = rect.right - rect.left, rect.bottom - rect.top
    return left, top, width, height


def list_windows(visible_only: bool = True, title_only: bool = True) -> list[WindowInfo]:
    windows: list[WindowInfo] = []

    def _enum_proc(h: HWND, _lparam: LPARAM) -> bool:  # type: ignore[override]
        if visible_only and not user32.IsWindowVisible(h):
            return True
        title = _get_window_text(int(h))
        if title_only and not title:
            return True
        left_val, top_val, width_val, height_val = _get_window_rect(int(h))
        windows.append(
            WindowInfo(
                hwnd=int(h),
                title=title,
                left=left_val,
                top=top_val,
                width=width_val,
                height=height_val,
            )
        )
        return True

    if not user32.EnumWindows(WNDENUMPROC(_enum_proc), 0):
        _raise_last_error("EnumWindows")
    return windows


def move_window(
    hwnd: int,
    x: int,
    y: int,
    width: int | None = None,
    height: int | None = None,
    repaint: bool = True,
) -> None:
    # If width/height not provided, keep existing size
    if width is None or height is None:
        _, _, w, h = _get_window_rect(hwnd)
        if width is None:
            width = w
        if height is None:
            height = h
    if not user32.MoveWindow(HWND(hwnd), int(x), int(y), int(width), int(height), bool(repaint)):
        _raise_last_error("MoveWindow")


def find_windows_by_title(substring: str) -> list[WindowInfo]:
    sub = substring.lower()
    return [w for w in list_windows(visible_only=True, title_only=False) if sub in w.title.lower()]


def set_foreground_window(hwnd: int) -> None:
    if not user32.SetForegroundWindow(HWND(hwnd)):
        _raise_last_error("SetForegroundWindow")
