from typing import (
    Any,
    Optional,
    Tuple,
)
import asyncio
import os
import threading

from IT8951.display import AutoEPDDisplay
from IT8951.constants import DisplayModes
from PIL import ImageDraw, ImageFont
from PIL.Image import Image

from .common import DO_NOTHING
from .knob import Knob
from .menu import Menu
from .sensors import Sensor


class EtchASketch:
    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop()
        self._display_mode = DisplayModes.GC16
        self._display_lock = threading.Lock()
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
        with self._display_lock:
            self._display.clear()

    def blank(self) -> None:
        self._display.frame_buf.paste(
            0xFF, box=(0, 0, self._display.width, self._display.height)
        )

    def set_display_mode(self, mode):
        self._display_mode = mode

    def refresh(self, full: bool = False, wait=False, mode: int = None) -> None:
        def redraw_screen() -> None:
            with self._display_lock:
                draw = self._display.draw_full if full else self._display.draw_partial
                try:
                    draw(mode or self._display_mode)
                except TypeError:
                    pass

        if wait:
            redraw_screen()
        else:
            try:
                threading.Thread(target=redraw_screen).start()
            except:
                pass

    def queue(self, task):
        asyncio_task = self._loop.create_task(task(self))
        # TODO: Task handler
        # asyncio_task.add_done_callback()
        return asyncio_task

    def run(self, task):
        asyncio_task = self.queue(task)
        if not self._loop.is_running:
            self._loop.run_until_complete(asyncio_task)

    def start(self, task=None):
        if task is not None:
            self.queue(task)
        self._loop.run_forever()

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

    def display_menu(self, title: str, *options: Tuple[str, Any], default=0) -> None:
        return self.run(Menu(self, title, *options, default=default))
