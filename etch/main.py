from time import sleep

from inky import InkyWHAT
from RPi import GPIO

from . import inputs, knob

print('Listening for knob movements...')

class Cursor:

    def __init__(self, x, y):
        self.x = x
        self.y = y


cursor = Cursor(0, 299)
ink = InkyWHAT("black")
ink.set_border(ink.WHITE)
ink.show()


ink._luts['black'][39] = 0x00
ink._luts['black'][44] = 0x00
ink._luts['black'][49] = 0x01

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
                      changed=lambda v: set_pixel(y=299 - v),
                      clicked=lambda: print('RIGHT CLICK'))
    i.register(right)
    old_x = cursor.x
    old_y = cursor.y
    while 1:
        if old_x != cursor.x or old_y != cursor.y:
            old_x = cursor.x
            old_y = cursor.y
            ink.show()
            sleep(1)
        sleep(.1)
