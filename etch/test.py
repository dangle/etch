import time

from RPi import GPIO

from . import knob

GPIO.setmode(GPIO.BCM)

try:
    left = knob.Knob(19, 18, 12, 0, 399,
                     changed=lambda v: print(f'LEFT {v}'),
                     clicked=lambda: print('LEFT CLICK'))
    right = knob.Knob(7, 16, 13, 0, 299,
                      changed=lambda v: print(f'RIGHT {v}'),
                      clicked=lambda: print('RIGHT CLICK'))
    while 1:
        time.sleep(0.01)
finally:
    GPIO.cleanup()
