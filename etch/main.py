from time import sleep

from inky import InkyWHAT
from RPi import GPIO

from . import inputs, knob

print('Listening for knob movements...')

class Cursor:

    def __init__(self, x, y):
        self.x = x
        self.y = y


cursor = Cursor(0, 149)
ink = InkyWHAT("black")
ink.set_border(ink.WHITE)
ink.show()

ink._luts['black'][39] = 0x00
ink._luts['black'][44] = 0x00
ink._luts['black'][49] = 0x01

dirty = False

def set_pixel(x=None, y=None):
    global cursor
    global ink
    global dirty
    if x is not None:
        cursor.x = x
    if y is not None:
        cursor.y = y
    ink.set_pixel(cursor.x, cursor.y, 1)
    dirty = True


with inputs.Inputs() as i:
    left = knob.Knob(19, 18, 12, min_=0, max_=199,
                     changed=lambda v: set_pixel(x=v * 2 - 1) ; set_pixel(x=v * 2),
                     clicked=lambda: print('LEFT CLICK'))
    i.register(left)
    right = knob.Knob(7, 16, 13, min_=0, max_=149,
                      changed=lambda v: set_pixel(y=148 - v * 2) ; set_pixel(y=149 - v * 2),
                      clicked=lambda: print('RIGHT CLICK'))
    i.register(right)
    while 1:
        if dirty:
            dirty = False
            ink.show()
        sleep(.01)
