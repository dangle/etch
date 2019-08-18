from RPi import GPIO


def _DO_NOTHING():
    pass


class Knob:

    def __init__(self, clk, dt, sw=None, clockwise=None, counterclockwise=None,
                 clicked=None):
        if not any([clockwise, counterclockwise, clicked]):
            raise ValueError('At least one callback method must be supplied.')
        if not (clk and 0 < clk <= 27):
            raise ValueError(
                'clk pin must be supplied and be between 0 and 27.')
        if not (dt and 0 < dt <= 27):
            raise ValueError('dt pin must be supplied and be between 0 and 27.')
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
        self._prev_clk = GPIO.input(clk)
        self._prev_dt = GPIO.input(dt)

    @property
    def channels(self):
        return self._channels

    def __call__(self, channel):
        if channel == self._clk:
            self._rotated()
        elif channel == self._sw:
            self._clicked()

    def _rotated(self):
        clk = GPIO.input(self._clk)
        dt = GPIO.input(self._dt)

        if self._prev_clk == 0 and self._prev_dt == 1:
            if clk == 1 and dt == 0:
                self._clockwise()
            if clk == 1 and dt == 1:
                self._counterclockwise()

        if self._prev_clk == 0 and self._prev_dt == 0:
            if clk == 1 and dt == 0:
                self._clockwise()
            if clk == 1 and dt == 1:
                self._counterclockwise()

        if self._prev_clk == 1 and self._prev_dt == 0:
            if clk == 0 and dt == 1:
                self._clockwise()
            if clk == 0 and dt == 0:
                self._counterclockwise()

        if self._prev_clk == 1 and self._prev_dt == 1:
            if clk == 0 and dt == 1:
                self._clockwise()
            if clk == 0 and dt == 0:
                self._counterclockwise()
