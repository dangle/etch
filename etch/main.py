from time import sleep

from RPi import GPIO

from . import inputs, knob

x = 0

def clock():
    global x
    if x < 399:
        x = x + 1
    print(x)

def counter():
    global x
    if x > 0:
        x = x - 1
    print(x)

print('Listening for knob movements...')

with inputs.Inputs() as i:
    k = knob.Knob(17, 18, clockwise=clock, counterclockwise=counter)
    i.register(k)
    while 1:
        sleep(0.5)
