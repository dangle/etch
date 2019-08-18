from RPi import GPIO


def _DO_NOTHING():
    pass


class Knob:

    def __init__(self, clk, dt, sw=None, clockwise=_DO_NOTHING,
                 counterclockwise=_DO_NOTHING, clicked=_DO_NOTHING):
        if not any([clockwise, counterclockwise, clicked]):
            raise ValueError('At least one callback method must be supplied.')
        if not clk or clk < 0 or clk > 27:
            raise ValueError(
                'clk pin must be supplied and be between 0 and 27.')
        if not dt or dt < 0 or dt > 27:
            raise ValueError('dt pin must be supplied and be between 0 and 27.')
        if sw:
            if sw < 0 or sw > 27:
                raise ValueError(
                    'When sw pin is supplied, it must be between 0 and 27.')
            self._channels.append(sw)
        self._clk = clk
        self._dt = dt
        self._sw = sw
        self._clockwise = clockwise
        self._counterclockwise = counterclockwise
        self._clicked = clicked
        self._channels = [clk, dt]

    @property
    def channels(self):
        return self._channels

    def __call__(self, channel):
        if channel == self._clk:
            self._rotated()
        elif channel == self._sw:
            self._clicked()

    def _rotated(self):
        clk_state = GPIO.input(self._clk)
        dt_state = GPIO.input(self._dt)
        if dt_state != clk_state:
            self._clockwise()
        else:
            self:_counterclockwise()
