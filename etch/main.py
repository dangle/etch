from time import sleep, time

from inky import InkyWHAT
from RPi import GPIO

from . import inputs, knob


class Cursor:

    def __init__(self, x, y):
        self.x = x
        self.y = y


print('Clearing the screen...')
cursor = Cursor(0, 299)
ink = InkyWHAT("black")
ink.set_border(ink.WHITE)
ink.show()

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


last_shake = time()


def clear_screen(channel):
    global ink
    global last_shake
    if time() - last_shake > 2:
        ink.set_border(ink.WHITE)
        ink.show()
        last_shake = time()
        dirty = False


clear_screen.channels = [2, 3, 26]

print('Listening for knob movements...')
with inputs.Inputs() as i:
    left = knob.Knob(17, 6, 13, 0, 399,
                     changed=lambda v: set_pixel(x=v),
                     clicked=lambda: print('LEFT CLICK'))
    right = knob.Knob(16, 5, 12, 0, 299,
                      changed=lambda v: set_pixel(y=299 - v),
                      clicked=lambda: print('RIGHT CLICK'))
    i.register(right)
    i.register(clear_screen)
    while 1:
        if dirty:
            dirty = False
            ink.show()
