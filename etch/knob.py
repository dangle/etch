import sys
import threading
import time

import qwiic_twist

from .common import DO_NOTHING, NOT_SUPPLIED


class Knob:

    def __init__(self, addr, max_=None, default=0, on_update=None,
                 on_press=None, on_release=None):
        self._twist = qwiic_twist.QwiicTwist(addr)
        self.configure(default, max_ or sys.maxint, on_update or DO_NOTHING,
                       on_press or DO_NOTHING, on_release or DO_NOTHING)
        thread = threading.Thread(target=self._poll)
        thread.daemon = True
        thread.start()

    def configure(self, value=NOT_SUPPLIED, max_=NOT_SUPPLIED,
                  on_update=NOT_SUPPLIED, on_press=NOT_SUPPLIED,
                  on_release=NOT_SUPPLIED):
        if max_ is not NOT_SUPPLIED:
            pass # TODO
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
        return (self.is_pressed and
                self._twist.since_last_press(False) > 3000)

    @property
    def value(self):
        return self._twist.count

    def _poll(self):
        _is_pressed = self.is_pressed
        while 1:
            try:
                if _is_pressed and not self._twist.is_pressed:
                    _is_pressed = False
                    self._on_release()
                elif not _is_pressed and self._twist.pressed:
                    _is_pressed = True
                    self._on_press()
                if self._twist.has_moved():
                    self._rotated()
            except OSError:
                time.sleep(0.01)

    def _rotated(self):
        current = self._twist.count
        max_ = self._twist.limit
        threadhold = max_ // 10
        if current in range(max_ - threadhold, max_ + 1) and self._last_count in range(threadhold):
            self._twist.set_count(0)
        elif current in range(threadhold) and self._last_count in range(max_ - threadhold, max_ + 1):
            self._twist.set_count(max_)
        else:
            self._last_count = current
            self._on_update(current)

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
