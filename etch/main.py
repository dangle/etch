from time import sleep

from RPi import GPIO

from . import inputs, knob

print('Listening for knob movements...')

with inputs.Inputs() as i:
    k1 = knob.Knob(17, 18)
    i.register(k1)
    old_k1 = k1.value
    k2 = knob.Knob(7, 8)
    i.register(k2)
    old_k2 = k2.value
    while 1:
        if k1.value != old_k1:
            print(f'LEFT KNOB {k1.value}')
            old_k1 = k1.value
        if k2.value != old_k2:
            print(f'RIGHT KNOB {k2.value}')
            old_k2 = k2.value
        sleep(0.01)
