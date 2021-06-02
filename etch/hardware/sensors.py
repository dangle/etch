from collections import namedtuple
from datetime import datetime, timedelta
from math import sqrt
from statistics import mean
import time
import threading

from ..common import DO_NOTHING, NOT_SUPPLIED


Point = namedtuple("Point", "x y z")


class Sensor:
    _OFFSET_SAMPLES = 100
    _SHAKE_THRESHOLD = 10
    _SHAKE_DELAY = 5

    def __init__(self, address, on_shake=None):
        # self._sensor = mpu6050(self._I2C_ADDRESS)
        # self._offset = mean(
        #     self._calc_accel(*self.accelerometer) for _ in range(self._OFFSET_SAMPLES)
        # )
        # self._setup_shaking()
        self.configure(on_shake)

    def configure(self, on_shake=NOT_SUPPLIED):
        if on_shake is not NOT_SUPPLIED:
            self._on_shake = on_shake or DO_NOTHING

    @property
    def temperature(self):
        return self._sensor.get_temp()

    @property
    def accelerometer(self):
        return Point(**self._sensor.get_accel_data())

    @property
    def gyroscope(self):
        return Point(**self._sensor.get_gyro_data())

    @property
    def acceleration(self):
        x, y, z = self.accelerometer
        return abs(self._calc_accel(x, y, z) - self._offset)

    def _calc_accel(self, *args):
        return abs(sqrt(sum(i ** 2 for i in args)))

    def _setup_shaking(self):
        self._last_shake = None
        thread = threading.Thread(target=self._update_shaking)
        thread.daemon = True
        thread.start()

    def _update_shaking(self):
        while 1:
            now = datetime.now()
            if self.acceleration > self._SHAKE_THRESHOLD and (
                not self._last_shake
                or now > self._last_shake + timedelta(seconds=self._SHAKE_DELAY)
            ):
                self._last_shake = now
                self._on_shake()
            else:
                time.sleep(0.01)
