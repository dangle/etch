import time

from RPi import GPIO

from . import knob

GPIO.setmode(GPIO.BCM)

try:
    left = knob.Knob(17, 6, 13, 0, 399,
                     updated=lambda v: print(f'LEFT {v}'),
                     pressed=lambda: print('LEFT PRESSED'),
                     released=lambda: print('RIGHT RELEASED')
                    )
    right = knob.Knob(16, 5, 12, 0, 299,
                      updated=lambda v: print(f'RIGHT {v}'),
                      pressed=lambda: print('RIGHT PRESSED'),
                      released=lambda: print('RIGHT RELEASED')
                    )
    while 1:
        time.sleep(0.01)
finally:
    GPIO.cleanup()
