from etch.common import DO_NOTHING
from random import randint
import asyncio

from IT8951.constants import DisplayModes
from PIL import ImageDraw


class Line:
    def __init__(self, etch):
        self._draw = ImageDraw.Draw(etch.image)
        self._size = 12
        self._x = 1872 / self._size / 2
        self._y = 1404 / self._size / 2
        self._direction = randint(0, 4)

    def update(self):
        if randint(0, 100) < 20:
            self._direction = randint(0, 4)

        if self._direction == 0:
            self._x += 1
        elif self._direction == 1:
            self._x -= 1
        elif self._direction == 2:
            self._y += 1
        else:
            self._y -= 1

        if self._x < 0:
            self._x = 0
            self._direction = randint(0, 4)
        elif self._x >= 1872 / self._size:
            self._x = 1872 / self._size - self._size
            self._direction = randint(0, 4)
        elif self._y < 0:
            self._y = 0
            self._direction = randint(0, 4)
        elif self._y >= 1404 / self._size:
            self._y = 1404 / self._size - self._size
            self._direction = randint(0, 4)

        self._place_pixel(self._x, self._y)

    def _place_pixel(self, x, y):
        self._draw.rectangle(
            (
                (self._size * x, self._size * y),
                (self._size * x + self._size, self._size * y + self._size),
            ),
            0x00,
        )


class Sketch:
    def __init__(self) -> None:
        self._etch = None

    async def __call__(self, etch) -> None:
        self._etch = etch
        self._etch.set_display_mode(DisplayModes.DU)
        self._etch.clear()

        with etch.left_knob.configuration(
            on_update=lambda v: print(f"LEFT {v}", flush=True),
            on_press=lambda: print("LEFT PRESSED", flush=True),
            on_release=lambda: print("LEFT RELEASED", flush=True),
        ):
            line = Line(etch)
            while True:
                line.update()
                etch.refresh()
                if etch.right_knob.is_pressed:
                    break
                await asyncio.sleep(0.1)

        etch.display_menu(
            "Choose an Activity",
            ("Sketch", sketch),
            ("Pong", DO_NOTHING),
            ("Tetris", DO_NOTHING),
        )


sketch = Sketch()
