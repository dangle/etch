import time

from RPi import GPIO


class Knob:

    def __init__(self, clk, dt, sw=None, min_=None, max_=None, default=0, changed=None, clicked=None):
        self._value = default
        self._min = min_
        self._max = max_
        self._clk = clk
        self._dt = dt
        self._sw = sw
        self._clicked = clicked
        self._changed = changed
        GPIO.setup(clk, GPIO.IN)
        GPIO.setup(dt, GPIO.IN)
        if sw:
            GPIO.setup(sw, GPIO.IN)
        GPIO.add_event_detect(clk, GPIO.RISING, callback=self._rotated,
                              bouncetime=2)

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
        time.sleep(0.002)
        if self.clk == 1 and self.dt == 0:
            while self.dt == 0:
                pass
            while self.dt == 1:
                pass
            if self._max is None or (
                    self._max is not None and self._value < self._max):
                self._value = self._value + 1
                self._changed(self._value)
        elif self.clk == 1 and self.dt == 1:
            while self.dt == 1:
                pass
            if self._min is None or (
                    self._min is not None and self._value > self._min):
                self._value = self._value - 1
                self._changed(self._value)
