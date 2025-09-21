from __future__ import annotations

import base64
import io
from dataclasses import dataclass
from typing import Literal

import mss
from PIL import Image


@dataclass
class ScreenshotResult:
    width: int
    height: int
    format: Literal["png", "jpeg"]
    data_base64: str


def take_screenshot(
    monitor: int | None = None,
    *,
    region: tuple[int, int, int, int] | None = None,  # left, top, width, height
    fmt: Literal["png", "jpeg"] = "png",
    quality: int | None = None,
) -> ScreenshotResult:
    with mss.mss() as sct:
        if region is not None:
            left, top, width, height = region
            bbox = {"left": int(left), "top": int(top), "width": int(width), "height": int(height)}
            shot = sct.grab(bbox)
        else:
            mon = sct.monitors[0] if monitor is None else sct.monitors[int(monitor)]
            shot = sct.grab(mon)

        img = Image.frombytes("RGB", shot.size, shot.rgb)
        buf = io.BytesIO()
        save_kwargs: dict = {}
        if fmt == "jpeg" and quality is not None:
            save_kwargs["quality"] = int(quality)
        img.save(buf, format=fmt.upper(), **save_kwargs)
        data_b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return ScreenshotResult(
            width=img.width,
            height=img.height,
            format=fmt,
            data_base64=data_b64,
        )
