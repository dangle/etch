import asyncio
import contextlib
import datetime
import sys
import time

import qwiic_i2c
import qwiic_twist

from ..common import DO_NOTHING, NOT_SUPPLIED


class Knob:
    _HAS_MOVED_MASK = 0x01
    _IS_PRESSED_MASK = 0x02
    _HALF_WORD = 0x8000
    _WORD_SIZE = 16

    def __init__(self, address):
        time.sleep(0.5)
        self._last_pressed = None
        self._address = address
        self._i2c = qwiic_i2c.getI2CDriver()
        self._twist = qwiic_twist.QwiicTwist(address)
        self.reset()

        self.configure(0, sys.maxsize, DO_NOTHING, DO_NOTHING, DO_NOTHING)

        loop = asyncio.get_event_loop()
        loop.create_task(self._poll_encoder())
        loop.create_task(self._poll_button())

    def configure(
        self,
        value=NOT_SUPPLIED,
        max_=NOT_SUPPLIED,
        on_update=NOT_SUPPLIED,
        on_press=NOT_SUPPLIED,
        on_release=NOT_SUPPLIED,
    ):
        if max_ is not NOT_SUPPLIED:
            while 1:
                try:
                    self._twist.set_limit(max_)
                    break
                except OSError:
                    time.sleep(0.05)
        if value is not NOT_SUPPLIED:
            while 1:
                try:
                    self._twist.set_count(value)
                    break
                except OSError:
                    time.sleep(0.05)
        if on_update is not NOT_SUPPLIED:
            self._on_update = on_update
        if on_press is not NOT_SUPPLIED:
            self._on_press = on_press
        if on_release is not NOT_SUPPLIED:
            self._on_release = on_release

    def reset(self):
        self._twist.set_int_timeout(0x00)
        self._twist.clear_interrupts()
        self._twist.set_color(0x00, 0x00, 0x00)
        self._twist.connect_color(0x00, 0x00, 0x00)
        self._i2c.writeWord(self._address, qwiic_twist.TWIST_DIFFERENCE, 0x00)

    @contextlib.contextmanager
    def config(self, **kwargs):
        # TODO: Create a stack to push values
        _push_value = self._twist.get_count()
        _push_max = self._twist.get_limit()
        _push_on_update = self._on_update
        _push_on_press = self._on_press
        _push_on_release = self._on_release
        self.configure(**kwargs)
        try:
            yield self
        finally:
            self.configure(
                _push_value,
                _push_max,
                _push_on_update,
                _push_on_press,
                _push_on_release,
            )

    async def blink(
        self,
        red: int = 0xFF,
        green: int = 0xFF,
        blue: int = 0xFF,
        duration: int = 500,
    ):
        old_red = self._red
        old_green = self._green
        old_blue = self._blue
        try:
            self.set_color(0x00, 0x00, 0x00)
            await asyncio.sleep(duration / 1000 / 3)
            self.set_color(red, green, blue)
            await asyncio.sleep(duration / 1000 / 3)
            self.set_color(0x00, 0x00, 0x00)
            await asyncio.sleep(duration / 1000 / 3)
        finally:
            self.set_color(old_red, old_green, old_blue)

    @property
    def is_pressed(self):
        while 1:
            try:
                return bool(
                    self._i2c.readByte(self._address, qwiic_twist.TWIST_STATUS)
                    & Knob._IS_PRESSED_MASK
                )
            except OSError:
                time.sleep(0.05)

    @property
    def has_moved(self):
        while 1:
            try:
                return bool(
                    self._i2c.readByte(self._address, qwiic_twist.TWIST_STATUS)
                    & Knob._HAS_MOVED_MASK
                )
            except OSError:
                time.sleep(0.05)

    def _clear_has_moved(self):
        while 1:
            try:
                status = self._i2c.readByte(self._address, qwiic_twist.TWIST_STATUS)
                self._i2c.writeByte(
                    self._address,
                    qwiic_twist.TWIST_STATUS,
                    status ^ Knob._HAS_MOVED_MASK,
                )
                return
            except OSError:
                time.sleep(0.05)

    @property
    def is_long_pressed(self):
        while 1:
            try:
                return (
                    self._last_pressed is not None
                    and self.is_pressed
                    and datetime.datetime.now() - self._last_pressed
                    > datetime.timedelta(seconds=2)
                )
            except OSError:
                time.sleep(0.1)

    @property
    def pressed_duration(self):
        if self._last_pressed:
            return datetime.datetime.now() - self._last_pressed

    @property
    def value(self):
        return self._twist.count

    @value.setter
    def value(self, val):
        while 1:
            try:
                self._twist.set_count(val)
                return
            except OSError:
                time.sleep(0.1)

    def set_color(self, red: int, green: int, blue: int) -> None:
        self._red = red
        self._green = green
        self._blue = blue
        while 1:
            try:
                self._twist.set_color(red, green, blue)
                return
            except OSError:
                time.sleep(0.1)

    def set_connect_color(self, red: int, green: int, blue: int) -> None:
        while 1:
            try:
                self._i2c.writeBlock(
                    self._address,
                    qwiic_twist.TWIST_CONNECT_RED,
                    [red, 0x00, green, 0x00, blue, 0x00],
                )
                return
            except OSError:
                time.sleep(0.1)

    async def _poll_encoder(self):
        while 1:
            if self.has_moved:
                while 1:
                    try:
                        count = self.value
                        limit = self._twist.get_limit()
                        self._clear_has_moved()
                        diff = self._twist.get_diff(True) - Knob._HALF_WORD
                        break
                    except OSError:
                        await asyncio.sleep(0.01)
                mask = diff >> Knob._WORD_SIZE - 1
                abs_diff = diff + mask ^ mask
                sign = -(diff // abs_diff)
                val = -(abs_diff - Knob._HALF_WORD)
                try:
                    for i in range(val):
                        self._on_update((count + i * sign) % limit, sign)
                except Exception:
                    pass
            await asyncio.sleep(0.05)

    async def _poll_button(self):
        while True:
            knob_pressed = self.is_pressed
            if not self._last_pressed and knob_pressed:
                self._last_pressed = datetime.datetime.now()
                self.set_color(0xFF, 0xFF, 0xFF)
                try:
                    self._on_press()
                except Exception:
                    pass
            elif self._last_pressed and not knob_pressed:
                duration = datetime.datetime.now() - self._last_pressed
                duration_ms = int(duration.total_seconds() * 1000)
                self._last_pressed = None
                self.set_color(0x00, 0x00, 0x00)
                try:
                    self._on_release(duration_ms)
                except Exception:
                    pass
            await asyncio.sleep(0.1)
