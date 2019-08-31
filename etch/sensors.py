from collections import NamedTuple
import time
import threading

from mpu6050 import mpu6050
from RPi import GPIO

from .common import DO_NOTHING


Point = NamedTuple('Point', 'x y z')


class Sensor:

    _I2C_ADDRESS = 0x68

    def __init__(self, on_shake=None):
        self._on_shake = on_shake or DO_NOTHING
        self._sensor = mpu6050(self._I2C_ADDRESS)
        self._setup_shaking()

    @property
    def is_shaking(self):
        return self._is_shaking

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
        return self.accelerometer

    def _setup_shaking(self):
        self._is_shaking = False
        thread = threading.Thread(target=self._update_shaking)
        thread.daemon = True
        thread.start()

    def _update_shaking(self):
        while 1:
            time.sleep(10)
            self._is_shaking = not self._is_shaking
            if self._is_shaking:
                self._on_shake()
