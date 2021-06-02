import asyncio
import logging
import os
import signal

from .apps.games.pong import Pong
from .apps.games.sketch import sketch
from .apps.games.snake import Snake
from .apps.games.tetris import Tetris
from .apps.system.boot import BootSequence
from .hardware.etchasketch import EtchASketch


if __name__ == "__main__":
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO").upper(),
        format="[%(levelname)s] %(message)s",
    )

    try:
        etch = EtchASketch()
        loop = asyncio.get_event_loop()

        def shutdown():
            etch.clear()
            loop.stop()

        for sig in (signal.SIGINT, signal.SIGQUIT, signal.SIGTERM):
            loop.add_signal_handler(sig, shutdown)

        etch.run(BootSequence())
        etch.set_system_menu(
            "Choose an Activity",
            ("Pong", Pong()),
            ("Sketch", sketch),
            ("Snake", Snake()),
            ("Tetris", Tetris()),
            default=1,
        )
        etch.start(sketch)
    except (KeyboardInterrupt, SystemExit):
        try:
            shutdown()
        except Exception as e:
            logging.exception("An error occurred while shutting down.")
