from .knob import Knob
from .sensors import Sensor


try:
    left = Knob(0x4f, 399,
                on_update=lambda v: print(f'LEFT {v}', flush=True),
                on_press=lambda: print('LEFT PRESSED', flush=True),
                on_release=lambda: print('LEFT RELEASED', flush=True))
    right = Knob(0x4e, 299,
                 on_update=lambda v: print(f'RIGHT {v}', flush=True),
                 on_press=lambda: print('RIGHT PRESSED', flush=True),
                 on_release=lambda: print('RIGHT RELEASED', flush=True))
    #sensor = Sensor(on_shake=lambda: print('SHAKING'))
    print('Listening...')
    while 1:
        if left.is_long_pressed and right.is_long_pressed:
            print('Exiting...')
            break
except (KeyboardInterrupt, SystemExit):
    print('Exiting...')
