from time import sleep

from RPi import GPIO

from . import inputs, knob

print('Listening for knob movements...')

with inputs.Inputs() as i:
    k = knob.Knob(17, 18)
    i.register(k)
    while 1:
        print(k.value)
        sleep(0.5)
