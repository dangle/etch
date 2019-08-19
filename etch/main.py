from time import sleep

from RPi import GPIO

from . import inputs, knob

print('Listening for knob movements...')

with inputs.Inputs() as i:
    k = knob.Knob(17, 18)
    i.register(k)
    old_k = k.value
    while 1:
        if k.value != old_k:
            print(k.value)
            old_k = k.value
        sleep(0.01)
