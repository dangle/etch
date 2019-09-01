from collections import namedtuple
from math import sqrt
from statistics import mean
import time
import threading

from mpu6050 import mpu6050
from RPi import GPIO

from .common import DO_NOTHING


Point = namedtuple('Point', 'x y z')


class Sensor:
    _I2C_ADDRESS = 0x68
    _GRAVITY = mpu6050.GRAVITIY_MS2
    _OFFSET_SAMPLES = 100
    _SHAKE_THRESHOLD = 10

    def __init__(self, on_shake=None):
        self._on_shake = on_shake or DO_NOTHING
        self._sensor = mpu6050(self._I2C_ADDRESS)

        samples = (self.accelerometer for _ in range(self._OFFSET_SAMPLES))

        self._offset = mean(self._calc_accel(x, y, z) - self._GRAVITY
                            for x, y, z in samples)

        self._setup_shaking()

    @property
    def temperature(self):
        return self._sensor.get_temp()

    @property
    def accelerometer(self):
        data = self._sensor.get_accel_data()
        return Point(**data)

    @property
    def gyroscope(self):
        data = self._sensor.get_gyro_data()
        return Point(**data)

    @property
    def acceleration(self):
        data = self.accelerometer
        return abs(self._calc_accel(
                   data.x, data.y, data.z) - self._GRAVITY - self._offset)

    def _calc_accel(self, *args):
        return abs(sqrt(sum(i ** 2 for i in args)))

    def _setup_shaking(self):
        thread = threading.Thread(target=self._update_shaking)
        thread.daemon = True
        thread.start()

    def _update_shaking(self):
        while 1:
            a = self.acceleration
            if a > self._SHAKE_THRESHOLD:
                print(a)
                self._on_shake()
                time.sleep(5)
            else:
                time.sleep(0.01)
