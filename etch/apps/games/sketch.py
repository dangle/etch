import asyncio

from IT8951.constants import DisplayModes

from ..app import App


class Sketch(App):
    def __init__(self) -> None:
        super().__init__()
        self._size = 3
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
            self.etch.left_knob.value = self._x
        return self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value >= 3 and value < self._height - 1:
            self._y = value
        else:
            self.etch.right_knob.value = self._y
        return self._y

    def _place_pixel(self, x, y):
        self.draw.rectangle(
            (
                (self._size * x, self._size * y),
                (self._size * x + self._size, self._size * y + self._size),
            ),
            0x00,
        )

    async def start(self) -> None:
        self.etch.set_display_mode(DisplayModes.A2)
        self._place_pixel(self.x, self._height - self.y)

        def set_x(_, sign):
            self.x += sign
            self._place_pixel(self.x, self._height - self.y)

        def set_y(_, sign):
            self.y += sign
            self._place_pixel(self.x, self._height - self.y)

        with self.etch.left_knob.config(
            value=self.x, max_=self._width, on_update=set_x
        ), self.etch.right_knob.config(
            value=self.y, max_=self._height, on_update=set_y
        ):
            while True:
                self.etch.refresh()
                await asyncio.sleep(0.05)


sketch = Sketch()
