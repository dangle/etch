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
        time.sleep(0.1)
        return self._twist.is_pressed()

    @property
    def is_long_pressed(self):
        return (self.is_pressed and
                self._twist.since_last_press(False) > 3000)

    @property
    def value(self):
        return self._twist.count

    def _poll(self):
        while 1:
            try:
                since_last_press = self._twist.since_last_press(False)
                if 0 < since_last_press < 100:
                    self._click()
                if self._twist.has_moved():
                    self._rotated()
            except OSError:
                time.sleep(0.2)

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


    def _click(self):
        if self.is_pressed:
            self._on_press()
        else:
            self._on_release()
