from typing import (
    Optional,
    Tuple,
)
import asyncio
import logging
import os
import signal

from IT8951.display import AutoEPDDisplay
from IT8951.constants import DisplayModes
from PIL import ImageDraw, ImageFont
from PIL.Image import Image

from .common import DO_NOTHING
from .knob import Knob
from .menu import Menu
from .sensors import Sensor


class EtchASketch:
    pass

    def __init__(self, on_double_long_press=DO_NOTHING) -> None:
        logging.basicConfig(
            level=os.environ.get("LOGLEVEL", "INFO").upper(),
            format="[%(levelname)s] %(message)s",
        )
        loop = self._loop = asyncio.get_event_loop()

        def signal_handler() -> None:
            """Stop the service and cleanup devices on receiving a signal."""
            loop.stop()

        for sig in (signal.SIGINT, signal.SIGQUIT, signal.SIGTERM):
            loop.add_signal_handler(sig, signal_handler)

        self._display_mode = DisplayModes.GC16
        self._left = Knob(0x3C)
        self._right = Knob(0x3D)
        self._sensor = Sensor(0x1D)
        self._display = AutoEPDDisplay(vcom=-1.61, track_gray=True)
        self.clear()

    @property
    def left_knob(self):
        return self._left

    @property
    def right_knob(self):
        return self._right

    @property
    def sensor(self):
        return self._sensor

    def clear(self) -> None:
        self._display.clear()

    def blank(self) -> None:
        draw = ImageDraw.Draw(self.image)
        draw.rectangle(
            (
                (0, 0),
                self.image.size,
            ),
            fill=0xFF,
        )

    def set_display_mode(self, mode):
        self._display_mode = mode

    def refresh(self, full: bool = False, mode: int = None) -> None:
        if full:
            self._display.draw_full(mode or self._display_mode)
        else:
            self._display.draw_partial(mode or self._display_mode)

    def run(self, task):
        self._loop.run_until_complete(task(self))

    @property
    def image(self) -> Image:
        return self._display.frame_buf

    def text(
        self,
        text: str,
        x: Optional[int] = None,
        y: Optional[int] = None,
        font: str = "DejaVuSans",
        size: int = 40,
        color: int = 0x00,
        update: bool = True,
        callback=None,
    ) -> Tuple[int, int]:
        draw = ImageDraw.Draw(self.image)

        image_font = self._get_font(font, size)

        width, height = self.image.size
        text_width, _ = image_font.getsize(text)
        text_height = size

        draw_x = x if x is not None else (width - text_width) // 2
        draw_y = y if y is not None else (height - text_height) // 2

        if callback:
            callback(draw_x, draw_y, text_width, text_height)

        draw.text((draw_x, draw_y), text, font=image_font, fill=color)

        if update:
            self.refresh()

        return draw_x, draw_y, text_width, text_height

    @staticmethod
    def _get_font(name: str, size: int) -> ImageFont:
        return ImageFont.truetype(
            os.path.join("home", "pi", "fonts", f"{name}.ttf"),
            size,
        )

    def menu(self, title: str, *options: Tuple[str], default=0) -> int:
        menu = Menu(self, title, *options, default=default)
        return menu.select()
