import sys
import threading
import time

import qwiic_twist

from .common import DO_NOTHING, NOT_SUPPLIED


class Knob:

    def __init__(self, addr, max_=None, default=0, on_update=None,
                 on_press=None, on_release=None):
        self.configure(default, max_ or sys.maxint, on_update or DO_NOTHING,
                       on_press or DO_NOTHING, on_release or DO_NOTHING)
        self._twist = qwiic_twist.QwiicTwist(addr)
        thread = threading.Thread(target=self._poll)
        thread.daemon = True
        thread.start()

    def configure(self, value=NOT_SUPPLIED, min_=NOT_SUPPLIED,
                  max_=NOT_SUPPLIED, on_update=NOT_SUPPLIED,
                  on_press=NOT_SUPPLIED, on_release=NOT_SUPPLIED):
        if max_ is not NOT_SUPPLIED:
            self._twist.set_limit(_max)
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
        return self._twist.is_pressed()

    @property
    def is_long_pressed(self):
        return (self._twist.is_pressed() and
                self._twist.since_last_pressed(False) > 3000)

    @property
    def value(self):
        return self._twist.count

    def _poll(self):
        while 1:
            if self._twist.was_clicked():
                self._click()
            if self._twist.has_moved():
                self._rotated()
            sleep(0.1)

    def _rotated(self):
        current = self._twist.count
        if current == self._max and self._last_count == 0:
            self._twist.set_count(0)
        elif current == 0 and self._last_count == self._max:
            self._twist.set_count(self._max)
        else:
            self._last_count = current
            self._on_update(current)
