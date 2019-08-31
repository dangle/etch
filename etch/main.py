import time

from RPi import GPIO

from . import sensors, knob

GPIO.setmode(GPIO.BCM)

try:
    left = knob.Knob(17, 6, 13, 0, 399,
                     on_update=lambda v: print(f'LEFT {v}'),
                     on_press=lambda: print('LEFT PRESSED'),
                     on_release=lambda: print('LEFT RELEASED'))
    right = knob.Knob(16, 5, 12, 0, 299,
                      on_update=lambda v: print(f'RIGHT {v}'),
                      on_press=lambda: print('RIGHT PRESSED'),
                      on_release=lambda: print('RIGHT RELEASED'))
    sensor = sensors.Sensor(on_shake=lambda: print('SHAKING'))
    while 1:
        if left.is_long_pressed and right.is_long_pressed:
            print('Exiting...')
            break
        time.sleep(1)
finally:
    GPIO.cleanup()
