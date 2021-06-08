import asyncio
import logging
import os
import signal

from .apps.games.pong import Pong
from .apps.games.sketch import Sketch
from .apps.games.snake import Snake
from .apps.games.tetris import Tetris
from .apps.games.ticktactoe import TicTacToe
from .apps.info.compass import Compass
from .apps.info.environment import Environment
from .apps.info.map import Map
from .apps.system.boot import BootSequence
from .apps.system.camera import Camera
from .hardware.etchasketch import EtchASketch


if __name__ == "__main__":
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO").upper(),
        format="[%(levelname)s] %(message)s",
    )

    try:
        etch = EtchASketch(
            "Choose an Activity",
            ("Camera", Camera()),
            ("Compass", Compass()),
            ("Environment", Environment()),
            ("Map", Map()),
            ("Pong", Pong()),
            ("Sketch", Sketch()),
            ("Snake", Snake()),
            ("Tetris", Tetris()),
            ("Tic-Tac-Toe", TicTacToe()),
            default=5,
        )
        loop = asyncio.get_event_loop()

        def shutdown():
            etch.clear()
            loop.stop()

        for sig in (signal.SIGINT, signal.SIGQUIT, signal.SIGTERM):
            loop.add_signal_handler(sig, shutdown)

        etch.push(Sketch())
        etch.push(BootSequence())
        etch.start()
    except (KeyboardInterrupt, SystemExit):
        try:
            shutdown()
        except Exception as e:
            logging.exception("An error occurred while shutting down.")
