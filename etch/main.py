from RPi import GPIO

from .knob import Knob
from .sensors import Sensor


GPIO.setmode(GPIO.BCM)

try:
    left = Knob(17, 6, 12, 0, 399,
                on_update=lambda v: print(f'LEFT {v}'),
                on_press=lambda: print('LEFT PRESSED'),
                on_release=lambda: print('LEFT RELEASED'))
    right = Knob(16, 5, 13, 0, 299,
                 on_update=lambda v: print(f'RIGHT {v}'),
                 on_press=lambda: print('RIGHT PRESSED'),
                 on_release=lambda: print('RIGHT RELEASED'))
    sensor = Sensor(on_shake=lambda: print('SHAKING'))
    print('Listening...')
    while 1:
        if left.is_long_pressed and right.is_long_pressed:
            print('Exiting...')
            break
except (KeyboardInterrupt, SystemExit):
    print('Exiting...')
finally:
    GPIO.cleanup()
