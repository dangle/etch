from mpu6050 import mpu6050
from RPi import GPIO


class Accelerometer:

    _I2C_ADDRESS = 0x68

    def __init__(self, int_):
        self._sensor = mpu6050(0x68)
        self._setup_interrupt(int_)

    def _setup_interrupt(self, int_):
        GPIO.setup(int_, GPIO.IN)
        GPIO.add_event_detect(
            int_, GPIO.BOTH, callback=lambda channel: self._updated())

    @property
    def temperature(self):
        return self._sensor.get_temp()

    @property
    def accelerometer(self):
        data = self._sensor.get_accel_data()
        return (data['x'], data['y'], data['z'])

    @property
    def gyro(self):
        data = self._sensor.get_gyro_data()
        return (data['x'], data['y'], data['z'])

    def _updated(self):
        print('DATA ON ACCELEROMETER')
