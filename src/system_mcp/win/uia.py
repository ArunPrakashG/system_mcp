from __future__ import annotations

from dataclasses import dataclass

import uiautomation as auto


@dataclass
class ElementInfo:
    name: str | None
    control_type: str | None
    class_name: str | None
    bounding: tuple[int, int, int, int] | None  # left, top, right, bottom
    runtime_id: list[int] | None
    hwnd: int | None


def element_from_point(x: int, y: int) -> ElementInfo | None:
    try:
        ele = auto.ControlFromPoint(x, y)
    except Exception:
        return None
    if not ele:
        return None
    rect = ele.BoundingRectangle
    bounding = (rect.left, rect.top, rect.right, rect.bottom) if rect else None
    rid = None
    try:
        rid = ele.RuntimeId
    except Exception:
        rid = None
    hwnd = None
    try:
        hwnd = int(ele.GetNativeWindowHandle()) if ele.GetNativeWindowHandle() else None
    except Exception:
        hwnd = None
    return ElementInfo(
        name=ele.Name if hasattr(ele, "Name") else None,
        control_type=str(ele.ControlTypeName) if hasattr(ele, "ControlTypeName") else None,
        class_name=ele.ClassName if hasattr(ele, "ClassName") else None,
        bounding=bounding,
        runtime_id=list(rid) if rid else None,
        hwnd=hwnd,
    )


def element_text_from_point(x: int, y: int) -> str | None:
    ele = auto.ControlFromPoint(x, y)
    if not ele:
        return None
    # Prefer ValuePattern or LegacyIAccessible pattern name/text if available
    try:
        value = ele.GetValuePattern().Value
        if value:
            return str(value)
    except Exception:
        pass
    try:
        leg = ele.GetLegacyIAccessiblePattern()
        if leg:
            name = leg.Name
            if name:
                return str(name)
    except Exception:
        pass
    # Fallback to Name property
    try:
        return str(ele.Name)
    except Exception:
        return None
