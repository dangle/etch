from __future__ import annotations

import time

from PIL import ImageDraw


class App:
    def __init__(self) -> None:
        self._etch = None

    async def __call__(self, etch) -> None:
        self._etch = etch
        async with etch:
            etch.clear()
            self.etch.set_display_mode(etch.modes.GC16)
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

    def on_left_rotate(self):
        pass

    def on_right_rotate(self):
        pass

    def on_left_click(self):
        pass

    def on_right_click(self):
        pass
