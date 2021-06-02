from typing import (
    Any,
    Tuple,
)
import asyncio
import datetime

from IT8951.constants import DisplayModes
from PIL import ImageDraw

from .common import DO_NOTHING


class Menu:
    def __init__(self, etch, title: str, *options: Tuple[str, Any], default=0) -> None:
        self._etch = etch
        self._title = title
        self._options = options
        self._offset = 150
        self._x = 0
        self._width = etch.image.size[0]
        self._selected = default % len(options)

    async def __call__(self, etch) -> None:
        done = False
        etch.set_display_mode(DisplayModes.GC16)
        self._draw_menu(True)
        last_set = datetime.datetime.now()

        def set_selected(sign):
            nonlocal last_set
            now = datetime.datetime.now()
            if (
                sign < 0
                and self._selected > 0
                or sign > 0
                and self._selected < len(self._options) - 1
            ):
                if now - last_set > datetime.timedelta(milliseconds=250):
                    last_set = now
                    self._selected = (self._selected + sign) % len(self._options)
                    self._draw_menu()

        def set_done():
            nonlocal done
            done = True

        with etch.left_knob.configuration(
            value=self._selected,
            max_=len(self._options),
            on_update=lambda _, s: set_selected(s),
            on_press=set_done,
        ), etch.right_knob.configuration(
            value=self._selected,
            max_=len(self._options),
            on_update=lambda _, s: set_selected(s),
            on_press=set_done,
        ):
            while not done:
                await asyncio.sleep(1)

        self._etch.queue(self._options[self._selected][1])

    def _draw_menu(self, full=False) -> None:
        self._etch.blank()
        self._draw_title()
        self._draw_options()
        self._etch.refresh(full, wait=True)

    def _draw_title(self) -> None:
        self._x, _, self._width, h = self._etch.text(
            self._title,
            y=self._offset,
            font="Magic",
            size=120,
            update=False,
        )
        draw = ImageDraw.Draw(self._etch.image)
        draw.line(
            (
                (self._x, self._offset - 10),
                (self._x + self._width, self._offset - 10),
            ),
            width=3,
        )
        draw.line(
            (
                (self._x, self._offset + h + 30),
                (self._x + self._width, self._offset + h + 30),
            ),
            width=3,
        )

    def _draw_options(self) -> None:
        draw = ImageDraw.Draw(self._etch.image)
        for i, (opt, _) in enumerate(self._options):
            self._etch.text(
                opt,
                x=self._x + 40,
                y=self._offset + 120 + 100 * (i + 1),
                size=60,
                update=False,
                color=0x00 if i == self._selected else 0x90,
                callback=lambda x, y, _, __: draw.rectangle(
                    (
                        (x - 10, y),
                        (x + self._width - 60, y + 70),
                    ),
                    fill=0xD0,
                )
                if i == self._selected
                else DO_NOTHING,
            )
