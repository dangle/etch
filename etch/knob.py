import asyncio
import contextlib
import datetime
import sys
import time

import qwiic_i2c
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
        self._address = address
        self._twist = qwiic_twist.QwiicTwist(address)
        self._twist.set_int_timeout(0)
        self._i2c = qwiic_i2c.getI2CDriver()
        self._twist.clear_interrupts()
        self._last_pressed = None
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

    @contextlib.contextmanager
    def configuration(self, **kwargs):
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

    @property
    def is_pressed(self):
        while 1:
            try:
                return bool(
                    self._i2c.readByte(self._address, qwiic_twist.TWIST_STATUS) & 0x02
                )
            except OSError:
                time.sleep(0.05)

    @property
    def has_moved(self):
        while 1:
            try:
                return bool(
                    self._i2c.readByte(self._address, qwiic_twist.TWIST_STATUS) & 0x01
                )
            except OSError:
                time.sleep(0.05)

    def _clear_has_moved(self):
        while 1:
            try:
                status = self._i2c.readByte(self._address, qwiic_twist.TWIST_STATUS)
                self._i2c.writeByte(
                    self._address, qwiic_twist.TWIST_STATUS, status & 0xFFFE
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

    def set_color(self, red: int, blue: int, green: int) -> None:
        while 1:
            try:
                self._twist.set_color(red, green, blue)
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
                        diff = self._twist.get_diff(True) - 0x8000
                        break
                    except OSError:
                        await asyncio.sleep(0.01)
                mask = diff >> 0x07F8 - 0x0001
                absval = (diff + mask) ^ mask
                sign = -(diff // absval)
                val = -(absval - 0x8000)
                try:
                    for i in range(val):
                        self._on_update((count + i * sign) % limit, sign)
                except Exception:
                    pass
            await asyncio.sleep(0.05)

    async def _poll_button(self):
        pressed = False
        while True:
            knob_pressed = self.is_pressed
            if not pressed and knob_pressed:
                pressed = True
                try:
                    self._last_pressed = datetime.datetime.now()
                    self._on_press()
                except Exception:
                    pass
            elif pressed and not knob_pressed:
                pressed = False
                try:
                    self._last_pressed = None
                    self._on_release()
                except Exception:
                    pass
            await asyncio.sleep(0.1)

    # TODO
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
