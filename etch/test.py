import time

from RPi import GPIO

from . import knob

GPIO.setmode(GPIO.BCM)

try:
    left = knob.Knob(19, 18, 12, 0, 399,
                     changed=lambda v: set_pixel(x=v))
    right = knob.Knob(7, 16, 13, 0, 299,
                      changed=lambda v: set_pixel(y=299 - v))
    while 1:
        time.sleep(0.01)
finally:
    GPIO.cleanup()
