from time import sleep

from IT8951.constants import DisplayModes

from .apps.pong import Pong
from .apps.sketch import sketch
from .apps.tetris import Tetris
from .etchasketch import EtchASketch


async def display_title_screen(etch):
    etch.set_display_mode(DisplayModes.DU)
    etch.text("Etch", font="Magic", size=200, y=400)
    sleep(1)
    etch.text("- a -", font="Magic", size=200, y=600)
    sleep(1)
    etch.text("Sketch", font="Magic", size=200, y=800)
    sleep(2)


try:
    etch = EtchASketch(
        on_double_long_press=lambda: etch.menu(
            "Choose an Activity",
            ("Sketch", sketch),
            ("Pong", Pong()),
            ("Tetris", Tetris()),
        )
    )

    # etch.left_knob.configure(
    #     on_update=lambda v: print(f"LEFT {v}", flush=True),
    #     on_press=lambda: print("LEFT PRESSED", flush=True),
    #     on_release=lambda: print("LEFT RELEASED", flush=True),
    # )
    # etch.right_knob.configure(
    #     on_update=lambda v: print(f"RIGHT {v}", flush=True),
    #     on_press=lambda: print("RIGHT PRESSED", flush=True),
    #     on_release=lambda: print("RIGHT RELEASED", flush=True),
    # )
    # etch.sensor.configure(on_shake=lambda: print("SHAKING"))

    etch.run(display_title_screen)
    etch.menu(
        "Choose an Activity",
        ("Sketch", sketch),
        ("Pong", Pong()),
        ("Tetris", Tetris()),
    )
except (KeyboardInterrupt, SystemExit):
    print("Exiting...")
