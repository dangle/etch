from etch.apps.snake import Snake
from time import sleep

from IT8951.constants import DisplayModes

from .apps.pong import pong
from .apps.sketch import sketch
from .apps.snake import snake
from .apps.tetris import tetris
from .etchasketch import EtchASketch


async def display_title_screen(etch):
    etch.set_display_mode(DisplayModes.A2)
    etch.text("Etch", font="Magic", size=200, y=400, update=False)
    etch.text("- a -", font="Magic", size=200, y=600, update=False)
    etch.text("Sketch", font="Magic", size=200, y=800)
    sleep(3)


async def menu(etch):
    etch.display_menu(
        "Choose an Activity",
        ("Sketch", sketch),
        ("Pong", pong),
        ("Tetris", tetris),
        ("Snake", snake),
    )


if __name__ == "__main__":
    try:
        etch = EtchASketch(on_double_long_press=menu)
        etch.run(display_title_screen)
        etch.start(sketch)
    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")
