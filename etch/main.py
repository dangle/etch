from time import sleep

from inky import InkyWHAT
from RPi import GPIO

from . import inputs, knob

print('Listening for knob movements...')

class Cursor:

    def __init__(self, x, y):
        self.x = x
        self.y = y


cursor = Cursor(0, 0)
ink = InkyWHAT("black")

def set_pixel(x=None, y=None):
    global cursor
    global ink
    if x is not None:
        cursor.x = x
    if y is not None:
        cursor.y = y
    ink.set_pixel(cursor.x, cursor.y, 1)


with inputs.Inputs() as i:
    left = knob.Knob(19, 18, 12, min_=0, max_=399,
                     changed=lambda v: set_pixel(x=v),
                     clicked=lambda: print('LEFT CLICK'))
    i.register(left)
    right = knob.Knob(7, 16, 13, min_=0, max_=299,
                     changed=lambda v: set_pixel(y=v),
                      clicked=lambda: print('RIGHT CLICK'))
    i.register(right)
    old_cursor = cursor
    while 1:
        if old_cursor.x != cursor.x or old_cursor.y != old_cursor.y:
            ink.show()
        sleep(1)
