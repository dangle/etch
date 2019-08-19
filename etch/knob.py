from RPi import GPIO


def _DO_NOTHING():
    pass


class Knob:
    pull = GPIO.PUD_UP
    bounce = 10

    def __init__(self, clk, dt, sw=None, min_value=None, max_value=None,
                 clicked=None, default=0):
        if not (clk and 0 < clk <= 27):
            raise ValueError(
                'clk pin must be supplied and be between 0 and 27.')
        if not (dt and 0 < dt <= 27):
            raise ValueError('dt pin must be supplied and be between 0 and 27.')
        self._value = default
        self._min = min_value
        self._max = max_value
        self._clk = clk
        self._dt = dt
        self._sw = sw
        self._clockwise = clockwise or _DO_NOTHING
        self._counterclockwise = counterclockwise or _DO_NOTHING
        self._clicked = clicked or _DO_NOTHING
        self._channels = [clk, dt]
        if sw:
            if not 0 < sw <= 27:
                raise ValueError(
                    'When sw pin is supplied, it must be between 0 and 27.')
            self._channels.append(sw)
        self._full_click = True

    @property
    def value(self):
        return self._value

    @property
    def channels(self):
        return self._channels

    def __call__(self, channel):
        if channel == self._clk:
            self._rotated()
        elif channel == self._sw:
            self._clicked()

    def _rotated(self):
        self._full_click = not self._full_click
        if not self._full_click:
            return
        clk_state = GPIO.input(self._clk)
        dt_state = GPIO.input(self._dt)
        if dt_state != clk_state:
            if not self._max or self._max and self._value < self._max:
                self._value = self._value + 1
        else:
            if not self._min or self._min and self._value > self._min:
                self._value = self._value - 1
