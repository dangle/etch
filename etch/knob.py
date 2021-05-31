import asyncio
import functools
import sys
import time

import qwiic_twist

from .common import DO_NOTHING, NOT_SUPPLIED


class Knob:
    def __init__(
        self,
        address,
        max_=None,
        default=0,
        on_update=None,
        on_press=None,
        on_release=None,
    ):
        self._twist = qwiic_twist.QwiicTwist(address)
        self._twist.set_int_timeout(0)
        self.configure(
            default,
            max_ or sys.maxsize,
            on_update or DO_NOTHING,
            on_press or DO_NOTHING,
            on_release or DO_NOTHING,
        )
        loop = asyncio.get_event_loop()
        rotate_task = loop.create_task(self._poll_encoder())
        button_task = loop.create_task(self._poll_button())
        # TODO: task.add_done_callback()

    def configure(
        self,
        value=NOT_SUPPLIED,
        max_=NOT_SUPPLIED,
        on_update=NOT_SUPPLIED,
        on_press=NOT_SUPPLIED,
        on_release=NOT_SUPPLIED,
    ):
        self._twist.begin()
        if max_ is not NOT_SUPPLIED:
            self._twist.set_limit(max_)
        if value is not NOT_SUPPLIED:
            self._twist.set_count(value)
            self._last_count = value
        if on_update is not NOT_SUPPLIED:
            self._on_update = on_update
        if on_press is not NOT_SUPPLIED:
            self._on_press = on_press
        if on_release is not NOT_SUPPLIED:
            self._on_release = on_release

    @property
    def is_pressed(self):
        while 1:
            try:
                return self._twist.pressed
            except OSError:
                time.sleep(0.01)

    @property
    def is_long_pressed(self):
        return self.is_pressed and self._twist.since_last_press(False) > 3000

    @property
    def value(self):
        return self._twist.count

    def set_color(self, red: int, blue: int, green: int) -> None:
        self._twist.set_color(red, green, blue)

    async def _poll_encoder(self):
        while 1:
            try:
                if (
                    self._twist.has_moved()
                ):  # FIXME: seems to trigger when register overflows
                    current = self._twist.count
                    diff = self._last_count - current
                    step = 1 if diff > 0 else -1
                    current
                    self._last_count = current
                    self._on_update(current)
                    self._twist._i2c.writeWord(self._twist.address, 0x01, 0x00)
            except OSError:
                pass
            await asyncio.sleep(0.05)

    async def _poll_button(self):
        _is_pressed = self.is_pressed
        while 1:
            try:
                if _is_pressed and not self._twist.is_pressed:
                    _is_pressed = False
                    self._on_release()
                elif not _is_pressed and self._twist.pressed:
                    _is_pressed = True
                    self._on_press()
            except OSError:
                pass
            await asyncio.sleep(0.1)

    # def _click(self):
    #     now = datetime.now()
    #     if self._sw:
    #         sw_data = GPIO.input(self._sw)
    #         if sw_data == 0 and not self._is_pressed and (
    #                 not self._last_released or
    #                 self._last_released + timedelta(microseconds=30000) < now):
    #             self._on_press()
    #             self._is_pressed = True
    #             self._last_pressed = now
    #         elif sw_data != 0 and self._is_pressed:
    #             self._on_release()
    #             self._is_pressed = False
    #             self._last_released = now

    # def _click(self):
    #     if self.is_pressed:
    #         self._on_press()
    #     else:
    #         self._on_release()
