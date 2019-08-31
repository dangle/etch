from RPi import GPIO
from smbus import SMBus


class Accelerometer:

    _I2C_ADDRESS = 68

    def __init__(self, int_):
        self._setup_i2c()
        self._setup_interrupt(int_)

    def _setup_i2c(self):
        self._bus = SMBus(self._I2C_ADDRESS)

    def _setup_interrupt(self, int_):
        GPIO.setup(int_, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(
            int_, GPIO.RISING, callback=lambda channel: self._updated())

    def _updated(self):
        print('DATA ON ACCELEROMETER')
