import time

from RPi import GPIO

from . import knob

GPIO.setmode(GPIO.BCM)

try:
    left = knob.Knob(17, 4, 13, 0, 399,
                     changed=lambda v: print(f'LEFT {v}'),
                     clicked=lambda: print('LEFT CLICK'))
    right = knob.Knob(16, 5, 12, 0, 299,
                      changed=lambda v: print(f'RIGHT {v}'),
                      clicked=lambda: print('RIGHT CLICK'))
    while 1:
        time.sleep(0.01)
finally:
    GPIO.cleanup()
