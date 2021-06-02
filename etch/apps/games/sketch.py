import asyncio

from IT8951.constants import DisplayModes
from PIL import ImageDraw

from ...common import DO_NOTHING


class Sketch:
    SMALL = 3

    def __init__(self) -> None:
        self._etch = None
        self._size = Sketch.SMALL
        self._width = 1872 // self._size
        self._height = 1404 // self._size
        self._x = self._width // 2
        self._y = self._height // 2

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value >= 0 and value < self._width:
            self._x = value
        else:
            self._etch.left_knob.value = self._x
        return self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value >= 3 and value < self._height - 1:
            self._y = value
        else:
            self._etch.right_knob.value = self._y
        return self._y

    def _place_pixel(self, x, y):
        ImageDraw.Draw(self._etch.image).rectangle(
            (
                (self._size * x, self._size * y),
                (self._size * x + self._size, self._size * y + self._size),
            ),
            0x00,
        )

    async def __call__(self, etch) -> None:
        self._etch = etch
        self._etch.set_display_mode(DisplayModes.A2)
        self._etch.clear()

        def set_x(_, sign):
            self.x += sign
            self._place_pixel(self.x, self._height - self.y)

        def set_y(_, sign):
            self.y += sign
            self._place_pixel(self.x, self._height - self.y)

        with etch.left_knob.config(
            value=self.x, max_=self._width, on_update=set_x
        ), etch.right_knob.config(value=self.y, max_=self._height, on_update=set_y):
            count = 0
            while True:
                if etch.left_knob.is_long_pressed and etch.right_knob.is_long_pressed:
                    break
                if etch.left_knob.is_pressed and etch.right_knob.is_pressed:
                    if not count:
                        etch.blank()
                    else:
                        etch.clear()
                    await asyncio.sleep(0.1)
                    count = (count + 1) % 2
                etch.refresh()
                await asyncio.sleep(0.05)

        etch.display_menu(
            "Choose an Activity",
            ("Pong", DO_NOTHING),
            ("Sketch", sketch),
            ("Snake", DO_NOTHING),
            ("Tetris", DO_NOTHING),
            default=1,
        )


sketch = Sketch()
