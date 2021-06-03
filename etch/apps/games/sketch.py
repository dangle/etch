import asyncio

from ..app import App


class Sketch(App):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self._size = 3
        self._width = 1872 // self._size
        self._height = 1404 // self._size
        self._x = self._width // 2
        self._y = self._height // 2

    async def start(self) -> None:
        self.etch.set_display_mode(self.etch.modes.A2)
        self.update()

        with self.etch.left_knob.config(
            value=self.x, max_=self._width
        ), self.etch.right_knob.config(value=self.y, max_=self._height):
            while True:
                self.etch.refresh()
                await asyncio.sleep(0.05)

    def on_left_rotate(self, _, direction):
        self.x += direction
        self.update()

    def on_right_rotate(self, _, direction):
        self.y -= direction
        self.update()

    def update(self):
        self.draw.rectangle(
            (
                (self._size * self.x, self._size * self.y),
                (self._size * self.x + self._size, self._size * self.y + self._size),
            ),
            0x00,
        )

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
