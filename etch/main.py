from time import sleep

from inky import InkyWHAT
from RPi import GPIO

from . import inputs, knob

print('Listening for knob movements...')

ink = InkyWHAT("black")

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
        if left.value != old_left or right.value != old_right:
            ink.set_pixel(left.value, right.value, 1)
            ink.show()
        sleep(3)
