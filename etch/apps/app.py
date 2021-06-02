from __future__ import annotations

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
            etch.clear()
            self.etch.set_display_mode(etch.modes.GC16)
            with self.etch.left_knob.config(
                on_update=lambda v, d: self.on_left_rotate(v, d)
            ), self.etch.right_knob.config(
                on_update=lambda v, d: self.on_right_rotate(v, d)
            ):
                return await self.start()

    @property
    def etch(self):
        return self._etch

    @property
    def draw(self):
        return ImageDraw.Draw(self.etch.image)

    async def start(self) -> Optional[App]:
        self.etch.set_display_mode(self.etch.modes.A2)
        self.etch.text("Not Implemented")
        time.sleep(3)

    def on_left_rotate(self, value, direction):
        pass

    def on_right_rotate(self, value, direction):
        pass

    def on_left_click(self):
        pass

    def on_right_click(self):
        pass
