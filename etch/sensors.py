import time
import threading

from mpu6050 import mpu6050
from RPi import GPIO


class Sensor:

    _I2C_ADDRESS = 0x68

    def __init__(self, shaking=None):
        self._shaking = shaking or (lambda: None)
        self._sensor = mpu6050(0x68)
        self._is_shaking = False
        threading.thread(target=self._update_shaking).start()

    @property
    def is_shaking(self):
        return self._shaking

    @property
    def temp(self):
        return self._sensor.get_temp()

    @property
    def accel(self):
        data = self._sensor.get_accel_data()
        return (data['x'], data['y'], data['z'])

    @property
    def gyro(self):
        data = self._sensor.get_gyro_data()
        return (data['x'], data['y'], data['z'])

    def _update_shaking(self):
        while 1:
            time.sleep(10)
            self._is_shaking = not self._is_shaking
