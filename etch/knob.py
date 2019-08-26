import time

from ctypes import c_uint8 as uint8
from ctypes import c_uint16 as uint16

from RPi import GPIO


class Knob:

    ENCODING_TABLE = (0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0)

    def __init__(self, clk, dt, sw=None, min_=None, max_=None, default=0, changed=None, clicked=None):
        self._value = default
        self._min = min_
        self._max = max_
        self._clk = clk
        self._dt = dt
        self._sw = sw
        self._clicked = clicked or lambda v: None
        self._changed = changed or lambda v: None
        GPIO.setup(clk, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(dt, GPIO.IN, GPIO.PUD_UP)
        if sw:
            GPIO.setup(sw, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(
            clk, GPIO.RISING, callback=lambda channel: self._rotated(),
            bouncetime=10)
        self._prevNextCode = uint8(0)
        self._storage = uint16(0)

    @property
    def value(self):
        return self._value

    @property
    def clk(self):
        return GPIO.input(self._clk)

    @property
    def dt(self):
        return GPIO.input(self._dt)

    def _rotated(self):
        if self.clk != self.dt:
            if self._max is None or (
                    self._max is not None and self._value < self._max):
                self._value = self._value + 1
                self._changed(self._value)
        else:
            if self._min is None or (
                    self._min is not None and self._value > self._min):
                self._value = self._value - 1
                self._changed(self._value)
