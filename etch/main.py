import time

from RPi import GPIO

from . import accelerometer, knob

GPIO.setmode(GPIO.BCM)

try:
    left = knob.Knob(17, 6, 13, 0, 399,
                     updated=lambda v: print(f'LEFT {v}'),
                     pressed=lambda: print('LEFT PRESSED'),
                     released=lambda: print('LEFT RELEASED'))
    right = knob.Knob(16, 5, 12, 0, 299,
                      updated=lambda v: print(f'RIGHT {v}'),
                      pressed=lambda: print('RIGHT PRESSED'),
                      released=lambda: print('RIGHT RELEASED'))
    accel = accelerometer.Accelerometer(27)
    while 1:
        if left.is_long_pressed and right.is_long_pressed:
            print(f'Temp: {accel.temperature}')
            print(f'Accel: {accel.accelerometer}')
            print(f'Gyro: {accel.gyro}')
        time.sleep(0.01)
finally:
    GPIO.cleanup()
