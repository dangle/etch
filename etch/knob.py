import time

from RPi import GPIO


class Knob:

    def __init__(self, clk, dt, sw=None, min_=None, max_=None, default=0,
                 updated=None, pressed=None, released=None):
        self._value = default
        self._min = min_
        self._max = max_
        self._clk = clk
        self._dt = dt
        self._sw = sw
        self._updated = updated or (lambda v: None)
        self._pressed = pressed or (lambda v: None)
        self._released = released or (lambda v: None)
        self._setup_rotate()
        self._setup_click()

    def _setup_rotate(self):
        GPIO.setup(self._dt, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._clk, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(
            self._clk, GPIO.RISING, callback=lambda channel: self._rotated(),
            bouncetime=10)

    def _setup_click(self):
        if self._sw:
            GPIO.setup(self._sw, GPIO.IN, GPIO.PUD_UP)
            GPIO.add_event_detect(
                self._sw, GPIO.BOTH, callback=lambda channel: self._clicked(),
                bouncetime=20)

    def _clicked(self):
        if self.sw:
            self._pressed()
        else:
            self._released()

    @property
    def value(self):
        return self._value

    @property
    def clk(self):
        return GPIO.input(self._clk)

    @property
    def dt(self):
        return GPIO.input(self._dt)

    @property
    def sw(self):
        if self._sw:
            return GPIO.input(self._sw)

    def _rotated(self):
        if self.clk == self.dt:
            if self._max is None or (
                    self._max is not None and self._value < self._max):
                self._value = self._value + 1
                self._updated(self._value)
        else:
            if self._min is None or (
                    self._min is not None and self._value > self._min):
                self._value = self._value - 1
                self._updated(self._value)
