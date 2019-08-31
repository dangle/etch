from datetime import datetime, timedelta

from RPi import GPIO


_NOT_SUPPLIED = object()
_DO_NOTHING = lambda *args: None


class Knob:

    def __init__(self, clk, dt, sw=None, min_=None, max_=None, default=0,
                 updated=None, pressed=None, released=None):
        self._setup_rotate(clk, dt)
        self._setup_click(sw)
        self.configure(default, min_, max_, updated or _DO_NOTHING,
                       pressed or _DO_NOTHING, released or _DO_NOTHING)

    def configure(self, value=_NOT_SUPPLIED, min_=_NOT_SUPPLIED,
                  max_=_NOT_SUPPLIED, updated=_NOT_SUPPLIED,
                  pressed=_NOT_SUPPLIED, released=_NOT_SUPPLIED):
        if value is not _NOT_SUPPLIED:
            self._value = value
        if min_ is not _NOT_SUPPLIED:
            self._min = min_
        if max_ is not _NOT_SUPPLIED:
            self._max = max_
        if updated is not _NOT_SUPPLIED:
            self._updated = updated
        if pressed is not _NOT_SUPPLIED:
            self._pressed = pressed
        if released is not _NOT_SUPPLIED:
            self._released = released

    def _setup_rotate(self, clk, dt):
        self._clk = clk
        self._dt = dt
        GPIO.setup(dt, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(clk, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(
            clk, GPIO.RISING, callback=lambda channel: self._rotated(),
            bouncetime=10)

    def _setup_click(self, sw):
        self._sw = sw
        self._is_pressed = False
        self._last_released = datetime(1, 1, 1)
        if sw:
            GPIO.setup(self._sw, GPIO.IN, GPIO.PUD_UP)
            GPIO.add_event_detect(
                sw, GPIO.BOTH, callback=lambda channel: self._click())

    def _click(self):
        now = datetime.now()
        if self._sw:
            if GPIO.input(self._sw) == 0 and not self._is_pressed and (
                    self._last_released + timedelta(microseconds=30000) < now):
                self._pressed()
                self._is_pressed = True
            elif GPIO.input(self._sw) != 0 and self._is_pressed:
                self._released()
                self._is_pressed = False
                self._last_released = now

    @property
    def is_pressed(self):
        if self._sw:
            return self._is_pressed

    @property
    def is_long_pressed(self):
        if self._sw:
            return self.pushed_duration.seconds > 1

    @property
    def pushed_duration(self):
        if not self._sw:
            return None
        if not self.is_pressed:
            return 0
        return datetime.now() - self._last_released

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
