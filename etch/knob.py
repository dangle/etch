from RPi import GPIO


def _DO_NOTHING(*args):
    pass


class Knob:
    pull = GPIO.PUD_UP
    bounce = 10

    def __init__(self, clk, dt, sw=None, min_=None, max_=None, default=0, changed=None, clicked=None):
        if not (clk and 0 < clk <= 27):
            raise ValueError(
                'clk pin must be supplied and be between 0 and 27.')
        if not (dt and 0 < dt <= 27):
            raise ValueError('dt pin must be supplied and be between 0 and 27.')
        self._value = default
        self._min = min_
        self._max = max_
        self._clk = clk
        self._dt = dt
        self._sw = sw
        self._clicked = clicked or _DO_NOTHING
        self._changed = changed or _DO_NOTHING
        self._channels = [clk, dt]
        if sw:
            if not 0 < sw <= 27:
                raise ValueError(
                    'When sw pin is supplied, it must be between 0 and 27.')
            self._channels.append(sw)
        self._prev_channel = None
        self._clk_level = 0
        self._dt_level = 0

    @property
    def value(self):
        return self._value

    @property
    def channels(self):
        return self._channels

    def __call__(self, channel):
        if channel in (self._clk, self._dt):
            self._rotated(channel)
        elif channel == self._sw:
            self._clicked()

    def _rotated(self, channel):
        level = GPIO.input(channel)
        if channel == self._clk:
            self._clk_level = level
        else:
            self._dt_level = level
        if channel == self._prev_channel:
            return
        self._prev_channel = channel
        if channel == self._clk and level == 1:
            if self._dt_level == 1 and self._max is None or (
                    self._max is not None and self._value < self._max):
                self._value = self._value + 1
                self._changed(self._value)
        if channel == self._dt and level == 1:
            if self._clk_level == 1 and self._min is None or (
                    self._min is not None and self._value > self._min):
                self._value = self._value - 1
                self._changed(self._value)
