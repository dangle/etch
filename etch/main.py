from .knob import Knob
from .sensors import Sensor


try:
    left = Knob(0x4f, 399,
                on_update=lambda v: print(f'LEFT {v}'),
                on_press=lambda: print('LEFT PRESSED'),
                on_release=lambda: print('LEFT RELEASED'))
    right = Knob(0x4e, 299,
                 on_update=lambda v: print(f'RIGHT {v}'),
                 on_press=lambda: print('RIGHT PRESSED'),
                 on_release=lambda: print('RIGHT RELEASED'))
    #sensor = Sensor(on_shake=lambda: print('SHAKING'))
    print('Listening...')
    while 1:
        if left.is_long_pressed and right.is_long_pressed:
            print('Exiting...')
            break
except (KeyboardInterrupt, SystemExit):
    print('Exiting...')
