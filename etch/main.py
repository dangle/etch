from time import sleep

from RPi import GPIO

from . import inputs, knob

print('Listening for knob movements...')

with inputs.Inputs() as i:
    left = knob.Knob(19, 18, 12, min_=0, max_=400,
                     clicked=lambda: print('LEFT CLICK'))
    i.register(left)
    old_left = left.value
    right = knob.Knob(7, 16, 13, min_=0, max_=300,
                      clicked=lambda: print('RIGHT CLICK'))
    i.register(right)
    old_right = right.value
    while 1:
        if left.value != old_left:
            print(f'LEFT KNOB {left.value}')
            old_left = left.value
        if right.value != old_right:
            print(f'RIGHT KNOB {right.value}')
            old_right = right.value
        sleep(0.01)
