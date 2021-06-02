import asyncio
import logging
import os
import signal

from .apps.boot import boot_sequence
from .apps.pong import pong
from .apps.sketch import sketch
from .apps.snake import snake
from .apps.tetris import tetris
from .etchasketch import EtchASketch


async def menu(etch):
    etch.display_menu(
        "Choose an Activity",
        ("Pong", pong),
        ("Sketch", sketch),
        ("Snake", snake),
        ("Tetris", tetris),
        default=1,
    )


if __name__ == "__main__":

    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO").upper(),
        format="[%(levelname)s] %(message)s",
    )

    try:
        etch = EtchASketch(on_double_long_press=menu)
        loop = asyncio.get_event_loop()

        def shutdown():
            etch.clear()
            loop.stop()

        for sig in (signal.SIGINT, signal.SIGQUIT, signal.SIGTERM):
            loop.add_signal_handler(sig, shutdown)

        etch.run(boot_sequence)
        etch.start(sketch)
    except (KeyboardInterrupt, SystemExit):
        try:
            shutdown()
        except Exception as e:
            logging.exception("An error occurred while shutting down.")
