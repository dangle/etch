from time import sleep

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


def clear_screen():
    global ink
    ink.set_border(ink.WHITE)
    ink.show()


def check_int(channel):
    print(f'INPUT {channel} has state: {GPIO.input(channel)}')
    print(f'INPUT 2 has state: {GPIO.input(2)}')
    print(f'INPUT 3 has state: {GPIO.input(3)}')


check_int.channels = [2, 3, 26]

#print('Listening for knob movements...')
with inputs.Inputs() as i:
    # left = knob.Knob(19, 18, 12, min_=0, max_=399,
    #                  changed=lambda v: set_pixel(x=v),
    #                  clicked=lambda: print('LEFT CLICK'))
    # i.register(left)
    # right = knob.Knob(7, 16, 13, min_=0, max_=299,
    #                   changed=lambda v: set_pixel(y=299 - v),
    #                   clicked=lambda: print('RIGHT CLICK'))
    # i.register(right)
    i.register(check_int)
    while 1:
        sleep(0.1)
        # if dirty:
        #     dirty = False
        #     ink.show()
