from mpu6050 import mpu6050
from RPi import GPIO


class Sensor:

    _I2C_ADDRESS = 0x68

    def __init__(self):
        self._sensor = mpu6050(0x68)

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
