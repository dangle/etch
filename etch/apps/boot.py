import time

from IT8951.constants import DisplayModes


class BootSequence:
    def __init__(self) -> None:
        self._etch = None

    async def __call__(self, etch) -> None:
        self._etch = etch
        self._display_logo()
        self._display_instructions()

    def _display_logo(self):
        self._etch.set_display_mode(DisplayModes.A2)
        self._etch.text("Etch", font="Magic", size=200, y=400, update=False)
        self._etch.text("- a -", font="Magic", size=200, y=600, update=False)
        self._etch.text("Sketch", font="Magic", size=200, y=800)
        time.sleep(5)

    def _display_instructions(self):
        pass


boot_sequence = BootSequence()
