from __future__ import annotations

import asyncio
import time

from PIL import ImageDraw


class App:
    LEFT = -1
    RIGHT = 1

    def __init__(self) -> None:
        self._etch = None

    async def __call__(self, etch) -> None:
        self._etch = etch

        async with etch:
            self.reset_hardware()
            with etch.left_knob.config(
                on_update=lambda v, d: self.on_left_rotate(v, d),
                on_release=lambda _: self.on_left_click(),
            ), etch.right_knob.config(
                on_update=lambda v, d: self.on_right_rotate(v, d),
                on_release=lambda _: self.on_right_click(),
            ):
                return await self.start()

    @property
    def etch(self):
        return self._etch

    @property
    def draw(self):
        return ImageDraw.Draw(self.etch.frame_buffer)

    def reset_hardware(self):
        self.etch.clear()
        self.etch.left_knob.reset()
        self.etch.right_knob.reset()
        self.etch.set_display_mode(self.etch.modes.GC16)

    async def start(self) -> Optional[App]:
        self.etch.set_display_mode(self.etch.modes.A2)
        self.etch.text("Not Implemented")
        time.sleep(3)

    def on_left_rotate(self, value, direction):
        self.on_rotate(value, direction)

    def on_right_rotate(self, value, direction):
        self.on_rotate(value, direction)

    def on_rotate(self, value, direction):
        pass

    def on_left_click(self):
        self.on_click()

    def on_right_click(self):
        self.on_click()

    def on_click(self):
        pass
