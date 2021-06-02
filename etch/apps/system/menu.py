from typing import (
    Optional,
    Tuple,
)
import asyncio
import datetime

from ..app import App


class Menu(App):
    def __init__(self, etch, title: str, *options: Tuple[str, ...], default=0) -> None:
        super().__init__()
        self._title = title
        self._options = options
        self._offset = 150
        self._x = 0
        self._width = etch.image.size[0]
        self._selected = default % len(options)

    async def start(self) -> Optional[App]:
        done = False
        self._draw_menu(True)
        last_set = datetime.datetime.now()

        def set_selected(sign: int) -> None:
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

        def set_done() -> None:
            nonlocal done
            done = True

        with self.etch.left_knob.config(
            value=self._selected,
            max_=len(self._options),
            on_update=lambda _, s: set_selected(s),
            on_press=set_done,
        ), self.etch.right_knob.config(
            value=self._selected,
            max_=len(self._options),
            on_update=lambda _, s: set_selected(s),
            on_press=set_done,
        ):
            while not done:
                await asyncio.sleep(1)

        return self._selected

    def _draw_menu(self, full: bool = False) -> None:
        self.etch.blank()
        self._draw_title()
        self._draw_options()
        self.etch.refresh(full, wait=True)

    def _draw_title(self) -> None:
        self._x, _, self._width, h = self.etch.text(
            self._title,
            y=self._offset,
            font="Magic",
            size=120,
            update=False,
        )
        self.draw.line(
            (
                (self._x, self._offset - 10),
                (self._x + self._width, self._offset - 10),
            ),
            width=3,
        )
        self.draw.line(
            (
                (self._x, self._offset + h + 30),
                (self._x + self._width, self._offset + h + 30),
            ),
            width=3,
        )

    def _draw_options(self) -> None:
        for i, opt in enumerate(self._options):
            self.etch.text(
                opt,
                x=self._x + 40,
                y=self._offset + 120 + 100 * (i + 1),
                size=60,
                update=False,
                color=0x00 if i == self._selected else 0x90,
                callback=lambda x, y, _, __: self.draw.rectangle(
                    (
                        (x - 10, y),
                        (x + self._width - 60, y + 70),
                    ),
                    fill=0xD0,
                )
                if i == self._selected
                else lambda *_: None,
            )
