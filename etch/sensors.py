from collections import namedtuple
from math import sqrt
from statistics import mean
import time
import threading

from mpu6050 import mpu6050
from RPi import GPIO

from .common import DO_NOTHING, NOT_SUPPLIED


Point = namedtuple('Point', 'x y z')


class Sensor:
    _I2C_ADDRESS = 0x68
    _OFFSET_SAMPLES = 100
    _SHAKE_THRESHOLD = 12
    _SHAKE_DELAY = 5

    def __init__(self, on_shake=None):
        self._on_shake = on_shake or DO_NOTHING
        self._sensor = mpu6050(self._I2C_ADDRESS)
        self._offset = 0
        # self._offset = mean(self._calc_accel(x, y, z)
        #                     for _ in range(self._OFFSET_SAMPLES)
        #                     for x, y, z in self.accelerometer)
        self._setup_shaking()

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
        data = self.accelerometer
        return abs(self._calc_accel(data.x, data.y, data.z) - self._offset)

    def _calc_accel(self, *args):
        return abs(sqrt(sum(i ** 2 for i in args)))

    def _setup_shaking(self):
        self._stop_event = threading.Event()
        thread = threading.Thread(target=self._update_shaking)
        thread.daemon = True
        thread.start()

    def _update_shaking(self):
        while not self._stop_event.is_set():
            if self.acceleration > self._SHAKE_THRESHOLD:
                self._on_shake()
                time.sleep(self._SHAKE_DELAY)
            else:
                time.sleep(0.01)
